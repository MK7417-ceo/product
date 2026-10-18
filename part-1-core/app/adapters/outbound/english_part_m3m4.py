"""Seed content: English Communication — Modules 3-4 (Speaking Skills, Email Writing).

Part-file for the SkillForge curriculum seed. All content is original,
written for Indian professionals: pronunciation pain points from
mother-tongue influence, fluency drills that actually work, and email
templates you can copy-paste at work tomorrow.

Exports a single variable, ``MODULES``: 2 module dicts.

Module 3 ``comm-speaking``      — 6 lessons (pronunciation, fluency,
small talk, thinking in English, filler words, pace & clarity).
Module 4 ``comm-email-writing`` — 5 lessons (formal vs informal, subject
lines, requesting, apologizing, follow-ups — with real templates).

Question dicts use qtype: mcq | speaking | writing | listening.
"""
from __future__ import annotations

MODULES = [
    {
        "slug": "comm-speaking",
        "name": "Speaking Skills",
        "description": (
            "Pronunciation fixes for Indian speakers, fluency drills, small talk, thinking in English, killing filler words, pace and clarity."
        ),
        "lessons": [
            {
                "slug": "comm-speaking-pronunciation-basics",
                "title": "Pronunciation: The 5 Sounds Indians Get Wrong",
                "practice_type": "speaking",
                "theory_md": """<!-- practice_type: speaking -->
## Pronunciation: The 5 Sounds Indians Get Wrong

You don't need a British accent. You need **clarity** — being understood
on the first try. These 5 sounds cause 80% of misunderstandings.

### 1. V vs W

- **V**: upper teeth touch lower lip — "vine, very, voice"
- **W**: lips round, no teeth — "wine, where, work"
- ❌ "I went to **vork**" → ✅ "I went to **work**" (round your lips)

### 2. TH (think / this)

Put your tongue **between your teeth** and blow:
- "think, three, thank" (unvoiced — just air)
- "this, that, they" (voiced — add voice)
- ❌ "I **tink** so" → ✅ "I **think** so"

### 3. Word stress (the hidden rule)

English stresses one syllable: **PHO**-to-graph, pho-**TO**-gra-phy.
Wrong stress confuses listeners more than wrong sounds.

- **DE**-ve-lop (verb) vs de-**VE**-lop-ment (noun)
- **PRE**-sent (gift) vs pre-**SENT** (to show)

### 4. T/D at word ends

Don't drop them: "test" not "tes", "and" not "an", "first" not "firs".
Final consonants carry meaning: "I work**ed**" (past) vs "I work".

### 5. The flat Indian intonation

Indian English often stays flat. English uses **rise and fall**:
- Questions rise: "Are you coming↗?"
- Statements fall: "I'm coming↘."
- Lists rise then fall: "We need time↗, budget↗, and people↘."

### The 10-minute daily drill

1. Pick one paragraph (news, email).
2. Read it aloud **slowly**, exaggerating V/W and TH.
3. Record on your phone. Compare day 1 vs day 14. The gap will shock you.
""",
                "difficulty_min": 2,
                "difficulty_max": 7,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "How do you physically make the 'th' sound in 'think'?",
                        "choices": [
                            "Teeth together, hum",
                            "Tongue between teeth, blow air out",
                            "Tongue behind teeth, like 't'",
                            "Lips rounded, like 'w'",
                        ],
                        "answer_index": 1,
                        "difficulty": 2,
                        "explanation": "TH needs the tongue visibly between the teeth with air flowing. 'Tink' happens when the tongue stays behind the teeth.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Say aloud 5 times, exaggerating: 'Very well, we work with vendors.' (V/W drill)",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 4,
                        "explanation": "Check: 'Very' (teeth on lip), 'well' (rounded lips), 'we work with' (all rounded), 'vendors' (teeth on lip). Record and listen — no 'vork' allowed.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "listening",
                        "prompt": "Use TTS to listen: 'I think this is the third Thursday.' Repeat it, then say what you noticed about the th-sounds.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 5,
                        "explanation": "Target: 'think' (unvoiced th, just air), 'this' (voiced th, with voice), 'third' (unvoiced), 'Thursday' (unvoiced). Four th-sounds, two types — feel the difference.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which stress pattern is correct for the noun 'development'?",
                        "choices": [
                            "de-ve-LOP-ment",
                            "de-ve-lop-MENT",
                            "DE-ve-lop-ment",
                            "de-VE-lop-ment",
                        ],
                        "answer_index": 3,
                        "difficulty": 6,
                        "explanation": "de-VE-lop-ment — stress on the second syllable. Wrong stress ('DE-velopment') is the #1 reason Indians get asked to repeat themselves.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Record yourself saying: 'The first test failed, and the third worked.' Check: final T/D sounds + th in 'third'.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 7,
                        "explanation": "Target: 'firsT TesT' (don't drop the T), 'anD' (don't drop the D), 'THird' (tongue out). These tiny endings are what separate clear from unclear speech.",
                        "company_tags": [
                            "tcs",
                            "infosys",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-speaking-fluency-building",
                "title": "Fluency Drills That Actually Work",
                "practice_type": "speaking",
                "theory_md": """<!-- practice_type: speaking -->
## Fluency Drills That Actually Work

Fluency is **not** vocabulary. It's speed of retrieval — getting words out
without freezing. These three drills build it. All need is 15 minutes daily.

### Drill 1: Shadowing (the #1 fluency builder)

1. Play a 1-minute clip of clear English (news anchor, podcast).
2. Speak **along with** the speaker, half a second behind — like an echo.
3. Copy rhythm, pauses, stress — not just words.

Do this 10 minutes daily for a month. It rewires your mouth muscles.

### Drill 2: The 1-minute talk

Pick a topic ("my weekend", "my project"). Speak for 60 seconds **without
stopping**. Rules:
- No pausing to search for words — say "uh" and keep going.
- If stuck, describe around it: "the thing you use to…"
- Timer is law. Fluency = continuity, not perfection.

### Drill 3: The retell

After any meeting or video, retell what happened in 60 seconds in English.
This converts passive listening into active speaking — the exact skill
meetings demand.

### What kills fluency (stop doing these)

- **Translating** from Hindi in your head (next lesson fixes this).
- **Perfectionism** — waiting for the perfect word. Say the 80% word now.
- **Silent reading** — reading without moving your mouth builds zero
  speaking muscle. Always read aloud.

### Measure it

Record a 1-minute talk on day 1 and day 30. Count: filler words, long
pauses (>2 sec), self-corrections. All three should drop by half.
""",
                "difficulty_min": 3,
                "difficulty_max": 9,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "What is 'shadowing' as a fluency drill?",
                        "choices": [
                            "Standing in someone's shadow while they speak",
                            "Speaking along with a recording, half a second behind the speaker",
                            "Writing down everything someone says",
                            "Repeating words the next day from memory",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "Shadowing = echo-speaking with a recording. It trains rhythm, stress, and speed simultaneously — the closest thing to a fluency shortcut.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Do a 1-minute talk RIGHT NOW: describe your current project. No stopping, no long pauses. Go.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 5,
                        "explanation": "Done is better than perfect. If you froze, note WHERE — that's your retrieval gap. Repeat the same topic tomorrow; it will be smoother. That's fluency being built.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "During a 1-minute talk you forget the word 'deadline'. Best recovery?",
                        "choices": [
                            "Apologize and end the talk",
                            "Say 'the date we must finish by' and keep going",
                            "Stop and think silently until the word comes",
                            "Switch to Hindi for that word",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "Circumlocution (describing around a missing word) is a real fluency skill — native speakers do it too. Stopping kills flow; describing keeps it.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Retell your last meeting in 60 seconds: what was decided, who does what. Record it.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 8,
                        "explanation": "Model: 'We discussed the login bug. Priya will fix the API by Wednesday, I'll test it Thursday, and we decided to skip the redesign for now.' Meeting-retell is the highest-value speaking drill for office life.",
                        "company_tags": [
                            "tcs",
                            "wipro",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "2-minute talk, no stopping: 'My biggest work challenge this year.' Record it and count fillers + long pauses.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 9,
                        "explanation": "This is the fluency exam. If you did 60 seconds last week, 120 seconds now proves growth. Count: fillers, pauses over 2 seconds, self-corrections. All three should be dropping week over week.",
                        "company_tags": [
                            "general",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-speaking-small-talk",
                "title": "Small Talk: The Skill That Gets You Noticed",
                "practice_type": "speaking",
                "theory_md": """<!-- practice_type: speaking -->
## Small Talk: The Skill That Gets You Noticed

In Indian offices, people jump straight to work. In global companies,
the 2 minutes before a meeting starts — the small talk — build the
relationships that get you recommended, mentored, and promoted.

### The safe ladder (start shallow, go deeper only if invited)

1. **Weekend**: "How was your weekend?" / "Any plans for the weekend?"
2. **Work-adjacent**: "How's the new project going?" / "Busy week?"
3. **Interests**: "Seen any good movies lately?" (only after rapport)

Never start with: salary, politics, religion, personal problems.

### Phrases that open doors

- "How was your weekend?" → they answer → "**Oh nice —** where did you go?"
  (one follow-up question = you actually listened)
- "I noticed you… [presented well / handled that client call nicely]."
  (specific compliments are remembered for months)
- "How long have you been with the team?"

### The exit (as important as the entry)

- "Anyway, I won't keep you — see you in the standup!"
- "Great chatting — let's catch up properly sometime."

Don't just walk away mid-conversation. A 5-second exit keeps the warmth.

### For introverts: the 2-minute rule

You don't need to be chatty. **Two minutes** of small talk before meetings
is enough. Prepare one question ("How was your weekend?") and one
follow-up. That's the whole skill.
""",
                "difficulty_min": 2,
                "difficulty_max": 7,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "A teammate says 'My weekend was great — we went trekking.' Best response?",
                        "choices": [
                            "Trekking is dangerous, you should be careful.",
                            "Oh nice — where did you go trekking?",
                            "My weekend was also good.",
                            "Okay.",
                        ],
                        "answer_index": 1,
                        "difficulty": 2,
                        "explanation": "One follow-up question ('where did you go?') shows you listened. 'Okay' kills the conversation; unsolicited advice annoys.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Practice: start a 30-second small-talk opener for a video call waiting room. Weekend question + follow-up.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 4,
                        "explanation": "Model: 'Hi! How was your weekend? … Oh, you watched a match — which one? I missed it.' Two turns, warm, zero awkwardness.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which topic should you AVOID in small talk with a new international colleague?",
                        "choices": [
                            "Their salary and appraisal",
                            "A recent festival",
                            "Their commute",
                            "Their weekend plans",
                        ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "Salary, politics, religion, health problems — never in small talk. Weekends, festivals, food, commute are safe worldwide.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Give a specific compliment to a colleague (real or imagined) + a clean 5-second exit line.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 6,
                        "explanation": "Model: 'I thought you handled the client questions really well in today's demo — especially the pricing one. Anyway, I won't keep you — see you tomorrow!' Specific + exit = memorable.",
                        "company_tags": [
                            "amazon",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You're making small talk with a SENIOR leader (VP). Best approach?",
                        "choices": [
                            "Ask about their salary",
                            "Ask one genuine question and listen attentively",
                            "Avoid them entirely",
                            "Pitch your achievements for 5 minutes",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "With seniors: one genuine question, then LISTEN. Don't pitch yourself, don't monologue. 'How are you finding the new org structure?' + attention beats 5 minutes of self-promotion.",
                        "company_tags": [
                            "general",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-speaking-thinking-in-english",
                "title": "Stop Translating: Start Thinking in English",
                "practice_type": "speaking",
                "theory_md": """<!-- practice_type: speaking -->
## Stop Translating: Start Thinking in English

The freeze before you speak? That's translation — Hindi thought → English
words → check grammar → speak. Three steps where one should do. Kill the
middle steps.

### Why translation fails

Hindi and English don't map 1:1. "Mujhe khana khana hai" → "I want to eat
food" works, but "Mujhe doubt hai" → "I have a doubt" fails (lesson 4).
Every translation is a chance to import a Hindi-ism.

### The 4-week retraining plan

**Week 1 — Narrate your day.** While brushing teeth, cooking, commuting:
describe what you're doing in English, silently. "I'm making tea. The
water is boiling. I need two spoons of sugar." Low stakes, high reps.

**Week 2 — Think in chunks, not words.** Stop building sentences
word-by-word. Learn ready chunks: "As far as I know…", "The thing is…",
"What I mean is…", "Let me put it this way…". Fluent speakers run on
chunks, not grammar rules.

**Week 3 — Dream in English.** Before sleep, replay your day in English
for 2 minutes. No pressure, no audience — pure thinking practice.

**Week 4 — The 3-second rule.** In real conversations, allow yourself max
3 seconds of thinking, then speak with whatever English you have. The
deadline forces direct thinking.

### Emergency phrases (buy time WITHOUT translating)

- "Let me think about that for a second…"
- "That's a good question…"
- "What I'm trying to say is…"

These sound fluent AND give your brain the second it needs.
""",
                "difficulty_min": 3,
                "difficulty_max": 9,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Why does word-for-word translation from Hindi cause mistakes?",
                        "choices": [
                            "Translation is always perfect, it never causes mistakes",
                            "Hindi and English have different structures and idioms that don't map 1:1",
                            "Hindi has more words than English",
                            "English grammar is completely random",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "Different word order (SOV vs SVO), different idioms ('good name', trailing 'only') — every translation step risks importing a Hindi pattern.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Narrate what you're doing RIGHT NOW in English for 30 seconds, silently or aloud. No Hindi allowed.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 5,
                        "explanation": "Model: 'I'm sitting at my desk. I'm reading a lesson on my phone. There's a glass of water next to me.' Boring is fine — the point is direct English thinking, not interesting content.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "In a meeting you need 5 seconds to think. Most fluent option?",
                        "choices": [
                            "Let me think about that for a second…",
                            "Sorry, my English is not good.",
                            "Uhh… matlab… I mean…",
                            "(long silence while translating)",
                        ],
                        "answer_index": 0,
                        "difficulty": 6,
                        "explanation": "'Let me think about that for a second' is what native speakers say too — it buys time while sounding completely fluent. Never apologize for your English mid-meeting.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Answer in 30 seconds WITHOUT preparing: 'What did you learn this week?' Use one chunk phrase ('What I mean is…' / 'The thing is…').",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 8,
                        "explanation": "The 3-second rule in action: start speaking before you feel ready, lean on a chunk phrase. Record it — notice how the chunk carried you through the thinking gap.",
                        "company_tags": [
                            "tcs",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Describe your morning routine in English for 45 seconds. Zero Hindi words allowed — if stuck, describe around the word.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 9,
                        "explanation": "The no-Hindi constraint forces direct thinking. Every time you route around a missing word ('the thing you heat water in' for kettle), you're building the circumlocution muscle that saves you in meetings.",
                        "company_tags": [
                            "general",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-speaking-filler-words",
                "title": "Filler Word Detox: Actually, Basically, Like…",
                "practice_type": "speaking",
                "theory_md": """<!-- practice_type: speaking -->
## Filler Word Detox: Actually, Basically, Like…

Fillers are the words you say while thinking: "actually", "basically",
"like", "you know", "I mean", "sort of". A few are natural. Twenty per
minute makes you sound unsure — even when you're right.

### The Indian top 5 (count yours for a day)

1. **"Actually…"** at the start of every sentence — use only for corrections:
   "Actually, the deadline is Friday, not Thursday."
2. **"Basically…"** — adds nothing 90% of the time. Delete and check: the
   sentence still works.
3. **"Like…"** — "It was, like, really good." Fine once; painful ten times.
4. **"You know…"** — seeking agreement you don't need.
5. **"I mean…"** — okay for clarifying, not as every sentence starter.

### The detox (2 weeks)

**Week 1 — Count.** Record one meeting or call. Count your top filler.
Most people are shocked: 30-50 in 10 minutes is normal at first.

**Week 2 — Replace with silence.** A pause is powerful; a filler is weak.
- ❌ "So basically the API is, like, down, you know?"
- ✅ "The API is down. [pause] We're fixing it now."

Pausing makes you sound **confident**. Fillers make you sound nervous.
Same content, opposite impression.

### What to keep

"Well…" to start a thoughtful answer, "So…" to summarize — used once or
twice, these are natural. The poison is in the dose.
""",
                "difficulty_min": 2,
                "difficulty_max": 7,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "When is 'actually' used CORRECTLY?",
                        "choices": [
                            "To correct something: 'Actually, the deadline is Friday, not Thursday.'",
                            "At the start of every sentence for emphasis",
                            "Instead of 'yes' in every answer",
                            "Three times in one sentence for fluency",
                        ],
                        "answer_index": 0,
                        "difficulty": 2,
                        "explanation": "'Actually' means 'in fact, contrary to what was said/thought' — it's a correction word. As a sentence starter habit, it's pure filler.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Say this WITHOUT fillers: 'So basically the deployment is, like, delayed, you know, because of, I mean, the server issue.'",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 4,
                        "explanation": "Model: 'The deployment is delayed because of a server issue.' Seven words, zero fillers, twice as professional. Record both versions and feel the difference.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You need a moment to think mid-sentence. Best option?",
                        "choices": [
                            "Laugh nervously",
                            "Say 'like, you know, basically' while thinking",
                            "Repeat the last three words",
                            "Pause silently for a second",
                        ],
                        "answer_index": 3,
                        "difficulty": 6,
                        "explanation": "Silence signals confidence — you're choosing words. Fillers signal panic. Senior leaders pause; juniors fill.",
                        "company_tags": [
                            "amazon",
                            "google",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your MANAGER says 'basically' in every sentence. You should:",
                        "choices": [
                            "Ignore it — correcting others' fillers is not your job",
                            "Count aloud so they notice",
                            "Mimic them to build rapport",
                            "Correct them mid-meeting",
                        ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "Never correct your manager's (or anyone's) fillers — it's not your job and it embarrasses them. Fix your own speech; ignore others'.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Explain your project in 30 seconds with MAXIMUM 2 fillers. Record and count afterwards.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 7,
                        "explanation": "The constraint forces the pause-instead-of-filler habit. Most people discover their '2 fillers' were actually 9 — that's the awareness that starts the detox.",
                        "company_tags": [
                            "general",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-speaking-pace-clarity",
                "title": "Slow Down: Pace and Clarity Beat Speed",
                "practice_type": "speaking",
                "theory_md": """<!-- practice_type: speaking -->
## Slow Down: Pace and Clarity Beat Speed

Indians often speak fast in English — nerves plus the habit of getting
words out quickly. Result: colleagues ask "sorry, could you repeat that?"
Fast speech that needs repeating is **slower** than slow speech understood
first time.

### The clarity toolkit

**1. Chunking.** Group words into meaning-chunks with micro-pauses:
- ❌ "Icompletedthereportyesterdayand sentittotheclient" (one blur)
- ✅ "I completed the report / yesterday / and sent it to the client."

**2. Stress the important word.** "I need it by **Friday**" — the listener's
brain grabs the stressed word even if the rest blurs.

**3. The 70% rule.** Speak at 70% of your Hindi speed in English. It feels
painfully slow to you and perfectly normal to listeners.

**4. Endings matter.** Don't swallow final sounds: "test**ed**",
"work**s**", "first". Endings carry tense and meaning.

### The phone-call test

On audio-only calls there's no lip-reading or slides. Before important
calls: take one breath, drop your speed 30%, over-enunciate the first
sentence. The rest of the call follows.

### Volume and energy

Speak 10% louder than feels natural on calls (mics eat volume), and smile
— listeners literally hear a smile in your voice. Monotone + fast =
incomprehensible. Varied + measured = authoritative.
""",
                "difficulty_min": 2,
                "difficulty_max": 7,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Colleagues keep asking you to repeat yourself. Most likely cause?",
                        "choices": [
                            "Speaking too fast without clear word endings and pauses",
                            "Speaking too slowly",
                            "Using too little vocabulary",
                            "Having an Indian accent",
                        ],
                        "answer_index": 0,
                        "difficulty": 2,
                        "explanation": "It's almost never the accent — it's speed plus swallowed endings. Slow down 30% and finish your consonants; repeat-requests will vanish.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Say with chunking pauses (marked /): 'I finished the testing / yesterday / and the results / look good.' Exaggerate the pauses.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 4,
                        "explanation": "Chunking gives the listener's brain time to process. What feels like dramatic pauses to you sounds like normal clear speech to them.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "listening",
                        "prompt": "Use TTS to listen to: 'The client needs the final report by Friday evening.' Notice which word is stressed, then repeat with the same stress.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 6,
                        "explanation": "'Friday' carries the stress — it's the new, important information. In every sentence, find the one word the listener must catch, and lean on it.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Client call, bad audio, they keep saying 'sorry, what?' You should:",
                        "choices": [
                            "Switch to Hindi",
                            "Speak louder and faster to push through",
                            "Slow down further, over-enunciate, confirm key points in chat",
                            "End the call immediately",
                        ],
                        "answer_index": 2,
                        "difficulty": 5,
                        "explanation": "Bad audio + fast speech = disaster. Slow down MORE than feels necessary, over-enunciate consonants, and confirm key points in chat afterwards.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "writing",
                        "prompt": "Write the 3-line chat message you'd send after an unclear call: decisions + owners + dates.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 7,
                        "explanation": "Model: 'Confirming from the call: (1) We go with the phased rollout — Priya owns API changes by Friday. (2) Pricing stays open, revisit Tuesday.' Written confirmation is the clarity backstop for bad audio.",
                        "company_tags": [
                            "tcs",
                        ],
                    },
                ],
            },
        ],
    },
    {
        "slug": "comm-email-writing",
        "name": "Email Writing",
        "description": (
            "Formal vs informal tone, subject lines that get opened, polite requests, real apology templates, and follow-ups that aren't rude."
        ),
        "lessons": [
            {
                "slug": "comm-email-writing-formal-informal",
                "title": "The Tone Ladder: Formal → Neutral → Casual",
                "practice_type": "writing",
                "theory_md": """<!-- practice_type: writing -->
## The Tone Ladder: Formal → Neutral → Casual

The #1 email skill is matching tone to the reader. Too formal with peers
sounds stiff; too casual with clients sounds disrespectful.

### The ladder

| | Formal (client, senior, first contact) | Neutral (colleagues, regular contacts) | Casual (close teammates only) |
|---|---|---|---|
| Greeting | Dear Mr. Sharma, | Hi Rahul, | Hey |
| Request | Could you please share…? | Can you share…? | Send me… |
| Thanks | Thank you for your time. | Thanks! | Thx |
| Close | Best regards, | Thanks, / Regards, | Cheers |

### Rules that prevent 90% of tone mistakes

1. **Default to neutral.** "Hi [Name]," + "Could you please…" + "Thanks,"
   works for 90% of office email.
2. **Mirror the other person.** If they sign "Best regards", don't reply
   "Cheers". Match their formality, then stay one notch warmer.
3. **Never casual with clients.** No "Hey", no "Thx", no emojis — until
   they've done it first, twice.
4. **First email = one notch more formal.** You can always relax later;
   you can't un-send a too-casual first impression.

### The 10-second tone test

Read your draft and ask: "If my manager's manager read this, would I be
proud or embarrassed?" Adjust one notch if embarrassed.
""",
                "difficulty_min": 2,
                "difficulty_max": 7,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "First email ever to a client. Best greeting + close?",
                        "choices": [
                            "Hey! … Cheers",
                            "Dear Ms. Rao, … Best regards,",
                            "Hi hi … Thx",
                            "(no greeting) … Sent from my iPhone",
                        ],
                        "answer_index": 1,
                        "difficulty": 2,
                        "explanation": "First contact = one notch more formal. 'Dear Ms. Rao' + 'Best regards' is safe; you can relax to 'Hi' after they reply casually.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A client signs their emails 'Best regards'. You should reply with:",
                        "choices": [
                            "Best regards, (mirror their formality)",
                            "Cheers!",
                            "Yours obediently",
                            "Thx!!",
                        ],
                        "answer_index": 0,
                        "difficulty": 4,
                        "explanation": "Mirror the other person's tone. 'Cheers' after their 'Best regards' feels presumptuous; 'Yours obediently' is school-era.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "writing",
                        "prompt": "Rewrite casual → neutral: 'Hey, send me the docs ASAP. Thx.'",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 6,
                        "explanation": "Model: 'Hi Ankit, could you please share the docs by today evening? Thanks!' Greeting + polite request + deadline + warm close — the neutral formula.",
                        "company_tags": [
                            "tcs",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A client replies 'Hi, thanks!' and signs 'Cheers, David'. Your next email:",
                        "choices": [
                            "'Hi' … (no close at all)",
                            "'Hi David,' … 'Thanks,' (mirror their tone)",
                            "'Hey Dave!! … Cheers mate'",
                            "'Dear Mr. David, … Yours obediently'",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "Mirror one notch: 'Hi David,' … 'Thanks,'. Match their warmth without jumping to 'Hey/Cheers' yourself until the relationship is established.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "writing",
                        "prompt": "Rewrite stiff → neutral: 'This is to inform you that the meeting has been postponed.'",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 7,
                        "explanation": "Model: 'Quick update: tomorrow's meeting is postponed to Thursday, 3pm. New invite coming shortly. Thanks!' 'This is to inform you' is bureaucratic — 'quick update' is human.",
                        "company_tags": [
                            "general",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-email-writing-subject-lines",
                "title": "Subject Lines That Get Opened",
                "practice_type": "writing",
                "theory_md": """<!-- practice_type: writing -->
## Subject Lines That Get Opened

Busy managers triage by subject line. "Hi" and "Request" get buried.
A good subject = **topic + action needed + deadline**.

### The 7 formulas (steal these)

1. **Action needed:** "Action needed: approve the leave request by Friday"
2. **FYI:** "FYI: deployment moved to Thursday"
3. **Update:** "Update: login bug fixed, testing today"
4. **Request:** "Request: 2 days WFH next week"
5. **Follow-up:** "Following up: API docs (sent Tuesday)"
6. **Meeting:** "Meeting notes: sprint planning, Oct 15"
7. **Urgent (rare!):** "Urgent: production down — need DB access"

### Rules

- **Front-load** the important word — mobile shows ~30 characters.
  ❌ "Regarding the matter we discussed…" → ✅ "Approval needed: budget v2"
- **One subject, one topic.** Two topics = two emails.
- **Never leave it blank.** Blank subjects look like spam/phishing.
- **"Urgent" is a fire alarm.** Use it twice a year max, or nobody
  believes the third time.

### Reply subjects

Keep the thread: don't change the subject mid-conversation. If the topic
changed completely, start a new email with a new subject.
""",
                "difficulty_min": 1,
                "difficulty_max": 6,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "You need your manager's approval on a document by Friday. Best subject?",
                        "choices": [
                            "Approval needed: Q3 report by Friday",
                            "Request",
                            "Hi",
                            "Regarding the document we talked about last week in the meeting",
                        ],
                        "answer_index": 0,
                        "difficulty": 1,
                        "explanation": "Action + topic + deadline, front-loaded. 'Hi' gets buried; the long one gets cut off on mobile.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "writing",
                        "prompt": "Write a subject line: you're informing the team the client demo moved from Monday to Wednesday.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 3,
                        "explanation": "Model: 'Update: client demo moved to Wednesday (was Monday)'. FYI-type, topic first, old vs new clear.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "When should you mark an email 'Urgent'?",
                        "choices": [
                            "Only for genuine emergencies (production down, blocking many people)",
                            "For all emails to your manager",
                            "Every Monday morning",
                            "Whenever you want a fast reply",
                        ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "'Urgent' is a fire alarm — overuse trains people to ignore you. Twice a year keeps it meaningful.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which subject survives a mobile inbox (30 chars visible)?",
                        "choices": [
                            "Regarding the matter we discussed last week",
                            "Approval needed: budget v2",
                            "(blank)",
                            "Hi",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "Front-load the verb: 'Approval needed: budget v2' shows the action even truncated. 'Regarding the matter…' shows nothing.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "writing",
                        "prompt": "You must BOTH reschedule Friday's demo AND request budget approval. How many emails? Write the subject(s).",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 6,
                        "explanation": "Two emails — one subject, one topic. 'Update: demo moved to Monday' + 'Approval needed: Q4 tooling budget'. Combined subjects get half-answered.",
                        "company_tags": [
                            "general",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-email-writing-requesting",
                "title": "Requesting Without Sounding Demanding",
                "practice_type": "writing",
                "theory_md": """<!-- practice_type: writing -->
## Requesting Without Sounding Demanding

Indians often write requests as orders ("Send me the report") or as
over-apologies ("Sorry sorry to disturb you, kindly please…"). Both hurt
you. The middle path:

### The request formula

**Context (1 line) + Request (polite) + Deadline + Thanks**

> Hi Priya,
>
> Following up on yesterday's call — could you please share the updated
> API specs by Thursday? I need them to finish the integration.
>
> Thanks,
> Rahul

### Softeners that work

- "Could you please…" (default) / "Would you mind…?" (extra polite)
- "When you get a chance…" (no rush) / "At your earliest…" (mild rush)
- "I'd appreciate it if…" (formal)

### What to avoid

- ❌ "I want…" / "I need you to…" (demanding)
- ❌ "Kindly do the needful" (archaic)
- ❌ Five sorrys before the request (undermines you)
- ❌ No deadline ("whenever" = never — always give a date)

### Requesting UP (to seniors/clients)

Add **reason + make it easy to say yes**:
- "Could you please approve the budget by Friday? The vendor needs
  confirmation to start Monday — I've attached the one-page summary."

The reason + attachment combo gets approvals. Bare requests get delayed.
""",
                "difficulty_min": 3,
                "difficulty_max": 8,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "You need data from a senior in another team. Best request?",
                        "choices": [
                            "Send sales data.",
                            "Sorry sorry to disturb you, kindly please please share data.",
                            "I want the sales data. Send it soon.",
                            "Could you please share the sales data by Thursday? I need it for the client presentation.",
                        ],
                        "answer_index": 3,
                        "difficulty": 3,
                        "explanation": "Polite form + deadline + reason. Orders offend seniors; over-apologizing makes you look junior. The middle path wins.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "writing",
                        "prompt": "Write a 3-line email asking your manager for approval to attend a conference. Include a reason.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 5,
                        "explanation": "Model: 'Hi Rahul, could you please approve my attending the React conference on Nov 5? The advanced hooks workshop directly applies to our dashboard rewrite — I've attached the agenda. Thanks!' Reason + easy yes (attached agenda).",
                        "company_tags": [
                            "infosys",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why should every request include a deadline?",
                        "choices": [
                            "Managers only read emails with dates",
                            "'Whenever you can' gets deprioritized forever — a date creates commitment",
                            "Deadlines are legally required in emails",
                            "It makes the email longer and more impressive",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "No deadline = no priority. 'By Thursday' turns a wish into a commitment both sides can plan around.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Requesting from a CLIENT vs a PEER — what's different?",
                        "choices": [
                            "Peers: no deadline needed",
                            "Clients: be extra casual to seem friendly",
                            "No difference at all",
                            "Clients: full polite formula, never casual. Peers: shorter is fine, but always include a deadline",
                        ],
                        "answer_index": 3,
                        "difficulty": 6,
                        "explanation": "Clients get the full formula (context + could-you-please + deadline + thanks) and zero casualness. Peers can be shorter, but the deadline stays — 'whenever' kills both.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "writing",
                        "prompt": "Ask a client for a 30-min feedback call next week. Offer 2 specific time slots (makes saying yes easy).",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 8,
                        "explanation": "Model: 'Hi Sarah, could we schedule 30 minutes next week to walk through the feedback? I'm free Tue 3–5pm IST or Wed 11am–1pm IST — let me know what suits you. Thanks!' Two options = easy yes.",
                        "company_tags": [
                            "amazon",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-email-writing-apologizing",
                "title": "Apologizing Like a Professional (Real Templates)",
                "practice_type": "writing",
                "theory_md": """<!-- practice_type: writing -->
## Apologizing Like a Professional (Real Templates)

Everyone misses deadlines and breaks things. What separates professionals
is the apology email: own it fast, fix it visibly, prevent repeat.

### The 4-part apology

1. **Own it** — no excuses, no passive voice.
2. **Impact** — show you understand what it cost them.
3. **Fix** — what's done / being done, with a date.
4. **Prevent** — what changes so it doesn't repeat.

### Template 1: Missed deadline

> Subject: Update: [deliverable] — new date [date]
>
> Hi [Name],
>
> I missed the [date] deadline for [deliverable] — that's on me. I know
> this delays [their plan], and I'm sorry for that.
>
> The work is [X]% done; you'll have it by [new date, with buffer].
> Going forward, I'll flag risks by [day] instead of the due date.
>
> Thanks for your patience,
> [You]

### Template 2: You broke something

> Subject: Issue with [system] — fixed, details inside
>
> Hi team,
>
> My change to [X] caused [outage/bug] at [time]. I've rolled it back
> and the system is stable since [time].
>
> Root cause: [one line]. Prevention: [what you'll add — a test, a
> review step, a checklist].
>
> Sorry for the disruption,
> [You]

### What NEVER to write

- ❌ "Mistakes were made." (passive = dodging)
- ❌ "Sorry if you felt…" (non-apology)
- ❌ Blaming others in your apology email (separate conversation)
- ❌ Over-apologizing 5 times (one sincere apology > five anxious ones)
""",
                "difficulty_min": 3,
                "difficulty_max": 8,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Why is 'Mistakes were made' a bad apology?",
                        "choices": [
                            "It's too short",
                            "It uses past tense",
                            "Passive voice hides who made the mistake — it dodges ownership",
                            "It's too formal",
                        ],
                        "answer_index": 2,
                        "difficulty": 3,
                        "explanation": "Ownership is the whole point of an apology. 'I missed the deadline' builds trust; 'mistakes were made' destroys it.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "writing",
                        "prompt": "You broke the staging build with a bad merge. Write the 4-part apology email (own, impact, fix, prevent) in 5 lines.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 6,
                        "explanation": "Model: 'Hi team — my merge broke the staging build at 3pm; that's on me, and I know it blocked QA's afternoon. I've reverted it and staging is green since 4pm. Root cause: I skipped the test run. Prevention: I'll add the pre-merge checklist to our wiki. Sorry for the disruption.'",
                        "company_tags": [
                            "tcs",
                            "wipro",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A client is angry about a delay. Your apology email should focus MOST on:",
                        "choices": [
                            "What you're doing to fix it and the new date",
                            "Why the delay wasn't really your fault",
                            "How sorry you are, repeated five times",
                            "How hard you've been working lately",
                        ],
                        "answer_index": 0,
                        "difficulty": 8,
                        "explanation": "Clients forgive delays; they don't forgive vagueness. One sincere 'I'm sorry' + concrete fix + new date + prevention = the professional apology.",
                        "company_tags": [
                            "amazon",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You missed a client deadline by a day. The email's FIRST line should be:",
                        "choices": [
                            "As you know, there were many challenges…",
                            "Mistakes were made by the team.",
                            "I missed yesterday's deadline — that's on me.",
                            "Hope you're doing well! So anyway…",
                        ],
                        "answer_index": 2,
                        "difficulty": 5,
                        "explanation": "Own it in line one: 'I missed yesterday's deadline — that's on me.' Burying the apology in paragraph 3 reads as hiding.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "speaking",
                        "prompt": "Apologize ALOUD in 20 seconds for joining a client call 10 minutes late. Own it, no excuses, state the fix.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 7,
                        "explanation": "Model: 'Apologies for joining late — that's on me, I misjudged the previous call. I've caught up on the notes; please continue and I'll jump in where I can.' 20 seconds, owned, forward-looking.",
                        "company_tags": [
                            "general",
                        ],
                    },
                ],
            },
            {
                "slug": "comm-email-writing-followups",
                "title": "Follow-Ups: Chasing Without Being Rude",
                "practice_type": "writing",
                "theory_md": """<!-- practice_type: writing -->
## Follow-Ups: Chasing Without Being Rude

70% of work emails need a follow-up. Most people either never follow up
(work dies) or follow up rudely ("As per my last email!!"). Here's the
professional middle.

### The follow-up ladder (use in order)

**Nudge 1 (2-3 days, friendly):**
> Hi [Name], just bringing this back to your attention — could you
> please [action] when you get a chance? Thanks!

**Nudge 2 (1 week, add context):**
> Hi [Name], following up on [action]. We're holding [dependent work]
> until this is done — is [new date] workable for you?

**Nudge 3 (escalate politely):**
> Hi [Name], I haven't heard back on [action] sent on [dates]. Looping
> in [manager] so we're all aligned on the timeline.

Notice: each nudge adds **new information** (a dependency, a date, a
person) — never just "reminder!!!" again.

### Rules

- **Reply in the same thread** — don't start a new email; context matters.
- **Change the subject** only with "Following up:" prefix if the thread
  is old: "Following up: API docs (Oct 10)".
- **One follow-up per 2-3 business days.** Daily chasing = harassment.
- **Assume they're busy, not ignoring you.** Tone stays warm until nudge 3.

### The magic line for nudge 2

"Is [date] workable for you?" — it turns an open request into a
negotiation with a deadline. Response rates jump.
""",
                "difficulty_min": 3,
                "difficulty_max": 8,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "You emailed specs 4 days ago, no reply. Best first follow-up?",
                        "choices": [
                            "(Send the same email again with no changes)",
                            "Why haven't you replied to my email?",
                            "As per my last email, I am still waiting!!!",
                            "Hi, just bringing this back to your attention — could you please share the specs when you get a chance? Thanks!",
                        ],
                        "answer_index": 3,
                        "difficulty": 3,
                        "explanation": "Warm, assumes busyness not rudeness, restates the ask. 'As per my last email!!!' burns the relationship for one email.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "writing",
                        "prompt": "Write nudge 2: it's been a week, and your testing is blocked until you get the credentials.",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 5,
                        "explanation": "Model: 'Hi Sneha, following up on the staging credentials. My testing is on hold until I have them — is tomorrow workable for you? Thanks!' New info (blocked testing) + proposed date = response.",
                        "company_tags": [
                            "infosys",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "When is it okay to loop in someone's manager on a follow-up?",
                        "choices": [
                            "Never, under any circumstances",
                            "On the very first email, to show seriousness",
                            "Only on Fridays",
                            "After 2+ friendly nudges with no response, framed as alignment not complaint",
                        ],
                        "answer_index": 3,
                        "difficulty": 7,
                        "explanation": "Escalation is nudge 3, not nudge 1 — and frame it as 'so we're all aligned', never as a complaint. Premature escalation poisons the relationship.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Nudge 1 got no reply after 3 days. Nudge 2 must add:",
                        "choices": [
                            "More exclamation marks",
                            "A complaint to their manager",
                            "The exact same text again",
                            "New information: a dependency, a proposed date, or wider impact",
                        ],
                        "answer_index": 3,
                        "difficulty": 6,
                        "explanation": "Every nudge adds NEW information — a dependency, a date, a person. Repeating 'just reminding!!!' trains people to ignore you.",
                        "company_tags": [
                            "general",
                        ],
                    },
                    {
                        "qtype": "writing",
                        "prompt": "Write nudge 3: two friendly nudges sent over 10 days, no reply. Loop in their manager for alignment (not complaint).",
                        "choices": None,
                        "answer_index": None,
                        "difficulty": 8,
                        "explanation": "Model: 'Hi Karan, I haven't heard back on the security review (my emails of Oct 5 and Oct 9). Looping in Meera so we're aligned — the release is blocked until this clears. Is Thursday workable? Thanks!' Facts, dates, alignment framing.",
                        "company_tags": [
                            "infosys",
                        ],
                    },
                ],
            },
        ],
    },
]
