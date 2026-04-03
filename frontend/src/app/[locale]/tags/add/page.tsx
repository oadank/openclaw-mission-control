"use client";

export const dynamic = "force-dynamic";

import { useRouter } from "next/navigation";
import { useTranslations } from "next-intl";

import { useAuth } from "@/auth/clerk";

import { ApiError } from "@/api/mutator";
import { useCreateTagApiV1TagsPost } from "@/api/generated/tags/tags";
import { TagForm } from "@/components/tags/TagForm";
import { DashboardPageLayout } from "@/components/templates/DashboardPageLayout";
import { useOrganizationMembership } from "@/lib/use-organization-membership";

export default function NewTagPage() {
  const t = useTranslations("tagsPage");
  const router = useRouter();
  const { isSignedIn } = useAuth();
  const { isAdmin } = useOrganizationMembership(isSignedIn);

  const createMutation = useCreateTagApiV1TagsPost<ApiError>({
    mutation: {
      retry: false,
    },
  });

  return (
    <DashboardPageLayout
      signedOut={{
        message: "Sign in to create tags.",
        forceRedirectUrl: "/tags/add",
        signUpForceRedirectUrl: "/tags/add",
      }}
      title={t("createTag")}
      description={t("createTagDesc")}
      isAdmin={isAdmin}
      adminOnlyMessage="Only organization owners and admins can manage tags."
    >
      <TagForm
        isSubmitting={createMutation.isPending}
        submitLabel={t("createTag")}
        submittingLabel="Creating…"
        onCancel={() => router.push("/tags")}
        onSubmit={async (values) => {
          const result = await createMutation.mutateAsync({
            data: values,
          });
          if (result.status !== 200) {
            throw new Error("Unable to create tag.");
          }
          router.push("/tags");
        }}
      />
    </DashboardPageLayout>
  );
}
