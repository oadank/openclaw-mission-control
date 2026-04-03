"use client";

import Link from "next/link";
import { useTranslations } from "next-intl";

import {
  SignInButton,
  SignedIn,
  SignedOut,
  isClerkEnabled,
} from "@/auth/clerk";

const ArrowIcon = () => (
  <svg
    width="16"
    height="16"
    viewBox="0 0 16 16"
    fill="none"
    aria-hidden="true"
  >
    <path
      d="M6 12L10 8L6 4"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

export function LandingHero() {
  const t = useTranslations("landing");
  const clerkEnabled = isClerkEnabled();

  const featureLabels = [
    t("features.agentFirst"),
    t("features.approvalQueues"),
    t("features.liveSignals"),
  ];

  const boardItems = [
    t("boardItems.releaseCandidate"),
    t("boardItems.triageApprovals"),
    t("boardItems.stabilizeHandoffs"),
  ];

  const approvalItems = [
    { title: t("approvalItems.deployConfirmed"), status: "ready" as const },
    { title: t("approvalItems.copyReviewed"), status: "waiting" as const },
    { title: t("approvalItems.securitySignoff"), status: "waiting" as const },
  ];

  const signals = [
    { text: t("signals.agentDelta"), time: "Now" },
    { text: t("signals.growthOps"), time: "5m" },
    { text: t("signals.releasePipeline"), time: "12m" },
  ];

  const featureCards = [
    {
      title: t("featureCards.boardsTitle"),
      description: t("featureCards.boardsDescription"),
    },
    {
      title: t("featureCards.approvalsTitle"),
      description: t("featureCards.approvalsDescription"),
    },
    {
      title: t("featureCards.signalsTitle"),
      description: t("featureCards.signalsDescription"),
    },
    {
      title: t("featureCards.auditTitle"),
      description: t("featureCards.auditDescription"),
    },
  ];

  const openBoardsLabel = t("openBoards");
  const createBoardLabel = t("createBoard");
  const viewBoardsLabel = t("viewBoards");

  return (
    <>
      <section className="hero">
        <div className="hero-content">
          <div className="hero-label">{t("heroLabel")}</div>
          <h1>
            {t("titlePrefix")}
            <span className="hero-highlight">{t("titleHighlight")}</span>
            <br />
            {t("titleSuffix")}
          </h1>
          <p>{t("description")}</p>

          <div className="hero-actions">
            <SignedOut>
              {clerkEnabled ? (
                <>
                  <SignInButton
                    mode="modal"
                    forceRedirectUrl="/boards"
                    signUpForceRedirectUrl="/boards"
                  >
                    <button type="button" className="btn-large primary">
                      {openBoardsLabel} <ArrowIcon />
                    </button>
                  </SignInButton>
                  <SignInButton
                    mode="modal"
                    forceRedirectUrl="/boards/new"
                    signUpForceRedirectUrl="/boards/new"
                  >
                    <button type="button" className="btn-large secondary">
                      {createBoardLabel}
                    </button>
                  </SignInButton>
                </>
              ) : (
                <>
                  <Link href="/boards" className="btn-large primary">
                    {openBoardsLabel} <ArrowIcon />
                  </Link>
                  <Link href="/boards/new" className="btn-large secondary">
                    {createBoardLabel}
                  </Link>
                </>
              )}
            </SignedOut>

            <SignedIn>
              <Link href="/boards" className="btn-large primary">
                {openBoardsLabel} <ArrowIcon />
              </Link>
              <Link href="/boards/new" className="btn-large secondary">
                {createBoardLabel}
              </Link>
            </SignedIn>
          </div>

          <div className="hero-features">
            {featureLabels.map((label) => (
              <div key={label} className="hero-feature">
                <div className="feature-icon">✓</div>
                <span>{label}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="command-surface">
          <div className="surface-header">
            <div className="surface-title">{t("commandSurface")}</div>
            <div className="live-indicator">
              <div className="live-dot" />
              {t("live")}
            </div>
          </div>
          <div className="surface-subtitle">
            <h3>{t("surfaceTitle")}</h3>
            <p>{t("surfaceDescription")}</p>
          </div>
          <div className="metrics-row">
            {[
              { label: t("metrics.boards"), value: "12" },
              { label: t("metrics.agents"), value: "08" },
              { label: t("metrics.tasks"), value: "46" },
            ].map((item) => (
              <div key={item.label} className="metric">
                <div className="metric-value">{item.value}</div>
                <div className="metric-label">{item.label}</div>
              </div>
            ))}
          </div>
          <div className="surface-content">
            <div className="content-section">
              <h4>{t("boardProgress")}</h4>
              {boardItems.map((title) => (
                <div key={title} className="status-item">
                  <div className="status-icon progress">⊙</div>
                  <div className="status-item-content">
                    <div className="status-item-title">{title}</div>
                  </div>
                </div>
              ))}
            </div>

            <div className="content-section">
              <h4>{t("approvalsPending")}</h4>
              {approvalItems.map((item) => (
                <div key={item.title} className="approval-item">
                  <div className="approval-title">{item.title}</div>
                  <div className={`approval-badge ${item.status}`}>
                    {item.status}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div
            style={{
              padding: "2rem",
              borderTop: "1px solid var(--neutral-200)",
            }}
          >
            <div className="content-section">
              <h4>{t("signalsUpdated")}</h4>
              {signals.map((signal) => (
                <div key={signal.text} className="signal-item">
                  <div className="signal-text">{signal.text}</div>
                  <div className="signal-time">{signal.time}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="features-section" id="capabilities">
        <div className="features-grid">
          {featureCards.map((feature, idx) => (
            <div key={feature.title} className="feature-card">
              <div className="feature-number">
                {String(idx + 1).padStart(2, "0")}
              </div>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="cta-section">
        <div className="cta-content">
          <h2>{t("ctaTitle")}</h2>
          <p>{t("ctaDescription")}</p>
          <div className="cta-actions">
            <SignedOut>
              {clerkEnabled ? (
                <>
                  <SignInButton
                    mode="modal"
                    forceRedirectUrl="/boards/new"
                    signUpForceRedirectUrl="/boards/new"
                  >
                    <button type="button" className="btn-large white">
                      {createBoardLabel}
                    </button>
                  </SignInButton>
                  <SignInButton
                    mode="modal"
                    forceRedirectUrl="/boards"
                    signUpForceRedirectUrl="/boards"
                  >
                    <button type="button" className="btn-large outline">
                      {viewBoardsLabel}
                    </button>
                  </SignInButton>
                </>
              ) : (
                <>
                  <Link href="/boards/new" className="btn-large white">
                    {createBoardLabel}
                  </Link>
                  <Link href="/boards" className="btn-large outline">
                    {viewBoardsLabel}
                  </Link>
                </>
              )}
            </SignedOut>

            <SignedIn>
              <Link href="/boards/new" className="btn-large white">
                {createBoardLabel}
              </Link>
              <Link href="/boards" className="btn-large outline">
                {viewBoardsLabel}
              </Link>
            </SignedIn>
          </div>
        </div>
      </section>
    </>
  );
}
