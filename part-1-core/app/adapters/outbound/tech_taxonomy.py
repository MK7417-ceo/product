"""Comprehensive Tech Taxonomy — every major tech tool/skill organized by category.

Proactive: the founder should never have to name tools one by one.
Each tool carries an importance level:
  "critical" — must-know for jobs (asked in most interviews)
  "high"     — very common in the industry
  "medium"   — good to know
  "low"      — niche / specialized

`related_domain` maps to a curriculum domain slug (see curriculum migration).
Pure data + helpers; zero I/O. All original descriptions.
"""
from __future__ import annotations

IMPORTANCE_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
VALID_IMPORTANCE = frozenset(IMPORTANCE_ORDER)

TECH_TAXONOMY: dict[str, dict] = {
    "backend-frameworks": {
        "name": "Backend Frameworks",
        "icon": "⚙️",
        "tools": [
            {"slug": "fastapi", "name": "FastAPI", "importance": "critical",
             "why": "Modern async Python API framework; SkillForge itself runs on it",
             "related_domain": "python"},
            {"slug": "django", "name": "Django", "importance": "high",
             "why": "Batteries-included Python framework; startups + enterprises",
             "related_domain": "python"},
            {"slug": "flask", "name": "Flask", "importance": "high",
             "why": "Lightweight Python micro-framework; great for learning APIs",
             "related_domain": "python"},
            {"slug": "spring-boot", "name": "Spring Boot", "importance": "high",
             "why": "Enterprise Java standard; banks and large companies",
             "related_domain": "java-advanced"},
            {"slug": "express", "name": "Express.js", "importance": "high",
             "why": "Minimal Node.js framework; the JS backend default",
             "related_domain": "webdev"},
            {"slug": "nestjs", "name": "NestJS", "importance": "medium",
             "why": "Structured TypeScript backend; Angular-style architecture",
             "related_domain": "webdev"},
            {"slug": "laravel", "name": "Laravel", "importance": "medium",
             "why": "Elegant PHP framework; huge freelance/agency market",
             "related_domain": "webdev"},
            {"slug": "rails", "name": "Ruby on Rails", "importance": "medium",
             "why": "Convention-over-configuration; classic startup framework",
             "related_domain": "ruby"},
            {"slug": "gin", "name": "Gin (Go)", "importance": "medium",
             "why": "Fast Go web framework for microservices",
             "related_domain": "go"},
        ],
    },
    "frontend": {
        "name": "Frontend",
        "icon": "🎨",
        "tools": [
            {"slug": "react", "name": "React", "importance": "critical",
             "why": "Dominant UI library; asked in most frontend interviews",
             "related_domain": "webdev"},
            {"slug": "nextjs", "name": "Next.js", "importance": "high",
             "why": "React meta-framework with SSR; production standard",
             "related_domain": "webdev"},
            {"slug": "typescript", "name": "TypeScript", "importance": "high",
             "why": "Typed JavaScript; required by most serious frontend jobs",
             "related_domain": "webdev"},
            {"slug": "tailwind", "name": "Tailwind CSS", "importance": "high",
             "why": "Utility-first CSS; fastest way to ship good-looking UIs",
             "related_domain": "webdev"},
            {"slug": "vue", "name": "Vue.js", "importance": "medium",
             "why": "Progressive framework; popular in Asia/Europe",
             "related_domain": "webdev"},
            {"slug": "angular", "name": "Angular", "importance": "medium",
             "why": "Full-featured Google framework; enterprise shops",
             "related_domain": "webdev"},
            {"slug": "svelte", "name": "Svelte", "importance": "medium",
             "why": "Compile-time framework; no virtual DOM overhead",
             "related_domain": "webdev"},
            {"slug": "vite", "name": "Vite", "importance": "medium",
             "why": "Blazing-fast build tool; replaced webpack for most new projects",
             "related_domain": "webdev"},
        ],
    },
    "databases": {
        "name": "Databases",
        "icon": "🗄️",
        "tools": [
            {"slug": "postgresql", "name": "PostgreSQL", "importance": "critical",
             "why": "Most-loved relational DB; default choice for new backends",
             "related_domain": "dbms"},
            {"slug": "mysql", "name": "MySQL", "importance": "high",
             "why": "Classic relational DB; WordPress/LAMP legacy + still huge",
             "related_domain": "dbms"},
            {"slug": "mongodb", "name": "MongoDB", "importance": "high",
             "why": "Document NoSQL; MERN stack staple",
             "related_domain": "dbms"},
            {"slug": "redis", "name": "Redis", "importance": "high",
             "why": "In-memory cache + queues; makes apps 10x faster",
             "related_domain": "dbms"},
            {"slug": "elasticsearch", "name": "Elasticsearch", "importance": "medium",
             "why": "Full-text search engine; powers site search everywhere",
             "related_domain": "dbms"},
            {"slug": "sqlite", "name": "SQLite", "importance": "medium",
             "why": "Zero-config embedded DB; perfect for learning + mobile",
             "related_domain": "dbms"},
            {"slug": "cassandra", "name": "Cassandra", "importance": "low",
             "why": "Wide-column NoSQL for massive write scale",
             "related_domain": "big-data"},
            {"slug": "dynamodb", "name": "DynamoDB", "importance": "medium",
             "why": "AWS serverless NoSQL; pay-per-request scaling",
             "related_domain": "aws"},
        ],
    },
    "devops-tools": {
        "name": "DevOps Tools",
        "icon": "🛠️",
        "tools": [
            {"slug": "docker", "name": "Docker", "importance": "critical",
             "why": "Container standard; 'works on my machine' killer",
             "related_domain": "devops"},
            {"slug": "kubernetes", "name": "Kubernetes", "importance": "high",
             "why": "Container orchestration; the DevOps job-interview topic",
             "related_domain": "devops"},
            {"slug": "github-actions", "name": "GitHub Actions", "importance": "high",
             "why": "CI/CD built into GitHub; simplest pipeline to learn",
             "related_domain": "devops"},
            {"slug": "terraform", "name": "Terraform", "importance": "high",
             "why": "Infrastructure as code; define cloud in files",
             "related_domain": "devops"},
            {"slug": "jenkins", "name": "Jenkins", "importance": "medium",
             "why": "Classic CI server; still runs many enterprise pipelines",
             "related_domain": "devops"},
            {"slug": "ansible", "name": "Ansible", "importance": "medium",
             "why": "Agentless config management; YAML-driven automation",
             "related_domain": "devops"},
            {"slug": "nginx", "name": "Nginx", "importance": "high",
             "why": "Reverse proxy + load balancer; sits in front of most apps",
             "related_domain": "devops"},
            {"slug": "prometheus", "name": "Prometheus", "importance": "medium",
             "why": "Metrics monitoring; pairs with Grafana dashboards",
             "related_domain": "devops"},
            {"slug": "grafana", "name": "Grafana", "importance": "medium",
             "why": "Visualization dashboards for metrics and logs",
             "related_domain": "devops"},
            {"slug": "helm", "name": "Helm", "importance": "low",
             "why": "Kubernetes package manager; charts for app deployment",
             "related_domain": "devops"},
        ],
    },
    "cloud": {
        "name": "Cloud Platforms",
        "icon": "☁️",
        "tools": [
            {"slug": "aws", "name": "AWS", "importance": "critical",
             "why": "Cloud market leader; EC2/S3/Lambda are interview staples",
             "related_domain": "aws"},
            {"slug": "gcp", "name": "Google Cloud", "importance": "medium",
             "why": "Strong in data/ML; BigQuery is best-in-class warehouse",
             "related_domain": "cloud"},
            {"slug": "azure", "name": "Azure", "importance": "medium",
             "why": "Enterprise/Microsoft shops; second-largest cloud",
             "related_domain": "cloud"},
            {"slug": "cloudflare", "name": "Cloudflare", "importance": "medium",
             "why": "CDN + DNS + edge; free tier powers half the indie web",
             "related_domain": "cloud"},
            {"slug": "vercel", "name": "Vercel", "importance": "medium",
             "why": "Zero-config frontend hosting; Next.js home",
             "related_domain": "cloud"},
        ],
    },
    "auth-security": {
        "name": "Auth & Security",
        "icon": "🔐",
        "tools": [
            {"slug": "jwt", "name": "JWT", "importance": "critical",
             "why": "Stateless auth tokens; every API interview touches this",
             "related_domain": "cybersecurity"},
            {"slug": "oauth2", "name": "OAuth 2.0", "importance": "high",
             "why": "'Login with Google' standard; delegated authorization",
             "related_domain": "cybersecurity"},
            {"slug": "bcrypt", "name": "bcrypt", "importance": "high",
             "why": "Password hashing done right; never store plaintext",
             "related_domain": "cybersecurity"},
            {"slug": "owasp", "name": "OWASP Top 10", "importance": "high",
             "why": "The 10 most critical web vulnerabilities; security interviews",
             "related_domain": "cybersecurity"},
            {"slug": "saml", "name": "SAML", "importance": "low",
             "why": "Enterprise SSO protocol; legacy but still around",
             "related_domain": "cybersecurity"},
            {"slug": "letsencrypt", "name": "Let's Encrypt / TLS", "importance": "medium",
             "why": "Free HTTPS certificates; every site needs TLS",
             "related_domain": "cybersecurity"},
        ],
    },
    "messaging": {
        "name": "Messaging & Queues",
        "icon": "📨",
        "tools": [
            {"slug": "kafka", "name": "Apache Kafka", "importance": "high",
             "why": "Event streaming at scale; backbone of data pipelines",
             "related_domain": "big-data"},
            {"slug": "rabbitmq", "name": "RabbitMQ", "importance": "medium",
             "why": "Classic message broker; task queues and workers",
             "related_domain": "devops"},
            {"slug": "celery", "name": "Celery", "importance": "medium",
             "why": "Python distributed task queue; pairs with Redis/RabbitMQ",
             "related_domain": "python"},
            {"slug": "sqs", "name": "AWS SQS", "importance": "medium",
             "why": "Serverless queues on AWS; no broker to manage",
             "related_domain": "aws"},
            {"slug": "grpc", "name": "gRPC", "importance": "medium",
             "why": "High-performance RPC; microservices communication",
             "related_domain": "system-design"},
        ],
    },
    "mobile": {
        "name": "Mobile",
        "icon": "📱",
        "tools": [
            {"slug": "flutter", "name": "Flutter", "importance": "high",
             "why": "One codebase, iOS+Android; Google's cross-platform bet",
             "related_domain": "webdev"},
            {"slug": "react-native", "name": "React Native", "importance": "high",
             "why": "Build mobile apps with React skills",
             "related_domain": "webdev"},
            {"slug": "kotlin", "name": "Kotlin", "importance": "medium",
             "why": "Official Android language; modern Java successor",
             "related_domain": "java"},
            {"slug": "swift", "name": "Swift", "importance": "medium",
             "why": "Apple's iOS language; required for native iPhone apps",
             "related_domain": "webdev"},
            {"slug": "expo", "name": "Expo", "importance": "low",
             "why": "Fastest React Native workflow; great for MVPs",
             "related_domain": "webdev"},
        ],
    },
    "ai-ml-tools": {
        "name": "AI / ML Tools",
        "icon": "🤖",
        "tools": [
            {"slug": "pytorch", "name": "PyTorch", "importance": "high",
             "why": "Research-standard deep learning; Meta's framework",
             "related_domain": "ml-basics"},
            {"slug": "tensorflow", "name": "TensorFlow", "importance": "high",
             "why": "Production deep learning; Google's framework",
             "related_domain": "ml-basics"},
            {"slug": "sklearn", "name": "scikit-learn", "importance": "high",
             "why": "Classical ML workhorse; every data science job",
             "related_domain": "data-science"},
            {"slug": "huggingface", "name": "Hugging Face", "importance": "high",
             "why": "Pretrained models hub; transformers in 3 lines of code",
             "related_domain": "ml-basics"},
            {"slug": "langchain", "name": "LangChain", "importance": "high",
             "why": "LLM app framework; RAG and agents made practical",
             "related_domain": "ml-basics"},
            {"slug": "pandas", "name": "pandas", "importance": "critical",
             "why": "Data manipulation standard; data jobs live in DataFrames",
             "related_domain": "data-science"},
            {"slug": "numpy", "name": "NumPy", "importance": "high",
             "why": "Numerical computing foundation; arrays done right",
             "related_domain": "data-science"},
            {"slug": "openai-api", "name": "OpenAI API", "importance": "medium",
             "why": "GPT models as a service; prototype AI features fast",
             "related_domain": "ml-basics"},
            {"slug": "mlflow", "name": "MLflow", "importance": "low",
             "why": "ML experiment tracking and model registry",
             "related_domain": "ml-basics"},
        ],
    },
    "big-data-tools": {
        "name": "Big Data",
        "icon": "📊",
        "tools": [
            {"slug": "spark", "name": "Apache Spark", "importance": "high",
             "why": "Distributed data processing; big-data job interviews",
             "related_domain": "big-data"},
            {"slug": "hadoop", "name": "Hadoop", "importance": "medium",
             "why": "Classic big-data ecosystem; HDFS + MapReduce concepts",
             "related_domain": "big-data"},
            {"slug": "airflow", "name": "Airflow", "importance": "medium",
             "why": "Workflow orchestration; data pipeline scheduling",
             "related_domain": "big-data"},
            {"slug": "dbt", "name": "dbt", "importance": "medium",
             "why": "SQL-based data transformations; analytics engineering",
             "related_domain": "data-analyst"},
            {"slug": "snowflake", "name": "Snowflake", "importance": "medium",
             "why": "Cloud data warehouse; separates storage and compute",
             "related_domain": "big-data"},
            {"slug": "databricks", "name": "Databricks", "importance": "low",
             "why": "Unified analytics on Spark; lakehouse platform",
             "related_domain": "big-data"},
        ],
    },
    "testing": {
        "name": "Testing",
        "icon": "🧪",
        "tools": [
            {"slug": "pytest", "name": "pytest", "importance": "high",
             "why": "Python testing standard; SkillForge's own suite runs on it",
             "related_domain": "python"},
            {"slug": "jest", "name": "Jest", "importance": "medium",
             "why": "JavaScript testing; React component tests",
             "related_domain": "webdev"},
            {"slug": "cypress", "name": "Cypress", "importance": "medium",
             "why": "End-to-end browser testing developers actually enjoy",
             "related_domain": "webdev"},
            {"slug": "selenium", "name": "Selenium", "importance": "medium",
             "why": "Classic browser automation; still in many QA job posts",
             "related_domain": "webdev"},
            {"slug": "playwright", "name": "Playwright", "importance": "medium",
             "why": "Modern E2E testing; Microsoft's cross-browser tool",
             "related_domain": "webdev"},
            {"slug": "junit", "name": "JUnit", "importance": "medium",
             "why": "Java unit testing; enterprise Java shops",
             "related_domain": "java"},
            {"slug": "postman", "name": "Postman", "importance": "medium",
             "why": "API testing and exploration; every backend dev's tool",
             "related_domain": "webdev"},
            {"slug": "k6", "name": "k6", "importance": "low",
             "why": "Load testing as code; find breaking points before users do",
             "related_domain": "devops"},
        ],
    },
    "dev-tools": {
        "name": "Developer Tools",
        "icon": "🧰",
        "tools": [
            {"slug": "git", "name": "Git", "importance": "critical",
             "why": "Version control is non-negotiable; every job needs it",
             "related_domain": "devops"},
            {"slug": "github", "name": "GitHub", "importance": "critical",
             "why": "Code hosting + portfolio; your public resume for dev jobs",
             "related_domain": "devops"},
            {"slug": "vscode", "name": "VS Code", "importance": "high",
             "why": "The editor most developers use; free and extensible",
             "related_domain": "python"},
            {"slug": "linux", "name": "Linux CLI", "importance": "high",
             "why": "Servers run Linux; terminal fluency is a superpower",
             "related_domain": "devops"},
            {"slug": "bash", "name": "Bash scripting", "importance": "medium",
             "why": "Automate repetitive tasks; glue of DevOps",
             "related_domain": "devops"},
            {"slug": "regex", "name": "Regex", "importance": "medium",
             "why": "Pattern matching for text; asked in interviews, used forever",
             "related_domain": "python"},
            {"slug": "markdown", "name": "Markdown", "importance": "medium",
             "why": "Docs and READMEs; the lingua franca of developer writing",
             "related_domain": "devops"},
        ],
    },
}


