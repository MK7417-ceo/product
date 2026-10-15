"""Curriculum tables: domains, modules, lessons, questions, study plans, daily tasks.

Revision ID: m1n2curr001
Revises: l1m2cms001

Seeds 24 curriculum domains (10 B.Tech CS core + 7 languages + 7 tech domains)
with 2-4 modules each. Lesson content and questions are added by content teams
/ sibling agents afterwards — this migration is the STRUCTURE.
"""
from alembic import op
import sqlalchemy as sa

revision = "m1n2curr001"
down_revision = "l1m2cms001"
branch_labels = None
depends_on = None


# (slug, name, icon, description, category, order)
DOMAINS = [
    # ---- B.Tech CS core subjects ----
    ("dsa", "Data Structures & Algorithms", "🧠",
     "Arrays to dynamic programming — the heart of every tech interview", "cs-core", 1),
    ("os", "Operating Systems", "⚙️",
     "Processes, memory, scheduling, deadlocks — how computers really run", "cs-core", 2),
    ("dbms", "Database Management Systems", "🗄️",
     "ER models, SQL, normalization, transactions, indexing", "cs-core", 3),
    ("cn", "Computer Networks", "🌐",
     "OSI, TCP/IP, routing, DNS — how the internet works", "cs-core", 4),
    ("oop", "Object Oriented Programming", "🧩",
     "Classes, inheritance, polymorphism, design patterns", "cs-core", 5),
    ("coa", "Computer Organization & Architecture", "💻",
     "CPU, memory hierarchy, pipelining — hardware meets software", "cs-core", 6),
    ("discrete-math", "Discrete Mathematics", "🔢",
     "Logic, sets, combinatorics, graphs — the math behind CS", "cs-core", 7),
    ("software-eng", "Software Engineering", "🏗️",
     "SDLC, Agile, testing, clean code — building software professionally", "cs-core", 8),
    ("toc", "Theory of Computation", "🔮",
     "Automata, grammars, Turing machines, complexity classes", "cs-core", 9),
    ("compiler", "Compiler Design", "🔧",
     "Lexing, parsing, code generation — how languages become programs", "cs-core", 10),
    # ---- Programming languages ----
    ("c", "C Programming", "🔵",
     "Pointers, memory, systems programming — the mother of languages", "language", 20),
    ("python", "Python", "🐍",
     "From basics to advanced — the most versatile language", "language", 21),
    ("java", "Java", "☕",
     "OOP, collections, multithreading — enterprise backbone", "language", 22),
    ("javascript", "JavaScript", "🟨",
     "The language of the web — frontend to backend", "language", 23),
    ("r-lang", "R Programming", "📉",
     "Statistics and data analysis — the data scientist's language", "language", 24),
    ("ruby", "Ruby", "💎",
     "Elegant syntax, Rails — developer happiness", "language", 25),
    ("go", "Go (Golang)", "🐹",
     "Concurrency, simplicity — the cloud-native language", "language", 26),
    # ---- Tech domains ----
    ("webdev", "Web Development", "🌍",
     "HTML to deployment — build complete web applications", "tech-domain", 40),
    ("ml-basics", "Machine Learning", "🤖",
     "Supervised, unsupervised, evaluation — teach machines to learn", "tech-domain", 41),
    ("data-science", "Data Science", "📊",
     "Statistics to ML pipelines — turn data into decisions", "tech-domain", 42),
    ("data-analyst", "Data Analytics", "📈",
     "SQL, dashboards, storytelling — insights from data", "tech-domain", 43),
    ("devops", "DevOps", "🛠️",
     "CI/CD, Docker, Kubernetes — ship software like a pro", "tech-domain", 44),
    ("cybersecurity", "Cybersecurity", "🛡️",
     "Cryptography, ethical hacking — defend the digital world", "tech-domain", 45),
    ("cloud", "Cloud Computing", "☁️",
     "AWS, storage, serverless — computing without servers", "tech-domain", 46),
]

