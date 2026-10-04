# Part 3 — Career Launchpad

**Status: planned, not built.** Full dossier: `docs/part-3-career-launchpad/`.

Hiring prep (GD/PI/extempore/presentation, typing, quant, IELTS), resume
builder + JD matcher (ATS-friendly), portfolio builder → user's GitHub Pages,
certificates, subscriptions/billing (Free ₹0 / Pro ₹249 / Expert ₹599).

Runs as **modules inside the Part 1 monolith**, each behind hexagonal ports:

```
# future modules (each: domain + ports + adapters)
hiring/       # inbound: HiringService
resume/       # inbound: ResumeService / outbound: ResumeRenderer
portfolio/    # inbound: PortfolioService / outbound: GitHubPublisher
billing/      # inbound: BillingService / outbound: PaymentGateway (Razorpay/Stripe)
```

**Build order:** P3.1 billing/entitlements first (it gates everything), then
resume → portfolio → hiring → certificates/linking/trends. Test-mode payments
only — never real money in tests.
