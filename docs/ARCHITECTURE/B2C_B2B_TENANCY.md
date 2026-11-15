# SKILLFORGE B2C + B2B architecture decision

**Status:** Accepted product direction; implementation is phased.  
**Decision:** One shared SKILLFORGE platform serves individual learners (B2C) and organizations (B2B). Do not fork the product into separate codebases.

## Customer segments

### B2C
- Individual students, freshers, career switchers and job seekers.
- Self-service registration, individual assessment, skill-gap report, roadmap, practice, evidence review, portfolio and interview preparation.
- Free and paid individual subscriptions; entitlements are enforced by the backend.

### B2B
1. Colleges and universities: departments, programs, batches, student readiness, assessment campaigns and placement analytics.
2. Training/coaching institutes: cohorts, instructor assignment, curriculum delivery, attendance/progress and outcome reports.
3. Employers/recruiters: role-specific assessments, candidate shortlists, consent-based skill profiles and interview pipelines.

## Architecture rules

- Shared learner identity and shared skill/assessment/evidence engines.
- Organization membership is separate from the global account role. Never encode an organization-specific role in `users.role`.
- Every organization-owned record carries `organization_id` directly or through a parent relation; every query is scoped by a verified membership.
- Roles are organization-scoped: owner, org_admin, instructor, reviewer, recruiter, learner. Permissions are capability-based and checked server-side.
- A user may belong to multiple organizations and may also use a personal B2C account.
- Organization admins see cohort-level aggregate analytics by default, not private learner evidence content.
- Reviewers can access only submissions belonging to cohorts/programs assigned to their organization and permission scope.
- Employers see candidate evidence only after the learner explicitly shares a profile/application with that employer.
- No organization can enumerate another organization's users, cohorts, assessments, submissions, reports or billing.
- All privileged actions are audit logged. Membership removal revokes access immediately.
- Do not trust an `organization_id` supplied by a browser without checking the caller's active membership.

## Initial data model (proposed)

- `organizations`: id, slug, legal/display name, kind (college, training_provider, employer), status, created_at.
- `organization_memberships`: organization_id, user_id, role, status, invited_by, joined_at; unique (organization_id, user_id).
- `cohorts`: id, organization_id, name, program/department, track, start/end dates, status.
- `cohort_memberships`: cohort_id, user_id, status, joined_at; unique (cohort_id, user_id).
- `assessment_assignments`: organization_id, cohort_id, assessment blueprint, schedule, attempts and policy.
- `reviewer_assignments`: organization_id, reviewer membership, cohort/track scope.
- `organization_subscriptions`: organization_id, plan, seat quantity, billing provider IDs, lifecycle state.
- `audit_events`: organization_id, actor, action, resource type/id, timestamp and safe metadata.
- `candidate_shares`: learner_id, employer_organization_id, scope, consent timestamp, expiry/revocation.

Existing learner assessment, roadmap, practice and evidence records remain user-owned. Organization reporting joins through active cohort membership and consent/permission rules rather than copying student data into separate silos.

## B2B experiences

### College / university dashboard
- Organization setup, verified domain and admin invitation.
- Department/program and cohort creation.
- Bulk invite/import with duplicate detection and CSV validation.
- Assign diagnostic assessments and role-specific skill tracks.
- Cohort completion, skill-gap heatmaps and placement-readiness reports.
- Export aggregate reports; individual evidence access requires explicit permission.

### Training institute dashboard
- Instructor and cohort management.
- Curriculum/roadmap assignment and weekly progress.
- Learner engagement and assessment analytics.
- Reviewer queue scoped to assigned cohorts.
- Seat usage and subscription management.

### Employer dashboard
- Create job roles and competency rubrics.
- Invite candidates or accept consented shared profiles.
- Run standardized role assessments.
- Shortlist using explainable skill evidence, not opaque AI ranking.
- Interview pipeline, reviewer notes and hiring outcome tracking.
- Candidate consent and retention controls.

## Delivery sequence

1. **Tenant security foundation:** organizations, memberships, role/permission matrix, tenant-scoped repository/query helpers, audit events and cross-tenant isolation tests.
2. **College/institute MVP:** cohorts, bulk invitations, learner enrollment, assessment assignments and aggregate dashboards.
3. **Review operations:** cohort-scoped reviewer assignments, review queue and review audit history.
4. **Employer MVP:** job-role rubrics, candidate consent/sharing, assessments and shortlist workflow.
5. **B2B monetization:** seat-based subscriptions, invoice/tax configuration, organization billing admin and server-enforced seat limits.
6. **Scale:** SSO/SAML where needed, SCIM provisioning, advanced exports, integrations and service-level monitoring.

## Explicit non-goals for the first B2B release

- No cross-tenant global reviewer queue.
- No employer access to private student evidence by default.
- No bulk import without preview, validation and reversible error reporting.
- No AI-only hiring decisions or guaranteed placement claims.
- No B2B payment collection before provider onboarding, signed webhooks and entitlement tests.

## Acceptance gates

- Automated tests prove user A in organization X cannot read or mutate organization Y's records.
- Membership removal immediately blocks API access.
- A user can belong to two organizations with different roles without role collision.
- Cohort analytics match underlying authorized membership data.
- Employer access is impossible until a learner has explicitly shared the profile.
- Seat limits and organization billing are enforced server-side.
