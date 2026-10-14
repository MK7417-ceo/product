"""Seed content: DBMS — Module 1 (ER Model & Design).

Part-file of the DBMS curriculum seed. Provides MODULES, LESSONS, QUESTIONS
lists using the frozen dataclasses from app.domain.curriculum. All theory is
original and interview-focused.

Expected to be picked up by the curriculum content loader alongside the other
dbms_part_*.py seed files (same MODULES/LESSONS/QUESTIONS shape).
"""

from __future__ import annotations

from app.domain.curriculum import (
    CurriculumLesson,
    CurriculumModule,
    CurriculumQuestion,
    validate_curriculum_question,
)

DOMAIN_SLUG = "dbms"


def _mkq(qid, lesson_id, module_slug, difficulty, prompt, choices, answer_index,
         explanation, company_tags):
    ch = tuple(choices)
    tags = tuple(company_tags)
    validate_curriculum_question("mcq", prompt, difficulty, ch, answer_index)
    return CurriculumQuestion(
        id=qid,
        domain_slug=DOMAIN_SLUG,
        module_slug=module_slug,
        lesson_id=lesson_id,
        difficulty=difficulty,
        qtype="mcq",
        prompt=prompt,
        choices=ch,
        answer_index=answer_index,
        explanation=explanation,
        company_tags=tags,
    )


def _mkl(lesson_id, module_id, slug, title, content, order_index,
         estimated_minutes=35):
    return CurriculumLesson(
        id=lesson_id,
        module_id=module_id,
        slug=slug,
        title=title,
        content=content,
        order_index=order_index,
        estimated_minutes=estimated_minutes,
    )


# ------------------------------------------------------------------ modules

MODULES = [
    CurriculumModule(
        id="dbms-m1",
        domain_slug=DOMAIN_SLUG,
        slug="er-model-design",
        name="ER Model & Design",
        description=(
            "Designing databases before building them: why DBMSs beat plain "
            "files, entities/attributes/relationships, keys, ER diagrams with "
            "cardinality and participation, weak entities and ISA hierarchies, "
            "and the relational model with integrity rules."
        ),
        order_index=1,
        estimated_days=6,
    ),
]

# ------------------------------------------------------------------ lessons