# ---------- helpers ----------

def _all_tools() -> list[dict]:
    out = []
    for cat_slug, cat in TECH_TAXONOMY.items():
        for tool in cat["tools"]:
            t = dict(tool)
            t["category"] = cat_slug
            t["category_name"] = cat["name"]
            t["category_icon"] = cat["icon"]
            out.append(t)
    return out


def list_tools(importance: str | None = None) -> list[dict]:
    """All tools, optionally filtered by importance. Sorted by importance then name."""
    tools = _all_tools()
    if importance is not None:
        if importance not in VALID_IMPORTANCE:
            raise ValueError(f"unknown importance: {importance}")
        tools = [t for t in tools if t["importance"] == importance]
    return sorted(tools, key=lambda t: (IMPORTANCE_ORDER[t["importance"]], t["name"]))


def get_tool(slug: str) -> dict | None:
    """Single tool by slug, or None."""
    for t in _all_tools():
        if t["slug"] == slug:
            return t
    return None


def get_important_tools(domain_slug: str, max_importance: str = "high") -> list[dict]:
    """Tools for a curriculum domain, at or above the given importance level.

    Sorted critical → high → medium → low. Never exposes a coding/non-coding
    label — just the tools.
    """
    if max_importance not in VALID_IMPORTANCE:
        raise ValueError(f"unknown importance: {max_importance}")
    cutoff = IMPORTANCE_ORDER[max_importance]
    tools = [
        t for t in _all_tools()
        if t["related_domain"] == domain_slug
        and IMPORTANCE_ORDER[t["importance"]] <= cutoff
    ]
    return sorted(tools, key=lambda t: (IMPORTANCE_ORDER[t["importance"]], t["name"]))


def get_critical_tools() -> list[dict]:
    """Every critical tool across all categories — the must-know list."""
    return list_tools("critical")


def list_categories() -> list[dict]:
    """Category summaries with tool counts."""
    return [
        {"slug": slug, "name": cat["name"], "icon": cat["icon"],
         "tool_count": len(cat["tools"])}
        for slug, cat in TECH_TAXONOMY.items()
    ]


def tool_count() -> int:
    return sum(len(cat["tools"]) for cat in TECH_TAXONOMY.values())
