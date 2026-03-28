"""Service layer for per-agent model assignment, fallback policy, and recommendation state.

Design principles:
- Admin intent (manual selections) is never silently overwritten by recommendation refresh.
- Invalid overrides are preserved in storage and surfaced via validation fields.
- Effective config is recomputed after every write; clients receive the same aggregate shape.
- Full-list replacement is used for manual fallback overrides to reduce ordering/race bugs.
- Recommendation state is stored separately from admin intent to support stale detection.
"""

from __future__ import annotations

import json
import logging
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app.core.time import utcnow

logger = logging.getLogger(__name__)

# OpenClaw agent config root (configurable via env)
_OPENCLAW_STATE_DIR = Path(
    os.environ.get("OPENCLAW_STATE_DIR", os.path.expanduser("~/.openclaw"))
)
from app.models.agents import Agent
from app.models.gateway_model_profiles import GatewayModelProfileDefaults
from app.models.model_controls import (
    AgentModelFallbackEntry,
    AgentModelProfile,
    AgentModelRecommendationRun,
)
from app.schemas.model_controls import (
    AgentModelAssignmentRead,
    FallbackEntry,
    FallbackSection,
    PatchPrimaryRequest,
    PrimarySection,
    PutFallbackOverrideRequest,
    RecommendationSection,
    RegenerateRecommendationRequest,
    ValidationIssue,
    ValidationSection,
)

if TYPE_CHECKING:
    from sqlmodel.ext.asyncio.session import AsyncSession


# ---------------------------------------------------------------------------
# In-memory model catalog (replaces static _ACTIVE_MODEL_IDS stub)
# ---------------------------------------------------------------------------
# Structured catalog derived from catalog-seed.json.  Provides validation,
# display metadata, capability filtering, and the data for the catalog
# endpoint in one place.  A future iteration may back this by a DB table
# or external catalog service; the in-memory structure ensures a clean
# upgrade path.

from app.schemas.model_controls import CatalogEntry

# Canonical catalog — sourced strictly from OpenClaw gateway config
# (`~/.openclaw/agents/mc-gateway-<id>/agent/models.json`).
# Only models present in the active gateway are listed.
# Phantom families (gemini, ag/claude-*-thinking, codex-xhigh/high/low)
# that were never in gateway config have been removed.
_MODEL_CATALOG: list[CatalogEntry] = [
    # --- Premium tier ---
    CatalogEntry(
        model_id="9router/cc/claude-opus-4-6",
        display_name="Claude Opus 4.6",
        provider_family="9router",
        routing_family="cc",
        family="claude",
        tier="premium",
        capability_class="reasoning",
        role_fit=["lead", "coding", "review"],
        supports_primary=True,
        supports_fallback=True,
        status="active",
        fallback_candidates=["9router/cc/claude-sonnet-4-6", "9router/cx/gpt-5.4"],
    ),
    CatalogEntry(
        model_id="9router/cx/gpt-5.4",
        display_name="GPT 5.4 (Codex)",
        provider_family="9router",
        routing_family="cx",
        family="gpt",
        tier="premium",
        capability_class="reasoning",
        role_fit=["lead", "coding", "worker", "review"],
        supports_primary=True,
        supports_fallback=True,
        status="active",
        fallback_candidates=["9router/cx/gpt-5.3-codex", "9router/cc/claude-sonnet-4-6"],
    ),
    CatalogEntry(
        model_id="9router/gh/gpt-5.4",
        display_name="GPT 5.4 (GitHub)",
        provider_family="9router",
        routing_family="gh",
        family="gpt",
        tier="premium",
        capability_class="reasoning",
        role_fit=["lead", "coding", "worker", "review"],
        supports_primary=True,
        supports_fallback=True,
        status="active",
        fallback_candidates=["9router/cx/gpt-5.3-codex", "9router/gh/gpt-5-mini"],
    ),
    # --- Balanced tier ---
    CatalogEntry(
        model_id="9router/cc/claude-sonnet-4-6",
        display_name="Claude Sonnet 4.6",
        provider_family="9router",
        routing_family="cc",
        family="claude",
        tier="balanced",
        capability_class="general",
        role_fit=["lead", "worker", "review"],
        supports_primary=True,
        supports_fallback=True,
        status="active",
        fallback_candidates=["9router/cc/claude-opus-4-6", "9router/cx/gpt-5.3-codex"],
    ),
    CatalogEntry(
        model_id="9router/cx/gpt-5.3-codex",
        display_name="GPT 5.3 Codex",
        provider_family="9router",
        routing_family="cx",
        family="gpt",
        tier="specialized",
        capability_class="coding",
        role_fit=["coding", "worker", "automation"],
        supports_primary=True,
        supports_fallback=True,
        status="active",
        fallback_candidates=["9router/cx/gpt-5.3-codex-none", "9router/cx/gpt-5.3-codex-spark"],
    ),
    CatalogEntry(
        model_id="9router/cx/gpt-5.3-codex-none",
        display_name="GPT 5.3 Codex (No Reasoning)",
        provider_family="9router",
        routing_family="cx",
        family="gpt",
        tier="balanced",
        capability_class="coding",
        role_fit=["coding", "worker"],
        supports_primary=True,
        supports_fallback=True,
        status="active",
        fallback_candidates=["9router/cx/gpt-5.3-codex-spark", "9router/cx/gpt-5.3-codex"],
    ),
    # --- Budget tier ---
    CatalogEntry(
        model_id="9router/gh/gpt-5-mini",
        display_name="GPT 5 Mini (GitHub)",
        provider_family="9router",
        routing_family="gh",
        family="gpt",
        tier="budget",
        capability_class="fast",
        role_fit=["automation", "worker"],
        supports_primary=True,
        supports_fallback=True,
        status="active",
        fallback_candidates=["9router/cx/gpt-5.3-codex-spark", "9router/cc/claude-sonnet-4-6"],
    ),
    CatalogEntry(
        model_id="9router/cx/gpt-5.3-codex-spark",
        display_name="GPT 5.3 Codex Spark",
        provider_family="9router",
        routing_family="cx",
        family="gpt",
        tier="budget",
        capability_class="coding",
        role_fit=["automation", "coding", "worker"],
        supports_primary=True,
        supports_fallback=True,
        status="active",
        fallback_candidates=["9router/cx/gpt-5.3-codex-none", "9router/gh/gpt-5-mini"],
    ),
]

