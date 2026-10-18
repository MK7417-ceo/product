"""Seed content: English Communication — Modules 5-6 (Meetings, Presentations).

Part-file for the SkillForge curriculum seed. All content is original,
written for Indian professionals: exact phrases for real meeting
situations, presentation structures that work, Q&A survival tactics.

Exports a single variable, ``MODULES``: 2 module dicts.

Module 5 ``comm-meetings``      — 5 lessons (self-introduction, giving
opinions, agreeing/disagreeing, asking questions, summarizing).
Module 6 ``comm-presentations`` — 5 lessons (opening structure, slide
talk, closing, handling Q&A, virtual presentations).

Question dicts use qtype: mcq | speaking | writing | listening.
"""
from __future__ import annotations

MODULES = [
    {
        "slug": "comm-meetings",
        "name": "Meetings",
        "description": (
            "Introducing yourself, giving opinions, polite disagreement, asking sharp questions, and summarizing like a lead."
        ),
        "lessons": [
            {
                "slug": "comm-meetings-self-introduction",
                "title": "The 30-Second Meeting Introduction",
                "practice_type": "speaking",
                "theory_md": """<!-- practice_type: speaking -->
## The 30-Second Meeting Introduction

"Let's go around and introduce ourselves" — and your mind goes blank.
Memorize this 4-part formula once; use it forever.

### The formula: Name → Role → Work → Connection

> "I'm **Rahul Sharma** (name), a **backend developer** on the **payments
> team** (role), currently working on the **UPI integration** (work).
> **Looking forward to** working with everyone on this (connection)."

Four parts, 30 seconds, zero rambling. Adapt the last part:
- Client meeting: "…excited to support your launch."
- New team: "…happy to be here — please reach out anytime."

### What to cut

- ❌ Your college, your hometown, your life story (not a matrimonial ad)
- ❌ "Myself Rahul" (never — it's "I'm Rahul" / "My name is Rahul")
- ❌ Apologizing: "Sorry, my English is not good" (never open with this)

### For video calls (add one line)

"I'm Rahul Sharma, backend developer — **I'm on mute most of the time,
ping me in chat if I miss something.**" Practical + human.

### Practice until boring

Say it 20 times until it needs zero thought. Introductions should be
automatic — your brain is needed for the actual meeting.
""",
                "difficulty_min": 1,
                "difficulty_max": 6,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Which introduction is correct?",
                        "choices": [
                            "Myself Rahul Sharma, backend developer.",
                            "I am Rahul Sharma itself.",
                            "I'm Rahul Sharma, a backend developer on the payments team.",
                            "My name is Rahul Sharma myself.",
                        ],
                        "answer_index": 2,
                        "difficulty": 1,
                        "explanation": "'Myself Rahul' is the classic Indianism — 'myself' is reflexive, not a subject. Use 'I'm…' or 'My name is…'.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Deliver your 30-second introduction using Name → Role → Work → Connection. Time it.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 3,
                        "explanation": "Target: under 35 seconds, all four parts, no 'myself', no life story. Record it — this exact recording is reusable for every new meeting.",
                        "company_tags": [
                            "tcs",
                            "infosys",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You're joining a client kickoff call. Best closing line for your intro?",
                        "choices": [
                            "I passed out in 2022.",
                            "Sorry for my bad English.",
                            "I am from a small town in UP.",
                            "Looking forward to supporting your launch.",
                        ],
                        "answer_index": 3,
                        "difficulty": 5,
                        "explanation": "End with a forward-looking connection to THEIR goal. Never apologize for English, share irrelevant biography, or say 'passed out'.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You're introducing yourself in a 50-person all-hands. Adjust how?",
                        "choices": [
                            "Longer: full life story, they have time",
                            "Shorter: 15 seconds — name, role, one line on your work",
                            "Skip it — 50 people won't listen anyway",
                            "Read your resume aloud",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "Big rooms = shorter. 15 seconds: name, role, one line. Details are for small meetings.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Introduce yourself for a CLIENT kickoff call: use the formula + the 'on mute, ping me in chat' line.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 6,
                        "explanation": "Model: 'I'm Rahul Sharma, backend developer on the payments team, currently on the UPI integration. I'm on mute most of the time — ping me in chat if I miss something. Looking forward to supporting your launch.' Professional + human + practical.",
                        "company_tags": [
                            "tcs",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-meetings-giving-opinions",
                "title": "Giving Opinions: Sound Confident, Not Arrogant",
                "practice_type": "speaking",
                "theory_md": """<!-- practice_type: speaking -->
## Giving Opinions: Sound Confident, Not Arrogant

Juniors stay silent; some seniors bulldoze. The professional middle:
state your view clearly, show your reasoning, invite challenge.

### The opinion toolkit (weak → strong)

1. **Tentative** (exploring): "What if we…?", "Could we consider…?"
2. **Standard** (your view): "In my view…", "I'd suggest…", "I think we should…"
3. **Strong** (you're sure): "I'm confident that…", "The data shows…"
4. ❌ **Arrogant**: "Obviously…", "Anyone can see…", "Trust me…"

Default to #2. Use #1 when you're new to the topic, #3 when you have
evidence. Never #4.

### The opinion sandwich (for pushback)

**Acknowledge → Your view → Reason → Invite response**

> "I understand the concern about the timeline. **In my view**, we should
> cut scope rather than add people — **because** onboarding takes two
> weeks anyway. **What do you think?**"

Four moves, 20 seconds, impossible to call rude.

### Back opinions with reasons

An opinion without a reason is noise. Always attach ONE:
- "…because the API isn't ready."
- "…since we tried this last quarter and it failed."
- "…given the client asked for Friday."

One reason beats three adjectives ("very very important").
""",
                "difficulty_min": 3,
                "difficulty_max": 8,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "You have a suggestion but you're not fully sure. Best phrasing?",
                        "choices": [
                            "Obviously we must move the deadline.",
                            "Could we consider moving the deadline by two days?",
                            "Trust me, move the deadline.",
                            "(Say nothing)",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "'Could we consider…?' is the tentative frame — it invites discussion instead of demanding agreement. Match strength to certainty.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Give an opinion on: 'Should standups be daily or twice a week?' Use the sandwich: acknowledge → view → reason → invite.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 5,
                        "explanation": "Model: 'I get why daily feels like overhead. In my view, daily is worth it because blockers surface a day earlier — but what do you think, would a 10-minute cap help?' Reason + invitation = professional.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which makes an opinion MORE persuasive?",
                        "choices": [
                            "Saying 'very very very important'",
                            "Attaching one concrete reason",
                            "Repeating the opinion three times",
                            "Speaking louder than others",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "One reason ('because the API isn't ready') persuades; adjectives, volume, and repetition just irritate. Evidence beats emphasis.",
                        "company_tags": [
                            "amazon",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You gave your opinion, the meeting moved on ignoring it, and it MATTERS. You should:",
                        "choices": [
                            "Send an angry email to all",
                            "Raise it 1:1 with the decision-maker after the meeting",
                            "Quit the team",
                            "Interrupt the next topic to repeat yourself",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "Let small things go (commit to the group). For things that genuinely matter, raise it 1:1 with the decision-maker after — not by re-fighting the whole room.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Disagree with a PEER (equal level) directly but respectfully, in 20 seconds. No sandwich needed — peers handle directness.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 8,
                        "explanation": "Model: 'I see it differently — I think cutting scope is safer than adding people, because onboarding alone takes two weeks. Want to stress-test both options?' Direct + reason + invitation. Peer-level honesty builds trust.",
                        "company_tags": [
                            "general",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-meetings-agree-disagree",
                "title": "Disagreeing Without Making Enemies",
                "practice_type": "speaking",
                "theory_md": """<!-- practice_type: speaking -->
## Disagreeing Without Making Enemies

In hierarchical Indian work culture, disagreeing with seniors feels
dangerous. But silent agreement with a bad plan is worse — for the
project and your career. Learn to disagree safely.

### The safe-disagreement ladder

1. **Ask a question** (safest): "Have we considered what happens if the
   API isn't ready by Friday?"
2. **Partial agreement**: "I agree with the goal. I'm wondering about
   the timeline — …"
3. **Alternative framing**: "Another way to look at it might be…"
4. **Direct but respectful**: "I have a concern about this approach…"

Start at #1 with seniors you don't know well. #4 is for people who
trust you.

### Phrases that disarm

- "I see your point. One thing I'd add…"
- "That's one way to look at it. Here's another angle…"
- "Can I play devil's advocate for a minute?"
- "Help me understand — what happens if…?"

### Never in disagreement

- ❌ "You're wrong." / "That's stupid." (attacks the person)
- ❌ Eye-rolls, sighs, interrupting (body language counts)
- ❌ Disagreeing in front of their boss to score points
- ❌ Bringing it up for the first time in a big meeting (talk 1:1 first
  for sensitive topics)

### The follow-through

If the group decides against you: "Okay, I'm on board — let's make it
work." Disagree honestly, commit fully. That's what seniors respect.
""",
                "difficulty_min": 4,
                "difficulty_max": 9,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "A senior proposes a plan you think will fail. Safest first move?",
                        "choices": [
                            "Email their manager after the meeting",
                            "Say 'You're wrong, this will fail.'",
                            "Stay silent and let it fail",
                            "Ask a question: 'Have we considered the API risk?'",
                        ],
                        "answer_index": 3,
                        "difficulty": 4,
                        "explanation": "A genuine question surfaces the risk without attacking anyone. It lets the senior discover the problem themselves — the most persuasive kind of disagreement.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Disagree with this plan using partial agreement: 'We'll rewrite the whole module in 2 days.'",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 6,
                        "explanation": "Model: 'I agree the module needs a rewrite. I'm wondering about the 2-day timeline though — the last refactor took a week. Could we scope it to the auth part first?' Agree on goal, question the plan, offer alternative.",
                        "company_tags": [
                            "tcs",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "The team overruled your objection and chose the risky plan. Best response?",
                        "choices": [
                            "\"Fine, but when it fails remember I warned you.\"",
                            "Complain about it in every later meeting",
                            "\"Okay, I'm on board — let's make it work.\"",
                            "Quietly stop contributing to that work",
                        ],
                        "answer_index": 2,
                        "difficulty": 8,
                        "explanation": "'Disagree and commit' — argue honestly, then back the decision fully. Seniors promote people who do this; they sideline people who sulk.",
                        "company_tags": [
                            "amazon",
                            "google",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You strongly disagree with a plan that'll be decided in tomorrow's big meeting. Best move TODAY?",
                        "choices": [
                            "Raise it privately with the proposer today, 1:1",
                            "Stay silent today, then attack it tomorrow in front of everyone",
                            "Email the whole company tonight",
                            "Hope someone else objects",
                        ],
                        "answer_index": 0,
                        "difficulty": 6,
                        "explanation": "Sensitive disagreements go 1:1 BEFORE the big meeting. Ambushing someone in front of 20 people makes them defend, not listen.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Play devil's advocate for 30 seconds on: 'We should rewrite everything in microservices.' Attack the idea, respect the people.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 9,
                        "explanation": "Model: 'Can I play devil's advocate? A full rewrite means 6 months with zero features while competitors ship. What if we extract just the payment service first and measure? Smaller bet, same learning.'",
                        "company_tags": [
                            "amazon",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-meetings-asking-questions",
                "title": "Asking Sharp Questions (Without Sounding Lost)",
                "practice_type": "speaking",
                "theory_md": """<!-- practice_type: speaking -->
## Asking Sharp Questions (Without Sounding Lost)

Good questions make you look smart. Bad questions ("What??") make you
look lost. The difference is framing.

### The clarification toolkit

- "Just to clarify — are we saying [your understanding]?"
- "Could you elaborate on [specific part]?"
- "When you say [term], do you mean [interpretation]?"
- "Sorry, I missed that — could you repeat the last part?"

Notice: every good question shows you were **listening** — it references
something specific.

### Questions that make you look good

- **Scope**: "What's the success criteria for this?"
- **Priority**: "If we can only do two of these, which two?"
- **Risk**: "What's the biggest risk you see here?"
- **Ownership**: "Who owns this after the handoff?"

These four work in almost any meeting. Memorize them.

### The 'dumb question' rule

If you're confused, **three other people are too** — they're just silent.
Asking "Sorry, could you explain what [term] means in this context?"
helps the whole room. Senior people ask clarifying questions constantly;
juniors nod and stay lost.

### Never

- ❌ "What??" / "Huh?" (sounds lost)
- ❌ Questions answered 2 minutes ago (you weren't listening)
- ❌ Five questions in a row (it's a meeting, not an interrogation)
- ❌ "This is a stupid question, but…" (don't insult your own question)
""",
                "difficulty_min": 3,
                "difficulty_max": 8,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "You didn't understand a technical term in a client call. Best?",
                        "choices": [
                            "Sorry, could you explain what 'webhook' means in this context?",
                            "(Nod and Google it later, staying confused now)",
                            "This is a stupid question, but what is webhook?",
                            "What??",
                        ],
                        "answer_index": 0,
                        "difficulty": 3,
                        "explanation": "Specific + polite + no self-insult. 'In this context' shows you're engaged, not lost. Three others in the call probably didn't know either.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Ask a clarifying question about this statement: 'We'll migrate the database next sprint.'",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 5,
                        "explanation": "Model: 'Just to clarify — are we saying a full migration, or just the user tables? And what's the rollback plan?' Specific, shows listening, surfaces risk.",
                        "company_tags": [
                            "infosys",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which question makes you look sharpest in a planning meeting?",
                        "choices": [
                            "If we can only do two of these, which two matter most?",
                            "So… what are we doing again?",
                            "Can you repeat everything from the start?",
                            "Why are we even having this meeting?",
                        ],
                        "answer_index": 0,
                        "difficulty": 7,
                        "explanation": "Priority questions ('if only two, which two?') force clarity and show strategic thinking. It's the single highest-value meeting question.",
                        "company_tags": [
                            "flipkart",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You have THREE questions about the plan. Best approach?",
                        "choices": [
                            "Ask none — figure it out alone",
                            "Fire all three rapid-fire",
                            "Ask all three, then two follow-ups each",
                            "Ask the most important one; save others for chat/after",
                        ],
                        "answer_index": 3,
                        "difficulty": 5,
                        "explanation": "One strong question asked well beats three asked rapidly. Ask the most important; park the rest for chat or after the call.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Ask the 'priority' question about YOUR team's current sprint, in 15 seconds.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 8,
                        "explanation": "Model: 'Quick one — if we can only ship two of these five tickets this sprint, which two matter most?' Then use the answer to focus your week. This question pays rent.",
                        "company_tags": [
                            "flipkart",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-meetings-summarizing",
                "title": "Summarizing: The Skill That Gets You Promoted",
                "practice_type": "speaking",
                "theory_md": """<!-- practice_type: speaking -->
## Summarizing: The Skill That Gets You Promoted

The person who summarizes the meeting controls the meeting's output —
and gets remembered. It's also the fastest way to look like leadership
material without a title.

### The 60-second meeting summary formula

**Decided → Owners → Dates → Open items**

> "So to recap: **we decided** to go with the phased rollout. **Priya
> owns** the API changes, **I own** the testing — both **by Friday**.
> **Open**: the pricing question, which we'll **circle back** to next
> week. Anything I missed?"

Four parts, 60 seconds. End with "Anything I missed?" — it invites
correction and shows humility.

### When to summarize

- **Mid-meeting** (every 20 min in long calls): "Just to make sure we're
  aligned — so far we've agreed on…"
- **End of meeting**: the full recap above.
- **After the meeting** (email): 5-line summary within an hour. This
  single habit will make you the most reliable person on the team.

### The written summary (copy this format)

> **Meeting:** Sprint planning, Oct 15
> **Decided:** Phased rollout starting Nov 1
> **Action items:**
> - Priya: API changes (by Fri)
> - Rahul: testing plan (by Fri)
> **Open:** pricing — revisit next Tue

### Why this gets you promoted

Managers promote people who create **clarity**. Summarizing is clarity as
a service. Do it consistently for 3 months and watch what happens.
""",
                "difficulty_min": 4,
                "difficulty_max": 8,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "The 4 parts of a meeting summary are:",
                        "choices": [
                            "Problems → Complaints → Blame → Excuses",
                            "Start time → End time → Duration → Breaks",
                            "Attendees → Agenda → Coffee → Goodbye",
                            "Decided → Owners → Dates → Open items",
                        ],
                        "answer_index": 3,
                        "difficulty": 4,
                        "explanation": "Decided (what), Owners (who), Dates (when), Open items (what's left). Miss any one and the meeting's value leaks away.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Summarize this in 45 seconds: 'The team discussed the login bug for 20 minutes. They decided to fix the API first. Priya will do it by Wednesday. The UI redesign was postponed.'",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 6,
                        "explanation": "Model: 'So to recap: we decided to fix the API first — Priya owns that, due Wednesday. The UI redesign is postponed to next sprint. Anything I missed?' Formula applied, under 45 seconds.",
                        "company_tags": [
                            "tcs",
                            "wipro",
                        ],
                    },
                    {
                        "qtype": "writing",
                        "prompt": "Write the 5-line email summary for the meeting above (meeting name, decided, action items with dates, open item).",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 8,
                        "explanation": "Model:\n**Meeting:** Bug triage, Oct 15\n**Decided:** Fix API first, UI redesign postponed\n**Action items:**\n- Priya: API fix (by Wed)\n**Open:** UI redesign timeline — revisit next sprint\nSend within an hour of the meeting. This is the reliability habit.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "25 minutes into a long call, people are drifting. You say:",
                        "choices": [
                            "Just to make sure we're aligned — so far we've agreed on X and Y, correct?",
                            "Start checking your phone too",
                            "'Can we end this meeting early?'",
                            "(Say nothing, let it drift)",
                        ],
                        "answer_index": 0,
                        "difficulty": 6,
                        "explanation": "Mid-meeting alignment checks ('so far we've agreed on X and Y — correct?') rescue drifting calls. Nobody minds; everyone benefits.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "listening",
                        "prompt": "Use TTS to listen: 'So to recap: we decided on the phased rollout, Priya owns the API by Friday, and pricing stays open.' Now repeat the 4 parts from memory.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 7,
                        "explanation": "Decided (phased rollout) → Owner (Priya) → Date (Friday) → Open (pricing). If you can echo the structure after one listen, you can summarize any meeting live.",
                        "company_tags": [
                            "general",
                        ],
                    },
                ],
            },
        ],
    },
    {
        "slug": "comm-presentations",
        "name": "Presentations",
        "description": (
            "Structuring talks, narrating slides, strong closings, handling Q&A, and presenting well on video calls."
        ),
        "lessons": [
            {
                "slug": "comm-presentations-opening",
                "title": "Openings: Hook Them in 60 Seconds",
                "practice_type": "speaking",
                "theory_md": """<!-- practice_type: speaking -->
## Openings: Hook Them in 60 Seconds

Audiences decide in the first minute whether to listen. "Good morning,
today I will present on…" loses them instantly. Open with a hook.

### The 4 hooks (pick one)

1. **Problem**: "Last month, our login page took 8 seconds to load. We
   lost 200 users a day. Here's how we fixed it."
2. **Question**: "What if I told you we can cut costs by 40% with one
   change?"
3. **Story**: "On Friday at 2am, our server crashed during the sale…"
4. **Number**: "Three numbers explain our quarter: 40%, 12 days, zero
   downtime."

### Then the roadmap (30 seconds)

After the hook, tell them the plan — audiences relax when they know
where they're going:

> "I'll cover three things: **what** the problem was, **how** we fixed
> it, and **what** we learned. About 10 minutes, then questions."

### Never open with

- ❌ "Good morning everyone, today I am going to present…" (they know)
- ❌ Apologies: "Sorry, I'm not a good speaker" (don't prime them)
- ❌ Reading the agenda slide word-for-word (they can read)
- ❌ "Can everyone see my screen?" as your first words (check tech
  BEFORE, open with the hook)

### The confidence cheat

Memorize your first 60 seconds word-for-word. Once the opening flows,
nerves drop and the rest gets easier. Every good speaker does this.
""",
                "difficulty_min": 3,
                "difficulty_max": 8,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Best opening for a presentation on fixing slow page loads?",
                        "choices": [
                            "Sorry, I'm not very good at presenting.",
                            "Last month our page took 8 seconds to load — we lost 200 users a day. Here's how we fixed it.",
                            "Can everyone see my screen? Okay so slide 1…",
                            "Good morning, today I will present on page load optimization.",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "Problem-hook with numbers grabs attention in 10 seconds. Agenda-reading and apologies lose the room before you start.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Write and deliver a 60-second opening for a talk on YOUR current project: hook + 3-part roadmap. Memorize it.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 6,
                        "explanation": "Model: 'In March, our checkout failed for 1 in 20 users — that's real money walking away. Today I'll show you what broke, how we fixed it in two weeks, and the one lesson I'd tattoo on every developer. Three parts, ten minutes.'",
                        "company_tags": [
                            "flipkart",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why memorize your first 60 seconds word-for-word?",
                        "choices": [
                            "It makes the presentation shorter",
                            "A smooth start kills nerves and the rest flows easier",
                            "Audiences can't understand unmemorized speech",
                            "Memorization is required by company policy",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "Nerves peak at the start. A memorized opening runs on autopilot, giving your confidence time to catch up before you improvise.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your hook landed — the room is listening. The next 30 seconds should be:",
                        "choices": [
                            "Another hook, then another",
                            "A 5-minute apology for being nervous",
                            "The roadmap: 3 parts, time, then questions",
                            "Your full biography",
                        ],
                        "answer_index": 2,
                        "difficulty": 5,
                        "explanation": "Hook creates attention; roadmap converts it into comfort. 'I'll cover X, Y, Z — 10 minutes, then questions.' Then deliver.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Open a talk on a BORING topic ('dependency updates') with a genuine hook. 45 seconds.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 8,
                        "explanation": "Model: 'Last Tuesday, a 2-year-old dependency nearly took down our checkout — one deprecated function, 40 minutes of downtime. Today: how a boring Friday task prevents the next outage. Three parts: what broke, the new process, and your action item.' Boring topic, human stakes.",
                        "company_tags": [
                            "general",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-presentations-slide-talk",
                "title": "Narrating Slides: Don't Read Them",
                "practice_type": "speaking",
                "theory_md": """<!-- practice_type: speaking -->
## Narrating Slides: Don't Read Them

The #1 presentation sin: reading every word on the slide. If you're
going to read it, email it — don't present it. Your job is to ADD what
the slide doesn't say.

### The slide-talk method

- **Slide shows**: the data, the diagram, the headline.
- **You say**: the story behind it, what it means, why it matters.

> Slide: "↓ 62% error rate"
> You: "This is the moment the fix went live — Tuesday 3pm. You can see
> the error rate fall off a cliff within the hour."

### Transition phrases (the glue)

- "Now let's look at…"
- "This brings us to…"
- "The key takeaway here is…"
- "What this means for us is…"
- "Let me show you what that looks like in practice…"

### Slide discipline

- **6 words per bullet, 6 bullets max** — if there's more text, it's a
  document, not a slide.
- **One idea per slide.** Two ideas = two slides.
- **Talk TO the audience**, not to the screen. Glance, don't stare.
- **Pause on key slides.** "Let that sink in…" — silence after an
  important number is powerful.

### The 10-20-30 rule (Guy Kawasaki)

10 slides, 20 minutes, 30-point font minimum. If your deck violates all
three, cut ruthlessly. Short decks respect the audience.
""",
                "difficulty_min": 3,
                "difficulty_max": 8,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your slide shows a graph of falling error rates. What should YOU say?",
                        "choices": [
                            "The story behind it — when the fix went live and what it means",
                            "Read the slide title word for word",
                            "Read the axis labels aloud: 'The x-axis shows time…'",
                            "Say 'As you can see on this slide' and move on",
                        ],
                        "answer_index": 0,
                        "difficulty": 3,
                        "explanation": "You add the story the slide can't tell. Reading labels aloud insults the audience's ability to read.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Narrate this slide in 30 seconds: [Slide: 'Deployment time: 45 min → 8 min']. Don't read the numbers — tell the story.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 5,
                        "explanation": "Model: 'This is my favorite slide. Three months ago every deploy ate 45 minutes of someone's evening. After we parallelized the pipeline — that change Ankit suggested — we're at 8 minutes. Deploys are now boring, which is exactly what we wanted.'",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A slide has 12 bullets of 20 words each. What do you do?",
                        "choices": [
                            "Split it: one idea per slide, 6x6 rule",
                            "Skip the slide entirely",
                            "Read all 12 bullets carefully so nothing is missed",
                            "Apologize for the slide and read it anyway",
                        ],
                        "answer_index": 0,
                        "difficulty": 7,
                        "explanation": "Dense slides are documents. Split into focused slides or move detail to an appendix. Never read walls of text aloud.",
                        "company_tags": [
                            "amazon",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You're showing a complex architecture diagram. You should:",
                        "choices": [
                            "Skip it — too complex to explain",
                            "Read every label aloud",
                            "Walk through it piece by piece, narrating the flow",
                            "Say 'as you can see' and move on",
                        ],
                        "answer_index": 2,
                        "difficulty": 5,
                        "explanation": "'As you can see' is the emptiest phrase in presentations. Walk the diagram: 'Requests enter here… then split to… notice this bottleneck…'",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Narrate a before/after in 30 seconds WITHOUT reading numbers off the slide: [Slide: 'Bug count: 47 → 3'].",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 8,
                        "explanation": "Model: 'This is six weeks of work in one picture. We started with a backlog that scared every new joiner — 47 open bugs. The triage process we built killed the noise: we're at 3, all minor. The story isn't the numbers — it's that the team trusts the tracker again.'",
                        "company_tags": [
                            "general",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-presentations-closing",
                "title": "Closings: End With Action, Not 'Thank You'",
                "practice_type": "speaking",
                "theory_md": """<!-- practice_type: speaking -->
## Closings: End With Action, Not 'Thank You'

Most presentations die with "…so, yeah. Thank you. Any questions?"
End with purpose instead: remind them what matters and what happens next.

### The 3-part close

1. **Recap** (the one thing to remember):
   "So the one thing I'd take away: the fix was a 3-line config change,
   not a rewrite."
2. **Action** (what happens next):
   "Next step: Priya rolls this out to staging on Monday. I'll share
   the runbook by Friday."
3. **Open the floor**:
   "Happy to take questions — especially on the rollout plan."

### Closing lines that work

- "If you remember one number from today: 62% fewer errors."
- "The ask from this room: approve the Monday rollout."
- "I'll leave you with this: the cheapest bug is the one we prevent."

### Never end with

- ❌ "So… yeah." (the most common and weakest ending)
- ❌ A slide that just says "Thank You" (wastes your final impression)
- ❌ "That's all from my side." (abrupt, no direction)
- ❌ New information in the closing (it confuses; close = reinforce)

### The final slide

Make it your **ask or takeaway**, not "Thank You". End on:
"Decision needed: approve staging rollout" — with your contact below.
People photograph final slides. Make yours worth photographing.
""",
                "difficulty_min": 2,
                "difficulty_max": 7,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Strongest way to end a project presentation?",
                        "choices": [
                            "'So… yeah. Thank you. Any questions?'",
                            "'That's all from my side.' (walk off)",
                            "Recap the one takeaway + state the next action + invite questions",
                            "A slide that only says 'Thank You'",
                        ],
                        "answer_index": 2,
                        "difficulty": 2,
                        "explanation": "Recap + action + questions gives the audience memory, direction, and engagement. 'So yeah' gives them nothing.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Deliver a 45-second closing for your project: one takeaway + next action + question invitation.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 6,
                        "explanation": "Model: 'So the one thing I'd take away: caching cut our load time from 5 seconds to under 1. Next step: I'm rolling this to the remaining services this week. Happy to take questions — especially on the rollout risks.'",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "writing",
                        "prompt": "Write your final slide text (not 'Thank You'): one takeaway + one decision needed + your contact. Max 20 words.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 4,
                        "explanation": "Model: 'Takeaway: 62% fewer errors after the fix. Decision needed: approve Monday rollout. Rahul — rahul@company.com'. People photograph final slides — make yours the ask, not a pleasantry.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "After 'any questions?' there's dead silence. You should:",
                        "choices": [
                            "Ask 'was my presentation bad?'",
                            "Stare at the audience until someone speaks",
                            "Say 'okay bye' and leave",
                            "Seed one yourself: 'One question I often get is…'",
                        ],
                        "answer_index": 3,
                        "difficulty": 5,
                        "explanation": "Seed a question: 'One question I often get is…' — it breaks the ice and lets you end on YOUR strongest point instead of awkward silence.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Close a 5-minute status update in 30 seconds: takeaway + next step + question invitation.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 7,
                        "explanation": "Model: 'So: migration's on track for Friday, testing starts Monday. Next step from me: the rollback runbook by EOD. Questions — especially on the rollback plan?' Short, directed, confident.",
                        "company_tags": [
                            "general",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-presentations-handling-qa",
                "title": "Handling Q&A: Surviving Tough Questions",
                "practice_type": "speaking",
                "theory_md": """<!-- practice_type: speaking -->
## Handling Q&A: Surviving Tough Questions

Q&A is where presentations are won or lost. The audience remembers how
you handled the hard question more than the slides.

### The 5 survival moves

1. **Repeat/paraphrase** (buys time + confirms understanding):
   "So you're asking whether this scales to 10x traffic — great question."
2. **Bridge to what you know**: "I don't have that number handy, but what
   I can tell you is…"
3. **Park it**: "That's outside today's scope — can I get back to you by
   tomorrow with the details?" (Then actually do it.)
4. **Bounce it**: "Has anyone else faced this? What worked for you?" (for
   discussion-style sessions)
5. **The honest 'I don't know'**: "I don't know — but I'll find out by
   Friday." (Said confidently, this BUILDS credibility.)

### The hostile question

Stay calm, slow down, and separate the person from the question:
- "That's a fair concern. Here's how we thought about it…"
- Never argue, never get defensive, never say "you don't understand."
- If they're right: "You're right — we should have covered that. Let me
  address it now."

### Rules

- **Listen fully** — don't answer halfway through the question.
- **One question at a time** — "Let's take the first part first…"
- **End Q&A yourself**: "We have time for one more…" (don't let it
  dribble; close strong)
- **Thank every questioner**: "Great question" — even the tough ones.
  It costs nothing and disarms everyone.
""",
                "difficulty_min": 4,
                "difficulty_max": 9,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Someone asks a question you can't answer. Best response?",
                        "choices": [
                            "Say 'Next question please' and move on",
                            "Make up a confident-sounding answer",
                            "I don't know — but I'll find out by Friday and share it with everyone.",
                            "Blame your teammate: 'Priya was supposed to cover that'",
                        ],
                        "answer_index": 2,
                        "difficulty": 4,
                        "explanation": "An honest 'I don't know + deadline' builds more trust than a bluff. Bluffs get exposed; honesty gets respected.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Handle this hostile question aloud: 'This plan obviously won't scale. Did you even think about that?' Stay calm, use the framework.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 7,
                        "explanation": "Model: 'That's a fair concern — scaling was our biggest debate. We tested to 5x current load and it held; beyond that we'd need sharding, which is phase 2. What scale are you worried about?' Calm + data + question back.",
                        "company_tags": [
                            "amazon",
                            "google",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Q&A is dragging with 5 minutes left and 3 hands up. You should:",
                        "choices": [
                            "Answer all three quickly in 30 seconds each",
                            "Let it continue 20 more minutes",
                            "Say 'no more questions' and walk off",
                            "Say 'We have time for one more' and close strong",
                        ],
                        "answer_index": 3,
                        "difficulty": 8,
                        "explanation": "'One more' respects the audience's time and ends you on a high. Rushed answers or abrupt exits undo a good talk.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Two people ask different questions at the same time. You:",
                        "choices": [
                            "Pick the easier one, ignore the other",
                            "'Let's take the first part first…' — one at a time",
                            "Say 'great questions!' and end the session",
                            "Answer both simultaneously",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "'Let's take the first part first' keeps control. Answering both at once garbles both.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Handle this in 30 seconds: 'Why didn't you just use X instead?' Paraphrase → bridge → answer. Stay warm.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 9,
                        "explanation": "Model: 'So you're asking why we built custom instead of using X — fair question. We evaluated X in March; it couldn't handle our transaction volume — it capped at 10k/min and we needed 100k. Happy to share the evaluation doc after.' Paraphrased, bridged, answered with data.",
                        "company_tags": [
                            "google",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-presentations-virtual",
                "title": "Virtual Presentations: Winning on Video Calls",
                "practice_type": "speaking",
                "theory_md": """<!-- practice_type: speaking -->
## Virtual Presentations: Winning on Video Calls

On video, you lose body language, eye contact, and room energy. Winners
adapt; losers read slides to black boxes.

### The setup (do once, benefit forever)

- **Camera at eye level** — stack books under the laptop. Looking down
  at the camera looks submissive; level looks confident.
- **Light on your face** — face a window or lamp. Backlit = silhouette.
- **Look at the camera**, not the faces — that's their "eye contact".
- **Mic check** — a ₹500 earphone mic beats a laptop mic. Audio matters
  more than video.

### The delivery adjustments

- **20% more energy** than in person — video flattens you.
- **Say names**: "Priya, what do you think?" — it wakes people up.
- **Pause for lag**: ask "Any questions?" then count to 5 silently.
- **Shorter segments**: 10 minutes max before interaction (poll, question,
  "type 1 in chat if…").

### Screen share discipline

- **Close** personal tabs, notifications, and chat apps. (Everyone has a
  horror story. Don't be one.)
- **Zoom to 150%** — what looks fine on your screen is tiny on theirs.
- **Share the specific window**, not your whole desktop.
- Have the deck open and ready BEFORE you start sharing — no fumbling.

### Engagement tricks

- Start with cameras-on request: "Cameras on if you can — it's nicer
  talking to faces."
- Cold-call kindly: "Rahul, you've worked on this — any thoughts?"
- End with a clear CTA in chat: paste the link/doc/action while talking.
""",
                "difficulty_min": 2,
                "difficulty_max": 6,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Most important virtual presentation setup fix?",
                        "choices": [
                            "The most expensive laptop",
                            "Wearing a suit",
                            "Camera at eye level + light on your face + look at the camera",
                            "A fancy virtual background",
                        ],
                        "answer_index": 2,
                        "difficulty": 2,
                        "explanation": "Eye-level camera and face lighting cost zero and change everything. People forgive backgrounds; they don't forgive silhouettes.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Practice: deliver your 60-second project opening (from the openings lesson) looking at your camera, with 20% more energy. Record it.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 5,
                        "explanation": "Watch the recording: are you looking at faces (wrong) or the lens (right)? Is your energy flat? One practice round fixes 80% of video awkwardness.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You ask 'Any questions?' on a video call and get silence. Best move?",
                        "choices": [
                            "Ask again louder",
                            "Say 'Okay nobody cares, moving on'",
                            "Assume no questions and rush on",
                            "Wait 5 full seconds, then call on someone by name kindly",
                        ],
                        "answer_index": 3,
                        "difficulty": 6,
                        "explanation": "Lag eats 2-3 seconds; shyness eats the rest. Count to 5, then 'Priya, any thoughts from the QA side?' — naming wakes people up without shaming.",
                        "company_tags": [
                            "tcs",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Biggest screen-share mistake?",
                        "choices": [
                            "Sharing without asking",
                            "Sharing in low resolution",
                            "Sharing your full desktop with personal tabs and notifications visible",
                            "Sharing for too long",
                        ],
                        "answer_index": 2,
                        "difficulty": 4,
                        "explanation": "Everyone has a horror story: personal chats, salary tabs, memes. Share the specific WINDOW, not the desktop — and close everything else first.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "writing",
                        "prompt": "Write your 5-item pre-call checklist (camera, light, mic, tabs, deck).",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 6,
                        "explanation": "Model: '1. Camera at eye level, light on face. 2. Earphones in, mic tested. 3. Personal tabs + notifications closed. 4. Deck open at 150% zoom. 5. Phone on silent, water nearby.' 2 minutes of prep prevents 100% of tech embarrassment.",
                        "company_tags": [
                            "general",
                        ],
                    },
                ],
            },
        ],
    },
]
