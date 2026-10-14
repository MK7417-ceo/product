/* ============================================================
   SkillForge Guide — local rule-based brain.
   100% offline: keyword matching, zero network calls, zero API keys.
   Every topic answers in en / hi / hinglish.
   ============================================================ */
import type { LangCode } from '../../lib/translations';

export interface TourStep {
  title: string;
  text: string;
}

export interface ChatMessage {
  id: number;
  from: 'bot' | 'user';
  text: string;
}

export interface QuickChip {
  id: string;
  /** canonical english query fed to answer() */
  query: string;
  label: Record<LangCode, string>;
}

type Resp = Record<LangCode, string>;

interface Topic {
  id: string;
  keywords: string[];
  response: Resp;
}

/* ---------------- welcome / fallback ---------------- */

export function welcomeMessage(lang: LangCode): string {
  const m: Resp = {
    en: "Namaste! I'm your SkillForge guide. Ask me anything about the app — or tap 'Take a tour' for a walkthrough!",
    hi: 'नमस्ते! मैं आपका SkillForge गाइड हूं। ऐप के बारे में कुछ भी पूछें — या walkthrough के लिए ‘Take a tour’ दबाएं!',
    hinglish:
      "Namaste! Main tumhara SkillForge guide hun. App ke baare me kuch bhi pucho — ya walkthrough ke liye 'Take a tour' dabao!",
  };
  return m[lang];
}

function fallback(lang: LangCode): string {
  const m: Resp = {
    en: "Hmm, I didn't quite get that. Try asking about: assessment, roadmap, code lab, certificates, pricing, practice, or interview prep — or tap a quick chip below!",
    hi: 'हम्म, मैं समझ नहीं पाया। इनके बारे में पूछकर देखें: assessment, roadmap, code lab, certificates, pricing, practice, या interview prep — या नीचे quick chip दबाएं!',
    hinglish:
      'Hmm, main samajh nahi paya. Inke baare me puchke dekho: assessment, roadmap, code lab, certificates, pricing, practice, ya interview prep — ya neeche quick chip dabao!',
  };
  return m[lang];
}

/* ---------------- topics ---------------- */

