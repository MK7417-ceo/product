"""Seed content: English Communication — Modules 1-2 (Foundations, Workplace Vocabulary).

Part-file for the SkillForge curriculum seed. All content is original and
written for Indian professionals: real Indian-English mistakes to fix,
real office phrases, DO/DON'T examples. No filler — every lesson earns
its place.

Exports a single variable, ``MODULES``: a list of 2 module dicts, each
with nested lesson dicts and, inside those, question/practice dicts.

Module 1 ``comm-foundations``  — 5 lessons (sentence structure, tenses in
speech, articles, Indian-English mistakes, uncountable nouns).
Module 2 ``comm-workplace-vocab`` — 5 lessons (business vocabulary,
office phrasal verbs, email phrases, meeting phrases, office idioms).

Question dicts use qtype: mcq | speaking | writing | listening.
Non-MCQ items carry the model answer / guidance in ``explanation``.
"""
from __future__ import annotations

MODULES = [
    {
        "slug": "comm-foundations",
        "name": "Foundations",
        "description": (
            "Sentence structure, tenses in real speech, articles, the 12 Indian-English mistakes to kill, and uncountable nouns."
        ),
        "lessons": [
            {
                "slug": "comm-foundations-sentence-structure",
                "title": "Build Correct Sentences: Subject-Verb-Object",
                "practice_type": "writing",
                "theory_md": """<!-- practice_type: writing -->
## Build Correct Sentences: Subject-Verb-Object

English word order is **Subject → Verb → Object** (SVO). Hindi is
Subject → Object → Verb ("Main khana khata hun"). When you translate
word-for-word from Hindi, the verb lands in the wrong place.

### DO / DON'T

| ❌ Don't (Hindi order) | ✅ Do (English order) |
|---|---|
| I office yesterday went. | I went to the office yesterday. |
| She very well English speaks. | She speaks English very well. |
| We the client tomorrow will meet. | We will meet the client tomorrow. |
| He not coming is. | He is not coming. |

### The 3 checks before you speak a sentence

1. **Who?** (subject) → 2. **What action?** (verb) → 3. **Whom/what?** (object)
   - "The team (who) finished (action) the report (what)."

### Time and place go at the end

- ✅ "I submitted the report **yesterday**." / "…**in the morning**."
- ❌ "Yesterday I the report submitted." (verb buried)

### Questions flip the order

- Statement: "You are coming." → Question: "**Are** you coming?"
- Statement: "He finished it." → Question: "**Did** he finish it?"

**One rule to remember:** find the verb first, then put the doer before it
and the receiver after it. Everything else (time, place, manner) goes last.
""",
                "difficulty_min": 1,
                "difficulty_max": 6,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Which sentence uses correct English word order?",
                        "choices": [
                            "Very well she speaks English.",
                            "She English very well speaks.",
                            "She very well English speaks.",
                            "She speaks English very well.",
                        ],
                        "answer_index": 3,
                        "difficulty": 1,
                        "explanation": "English is Subject-Verb-Object: She (subject) speaks (verb) English (object). The adverb 'very well' comes after the object.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Fix the sentence: 'We the client tomorrow will meet.'",
                        "choices": [
                            "We meet will the client tomorrow.",
                            "Tomorrow we the client meet will.",
                            "We will meet the client tomorrow.",
                            "We tomorrow the client will meet.",
                        ],
                        "answer_index": 2,
                        "difficulty": 2,
                        "explanation": "Subject (We) → helping verb (will) → main verb (meet) → object (the client) → time (tomorrow) at the end.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "writing",
                        "prompt": "Rewrite in correct order: 'He not coming is to the meeting.'",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 3,
                        "explanation": "Model answer: 'He is not coming to the meeting.' The verb 'is' comes right after the subject; 'not' sits between the helping verb and the main verb.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your manager asks 'Did you finish the report?' You want to say yes. The natural reply is:",
                        "choices": [
                            "Yes, I yesterday finished it.",
                            "Yes, I finished it yesterday.",
                            "Yes, finished I it yesterday.",
                            "Yes, yesterday I it finished.",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "Keep SVO even in short answers: I (subject) finished (verb) it (object), then the time word last.",
                        "company_tags": [
                            "tcs",
                            "infosys",
                        ],
                    },
                    {
                        "qtype": "writing",
                        "prompt": "Turn into a question: 'The team delivered the release on Friday.'",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 6,
                        "explanation": "Model answer: 'Did the team deliver the release on Friday?' Questions use do/does/did + subject + base verb — the main verb loses its past tense.",
                        "company_tags": [
                            "general",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-foundations-tenses-speaking",
                "title": "Tenses When You Speak (Not Just in Exams)",
                "practice_type": "speaking",
                "theory_md": """<!-- practice_type: speaking -->
## Tenses When You Speak (Not Just in Exams)

You probably scored well in tense exercises at school — and still say
"I am working here since 2 years" in meetings. The exam tense and the
speaking tense are different skills. Fix the three that embarrass
professionals most.

### 1. "Since / for" needs Present Perfect Continuous

| ❌ Don't | ✅ Do |
|---|---|
| I am working here since 2 years. | I **have been working** here **for** 2 years. |
| She is living in Pune since 2020. | She **has been living** in Pune **since** 2020. |

Rule: **since** + point in time (2020, Monday, morning). **For** + duration
(2 years, 3 days). Both need **have/has been + verb-ing**.

### 2. Finished past vs connected present

- Past simple (finished, over): "I **completed** the module **yesterday**."
- Present perfect (result matters now): "I **have completed** the module —
  you can review it now."

In standups, present perfect is your friend: "I **have fixed** the bug"
(the fix exists now) vs "I **fixed** it yesterday" (just reporting history).

### 3. "Will" vs "going to" in commitments

- "I **will** send it today." — promise made now.
- "I **am going to** miss the deadline." — you already see it coming.

Never say "I will do it yesterday." Will is only for the future.

### Quick self-test before any meeting

Ask: is it still continuing? → have been doing. Is the result relevant now?
→ have done. Is it over and dated? → did.
""",
                "difficulty_min": 2,
                "difficulty_max": 7,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "You joined the company in 2023 and still work there. Correct sentence?",
                        "choices": [
                            "I work here since 2023.",
                            "I am working here since 2023.",
                            "I have been working here since 2023.",
                            "I was working here since 2023.",
                        ],
                        "answer_index": 2,
                        "difficulty": 2,
                        "explanation": "'Since 2023' (a point in time) with a still-continuing action needs present perfect continuous: have been working.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "In a standup you want to say the bug is fixed and ready for testing. Best?",
                        "choices": [
                            "I will fix the bug yesterday.",
                            "I have fixed the bug — it's ready for testing.",
                            "I fix the bug daily.",
                            "I am fixing the bug since morning.",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "Present perfect ('have fixed') connects the past action to the present result — exactly what a standup needs.",
                        "company_tags": [
                            "tcs",
                            "wipro",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Say aloud (30 sec): describe what you have been doing in your current role since you joined. Use 'have been' twice.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 5,
                        "explanation": "Model: 'I have been working as a developer since 2023. I have been handling the payment module for six months.' Record yourself and check every verb after since/for.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which is correct?",
                        "choices": [
                            "She has been living in Pune for three years.",
                            "She is living in Pune for since three years.",
                            "She has been living in Pune since three years.",
                            "She is living in Pune since three years.",
                        ],
                        "answer_index": 0,
                        "difficulty": 6,
                        "explanation": "'For three years' is a duration, so it pairs with 'for' + present perfect continuous. 'Since' only takes points in time.",
                        "company_tags": [
                            "infosys",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Give your last-week update in 45 seconds using: one past-simple sentence ('I completed…'), one present-perfect ('I have started…'), one future ('I will…').",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 7,
                        "explanation": "Model: 'I completed the login API on Tuesday. I have started the payment integration — the basic flow works. I will finish testing by Friday.' This is the exact rhythm of a professional standup.",
                        "company_tags": [
                            "tcs",
                            "infosys",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-foundations-articles",
                "title": "A, An, The — Three Small Words, Big Difference",
                "practice_type": "writing",
                "theory_md": """<!-- practice_type: writing -->
## A, An, The — Three Small Words, Big Difference

Missing articles is the fastest way to sound non-fluent: "He is engineer",
"I went to office", "Give me report". Three rules fix 90% of cases.

### Rule 1: First mention → a/an. Later mentions → the.

- "I saw **a** bug in the code. **The** bug crashes the login page."
- "She is **an** engineer." (an before vowel sounds: an hour, an MBA)

### Rule 2: Job titles and singular countable nouns need one

| ❌ Don't | ✅ Do |
|---|---|
| He is engineer. | He is **an** engineer. |
| Give me report. | Give me **the** report. |
| I have meeting. | I have **a** meeting. |

### Rule 3: "The" for the specific one you both know

- "I went to **the** office" (our office, the one we know) — not "to office".
- BUT: "I go to **work**" / "She is in **hospital**" (British) — some places
  drop the article by idiom. When unsure, "the office" is always safe.

### No article needed

- Plural/general: "Bugs are common in new code." (not "The bugs are common")
- Names: "Rahul", "Monday", "India" — no article.
- Meals: "Let's have lunch." (not "have a lunch")

### The 5-second check

Before a singular noun (engineer, report, meeting, issue), ask: did I put
a/an/the in front? If not, add one.
""",
                "difficulty_min": 1,
                "difficulty_max": 6,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Fill in: 'He is ___ engineer at TCS.'",
                        "choices": [
                            "the",
                            "a",
                            "an",
                            "(no article)",
                        ],
                        "answer_index": 2,
                        "difficulty": 1,
                        "explanation": "'Engineer' starts with a vowel sound, so 'an'. Job titles with singular nouns always need an article.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which is correct?",
                        "choices": [
                            "I went office yesterday.",
                            "I went to the office yesterday.",
                            "I went to office yesterday.",
                            "I went to an office yesterday.",
                        ],
                        "answer_index": 1,
                        "difficulty": 2,
                        "explanation": "'To office' without an article is Indian English. Standard: 'to the office' (the specific office you work at).",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "writing",
                        "prompt": "Fix: 'Give me report after you complete testing.'",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 3,
                        "explanation": "Model answer: 'Give me the report after you complete the testing.' Two missing articles: 'the report' (the specific one), 'the testing' (the testing we discussed).",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "First mention vs later mention: 'I found ___ issue. ___ issue blocks the release.'",
                        "choices": [
                            "an / The",
                            "a / A",
                            "the / The",
                            "the / An",
                        ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "First mention of a new thing takes a/an ('an issue'); once introduced, it becomes 'the issue' — the specific one we both know about.",
                        "company_tags": [
                            "infosys",
                        ],
                    },
                    {
                        "qtype": "writing",
                        "prompt": "Write 2 sentences about your project: introduce a new module with a/an, then refer to it with the.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 6,
                        "explanation": "Model: 'We built a notification service last sprint. The service now handles 10,000 alerts a day.' Check: first mention a/an, second mention the.",
                        "company_tags": [
                            "general",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-foundations-indian-english-mistakes",
                "title": "Kill These 12 Indian-English Mistakes",
                "practice_type": "speaking",
                "theory_md": """<!-- practice_type: speaking -->
## Kill These 12 Indian-English Mistakes

These phrases are understood in India but sound wrong — sometimes rude —
to international colleagues and interviewers. Replace them this week.

| ❌ Indian English | ✅ Say this instead | Why |
|---|---|---|
| Discuss **about** the issue | **Discuss** the issue | Discuss is already transitive |
| **Revert back** to me | **Get back** to me / **Reply** | Revert means 'go back to an earlier state' |
| **Do the needful** | Please **take care of** this / Please **handle** this | Sounds colonial to foreign ears |
| **Prepone** the meeting | **Move the meeting up** / Reschedule to an earlier date | Prepone exists only in Indian English |
| I **passed out** in 2022 | I **graduated** in 2022 | Pass out = faint, in US/UK English |
| He is **out of station** | He is **out of town** / travelling | Station = railway station abroad |
| I have a **doubt** | I have a **question** | Doubt = you suspect something is wrong |
| What is your **good name**? | What is **your name**? | Literal Hindi translation |
| I came **years back** | I came **years ago** | Back = direction, ago = time |
| I was there **only** | I was there | Trailing 'only' is pure Hindi-ism |
| **Itself** — "I only told him itself" | "I told him myself" / just drop it | Itself ≠ emphasis marker |
| **Kindly revert** ASAP | Please **reply** at the earliest | Double Indianism in one phrase |

### How to actually kill them

1. Pick **3** from this list you personally use.
2. Write the replacement on a sticky note on your monitor.
3. Catch yourself for one week. They die fast once noticed.

Interviewers at product companies notice these in the first two minutes.
Fixing them is the highest-ROI English work you can do.
""",
                "difficulty_min": 2,
                "difficulty_max": 8,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "A US client emails you. Which closing line is professional?",
                        "choices": [
                            "Do the needful by Friday.",
                            "Do needful and revert back.",
                            "Please take care of this by Friday.",
                            "Kindly do the needful ASAP.",
                        ],
                        "answer_index": 2,
                        "difficulty": 2,
                        "explanation": "'Do the needful' sounds archaic/colonial to native speakers. 'Please take care of this' / 'Please handle this' is direct and modern.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You want to ask a question in a meeting. What do you say?",
                        "choices": [
                            "I am having a doubt in the timeline.",
                            "I have a question about the timeline.",
                            "Mujhe timeline me doubt hai.",
                            "I have a doubt about the timeline.",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "'Doubt' implies you believe something is wrong. For neutral questions, always say 'I have a question'.",
                        "company_tags": [
                            "tcs",
                            "infosys",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Say aloud: tell a colleague the meeting moved from Friday to Wednesday — without using 'prepone'.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 5,
                        "explanation": "Model: 'The meeting has been moved up from Friday to Wednesday.' or 'We've rescheduled the meeting to Wednesday — two days earlier.' 'Prepone' will confuse anyone outside India.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "In a job interview: 'When did you ___ college?'",
                        "choices": [
                            "complete pass out",
                            "pass out of",
                            "graduate from",
                            "pass out from",
                        ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "'Pass out' means to faint in US/UK English — saying 'I passed out in 2022' in an interview gets a very wrong laugh. Use 'graduated'.",
                        "company_tags": [
                            "amazon",
                            "flipkart",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Record a 30-second self-introduction with zero Indianisms: no 'good name', no trailing 'only', no 'itself', no 'do the needful'.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 8,
                        "explanation": "Model: 'I'm Rahul Sharma, a backend developer with three years of experience at Infosys. I work on payment systems, mostly in Java and Spring Boot.' Listen back and count violations — aim for zero.",
                        "company_tags": [
                            "amazon",
                            "google",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-foundations-uncountable-nouns",
                "title": "'Informations' Is Not a Word — Uncountable Nouns",
                "practice_type": "writing",
                "theory_md": """<!-- practice_type: writing -->
## 'Informations' Is Not a Word — Uncountable Nouns

Some nouns have **no plural** in English. Adding an 's' is an instant
fluency giveaway. Memorize the 10 that appear in offices daily.

### The office hit-list (never add 's')

information, advice, furniture, equipment, knowledge, luggage, baggage,
news ("the news **is** good" — singular verb!), work (= job tasks),
software, hardware, research, feedback.

| ❌ Don't | ✅ Do |
|---|---|
| I need your **advices**. | I need your **advice**. / I need **a piece of advice**. |
| Send me the **informations**. | Send me the **information**. |
| We bought new **furnitures**. | We bought new **furniture**. / **some furniture**. |
| The **softwares** are ready. | The **software** is ready. |

### How to count the uncountable

Use a **counter phrase**: a piece of (advice, information, news, feedback),
an item of (furniture, equipment), a bit of (knowledge).

- "Two **pieces of feedback** came from the client."
- "We need **three items of equipment** for the new lab."

### Watch the verb

Uncountable nouns take **singular** verbs: "The news **is** good",
"Your feedback **was** helpful", "The equipment **has** arrived."
""",
                "difficulty_min": 1,
                "difficulty_max": 6,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Which sentence is correct?",
                        "choices": [
                            "Please share your feedbacks on the draft.",
                            "Please share a feedback on the draft.",
                            "Please share your feedback on the draft.",
                            "Please share the feedbacks on draft.",
                        ],
                        "answer_index": 2,
                        "difficulty": 1,
                        "explanation": "Feedback is uncountable — no 's', no 'a'. 'Your feedback' or 'a piece of feedback'.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Choose the correct verb: 'The news ___ good today.'",
                        "choices": [
                            "are",
                            "be",
                            "is",
                            "were",
                        ],
                        "answer_index": 2,
                        "difficulty": 2,
                        "explanation": "News looks plural but is singular — it takes 'is'. Same with 'the equipment has arrived'.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "writing",
                        "prompt": "Fix: 'He gave me many advices about the interviews.'",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 3,
                        "explanation": "Model answer: 'He gave me a lot of advice about the interviews.' or '…many pieces of advice…'. 'Advices' is never correct.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You need to say the office got 5 new chairs and 2 tables. Correct?",
                        "choices": [
                            "We got some new furnitures for the office.",
                            "We got some new furniture for the office.",
                            "We got a furniture for the office.",
                            "We got five furnitures and two furnitures.",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "Furniture is uncountable: 'some new furniture' or 'five pieces of furniture'. Never 'furnitures', and never 'a furniture'.",
                        "company_tags": [
                            "wipro",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "'The police ___ investigating the case.' (is/are)?",
                        "choices": [
                            "is",
                            "has",
                            "are",
                            "was",
                        ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "Tricky one: 'police' is PLURAL in English — 'The police ARE investigating.' Same with 'people are'. Uncountable ≠ always singular; learn the exceptions.",
                        "company_tags": [
                            "general",
                        ],
                    },
                ],
            },
        ],
    },
    {
        "slug": "comm-workplace-vocab",
        "name": "Workplace Vocabulary",
        "description": (
            "Business vocabulary, office phrasal verbs, email phrases, meeting phrases, and the idioms people actually use at work."
        ),
        "lessons": [
            {
                "slug": "comm-workplace-vocab-business-core",
                "title": "30 Business Words You Hear Every Day",
                "practice_type": "mcq",
                "theory_md": """<!-- practice_type: mcq -->
## 30 Business Words You Hear Every Day

Nobody teaches these in school, but every standup and email runs on them.
Learn them in context, not from a dictionary.

### The daily-standup set

- **Blocker** — something stopping your work. "The API downtime is a blocker."
- **Bandwidth** — free time/energy. "I don't have bandwidth this week."
- **Sync (up)** — a quick alignment meeting. "Let's sync after lunch."
- **ETA** — estimated time of arrival/completion. "What's the ETA on the fix?"
- **Deliverable** — what you must hand over. "The deliverable is the report."

### The planning set

- **Stakeholder** — anyone affected by the work (client, manager, team).
- **Action items** — tasks assigned in a meeting. "Two action items came out of the call."
- **Ownership** — who is responsible. "Rahul has ownership of the module."
- **Align** — get everyone on the same page. "We need to align on the scope."
- **Scope creep** — the work keeps growing beyond the plan.

### The status set

- **On track** — going as planned. **Off track** — behind.
- **WIP** (work in progress) — not finished yet.
- **Blocked** — can't move forward. **Unblocked** — the blocker is gone.
- **Roll out** — release gradually. "We're rolling out the feature to 10% of users."

### How to learn them

Don't memorize lists. After every meeting, write down **2 new words you
heard** and use each in one sentence the same day. In two weeks you'll own
the vocabulary of your workplace.
""",
                "difficulty_min": 2,
                "difficulty_max": 7,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your manager asks 'Do you have bandwidth for this?' She means:",
                        "choices": [
                            "Do you have free time and energy for this?",
                            "Do you have budget approval for this?",
                            "Do you have the technical skill for this?",
                            "Do you have internet speed for this?",
                        ],
                        "answer_index": 0,
                        "difficulty": 2,
                        "explanation": "In offices, 'bandwidth' means spare capacity — time and mental energy — not internet speed.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "'The payment gateway issue is a blocker.' A blocker is:",
                        "choices": [
                            "A type of software firewall",
                            "Something preventing the work from moving forward",
                            "A scheduled break",
                            "A person who blocks emails",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "A blocker is anything stopping progress — the single most useful standup word. Name your blockers explicitly.",
                        "company_tags": [
                            "tcs",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Give a 30-second status update using: blocker, ETA, on track.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 5,
                        "explanation": "Model: 'The login module is on track — ETA Friday. One blocker: I'm waiting on the API keys from the backend team.' Short, professional, complete.",
                        "company_tags": [
                            "infosys",
                            "wipro",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "After a planning meeting, your manager says 'send the action items'. You send:",
                        "choices": [
                            "Your personal to-do list",
                            "The meeting recording",
                            "The list of tasks assigned to each person with deadlines",
                            "The project budget",
                        ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "Action items = who does what by when, decided in the meeting. Sending them within an hour of the meeting marks you as reliable.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Explain 'scope creep' to a junior developer in 20 seconds, with a real example.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 7,
                        "explanation": "Model: 'Scope creep is when the work keeps growing beyond the plan — like when the client asked for login, then added OTP, then social login, all in the same sprint with no extra time.'",
                        "company_tags": [
                            "general",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-workplace-vocab-phrasal-verbs",
                "title": "Office Phrasal Verbs: Follow Up, Loop In, Touch Base",
                "practice_type": "speaking",
                "theory_md": """<!-- practice_type: speaking -->
## Office Phrasal Verbs: Follow Up, Loop In, Touch Base

Phrasal verbs (verb + preposition) carry half of office conversation.
Indians often know the verb but miss the preposition — and the meaning
changes completely.

### The 8 you need this month

| Phrasal verb | Meaning | Example |
|---|---|---|
| **follow up** | check on progress later | "I'll follow up with the client tomorrow." |
| **loop in** | add someone to the conversation | "Looping in Priya from QA." |
| **touch base** | make quick contact | "Let's touch base after the demo." |
| **circle back** | return to a topic later | "We'll circle back to the budget next week." |
| **ping** | send a quick message | "Ping me when it's deployed." |
| **roll out** | release in stages | "We're rolling out the update tonight." |
| **ramp up** | increase speed/effort | "We need to ramp up testing before launch." |
| **drill down** | go into detail | "Let's drill down into the error logs." |

### The preposition matters

- "Follow **up**" (check later) vs "follow" (walk behind someone).
- "Loop **in**" (include) — never "loop on" or just "loop".
- "Touch **base**" — from baseball; "touch basis" is a common mistake.

### Sound natural, not forced

Use **one or two** per conversation. Stuffing five phrasal verbs into one
sentence ("Let's touch base to circle back and drill down as we ramp up")
sounds like a parody. Natural beats impressive.
""",
                "difficulty_min": 3,
                "difficulty_max": 8,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "You want to add your manager to an email thread. You write:",
                        "choices": [
                            "I loop to Rahul.",
                            "Looping in Rahul from engineering.",
                            "Looping on Rahul from engineering.",
                            "Loop Rahul in the engineering.",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "'Loop in' is the fixed phrase — preposition 'in', person after it. 'Looping in [name]' is the standard email opener.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "'Let's circle back to this next week' means:",
                        "choices": [
                            "We'll draw circles on the whiteboard",
                            "We'll cancel this topic",
                            "We'll walk around the office next week",
                            "We'll return to this topic next week",
                        ],
                        "answer_index": 3,
                        "difficulty": 4,
                        "explanation": "Circle back = revisit later. It's the polite way to postpone a discussion without killing it.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Leave a 20-second voice note for a teammate: use 'follow up' and 'ping' naturally.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 6,
                        "explanation": "Model: 'Hey, I'll follow up with the client about the API keys tomorrow. Ping me if the build breaks before that.' One context, two verbs, zero forcing.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which sentence sounds natural?",
                        "choices": [
                            "Let's touch base after the demo to discuss feedback.",
                            "Let's base touch after the demo.",
                            "Let's touch base to circle back and drill down as we ramp up the rollout.",
                            "I will touch the base after demo.",
                        ],
                        "answer_index": 0,
                        "difficulty": 7,
                        "explanation": "One phrasal verb per sentence keeps you natural. Stacking four ('touch base… circle back… drill down… ramp up') sounds memorized, not fluent.",
                        "company_tags": [
                            "amazon",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "'Ramp up' vs 'roll out' — which is which?",
                        "choices": [
                            "Ramp up = increase effort; roll out = release in stages",
                            "Ramp up = release; roll out = increase effort",
                            "Both mean 'cancel'",
                            "Both mean 'schedule a meeting'",
                        ],
                        "answer_index": 0,
                        "difficulty": 8,
                        "explanation": "'Ramp UP = increase speed/effort ('ramp up testing'). 'Roll OUT = release in stages ('rolling out the update'). Up = intensity, out = distribution.",
                        "company_tags": [
                            "general",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-workplace-vocab-email-phrases",
                "title": "Email Phrases That Work (and Ones That Backfire)",
                "practice_type": "writing",
                "theory_md": """<!-- practice_type: writing -->
## Email Phrases That Work (and Ones That Backfire)

Emails are permanent. Tone mistakes live forever in inboxes. Learn the
phrases that get replies — and the ones that quietly damage you.

### Openers that work

- "Hope you're doing well." (safe, warm)
- "Following up on…" (not "This is a reminder" — less bossy)
- "Looping in…" (adding people)
- "As discussed," (referencing a call — professional)

### The polite request ladder (weak → strong)

1. "Could you please share the report by Friday?" ✅ best default
2. "Would you mind sharing…?" (very polite, slightly formal)
3. "Please share the report by Friday." (direct — fine with juniors/peers)
4. "Send me the report." ❌ (order — only for your direct reports, rarely)

### Phrases that backfire

| ❌ Avoid | Why | ✅ Instead |
|---|---|---|
| "As per my last email…" | Reads as: "can't you read?" | "Just bringing this back to your attention…" |
| "Please do the needful" | Archaic to native speakers | "Could you please take care of this?" |
| "Kindly revert ASAP" | Double Indianism | "Please reply at the earliest." |
| "This is to inform you" | Stiff, bureaucratic | "I wanted to let you know" / "Quick update:" |
| "PFA" (no context) | Cryptic | "Please find the report attached." |

### Closers

- Neutral: "Best regards," / "Thanks,"
- Warm: "Many thanks," / "Appreciate your help,"
- Never: "Yours obediently" (school, not office), "Thx" (too casual for clients)

**Golden rule:** read your email once imagining you're the receiver, tired,
at 6pm. If any line would irritate you — rewrite it.
""",
                "difficulty_min": 2,
                "difficulty_max": 9,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "You need a report from a colleague by Friday. Best line?",
                        "choices": [
                            "This is to inform you I need the report.",
                            "Do the needful and send the report ASAP.",
                            "Could you please share the report by Friday?",
                            "As per my last email, send the report.",
                        ],
                        "answer_index": 2,
                        "difficulty": 2,
                        "explanation": "'Could you please…' is the professional default — polite but clear, with a deadline. The others are passive-aggressive, archaic, or stiff.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "writing",
                        "prompt": "Rewrite politely: 'Send me the API docs. I asked yesterday also.'",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 5,
                        "explanation": "Model: 'Hi Ankit, just following up on the API docs — could you please share them when you get a chance? Thanks!' 'Just bringing this back…' beats 'As per my last email' every time.",
                        "company_tags": [
                            "tcs",
                            "infosys",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why is 'As per my last email…' risky?",
                        "choices": [
                            "It is too long for an email",
                            "It is only used in legal documents",
                            "It is grammatically incorrect",
                            "It sounds passive-aggressive, like blaming the reader for not reading",
                        ],
                        "answer_index": 3,
                        "difficulty": 6,
                        "explanation": "The grammar is fine — the tone is the problem. It implies 'I already told you, why haven't you done it?' Use 'Just bringing this back to your attention' instead.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "writing",
                        "prompt": "Write a 3-line email: you're looping in your manager on a delayed delivery, without blaming anyone.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 8,
                        "explanation": "Model: 'Hi team — looping in Rahul for visibility. The delivery is running two days behind due to the API changes; we're now targeting Thursday. I'll share an update tomorrow morning. Thanks!' Notice: facts, new date, next update — no blame, no drama.",
                        "company_tags": [
                            "amazon",
                            "flipkart",
                        ],
                    },
                    {
                        "qtype": "writing",
                        "prompt": "Rewrite professionally: 'PFA the report. Kindly revert.'",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 9,
                        "explanation": "Model: 'Hi team — please find the Q3 report attached. Please share your feedback by Thursday. Thanks!' 'PFA' without context is cryptic; 'kindly revert' is a double Indianism.",
                        "company_tags": [
                            "tcs",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-workplace-vocab-meeting-phrases",
                "title": "Meeting Phrases: Jump In Without Interrupting",
                "practice_type": "speaking",
                "theory_md": """<!-- practice_type: speaking -->
## Meeting Phrases: Jump In Without Interrupting

In Indian meetings many people stay silent because they don't know how to
enter the conversation politely. These 10 phrases are your entry tickets.

### Entering the conversation

- "Can I jump in here?" / "Can I add something?"
- "Sorry to interrupt — quick point on that…"
- "Building on what Priya said…"

### Giving your view

- "In my view, we should…"
- "I'd suggest we…"
- "From my side, the risk is…"

### Agreeing and disagreeing

- Agree: "That makes sense." / "I'm on board with that."
- Soft disagree: "I see your point. However, …" / "That's one way to look at it. Another angle…"
- Never: "You are wrong." → "I have a slightly different take…"

### Asking without sounding lost

- "Could you elaborate on that?" (not "What??")
- "Just to clarify — are we saying…?"
- "Sorry, I missed that — could you repeat the last part?"

### Parking a topic

- "Let's take this offline." (= discuss separately, not in this meeting)
- "Can we park that for now and come back to it?"

### The confidence trick

You don't need perfect sentences to speak in meetings. One clear phrase
("In my view…") + one clear point beats five minutes of perfect silence.
Prepare **one** thing to say before every meeting — then say it early.
""",
                "difficulty_min": 3,
                "difficulty_max": 8,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "You disagree with a senior's proposal. Most professional?",
                        "choices": [
                            "I don't agree. That's a bad idea.",
                            "You are wrong about this.",
                            "I see your point. However, I have a slightly different take…",
                            "(Stay silent)",
                        ],
                        "answer_index": 2,
                        "difficulty": 3,
                        "explanation": "'I see your point. However…' respects the person while challenging the idea. Direct contradiction ('you are wrong') ends your credibility in that room.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Practice aloud: interrupt politely with 'Can I jump in here?' then give one opinion about daily standups in 20 seconds.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 5,
                        "explanation": "Model: 'Can I jump in here? In my view, standups would be sharper if we capped updates at one minute each.' Entry phrase + opinion + reason — the full meeting move.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "'Let's take this offline' means:",
                        "choices": [
                            "Let's cancel the discussion forever",
                            "Let's discuss this separately, not in this meeting",
                            "Let's meet in person instead of online",
                            "Let's disconnect from the internet",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "'Take offline' = park it for a smaller/separate discussion. It's how professionals keep meetings on track without dismissing anyone.",
                        "company_tags": [
                            "tcs",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "You missed a key point in a client call. Ask for repetition professionally in one sentence.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 7,
                        "explanation": "Model: 'Sorry, I missed that last part — could you please repeat it?' Never say 'What?' or go silent. Asking for clarity is professional; pretending to understand is not.",
                        "company_tags": [
                            "infosys",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Run a 30-second meeting entry: interrupt politely + agree with someone + add your own point.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 8,
                        "explanation": "Model: 'Can I jump in here? I agree with Priya on the phased approach — and I'd add that we should start with the low-traffic service to de-risk it.' Entry + agreement + addition = the complete meeting move.",
                        "company_tags": [
                            "general",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-workplace-vocab-office-idioms",
                "title": "Office Idioms: What 'Ballpark Figure' Actually Means",
                "practice_type": "mcq",
                "theory_md": """<!-- practice_type: mcq -->
## Office Idioms: What 'Ballpark Figure' Actually Means

Idioms confuse everyone at first — including native speakers from other
industries. Learn the 8 you'll actually hear; ignore the other 800.

| Idiom | Meaning | Example |
|---|---|---|
| **ballpark figure** | rough estimate | "Give me a ballpark figure for the cost." |
| **low-hanging fruit** | easy wins first | "Let's pick the low-hanging fruit this sprint." |
| **move the needle** | make a noticeable difference | "Will this feature move the needle on retention?" |
| **deep dive** | detailed analysis | "Let's do a deep dive into the crash logs." |
| **win-win** | good for both sides | "This timeline is a win-win." |
| **on the same page** | in agreement | "Are we on the same page about the scope?" |
| **think outside the box** | be creative | (Cliché — use sparingly) |
| **game-changer** | big improvement | (Overused — use only for real breakthroughs) |

### Rules for using idioms

1. **Understand before you use.** Never say an idiom you couldn't explain.
2. **One per conversation max.** Two idioms in one sentence sounds rehearsed.
3. **Match your audience.** Fine with peers; go simpler with clients and
   non-native speakers — clarity beats style.
4. **Never in writing to clients.** "As per the low-hanging fruit…" in a
   formal email looks unprofessional. Idioms are spoken-register.

### If you don't understand one in a meeting

Ask: "Sorry — when you say 'ballpark figure', do you mean a rough
estimate?" Nobody minds; everyone has been there.
""",
                "difficulty_min": 2,
                "difficulty_max": 7,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your manager asks for a 'ballpark figure' for the project cost. She wants:",
                        "choices": [
                            "A rough estimate, not an exact number",
                            "A figure drawn in a circle",
                            "The cost of a baseball stadium",
                            "The final audited budget",
                        ],
                        "answer_index": 0,
                        "difficulty": 2,
                        "explanation": "Ballpark figure = approximate number to start planning with. Give a range ('roughly 8-10 lakhs') and say you'll refine it.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "'Let's focus on the low-hanging fruit this quarter' means:",
                        "choices": [
                            "Avoid difficult problems forever",
                            "Only work on agriculture projects",
                            "Buy fruit for the office",
                            "Do the easy, high-value tasks first",
                        ],
                        "answer_index": 3,
                        "difficulty": 4,
                        "explanation": "Low-hanging fruit = easy wins. It's prioritization advice: grab quick victories before tackling hard problems.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Explain 'move the needle' to a junior in one sentence, with a work example.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 6,
                        "explanation": "Model: \"'Move the needle' means making a difference big enough to notice — like when our caching fix moved the needle on page load time from 5 seconds to 1.\" If you can teach it, you own it.",
                        "company_tags": [
                            "flipkart",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You're writing a FORMAL email to a client. Which is safe?",
                        "choices": [
                            "Idioms are mandatory in formal emails",
                            "Use as many idioms as possible to impress",
                            "Avoid idioms — use plain words: 'a rough estimate'",
                            "'As per the low-hanging fruit, kindly do the needful'",
                        ],
                        "answer_index": 2,
                        "difficulty": 7,
                        "explanation": "Idioms are spoken-register. In formal client writing, plain words win: 'a rough estimate' beats 'a ballpark figure', 'easy first steps' beats 'low-hanging fruit'.",
                        "company_tags": [
                            "general",
                        ],
                    },
                ],
            },
        ],
    },
]