# domain_slug -> [(module_slug, name, description, estimated_days)]
MODULES = {
    "dsa": [
        ("arrays-strings", "Arrays & Strings", "Foundation: traversal, two pointers, sliding window", 10),
        ("linked-lists", "Linked Lists", "Singly, doubly, fast-slow pointers, reversal", 7),
        ("stacks-queues", "Stacks & Queues", "LIFO/FIFO, monotonic stack, BFS patterns", 7),
        ("trees-graphs", "Trees & Graphs", "BST, traversals, DFS/BFS, shortest paths", 14),
        ("sorting-searching", "Sorting & Searching", "Binary search patterns, merge/quick sort internals", 7),
        ("dynamic-programming", "Dynamic Programming", "Memoization, tabulation, classic DP patterns", 14),
        ("hashing-heaps", "Hashing & Heaps", "Hash maps, priority queues, top-K patterns", 7),
    ],
    "os": [
        ("processes-threads", "Processes & Threads", "PCB, context switching, multithreading", 7),
        ("scheduling", "CPU Scheduling", "FCFS, SJF, Round Robin, priority scheduling", 5),
        ("synchronization", "Synchronization & Deadlocks", "Mutex, semaphores, deadlock conditions & prevention", 7),
        ("memory-management", "Memory Management", "Paging, segmentation, virtual memory, page replacement", 7),
        ("file-systems", "File Systems & IO", "Inodes, journaling, disk scheduling", 5),
    ],
    "dbms": [
        ("er-model", "ER Model & Design", "Entities, relationships, schema design", 5),
        ("sql", "SQL Mastery", "Joins, subqueries, window functions, optimization", 10),
        ("normalization", "Normalization", "1NF to BCNF, denormalization trade-offs", 5),
        ("transactions", "Transactions & Concurrency", "ACID, isolation levels, locking", 7),
        ("indexing", "Indexing & Query Plans", "B-trees, EXPLAIN, performance tuning", 5),
    ],
    "cn": [
        ("network-models", "Network Models", "OSI vs TCP/IP, encapsulation", 5),
        ("ip-addressing", "IP Addressing & Subnetting", "IPv4/IPv6, CIDR, NAT", 7),
        ("tcp-udp", "TCP & UDP", "Handshake, flow control, congestion control", 7),
        ("routing-switching", "Routing & Switching", "Distance vector, link state, VLANs", 7),
        ("application-layer", "Application Layer", "HTTP, DNS, TLS, WebSockets", 7),
    ],
    "oop": [
        ("classes-objects", "Classes & Objects", "Encapsulation, constructors, access modifiers", 5),
        ("inheritance-poly", "Inheritance & Polymorphism", "IS-A vs HAS-A, virtual functions, interfaces", 7),
        ("abstraction", "Abstraction & SOLID", "Abstract classes, SOLID principles", 5),
        ("design-patterns", "Design Patterns", "Singleton, factory, observer, strategy", 10),
    ],
    "coa": [
        ("number-systems", "Number Systems & Logic", "Binary, Boolean algebra, gates", 5),
        ("cpu-architecture", "CPU Architecture", "ALU, control unit, instruction cycle", 7),
        ("memory-hierarchy", "Memory Hierarchy", "Cache, locality, virtual memory hardware", 5),
        ("pipelining", "Pipelining & Parallelism", "Hazards, superscalar, multicore", 7),
    ],
    "discrete-math": [
        ("logic-sets", "Logic & Sets", "Propositional logic, set operations, proofs", 7),
        ("combinatorics", "Combinatorics", "Permutations, combinations, pigeonhole", 7),
        ("graph-theory", "Graph Theory", "Paths, trees, coloring, Euler/Hamilton", 7),
        ("recurrence", "Recurrence & Induction", "Mathematical induction, recurrence relations", 5),
    ],
    "software-eng": [
        ("sdlc", "SDLC & Agile", "Waterfall, Scrum, Kanban, estimation", 5),
        ("testing", "Testing", "Unit, integration, TDD, test pyramids", 7),
        ("version-control", "Version Control", "Git workflows, branching strategies, PRs", 5),
        ("design-principles", "Design Principles", "DRY, KISS, clean code, refactoring", 7),
    ],
    "toc": [
        ("automata", "Finite Automata", "DFA, NFA, epsilon transitions", 7),
        ("regular-languages", "Regular Languages", "Regex, pumping lemma", 5),
        ("context-free", "Context-Free Grammars", "PDA, parsing basics", 7),
        ("turing-complexity", "Turing Machines & Complexity", "Decidability, P vs NP", 7),
    ],
    "compiler": [
        ("lexical-analysis", "Lexical Analysis", "Tokens, regex-based lexers", 5),
        ("parsing", "Parsing", "LL, LR, AST construction", 7),
        ("semantic-analysis", "Semantic Analysis", "Type checking, symbol tables", 5),
        ("code-generation", "Code Generation", "IR, optimization basics", 7),
    ],
    "c": [
        ("c-basics", "C Basics", "Syntax, control flow, functions", 7),
        ("pointers", "Pointers", "Pointer arithmetic, double pointers, function pointers", 10),
        ("memory-c", "Memory Management", "Stack vs heap, malloc/free, valgrind", 7),
        ("data-structures-c", "Data Structures in C", "Linked lists, trees from scratch", 10),
        ("file-io", "File I/O & Preprocessor", "Streams, macros, multi-file programs", 5),
    ],
    "python": [
        ("python-basics", "Python Basics", "Syntax, data types, control flow", 7),
        ("python-ds", "Data Structures", "Lists, dicts, sets, comprehensions", 7),
        ("functions-modules", "Functions & Modules", "Decorators, generators, packaging", 7),
        ("oop-python", "OOP in Python", "Classes, dunder methods, dataclasses", 7),
        ("libraries", "Essential Libraries", "NumPy, pandas, requests basics", 10),
    ],
    "java": [
        ("java-basics", "Java Basics", "JVM, syntax, data types", 7),
        ("oop-java", "OOP in Java", "Inheritance, interfaces, abstract classes", 7),
        ("collections", "Collections Framework", "List, Set, Map, streams", 10),
        ("exceptions", "Exceptions & IO", "Checked vs unchecked, try-with-resources", 5),
        ("multithreading-java", "Multithreading", "Threads, synchronized, executors", 7),
    ],
    "javascript": [
        ("js-basics", "JS Basics", "Variables, types, functions, scope", 7),
        ("dom", "DOM & Events", "Selectors, event loop, async patterns", 7),
        ("es6", "Modern JS (ES6+)", "Arrow functions, destructuring, modules", 5),
        ("async-js", "Async JavaScript", "Promises, async/await, fetch", 7),
        ("nodejs-basics", "Node.js Basics", "NPM, Express intro, APIs", 10),
    ],
    "r-lang": [
        ("r-basics", "R Basics", "Vectors, data types, control flow", 5),
        ("dataframes", "Data Frames", "dplyr: filter, select, mutate, summarize", 7),
        ("visualization-r", "Visualization", "ggplot2 grammar of graphics", 7),
        ("statistics-r", "Statistics in R", "Hypothesis tests, regression", 7),
    ],
    "ruby": [
        ("ruby-basics", "Ruby Basics", "Syntax, blocks, enumerables", 7),
        ("oop-ruby", "OOP in Ruby", "Classes, modules, mixins", 7),
        ("ruby-advanced", "Advanced Ruby", "Metaprogramming basics, gems", 5),
        ("rails-intro", "Rails Intro", "MVC, routing, ActiveRecord basics", 10),
    ],
    "go": [
        ("go-basics", "Go Basics", "Syntax, types, functions, packages", 7),
        ("concurrency", "Concurrency", "Goroutines, channels, select", 10),
        ("go-tooling", "Tooling & Modules", "go mod, testing, profiling", 5),
    ],
    "webdev": [
        ("html-css", "HTML & CSS", "Semantic HTML, flexbox, grid, responsive", 10),
        ("javascript-frontend", "Frontend JS", "DOM, fetch, SPA concepts", 10),
        ("backend-basics", "Backend Basics", "REST APIs, Express/Django intro", 14),
        ("databases-web", "Databases for Web", "PostgreSQL/MongoDB basics, ORMs", 7),
        ("deployment", "Deployment", "Hosting, CI/CD basics, domains & TLS", 7),
    ],
    "ml-basics": [
        ("math-for-ml", "Math for ML", "Linear algebra, probability essentials", 10),
        ("supervised", "Supervised Learning", "Regression, classification, trees", 14),
        ("unsupervised", "Unsupervised Learning", "Clustering, dimensionality reduction", 7),
        ("model-evaluation", "Model Evaluation", "Cross-validation, metrics, overfitting", 7),
    ],
    "data-science": [
        ("statistics", "Statistics", "Distributions, hypothesis testing", 10),
        ("data-wrangling", "Data Wrangling", "pandas, cleaning, feature engineering", 14),
        ("visualization", "Visualization", "Matplotlib, seaborn, storytelling", 7),
        ("ml-pipeline", "ML Pipeline", "End-to-end project: train, evaluate, deploy", 14),
    ],
    "data-analyst": [
        ("sql-analytics", "SQL for Analytics", "Joins, aggregations, window functions", 10),
        ("excel", "Spreadsheets", "Pivot tables, VLOOKUP/XLOOKUP, formulas", 7),
        ("dashboards", "Dashboards", "Power BI / Tableau basics", 10),
        ("storytelling", "Data Storytelling", "KPIs, narratives, stakeholder reports", 5),
    ],
    "devops": [
        ("linux", "Linux Essentials", "Shell, permissions, processes, networking cmds", 7),
        ("git-cicd", "Git & CI/CD", "Branching, GitHub Actions, pipelines", 10),
        ("docker", "Docker", "Images, containers, compose", 10),
        ("kubernetes-basics", "Kubernetes Basics", "Pods, deployments, services", 14),
        ("monitoring", "Monitoring & IaC", "Prometheus, Terraform basics", 7),
    ],
    "cybersecurity": [
        ("security-basics", "Security Fundamentals", "Threat model, CIA triad, OWASP top 10", 7),
        ("cryptography", "Cryptography", "Symmetric/asymmetric, hashing, TLS", 7),
        ("network-security-cyber", "Network Security", "Firewalls, VPNs, intrusion detection", 7),
        ("ethical-hacking-intro", "Ethical Hacking Intro", "Recon, scanning, labs (legal only)", 10),
    ],
    "cloud": [
        ("cloud-basics", "Cloud Fundamentals", "IaaS/PaaS/SaaS, regions, pricing", 5),
        ("aws-core", "AWS Core Services", "EC2, S3, IAM, VPC", 14),
        ("storage-compute", "Storage & Compute", "Databases on cloud, load balancing", 7),
        ("serverless", "Serverless", "Lambda, API Gateway, event-driven", 7),
    ],
}


