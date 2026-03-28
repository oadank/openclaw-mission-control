"""Contract + regression tests for dynamic model catalog correctness.

Task: 343a4ba4 — prevent recurrence of catalog/source drift.

Tests cover:
1. Catalog returns only active models with required metadata fields
2. Negative test: unknown/fabricated namespaces are not in catalog
3. Alias/ID consistency: model_ids in catalog match those accepted by assignment endpoints
4. Filtering contract: role_fit, capability_class, supports_primary, supports_fallback
5. Smoke test: assignment endpoints reject model_ids not in catalog
"""

from __future__ import annotations

import os
import httpx
import pytest

BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:8000")
# Use agent token for dual-auth endpoints
AUTH_TOKEN = os.environ.get("TEST_AUTH_TOKEN", "test-token-placeholder")
HEADERS = {"Authorization": f"Bearer {AUTH_TOKEN}", "Content-Type": "application/json"}

CATALOG_URL = f"{BASE_URL}/api/v1/mission-control/agents/model-catalog"

# Expected active model_id set (source of truth: OpenClaw gateway config)
# Populate from your deployment's active model catalog
EXPECTED_MODEL_IDS = {
    "9router/cc/claude-opus-4-6",
    "9router/cc/claude-sonnet-4-6",
    "9router/cx/gpt-5.4",
    "9router/cx/gpt-5.3-codex",
    "9router/cx/gpt-5.3-codex-none",
    "9router/cx/gpt-5.3-codex-spark",
    "9router/gh/gpt-5-mini",
    "9router/gh/gpt-5.4",
}

# Known-bad namespaces that must NOT appear in catalog
# Note: 9router/cc/ and 9router/gh/ are valid gateway routing families
KNOWN_BAD_NAMESPACES = [
    "9router/ag/",    # phantom ag namespace (never in gateway config)
    "openai/",        # raw provider prefix, not 9router canonical
    "anthropic/",     # raw provider prefix
    "google/",        # raw provider prefix
]

REQUIRED_CATALOG_FIELDS = {
    "model_id", "display_name", "provider_family", "routing_family",
    "family", "tier", "capability_class", "role_fit",
    "supports_primary", "supports_fallback", "status",
}

VALID_TIERS = {"premium", "specialized", "balanced", "budget"}
VALID_CAPABILITY_CLASSES = {"reasoning", "general", "coding", "fast"}
VALID_ROLES = {"lead", "worker", "coding", "automation", "review"}
VALID_STATUSES = {"active", "deprecated", "unavailable"}


@pytest.fixture(scope="module")
def catalog_response():
    """Fetch the full catalog once for the test module."""
    resp = httpx.get(CATALOG_URL, headers=HEADERS, timeout=10)
    assert resp.status_code == 200, f"Catalog fetch failed: {resp.status_code} {resp.text}"
    data = resp.json()
    assert "models" in data
    assert "total" in data
    return data


@pytest.fixture(scope="module")
def catalog_models(catalog_response):
    return catalog_response["models"]


@pytest.fixture(scope="module")
def catalog_model_ids(catalog_models):
    return {m["model_id"] for m in catalog_models}


# =========================================================================
# 1. Contract: catalog returns only active models with correct metadata
# =========================================================================


class TestCatalogContract:
    def test_catalog_returns_expected_model_set(self, catalog_model_ids):
        """Catalog model_id set must exactly match expected active models."""
        assert catalog_model_ids == EXPECTED_MODEL_IDS, (
            f"Catalog drift detected.\n"
            f"  Extra: {catalog_model_ids - EXPECTED_MODEL_IDS}\n"
            f"  Missing: {EXPECTED_MODEL_IDS - catalog_model_ids}"
        )

    def test_total_matches_model_count(self, catalog_response, catalog_models):
        """Response total must match actual models array length."""
        assert catalog_response["total"] == len(catalog_models)

    def test_all_models_have_required_fields(self, catalog_models):
        """Every catalog entry must have all required fields present and non-null."""
        for model in catalog_models:
            missing = REQUIRED_CATALOG_FIELDS - set(model.keys())
            assert not missing, (
                f"Model {model.get('model_id', '?')} missing fields: {missing}"
            )
            for field in REQUIRED_CATALOG_FIELDS:
                assert model[field] is not None, (
                    f"Model {model['model_id']} has null {field}"
                )

    def test_all_models_are_active(self, catalog_models):
        """Only active models should appear in the catalog response."""
        for model in catalog_models:
            assert model["status"] == "active", (
                f"Non-active model in catalog: {model['model_id']} status={model['status']}"
            )

    def test_tier_values_are_valid(self, catalog_models):
        for model in catalog_models:
            assert model["tier"] in VALID_TIERS, (
                f"Invalid tier for {model['model_id']}: {model['tier']}"
            )

    def test_capability_class_values_are_valid(self, catalog_models):
        for model in catalog_models:
            assert model["capability_class"] in VALID_CAPABILITY_CLASSES, (
                f"Invalid capability_class for {model['model_id']}: {model['capability_class']}"
            )

    def test_role_fit_values_are_valid(self, catalog_models):
        for model in catalog_models:
            assert isinstance(model["role_fit"], list)
            assert len(model["role_fit"]) > 0, (
                f"Empty role_fit for {model['model_id']}"
            )
            for role in model["role_fit"]:
                assert role in VALID_ROLES, (
                    f"Invalid role '{role}' for {model['model_id']}"
                )

    def test_model_ids_follow_canonical_format(self, catalog_models):
        """All model_ids must follow 9router/{routing_family}/... format."""
        for model in catalog_models:
            mid = model["model_id"]
            assert mid.startswith("9router/"), (
                f"Non-canonical model_id: {mid}"
            )
            parts = mid.split("/")
            assert len(parts) >= 3, f"Malformed model_id: {mid}"
            assert parts[1] == model["routing_family"], (
                f"routing_family mismatch for {mid}: "
                f"path says '{parts[1]}', field says '{model['routing_family']}'"
            )

    def test_display_names_are_unique(self, catalog_models):
        names = [m["display_name"] for m in catalog_models]
        assert len(names) == len(set(names)), (
            f"Duplicate display_names: {[n for n in names if names.count(n) > 1]}"
        )

    def test_model_ids_are_unique(self, catalog_models):
        ids = [m["model_id"] for m in catalog_models]
        assert len(ids) == len(set(ids)), "Duplicate model_ids in catalog"


