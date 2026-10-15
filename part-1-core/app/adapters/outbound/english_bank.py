"""Outbound adapter: English proficiency question bank for the Placement Simulator.

104 original questions across 10 categories:
  grammar: tenses (10), articles (8), prepositions (8), subject-verb agreement (8)
  vocabulary: synonyms (8), antonyms (8), idioms & phrases (8)
  reading: 5 passages x 4 questions (20)
  sentence correction (10), error spotting (12), extra vocabulary (4)

Format matches question_bank.py: Question(id, topic, level, prompt, choices,
answer_index, skill). Reading passages live in READING_PASSAGES and are
attached by the simulator service via the question's skill tag (rc-p1..p5).

All content written originally for SkillForge.
"""
from __future__ import annotations

from app.domain.profile import Question


def _q(qid: str, level: str, skill: str, prompt: str,
       choices: list[str], answer: int) -> Question:
    return Question(id=qid, topic="english", level=level, skill=skill,
                    prompt=prompt, choices=tuple(choices), answer_index=answer)


READING_PASSAGES: dict[str, dict] = {
    "rc-p1": {
        "title": "The Rise of Remote Work",
        "text": (
            "Remote work has transformed from a rare perk into a mainstream way of working. "
            "When companies shifted to work-from-home during the pandemic, many discovered that "
            "productivity did not collapse as feared. Instead, employees reported saving hours of "
            "commuting time, and companies saved on office costs. However, remote work brought new "
            "challenges: isolation, blurred boundaries between work and home, and difficulties in "
            "mentoring junior employees. The most successful organizations adopted a hybrid model, "
            "combining office collaboration days with focused remote work. Studies suggest that the "
            "future of work is neither fully remote nor fully office-based, but a flexible blend "
            "that trusts employees to choose where they do their best work."
        ),
    },
    "rc-p2": {
        "title": "Why Sleep Matters",
        "text": (
            "Sleep is often the first thing people sacrifice when life gets busy, yet it is one of "
            "the most critical pillars of health. During deep sleep, the brain consolidates memories, "
            "moving information from short-term to long-term storage. Students who sleep well after "
            "studying consistently outperform those who pull all-nighters. Lack of sleep impairs "
            "decision-making as severely as alcohol intoxication, slowing reaction times and reducing "
            "creativity. Experts recommend 7-9 hours for adults, a consistent schedule, and avoiding "
            "screens an hour before bed. In short, sleep is not lost time — it is when the brain does "
            "some of its most important work."
        ),
    },
    "rc-p3": {
        "title": "The Digital Divide",
        "text": (
            "While cities enjoy high-speed internet, millions in rural areas still struggle with "
            "basic connectivity. This digital divide affects education most sharply: during online "
            "classes, rural students often climb rooftops or walk to hilltops searching for a signal. "
            "Governments have launched programs to lay fiber-optic cables to villages, but progress is "
            "slow and maintenance is expensive. Some startups are experimenting with low-cost solutions "
            "like community Wi-Fi hotspots and satellite internet. Bridging this divide is not just about "
            "technology — it is about giving every child a fair chance to learn, regardless of geography."
        ),
    },
    "rc-p4": {
        "title": "Failure as a Teacher",
        "text": (
            "Every successful entrepreneur has a long list of failures behind them. Thomas Edison tested "
            "thousands of materials before finding the right filament for the light bulb. When asked about "
            "his failures, he reportedly said he had not failed but found thousands of ways that would not "
            "work. Modern research supports this mindset: students who view failure as feedback rather than "
            "a verdict on their ability persist longer and learn faster. The key distinction is between "
            "failing and being a failure — the first is an event, the second is an identity nobody should "
            "adopt. Organizations that punish every mistake create cultures of fear; those that analyze "
            "mistakes openly build cultures of innovation."
        ),
    },
    "rc-p5": {
        "title": "Urban Green Spaces",
        "text": (
            "As cities grow denser, parks and green spaces become more valuable, not less. Research shows "
            "that people living near parks report lower stress and better mental health. Trees cool streets "
            "by several degrees in summer, reducing air-conditioning costs and heat-related illness. Yet "
            "urban planners often treat green space as a luxury to be sacrificed for development. Forward-"
            "thinking cities are reversing this: converting abandoned lots into pocket parks, planting trees "
            "along streets, and requiring rooftop gardens on new buildings. A city without green space may be "
            "efficient, but it is rarely a place where people truly thrive."
        ),
    },
}