# Derived lookup sets for fast validation
_ACTIVE_MODEL_IDS: set[str] = {m.model_id for m in _MODEL_CATALOG if m.status == "active"}
_CATALOG_INDEX: dict[str, CatalogEntry] = {m.model_id: m for m in _MODEL_CATALOG}


def _is_valid_model(model_id: str) -> bool:
    return model_id in _ACTIVE_MODEL_IDS


def get_model_catalog(
    *,
    role_fit: str | None = None,
    capability_class: str | None = None,
    supports_primary: bool | None = None,
    supports_fallback: bool | None = None,
) -> list[CatalogEntry]:
    """Return filtered model catalog entries.

    All filters are optional; omitting a filter includes all values for that axis.
    Only active models are returned.
    """
    results: list[CatalogEntry] = []
    for entry in _MODEL_CATALOG:
        if entry.status != "active":
            continue
        if role_fit and role_fit not in entry.role_fit:
            continue
        if capability_class and entry.capability_class != capability_class:
            continue
        if supports_primary is not None and entry.supports_primary != supports_primary:
            continue
        if supports_fallback is not None and entry.supports_fallback != supports_fallback:
            continue
        results.append(entry)
    return results


# ---------------------------------------------------------------------------
# Effective-config assembly helpers
# ---------------------------------------------------------------------------


def _assemble_effective_fallback(
    generated: list[AgentModelFallbackEntry],
    manual: list[AgentModelFallbackEntry],
    override_mode: str,
    effective_primary: str | None,
) -> tuple[list[FallbackEntry], str, str, bool, str | None]:
    """Assemble effective fallback list from generated + manual entries.

    Returns:
        (effective_entries, source_label, status_label, has_effective_fallback,
         no_valid_fallback_reason)
    """

    def _to_read(e: AgentModelFallbackEntry) -> FallbackEntry:
        return FallbackEntry(
            model_id=e.model_id,
            position=e.position,
            trigger_type=e.trigger_type,
            source=e.source,
            enabled=e.enabled,
            constraints=e.constraints,
        )

    gen_entries = [_to_read(e) for e in sorted(generated, key=lambda x: x.position) if e.enabled]
    man_entries = [_to_read(e) for e in sorted(manual, key=lambda x: x.position) if e.enabled]

    if override_mode == "replace":
        raw = man_entries
        source = "manual_only"
    elif override_mode == "append":
        raw = gen_entries + man_entries
        source = "generated_plus_manual" if (gen_entries and man_entries) else (
            "generated_only" if gen_entries else "manual_only"
        )
    else:  # none
        raw = gen_entries
        source = "generated_only"

    # Deduplicate: first occurrence wins. Also remove entries matching effective primary.
    seen: set[str] = set()
    if effective_primary:
        seen.add(effective_primary)
    effective: list[FallbackEntry] = []
    for entry in raw:
        if not _is_valid_model(entry.model_id):
            continue
        if entry.model_id in seen:
            continue
        seen.add(entry.model_id)
        effective.append(entry)

    # Rebuild positions
    for i, e in enumerate(effective):
        e = e.model_copy(update={"position": i})
        effective[i] = e

    has_effective = len(effective) > 0

    # Determine status
    if not has_effective:
        if not raw:
            status = "empty_allowed" if override_mode == "none" else "empty_invalid"
        else:
            status = "empty_invalid"
        reason = "No valid fallback entries remain after validation and deduplication."
    elif override_mode == "none":
        status = "generated_only"
        reason = None
    elif override_mode == "replace":
        status = "manual_only"
        reason = None
    else:
        status = "merged"
        reason = None

    return effective, source, status, has_effective, reason