const TOPICS: Topic[] = [
  {
    id: 'greeting',
    keywords: [
      'hello', 'hi', 'hey', 'namaste', 'namaskar', 'hii', 'helo',
      'नमस्ते', 'नमस्कार', 'हैलो', 'हाय',
    ],
    response: {
      en: "Namaste! Great to see you here. I'm your SkillForge guide — ask me about assessments, roadmaps, certificates, or tap 'Take a tour' and I'll walk you through the app step by step.",
      hi: 'नमस्ते! आपसे मिलकर अच्छा लगा। मैं आपका SkillForge गाइड हूं — असेसमेंट, रोडमैप, सर्टिफिकेट के बारे में पूछें, या ‘Take a tour’ दबाएं और मैं आपको ऐप में step-by-step घुमाऊंगा।',
      hinglish:
        "Namaste! Milke achha laga. Main tumhara SkillForge guide hun — assessment, roadmap, certificates ke baare me pucho, ya 'Take a tour' dabao aur main tumhe app me step-by-step ghumaunga.",
    },
  },
  {
    id: 'language',
    keywords: [
      'language', 'bhasha', 'hindi', 'hinglish', 'english language', 'change language',
      'भाषा', 'हिन्दी', 'हिंदी', 'अंग्रेजी',
    ],
    response: {
      en: 'You can use SkillForge in English, Hindi (हिन्दी), or Hinglish. Tap the language chips at the top of this panel — or the language switcher in the top navigation — and the whole app, including me, switches instantly. Your choice is saved.',
      hi: 'आप SkillForge को English, Hindi (हिन्दी) या Hinglish में चला सकते हैं। इस panel के ऊपर language chips दबाएं — या top navigation में language switcher — और पूरा ऐप, जिसमें मैं भी शामिल हूं, तुरंत बदल जाएगा। आपकी choice save हो जाती है।',
      hinglish:
        'Tum SkillForge ko English, Hindi (हिन्दी) ya Hinglish me chala sakte ho. Is panel ke upar language chips dabao — ya top navigation me language switcher — aur poora app, jisme main bhi hun, turant badal jayega. Tumhari choice save ho jaati hai.',
    },
  },
  {
    id: 'english-track',
    keywords: [
      'english track', 'ielts', 'spoken english', 'speaking', 'angrezi',
      'अंग्रेजी', 'अंग्रेज़ी',
    ],
    response: {
      en: "The English track takes you to IELTS-level fluency with daily sets, speaking practice, and server-side scoring. It's built for aspirants targeting foreign companies. Check the English page for today's set.",
      hi: 'English track आपको daily sets, speaking practice और server-side scoring के साथ IELTS-level fluency तक ले जाता है। यह foreign companies के aspirants के लिए बनाया गया है। आज का set English page पर देखें।',
      hinglish:
        'English track tumhe daily sets, speaking practice aur server-side scoring ke saath IELTS-level fluency tak le jaata hai. Ye foreign companies target karne walon ke liye banaya gaya hai. Aaj ka set English page par dekho.',
    },
  },
  {
    id: 'assessment',
    keywords: [
      'assessment', 'test', 'exam', 'quiz', 'verify', 'verification', 'placement',
      'level', 'marks', 'score', 'result', 'pariksha', 'imtihan',
      'मूल्यांकन', 'परीक्षा', 'टेस्ट', 'असेसमेंट', 'प्लेसमेंट', 'अंक',
    ],
    response: {
      en: 'The placement assessment has 23 questions: 15 MCQs (5 beginner, 5 intermediate, 5 advanced), 5 coding problems, and 3 written answers. MCQs decide your verified level — score 70%+ at a level with all lower levels passing. Coding and written answers are graded locally and shown separately as skill gaps.',
      hi: 'प्लेसमेंट असेसमेंट में 23 प्रश्न होते हैं: 15 MCQ (5 beginner, 5 intermediate, 5 advanced), 5 कोडिंग प्रश्न और 3 लिखित उत्तर। MCQ आपका verified level तय करते हैं — किसी level पर 70%+ स्कोर करें और निचले सभी level पास हों। कोडिंग और लिखित उत्तर स्थानीय रूप से ग्रेड होते हैं और अलग से skill gaps में दिखते हैं।',
      hinglish:
        'Placement assessment me 23 questions hote hain: 15 MCQ (5 beginner, 5 intermediate, 5 advanced), 5 coding problems aur 3 written answers. MCQ tumhara verified level decide karte hain — kisi level par 70%+ lao aur neeche ke saare levels pass ho. Coding aur written locally grade hote hain aur alag se skill gaps me dikhte hain.',
    },
  },
  {
    id: 'roadmap',
    keywords: [
      'roadmap', 'road map', 'learning path', 'study plan', 'plan', 'syllabus',
      'रoadमैप', 'रोडमैप', 'योजना', 'पढ़ाई', 'rasta',
    ],
    response: {
      en: 'Your roadmap is built from your real skill gaps — never generic. Each task has a title, why it matters, target skills, prerequisites, effort estimate, and acceptance criteria. Complete tasks, submit evidence, and the roadmap adapts. Regenerating never deletes your completed work.',
      hi: 'आपका रोडमैप आपकी असली skill gaps से बनता है — कभी generic नहीं। हर task में title, क्यों जरूरी है, target skills, prerequisites, समय का अनुमान और acceptance criteria होता है। Tasks पूरे करें, evidence जमा करें, और रोडमैप खुद adapt करेगा। Regenerate करने पर आपका पूरा किया काम कभी delete नहीं होता।',
      hinglish:
        'Tumhara roadmap tumhari real skill gaps se banta hai — kabhi generic nahi. Har task me title, kyun zaroori hai, target skills, prerequisites, time estimate aur acceptance criteria hota hai. Tasks complete karo, evidence submit karo, roadmap khud adapt karega. Regenerate karne par tumhara completed kaam kabhi delete nahi hota.',
    },
  },
  {
    id: 'codelab',
    keywords: [
      'code lab', 'codelab', 'coding', 'compiler', 'program', 'code',
      'कोड', 'कोडिंग', 'प्रोग्राम',
    ],
    response: {
      en: 'Code Lab is your in-browser compiler — write and run C, C++, Python, and Java right here, no setup needed. Use it for daily practice, DSA problems, and placement coding questions. Your submissions are checked against hidden tests.',
      hi: 'Code Lab आपका in-browser compiler है — C, C++, Python और Java यहीं लिखें और चलाएं, कोई setup नहीं चाहिए। Daily practice, DSA problems और placement coding questions के लिए इसका उपयोग करें। आपके submissions hidden tests पर check होते हैं।',
      hinglish:
        'Code Lab tumhara in-browser compiler hai — C, C++, Python aur Java yahin likho aur chalao, koi setup nahi chahiye. Daily practice, DSA problems aur placement coding questions ke liye use karo. Tumhare submissions hidden tests par check hote hain.',
    },
  },
  {
    id: 'certificates',
    keywords: [
      'certificate', 'certification', 'cert', 'certificates', 'verify certificate',
      'प्रमाणपत्र', 'सर्टिफिकेट', 'सर्टिफिकेट्स',
    ],
    response: {
      en: 'You earn certificates by completing assessments and learning milestones — each has a unique verification code anyone can check. Share them on LinkedIn or your resume. Also visit the Certificate Directory to discover free and budget-friendly certificates from platforms like Forage, Great Learning, and freeCodeCamp.',
      hi: 'Assessments और learning milestones पूरे करके आप certificates कमाते हैं — हर एक में unique verification code होता है जिसे कोई भी check कर सकता है। इन्हें LinkedIn या resume पर share करें। Free और budget-friendly certificates के लिए Certificate Directory भी देखें — Forage, Great Learning और freeCodeCamp जैसे platforms से।',
      hinglish:
        'Assessments aur learning milestones complete karke tum certificates earn karte ho — har ek me unique verification code hota hai jo koi bhi check kar sakta hai. LinkedIn ya resume par share karo. Free aur budget-friendly certificates ke liye Certificate Directory bhi dekho — Forage, Great Learning, freeCodeCamp jaise platforms se.',
    },
  },
  {
    id: 'pricing',
    keywords: [
      'price', 'pricing', 'cost', 'pro', 'expert', 'free plan', 'paid',
      'subscription', 'upgrade', 'premium', 'कीमत', 'दाम', 'पैसा', 'शुल्क',
      'kimat', 'paisa', 'daam',
    ],
    response: {
      en: 'SkillForge has three tiers: Free (placement assessment, basic roadmap, daily practice), Pro (full roadmaps, code lab, certificates, AI feedback), and Expert (everything + interview prep, priority support). Go to the Billing page to see current prices and upgrade — checkout is secure.',
      hi: 'SkillForge के तीन tiers हैं: Free (placement assessment, basic roadmap, daily practice), Pro (full roadmaps, code lab, certificates, AI feedback), और Expert (सब कुछ + interview prep, priority support)। मौजूदा prices और upgrade के लिए Billing page पर जाएं — checkout secure है।',
      hinglish:
        'SkillForge ke teen tiers hain: Free (placement assessment, basic roadmap, daily practice), Pro (full roadmaps, code lab, certificates, AI feedback), aur Expert (sab kuch + interview prep, priority support). Current prices aur upgrade ke liye Billing page par jao — checkout secure hai.',
    },
  },
  {
    id: 'practice',
    keywords: [
      'practice', 'dsa', 'daily', 'streak', 'questions daily', 'leetcode',
      'अभ्यास', 'प्रैक्टिस', 'रोज़',
    ],
    response: {
      en: 'Daily Practice gives you 2–5 handpicked questions every day, plus a Daily DSA problem to keep your streak alive. Consistency beats intensity — 20 minutes a day builds real skill. Find it on the Practice page.',
      hi: 'Daily Practice आपको हर दिन 2–5 चुने हुए प्रश्न देता है, साथ में Daily DSA problem ताकि आपकी streak बनी रहे। Consistency intensity से बेहतर है — रोज़ 20 मिनट से असली skill बनती है। Practice page पर मिलेगा।',
      hinglish:
        'Daily Practice tumhe roz 2–5 handpicked questions deta hai, saath me Daily DSA problem taaki streak bani rahe. Consistency intensity se better hai — roz 20 minute se real skill banti hai. Practice page par milega.',
    },
  },
  {
    id: 'evidence',
    keywords: [
      'evidence', 'proof', 'submit', 'submission', 'सबूत', 'प्रमाण', 'saboot',
      'pramaan',
    ],
    response: {
      en: 'Evidence is proof of your work — code, project links, or write-ups you submit after completing a roadmap task. Verified evidence builds your skill profile and unlocks certificates. Be honest: only submit work you actually did.',
      hi: 'Evidence आपके काम का सबूत है — roadmap task पूरा करने के बाद जमा किया गया code, project links या write-ups। Verified evidence आपकी skill profile बनाता है और certificates unlock करता है। ईमानदार रहें: वही submit करें जो आपने सच में किया है।',
      hinglish:
        'Evidence tumhare kaam ka proof hai — roadmap task complete karne ke baad submit kiya gaya code, project links ya write-ups. Verified evidence tumhari skill profile banata hai aur certificates unlock karta hai. Honest raho: wahi submit karo jo tumne actually kiya hai.',
    },
  },
  {
    id: 'portfolio',
    keywords: [
      'portfolio', 'github', 'project', 'projects', 'पोर्टफोलियो', 'परियोजना',
    ],
    response: {
      en: 'The Portfolio builder turns your projects and certificates into a polished portfolio site in about a week of guided steps. You can publish it as a GitHub repo with Pages hosting — you own it completely. Start from the Portfolio page.',
      hi: 'Portfolio builder आपके projects और certificates को guided steps में लगभग एक हफ्ते में polished portfolio site में बदल देता है। इसे GitHub repo के रूप में Pages hosting के साथ publish कर सकते हैं — यह पूरी तरह आपका होता है। Portfolio page से शुरू करें।',
      hinglish:
        'Portfolio builder tumhare projects aur certificates ko guided steps me lagbhag ek hafte me polished portfolio site me badal deta hai. Ise GitHub repo ke roop me Pages hosting ke saath publish kar sakte ho — ye completely tumhara hota hai. Portfolio page se start karo.',
    },
  },
  {
    id: 'interview',
    keywords: [
      'interview', 'job', 'hr round', 'pi', 'gd', 'mock', 'placement drive',
      'इंटरव्यू', 'नौकरी', 'naukri',
    ],
    response: {
      en: 'Interview Prep covers the full hiring loop: resume and JD matching, technical questions, quant, typing, group discussion, and personal interview practice. There are weekly mock tests — one compulsory and one optional. Camera-ON proctoring keeps mocks realistic.',
      hi: 'Interview Prep पूरी hiring loop cover करता है: resume और JD matching, technical questions, quant, typing, group discussion और personal interview practice। Weekly mock tests होते हैं — एक compulsory और एक optional। Camera-ON proctoring mocks को realistic बनाता है।',
      hinglish:
        'Interview Prep poori hiring loop cover karta hai: resume aur JD matching, technical questions, quant, typing, group discussion aur personal interview practice. Weekly mock tests hote hain — ek compulsory aur ek optional. Camera-ON proctoring mocks ko realistic banata hai.',
    },
  },
  {
    id: 'profile',
    keywords: [
      'profile', 'account', 'my details', 'edit profile', 'प्रोफाइल', 'खाता',
      'अकाउंट',
    ],
    response: {
      en: 'Your profile is your career snapshot: education, experience, current skills, target role, domain, and level. It powers your personalized roadmap — keep it updated as you grow. You can edit it anytime from the Profile page.',
      hi: 'आपकी profile आपका career snapshot है: education, experience, current skills, target role, domain और level। यही आपके personalized roadmap को power देती है — जैसे-जैसे आगे बढ़ें इसे update रखें। Profile page से कभी भी edit कर सकते हैं।',
      hinglish:
        'Tumhari profile tumhara career snapshot hai: education, experience, current skills, target role, domain aur level. Yehi tumhare personalized roadmap ko power deti hai — jaise-jaise grow karo ise updated rakho. Profile page se kabhi bhi edit kar sakte ho.',
    },
  },
  {
    id: 'login',
    keywords: [
      'login', 'log in', 'sign in', 'signin', 'register', 'sign up', 'signup',
      'password', 'forgot', 'reset password', 'google login', 'otp',
      'लॉगिन', 'पासवर्ड', 'रजिस्टर',
    ],
    response: {
      en: "You can register with email + password or continue with Google. Forgot your password? Use 'Forgot password' on the login page to reset it via email. Keep your account safe — never share your password.",
      hi: 'आप email + password से register कर सकते हैं या Google से continue कर सकते हैं। Password भूल गए? Login page पर ‘Forgot password’ से email द्वारा reset करें। अपना account सुरक्षित रखें — password कभी share न करें।',
      hinglish:
        "Tum email + password se register kar sakte ho ya Google se continue kar sakte ho. Password bhool gaye? Login page par 'Forgot password' se email dwara reset karo. Apna account safe rakho — password kabhi share mat karo.",
    },
  },
];