# =========================================================================
# 2. Negative test: unknown namespaces must not leak into catalog
# =========================================================================


class TestNamespaceLeakage:
    def test_no_known_bad_namespaces(self, catalog_model_ids):
        """Catalog must not contain models from known-bad namespaces."""
        for ns in KNOWN_BAD_NAMESPACES:
            leaked = [mid for mid in catalog_model_ids if mid.startswith(ns)]
            assert not leaked, (
                f"Namespace leakage: {ns} models in catalog: {leaked}"
            )

    def test_no_raw_provider_prefixes(self, catalog_model_ids):
        """No model should use raw provider names instead of 9router canonical refs."""
        raw_prefixes = ["openai/", "anthropic/", "google/", "azure/", "aws/"]
        for prefix in raw_prefixes:
            leaked = [mid for mid in catalog_model_ids if mid.startswith(prefix)]
            assert not leaked, f"Raw provider prefix leaked: {prefix} → {leaked}"


# =========================================================================
# 3. Filtering contract
# =========================================================================


class TestCatalogFiltering:
    def test_filter_by_role_fit(self):
        """Filtering by role_fit returns only models with that role."""
        for role in ["lead", "coding", "worker", "automation", "review"]:
            resp = httpx.get(
                CATALOG_URL, params={"role_fit": role}, headers=HEADERS, timeout=10
            )
            assert resp.status_code == 200
            data = resp.json()
            for model in data["models"]:
                assert role in model["role_fit"], (
                    f"Model {model['model_id']} returned for role_fit={role} "
                    f"but role_fit is {model['role_fit']}"
                )
            assert data["filters_applied"]["role_fit"] == role

    def test_filter_by_capability_class(self):
        """Filtering by capability_class returns only matching models."""
        for cap in ["reasoning", "general", "coding", "fast"]:
            resp = httpx.get(
                CATALOG_URL, params={"capability_class": cap}, headers=HEADERS, timeout=10
            )
            assert resp.status_code == 200
            data = resp.json()
            for model in data["models"]:
                assert model["capability_class"] == cap, (
                    f"Model {model['model_id']} returned for capability_class={cap} "
                    f"but has {model['capability_class']}"
                )

    def test_filter_supports_primary(self):
        resp = httpx.get(
            CATALOG_URL, params={"supports_primary": "true"}, headers=HEADERS, timeout=10
        )
        assert resp.status_code == 200
        for model in resp.json()["models"]:
            assert model["supports_primary"] is True

    def test_filter_supports_fallback(self):
        resp = httpx.get(
            CATALOG_URL, params={"supports_fallback": "true"}, headers=HEADERS, timeout=10
        )
        assert resp.status_code == 200
        for model in resp.json()["models"]:
            assert model["supports_fallback"] is True

    def test_combined_filters(self):
        """Composing filters narrows correctly."""
        resp = httpx.get(
            CATALOG_URL,
            params={"role_fit": "lead", "capability_class": "reasoning"},
            headers=HEADERS,
            timeout=10,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] > 0, "Expected at least one lead+reasoning model"
        for model in data["models"]:
            assert "lead" in model["role_fit"]
            assert model["capability_class"] == "reasoning"

    def test_nonexistent_role_returns_empty(self):
        resp = httpx.get(
            CATALOG_URL, params={"role_fit": "nonexistent_role"}, headers=HEADERS, timeout=10
        )
        assert resp.status_code == 200
        assert resp.json()["total"] == 0
        assert resp.json()["models"] == []

    def test_unfiltered_returns_all_active(self, catalog_response):
        """No filters returns the full active catalog."""
        assert catalog_response["total"] == len(EXPECTED_MODEL_IDS)


