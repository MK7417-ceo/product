# SkillForge — Features Test List

Tick off each feature as you test it in the Codespace. Mark ✅ working, ❌ broken (note what happens).

## 1. Auth & Onboarding
- [ ] Landing page loads for logged-out visitor (hero, features, CTA)
- [ ] Register with email + password (eye toggle shows/hides password)
- [ ] Login with email + password (eye toggle works)
- [ ] Wrong password shows error message
- [ ] Forgot password link → email form → "check inbox" message
- [ ] After login/register → lands on Dashboard (not blank)
- [ ] Bell icon → opens Notifications popup
- [ ] Avatar menu → Profile, Settings, Subscription, Billing, Logout all open
- [ ] Logout → back to Landing page

## 2. Dashboard
- [ ] Greeting shows your name (from email)
- [ ] "Next best step" button navigates to the right page
- [ ] Hero card: "Start 15-min diagnostic →" goes to /plan
- [ ] Hero card: "How scoring works" opens explanation modal (not a page)
- [ ] 4 stat cards are clickable → go to Skills / Gaps / Roadmap pages
- [ ] "No test scheduled" shows (not "in nulld")
- [ ] Daily DSA card shows today's question (not blank/crash)
- [ ] Right sidebar: streak, coins, weekly test, simulator links all work

## 3. Search (top bar)
- [ ] Search box looks modern (no "Ctrl K" button)
- [ ] Typing 2+ letters shows live dropdown results
- [ ] Filter chips (All/Roadmaps/Tasks/Evidence/Assessments/Certificates) filter
- [ ] "No matches" shows for gibberish query
- [ ] Escape or outside click closes dropdown

## 4. Assessment (/plan)
- [ ] Subject selection shows
- [ ] Level cards show correct question counts (8 / 12, not 23)
- [ ] Start → verification questions load
- [ ] Answer all → verified level shown in results

## 5. Roadmap
- [ ] Empty state: "Pick the domains" chip list appears (29 domains)
- [ ] Tapping domain chips adds them as gaps (✓ highlighted)
- [ ] "Generate my roadmap" creates tasks
- [ ] Roadmap renders as navigation journey: 📍 route summary, blue YOU ARE HERE dot, numbered stops, 🏁 destination
- [ ] Clicking a stop opens its detail panel
- [ ] Task detail: Start task, submit evidence (text/code/url) works
- [ ] Regenerate keeps completed work

## 6. Code Lab
- [ ] Page loads with editor
- [ ] **Engine must be running** (3rd terminal): `cd part-2-code-engine && uvicorn app.main:create_app --factory --host 0.0.0.0 --port 8028`
- [ ] Run Python code → output appears
- [ ] Run C / C++ / Java code → output appears
- [ ] Syntax error → stderr shows the error (not a crash)
- [ ] Infinite loop → times out gracefully

## 7. Practice
- [ ] Daily questions load with clickable options
- [ ] Submitting an answer shows correct/incorrect
- [ ] Streak/coins update

## 8. Other pages (spot check)
- [ ] Skill Profile, Skill Gaps, Evidence, Certificates load without errors
- [ ] Placement Simulator page loads
- [ ] English page loads
- [ ] Settings page loads and saves
- [ ] Coin Shop page loads

## 9. Mobile (phone browser)
- [ ] Bottom nav appears, all tabs work
- [ ] Dashboard readable, no horizontal scroll
- [ ] Auth pages usable

---

**Setup reminder (3 terminals):**
1. `cd part-1-core && uvicorn app.main:app --host 0.0.0.0 --port 8001`
2. `cd part-1-core/frontend && npm run dev -- --host 0.0.0.0 --port 5173`
3. `cd part-2-code-engine && uvicorn app.main:create_app --factory --host 0.0.0.0 --port 8028`