LESSONS = [
    _mkl(
        "dbms-m1-l1", "dbms-m1", "dbms-vs-file-systems", "DBMS vs File Systems",
        """Before DBMSs, applications stored data in plain files managed by the
OS. It worked until data grew: every program kept its own copy of the same
data — a student's record in the admissions file, the hostel file, and the
library file. Update one copy, forget another, and you get data redundancy
leading to inconsistency.

File systems also lack data independence: change the file's format and every
program reading it breaks. Concurrent access is a free-for-all — two programs
writing the same file can interleave and corrupt it. And when the machine
crashes mid-write, there is no recovery story: half-written files are just
broken.

A DBMS fixes all four: it keeps one authoritative copy (redundancy
controlled), insulates programs from storage details (physical data
independence — add an index without rewriting apps; logical independence —
extend the schema without breaking old views), serializes concurrent
transactions (isolation), and guarantees atomicity and durability — a crashed
transaction rolls back, a committed one survives.

Interview framing: "why not just use files?" — answer with the four:
redundancy/inconsistency, independence, concurrency, recovery. And know the
honest cost: DBMS overhead is overkill for a single-user, single-app toy —
there, files win on simplicity.""",
        1,
    ),
    _mkl(
        "dbms-m1-l2", "dbms-m1", "entities-attributes-relationships",
        "Entities, Attributes & Relationships",
        """An entity is a real-world object (a student, a course); an entity set
is all entities of one type. Each entity is described by attributes.

Attribute types — an interview favorite: simple attributes cannot be divided
(age); composite attributes can (name splits into first/last); derived
attributes are computed from others (age from date_of_birth — stored nowhere);
multivalued attributes hold many values (phone_numbers). Key attributes
uniquely identify each entity (roll_no). NULL means unknown or inapplicable —
it is distinct from zero or an empty string.

A relationship set connects entity sets, and its degree is how many entity
sets participate: binary (student enrolls in course — the common case),
ternary (supplier supplies part to project), or n-ary. Relationships can carry
their own descriptive attributes: an enrollment has a grade and a semester,
which belong to neither the student nor the course alone.

Design judgment: ternary relationships are rarer and harder to reason about
than binary ones — most real schemas decompose them. When an interviewer says
"model a university," start with entity sets, mark key attributes, then add
relationships with their degrees before drawing anything.""",
        2,
    ),
    _mkl(
        "dbms-m1-l3", "dbms-m1", "keys", "Keys",
        """Keys identify tuples. A super key is any attribute set that uniquely
identifies a tuple — roll_no alone, but also the (non-minimal) set {roll_no,
name}. A candidate key is a minimal super key: remove any attribute and
uniqueness breaks. roll_no and email might both be candidate keys. The primary
key is the candidate key the designer chooses as the official identifier
(underlined in ER diagrams). Alternate keys are the candidate keys not chosen
— email, if roll_no is primary. A foreign key is an attribute in one table
that references the primary key of another — the glue of relationships.

Example: Student(roll_no PK, name, email unique, dept); Course(course_id PK,
title, credits); Enrollment(student_id FK, course_id FK, semester, grade),
with the composite primary key {student_id, course_id} — one row per
student-course pair.

Interview traps: primary keys can never be NULL and should never change
(entity integrity); a foreign key must match an existing primary key value or
be NULL (referential integrity); and minimality is exactly what separates a
candidate key from a mere super key. If you can drop an attribute and stay
unique, it was never a candidate key.""",
        3,
    ),
    _mkl(
        "dbms-m1-l4", "dbms-m1", "er-diagrams", "ER Diagrams",
        """ER notation: rectangles are entity sets, diamonds are relationship
sets, ovals are attributes (double ovals for multivalued, dashed ovals for
derived), lines connect them, and primary-key attributes are underlined.

Cardinality ratios constrain how many entities may relate: 1:1 (one person,
one passport), 1:N (one department, many students), M:N (students to courses).
Read the ratio from the relationship's perspective and mark it on the diagram.

Participation constrains whether entities must relate at all: total
participation (double line) means every entity participates — every student
must enroll in at least one course; partial participation (single line) means
some may not — a course may have zero students. The classic interview prompt
is "show total participation" — draw the double line.

Putting it together: Student —< Enrolls >— Course, M:N, with grade as a
descriptive attribute on the diamond. Tables fall out of this diagram
mechanically: entity sets become tables, and the M:N relationship becomes its
own table holding both foreign keys plus grade. Learn the mapping, not just
the drawing.""",
        4,
    ),
    _mkl(
        "dbms-m1-l5", "dbms-m1", "weak-entities-specialization",
        "Weak Entities, Specialization & Generalization",
        """A weak entity cannot be identified by its own attributes — it depends
on an owner. Dependent(name) of Employee is the textbook example: two
employees could each have a dependent named "Aarav". A weak entity is
identified by the owner's key plus its own partial key (discriminator):
{employee_id, dependent_name}. The relationship to the owner is the
identifying relationship (double diamond), and the weak entity always has
total participation — a dependent cannot exist without the employee.

Specialization and generalization are two views of one ISA hierarchy:
top-down, Person specializes into Student and Faculty; bottom-up, Student and
Faculty generalize into Person. Attributes and relationships inherit downward.
Two constraints matter: disjoint vs overlapping (can someone be both a student
and faculty?), and total vs partial specialization (must every person be one
of the subtypes?).

Aggregation handles the case where a relationship itself participates in
another relationship: an advisor monitors a student's enrollment — the Enrolls
relationship is treated as a higher-level entity so Monitors can reference it.
Reach for aggregation when the "thing" being related is itself a
relationship, not an entity.""",
        5,
    ),
    _mkl(
        "dbms-m1-l6", "dbms-m1", "relational-model", "Relational Model",
        """The relational model sees data as relations (tables): a relation is
a set of tuples (rows); each tuple has attributes (columns) whose values come
from a domain — the allowed value set, e.g. Grade in {A, B, C, D, F}. Tuples
are never duplicated, attribute values are atomic, and the order of rows and
columns is meaningless.

Schema vs instance: the schema is the structure — Student(roll_no, name,
dept) — and changes rarely; the instance is the actual data right now and
changes constantly. Confusing the two is a classic beginner error.

Two integrity rules hold every database together. Entity integrity: no part of
a primary key may be NULL — otherwise identity breaks. Referential integrity:
every foreign-key value must match an existing primary-key value (or be NULL),
enforced by the DBMS on every insert, update, and delete, with cascade or
restrict policies for deletions.

These two constraints are why relational databases stay consistent while piles
of files do not — and interviewers will ask you to state both verbatim. If
you remember nothing else from this module: keys identify, foreign keys
connect, and the two integrities protect.""",
        6, estimated_minutes=30,
    ),
]