# =========================================================================
# 4. Alias/ID consistency: catalog IDs match assignment endpoint validation
# =========================================================================


class TestCatalogAssignmentConsistency:
    """Verify catalog model_ids are accepted by the assignment PATCH endpoint
    and non-catalog IDs are rejected (400)."""

    # Use a known agent_id — bootstrap will create a profile if needed
    AGENT_ID = "aff19090-9335-400a-8573-3ab5aa20f662"

    def _assignment_url(self, suffix=""):
        return (
            f"{BASE_URL}/api/v1/mission-control/agents/"
            f"{self.AGENT_ID}/model-assignment{suffix}"
        )

    def test_catalog_model_accepted_as_primary(self, catalog_model_ids):
        """A model_id from the catalog must be accepted by PATCH primary."""
        # Pick the first catalog model
        model_id = sorted(catalog_model_ids)[0]
        resp = httpx.patch(
            self._assignment_url("/primary"),
            json={"selection_mode": "manual", "model_id": model_id},
            headers=HEADERS,
            timeout=10,
        )
        assert resp.status_code == 200, (
            f"Catalog model {model_id} rejected by assignment: {resp.status_code} {resp.text}"
        )
        data = resp.json()
        assert data["primary"]["manual_model_id"] == model_id
        assert data["primary"]["effective_model_id"] == model_id

    def test_non_catalog_model_rejected_as_primary(self):
        """A model_id NOT in the catalog must be rejected with 400."""
        fake_id = "9router/fake/nonexistent-model-v99"
        resp = httpx.patch(
            self._assignment_url("/primary"),
            json={"selection_mode": "manual", "model_id": fake_id},
            headers=HEADERS,
            timeout=10,
        )
        assert resp.status_code == 400, (
            f"Non-catalog model {fake_id} was not rejected: {resp.status_code} {resp.text}"
        )

    def test_ag_namespace_model_rejected(self):
        """9router/ag/ phantom models should be rejected (not in catalog)."""
        resp = httpx.patch(
            self._assignment_url("/primary"),
            json={"selection_mode": "manual", "model_id": "9router/ag/claude-opus-4-6-thinking"},
            headers=HEADERS,
            timeout=10,
        )
        assert resp.status_code == 400, (
            f"ag-namespace phantom model was accepted but should not be in catalog: {resp.status_code}"
        )

    def test_cc_namespace_model_accepted(self):
        """9router/cc/ models are valid gateway models and should be accepted."""
        resp = httpx.patch(
            self._assignment_url("/primary"),
            json={"selection_mode": "manual", "model_id": "9router/cc/claude-sonnet-4-6"},
            headers=HEADERS,
            timeout=10,
        )
        assert resp.status_code == 200, (
            f"cc-namespace model was rejected but should be valid: {resp.status_code} {resp.text}"
        )

    def test_gh_namespace_model_accepted(self):
        """9router/gh/ models are valid gateway models and should be accepted."""
        resp = httpx.patch(
            self._assignment_url("/primary"),
            json={"selection_mode": "manual", "model_id": "9router/gh/gpt-5-mini"},
            headers=HEADERS,
            timeout=10,
        )
        assert resp.status_code == 200, (
            f"gh-namespace model was rejected but should be valid: {resp.status_code} {resp.text}"
        )

    def test_reset_to_auto_after_tests(self):
        """Clean up: reset primary to auto mode."""
        resp = httpx.patch(
            self._assignment_url("/primary"),
            json={"selection_mode": "auto", "model_id": None},
            headers=HEADERS,
            timeout=10,
        )
        assert resp.status_code == 200


# =========================================================================
# 5. Fallback candidate consistency
# =========================================================================


class TestFallbackCandidateConsistency:
    def test_fallback_candidates_reference_valid_catalog_ids(self, catalog_models, catalog_model_ids):
        """Every fallback_candidate must itself be a valid catalog model_id."""
        for model in catalog_models:
            candidates = model.get("fallback_candidates", [])
            for candidate in candidates:
                assert candidate in catalog_model_ids, (
                    f"Model {model['model_id']} has fallback_candidate "
                    f"'{candidate}' which is not in the catalog"
                )

    def test_no_self_referencing_fallback(self, catalog_models):
        """A model must not list itself as a fallback candidate."""
        for model in catalog_models:
            candidates = model.get("fallback_candidates", [])
            assert model["model_id"] not in candidates, (
                f"Model {model['model_id']} lists itself as fallback candidate"
            )