def upgrade() -> None:
    # ---- curriculum_domains ----
    op.create_table(
        "curriculum_domains",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("slug", sa.String(80), nullable=False, unique=True, index=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("icon", sa.String(80), nullable=False, server_default=""),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("category", sa.String(16), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="1"),
    )
    # ---- curriculum_modules ----
    op.create_table(
        "curriculum_modules",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("domain_slug", sa.String(80), nullable=False, index=True),
        sa.Column("slug", sa.String(80), nullable=False, index=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("order_index", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("estimated_days", sa.Integer(), nullable=False, server_default="7"),
        sa.ForeignKeyConstraint(["domain_slug"], ["curriculum_domains.slug"],
                                ondelete="CASCADE"),
    )
    # ---- curriculum_lessons ----
    op.create_table(
        "curriculum_lessons",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("module_id", sa.String(36), nullable=False, index=True),
        sa.Column("slug", sa.String(80), nullable=False, index=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("content", sa.Text(), nullable=False, server_default=""),
        sa.Column("order_index", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("estimated_minutes", sa.Integer(), nullable=False, server_default="30"),
        sa.Column("has_visual", sa.Boolean(), nullable=False, server_default="0"),
        sa.ForeignKeyConstraint(["module_id"], ["curriculum_modules.id"],
                                ondelete="CASCADE"),
    )
    # ---- curriculum_questions ----
    op.create_table(
        "curriculum_questions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("domain_slug", sa.String(80), nullable=False, index=True),
        sa.Column("module_slug", sa.String(80), nullable=False, server_default="", index=True),
        sa.Column("lesson_id", sa.String(36), nullable=True, index=True),
        sa.Column("difficulty", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("qtype", sa.String(16), nullable=False, server_default="mcq"),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("choices", sa.Text(), nullable=True),
        sa.Column("answer_index", sa.Integer(), nullable=True),
        sa.Column("explanation", sa.Text(), nullable=False, server_default=""),
        sa.Column("company_tags", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["lesson_id"], ["curriculum_lessons.id"],
                                ondelete="SET NULL"),
    )
    # ---- study_plans ----
    op.create_table(
        "study_plans",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), nullable=False, index=True),
        sa.Column("domain_slug", sa.String(80), nullable=False, index=True),
        sa.Column("start_level", sa.String(16), nullable=False),
        sa.Column("total_days", sa.Integer(), nullable=False),
        sa.Column("current_day", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(16), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )
    # ---- daily_tasks ----
    op.create_table(
        "daily_tasks",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("plan_id", sa.String(36), nullable=False, index=True),
        sa.Column("day_number", sa.Integer(), nullable=False),
        sa.Column("lesson_id", sa.String(36), nullable=True),
        sa.Column("task_type", sa.String(16), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("question_ids", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("status", sa.String(16), nullable=False, server_default="pending"),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["plan_id"], ["study_plans.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["lesson_id"], ["curriculum_lessons.id"],
                                ondelete="SET NULL"),
    )

    # ---- seed domains ----
    for i, (slug, name, icon, desc, cat, order) in enumerate(DOMAINS):
        did = f"seed-curr-dom-{i:04d}".ljust(36, "0")[:36]
        safe_desc = desc.replace("'", "''")
        op.execute(
            "INSERT INTO curriculum_domains (id, slug, name, icon, description, "
            f"category, order_index, is_active) VALUES ('{did}', '{slug}', "
            f"'{name}', '{icon}', '{safe_desc}', '{cat}', {order}, 1)"
        )

    # ---- seed modules ----
    mi = 0
    for slug, _name, _icon, _desc, _cat, _order in DOMAINS:
        for j, (mslug, mname, mdesc, days) in enumerate(MODULES.get(slug, [])):
            mid = f"seed-curr-mod-{mi:04d}".ljust(36, "0")[:36]
            safe_mdesc = mdesc.replace("'", "''")
            safe_mname = mname.replace("'", "''")
            op.execute(
                "INSERT INTO curriculum_modules (id, domain_slug, slug, name, "
                f"description, order_index, estimated_days) VALUES ('{mid}', "
                f"'{slug}', '{mslug}', '{safe_mname}', '{safe_mdesc}', {j}, {days})"
            )
            mi += 1


def downgrade() -> None:
    op.drop_table("daily_tasks")
    op.drop_table("study_plans")
    op.drop_table("curriculum_questions")
    op.drop_table("curriculum_lessons")
    op.drop_table("curriculum_modules")
    op.drop_table("curriculum_domains")
