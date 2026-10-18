"""Seed content: English Communication — Modules 7-8 (Interviews, Advanced).

Part-file for the SkillForge curriculum seed. All content is original,
written for Indian professionals: word-for-word frameworks for interview
answers, salary negotiation language, and advanced workplace
communication (persuasion, feedback, cross-cultural, networking).

Exports a single variable, ``MODULES``: 2 module dicts.

Module 7 ``comm-interviews`` — 5 lessons (self-introduction frameworks,
tell-me-about-yourself, strengths/weaknesses, salary discussion,
follow-up email).
Module 8 ``comm-advanced``   — 5 lessons (persuasion, storytelling at
work, giving feedback, cross-cultural communication, networking).

Question dicts use qtype: mcq | speaking | writing | listening.
"""
from __future__ import annotations

MODULES = [
    {
        "slug": "comm-interviews",
        "name": "Interviews",
        "description": (
            "Self-introductions that land, 'tell me about yourself', strengths and weaknesses, salary discussion, and the follow-up email."
        ),
        "lessons": [
            {
                "slug": "comm-interviews-self-intro-frameworks",
                "title": "Self-Introduction: The 30-Second and 2-Minute Versions",
                "practice_type": "speaking",
                "theory_md": """<!-- practice_type: speaking -->
## Self-Introduction: The 30-Second and 2-Minute Versions

"TELL me about yourself" is coming in every interview. Prepare TWO
versions now — the 30-second (screening calls) and the 2-minute (main
rounds). Never improvise this answer.

### The 30-second version (phone screening)

**Present → Past → Future** in 3 sentences:

> "I'm a **backend developer with 3 years at Infosys** (present),
> where I **built payment APIs handling 1M transactions a day** (past
> proof). **I'm now looking for** a role with deeper system-design
> ownership (future — why you're here)."

### The 2-minute version (main rounds)

**Present → Past proof → Spike → Future**

1. **Present** (20 sec): role, company, core work.
2. **Past proof** (60 sec): 2 achievements with NUMBERS.
3. **Spike** (20 sec): what makes you different (open source, hackathons,
   a hard problem you solved).
4. **Future** (20 sec): why THIS company, THIS role.

> "I'm a backend developer at Infosys, working on payment systems in
> Java. In the last year I cut our API latency from 800ms to 200ms and
> led the migration of 3 services to the new platform with zero
> downtime. Outside work I contribute to an open-source rate-limiting
> library. I'm excited about Flipkart because of the scale — 1M
> transactions a day is exactly the kind of problem I want to own."

### Rules

- **Numbers everywhere**: "3 years", "1M transactions", "800ms → 200ms".
  Numbers are proof; adjectives are claims.
- **End with THEM**: always close on why this company/role (shows intent).
- **Never**: life story, "myself", apologies, salary talk (unprompted).
- **Practice aloud 10 times.** It must sound natural, not memorized.
""",
                "difficulty_min": 2,
                "difficulty_max": 8,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "The 3-part structure of a 30-second self-introduction is:",
                        "choices": [
                            "Childhood → School → College",
                            "Present → Past proof → Future (why you're here)",
                            "Name → Hobbies → Family",
                            "Apology → Excuses → Hope",
                        ],
                        "answer_index": 1,
                        "difficulty": 2,
                        "explanation": "Present (who you are now), past proof (one achievement with numbers), future (why this role). Interviewers decide in 30 seconds — spend them on proof, not biography.",
                        "company_tags": [
                            "tcs",
                            "infosys",
                            "wipro",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Deliver your 30-second self-introduction NOW. Present → past proof (with a number) → future. Time it.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 4,
                        "explanation": "Checklist: under 40 sec? One number minimum? Ends with why THIS role? No 'myself'? Record it — this is your most-repeated interview answer.",
                        "company_tags": [
                            "amazon",
                            "flipkart",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which line makes a self-introduction stronger?",
                        "choices": [
                            "I am a very hardworking and sincere person.",
                            "I cut API latency from 800ms to 200ms last year.",
                            "I am good at many things.",
                            "I always give my 100%.",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "Numbers are proof; adjectives ('hardworking', 'sincere') are claims every candidate makes. One metric beats five adjectives.",
                        "company_tags": [
                            "google",
                            "amazon",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Deliver the full 2-minute version: present (20s) → 2 achievements with numbers (60s) → spike (20s) → why this company (20s).",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 7,
                        "explanation": "This is the highest-ROI 2 minutes of interview prep. Practice until the numbers roll off your tongue — hesitation on your own achievements kills credibility.",
                        "company_tags": [
                            "google",
                            "flipkart",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "The interviewer cuts your 2-minute intro short at 60 seconds with a question. You:",
                        "choices": [
                            "Say 'as I was saying…' and restart",
                            "Complain about being interrupted",
                            "Answer their question directly — the intro worked",
                            "Go silent",
                        ],
                        "answer_index": 2,
                        "difficulty": 8,
                        "explanation": "The intro did its job — it got them curious. Answer the question directly; never restart or sulk about the interruption.",
                        "company_tags": [
                            "general",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-interviews-tell-me-about-yourself",
                "title": "'Tell Me About Yourself' — The Full Playbook",
                "practice_type": "speaking",
                "theory_md": """<!-- practice_type: speaking -->
## 'Tell Me About Yourself' — The Full Playbook

It's not a biography request. It's: "Give me your 2-minute pitch for
why you fit this role." Every word should point at the job.

### The tailored version (for a specific job)

1. **Hook** (10 sec): "I'm a [role] with [X] years in [domain]."
2. **Relevant proof** (60 sec): 2 achievements MATCHED to the job
   description. Applying for backend? Talk backend wins, not your
   college fest.
3. **Why them** (30 sec): one specific thing about THIS company —
   their scale, their tech, their problem.
4. **Close** (10 sec): "That's why I'm excited about this role."

### Adapting per interviewer

- **HR**: emphasize journey, motivation, stability. Less tech depth.
- **Hiring manager**: emphasize relevant projects, ownership, results.
- **CTO/VP**: emphasize scale, impact, decisions you drove.

Same person, three spotlights. Prepare the emphasis, not three scripts.

### Traps

- ❌ Reciting your resume top to bottom (they've read it)
- ❌ "Well, I was born in…" (not a biography)
- ❌ Ending with "…yeah, that's about it." (weak close — end on THEM)
- ❌ More than 2.5 minutes (watch for the glaze; stop at the peak)

### The one-line version (networking, "who are you?" moments)

"I'm Rahul — I build payment systems at Infosys, currently obsessed
with cutting latency." One line, memorable, invites a question.
""",
                "difficulty_min": 3,
                "difficulty_max": 9,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "'Tell me about yourself' is really asking:",
                        "choices": [
                            "Describe your hobbies and family",
                            "Tell me your life story from childhood",
                            "List every job you've ever had in order",
                            "Give me your 2-minute pitch for why you fit THIS role",
                        ],
                        "answer_index": 3,
                        "difficulty": 3,
                        "explanation": "It's a fit pitch, not a biography. Every achievement you mention should connect to the job description.",
                        "company_tags": [
                            "tcs",
                            "infosys",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Answer 'tell me about yourself' for a BACKEND role in 2 minutes: hook → 2 backend achievements → why this company → close.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 6,
                        "explanation": "Tailoring test: did you mention frontend/college-fest wins? Cut them. Every proof point should make a backend hiring manager nod.",
                        "company_tags": [
                            "amazon",
                            "flipkart",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You're at 2 minutes and the interviewer looks glazed. You should:",
                        "choices": [
                            "Wrap up in 15 seconds and close on why you want the role",
                            "Ask 'should I continue?' and wait",
                            "Keep going — more detail is always better",
                            "Start over with more energy",
                        ],
                        "answer_index": 0,
                        "difficulty": 8,
                        "explanation": "Stop at the peak, not past it. A crisp close ('that's why I'm excited about this role') beats 2 more minutes of fading attention.",
                        "company_tags": [
                            "google",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "The interviewer is HR (non-technical). You adjust by:",
                        "choices": [
                            "Less tech depth — more journey, motivation, why this company",
                            "The exact same script as for engineers",
                            "Skip the answer — HR doesn't matter",
                            "Even MORE technical jargon to impress",
                        ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "HR scores journey, motivation, stability, communication. Save the deep tech for the hiring manager round.",
                        "company_tags": [
                            "tcs",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Give the ONE-LINE version for a networking event: name → what you do → one memorable line. 10 seconds.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 9,
                        "explanation": "Model: 'I'm Rahul — I build payment systems at Infosys, currently obsessed with cutting latency.' Memorable, invites a question, zero rambling.",
                        "company_tags": [
                            "general",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-interviews-strengths-weaknesses",
                "title": "Strengths and Weaknesses: Answer Without Lying",
                "practice_type": "speaking",
                "theory_md": """<!-- practice_type: speaking -->
## Strengths and Weaknesses: Answer Without Lying

"What are your weaknesses?" — the question everyone dreads. The trick:
be honest about a REAL weakness, then show the system you built to
manage it. That's what interviewers actually score.

### Strengths: claim → proof → relevance

Never just name a strength. Attach proof and tie it to the role:

> "My strength is **debugging under pressure** (claim). Last quarter I
> found the race condition that had blocked the release for two weeks
> (proof) — which is why I'm confident handling your on-call rotation
> (relevance)."

Pick strengths from the **job description**, not your personality.

### Weaknesses: the 3-part honest formula

**Real weakness → Impact → What you're doing about it**

> "I **used to avoid public speaking** (real), which meant my good work
> wasn't visible (impact). **For the last 6 months I've been presenting
> in our team demos monthly**, and I presented to 40 people last week
> (action + progress)."

This works because it's TRUE and shows growth — exactly what the
question tests.

### Weaknesses that work (pick a real one)

- Public speaking / presenting (with the demo-practice fix)
- Saying no / overcommitting (with the prioritization-framework fix)
- Perfectionism slowing delivery (with the timeboxing fix)
- Asking for help late (with the 30-minute rule fix)

### Never say

- ❌ "I'm a perfectionist" (with no fix — it's a humblebrag)
- ❌ "I work too hard" (they've heard it 1000 times)
- ❌ "I have no weaknesses" (instant fail — everyone does)
- ❌ A weakness that's core to the job ("I'm bad with deadlines" for
  a delivery role — pick something else)
""",
                "difficulty_min": 4,
                "difficulty_max": 8,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Best weakness answer?",
                        "choices": [
                            "I avoided public speaking, which hid my work — so I've presented in team demos monthly for 6 months.",
                            "I don't have any weaknesses.",
                            "I'm a perfectionist.",
                            "I work too hard.",
                        ],
                        "answer_index": 0,
                        "difficulty": 4,
                        "explanation": "Real weakness + impact + concrete fix with timeline. The others are clichés or lies — interviewers filter them instantly.",
                        "company_tags": [
                            "tcs",
                            "wipro",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Answer 'What's your greatest strength?' in 45 seconds: claim → proof (with number) → relevance to the role.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 6,
                        "explanation": "Model: 'My strength is owning ambiguous problems end to end. When our payment dashboard had no owner, I took it, shipped it in 3 sprints, and it now serves 200 internal users — which maps directly to this role's ownership expectations.'",
                        "company_tags": [
                            "amazon",
                            "flipkart",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why does 'I'm a perfectionist' fail as a weakness answer?",
                        "choices": [
                            "It's too short an answer",
                            "Perfectionism is always a strength",
                            "Interviewers love perfectionists",
                            "It's a disguised brag with no real weakness or fix — interviewers see through it",
                        ],
                        "answer_index": 3,
                        "difficulty": 8,
                        "explanation": "Without a genuine struggle and a system to manage it, 'perfectionist' is just vanity. The question tests self-awareness — show yours.",
                        "company_tags": [
                            "google",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Choosing which weakness to share: it should be…",
                        "choices": [
                            "Real, not core to the job, with a fix already in progress",
                            "Your biggest actual flaw with no fix",
                            "Completely made up",
                            "A strength in disguise with no honesty",
                        ],
                        "answer_index": 0,
                        "difficulty": 6,
                        "explanation": "Real + not core to the job + fix in progress. 'Bad with deadlines' for a delivery role = self-sabotage; pick a genuine-but-manageable one.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "writing",
                        "prompt": "Write your weakness answer in exactly 3 sentences: weakness → impact → fix. Max 60 words.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 7,
                        "explanation": "Model (48 words): 'I used to avoid speaking up in reviews, so good catches of mine never surfaced. For six months I've forced myself to raise one point per review — last month my flag caught a data-loss bug.' Count your words; brevity is confidence.",
                        "company_tags": [
                            "wipro",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-interviews-salary-discussion",
                "title": "Salary Discussion: Numbers Without Fear",
                "practice_type": "speaking",
                "theory_md": """<!-- practice_type: speaking -->
## Salary Discussion: Numbers Without Fear

Indians often undersell ("whatever you give is fine") or overshoot
blindly. Salary talk is a negotiation — and negotiation is a learnable
skill with exact phrases.

### Before the conversation (homework)

1. **Know your number**: current CTC + market rate (check levels.fyi,
   Glassdoor, peers) → set a **range**, not a point.
2. **Know your walk-away**: the minimum you'd accept. Never reveal it.
3. **List your leverage**: competing offer > niche skill > strong
   alternative (even "I'm happy where I am" is leverage).

### The phrases

**When asked "What are your expectations?":**
> "Based on my research for this role and level, I'm looking at **₹X–Y
> LPA**. I'm flexible for the right opportunity — what range have you
> budgeted for this role?"

(Range + flip the question back. Never say one number first if you can
avoid it.)

**When the offer is low:**
> "Thank you for the offer — I'm excited about the role. The number is
> a bit below my expectations given [market data / competing offer].
> Is there flexibility to get closer to ₹Y?"

**When they say "that's our final":**
> "I understand. Could we look at the joining bonus / first review
> cycle / ESOPs to bridge the gap?"

### Rules

- **Never accept on the spot.** "Thank you — can I get back by
  tomorrow?" (Even if you love it. Overnight thinking is free.)
- **Get it in writing** before resigning. Verbal offers evaporate.
- **Don't lie about current CTC** — background checks verify it.
- **Total comp, not just fixed**: bonus, ESOPs, joining bonus, review
  cycle all count.
""",
                "difficulty_min": 5,
                "difficulty_max": 10,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "HR asks 'What are your salary expectations?' Best response?",
                        "choices": [
                            "Refuse to discuss money at all",
                            "Name one exact number immediately",
                            "Give a researched range, then ask what they've budgeted for the role",
                            "Say 'Whatever you give is fine'",
                        ],
                        "answer_index": 2,
                        "difficulty": 5,
                        "explanation": "A researched range shows you know your worth; flipping the question reveals their budget. 'Whatever is fine' leaves lakhs on the table.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Practice aloud: respond to 'We can offer ₹12 LPA' when you wanted ₹15. Use the low-offer phrase with a reason.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 7,
                        "explanation": "Model: 'Thank you — I'm genuinely excited about the role. ₹12 is below what I've seen for this level; my research puts it closer to ₹14–15. Is there flexibility to bridge that gap?' Grateful + data + ask. Never angry, never apologetic.",
                        "company_tags": [
                            "flipkart",
                            "amazon",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You love the offer and want to accept. You should still:",
                        "choices": [
                            "Accept but keep interviewing secretly for months",
                            "Ask for a day to decide, and get the full offer in writing before resigning",
                            "Ask for double the offer just to try",
                            "Accept verbally on the spot and resign today",
                        ],
                        "answer_index": 1,
                        "difficulty": 9,
                        "explanation": "Overnight thinking is free and prevents regret; written offers prevent 'misunderstandings'. Verbal offers have evaporated for many candidates.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "They ask your CURRENT salary. You:",
                        "choices": [
                            "Inflate it by 40%",
                            "Answer honestly (it's verifiable), then pivot: 'I'm at X; for this role I'm looking at Y–Z'",
                            "Say 'that's confidential'",
                            "Refuse to answer",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "Never lie about current CTC — background verification checks it. Answer honestly, then pivot to expectations for the new role.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "60-second role-play, full arc: state expectation → hear low offer → counter with data → probe joining bonus.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 10,
                        "explanation": "Model: 'I'm looking at 14–15 based on the level… I see — 12 is below that; my research and a competing process put this role at 14. Is there flexibility? … I understand — could we bridge it with the joining bonus or an early review?' Full negotiation in one breath.",
                        "company_tags": [
                            "flipkart",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-interviews-followup-email",
                "title": "The Follow-Up Email That Gets You Remembered",
                "practice_type": "writing",
                "theory_md": """<!-- practice_type: writing -->
## The Follow-Up Email That Gets You Remembered

90% of candidates never follow up. A 5-minute email within 24 hours puts
you in the top 10% — interviewers literally mention it in debriefs.

### The template (copy-paste ready)

> **Subject:** Thank you — [Role] interview today
>
> Hi [Name],
>
> Thank you for your time today. I really enjoyed discussing [ONE
> specific topic from the interview — the scaling challenge / the team
> structure / the migration plan].
>
> Our conversation about [topic] made me even more excited about the
> role — especially [one specific reason].
>
> Please let me know if you need anything else from my side.
>
> Best regards,
> [Your name] | [phone]

### Why it works

- **Specific topic** = you were listening (not a mass template).
- **24 hours** = still fresh in their memory.
- **Short** = respects their inbox.

### If you want to add value (advanced)

Attach or link ONE relevant thing: "As discussed, here's the article
on rate limiting I mentioned." This moves you from 'polite candidate'
to 'already contributing'.

### After rejection (yes, really)

> Hi [Name], thank you for letting me know. I really enjoyed meeting
> the team — if a similar role opens up, I'd love to be considered.
> Wishing you the best with the hire!

30% of rejections turn into referrals or future roles. Grace is
remembered.
""",
                "difficulty_min": 2,
                "difficulty_max": 7,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "When should you send the post-interview thank-you email?",
                        "choices": [
                            "After a week, so you don't look desperate",
                            "Within 24 hours, mentioning one specific discussion topic",
                            "Never — it's unprofessional to email interviewers",
                            "Only if they ask you to",
                        ],
                        "answer_index": 1,
                        "difficulty": 2,
                        "explanation": "24 hours keeps you fresh in memory; the specific topic proves genuine engagement. 90% of candidates skip this — it's free differentiation.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "writing",
                        "prompt": "Write the thank-you email: you interviewed for a backend role, discussed their migration to microservices, interviewer's name is Neha.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 4,
                        "explanation": "Model:\nSubject: Thank you — Backend Developer interview today\n\nHi Neha,\n\nThank you for your time today. I really enjoyed discussing the microservices migration — the strangler-fig approach you described was new to me.\n\nOur conversation made me even more excited about the role, especially the ownership over the payments services.\n\nPlease let me know if you need anything else from my side.\n\nBest regards,\nRahul | 98XXXXXXXX",
                        "company_tags": [
                            "tcs",
                            "infosys",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You got rejected after the final round. Best move?",
                        "choices": [
                            "Immediately ask for the interviewer's personal number",
                            "Argue with the recruiter about the decision",
                            "Send a gracious reply asking to be considered for future roles",
                            "Ghost them and badmouth the company online",
                        ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "Graceful rejections convert to referrals — hiring managers remember mature candidates and call them first for the next opening.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "The interviewer recommended a book during the chat. In your follow-up:",
                        "choices": [
                            "Pretend you already read it",
                            "Mention it with one line on what you took from it",
                            "Ask them to buy it for you",
                            "Ignore it — too personal",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "One specific callback ('started the first chapter on…') proves you listened AND keeps the conversation alive. Generic thanks don't.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "writing",
                        "prompt": "Write the graceful rejection reply: thank them, keep the door open, wish them well. 3 lines.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 7,
                        "explanation": "Model: 'Hi Neha, thank you for letting me know — I really enjoyed meeting the team. If a similar backend role opens up, I'd love to be considered. Wishing you the best with the hire!' Dignity now = referrals later.",
                        "company_tags": [
                            "general",
                        ],
                    },
                ],
            },
        ],
    },
    {
        "slug": "comm-advanced",
        "name": "Advanced",
        "description": (
            "Persuasion, storytelling at work, giving feedback, cross-cultural communication, and professional networking."
        ),
        "lessons": [
            {
                "slug": "comm-advanced-persuasion",
                "title": "Persuasion: Getting to Yes at Work",
                "practice_type": "speaking",
                "theory_md": """<!-- practice_type: speaking -->
## Persuasion: Getting to Yes at Work

Promotions go to people who can move others — approve the idea, fund
the project, change the plan. Persuasion is a structure, not a talent.

### The 4-part persuasion frame

1. **Problem** (their pain, not yours): "Every deploy currently needs
   2 hours of manual checks…"
2. **Cost of inaction**: "…which cost us 3 delayed releases last quarter."
3. **Proposal**: "Automating the checks takes 2 weeks and pays for
   itself by March."
4. **Ask** (specific, small): "Can we try it on one service first?"

### Why it works

- **Their pain first**: nobody cares about your solution until they
  feel the problem.
- **Numbers**: "3 delayed releases" beats "it's really bad".
- **Small ask**: "try on one service" is easy to say yes to; "rewrite
  everything" isn't. Get the small yes, earn the big one.

### Handling objections (pre-empt them)

Before the meeting, list the top 3 objections and prepare answers:
- "No time" → "2 weeks, and it saves 2 hours per deploy forever."
- "Too risky" → "That's why I propose one service first."
- "Not a priority" → "The 3 delays last quarter say otherwise."

Bringing up objections yourself ("You might be thinking…") makes you
look thorough, not defensive.

### The one-line test

If you can't state your proposal in one sentence, you're not ready:
"We should automate deploy checks to stop losing release days."
""",
                "difficulty_min": 5,
                "difficulty_max": 10,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Most persuasive order for a proposal?",
                        "choices": [
                            "Your solution → your effort → demand approval",
                            "Their pain → cost of inaction → proposal → small specific ask",
                            "Send a 10-page document with no summary",
                            "Complain about the problem → wait for someone else to fix it",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "Lead with THEIR pain (not your solution), quantify the cost, propose, then make the ask small enough to say yes to.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Persuade your manager in 60 seconds: you want 2 days for a refactoring that will speed up future work. Use all 4 parts.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 7,
                        "explanation": "Model: 'Every new feature in the auth module takes a day extra because of the tangled code — that's 5 days lost last month alone. Two days of refactoring now saves that every month. Can we slot it into next sprint?' Pain → cost → proposal → ask.",
                        "company_tags": [
                            "flipkart",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Someone objects 'we don't have time for this.' Best response?",
                        "choices": [
                            "'Management doesn't understand engineering.'",
                            "'You're wrong, we have plenty of time.'",
                            "'Fine, forget I mentioned it.'",
                            "'That's exactly why I'm proposing we start with one service — 2 days now saves 2 hours per deploy forever.'",
                        ],
                        "answer_index": 3,
                        "difficulty": 9,
                        "explanation": "Answer the objection with THEIR concern (time) reframed as the reason to act. Pre-empted objections, answered calmly, are persuasion fuel.",
                        "company_tags": [
                            "amazon",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You can't state your proposal in one sentence. That means:",
                        "choices": [
                            "Cancel the proposal",
                            "You're not ready — sharpen the proposal before the meeting",
                            "Add more slides to explain it",
                            "It's fine, complexity impresses people",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "The one-line test is brutal and honest: if you can't say it simply, you don't understand it well enough to sell it yet.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "writing",
                        "prompt": "Write a 4-line Slack message persuading your team to adopt the new linter. All 4 parts: pain → cost → proposal → small ask.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 10,
                        "explanation": "Model: 'Our last 3 PRs each needed 2 review rounds for style nits (pain+cost). The new linter auto-fixes them on save — 10 min setup each (proposal). Can we trial it on the auth service this week? (ask)' Four lines, hard to say no to.",
                        "company_tags": [
                            "general",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-advanced-storytelling",
                "title": "Storytelling at Work: STAR Stories That Stick",
                "practice_type": "speaking",
                "theory_md": """<!-- practice_type: speaking -->
## Storytelling at Work: STAR Stories That Stick

Facts tell, stories sell. In appraisals, interviews, and team meetings,
the person with the best stories wins — because humans remember stories,
not bullet points.

### The STAR frame (memorize it)

- **S**ituation: "Our checkout was failing for 1 in 20 users…"
- **T**ask: "…and I owned the investigation…"
- **A**ction: "…so I added distributed tracing and found the race
  condition in the inventory check…"
- **R**esult: "…failures dropped to zero, saving an estimated ₹2L/month."

30-60 seconds. Numbers in the Result. Always.

### Build your story bank (do this once)

Write down 5 stories from your work:
1. A hard bug you fixed
2. A deadline you saved
3. A conflict you resolved
4. Something you improved (process, speed, cost)
5. Something you learned from failing

These 5 stories answer 80% of behavioral questions ("Tell me about a
challenge…", "A time you disagreed…", "Your biggest achievement…").

### Storytelling rules

- **Start with the stakes**: "We were losing ₹2L a month…" (not "So
  there was this bug…")
- **You are the hero of YOUR stories** — say "I", not "we", for your
  actions. ("The team" did the work; YOU did your part — name it.)
- **End with the lesson**: "…which is why I now add tracing from day one."
- **60 seconds max** in interviews. Longer = rambling.

### Where stories win

Appraisals ("here are my 3 impact stories"), interviews, promotion
packets, team retros, client calls. One good story > ten bullet points.
""",
                "difficulty_min": 4,
                "difficulty_max": 9,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "STAR stands for:",
                        "choices": [
                            "Subject, Topic, Argument, Resolution",
                            "Situation, Task, Action, Result",
                            "Story, Theory, Analysis, Review",
                            "Start, Talk, Answer, Rest",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "Situation (stakes) → Task (your responsibility) → Action (what YOU did) → Result (numbers). 60 seconds, always.",
                        "company_tags": [
                            "amazon",
                            "google",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Tell a 60-second STAR story about a real problem you solved (work, college project, anything). Include one number in the Result.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 6,
                        "explanation": "Checklist: stakes in first 10 seconds? 'I' for your actions (not just 'we')? Number in result? Lesson at the end? This story goes in your bank — reuse it in interviews.",
                        "company_tags": [
                            "amazon",
                            "flipkart",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "In your STAR story, you should say 'we' instead of 'I' when:",
                        "choices": [
                            "Never mention the team at all",
                            "Almost never for YOUR actions — say 'I' for what you did; 'we' only for genuine team actions",
                            "Only in the Situation part",
                            "Always — it shows you're a team player",
                        ],
                        "answer_index": 1,
                        "difficulty": 8,
                        "explanation": "Interviewers score YOU. 'We fixed it' hides your contribution; 'I traced it to the race condition while the team handled the rollout' shows both ownership and teamwork.",
                        "company_tags": [
                            "google",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Best story choice for 'tell me about a failure'?",
                        "choices": [
                            "'I once worked too hard and burned out'",
                            "A real failure, your fault, the lesson, what you changed since",
                            "'I've never really failed'",
                            "Blame your old manager",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "Interviewers want: real failure + YOUR fault + lesson + changed behavior. Fake failures ('I worked too hard') insult their intelligence.",
                        "company_tags": [
                            "amazon",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Tell a 60-second FAILURE story: stakes → your mistake → lesson → what changed. End on growth.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 9,
                        "explanation": "Model: 'We lost a client demo because I hadn't tested on slow networks — my call to skip it. Cost us the deal. Since then I maintain a pre-demo checklist with network throttling, and we've had zero demo failures in a year.' Owning failure confidently is a senior signal.",
                        "company_tags": [
                            "google",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-advanced-giving-feedback",
                "title": "Giving Feedback: Honest Without Being Harsh",
                "practice_type": "speaking",
                "theory_md": """<!-- practice_type: speaking -->
## Giving Feedback: Honest Without Being Harsh

Indians often avoid feedback ("don't want to hurt feelings") or deliver
it brutally ("your code is garbage"). Both fail. The SBI model threads
the needle.

### The SBI model: Situation → Behavior → Impact

> "**In yesterday's review** (situation), **the API returned 500s on 3
> of 10 test cases** (behavior — observable fact, not judgment).
> **That blocked QA's whole afternoon** (impact)."

Then add the forward look: "**Next time, could we run the full suite
before the review?**"

### Why SBI works

- **Situation** anchors it (not "you always…")
- **Behavior** is factual (not "you're careless")
- **Impact** explains WHY it matters (people accept feedback they
  understand)
- **Request** makes it actionable (not just criticism)

### Positive feedback (give 3x more than negative)

Same model: "In today's demo (S), your error-handling walkthrough (B)
made the client confident enough to approve phase 2 (I)." Specific
praise gets repeated; "good job" gets forgotten.

### Rules

- **Timely**: within 24-48 hours. Month-old feedback is archaeology.
- **Private** for negative, **public** for positive.
- **Ask permission** for big ones: "Can I share some feedback on the
  presentation?" (Lowers defenses instantly.)
- **Never**: "You're too sensitive" / feedback about personality
  ("you're lazy") — only about behavior ("the report was 2 days late").

### Receiving feedback (the other half)

"Thank you — can you give me an example?" Then listen, don't defend.
The person giving you feedback is doing you a favor.
""",
                "difficulty_min": 5,
                "difficulty_max": 10,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Using SBI, which feedback is best?",
                        "choices": [
                            "Your code is garbage.",
                            "You always break things.",
                            "In yesterday's review, the API failed 3 of 10 cases, which blocked QA — could we run the full suite before reviews?",
                            "You're too careless as a person.",
                        ],
                        "answer_index": 2,
                        "difficulty": 5,
                        "explanation": "Situation (yesterday's review) + Behavior (3 of 10 failed — fact) + Impact (blocked QA) + Request. No personality attacks, fully actionable.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Give SBI feedback: a teammate's slides had tiny fonts and the client couldn't read them.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 7,
                        "explanation": "Model: 'In today's client demo, the slides were at maybe 12-point font and the client squinted through three of them — I think it hurt our credibility a bit. Could we use the 30-point minimum rule for client decks?' Fact, impact, request.",
                        "company_tags": [
                            "tcs",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Someone gives you critical feedback. Best first response?",
                        "choices": [
                            "'Well, YOU did the same thing last week.'",
                            "(Silent treatment for a week)",
                            "'You're wrong, that's not true.'",
                            "'Thank you — can you give me a specific example?'",
                        ],
                        "answer_index": 3,
                        "difficulty": 9,
                        "explanation": "Thanks + example-request keeps you learning and keeps the giver willing to be honest next time. Defensiveness trains people to never tell you the truth.",
                        "company_tags": [
                            "google",
                            "amazon",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "The feedback is 3 weeks old. You should:",
                        "choices": [
                            "Tell everyone except the person",
                            "Save it for the appraisal",
                            "Drop it, or raise it only as part of a current pattern",
                            "Deliver it dramatically for impact",
                        ],
                        "answer_index": 2,
                        "difficulty": 7,
                        "explanation": "Stale feedback confuses ('what incident?') and feels like stored ammunition. Either drop it or fold it into a current pattern conversation.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "writing",
                        "prompt": "Write 3-line POSITIVE SBI feedback for a teammate. Specific enough that they'd repeat the behavior.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 10,
                        "explanation": "Model: 'In yesterday's client call (S), you caught the pricing error before I sent the quote (B) — that saved us an embarrassing correction (I).' Specific praise gets repeated; 'great job!' evaporates.",
                        "company_tags": [
                            "general",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-advanced-cross-cultural",
                "title": "Cross-Cultural Communication: US, UK, and Beyond",
                "practice_type": "mcq",
                "theory_md": """<!-- practice_type: mcq -->
## Cross-Cultural Communication: US, UK, and Beyond

The same sentence lands differently in Mumbai, Texas, and London.
Working with international clients/teams means adjusting — not
faking an accent, but tuning directness, small talk, and expectations.

### Directness scale

- **US**: direct is respectful. "I disagree because…" is normal, even
  with seniors. Silence reads as agreement.
- **UK**: indirect is polite. "That's an interesting idea…" can mean
  "no". Listen for softeners.
- **Germany/Netherlands**: very direct — don't take bluntness personally.
- **Japan/Middle East**: relationship first, business second. Rushing to
  the point feels rude.

### Practical adjustments for US clients

1. **Get to the point in 30 seconds.** Long context-building ("So
   actually what happened was…") loses Americans. Headline first,
   details on request.
2. **Say no clearly.** "That won't work because…" beats a vague
   "We'll try our best" (which Americans read as a yes).
3. **Small talk is short**: weather, weekend — 2 minutes max, then work.
4. **Time is literal**: "EOD" means their EOD — clarify timezone.
   "I'll send it by EOD IST" prevents 5.5 hours of confusion.

### With UK clients

- Expect understatement: "a bit concerned" = quite worried.
- Humor is drier — don't force jokes; a light touch is enough.
- "Cheers" as thanks is normal; don't overthink it.

### Universal rules

- **Confirm in writing** after calls: timezones and accents cause
  misunderstandings; a 3-line email prevents them.
- **Ask about holidays**: "Are you working next week?" before planning
  around Thanksgiving/Christmas — India works, they don't.
- **Never assume**: "Just checking — by Friday, did you mean your
  Friday or mine?"
""",
                "difficulty_min": 4,
                "difficulty_max": 9,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "A US client asks 'Can you deliver by Friday?' and it looks impossible. Best response?",
                        "choices": [
                            "We'll try our best.",
                            "Yes. (then miss the deadline)",
                            "Maybe, I'll do the needful.",
                            "That won't work because the API isn't ready — but I can deliver the core flow by Friday and the rest by Monday.",
                        ],
                        "answer_index": 3,
                        "difficulty": 4,
                        "explanation": "Americans read vague optimism as a commitment. A clear no + alternative + dates is respected; 'we'll try our best' followed by failure destroys trust.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A UK client says your proposal is 'quite interesting'. You should read this as:",
                        "choices": [
                            "An insult",
                            "Enthusiastic approval — start work immediately",
                            "Polite but non-committal — ask what concerns they have",
                            "A legal commitment",
                        ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "British understatement: 'quite interesting' often means 'I have reservations'. Probe gently: 'What would make it work for you?'",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "You're emailing a US client a delay. In 30 seconds, give: headline first, then one detail, then the new date. No long backstory.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 8,
                        "explanation": "Model: 'Heads-up: the delivery moves from Friday to Monday. The payment API changed their spec yesterday, adding a day of rework. I'll confirm by Monday 10am your time.' Headline → reason → date. Americans skim — front-load.",
                        "company_tags": [
                            "amazon",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You email a US client 'I'll send it by EOD Friday.' Fix it:",
                        "choices": [
                            "Remove the deadline entirely",
                            "'I'll send it by EOD Friday IST — that's your Friday morning.'",
                            "It's fine as is",
                            "'I'll send it by EOD Friday IST PST EST GMT'",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "'EOD' without a timezone is a 5.5-hour ambiguity bomb. Always anchor: 'EOD Friday IST (your Friday morning)'.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Leave a 20-second voicemail for a US client about a delay. Headline first, no backstory, new date.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 9,
                        "explanation": "Model: 'Hi Sarah, quick heads-up: the report moves from Friday to Monday — the API spec changed yesterday. I'll confirm by Monday 10am your time. Call me back if that's an issue.' 20 seconds, complete, respectful of their time.",
                        "company_tags": [
                            "general",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-advanced-networking",
                "title": "Networking: LinkedIn Messages That Get Replies",
                "practice_type": "writing",
                "theory_md": """<!-- practice_type: writing -->
## Networking: LinkedIn Messages That Get Replies

Referrals beat applications — referred candidates get interviewed 10x
more. But "Hi sir, please refer me" messages get ignored. Here's what
works.

### The referral request (template)

> Hi [Name],
>
> I'm [Rahul], a backend developer with 3 years in Java/Spring Boot.
> I saw the [exact role title] opening on your team — my [specific
> relevant work: payment APIs at 1M/day] looks like a strong match.
>
> Would you be open to referring me? Happy to share my resume and a
> short note on why I fit.
>
> Thanks either way,
> Rahul

Why it works: **specific role + specific proof + low effort for them**
(resume attached, note ready). Generic "please refer me" = work for
them = ignored.

### The cold outreach (to someone you admire)

> Hi [Name], I read your post on [specific topic] — the point about
> [specific detail] changed how I think about [X]. I'm a [your role]
> working on [related thing]. Would love to stay connected.

**Specific > flattery.** "Your post on Kafka partitioning — the
consumer-lag point — helped me fix our setup" beats "You're so
inspiring" 100:1.

### Rules

- **Never** "Hi sir/mam, I need a job, please help." (begging, no context)
- **Always** personalize: one specific detail proves it's not spam.
- **Follow up once** after a week, then drop it gracefully.
- **Give before you ask**: comment thoughtfully on their posts for
 2 weeks before messaging. Warm > cold.

### After they help you

Thank them, and update them when you get the interview/offer. People
who feel their referral mattered refer again — building your network
compounds.
""",
                "difficulty_min": 4,
                "difficulty_max": 9,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Best LinkedIn referral request?",
                        "choices": [
                            "A 500-word life story",
                            "'Hi sir, please refer me, I need a job urgently'",
                            "'Hello' (no other text)",
                            "Specific role + your matching proof + resume ready + thanks either way",
                        ],
                        "answer_index": 3,
                        "difficulty": 4,
                        "explanation": "Referrers spend social capital on you — make it easy (resume + fit note ready) and specific (exact role, exact proof). 'Please refer me' with zero context gets archived.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "writing",
                        "prompt": "Write a cold LinkedIn message (4 lines max) to an engineer whose post on system design you actually read. Include one specific detail.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 6,
                        "explanation": "Model: 'Hi Ananya, your post on cache stampedes was excellent — the probabilistic-early-expiration trick is something I'll try on our hot keys. I'm a backend dev working on similar scaling problems. Would love to stay connected.' Specific detail = not spam.",
                        "company_tags": [
                            "google",
                            "flipkart",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "No reply to your networking message after a week. You should:",
                        "choices": [
                            "Comment 'why are you ignoring me' on their posts",
                            "Message their manager to complain",
                            "Follow up once politely, then let it go gracefully",
                            "Send 5 more messages",
                        ],
                        "answer_index": 2,
                        "difficulty": 8,
                        "explanation": "One polite follow-up is professional; more is harassment. Networks compound over years — never burn a bridge over one unanswered message.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Someone referred you and you GOT the interview. You must:",
                        "choices": [
                            "Nothing — they did their part",
                            "Thank them and update them on the outcome",
                            "Forget their name",
                            "Ask for another referral immediately",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "Referrers spend social capital. Thank them + update the outcome — people who feel their referral mattered refer again. Your network compounds.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Record a 20-second conference intro: name → what you do → one memorable line. (Use it at actual events.)",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 9,
                        "explanation": "Model: 'I'm Rahul, backend dev at Infosys — I make payment APIs fast. Currently obsessed with cutting our p99 latency in half.' Memorable + specific + invites exactly one follow-up question.",
                        "company_tags": [
                            "general",
                        ],
                    },
                ],
            },
        ],
    },
]
