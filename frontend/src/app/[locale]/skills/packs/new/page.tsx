"use client";

export const dynamic = "force-dynamic";

import { useRouter } from "next/navigation";
import { useTranslations } from "next-intl";

import { useAuth } from "@/auth/clerk";

import { ApiError } from "@/api/mutator";
import { useCreateSkillPackApiV1SkillsPacksPost } from "@/api/generated/skills/skills";
import { MarketplaceSkillForm } from "@/components/skills/MarketplaceSkillForm";
import { DashboardPageLayout } from "@/components/templates/DashboardPageLayout";
import { useOrganizationMembership } from "@/lib/use-organization-membership";

export default function NewSkillPackPage() {
  const t = useTranslations("skillPacksPage");
  const router = useRouter();
  const { isSignedIn } = useAuth();
  const { isAdmin } = useOrganizationMembership(isSignedIn);

  const createMutation = useCreateSkillPackApiV1SkillsPacksPost<ApiError>();

  return (
    <DashboardPageLayout
      signedOut={{
        message: "Sign in to add skill packs.",
        forceRedirectUrl: "/skills/packs/new",
      }}
      title={t("addPack")}
      description={t("addPackDesc")}
      isAdmin={isAdmin}
      adminOnlyMessage="Only organization owners and admins can manage skill packs."
      stickyHeader
    >
      <MarketplaceSkillForm
        sourceLabel="Pack URL"
        nameLabel="Pack name (optional)"
        descriptionLabel="Pack description (optional)"
        descriptionPlaceholder="Short summary shown in the packs list."
        branchLabel="Pack branch (optional)"
        branchPlaceholder="main"
        showBranch
        requiredUrlMessage="Pack URL is required."
        invalidUrlMessage="Pack URL must be a GitHub repository URL (https://github.com/<owner>/<repo>)."
        submitLabel={t("addPack")}
        submittingLabel="Adding..."
        isSubmitting={createMutation.isPending}
        onCancel={() => router.push("/skills/packs")}
        onSubmit={async (values) => {
          const result = await createMutation.mutateAsync({
            data: {
              source_url: values.sourceUrl,
              name: values.name || undefined,
              description: values.description || undefined,
              branch: values.branch || "main",
              metadata: {},
            },
          });
          if (result.status !== 200) {
            throw new Error("Unable to add pack.");
          }
          router.push("/skills/packs");
        }}
      />
    </DashboardPageLayout>
  );
}