ENGLISH_BANK: list[Question] = [
    # ==================== TENSES (10) ====================
    _q("eng-t1", "beginner", "tenses",
       "She ___ to school every day.",
       ["go", "goes", "going", "gone"], 1),
    _q("eng-t2", "beginner", "tenses",
       "They ___ football right now.",
       ["play", "plays", "are playing", "played"], 2),
    _q("eng-t3", "beginner", "tenses",
       "I ___ my homework yesterday.",
       ["finish", "finishes", "finished", "finishing"], 2),
    _q("eng-t4", "intermediate", "tenses",
       "By the time we arrived, the movie ___.",
       ["already started", "had already started", "has already started", "already starts"], 1),
    _q("eng-t5", "intermediate", "tenses",
       "She ___ here since 2018.",
       ["works", "is working", "has been working", "worked"], 2),
    _q("eng-t6", "intermediate", "tenses",
       "If it rains tomorrow, we ___ the match.",
       ["cancel", "will cancel", "cancelled", "would cancel"], 1),
    _q("eng-t7", "advanced", "tenses",
       "Hardly ___ the door when the phone rang.",
       ["I had closed", "had I closed", "I have closed", "did I closed"], 1),
    _q("eng-t8", "advanced", "tenses",
       "He ___ for the company for ten years before he resigned.",
       ["worked", "has worked", "had been working", "is working"], 2),
    _q("eng-t9", "intermediate", "tenses",
       "Look at those clouds! It ___ rain.",
       ["is going to", "will to", "goes to", "going to"], 0),
    _q("eng-t10", "advanced", "tenses",
       "I wish I ___ harder for the exam.",
       ["studied", "had studied", "study", "have studied"], 1),

    # ==================== ARTICLES (8) ====================
    _q("eng-a1", "beginner", "articles",
       "___ sun rises in the east.",
       ["A", "An", "The", "No article"], 2),
    _q("eng-a2", "beginner", "articles",
       "She is ___ honest person.",
       ["a", "an", "the", "no article"], 1),
    _q("eng-a3", "intermediate", "articles",
       "He plays ___ guitar very well.",
       ["a", "an", "the", "no article"], 2),
    _q("eng-a4", "intermediate", "articles",
       "___ Mount Everest is the highest peak in the world.",
       ["A", "An", "The", "No article"], 3),
    _q("eng-a5", "intermediate", "articles",
       "I had ___ sandwich for lunch.",
       ["a", "an", "the", "no article"], 0),
    _q("eng-a6", "advanced", "articles",
       "___ rich should help ___ poor.",
       ["A / a", "The / the", "An / an", "No article / no article"], 1),
    _q("eng-a7", "advanced", "articles",
       "She went to ___ hospital to visit her friend. (not as a patient)",
       ["a", "an", "the", "no article"], 2),
    _q("eng-a8", "intermediate", "articles",
       "What ___ beautiful day it is!",
       ["a", "an", "the", "no article"], 0),

    # ==================== PREPOSITIONS (8) ====================
    _q("eng-p1", "beginner", "prepositions",
       "She is good ___ mathematics.",
       ["in", "at", "for", "with"], 1),
    _q("eng-p2", "beginner", "prepositions",
       "The cat is hiding ___ the table.",
       ["on", "under", "over", "above"], 1),
    _q("eng-p3", "intermediate", "prepositions",
       "He has been suffering ___ fever since Monday.",
       ["with", "from", "by", "of"], 1),
    _q("eng-p4", "intermediate", "prepositions",
       "She apologized ___ being late.",
       ["for", "of", "about", "at"], 0),
    _q("eng-p5", "intermediate", "prepositions",
       "The meeting is scheduled ___ 3 PM ___ Friday.",
       ["at / on", "on / at", "in / on", "at / in"], 0),
    _q("eng-p6", "advanced", "prepositions",
       "He is accused ___ stealing the documents.",
       ["for", "of", "with", "about"], 1),
    _q("eng-p7", "advanced", "prepositions",
       "___ my opinion, the plan needs revision.",
       ["In", "On", "At", "By"], 0),
    _q("eng-p8", "intermediate", "prepositions",
       "She is married ___ my cousin.",
       ["with", "to", "by", "for"], 1),

    # ==================== SUBJECT-VERB AGREEMENT (8) ====================
    _q("eng-s1", "beginner", "subject-verb",
       "Neither of the answers ___ correct.",
       ["are", "is", "were", "be"], 1),
    _q("eng-s2", "beginner", "subject-verb",
       "The team ___ playing well today.",
       ["are", "is", "were", "be"], 1),
    _q("eng-s3", "intermediate", "subject-verb",
       "Each of the students ___ a laptop.",
       ["have", "has", "are having", "were having"], 1),
    _q("eng-s4", "intermediate", "subject-verb",
       "The list of items ___ on the table.",
       ["are", "is", "were", "be"], 1),
    _q("eng-s5", "intermediate", "subject-verb",
       "Not only the students but also the teacher ___ confused.",
       ["were", "was", "are", "be"], 1),
    _q("eng-s6", "advanced", "subject-verb",
       "The number of applicants ___ increased this year.",
       ["have", "has", "are", "were"], 1),
    _q("eng-s7", "advanced", "subject-verb",
       "A number of students ___ absent today.",
       ["was", "were", "is", "has been"], 1),
    _q("eng-s8", "intermediate", "subject-verb",
       "Bread and butter ___ my favorite breakfast.",
       ["are", "is", "were", "be"], 1),

    # ==================== SYNONYMS (8) ====================
    _q("eng-syn1", "beginner", "synonyms",
       "Choose the synonym of HAPPY.",
       ["gloomy", "joyful", "angry", "tired"], 1),
    _q("eng-syn2", "beginner", "synonyms",
       "Choose the synonym of BEGIN.",
       ["end", "start", "stop", "finish"], 1),
    _q("eng-syn3", "intermediate", "synonyms",
       "Choose the synonym of CANDID.",
       ["rude", "frank", "shy", "clever"], 1),
    _q("eng-syn4", "intermediate", "synonyms",
       "Choose the synonym of ABANDON.",
       ["keep", "desert", "hold", "cherish"], 1),
    _q("eng-syn5", "intermediate", "synonyms",
       "Choose the synonym of TRANQUIL.",
       ["noisy", "peaceful", "crowded", "bright"], 1),
    _q("eng-syn6", "advanced", "synonyms",
       "Choose the synonym of METICULOUS.",
       ["careless", "thorough", "hasty", "lazy"], 1),
    _q("eng-syn7", "advanced", "synonyms",
       "Choose the synonym of PRAGMATIC.",
       ["idealistic", "practical", "theoretical", "emotional"], 1),
    _q("eng-syn8", "intermediate", "synonyms",
       "Choose the synonym of RESILIENT.",
       ["fragile", "flexible", "rigid", "weak"], 1),

    # ==================== ANTONYMS (8) ====================
    _q("eng-ant1", "beginner", "antonyms",
       "Choose the antonym of BRAVE.",
       ["bold", "cowardly", "strong", "wise"], 1),
    _q("eng-ant2", "beginner", "antonyms",
       "Choose the antonym of ANCIENT.",
       ["old", "modern", "historic", "classic"], 1),
    _q("eng-ant3", "intermediate", "antonyms",
       "Choose the antonym of TRANSPARENT.",
       ["clear", "opaque", "visible", "clean"], 1),
    _q("eng-ant4", "intermediate", "antonyms",
       "Choose the antonym of EXPAND.",
       ["extend", "contract", "enlarge", "stretch"], 1),
    _q("eng-ant5", "intermediate", "antonyms",
       "Choose the antonym of SCARCE.",
       ["rare", "abundant", "limited", "short"], 1),
    _q("eng-ant6", "advanced", "antonyms",
       "Choose the antonym of BENEVOLENT.",
       ["kind", "malevolent", "generous", "charitable"], 1),
    _q("eng-ant7", "advanced", "antonyms",
       "Choose the antonym of AMBIGUOUS.",
       ["vague", "clear", "uncertain", "doubtful"], 1),
    _q("eng-ant8", "intermediate", "antonyms",
       "Choose the antonym of VICTORY.",
       ["triumph", "defeat", "success", "win"], 1),

    # ==================== IDIOMS (8) ====================
    _q("eng-id1", "beginner", "idioms",
       "'Break the ice' means:",
       ["to break frozen water", "to start a conversation", "to end a friendship", "to feel cold"], 1),
    _q("eng-id2", "beginner", "idioms",
       "'A piece of cake' means:",
       ["a dessert", "something very easy", "a small share", "a celebration"], 1),
    _q("eng-id3", "intermediate", "idioms",
       "'Hit the nail on the head' means:",
       ["to hurt someone", "to say exactly the right thing", "to build something", "to miss a target"], 1),
    _q("eng-id4", "intermediate", "idioms",
       "'Burn the midnight oil' means:",
       ["to waste fuel", "to work late into the night", "to set fire", "to stay awake partying"], 1),
    _q("eng-id5", "intermediate", "idioms",
       "'Let the cat out of the bag' means:",
       ["to free a pet", "to reveal a secret", "to cause trouble", "to clean up"], 1),
    _q("eng-id6", "advanced", "idioms",
       "'Bite the bullet' means:",
       ["to get injured", "to face a difficult situation bravely", "to eat quickly", "to avoid work"], 1),
    _q("eng-id7", "advanced", "idioms",
       "'The ball is in your court' means:",
       ["a sports match", "it is your turn to act", "you lost the game", "the court is yours"], 1),
    _q("eng-id8", "intermediate", "idioms",
       "'Once in a blue moon' means:",
       ["every month", "very rarely", "at night", "during festivals"], 1),

    # ==================== READING COMPREHENSION (20 = 5 passages x 4) ====================
    _q("eng-rc1", "intermediate", "rc-p1",
       "According to the passage, what did companies discover about productivity during remote work?",
       ["It collapsed completely", "It did not collapse as feared",
        "It doubled overnight", "It only worked for managers"], 1),
    _q("eng-rc2", "intermediate", "rc-p1",
       "Which of the following is mentioned as a challenge of remote work?",
       ["High office rents", "Employee isolation",
        "Slow internet in cities", "Too many holidays"], 1),
    _q("eng-rc3", "advanced", "rc-p1",
       "What does the 'hybrid model' described in the passage combine?",
       ["Two different companies", "Office collaboration days with focused remote work",
        "Part-time and full-time roles", "Morning and night shifts"], 1),
    _q("eng-rc4", "intermediate", "rc-p1",
       "What is the passage's conclusion about the future of work?",
       ["Everyone will return to offices", "A flexible blend of remote and office",
        "Remote work will be banned", "Only IT jobs will stay remote"], 1),

    _q("eng-rc5", "intermediate", "rc-p2",
       "What happens in the brain during deep sleep, according to the passage?",
       ["It shuts down completely", "It consolidates memories",
        "It stops all activity", "It only dreams"], 1),
    _q("eng-rc6", "beginner", "rc-p2",
       "Students who sleep well after studying:",
       ["forget everything", "outperform those who stay up all night",
        "need less study time always", "cannot concentrate"], 1),
    _q("eng-rc7", "advanced", "rc-p2",
       "Lack of sleep is compared to what in the passage?",
       ["Skipping meals", "Alcohol intoxication",
        "Missing exercise", "Drinking coffee"], 1),
    _q("eng-rc8", "intermediate", "rc-p2",
       "How many hours of sleep do experts recommend for adults?",
       ["4-5 hours", "5-6 hours", "7-9 hours", "10-12 hours"], 2),

    _q("eng-rc9", "intermediate", "rc-p3",
       "What is the 'digital divide' as described in the passage?",
       ["A gap in computer prices", "Unequal internet access between cities and rural areas",
        "A new social media app", "Division of tech companies"], 1),
    _q("eng-rc10", "beginner", "rc-p3",
       "What do rural students sometimes do to attend online classes?",
       ["Buy new phones", "Climb rooftops searching for signal",
        "Skip classes entirely", "Move to cities"], 1),
    _q("eng-rc11", "advanced", "rc-p3",
       "Which low-cost solutions are mentioned for rural connectivity?",
       ["Building malls", "Community Wi-Fi hotspots and satellite internet",
        "Free laptops for all", "Closing village schools"], 1),
    _q("eng-rc12", "intermediate", "rc-p3",
       "The passage argues bridging the divide is really about:",
       ["Selling more phones", "Fair learning chances regardless of geography",
        "Faster gaming", "Cheaper data plans"], 1),

    _q("eng-rc13", "intermediate", "rc-p4",
       "What did Edison reportedly say about his many attempts?",
       ["He had failed completely", "He found thousands of ways that would not work",
        "He gave up early", "He copied others"], 1),
    _q("eng-rc14", "advanced", "rc-p4",
       "According to research in the passage, students who see failure as feedback:",
       ["quit faster", "persist longer and learn faster",
        "avoid all risks", "score lower"], 1),
    _q("eng-rc15", "intermediate", "rc-p4",
       "What is the key distinction the passage makes?",
       ["Failing is an event; being a failure is an identity",
        "Failure is always final", "Success needs no effort",
        "Mistakes should be hidden"], 0),
    _q("eng-rc16", "advanced", "rc-p4",
       "Organizations that punish every mistake create:",
       ["Cultures of innovation", "Cultures of fear",
        "Faster growth", "Better products"], 1),

    _q("eng-rc17", "intermediate", "rc-p5",
       "According to the passage, green spaces help cities by:",
       ["Increasing traffic", "Lowering stress and cooling streets",
        "Raising rents", "Reducing jobs"], 1),
    _q("eng-rc18", "beginner", "rc-p5",
       "Trees cool streets in summer, which:",
       ["increases pollution", "reduces air-conditioning costs",
        "blocks sunlight fully", "kills plants"], 1),
    _q("eng-rc19", "advanced", "rc-p5",
       "What are 'forward-thinking cities' doing?",
       ["Removing all parks", "Converting abandoned lots into pocket parks",
        "Banning trees", "Building only malls"], 1),
    _q("eng-rc20", "intermediate", "rc-p5",
       "The passage's view of a city without green space:",
       ["It is ideal", "It may be efficient but not a place where people thrive",
        "It is impossible", "It is cheaper to run"], 1),

    # ==================== SENTENCE CORRECTION (10) ====================
    _q("eng-sc1", "beginner", "sentence-correction",
       "Choose the correct sentence.",
       ["She don't like tea.", "She doesn't like tea.",
        "She not like tea.", "She don't likes tea."], 1),
    _q("eng-sc2", "beginner", "sentence-correction",
       "Choose the correct sentence.",
       ["He go to office by bus.", "He goes to office by bus.",
        "He going to office by bus.", "He gone to office by bus."], 1),
    _q("eng-sc3", "intermediate", "sentence-correction",
       "Choose the correct sentence.",
       ["The informations are useful.", "The information is useful.",
        "The informations is useful.", "The information are useful."], 1),
    _q("eng-sc4", "intermediate", "sentence-correction",
       "Choose the correct sentence.",
       ["Between you and I, this is secret.", "Between you and me, this is secret.",
        "Between you and myself, this is secret.", "Between you with I, this is secret."], 1),
    _q("eng-sc5", "intermediate", "sentence-correction",
       "Choose the correct sentence.",
       ["She is more smarter than him.", "She is smarter than him.",
        "She is most smarter than him.", "She is smartest than him."], 1),
    _q("eng-sc6", "advanced", "sentence-correction",
       "Choose the correct sentence.",
       ["Scarcely had he arrived when it started raining.",
        "Scarcely he had arrived when it started raining.",
        "Scarcely had he arrived than it started raining.",
        "Scarcely did he arrived when it started raining."], 0),
    _q("eng-sc7", "advanced", "sentence-correction",
       "Choose the correct sentence.",
       ["No sooner did the bell ring than the students left.",
        "No sooner the bell rang than the students left.",
        "No sooner did the bell ring when the students left.",
        "No sooner had the bell ring than the students left."], 0),
    _q("eng-sc8", "intermediate", "sentence-correction",
       "Choose the correct sentence.",
       ["I look forward to meet you.", "I look forward to meeting you.",
        "I look forward to met you.", "I look forward for meeting you."], 1),
    _q("eng-sc9", "advanced", "sentence-correction",
       "Choose the correct sentence.",
       ["He denied to steal the money.", "He denied stealing the money.",
        "He denied steal the money.", "He denied stolen the money."], 1),
    _q("eng-sc10", "intermediate", "sentence-correction",
       "Choose the correct sentence.",
       ["One of my friends are coming.", "One of my friends is coming.",
        "One of my friend is coming.", "One of my friends were coming."], 1),

    # ==================== ERROR SPOTTING (12) ====================
    _q("eng-es1", "beginner", "error-spotting",
       "Spot the error: 'She have two brothers.'",
       ["She", "have", "two", "brothers"], 1),
    _q("eng-es2", "beginner", "error-spotting",
       "Spot the error: 'They was playing outside.'",
       ["They", "was", "playing", "outside"], 1),
    _q("eng-es3", "intermediate", "error-spotting",
       "Spot the error: 'He is the most tallest boy in class.'",
       ["is", "the", "most", "tallest"], 2),
    _q("eng-es4", "intermediate", "error-spotting",
       "Spot the error: 'I am agree with you.'",
       ["I", "am", "agree", "with you"], 1),
    _q("eng-es5", "intermediate", "error-spotting",
       "Spot the error: 'She didn't went to the party.'",
       ["She", "didn't", "went", "to the party"], 2),
    _q("eng-es6", "advanced", "error-spotting",
       "Spot the error: 'The committee have decided the matter.'",
       ["The", "committee", "have", "decided"], 2),
    _q("eng-es7", "advanced", "error-spotting",
       "Spot the error: 'He is working here from five years.'",
       ["is working", "here", "from", "five years"], 2),
    _q("eng-es8", "intermediate", "error-spotting",
       "Spot the error: 'Each students must bring their ID.'",
       ["Each", "students", "must", "their"], 1),
    _q("eng-es9", "intermediate", "error-spotting",
       "Spot the error: 'I prefer coffee than tea.'",
       ["prefer", "coffee", "than", "tea"], 2),
    _q("eng-es10", "advanced", "error-spotting",
       "Spot the error: 'Neither the teacher nor the students was present.'",
       ["Neither", "nor", "was", "present"], 2),
    _q("eng-es11", "beginner", "error-spotting",
       "Spot the error: 'There is many books on the shelf.'",
       ["There", "is", "many", "books"], 1),
    _q("eng-es12", "advanced", "error-spotting",
       "Spot the error: 'Hardly he had slept when the alarm rang.'",
       ["Hardly", "he", "had", "slept"], 1),

    # ==================== EXTRA VOCABULARY (4) ====================
    _q("eng-x1", "intermediate", "vocabulary",
       "Choose the correctly spelled word.",
       ["occassion", "ocassion", "occasion", "occason"], 2),
    _q("eng-x2", "intermediate", "vocabulary",
       "Choose the correctly spelled word.",
       ["seperate", "separate", "separete", "seprate"], 1),
    _q("eng-x3", "advanced", "one-word",
       "One word for: 'a person who speaks many languages'.",
       ["linguist", "polyglot", "orator", "translator"], 1),
    _q("eng-x4", "advanced", "one-word",
       "One word for: 'fear of heights'.",
       ["claustrophobia", "acrophobia", "agoraphobia", "hydrophobia"], 1),
]


def get_bank() -> list[Question]:
    """Full English question bank."""
    return list(ENGLISH_BANK)


def get_passage(skill: str) -> dict | None:
    """Reading passage for an rc-p* skill tag, or None."""
    return READING_PASSAGES.get(skill)