def _compute_validation(
    profile: AgentModelProfile,
    effective_primary: str | None,
    has_effective_fallback: bool,
    fallback_status: str,
) -> ValidationSection:
    issues: list[ValidationIssue] = []
    warnings: list[ValidationIssue] = []

    # Primary validity
    if profile.primary_selection_mode == "manual" and profile.primary_model_id:
        if not _is_valid_model(profile.primary_model_id):
            issues.append(ValidationIssue(
                code="primary_model_invalid",
                severity="error",
                scope="primary",
                message=(
                    f"Manually selected primary model '{profile.primary_model_id}' "
                    "is not in the active catalog. Please update your selection."
                ),
            ))

    # Recommended model references stale/phantom ID
    if (
        profile.recommended_primary_model_id
        and not _is_valid_model(profile.recommended_primary_model_id)
    ):
        issues.append(ValidationIssue(
            code="recommended_model_invalid",
            severity="error",
            scope="recommendation",
            message=(
                f"Recommended model '{profile.recommended_primary_model_id}' "
                "is not in the active catalog. Regenerate the recommendation."
            ),
        ))

    # No effective primary
    if effective_primary is None:
        issues.append(ValidationIssue(
            code="no_effective_primary",
            severity="error",
            scope="primary",
            message="No effective primary model is available. Assign a model or wait for recommendation.",
        ))

    # No effective fallback
    if not has_effective_fallback and fallback_status == "empty_invalid":
        issues.append(ValidationIssue(
            code="no_effective_fallback",
            severity="error",
            scope="fallback",
            message="No valid fallback remains after validation and deduplication.",
        ))

    # Stale recommendation warning
    if profile.recommendation_status == "stale":
        warnings.append(ValidationIssue(
            code="recommendation_stale",
            severity="warning",
            scope="recommendation",
            message="The model recommendation is stale. Consider regenerating to get an updated suggestion.",
        ))

    # Determine config_status
    if issues:
        config_status = "invalid"
    elif warnings or profile.recommendation_status in ("stale", "error"):
        config_status = "stale" if profile.recommendation_status == "stale" else "degraded"
    elif effective_primary is None:
        config_status = "degraded"
    elif profile.config_status == "pending":
        config_status = "pending"
    else:
        config_status = "valid"

    return ValidationSection(
        config_status=config_status,
        blocking_issues=issues,
        warnings=warnings,
    )


def _resolve_effective_primary(profile: AgentModelProfile) -> str | None:
    if profile.primary_selection_mode == "manual" and profile.primary_model_id:
        if _is_valid_model(profile.primary_model_id):
            return profile.primary_model_id
    # Only use recommendation if it references a valid catalog model
    rec = profile.recommended_primary_model_id
    if rec and _is_valid_model(rec):
        return rec
    return None


def _primary_source(profile: AgentModelProfile, effective: str | None) -> str:
    if profile.primary_selection_mode == "manual" and profile.primary_model_id:
        return "manual"
    if effective == profile.recommended_primary_model_id:
        return "recommended"
    return "none"


# ---------------------------------------------------------------------------
# Service
# ---------------------------------------------------------------------------