/* ---------------- public API ---------------- */

/** Answer a free-text question in the requested language. Pure function, no I/O. */
export function answer(question: string, lang: LangCode): string {
  const q = question.toLowerCase().trim();
  if (!q) return fallback(lang);
  for (const topic of TOPICS) {
    for (const kw of topic.keywords) {
      if (matchesKeyword(q, kw)) return topic.response[lang];
    }
  }
  return fallback(lang);
}

/**
 * Keyword matching with a guard for short keywords: keywords of length ≤ 3
 * must match a whole token (unicode-aware split), so 'hi' doesn't fire inside
 * 'chahiye' and 'pi' doesn't fire inside 'capital'. Longer keywords use
 * substring matching (safe for multi-word / Devanagari phrases).
 */
function matchesKeyword(q: string, kw: string): boolean {
  const k = kw.toLowerCase();
  if (k.length <= 3) {
    const tokens = q.split(/[^\p{L}\p{N}]+/u).filter(Boolean);
    return tokens.includes(k);
  }
  return q.includes(k);
}

/** 5-step product tour, localized. */
export function tourSteps(lang: LangCode): TourStep[] {
  const steps: Record<LangCode, TourStep[]> = {
    en: [
      {
        title: 'Welcome to SkillForge!',
        text: "I'm your personal guide. SkillForge takes you from learner to job-ready engineer: assess your skills, follow a personal roadmap, practice daily, and prove it with evidence and certificates. Let's take a quick look around!",
      },
      {
        title: 'Your Dashboard',
        text: 'This is home base — your verified level, streak, today\u2019s tasks, and progress at a glance. Come back daily: small consistent steps beat weekend marathons.',
      },
      {
        title: 'Take the Assessment',
        text: 'Start with the 23-question placement: 15 MCQs, 5 coding problems, 3 written answers. It verifies your true level — no self-rating, no guessing. Your roadmap is built on this result.',
      },
      {
        title: 'Follow Your Roadmap',
        text: 'Each task targets a real gap found in your assessment, with prerequisites respected. Complete tasks, submit evidence, and watch skills turn green. Regenerating adapts the future — never erases your past.',
      },
      {
        title: 'Earn Certificates',
        text: "Finish milestones to earn verifiable certificates you can share on LinkedIn. Then explore the Certificate Directory for free and budget courses from Forage, Great Learning, and more. That's the tour — ask me anything, anytime!",
      },
    ],
    hi: [
      {
        title: 'SkillForge में आपका स्वागत है!',
        text: 'मैं आपका personal guide हूं। SkillForge आपको learner से job-ready engineer बनाता है: skills का आकलन करें, personal roadmap follow करें, रोज़ practice करें, और evidence व certificates से साबित करें। चलिए जल्दी से देख लेते हैं!',
      },
      {
        title: 'आपका Dashboard',
        text: 'यह home base है — आपका verified level, streak, आज के tasks और progress एक नज़र में। रोज़ आएं: छोटे consistent steps weekend marathons से बेहतर हैं।',
      },
      {
        title: 'Assessment दें',
        text: '23-प्रश्न placement से शुरू करें: 15 MCQ, 5 coding problems, 3 लिखित उत्तर। यह आपका true level verify करता है — कोई self-rating नहीं, कोई guessing नहीं। आपका roadmap इसी result पर बनता है।',
      },
      {
        title: 'अपना Roadmap Follow करें',
        text: 'हर task आपके assessment में मिली real gap को target करता है, prerequisites का सम्मान करते हुए। Tasks पूरे करें, evidence जमा करें, और skills को green होते देखें। Regenerate भविष्य को adapt करता है — अतीत कभी मिटाता नहीं।',
      },
      {
        title: 'Certificates कमाएं',
        text: 'Milestones पूरे करके verifiable certificates कमाएं जिन्हें LinkedIn पर share कर सकते हैं। फिर Certificate Directory में Forage, Great Learning आदि से free और budget courses देखें। Tour खत्म — कभी भी कुछ भी पूछें!',
      },
    ],
    hinglish: [
      {
        title: 'SkillForge me welcome!',
        text: 'Main tumhara personal guide hun. SkillForge tumhe learner se job-ready engineer banata hai: skills assess karo, personal roadmap follow karo, roz practice karo, aur evidence aur certificates se prove karo. Chalo jaldi se dekh lete hain!',
      },
      {
        title: 'Tumhara Dashboard',
        text: 'Ye home base hai — tumhara verified level, streak, aaj ke tasks aur progress ek nazar me. Roz aao: chhote consistent steps weekend marathons se better hain.',
      },
      {
        title: 'Assessment do',
        text: '23-question placement se start karo: 15 MCQ, 5 coding problems, 3 written answers. Ye tumhara true level verify karta hai — koi self-rating nahi, koi guessing nahi. Tumhara roadmap isi result par banta hai.',
      },
      {
        title: 'Apna Roadmap follow karo',
        text: 'Har task tumhare assessment me mili real gap ko target karta hai, prerequisites respect karte hue. Tasks complete karo, evidence submit karo, aur skills ko green hote dekho. Regenerate future ko adapt karta hai — past kabhi erase nahi karta.',
      },
      {
        title: 'Certificates earn karo',
        text: 'Milestones complete karke verifiable certificates earn karo jinhe LinkedIn par share kar sakte ho. Phir Certificate Directory me Forage, Great Learning se free aur budget courses dekho. Tour khatm — kabhi bhi kuch bhi pucho!',
      },
    ],
  };
  return steps[lang];
}

