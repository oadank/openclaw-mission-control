"use client";

import { AuthMode } from "@/auth/mode";

let localToken: string | null = null;
const STORAGE_KEY = "mc_local_auth_token";

export function isLocalAuthMode(): boolean {
  return process.env.NEXT_PUBLIC_AUTH_MODE === AuthMode.Local;
}

export function setLocalAuthToken(token: string): void {
  localToken = token;
  if (typeof window === "undefined") return;
  try {
    window.sessionStorage.setItem(STORAGE_KEY, token);
  } catch {
    // Ignore storage failures (private mode / policy).
  }
}

export function getLocalAuthToken(): string | null {
  if (localToken) return localToken;
  // Check for preset token from environment variable
  const presetToken = getPresetLocalAuthToken();
  if (presetToken) {
    localToken = presetToken;
    return presetToken;
  }
  if (typeof window === "undefined") return null;
  try {
    const stored = window.sessionStorage.getItem(STORAGE_KEY);
    if (stored) {
      localToken = stored;
      return stored;
    }
  } catch {
    // Ignore storage failures (private mode / policy).
  }
  return null;
}

// Get preset token from environment variable or hardcoded fallback
const HARDCODED_TOKEN = "46f90dff116b9a60a1d21b5d403b781c366e566114313bd6-6308fee6aed16bb491aff66fa3a70d81";

export function getPresetLocalAuthToken(): string | null {
  // Check process.env first (if built with the variable)
  if (process.env.NEXT_PUBLIC_PRESET_LOCAL_AUTH_TOKEN) {
    return process.env.NEXT_PUBLIC_PRESET_LOCAL_AUTH_TOKEN;
  }
  // Fallback to hardcoded token
  return HARDCODED_TOKEN;
}

export function clearLocalAuthToken(): void {
  localToken = null;
  if (typeof window === "undefined") return;
  try {
    window.sessionStorage.removeItem(STORAGE_KEY);
  } catch {
    // Ignore storage failures (private mode / policy).
  }
}