class AgentModelAssignmentService:
    """Handles reads and writes for per-agent model assignment."""

    def __init__(self, session: "AsyncSession") -> None:
        self._session = session

    async def _exec_scalars(self, stmt: object):
        """Execute a mapped select and return ORM scalar rows."""
        result = await self._session.execute(stmt)  # type: ignore[arg-type]
        return result.scalars()

    # -----------------------------------------------------------------------
    # Internal helpers
    # -----------------------------------------------------------------------

    async def _get_or_create_profile(self, agent_id: UUID) -> AgentModelProfile:
        """Return the existing profile for an agent or bootstrap a new pending one."""
        stmt = select(AgentModelProfile).where(AgentModelProfile.agent_id == agent_id)
        result = await self._exec_scalars(stmt)
        profile = result.one_or_none()
        if profile is None:
            profile = AgentModelProfile(
                agent_id=agent_id,
                primary_selection_mode="auto",
                fallback_override_mode="none",
                recommendation_status="pending",
                config_status="pending",
            )
            self._session.add(profile)
            await self._session.flush()
        return profile

    async def _get_profile(self, agent_id: UUID) -> AgentModelProfile:
        stmt = select(AgentModelProfile).where(AgentModelProfile.agent_id == agent_id)
        result = await self._exec_scalars(stmt)
        profile = result.one_or_none()
        if profile is None:
            raise NoResultFound(f"No model profile for agent {agent_id}")
        return profile

    async def _get_gateway_profile_defaults(
        self, agent_id: UUID
    ) -> GatewayModelProfileDefaults | None:
        """Look up gateway model profile defaults for an agent's gateway.

        Returns None if the agent has no gateway or the gateway has no
        profile defaults configured.
        """
        # Get agent's gateway_id
        agent_stmt = select(Agent.gateway_id).where(Agent.id == agent_id)
        agent_result = await self._session.execute(agent_stmt)
        gateway_id = agent_result.scalar_one_or_none()
        if gateway_id is None:
            return None

        # Get gateway profile defaults
        defaults_stmt = select(GatewayModelProfileDefaults).where(
            GatewayModelProfileDefaults.gateway_id == gateway_id
        )
        defaults_result = await self._session.execute(defaults_stmt)
        return defaults_result.scalars().first()

    async def _get_fallback_entries(
        self, profile_id: UUID
    ) -> tuple[list[AgentModelFallbackEntry], list[AgentModelFallbackEntry]]:
        stmt = select(AgentModelFallbackEntry).where(
            AgentModelFallbackEntry.agent_model_profile_id == profile_id
        )
        result = await self._exec_scalars(stmt)
        all_entries = list(result.all())
        generated = [e for e in all_entries if e.source == "generated"]
        manual = [e for e in all_entries if e.source == "manual"]
        return generated, manual

    def _build_aggregate(
        self,
        profile: AgentModelProfile,
        generated_entries: list[AgentModelFallbackEntry],
        manual_entries: list[AgentModelFallbackEntry],
    ) -> AgentModelAssignmentRead:
        effective_primary = _resolve_effective_primary(profile)

        # Assemble fallback
        (
            effective_fallback,
            fallback_source,
            fallback_status,
            has_effective_fallback,
            no_valid_fallback_reason,
        ) = _assemble_effective_fallback(
            generated_entries,
            manual_entries,
            profile.fallback_override_mode,
            effective_primary,
        )

        # Validation
        validation = _compute_validation(
            profile,
            effective_primary,
            has_effective_fallback,
            fallback_status,
        )

        # Primary section
        primary = PrimarySection(
            manual_model_id=profile.primary_model_id,
            recommended_model_id=profile.recommended_primary_model_id,
            effective_model_id=effective_primary,
            source=_primary_source(profile, effective_primary),
            selection_mode=profile.primary_selection_mode,
            is_valid=not any(
                i.scope == "primary" and i.severity == "error"
                for i in validation.blocking_issues
            ),
            recommendation_changed=False,  # Phase 2: derive from run history
        )

        # Fallback section
        gen_read = [
            FallbackEntry(
                model_id=e.model_id,
                position=e.position,
                trigger_type=e.trigger_type,
                source=e.source,
                enabled=e.enabled,
                constraints=e.constraints,
            )
            for e in sorted(generated_entries, key=lambda x: x.position)
        ]
        man_read = [
            FallbackEntry(
                model_id=e.model_id,
                position=e.position,
                trigger_type=e.trigger_type,
                source=e.source,
                enabled=e.enabled,
                constraints=e.constraints,
            )
            for e in sorted(manual_entries, key=lambda x: x.position)
        ]
        fallback = FallbackSection(
            override_mode=profile.fallback_override_mode,
            generated_entries=gen_read,
            manual_entries=man_read,
            effective_entries=effective_fallback,
            source=fallback_source,
            status=fallback_status,
            has_effective_fallback=has_effective_fallback,
            no_valid_fallback_reason=no_valid_fallback_reason,
        )

        # Recommendation section
        recommendation = RecommendationSection(
            status=profile.recommendation_status,
            generated_at=profile.recommendation_generated_at,
            version=profile.recommendation_version,
            explanation=profile.recommendation_explanation or {},
        )

        return AgentModelAssignmentRead(
            agent_id=profile.agent_id,
            board_id=profile.board_id,
            role_key=profile.role_key,
            primary=primary,
            fallback=fallback,
            recommendation=recommendation,
            validation=validation,
            updated_at=profile.updated_at,
        )

    async def _update_effective_and_validation(self, profile: AgentModelProfile) -> None:
        """Recompute and persist effective_primary_model_id and config_status."""
        generated_entries, manual_entries = await self._get_fallback_entries(profile.id)
        effective_primary = _resolve_effective_primary(profile)
        (_, _, fallback_status, has_effective_fallback, _) = _assemble_effective_fallback(
            generated_entries, manual_entries, profile.fallback_override_mode, effective_primary
        )
        validation = _compute_validation(
            profile, effective_primary, has_effective_fallback, fallback_status
        )
        profile.effective_primary_model_id = effective_primary
        profile.config_status = validation.config_status
        profile.effective_config_updated_at = utcnow()
        profile.updated_at = utcnow()
        self._session.add(profile)

    # -----------------------------------------------------------------------
    # Runtime sync — config-file bridge to OpenClaw gateway
    # -----------------------------------------------------------------------

    async def _resolve_agent_dir(self, agent_id: UUID) -> str | None:
        """Resolve the OpenClaw agent directory name from the agent's session ID.

        Session IDs follow the pattern: agent:{agent_dir}:main
        Agent dirs follow: mc-{agent_id} (workers) or lead-{board_id} (leads).
        """
        stmt = select(Agent.openclaw_session_id).where(Agent.id == agent_id)
        result = await self._session.execute(stmt)
        session_id = result.scalar_one_or_none()
        if not session_id:
            return None
        # Parse: "agent:mc-xxxx:main" → "mc-xxxx"
        parts = session_id.split(":")
        if len(parts) >= 2:
            return parts[1]
        return None

    def _sync_model_to_runtime(
        self,
        agent_dir: str,
        effective_model_id: str,
    ) -> RuntimeSyncResult:
        """Write effective model into the agent's entry in openclaw.json.

        Per-agent model override lives at:
            openclaw.json → agents.list[n].model.primary

        This is the config path OpenClaw gateway reads at session start.
        MC DB write is always the source of truth; this is best-effort.
        """
        from app.schemas.model_controls import RuntimeSyncResult

        config_path = _OPENCLAW_STATE_DIR / "openclaw.json"

        try:
            if not config_path.exists():
                return RuntimeSyncResult(
                    status="skipped",
                    error=f"Gateway config not found: {config_path}",
                    target_path=str(config_path),
                )
        except OSError as exc:
            logger.warning("Cannot stat openclaw.json: %s", exc)
            return RuntimeSyncResult(
                status="failed",
                error=f"Cannot access config: {exc}",
                target_path=str(config_path),
            )

        try:
            config = json.loads(config_path.read_text())
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            logger.error("Corrupt openclaw.json: %s", exc)
            return RuntimeSyncResult(
                status="failed",
                error=f"Corrupt config: {exc}",
                target_path=str(config_path),
            )
        except OSError as exc:
            logger.warning("Cannot read openclaw.json: %s", exc)
            return RuntimeSyncResult(
                status="failed",
                error=f"Read error: {exc}",
                target_path=str(config_path),
            )

        # Find the agent entry in agents.list by agent_dir id
        agents_list = config.get("agents", {}).get("list", [])
        agent_entry = None
        for entry in agents_list:
            if entry.get("id") == agent_dir:
                agent_entry = entry
                break

        if agent_entry is None:
            return RuntimeSyncResult(
                status="skipped",
                error=f"Agent '{agent_dir}' not found in openclaw.json agents.list",
                target_path=str(config_path),
            )

        # Set agents.list[n].model.primary to the effective model
        existing_model = agent_entry.get("model")
        if isinstance(existing_model, dict):
            agent_entry["model"]["primary"] = effective_model_id
        elif isinstance(existing_model, str):
            # Simple string model → upgrade to object with primary
            agent_entry["model"] = {"primary": effective_model_id}
        else:
            # No model set yet → create
            agent_entry["model"] = {"primary": effective_model_id}

        # Write in-place to preserve file ownership (container user may differ
        # from host user; atomic rename would change ownership).
        try:
            config_path.write_text(json.dumps(config, indent=2))
        except OSError as exc:
            logger.warning("Failed to write openclaw.json: %s", exc)
            return RuntimeSyncResult(
                status="failed",
                error=f"Write error: {exc}",
                target_path=str(config_path),
            )

        now = utcnow()
        logger.info(
            "Runtime sync: %s → %s (path=%s, field=agents.list[].model.primary)",
            agent_dir, effective_model_id, config_path,
        )
        return RuntimeSyncResult(
            status="synced",
            synced_at=now,
            target_path=str(config_path),
            next_effective="next_session_start",
        )

    async def _sync_effective_to_runtime(
        self, agent_id: UUID, effective_model_id: str | None
    ) -> RuntimeSyncResult | None:
        """Resolve agent dir and sync effective model to gateway runtime."""
        from app.schemas.model_controls import RuntimeSyncResult

        if not effective_model_id:
            return RuntimeSyncResult(
                status="skipped",
                error="No effective model to sync",
            )

        agent_dir = await self._resolve_agent_dir(agent_id)
        if not agent_dir:
            return RuntimeSyncResult(
                status="skipped",
                error="Agent has no openclaw_session_id",
            )

        return self._sync_model_to_runtime(agent_dir, effective_model_id)

    # -----------------------------------------------------------------------
    # Public API
    # -----------------------------------------------------------------------

    async def get_assignment(self, agent_id: UUID) -> AgentModelAssignmentRead:
        """Return aggregate model assignment for an agent, bootstrapping profile if absent."""
        profile = await self._get_or_create_profile(agent_id)
        await self._session.commit()
        generated_entries, manual_entries = await self._get_fallback_entries(profile.id)
        return self._build_aggregate(profile, generated_entries, manual_entries)

    async def patch_primary(
        self,
        agent_id: UUID,
        payload: PatchPrimaryRequest,
    ) -> AgentModelAssignmentRead:
        """Set or clear manual primary model selection.

        - Does not overwrite recommendation state.
        - Recomputes effective config and validation after mutation.
        """
        profile = await self._get_or_create_profile(agent_id)

        if payload.selection_mode == "manual":
            if not payload.model_id:
                raise ValueError("model_id is required when selection_mode=manual")
            if not _is_valid_model(payload.model_id):
                raise ValueError(f"Invalid model_id: {payload.model_id}")
            profile.primary_model_id = payload.model_id
            profile.primary_selection_mode = "manual"
        else:  # auto
            profile.primary_model_id = None
            profile.primary_selection_mode = "auto"

        await self._update_effective_and_validation(profile)
        await self._session.commit()

        # Sync effective model to OpenClaw gateway runtime (best-effort)
        sync_result = await self._sync_effective_to_runtime(
            agent_id, profile.effective_primary_model_id
        )

        generated_entries, manual_entries = await self._get_fallback_entries(profile.id)
        result = self._build_aggregate(profile, generated_entries, manual_entries)
        result.runtime_sync = sync_result
        return result

    async def put_fallback_override(
        self,
        agent_id: UUID,
        payload: PutFallbackOverrideRequest,
    ) -> AgentModelAssignmentRead:
        """Full-list replacement for manual fallback entries.

        Replaces all existing manual fallback rows atomically.
        Does not touch generated entries.
        """
        profile = await self._get_or_create_profile(agent_id)

        # Delete existing manual entries
        stmt = select(AgentModelFallbackEntry).where(
            AgentModelFallbackEntry.agent_model_profile_id == profile.id,
            AgentModelFallbackEntry.source == "manual",
        )
        result = await self._exec_scalars(stmt)
        for entry in result.all():
            await self._session.delete(entry)

        # Insert new manual entries
        new_entries: list[AgentModelFallbackEntry] = []
        for item in payload.entries:
            entry = AgentModelFallbackEntry(
                agent_model_profile_id=profile.id,
                source="manual",
                position=item.position,
                model_id=item.model_id,
                trigger_type=item.trigger_type,
                constraints=item.constraints,
                enabled=item.enabled,
            )
            self._session.add(entry)
            new_entries.append(entry)

        # Update override mode
        profile.fallback_override_mode = payload.override_mode
        profile.fallback_override_updated_at = utcnow()

        await self._update_effective_and_validation(profile)
        await self._session.commit()

        # Refresh to pick up persisted manual entries
        await self._session.refresh(profile)
        generated_entries, manual_entries = await self._get_fallback_entries(profile.id)
        return self._build_aggregate(profile, generated_entries, manual_entries)

    async def regenerate_recommendation(
        self,
        agent_id: UUID,
        payload: RegenerateRecommendationRequest,
    ) -> AgentModelAssignmentRead:
        """Recompute recommended primary and generated fallback policy.

        - Does not overwrite valid manual overrides.
        - Updates recommendation_status and generated fallback entries.
        - Appends a recommendation run history record.
        """
        profile = await self._get_or_create_profile(agent_id)

        # --- Role-fit → profile mapping policy ---
        # Maps agent role to preferred gateway profile slot, with fallback chain:
        #   1. Preferred profile slot (coder for coding, budget for automation)
        #   2. General profile slot (baseline)
        #   3. Hardcoded catalog-aware defaults (last resort)
        #
        # Only explicit user-selected values and "default" sentinel are used.
        # No guessing — if a profile slot is unset (null), it is skipped.

        ROLE_TO_PROFILE_SLOT: dict[str, str] = {
            "coding": "coder",
            "automation": "budget",
            # All others (lead, worker, review) map to general
        }
        # Defaults use only models present in gateway config.
        HARDCODED_DEFAULTS: dict[str, str] = {
            "lead": "9router/cc/claude-opus-4-6",
            "coding": "9router/cx/gpt-5.4",
            "worker": "9router/cc/claude-sonnet-4-6",
            "automation": "9router/gh/gpt-5-mini",
            "review": "9router/cc/claude-opus-4-6",
        }
        HARDCODED_FALLBACKS: dict[str, list[str]] = {
            "lead": ["9router/cx/gpt-5.4", "9router/cc/claude-sonnet-4-6"],
            "coding": ["9router/cx/gpt-5.3-codex", "9router/cc/claude-sonnet-4-6"],
            "worker": ["9router/cx/gpt-5.3-codex-spark", "9router/gh/gpt-5-mini"],
            "automation": ["9router/cx/gpt-5.3-codex-spark", "9router/cc/claude-sonnet-4-6"],
            "review": ["9router/cc/claude-sonnet-4-6", "9router/cx/gpt-5.4"],
        }

        role = profile.role_key if profile.role_key in HARDCODED_DEFAULTS else "worker"
        preferred_slot = ROLE_TO_PROFILE_SLOT.get(role, "general")

        # Look up gateway profile defaults for this agent
        gateway_defaults = await self._get_gateway_profile_defaults(agent_id)

        # Resolve recommendation through profile precedence chain
        recommended_primary: str | None = None
        recommendation_source: str = "hardcoded_default"
        explanation_reasons: list[dict] = []

        if gateway_defaults is not None:
            # Try preferred profile slot first
            slot_model_id = getattr(gateway_defaults, f"{preferred_slot}_model_id", None)
            if slot_model_id is not None and slot_model_id != "default":
                if _is_valid_model(slot_model_id):
                    recommended_primary = slot_model_id
                    recommendation_source = f"gateway_profile_{preferred_slot}"
                    explanation_reasons.append({
                        "code": "profile_match",
                        "label": f"Selected from gateway '{preferred_slot}' profile",
                        "weight": 1.0,
                        "profile_slot": preferred_slot,
                        "model_id": slot_model_id,
                    })
            elif slot_model_id == "default":
                # "default" sentinel — use hardcoded default for this role
                recommended_primary = HARDCODED_DEFAULTS[role]
                recommendation_source = f"gateway_profile_{preferred_slot}_default_sentinel"
                explanation_reasons.append({
                    "code": "default_sentinel",
                    "label": f"Gateway '{preferred_slot}' profile set to 'default', using role-based default",
                    "weight": 1.0,
                    "profile_slot": preferred_slot,
                })

            # Fallback to general profile if preferred slot didn't resolve
            if recommended_primary is None and preferred_slot != "general":
                general_model_id = gateway_defaults.general_model_id
                if general_model_id is not None and general_model_id != "default":
                    if _is_valid_model(general_model_id):
                        recommended_primary = general_model_id
                        recommendation_source = "gateway_profile_general_fallback"
                        explanation_reasons.append({
                            "code": "fallback_to_general",
                            "label": f"'{preferred_slot}' profile unset, fell back to 'general' profile",
                            "weight": 0.8,
                            "profile_slot": "general",
                            "model_id": general_model_id,
                        })
                elif general_model_id == "default":
                    recommended_primary = HARDCODED_DEFAULTS[role]
                    recommendation_source = "gateway_profile_general_default_sentinel"
                    explanation_reasons.append({
                        "code": "general_default_sentinel",
                        "label": "General profile set to 'default', using role-based default",
                        "weight": 0.8,
                    })

            # Fallback: general profile for roles that map directly to general
            if recommended_primary is None and preferred_slot == "general":
                general_model_id = gateway_defaults.general_model_id
                if general_model_id is not None and general_model_id != "default":
                    if _is_valid_model(general_model_id):
                        recommended_primary = general_model_id
                        recommendation_source = "gateway_profile_general"
                        explanation_reasons.append({
                            "code": "profile_match",
                            "label": "Selected from gateway 'general' profile",
                            "weight": 1.0,
                            "profile_slot": "general",
                            "model_id": general_model_id,
                        })
                elif general_model_id == "default":
                    recommended_primary = HARDCODED_DEFAULTS[role]
                    recommendation_source = "gateway_profile_general_default_sentinel"
                    explanation_reasons.append({
                        "code": "default_sentinel",
                        "label": "General profile set to 'default', using role-based default",
                        "weight": 1.0,
                    })

        # Last resort: hardcoded catalog-aware defaults
        if recommended_primary is None:
            recommended_primary = HARDCODED_DEFAULTS[role]
            recommendation_source = "hardcoded_default"
            explanation_reasons.append({
                "code": "role_default",
                "label": f"No gateway profile configured, using hardcoded default for role '{role}'",
                "weight": 0.5,
            })

        # Build fallback list from catalog-aware defaults
        # (Future: derive from gateway profiles + catalog fallback_candidates)
        recommended_fallbacks = HARDCODED_FALLBACKS.get(role, HARDCODED_FALLBACKS["worker"])

        now = utcnow()
        version = f"profile-v1/catalog-{now.date()}"

        # Update profile
        profile.recommended_primary_model_id = recommended_primary
        profile.recommendation_status = "fresh"
        profile.recommendation_generated_at = now
        profile.recommendation_version = version
        # Build explanation summary
        cat_entry = _CATALOG_INDEX.get(recommended_primary)
        model_display = cat_entry.display_name if cat_entry else recommended_primary
        summary_parts = [
            f"Recommended '{model_display}' for role '{role}'",
            f"via {recommendation_source.replace('_', ' ')}.",
        ]
        if preferred_slot != "general" and recommendation_source.startswith("gateway_profile_general"):
            summary_parts.append(
                f"'{preferred_slot}' profile was unset, fell back to 'general'."
            )

        profile.recommendation_explanation = {
            "summary": " ".join(summary_parts),
            "reasons": explanation_reasons,
            "tradeoffs": [],
            "inputs": {
                "role_key": role,
                "preferred_profile_slot": preferred_slot,
                "recommendation_source": recommendation_source,
                "reason": payload.reason,
                "gateway_profiles_configured": gateway_defaults is not None,
            },
        }

        # Replace generated fallback entries
        stmt = select(AgentModelFallbackEntry).where(
            AgentModelFallbackEntry.agent_model_profile_id == profile.id,
            AgentModelFallbackEntry.source == "generated",
        )
        result = await self._exec_scalars(stmt)
        for entry in result.all():
            await self._session.delete(entry)
        await self._session.flush()

        for i, model_id in enumerate(recommended_fallbacks):
            entry = AgentModelFallbackEntry(
                agent_model_profile_id=profile.id,
                source="generated",
                position=i,
                model_id=model_id,
                trigger_type="unavailable",
                enabled=True,
                generation_version=version,
            )
            self._session.add(entry)

        # Append history record
        run = AgentModelRecommendationRun(
            agent_id=agent_id,
            board_id=profile.board_id,
            role_key=role,
            catalog_version="seed-v1",
            policy_version="profile-v1",
            status="success",
            recommended_primary_model_id=recommended_primary,
            fallback_plan=[
                {"model_id": m, "position": i} for i, m in enumerate(recommended_fallbacks)
            ],
            explanation=profile.recommendation_explanation,
            signals={"role_key": role, "reason": payload.reason},
            generated_at=now,
        )
        self._session.add(run)

        await self._update_effective_and_validation(profile)
        await self._session.commit()

        # Sync effective model to OpenClaw gateway runtime (best-effort)
        sync_result = await self._sync_effective_to_runtime(
            agent_id, profile.effective_primary_model_id
        )

        generated_entries, manual_entries = await self._get_fallback_entries(profile.id)
        result = self._build_aggregate(profile, generated_entries, manual_entries)
        result.runtime_sync = sync_result
        return result