/** Quick-action chips shown under the welcome message. `tour` is a special action. */
export const quickChips: QuickChip[] = [
  {
    id: 'tour',
    query: '__tour__',
    label: { en: 'Take a tour', hi: 'टूर लें', hinglish: 'Tour lo' },
  },
  {
    id: 'assessment',
    query: 'How does the assessment work?',
    label: {
      en: 'How assessment works',
      hi: 'असेसमेंट कैसे काम करता है',
      hinglish: 'Assessment kaise kaam karta hai',
    },
  },
  {
    id: 'roadmap',
    query: 'What is a roadmap?',
    label: { en: 'What is roadmap?', hi: 'रोडमैप क्या है?', hinglish: 'Roadmap kya hai?' },
  },
  {
    id: 'certificates',
    query: 'How do I get certificates?',
    label: { en: 'Get certificates', hi: 'सर्टिफिकेट पाएं', hinglish: 'Certificates pao' },
  },
  {
    id: 'language',
    query: 'How do I change the language?',
    label: { en: 'Change language', hi: 'भाषा बदलें', hinglish: 'Language badlo' },
  },
];

/** Localized UI strings for the panel chrome (header, input, tour controls). */
export const uiStrings: Record<LangCode, Record<string, string>> = {
  en: {
    title: 'SkillForge Guide',
    subtitle: 'Ask me anything',
    placeholder: 'Type your question...',
    send: 'Send',
    close: 'Close',
    tourNext: 'Next',
    tourBack: 'Back',
    tourSkip: 'Skip tour',
    tourDone: 'Start exploring!',
    tourStepOf: 'Step',
    typing: 'Guide is typing…',
  },
  hi: {
    title: 'SkillForge गाइड',
    subtitle: 'कुछ भी पूछें',
    placeholder: 'अपना प्रश्न लिखें...',
    send: 'भेजें',
    close: 'बंद करें',
    tourNext: 'आगे',
    tourBack: 'पीछे',
    tourSkip: 'टूर छोड़ें',
    tourDone: 'एक्सप्लोर शुरू करें!',
    tourStepOf: 'चरण',
    typing: 'गाइड लिख रहा है…',
  },
  hinglish: {
    title: 'SkillForge Guide',
    subtitle: 'Kuch bhi pucho',
    placeholder: 'Apna question likho...',
    send: 'Bhejo',
    close: 'Band karo',
    tourNext: 'Aage',
    tourBack: 'Peeche',
    tourSkip: 'Tour skip karo',
    tourDone: 'Explore shuru karo!',
    tourStepOf: 'Step',
    typing: 'Guide likh raha hai…',
  },
};

export function ui(lang: LangCode, key: string): string {
  return uiStrings[lang][key] ?? uiStrings.en[key] ?? key;
}