# ---------------------------------------------------------------- questions

QUESTIONS = [
    # ---- dbms-m1-l1 DBMS vs File Systems (difficulties 1-5)
    _mkq("dbms-m1-l1-q1", "dbms-m1-l1", "er-model-design", 1,
         "Which of these is a problem of storing data in plain OS files that a DBMS solves?",
         ["Files cannot store text",
          "Data redundancy and inconsistency across copies",
          "Files are too small for any real data",
          "DBMSs make data impossible to delete"],
         1,
         "With plain files every application keeps its own copy, so updates to "
         "one copy leave the others stale — redundancy breeds inconsistency. A "
         "DBMS stores one authoritative copy that all applications share.",
         ["tcs", "infosys"]),
    _mkq("dbms-m1-l1-q2", "dbms-m1-l1", "er-model-design", 2,
         "Two clerks update the same stock file at the same time and the final count is wrong. What is this problem, and how does a DBMS prevent it?",
         ["It is a hardware fault; a DBMS replaces the disk",
          "It is a lost update from uncontrolled concurrent access; a DBMS serializes transactions to provide isolation",
          "It is a virus; a DBMS includes antivirus",
          "It is unavoidable in any system"],
         1,
         "When two writes interleave without coordination, one update is lost. "
         "The DBMS treats each clerk's work as a transaction and isolates them, "
         "so the final count reflects both updates correctly.",
         ["wipro", "accenture"]),
    _mkq("dbms-m1-l1-q3", "dbms-m1-l1", "er-model-design", 3,
         "What is data independence?",
         ["Data that never changes",
          "Applications keep working even when the physical storage or the logical schema changes",
          "Data stored without any schema",
          "The database running without administrators"],
         1,
         "Physical independence means you can add an index or change file "
         "organization without rewriting apps; logical independence means you "
         "can extend the schema without breaking existing views. Plain files "
         "give you neither — change the format, rewrite every program.",
         ["tcs", "infosys"]),
    _mkq("dbms-m1-l1-q3b", "dbms-m1-l1", "er-model-design", 3,
         "The system crashes halfway through transferring money between two accounts. The DBMS undoes the half-done transfer. Which property is this?",
         ["Atomicity", "Redundancy", "Indexing", "Caching"],
         0,
         "Atomicity means a transaction is all-or-nothing: a crash mid-transfer "
         "rolls everything back, so money is never created or destroyed by a "
         "half-finished operation. Plain files have no such guarantee.",
         ["amazon", "microsoft"]),
    _mkq("dbms-m1-l1-q4", "dbms-m1-l1", "er-model-design", 4,
         "A single-user, single-application address book: plain files or a DBMS? Justify the choice.",
         ["DBMS, because every application needs transactions",
          "Plain files — DBMS overhead (parsing, transaction machinery, background processes) is not worth it with no concurrency or recovery needs",
          "DBMS, because files cannot store names",
          "Plain files, because a DBMS cannot run on a laptop"],
         1,
         "A DBMS earns its cost through shared, concurrent, crash-safe access. "
         "One user and one app have none of those needs, so the simplicity of "
         "files wins. Choosing technology by matching it to actual requirements "
         "is the engineering judgment interviewers want to hear.",
         ["google", "amazon"]),
    _mkq("dbms-m1-l1-q5", "dbms-m1-l1", "er-model-design", 5,
         '"A DBMS eliminates all redundancy." True or false — and why do foreign keys still repeat values across tables?',
         ["True; a proper DBMS stores every value exactly once",
          "False — the DBMS eliminates uncontrolled duplication, but controlled redundancy like foreign keys is the price of representing relationships",
          "True; foreign keys are not really redundant",
          "False; redundancy is the main goal of a DBMS"],
         1,
         "A foreign key repeats the referenced primary-key value in every child "
         "row — deliberate, controlled redundancy that makes joins possible. "
         "What the DBMS kills is the uncontrolled kind: the same fact stored in "
         "three unsynchronized files.",
         ["microsoft", "google"]),

    # ---- dbms-m1-l2 Entities, Attributes & Relationships (difficulties 1-5)
    _mkq("dbms-m1-l2-q1", "dbms-m1-l2", "er-model-design", 1,
         'In Student(roll_no, name, age), what is an "entity"?',
         ["The whole Student table",
          "A single student object — one row of the table",
          "The roll_no column",
          "The database server"],
         1,
         "An entity is one real-world object; the entity set is the collection "
         "of all such objects. One student row = one entity; the table holds "
         "the entity set.",
         ["tcs", "wipro"]),
    _mkq("dbms-m1-l2-q2", "dbms-m1-l2", "er-model-design", 2,
         "If age is computed from date_of_birth instead of being stored, what kind of attribute is age?",
         ["Simple", "Composite", "Derived", "Multivalued"],
         2,
         "A derived attribute is calculated from other stored attributes and is "
         "not stored itself — it can always be recomputed. Storing it anyway "
         "risks it going stale.",
         ["infosys", "accenture"]),
    _mkq("dbms-m1-l2-q3", "dbms-m1-l2", "er-model-design", 3,
         "A student can have several phone numbers stored in phone_numbers. What kind of attribute is this?",
         ["Derived", "Multivalued", "Composite", "Key"],
         1,
         "Multivalued attributes hold a set of values per entity, drawn with a "
         "double oval in ER diagrams. In tables they usually become a separate "
         "relation — one row per phone number.",
         ["tcs", "wipro"]),
    _mkq("dbms-m1-l2-q3b", "dbms-m1-l2", "er-model-design", 3,
         "A relationship set connecting the Student and Course entity sets has what degree?",
         ["Unary", "Binary", "Ternary", "Quaternary"],
         1,
         "Degree counts the participating entity sets: two sets make it "
         "binary — the overwhelmingly common case. Ternary needs three sets, "
         "like supplier–part–project.",
         ["infosys", "tcs"]),
    _mkq("dbms-m1-l2-q4", "dbms-m1-l2", "er-model-design", 4,
         "In Student — Enrolls — Course, where does the attribute 'grade' belong, and why not on Student?",
         ["On Student, because the student earned it",
          "On the Enrolls relationship — it describes the enrollment, not the student, since one student has many grades",
          "On Course, because the course awards it",
          "Nowhere; grades cannot be modeled"],
         1,
         "Descriptive attributes belong to whatever they describe. A grade "
         "describes a specific student taking a specific course — the "
         "relationship instance — not the student alone.",
         ["amazon", "microsoft"]),
    _mkq("dbms-m1-l2-q5", "dbms-m1-l2", "er-model-design", 5,
         "Why are ternary relationships often decomposed into binary ones in real schemas?",
         ["Ternary relationships are forbidden by the relational model",
          "Their cardinality constraints are harder to enforce and query, while binary decomposition with an associative entity maps directly to tables",
          "Binary relationships run faster on all hardware",
          "Ternary relationships cannot have attributes"],
         1,
         "A ternary's constraints are subtle (what does 1:N mean across three "
         "sides?), and SQL joins are binary. Decomposing into an associative "
         "entity plus binary relationships keeps the design checkable and the "
         "queries natural.",
         ["google", "amazon"]),

    # ---- dbms-m1-l3 Keys (difficulties 1-5)
    _mkq("dbms-m1-l3-q1", "dbms-m1-l3", "er-model-design", 1,
         "Which key uniquely identifies each tuple and is chosen as the official identifier of the table?",
         ["Foreign key", "Primary key", "Alternate key", "Super key"],
         1,
         "The primary key is the chosen candidate key — underlined in ER "
         "diagrams, never NULL, never changing. The others are either broader "
         "(super), unchosen (alternate), or referencing (foreign).",
         ["tcs", "infosys"]),
    _mkq("dbms-m1-l3-q2", "dbms-m1-l3", "er-model-design", 2,
         "{roll_no, name} uniquely identifies a student, but {roll_no} alone also does. Is {roll_no, name} a candidate key?",
         ["Yes, because it is unique",
          "No — it is a super key but not minimal; a candidate key must stay unique after removing any attribute",
          "Yes, composite keys are always candidate keys",
          "No, because it has two attributes"],
         1,
         "Minimality is the whole difference: a candidate key is a minimal "
         "super key. Since name can be dropped without losing uniqueness, "
         "{roll_no, name} is merely a super key.",
         ["wipro", "accenture"]),
    _mkq("dbms-m1-l3-q3", "dbms-m1-l3", "er-model-design", 3,
         "In Enrollment(student_id, course_id, grade), student_id references Student(roll_no). What is student_id here?",
         ["A primary key", "A foreign key", "An alternate key", "A derived attribute"],
         1,
         "A foreign key is an attribute that references another table's "
         "primary key — the glue that turns two tables into a relationship. "
         "The DBMS enforces that every value matches a real student.",
         ["tcs", "infosys"]),
    _mkq("dbms-m1-l3-q3b", "dbms-m1-l3", "er-model-design", 3,
         "email is unique for every student, but roll_no was chosen as the primary key. What is email?",
         ["A foreign key", "An alternate key", "A super key only", "Not a key at all"],
         1,
         "email is a candidate key (minimal and unique) that was not chosen — "
         "that is exactly the definition of an alternate key. It typically "
         "still gets a UNIQUE constraint.",
         ["accenture", "wipro"]),
    _mkq("dbms-m1-l3-q4", "dbms-m1-l3", "er-model-design", 4,
         "Can a primary key contain NULL? Why not?",
         ["Yes, NULL is just another value",
          "No — entity integrity forbids it, because NULL means unknown and an unknown value cannot identify a tuple",
          "Yes, but only in the first row",
          "No, because NULL takes too much storage"],
         1,
         "The primary key is how the DBMS (and every foreign key) identifies "
         "the row. An unknown identifier identifies nothing, so entity "
         "integrity bans NULL in any part of a primary key.",
         ["amazon", "microsoft"]),
    _mkq("dbms-m1-l3-q5", "dbms-m1-l3", "er-model-design", 5,
         "Enrollment uses the composite primary key {student_id, course_id}. What real-world rule does this enforce, and what breaks if grade is added to the key?",
         ["It enforces one row per student-course pair; adding grade would allow the same student-course pair to appear multiple times with different grades",
          "It enforces alphabetical ordering; adding grade would break sorting",
          "Nothing changes; keys do not enforce rules",
          "It prevents any grades from being stored"],
         0,
         "The key is the table's uniqueness contract: {student_id, course_id} "
         "says 'one enrollment per pair'. Widen the key with grade and the "
         "contract loosens — duplicates of the pair become legal, one per "
         "grade value.",
         ["google", "microsoft"]),
    # ---- dbms-m1-l4 ER Diagrams (difficulties 1-5)
    _mkq("dbms-m1-l4-q1", "dbms-m1-l4", "er-model-design", 1,
         "In ER notation, a diamond represents...",
         ["An entity set", "An attribute", "A relationship set", "A primary key"],
         2,
         "Rectangles are entity sets, diamonds are relationship sets, ovals are "
         "attributes. The diamond sits between the rectangles it connects.",
         ["tcs", "wipro"]),
    _mkq("dbms-m1-l4-q2", "dbms-m1-l4", "er-model-design", 2,
         "In an ER diagram, a double oval represents...",
         ["A derived attribute", "A multivalued attribute",
          "A primary key", "A weak entity"],
         1,
         "Double oval = multivalued (e.g. phone_numbers); dashed oval = "
         "derived (e.g. age from dob). The doubling visually suggests 'more "
         "than one value'.",
         ["infosys", "accenture"]),
    _mkq("dbms-m1-l4-q3", "dbms-m1-l4", "er-model-design", 3,
         "The relationship Department — has — Student is 1:N. Which side is the N side?",
         ["Department — one student belongs to many departments",
          "Student — one department has many students",
          "Both sides are N",
          "Neither; 1:N is read right to left only"],
         1,
         "1:N is read as 'one department to N students': the entity that can "
         "appear many times per single instance of the other is the N side. "
         "Getting this backwards is the most common ER error.",
         ["tcs", "infosys"]),
    _mkq("dbms-m1-l4-q3b", "dbms-m1-l4", "er-model-design", 3,
         "How is total participation drawn in an ER diagram, and what does it mean?",
         ["Single line; the entity may or may not participate",
          "Double line; every entity in the set must participate in the relationship",
          "Dashed line; participation is derived",
          "Double diamond; the relationship is weak"],
         1,
         "The double line is the visual 'must': every student must enroll in "
         "at least one course. Single line is partial — a course may exist "
         "with zero students.",
         ["wipro", "tcs"]),
    _mkq("dbms-m1-l4-q4", "dbms-m1-l4", "er-model-design", 4,
         "Student — Enrolls — Course is M:N, with grade as a descriptive attribute on the relationship. How many tables does the relational mapping need, and why?",
         ["Two — grade goes on the Student table",
          "Three — Student, Course, and an Enrolls table holding both foreign keys plus grade, because M:N cannot be a foreign key on either side",
          "One — everything fits in a single wide table",
          "Four — M:N always needs two link tables"],
         1,
         "A foreign key on Student could point to only one course, and vice "
         "versa — neither side can hold an M:N. So the relationship becomes "
         "its own table keyed by both foreign keys, and grade rides along as "
         "a regular column.",
         ["amazon", "microsoft"]),
    _mkq("dbms-m1-l4-q5", "dbms-m1-l4", "er-model-design", 5,
         "Person — has — Passport is 1:1. On which side can the foreign key go, and what constraint makes it 1:1 rather than 1:N?",
         ["Only on Person; nothing else is needed",
          "On either side; a UNIQUE constraint on the foreign key",
          "On either side; a NOT NULL constraint on the foreign key",
          "It must go on both sides"],
         1,
         "A plain foreign key gives 1:N (many passports could point at one "
         "person). UNIQUE on that foreign key collapses the 'many' to 'one'. "
         "Either side can host it — the choice is a design convenience.",
         ["google", "amazon"]),

    # ---- dbms-m1-l5 Weak Entities, Specialization & Generalization (difficulties 1-5)
    _mkq("dbms-m1-l5-q1", "dbms-m1-l5", "er-model-design", 1,
         "A weak entity is identified by...",
         ["Its own attributes alone",
          "Its owner's key plus its own partial key (discriminator)",
          "A randomly generated UUID only",
          "The relationship's cardinality"],
         1,
         "Weak means 'cannot stand alone': Dependent needs employee_id from "
         "its owner Employee plus its own partial key (dependent name) to be "
         "unique. Neither part suffices by itself.",
         ["tcs", "infosys"]),
    _mkq("dbms-m1-l5-q2", "dbms-m1-l5", "er-model-design", 2,
         "Dependent of Employee: why is Dependent a weak entity?",
         ["It has too many attributes",
          "Its name alone is not unique across employees — it needs the owner's key to be identified",
          "It has no relationship to Employee",
          "Weak entities cannot have attributes"],
         1,
         "Two employees can each have a dependent named 'Aarav', so name alone "
         "identifies nothing globally. The weak entity borrows identity from "
         "its owner — the defining trait of weakness.",
         ["wipro", "accenture"]),
    _mkq("dbms-m1-l5-q3", "dbms-m1-l5", "er-model-design", 3,
         "What is an identifying relationship, and how is it drawn?",
         ["Any M:N relationship; drawn as a double rectangle",
          "The relationship linking a weak entity to its owner; drawn as a double diamond",
          "A relationship with no attributes; drawn dashed",
          "A self-relationship; drawn as a loop"],
         1,
         "The identifying relationship is what the weak entity hangs its "
         "identity on — double diamond, and the weak entity connects to it "
         "with total participation (double line).",
         ["tcs", "wipro"]),
    _mkq("dbms-m1-l5-q3b", "dbms-m1-l5", "er-model-design", 3,
         "In the ISA hierarchy Student ISA Person, which direction does inheritance flow?",
         ["Upward — Person inherits from Student",
          "Downward — Student inherits Person's attributes and relationships",
          "Both directions equally",
          "Inheritance does not apply to ER hierarchies"],
         1,
         "Specialization flows down: the subtype gets everything the "
         "supertype has, plus its own extras. Student has name (from Person) "
         "plus roll_no (its own).",
         ["infosys", "tcs"]),
    _mkq("dbms-m1-l5-q4", "dbms-m1-l5", "er-model-design", 4,
         'The design must allow a person to be both a student and a faculty member. Which specialization constraint applies?',
         ["Disjoint specialization",
          "Overlapping specialization",
          "Total specialization",
          "Partial specialization"],
         1,
         "Disjoint forbids belonging to two subtypes at once; overlapping "
         "permits it. (Total vs partial is the separate question of whether "
         "every supertype member must belong to some subtype.)",
         ["amazon", "microsoft"]),
    _mkq("dbms-m1-l5-q5", "dbms-m1-l5", "er-model-design", 5,
         "When should you use aggregation instead of a plain ternary relationship?",
         ["When the database has more than three tables",
          "When a relationship itself needs to participate in another relationship — e.g. an advisor monitoring a student's enrollment",
          "When all relationships are 1:1",
          "Aggregation and ternary relationships are identical"],
         1,
         "Aggregation promotes a relationship to a higher-level entity so "
         "another relationship can reference it. A ternary just connects three "
         "entity sets — it cannot express 'a relationship about a "
         "relationship'.",
         ["google", "amazon"]),

    # ---- dbms-m1-l6 Relational Model (difficulties 1-5)
    _mkq("dbms-m1-l6-q1", "dbms-m1-l6", "er-model-design", 1,
         "In the relational model, a tuple is...",
         ["A column", "A row", "A table", "A database"],
         1,
         "Relation = table, tuple = row, attribute = column, domain = allowed "
         "values. The vocabulary is the first thing interviewers check.",
         ["tcs", "infosys"]),
    _mkq("dbms-m1-l6-q2", "dbms-m1-l6", "er-model-design", 2,
         "What is the difference between a schema and an instance?",
         ["They are synonyms",
          "The schema is the structure (table definitions), which changes rarely; the instance is the actual data right now, which changes constantly",
          "The instance is the structure; the schema is the data",
          "Schemas exist only in ER diagrams"],
         1,
         "Student(roll_no, name, dept) is schema — it may live for years. The "
         "10,000 rows in it today are the instance — different tomorrow. "
         "Confusing them is a classic beginner error.",
         ["wipro", "accenture"]),
    _mkq("dbms-m1-l6-q3", "dbms-m1-l6", "er-model-design", 3,
         "The domain of Grade is {A, B, C, D, F}. What does a domain restrict?",
         ["The number of rows in the table",
          "The allowed values for that attribute",
          "Which users can see the column",
          "The primary key of the table"],
         1,
         "A domain is the value set an attribute draws from — the type-level "
         "contract. 'Z' as a grade violates the domain before any other "
         "constraint is even checked.",
         ["tcs", "infosys"]),
    _mkq("dbms-m1-l6-q3b", "dbms-m1-l6", "er-model-design", 3,
         "Entity integrity states that...",
         ["Every table must have at least one row",
          "No part of a primary key may be NULL",
          "Foreign keys must always be NULL",
          "Every attribute must be a key"],
         1,
         "The primary key is the row's identity; NULL means unknown, and an "
         "unknown value cannot identify anything. So the DBMS rejects NULL in "
         "any primary-key column, always.",
         ["accenture", "wipro"]),
    _mkq("dbms-m1-l6-q4", "dbms-m1-l6", "er-model-design", 4,
         "A new Enrollment row has student_id = 999, but no student with roll_no 999 exists. What happens?",
         ["The DBMS accepts it and creates the student automatically",
          "The DBMS rejects the insert — it violates referential integrity",
          "The row is stored with a warning",
          "Referential integrity only applies to deletes"],
         1,
         "Referential integrity demands every foreign-key value match a real "
         "primary key (or be NULL). Dangling references are rejected on "
         "insert and update — the DBMS guards the relationship, not just the "
         "tables.",
         ["amazon", "microsoft"]),
    _mkq("dbms-m1-l6-q5", "dbms-m1-l6", "er-model-design", 5,
         "A foreign key from Student to Department is defined ON DELETE CASCADE. The 'Physics' department row is deleted. What happens to its students, and when is CASCADE dangerous?",
         ["Nothing happens to the students; CASCADE only affects the parent",
          "The Physics students' rows are deleted too; CASCADE is dangerous when the child rows are valuable independent data — deleting a department wipes student records, so RESTRICT or SET NULL is usually safer",
          "The students move to a random department",
          "CASCADE is never dangerous"],
         1,
         "CASCADE propagates the delete down the foreign key — powerful and "
         "destructive. It fits expendable children (order lines when the order "
         "is deleted), not entities with independent meaning like students. "
         "Choosing the delete policy is a real design decision.",
         ["google", "microsoft"]),
]
