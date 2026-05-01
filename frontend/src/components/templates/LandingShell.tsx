"use client";

import { useTranslations } from "next-intl";

import Link from "next/link";
import type { ReactNode } from "react";

import {
  SignInButton,
  SignedIn,
  SignedOut,
  isClerkEnabled,
} from "@/auth/clerk";

import { UserMenu } from "@/components/organisms/UserMenu";

export function LandingShell({ children }: { children: ReactNode }) {
  const t = useTranslations("landing");
  const clerkEnabled = isClerkEnabled();

  return (
    <div className="landing-enterprise">
      <nav className="landing-nav" aria-label="Primary navigation">
        <div className="nav-container">
          <Link href="/" className="logo-section" aria-label="OpenClaw home">
            <div className="logo-icon" aria-hidden="true">
              OC
            </div>
            <div className="logo-text">
              <div className="logo-name">OpenClaw</div>
              <div className="logo-tagline">Mission Control</div>
            </div>
          </Link>

          <div className="nav-links">
            <Link href="#capabilities">{t("capabilities")}</Link>
            <Link href="/boards">{t("boards")}</Link>
            <Link href="/activity">{t("activity")}</Link>
            <Link href="/gateways">{t("gateways")}</Link>
          </div>

          <div className="nav-cta">
            <SignedOut>
              {clerkEnabled ? (
                <>
                  <SignInButton
                    mode="modal"
                    forceRedirectUrl="/onboarding"
                    signUpForceRedirectUrl="/onboarding"
                  >
                    <button type="button" className="btn-secondary">
                      {t('sign_in')}
                    </button>
                  </SignInButton>
                  <SignInButton
                    mode="modal"
                    forceRedirectUrl="/onboarding"
                    signUpForceRedirectUrl="/onboarding"
                  >
                    <button type="button" className="btn-primary">
                      {t('start_free_trial')}
                    </button>
                  </SignInButton>
                </>
              ) : (
                <>
                  <Link href="/boards" className="btn-secondary">
                    {t("viewBoards")}
                  </Link>
                  <Link href="/onboarding" className="btn-primary">
                    {t('get_started')}
                  </Link>
                </>
              )}
            </SignedOut>

            <SignedIn>
              <Link href="/boards/new" className="btn-secondary">
                {t("createBoard")}
              </Link>
              <Link href="/boards" className="btn-primary">
                {t("openBoards")}
              </Link>
              <UserMenu />
            </SignedIn>
          </div>
        </div>
      </nav>

      <main>{children}</main>

      <footer className="landing-footer">
        <div className="footer-content">
          <div className="footer-brand">
            <h3>{t('openclaw')}</h3>
            <p>{t("footerDesc")}</p>
            <div className="footer-tagline">{t("realtimeVisibility")}</div>
          </div>

          <div className="footer-column">
            <h4>{t('product')}</h4>
            <div className="footer-links">
              <Link href="#capabilities">{t("capabilities")}</Link>
              <Link href="/boards">{t("boards")}</Link>
              <Link href="/activity">{t("activity")}</Link>
              <Link href="/dashboard">{t("dashboard")}</Link>
            </div>
          </div>

          <div className="footer-column">
            <h4>{t('platform')}</h4>
            <div className="footer-links">
              <Link href="/gateways">{t("gateways")}</Link>
              <Link href="/agents">{t("agents")}</Link>
              <Link href="/dashboard">{t("dashboard")}</Link>
            </div>
          </div>

          <div className="footer-column">
            <h4>{t('access')}</h4>
            <div className="footer-links">
              <SignedOut>
                {clerkEnabled ? (
                  <>
                    <SignInButton
                      mode="modal"
                      forceRedirectUrl="/onboarding"
                      signUpForceRedirectUrl="/onboarding"
                    >
                      <button type="button">{t("sign_in")}</button>
                    </SignInButton>
                    <SignInButton
                      mode="modal"
                      forceRedirectUrl="/onboarding"
                      signUpForceRedirectUrl="/onboarding"
                    >
                      <button type="button">{t("create_account")}</button>
                    </SignInButton>
                  </>
                ) : (
                  <>
                    <Link href="/boards">{t("openBoards")}</Link>
                    <Link href="/onboarding">{t("get_started")}</Link>
                  </>
                )}
              </SignedOut>
              <SignedIn>
                <Link href="/boards">{t("openBoards")}</Link>
                <Link href="/boards/new">{t("createBoard")}</Link>
                <Link href="/dashboard">{t("dashboard")}</Link>
              </SignedIn>
            </div>
          </div>
        </div>

        <div className="footer-bottom">
          <div className="footer-copyright">
            {t('copyright')}
          </div>
          <div className="footer-bottom-links">
            <Link href="#capabilities">{t("capabilities")}</Link>
            <Link href="/boards">{t("boards")}</Link>
            <Link href="/activity">{t("activity")}</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
