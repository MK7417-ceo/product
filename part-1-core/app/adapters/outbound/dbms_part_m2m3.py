"""Seed content: DBMS — Modules 2-3 (SQL, Normalization)."""

from __future__ import annotations

from app.domain.curriculum import (
    CurriculumLesson,
    CurriculumModule,
    CurriculumQuestion,
    validate_curriculum_question,
)

DOMAIN_SLUG = "dbms"

MODULES = [
    CurriculumModule(
        id="dbms-m2",
        domain_slug=DOMAIN_SLUG,
        slug="sql",
        name="SQL",
        description=(
            "Retrieve and manipulate data with SQL — SELECT, filtering, joins, "
            "subqueries, set operations, DDL/DML, transactions, and window "
            "functions — all on one consistent Employees/Departments schema."
        ),
        order_index=2,
        estimated_days=12,
    ),
    CurriculumModule(
        id="dbms-m3",
        domain_slug=DOMAIN_SLUG,
        slug="normalization",
        name="Normalization",
        description=(
            "Eliminate redundancy the principled way — data anomalies, functional "
            "dependencies, 1NF through BCNF, 4NF/5NF, and when to denormalize "
            "on purpose."
        ),
        order_index=3,
        estimated_days=8,
    ),
]


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


LESSONS = [
    # ------------------------------------------------------------------
    # MODULE 2 — SQL
    # ------------------------------------------------------------------
    CurriculumLesson(
        id="dbms-m2-l1", module_id="dbms-m2", slug="select-where",
        title="SELECT & WHERE", order_index=1, estimated_minutes=25,
        content="""## Reading data: SELECT and WHERE

Every SQL journey starts with two clauses. **SELECT** chooses *which columns*
(projection); **WHERE** chooses *which rows* (selection). We will use one
schema everywhere in this module:

```sql
Employees(emp_id PK, name, dept_id FK, salary, hire_date)
Departments(dept_id PK, dept_name, location)
```

Sample data (keep it in mind — questions use it):

| emp_id | name  | dept_id | salary | hire_date  |
|--------|-------|---------|--------|------------|
| 101    | Aarav | 1       | 90000  | 2021-03-15 |
| 102    | Diya  | 2       | 60000  | 2022-07-01 |
| 103    | Kabir | 1       | 120000 | 2020-01-10 |
| 104    | Mira  | 3       | 55000  | 2023-05-20 |
| 105    | Arjun | 2       | NULL   | 2024-01-05 |
| 106    | Zara  | NULL    | 70000  | 2022-11-11 |

```sql
SELECT name, salary FROM Employees;          -- projection: 2 columns, 6 rows
SELECT * FROM Employees WHERE salary > 80000; -- Aarav, Kabir
```

## Filtering

- **Comparison:** `=`, `<>` (or `!=`), `<`, `>`, `<=`, `>=`
- **Logical:** `AND`, `OR`, `NOT` — `AND` binds tighter than `OR`, so use
  parentheses: `WHERE dept_id = 1 AND (salary > 50000 OR hire_date > '2023-01-01')`
- **Ranges:** `WHERE salary BETWEEN 50000 AND 70000` (inclusive on both ends)
- **Lists:** `WHERE dept_id IN (1, 3)`
- **Patterns:** `WHERE name LIKE 'A%'` — `%` matches any run of characters,
  `_` matches exactly one character. So `'A%'` = starts with A, `'%a'` = ends
  with a, `'_iya'` = 4 letters ending in iya.

## The NULL trap

`NULL` means *unknown*, not zero and not empty string. Any comparison with
`NULL` — even `NULL = NULL` — evaluates to **unknown**, and `WHERE` keeps
only rows that are **true**. So `WHERE salary = NULL` returns **zero rows,
always**. Use the special predicates instead:

```sql
SELECT name FROM Employees WHERE salary IS NULL;      -- Arjun
SELECT name FROM Employees WHERE dept_id IS NOT NULL; -- everyone but Zara
```

This single rule explains half of all SQL interview traps.
""",
    ),
    CurriculumLesson(
        id="dbms-m2-l2", module_id="dbms-m2", slug="order-by-aggregates",
        title="ORDER BY, DISTINCT & Aggregates", order_index=2,
        estimated_minutes=25,
        content="""## Ordering, deduplication, and summarising

Raw rows are rarely the answer — you sort them, collapse duplicates, or boil
them down to a number. Same Employees/Departments schema as lesson 1.

```sql
SELECT name, salary FROM Employees ORDER BY salary DESC; -- highest first
SELECT name FROM Employees ORDER BY hire_date ASC, name; -- oldest hire, ties by name
SELECT DISTINCT dept_id FROM Employees;                  -- 1, 2, 3, NULL (4 rows)
```

`DISTINCT` removes duplicate *combinations* — it treats all NULLs as one
value, so `dept_id` yields 4 distinct values including NULL.

## Aggregate functions

`COUNT`, `SUM`, `AVG`, `MIN`, `MAX` collapse many rows into one value. The
critical rule: **aggregates ignore NULLs** (except `COUNT(*)`).

```sql
SELECT COUNT(*) FROM Employees;        -- 6 (counts rows)
SELECT COUNT(salary) FROM Employees;   -- 5 (Arjun's NULL skipped)
SELECT AVG(salary) FROM Employees;     -- 79000, not 65833:
                                       -- (90000+60000+120000+55000+70000)/5
SELECT MIN(hire_date) FROM Employees;  -- 2020-01-10 (Kabir)
```

Notice the `AVG` trap: dividing by 6 would give 65833, but NULLs are skipped
so the denominator is 5. `COUNT(DISTINCT dept_id)` goes further — it also
skips NULL, returning **3**, unlike `SELECT DISTINCT` which returns 4 rows.

```sql
SELECT COUNT(DISTINCT dept_id) FROM Employees; -- 3 (NULL ignored)
```

Rule of thumb: `COUNT(*)` counts rows, `COUNT(column)` counts non-NULL
values, and `DISTINCT` inside an aggregate deduplicates before counting.
""",
    ),
    CurriculumLesson(
        id="dbms-m2-l3", module_id="dbms-m2", slug="group-by-having",
        title="GROUP BY & HAVING", order_index=3, estimated_minutes=30,
        content="""## Summarising per group

`GROUP BY` splits rows into buckets that share a value, then runs aggregates
*inside each bucket*. Rows whose grouping column is NULL form their own
bucket.

```sql
SELECT dept_id, AVG(salary) AS avg_sal, COUNT(*) AS n
FROM Employees
GROUP BY dept_id;
```

On our data this yields 4 groups: dept 1 → avg 105000 (2 people), dept 2 →
avg 60000 (2 people, Arjun's NULL salary skipped), dept 3 → avg 55000
(1 person), NULL → avg 70000 (Zara alone).

## WHERE vs HAVING — the most-asked distinction

They filter at different stages of the pipeline:

```sql
SELECT dept_id, AVG(salary) AS avg_sal
FROM Employees
WHERE hire_date >= '2021-01-01'   -- 1) filter ROWS first (Kabir's 2020 row gone)
GROUP BY dept_id                  -- 2) then group what remains
HAVING AVG(salary) > 70000;       -- 3) then filter GROUPS (only dept 1 survives)
```

- **WHERE** filters individual rows *before* grouping. It cannot use
  aggregates (`WHERE AVG(salary) > 70000` is illegal).
- **HAVING** filters groups *after* grouping. It exists precisely because
  `WHERE` cannot see aggregates.

Execution order to memorise: `FROM → WHERE → GROUP BY → HAVING → SELECT →
ORDER BY`. That order explains why `HAVING COUNT(*) >= 2` keeps only depts
1 and 2 (each has 2 employees), and why adding `WHERE salary > 55000`
makes dept 3 vanish entirely — Mira's 55000 is not *greater than* 55000,
so her group ends up empty and disappears.
""",
    ),
    CurriculumLesson(
        id="dbms-m2-l4", module_id="dbms-m2", slug="inner-join",
        title="INNER JOIN", order_index=4, estimated_minutes=30,
        content="""## Combining tables: INNER JOIN

Real databases split facts across tables — `Employees` holds people,
`Departments` holds departments, linked by `dept_id`. A **join** reunites
them by matching the foreign key to the primary key. An **INNER JOIN**
keeps only rows that match on *both* sides.

```sql
SELECT e.name, d.dept_name
FROM Employees e JOIN Departments d
  ON e.dept_id = d.dept_id;
```

Trace it: Aarav(1), Diya(2), Kabir(1), Mira(3), Arjun(2) all find their
department — Zara's NULL `dept_id` matches nothing, so she is **dropped**.
Result: 5 rows. The `e` and `d` are table aliases that keep the query short.

## Two syntaxes, one meaning

```sql
-- modern, explicit
SELECT e.name, d.dept_name FROM Employees e
JOIN Departments d ON e.dept_id = d.dept_id;

-- old comma style (same result — an inner join)
SELECT e.name, d.dept_name FROM Employees e, Departments d
WHERE e.dept_id = d.dept_id;
```

Both are inner joins. The `ON` style is preferred: the join condition stays
with the join instead of hiding among filters in `WHERE`.

## Chaining joins

Joins compose — each join adds one more table, and an n-table join needs
n-1 join conditions:

```sql
SELECT e.name, d.dept_name, d.location
FROM Employees e
JOIN Departments d ON e.dept_id = d.dept_id
WHERE d.location = 'Bengaluru';   -- Aarav, Kabir (dept 1 is in Bengaluru)
```

**Deadly beginner mistake:** omitting the `ON` clause. `FROM Employees,
Departments` with no condition produces the **cartesian product** — every
employee paired with every department: 6 x 4 = **24 rows** of nonsense.
If a join returns suspiciously many rows, check the `ON` first.
""",
    ),
    CurriculumLesson(
        id="dbms-m2-l5", module_id="dbms-m2", slug="outer-joins",
        title="OUTER JOINs", order_index=5, estimated_minutes=30,
        content="""## Keeping the unmatched rows: OUTER JOINs

INNER JOIN silently drops unmatched rows — Zara (no department) vanishes,
and so would any department with no employees. OUTER JOINs keep one side's
unmatched rows, filling the missing side with NULLs.

```sql
-- all departments, even those with no employees
SELECT d.dept_name, e.name
FROM Departments d LEFT JOIN Employees e
  ON d.dept_id = e.dept_id;
```

Result (6 rows): Engineering->Aarav, Engineering->Kabir, Sales->Diya,
Sales->Arjun, HR->Mira, **Support->NULL**. Support has no employees, but
LEFT JOIN keeps the department row and puts NULL where the employee would
be. Those NULLs are the signature of an outer join — they mark "no match".

## LEFT, RIGHT, FULL

- **LEFT JOIN** — keep every row of the *left* (first) table.
- **RIGHT JOIN** — keep every row of the *right* (second) table.
  (`A RIGHT JOIN B` = `B LEFT JOIN A` — same result, flipped reading order.)
- **FULL OUTER JOIN** — keep unmatched rows from *both* sides.

```sql
SELECT d.dept_name, e.name
FROM Departments d FULL OUTER JOIN Employees e
  ON d.dept_id = e.dept_id;   -- 7 rows: 5 matches + Support/NULL + NULL/Zara
```

Count: 5 matched pairs, plus Support with NULL employee, plus Zara with
NULL department = 7 rows.

## The classic reporting query

"Headcount per department, including empty departments" needs LEFT JOIN,
because INNER JOIN would hide Support:

```sql
SELECT d.dept_name, COUNT(e.emp_id) AS headcount
FROM Departments d LEFT JOIN Employees e ON d.dept_id = e.dept_id
GROUP BY d.dept_name;
-- Support -> 0. COUNT(e.emp_id) counts non-NULL ids, so the NULL row scores 0.
```

Note `COUNT(e.emp_id)` vs `COUNT(*)`: with `COUNT(*)` Support would show 1
(the NULL row still exists). Counting the nullable side's key gives the
honest 0.
""",
    ),
    CurriculumLesson(
        id="dbms-m2-l6", module_id="dbms-m2", slug="subqueries",
        title="Subqueries", order_index=6, estimated_minutes=30,
        content="""## Queries inside queries

A **subquery** is a SELECT nested inside another query. The outer query
cannot compute some value itself, so it asks an inner query first.

```sql
-- employees earning above the company average (avg = 79000)
SELECT name FROM Employees
WHERE salary > (SELECT AVG(salary) FROM Employees);
-- Aarav (90000), Kabir (120000). Arjun's NULL is not > anything.
```

## Three shapes

- **Scalar** — returns one value, used with `=`, `>`, etc. (the AVG above).
- **Row/table** — returns many rows, used with `IN`:
  ```sql
  SELECT name FROM Employees
  WHERE dept_id IN (SELECT dept_id FROM Departments WHERE location = 'Bengaluru');
  -- dept 1 and 4 are in Bengaluru -> Aarav, Kabir (Arjun/Mira/Diya out; Zara's NULL out)
  ```
- **Correlated** — the inner query references the *outer* row, so it
  re-runs per row. "Employees earning above *their own department's*
  average":

  ```sql
  SELECT name FROM Employees e
  WHERE salary > (SELECT AVG(salary) FROM Employees
                  WHERE dept_id = e.dept_id);
  ```

  Trace dept 1: avg = 105000. Aarav 90000 — no. Kabir 120000 — **yes**.
  Dept 2: avg = 60000; Diya 60000 not > 60000 — no; Arjun NULL — no. Dept 3:
  Mira 55000 not > 55000 — no. Zara: inner WHERE `dept_id = NULL` is
  unknown, avg of nothing is NULL — no. **Answer: Kabir only.**

## IN vs EXISTS, and the NOT IN trap

`EXISTS` checks "does at least one matching row exist" and stops at the
first hit — often faster than `IN` on big tables. But memorise the trap:

```sql
SELECT name FROM Employees WHERE dept_id NOT IN (1, 2, NULL); -- 0 rows!
```

For every row, the test becomes `dept_id <> 1 AND dept_id <> 2 AND
dept_id <> NULL`. The last piece is always unknown, AND with unknown is
never true — so **zero rows**, even for Mira (dept 3). A single NULL in a
`NOT IN` list poisons the whole query. Prefer `NOT EXISTS` when NULLs are
possible.
""",
    ),
    CurriculumLesson(
        id="dbms-m2-l7", module_id="dbms-m2", slug="set-operations",
        title="Set Operations", order_index=7, estimated_minutes=20,
        content="""## Combining result sets: UNION, INTERSECT, EXCEPT

Joins combine tables *sideways* (more columns). Set operations combine
query results *vertically* (more rows). Both SELECTs must return the same
number of columns with compatible types.

```sql
SELECT dept_id FROM Employees
UNION
SELECT dept_id FROM Departments;
```

## UNION vs UNION ALL

- **UNION** — combines and **removes duplicates** (it sorts/dedups).
- **UNION ALL** — combines and **keeps duplicates** (faster — no dedup step).

Trace on our data. Employee dept_ids: 1, 2, 1, 3, 2, NULL. Department ids:
1, 2, 3, 4. UNION -> {1, 2, 3, 4, NULL} = **5 rows**. UNION ALL would give
6 + 4 = **10 rows** (dupes kept). Interviewers love asking which to use:
UNION ALL when you know there are no duplicates or you want them — it
avoids the expensive sort.

## INTERSECT and EXCEPT

- **INTERSECT** — rows present in *both*: {1,2,3} n {1,2,3,4} = **3 rows**.
- **EXCEPT** (MINUS in Oracle) — rows in the first but not the second:
  {1, 2, 3, NULL} minus {1, 2, 3, 4} = **{NULL}**, 1 row. For duplicate
  elimination NULL counts as equal to NULL, and since no department has a
  NULL id, the NULL survives.

```sql
-- departments that have no employees
SELECT dept_id FROM Departments
EXCEPT
SELECT dept_id FROM Employees;   -- 4 (Support)
```

That last query is the set-operation answer to "find unmatched rows" —
the same question LEFT JOIN + IS NULL answers. Two tools, same result;
pick whichever reads clearer.
""",
    ),
    CurriculumLesson(
        id="dbms-m2-l8", module_id="dbms-m2", slug="ddl-constraints",
        title="DDL & Constraints", order_index=8, estimated_minutes=25,
        content="""## Defining the schema: DDL

**DDL** (Data Definition Language) shapes the database itself: `CREATE`
makes objects, `ALTER` changes them, `DROP` deletes them.

```sql
CREATE TABLE Departments (
  dept_id   INT PRIMARY KEY,
  dept_name VARCHAR(50) NOT NULL UNIQUE,
  location  VARCHAR(50) DEFAULT 'Bengaluru'
);

CREATE TABLE Employees (
  emp_id    INT PRIMARY KEY,
  name      VARCHAR(50) NOT NULL,
  dept_id   INT,
  salary    INT CHECK (salary > 0),
  hire_date DATE,
  FOREIGN KEY (dept_id) REFERENCES Departments(dept_id)
);

ALTER TABLE Employees ADD email VARCHAR(100);  -- new column, NULL for old rows
DROP TABLE Employees;                          -- table AND its data are gone
```

## Constraints: rules the database enforces

- **PRIMARY KEY** — unique + NOT NULL, one per table (`emp_id`).
- **FOREIGN KEY ... REFERENCES** — `dept_id` must match a real
  `Departments.dept_id` (or be NULL). Inserting `dept_id = 99` with no
  department 99 is **rejected** — this is referential integrity.
- **UNIQUE** — no duplicates, but unlike PK it allows one NULL and you can
  have several per table.
- **NOT NULL** — the column must always have a value.
- **CHECK** — a per-row rule: `CHECK (salary > 0)` rejects -100.
- **DEFAULT** — value used when INSERT omits the column.

Constraints push validation *into the database*, so bad data is impossible
no matter how buggy the application is. That is why interviewers ask
"UNIQUE vs PRIMARY KEY": one table gets a single PK with no NULLs, but
many UNIQUE columns each tolerating one NULL.
""",
    ),
    CurriculumLesson(
        id="dbms-m2-l9", module_id="dbms-m2", slug="dml-tcl-dcl",
        title="DML, TCL & DCL", order_index=9, estimated_minutes=25,
        content="""## Changing data and controlling access

**DML** (Data Manipulation Language) changes rows: `INSERT`, `UPDATE`,
`DELETE`.

```sql
INSERT INTO Departments VALUES (4, 'Support', 'Bengaluru');
UPDATE Employees SET salary = 95000 WHERE emp_id = 101;  -- never forget WHERE!
DELETE FROM Employees WHERE emp_id = 105;
```

A missing `WHERE` on UPDATE/DELETE hits *every* row — the most expensive
typo in SQL.

## TCL: transactions

**TCL** (Transaction Control Language) groups DML into atomic units:

```sql
BEGIN;
UPDATE Employees SET salary = salary * 1.1 WHERE dept_id = 1;
SAVEPOINT before_bonus;
UPDATE Employees SET salary = salary + 5000 WHERE emp_id = 103;
ROLLBACK TO before_bonus;  -- undo only the second update
COMMIT;                    -- make the 10% raise permanent
```

- **COMMIT** — persist everything since BEGIN.
- **ROLLBACK** — discard everything since BEGIN (or since a SAVEPOINT).
- **SAVEPOINT** — a named checkpoint for *partial* rollback.

## DCL: permissions

```sql
GRANT SELECT ON Employees TO analyst;   -- give read access
REVOKE SELECT ON Employees FROM analyst; -- take it back
```

## DELETE vs TRUNCATE vs DROP — the favourite trap

| | Removes | Keeps table? | Rollback? | WHERE? |
|---|---|---|---|---|
| DELETE (no WHERE) | all rows | yes | yes (in txn) | optional |
| TRUNCATE | all rows | yes | usually no (DDL) | no |
| DROP | table + data | **no** | no (DDL) | no |

DELETE is DML — slow row-by-row, but transactional and selective.
TRUNCATE is DDL — instant deallocation, no WHERE, and in MySQL/Oracle it
auto-commits so you cannot roll it back. DROP goes further and deletes the
table definition itself.
""",
    ),
    CurriculumLesson(
        id="dbms-m2-l10", module_id="dbms-m2", slug="window-functions",
        title="Window Functions", order_index=10, estimated_minutes=30,
        content="""## Calculations across rows without collapsing them

Aggregates squash rows; **window functions** compute across a *window* of
rows while keeping every row in the output. The magic keyword is `OVER()`.

```sql
SELECT name, salary,
       AVG(salary) OVER () AS company_avg   -- 79000 on EVERY row
FROM Employees;
```

Six rows in, six rows out — each row just gains a new column.

## PARTITION BY: per-group windows

```sql
SELECT name, dept_id, salary,
       AVG(salary) OVER (PARTITION BY dept_id) AS dept_avg
FROM Employees;
-- Aarav/Kabir see 105000; Diya/Arjun see 60000; Mira 55000; Zara 70000
```

`PARTITION BY` restarts the calculation for each group — like GROUP BY,
but without collapsing.

## Ranking: ROW_NUMBER vs RANK vs DENSE_RANK

The tie-handling trio. Take salaries [120000, 90000, 90000, 60000]:

| salary | ROW_NUMBER | RANK | DENSE_RANK |
|--------|-----------|------|------------|
| 120000 | 1 | 1 | 1 |
| 90000  | 2 | 2 | 2 |
| 90000  | 3 | 2 | 2 |
| 60000  | 4 | 4 | 3 |

- **ROW_NUMBER** — 1,2,3,4 always; ties get arbitrary distinct numbers.
- **RANK** — ties share a rank, then the next rank **skips** (1,2,2,4).
- **DENSE_RANK** — ties share, next rank does **not** skip (1,2,2,3).

"Top 3 salaries including ties" needs DENSE_RANK <= 3; RANK would wrongly
skip.

## LEAD / LAG: peeking at neighbours

```sql
SELECT name, hire_date, salary,
       LAG(salary) OVER (ORDER BY hire_date) AS prev_salary
FROM Employees;
-- Kabir (earliest hire) -> prev_salary NULL: no previous row exists
-- Aarav -> 120000 (Kabir's salary), Diya -> 90000, ...
```

`LAG` reads the previous row's value, `LEAD` the next row's — the standard
way to compute differences ("salary hike vs previous hire") in one pass.
""",
    ),
    # ------------------------------------------------------------------
    # MODULE 3 — NORMALIZATION
    # ------------------------------------------------------------------
    CurriculumLesson(
        id="dbms-m3-l1", module_id="dbms-m3", slug="data-anomalies",
        title="Data Anomalies", order_index=1, estimated_minutes=25,
        content="""## Why normalization exists: anomalies

Normalization is not academic fussiness — it fixes three concrete bugs
that appear when one table stores facts about *several different things*.
Study this unnormalized table:

| student_id | student_name | course_id | course_name | instructor | instructor_office |
|------------|--------------|-----------|-------------|------------|-------------------|
| S1 | Aarav | C101 | DBMS | Dr Rao | R-201 |
| S1 | Aarav | C102 | OS   | Dr Sen | R-105 |
| S2 | Diya  | C101 | DBMS | Dr Rao | R-201 |

It mixes student facts, course facts, and instructor facts. That causes:

## The three anomalies

**1. Insertion anomaly — cannot store a fact alone.** A new instructor,
Dr Iyer, joins to teach a new course 'AI', but no student has enrolled
yet. There is nowhere to record (AI, Dr Iyer, R-310) without inventing a
fake student — the table's key demands a student_id.

**2. Update anomaly — one fact lives in many rows.** Dr Rao moves from
R-201 to R-205. Her office appears in 2 rows (and could be 200). Update
only one and the database contradicts itself: two offices for one person.
Redundancy *is* the update anomaly waiting to happen.

**3. Deletion anomaly — deleting a fact destroys unrelated facts.** Diya
drops OS (her only course). Deleting her row also deletes the only record
that Dr Sen's office is R-105. One deletion, two facts lost.

## The pattern

Every anomaly here comes from **redundancy**: `instructor_office` repeats
per enrollment instead of being stored once per instructor. Normalization
is the systematic process of splitting such tables until each fact is
stored exactly once — which is what lessons 3-6 do, one normal form at a
time.
""",
    ),
    CurriculumLesson(
        id="dbms-m3-l2", module_id="dbms-m3", slug="functional-dependencies",
        title="Functional Dependencies", order_index=2, estimated_minutes=30,
        content="""## The machinery behind normal forms: FDs

A **functional dependency** `X -> Y` means: *whenever two rows agree on X,
they must agree on Y*. X **determines** Y. In the enrollment table:
`student_id -> student_name` (one id, one name, always) and
`instructor -> instructor_office`. But `course_id -> instructor` does NOT
hold if two instructors can teach the same course.

## Armstrong's axioms — deriving new FDs

From known FDs you can infer more, using three rules:

- **Reflexivity:** if Y is a subset of X, then X -> Y. Trivial but needed:
  `{student_id, course_id} -> {student_id}`.
- **Augmentation:** if X -> Y then XZ -> YZ for any Z. Add the same
  attributes to both sides: `instructor -> instructor_office` gives
  `{instructor, course_id} -> {instructor_office, course_id}`.
- **Transitivity:** if X -> Y and Y -> Z then X -> Z. The workhorse:
  `emp_id -> dept_id` and `dept_id -> dept_name` yield
  `emp_id -> dept_name`.

## Attribute closure X+ — the key-finding algorithm

The **closure** of X is everything X determines, computed iteratively:
start with X, repeatedly add the right side of any FD whose left side is
already inside, until nothing new appears.

Worked example. R(A, B, C, D, E), FDs = {A->B, B->C, CD->E}. Find A+:

1. Start: {A}
2. A->B fires: {A, B}
3. B->C fires: {A, B, C}
4. CD->E? C is in, D is not — cannot fire. Done.

**A+ = {A, B, C}.** Since it is not all attributes, A is not a key. Try
(ACD)+: {A,C,D} -> A->B fires -> {A,B,C,D} -> CD->E fires -> **{A,B,C,D,E}**:
ACD determines everything, so **ACD is a candidate key** (and minimal —
drop any letter and it fails). Closure turns key-finding into arithmetic.
""",
    ),
    CurriculumLesson(
        id="dbms-m3-l3", module_id="dbms-m3", slug="1nf",
        title="1NF", order_index=3, estimated_minutes=20,
        content="""## First Normal Form: atomic values only

**1NF** has one demand: every cell holds a single, **atomic** (indivisible)
value. No lists, no comma-separated bundles, no repeating groups.

## The violation

```sql
-- NOT 1NF: items is a packed list
Orders(order_id, customer, items)
--  (501, 'Aarav', 'laptop, mouse, keyboard')
```

'items' is not atomic — you cannot index it, join on it, or count 'how
many mice were ordered' without string surgery. Same disease:

```sql
Students(student_id, name, phone_numbers)   -- '98xx, 97xx' in one cell
Marks(student_id, course1, course2, course3) -- repeating group as columns
```

The `course1, course2, course3` pattern is the sneakiest: what happens when
a student takes a 4th course? ALTER TABLE every semester. Columns must not
multiply to simulate rows.

## The fix

Give each value its own row (or its own table):

```sql
-- 1NF: one row per item
OrderItems(order_id, item)
--  (501, 'laptop'), (501, 'mouse'), (501, 'keyboard')

StudentPhones(student_id, phone)  -- one row per phone number
```

Now 'how many items in order 501?' is `COUNT(*)`, and a 4th course is just
another row — no schema change. 1NF is the foundation: every higher normal
form *assumes* 1NF and adds one more restriction on top.
""",
    ),
    CurriculumLesson(
        id="dbms-m3-l4", module_id="dbms-m3", slug="2nf",
        title="2NF", order_index=4, estimated_minutes=25,
        content="""## Second Normal Form: no partial dependencies

**2NF** = in 1NF **and** no non-key attribute depends on *part* of a
composite key. A **partial dependency** is when a proper subset of the key
already determines some column.

Worked example. Registration table, key = (student_id, course_id):

| student_id | course_id | grade | student_name | course_name |
|------------|-----------|-------|--------------|-------------|
| S1 | C101 | A | Aarav | DBMS |
| S1 | C102 | B | Aarav | OS   |

FDs: `student_id -> student_name` (partial! only part of the key),
`course_id -> course_name` (partial!), `(student_id, course_id) -> grade`
(full — needs the whole key).

The symptom is familiar: 'Aarav' repeats per course (update anomaly), and
a new course 'AI' cannot be stored without a student (insertion anomaly).

## Decomposition

Split so each fact lives with the key that determines it:

```sql
Students(student_id PK, student_name)      -- student_id -> student_name
Courses(course_id PK, course_name)         -- course_id -> course_name
Grades(student_id FK, course_id FK, grade) -- (student_id, course_id) -> grade
```

Every FD now lives inside one table, keyed correctly — nothing is lost
(the original is recoverable by join) and nothing repeats.

## The shortcut

Partial dependency needs a **composite key** to exist. If the primary key
is a single attribute, partial dependencies are impossible — the table is
automatically in 2NF (given 1NF). Interview fast-check: "single-column
key -> skip 2NF worries, look for transitive dependencies (3NF) instead."
""",
    ),
    CurriculumLesson(
        id="dbms-m3-l5", module_id="dbms-m3", slug="3nf",
        title="3NF", order_index=5, estimated_minutes=25,
        content="""## Third Normal Form: no transitive dependencies

**3NF** = in 2NF **and** no non-key attribute depends *transitively* on the
key — i.e. no chain `key -> X -> Y` where Y is non-key and X is not a
superkey.

Worked example. Employee table, key = emp_id:

| emp_id | dept_id | dept_name   |
|--------|---------|-------------|
| 101    | 1       | Engineering |
| 103    | 1       | Engineering |

FDs: `emp_id -> dept_id`, `dept_id -> dept_name`. By transitivity,
`emp_id -> dept_name` — but it goes *through* dept_id. That middle hop is
the violation: `dept_name` depends on the key only indirectly.

Consequence: 'Engineering' repeats per employee (update anomaly — rename
the department, update N rows), and a new department cannot be stored
without an employee (insertion anomaly). Same diseases as lesson 1, now
with a precise diagnosis.

## Decomposition

```sql
Employees(emp_id PK, dept_id FK)      -- emp_id -> dept_id
Departments(dept_id PK, dept_name)    -- dept_id -> dept_name
```

Each FD is enforced in exactly one table; the original is recovered with
a join on dept_id. Notice this is the exact Employees/Departments schema
from the SQL module — normalization is *why* that schema looks the way it
does.

## 3NF vs 2NF, one line each

- **2NF** kills dependencies on *part* of the key (needs composite keys).
- **3NF** kills dependencies *through* a non-key middleman (the transitive
  chain key -> X -> Y).
""",
    ),
    CurriculumLesson(
        id="dbms-m3-l6", module_id="dbms-m3", slug="bcnf",
        title="BCNF", order_index=6, estimated_minutes=30,
        content="""## Boyce-Codd Normal Form: every determinant is a superkey

**BCNF** is stricter than 3NF: for *every* FD `X -> Y`, X must be a
**superkey** (a set of attributes that uniquely identifies rows). 3NF lets
a non-superkey determine a *prime* attribute (one belonging to some
candidate key); BCNF allows no exceptions.

## The classic 3NF-but-not-BCNF example

Teaching assignments: each instructor teaches exactly one course, but a
course can have many instructors. Table Takes(student, course, instructor):

FDs: `(student, course) -> instructor`, and `instructor -> course`.

Candidate keys: (student, course) *and* (student, instructor) — check:
(student, instructor)+ = {student, instructor} -> course via instructor ->
course, so it determines all three. **Every attribute is prime** (each
belongs to some key), so 3NF is trivially satisfied.

But `instructor -> course` violates BCNF: instructor is a determinant yet
not a superkey (one instructor, many students — instructor alone does not
identify a row).

## The anomaly survives 3NF

Each instructor's course repeats per student (update anomaly), and a new
instructor's course cannot be recorded until they get a student (insertion
anomaly). 3NF did not save us — BCNF exists for exactly this gap.

## Decomposition

```sql
Teaching(instructor PK, course)       -- instructor -> course
Enrollment(student, instructor)       -- join key back via instructor
```

Lossless (instructor is a key of Teaching, so the join reconstructs the
original exactly) and both FDs are preserved. Rule of thumb: every BCNF
table is in 3NF, but as this example proves, the converse is false.
""",
    ),
    CurriculumLesson(
        id="dbms-m3-l7", module_id="dbms-m3", slug="4nf-5nf-denormalization",
        title="4NF/5NF & Denormalization", order_index=7, estimated_minutes=25,
        content="""## Fourth Normal Form: independent multi-valued facts

A **multivalued dependency** `X ->-> Y` means: each X value is associated
with a *set* of Y values, independently of the other attributes. Example —
Aarav has skills {Java, Python} and speaks {Hindi, English}, independently:

| name  | skill  | language |
|-------|--------|----------|
| Aarav | Java   | Hindi    |
| Aarav | Java   | English  |
| Aarav | Python | Hindi    |
| Aarav | Python | English  |

2 skills x 2 languages = 4 rows of cross-product redundancy. Add a third
language and two rows must be inserted. **4NF** = in BCNF with no
non-trivial multivalued dependencies. Fix: split the independent facts:

```sql
PersonSkills(name, skill)       -- one row per skill
PersonLanguages(name, language) -- one row per language
```

## Fifth Normal Form: join dependencies

**5NF** handles the rarest case: a table that decomposes losslessly into
*three or more* smaller tables but into no two. If a table can be split
into three projections and rejoined without loss or spurious rows, it has
a **join dependency** and violates 5NF. In practice: if you are splitting
into 3+ tables to kill redundancy, you have arrived at 5NF thinking.

## Denormalization: breaking the rules on purpose

Higher normal forms optimise for *writes* (no anomalies) at the cost of
*reads* (more joins). Sometimes that trade is wrong:

- A dashboard queries department-wise headcount 10,000x/day; departments
  change twice a year. Joining + aggregating every time is wasteful — a
  denormalized `dept_headcount` column (or materialized summary), refreshed
  on write, is the pragmatic choice.
- Reporting tables, data warehouses, and read replicas routinely store
  redundant, pre-joined data for speed.

Denormalization is not "giving up" — it is a conscious trade: you accept
controlled redundancy (with disciplined refresh) to buy read performance.
The key word is *conscious*: normalize first, then denormalize where
measurements justify it, never by accident.
""",
    ),
]

QUESTIONS = [
    # ---------------- dbms-m2-l1: SELECT & WHERE ----------------
    _mkq("dbms-m2-l1-q1", "dbms-m2-l1", "sql", 2,
         "Which query returns ONLY the names of all employees (one column, six rows)?",
         ["SELECT name FROM Employees;", "SELECT * FROM Employees;",
          "SELECT names FROM Employees;", "SELECT name, salary FROM Employees;"],
         0,
         "SELECT lists exactly the columns you name, so SELECT name gives one "
         "column. SELECT * returns every column, and there is no 'names' column "
         "in the schema.",
         ["tcs", "infosys", "wipro"]),
    _mkq("dbms-m2-l1-q2", "dbms-m2-l1", "sql", 3,
         "Using the sample data, what does this return?\n"
         "SELECT name FROM Employees WHERE salary > 60000 AND dept_id = 1;",
         ["Aarav and Kabir", "Aarav, Kabir and Diya", "Kabir only", "No rows"],
         0,
         "Trace each row: Aarav (90000 > 60000, dept 1) qualifies; Kabir "
         "(120000, dept 1) qualifies; Diya earns exactly 60000 which is not > "
         "60000, so AND drops her. Both conditions must be true.",
         ["tcs", "wipro", "accenture"]),
    _mkq("dbms-m2-l1-q3", "dbms-m2-l1", "sql", 4,
         "How many rows does this return?\n"
         "SELECT name FROM Employees WHERE name LIKE 'A%';",
         ["2", "1", "3", "6"],
         0,
         "'A%' means starts with A. Only Aarav and Arjun qualify — 2 rows. "
         "LIKE matching is case-sensitive in most databases, and % matches any "
         "number of characters including zero.",
         ["infosys", "accenture"]),
    _mkq("dbms-m2-l1-q4", "dbms-m2-l1", "sql", 5,
         "How many rows does this return?\n"
         "SELECT name FROM Employees WHERE salary BETWEEN 55000 AND 70000;",
         ["3", "4", "2", "5"],
         0,
         "BETWEEN is inclusive on both ends: Mira (55000), Diya (60000) and "
         "Zara (70000) all qualify — 3 rows. Arjun's NULL salary is unknown, "
         "not inside any range, so he is excluded.",
         ["tcs", "amazon"]),
    _mkq("dbms-m2-l1-q5", "dbms-m2-l1", "sql", 6,
         "How many rows does this return?\n"
         "SELECT name FROM Employees WHERE salary = NULL;",
         ["0 — always, on every database", "1 (Arjun)", "6", "It is a syntax error"],
         0,
         "NULL means unknown, and any comparison with NULL (even NULL = NULL) "
         "is unknown, never true. WHERE keeps only true rows, so this is "
         "always empty. The correct predicate is IS NULL.",
         ["amazon", "microsoft", "google"]),
    _mkq("dbms-m2-l1-q6", "dbms-m2-l1", "sql", 7,
         "Using the sample data, how many rows does this return?\n"
         "SELECT name FROM Employees\n"
         "WHERE hire_date BETWEEN '2022-01-01' AND '2022-12-31' AND dept_id <> 2;",
         ["0", "1", "2", "3"],
         0,
         "The 2022 hires are Diya (dept 2 — killed by <> 2) and Zara "
         "(dept_id NULL — NULL <> 2 is unknown, so the row is dropped). No "
         "rows survive both conditions: 0 rows. This is the classic NULL + "
         "inequality trap.",
         ["google", "amazon", "microsoft"]),
    # ---------------- dbms-m2-l2: ORDER BY, DISTINCT, Aggregates ----------------
    _mkq("dbms-m2-l2-q1", "dbms-m2-l2", "sql", 2,
         "What does ORDER BY salary DESC do to the result rows?",
         ["Puts the highest salary first", "Puts the lowest salary first",
          "Removes duplicate salaries", "Groups rows by salary"],
         0,
         "ORDER BY sorts; DESC means descending, so the largest value comes "
         "first. Deduplication is DISTINCT's job and grouping is GROUP BY's.",
         ["tcs", "infosys"]),
    _mkq("dbms-m2-l2-q2", "dbms-m2-l2", "sql", 3,
         "Using the sample data, how many rows does SELECT DISTINCT dept_id FROM Employees return?",
         ["4", "3", "6", "5"],
         0,
         "The dept_id values are 1, 2, 3 and NULL. DISTINCT collapses the "
         "duplicates (1 and 2 repeat) but keeps NULL as one distinct value, "
         "giving 4 rows: 1, 2, 3, NULL.",
         ["wipro", "accenture"]),
    _mkq("dbms-m2-l2-q3", "dbms-m2-l2", "sql", 4,
         "Using the sample data: SELECT COUNT(*) ... returns 6. What does SELECT COUNT(salary) return?",
         ["5", "6", "4", "0"],
         0,
         "COUNT(*) counts rows; COUNT(column) counts non-NULL values. Arjun's "
         "salary is NULL, so it is skipped: 5.",
         ["tcs", "infosys", "accenture"]),
    _mkq("dbms-m2-l2-q4", "dbms-m2-l2", "sql", 5,
         "Using the sample data, what is SELECT AVG(salary) FROM Employees?",
         ["79000", "65833.33", "72500", "90000"],
         0,
         "AVG ignores NULLs: (90000 + 60000 + 120000 + 55000 + 70000) / 5 = "
         "395000 / 5 = 79000. Dividing by 6 (65833.33) is the trap — Arjun's "
         "NULL salary is skipped entirely.",
         ["amazon", "microsoft"]),
    _mkq("dbms-m2-l2-q5", "dbms-m2-l2", "sql", 6,
         "Using the sample data, what does SELECT MIN(hire_date) FROM Employees return?",
         ["2020-01-10", "2024-01-05", "2021-03-15", "NULL"],
         0,
         "MIN on dates returns the earliest date. Kabir was hired 2020-01-10, "
         "the oldest date in the table. 2024-01-05 (Arjun) is the MAX.",
         ["tcs", "wipro"]),
    _mkq("dbms-m2-l2-q6", "dbms-m2-l2", "sql", 7,
         "Using the sample data, what does SELECT COUNT(DISTINCT dept_id) FROM Employees return?",
         ["3", "4", "5", "6"],
         0,
         "DISTINCT gives 4 values (1, 2, 3, NULL), but COUNT ignores NULLs "
         "even inside DISTINCT, so the answer is 3. Contrast with SELECT "
         "DISTINCT which returns 4 rows including the NULL row.",
         ["google", "amazon"]),
    # ---------------- dbms-m2-l3: GROUP BY & HAVING ----------------
    _mkq("dbms-m2-l3-q1", "dbms-m2-l3", "sql", 2,
         "What does GROUP BY dept_id do before aggregates like AVG(salary) run?",
         ["Splits rows into one bucket per dept_id value, then aggregates inside each bucket",
          "Sorts the rows by dept_id",
          "Removes rows with duplicate dept_id",
          "Joins Employees with Departments"],
         0,
         "GROUP BY partitions rows into groups sharing the grouping value; "
         "aggregates then run per group. Sorting is ORDER BY, dedup is "
         "DISTINCT, joining is JOIN.",
         ["tcs", "infosys"]),
    _mkq("dbms-m2-l3-q2", "dbms-m2-l3", "sql", 3,
         "Using the sample data, how many groups does GROUP BY dept_id produce?",
         ["4", "3", "5", "6"],
         0,
         "Groups: dept 1 (Aarav, Kabir), dept 2 (Diya, Arjun), dept 3 (Mira), "
         "and a NULL group (Zara). NULL forms its own bucket, so 4 groups.",
         ["wipro", "accenture"]),
    _mkq("dbms-m2-l3-q3", "dbms-m2-l3", "sql", 4,
         "Which statement about WHERE and HAVING is TRUE?",
         ["WHERE filters rows before grouping; HAVING filters groups after grouping",
          "HAVING filters rows before grouping; WHERE filters groups after",
          "WHERE can use aggregate functions like AVG, HAVING cannot",
          "They are interchangeable — the optimizer treats them identically"],
         0,
         "The pipeline is FROM -> WHERE (rows) -> GROUP BY -> HAVING "
         "(groups). WHERE cannot see aggregates because grouping has not "
         "happened yet; that is exactly why HAVING exists.",
         ["tcs", "amazon", "microsoft"]),
    _mkq("dbms-m2-l3-q4", "dbms-m2-l3", "sql", 5,
         "Using the sample data, which departments satisfy HAVING AVG(salary) > 70000?",
         ["Engineering (dept 1) only",
          "Engineering (dept 1) and Sales (dept 2)",
          "Engineering (dept 1) and the NULL-dept group",
          "All four groups"],
         0,
         "Averages: dept 1 = 105000, dept 2 = 60000 (NULL skipped), dept 3 = "
         "55000, NULL group = 70000. Only 105000 is strictly greater than "
         "70000 — the NULL group ties at exactly 70000 and fails the > test.",
         ["amazon", "google"]),
    _mkq("dbms-m2-l3-q5", "dbms-m2-l3", "sql", 6,
         "Using the sample data, how many groups survive HAVING COUNT(*) >= 2?",
         ["2", "3", "1", "4"],
         0,
         "Group sizes: dept 1 has 2, dept 2 has 2, dept 3 has 1, NULL group has "
         "1. Only depts 1 and 2 meet >= 2, so 2 groups survive.",
         ["microsoft", "accenture"]),
    _mkq("dbms-m2-l3-q6", "dbms-m2-l3", "sql", 7,
         "Using the sample data, what changes when you add WHERE salary > 55000 before GROUP BY dept_id?",
         ["Dept 3 (HR) disappears from the result entirely",
          "Dept 2 disappears from the result entirely",
          "The NULL-dept group disappears",
          "Nothing changes — WHERE runs after grouping"],
         0,
         "WHERE runs before grouping: Mira's 55000 is not > 55000, and she is "
         "dept 3's only employee, so the whole group vanishes. Arjun's NULL is "
         "also filtered (unknown is not true), leaving dept 2 with just Diya. "
         "WHERE always precedes GROUP BY.",
         ["google", "amazon", "microsoft"]),
    # ---------------- dbms-m2-l4: INNER JOIN ----------------
    _mkq("dbms-m2-l4-q1", "dbms-m2-l4", "sql", 2,
         "What does an INNER JOIN of Employees and Departments on dept_id return?",
         ["Only employees whose dept_id matches a real department",
          "All employees, with NULLs where the department is missing",
          "All departments, with NULLs where employees are missing",
          "Every employee paired with every department"],
         0,
         "INNER keeps only matching pairs. Zara's NULL dept_id matches nothing, "
         "so she is dropped — 5 rows. Keeping unmatched rows is what OUTER "
         "JOINs do; pairing everything is a cartesian product.",
         ["tcs", "infosys"]),
    _mkq("dbms-m2-l4-q2", "dbms-m2-l4", "sql", 3,
         "Using the sample data, how many rows does this return?\n"
         "SELECT e.name, d.dept_name FROM Employees e "
         "JOIN Departments d ON e.dept_id = d.dept_id;",
         ["5", "6", "4", "7"],
         0,
         "Five employees have a dept_id that exists in Departments (101, 102, "
         "103, 104, 105). Zara's NULL matches nothing and is dropped, so 5 "
         "rows — one per matched employee.",
         ["tcs", "wipro", "accenture"]),
    _mkq("dbms-m2-l4-q3", "dbms-m2-l4", "sql", 4,
         "Compare: (A) ... FROM Employees e JOIN Departments d ON e.dept_id = d.dept_id "
         "vs (B) ... FROM Employees e, Departments d WHERE e.dept_id = d.dept_id. True statement?",
         ["Both are inner joins and return identical results",
          "A is an inner join, B is a cross join",
          "A is faster because ON is optimized, B is always slower",
          "B returns more rows than A"],
         0,
         "The comma-plus-WHERE style is the old syntax for exactly the same "
         "inner join. The ON form is preferred for readability (join logic "
         "stays with the join), not for performance.",
         ["infosys", "accenture"]),
    _mkq("dbms-m2-l4-q4", "dbms-m2-l4", "sql", 5,
         "You join 3 tables in one query. How many join conditions (ON clauses) do you need at minimum?",
         ["2", "3", "1", "6"],
         0,
         "Each new table must be linked to the already-joined set: table 2 "
         "joins table 1 (1 condition), table 3 joins the result (1 more). "
         "An n-table join needs n-1 conditions — a missing one means a "
         "cartesian product sneaks in.",
         ["amazon", "microsoft"]),
    _mkq("dbms-m2-l4-q5", "dbms-m2-l4", "sql", 6,
         "Departments: (1, Engineering, Bengaluru), (2, Sales, Mumbai), (3, HR, Delhi), "
         "(4, Support, Bengaluru). Which employees does this return?\n"
         "SELECT e.name FROM Employees e JOIN Departments d ON e.dept_id = d.dept_id "
         "WHERE d.location = 'Bengaluru';",
         ["Aarav and Kabir", "Aarav, Kabir and Zara",
          "Aarav, Kabir and Arjun", "No rows"],
         0,
         "Bengaluru departments are 1 (Engineering) and 4 (Support). Dept 1 "
         "employees: Aarav, Kabir. Support has no employees, and the INNER "
         "JOIN drops Zara (NULL dept) anyway. So 2 rows.",
         ["amazon", "google"]),
    _mkq("dbms-m2-l4-q6", "dbms-m2-l4", "sql", 7,
         "What happens if you write FROM Employees e JOIN Departments d with NO on-clause at all?",
         ["Cartesian product: 6 x 4 = 24 rows",
          "Syntax error — ON is mandatory",
          "It behaves like a LEFT JOIN",
          "0 rows, because nothing matches"],
         0,
         "Without a join condition every row pairs with every row: 6 "
         "employees x 4 departments = 24 nonsense rows. (Comma-style without "
         "WHERE does the same.) If a join explodes in row count, the missing "
         "ON is the first suspect.",
         ["google", "microsoft", "amazon"]),
    # ---------------- dbms-m2-l5: OUTER JOINs ----------------
    _mkq("dbms-m2-l5-q1", "dbms-m2-l5", "sql", 2,
         "What does Departments LEFT JOIN Employees keep?",
         ["Every department, even those with no employees (NULLs for missing employees)",
          "Every employee, even those with no department",
          "Only departments that have at least one employee",
          "Only employees that have a department"],
         0,
         "LEFT JOIN preserves all rows of the left (first) table. Unmatched "
         "departments survive with NULL employee columns. Keeping only "
         "matches is INNER JOIN's behaviour.",
         ["tcs", "infosys"]),
    _mkq("dbms-m2-l5-q2", "dbms-m2-l5", "sql", 3,
         "Using the sample data, how many rows does this return?\n"
         "SELECT d.dept_name, e.name FROM Departments d "
         "LEFT JOIN Employees e ON d.dept_id = e.dept_id;",
         ["6", "5", "7", "4"],
         0,
         "Engineering->2, Sales->2, HR->1 = 5 matched rows, plus Support with "
         "a NULL employee row = 6. LEFT JOIN keeps the unmatched department "
         "instead of dropping it.",
         ["wipro", "accenture"]),
    _mkq("dbms-m2-l5-q3", "dbms-m2-l5", "sql", 4,
         "In the LEFT JOIN above, which dept_name row has a NULL name?",
         ["Support", "HR", "Sales", "None — LEFT JOIN never produces NULLs"],
         0,
         "Support (dept 4) has no employees, so its row survives with NULL in "
         "the employee columns. Those NULLs are the signature of an outer "
         "join — they mark 'no match found'.",
         ["tcs", "infosys"]),
    _mkq("dbms-m2-l5-q4", "dbms-m2-l5", "sql", 5,
         "A RIGHT JOIN keeps all rows from which table?",
         ["The right (second) table",
          "The left (first) table",
          "Both tables",
          "Only the matched rows of both"],
         0,
         "RIGHT JOIN preserves the right table's rows. A RIGHT JOIN B is "
         "exactly B LEFT JOIN A — same result, just written from the other "
         "side. Keeping both sides' unmatched rows is FULL OUTER JOIN.",
         ["accenture", "wipro"]),
    _mkq("dbms-m2-l5-q5", "dbms-m2-l5", "sql", 6,
         "Using the sample data, how many rows does this return?\n"
         "SELECT d.dept_name, e.name FROM Departments d "
         "FULL OUTER JOIN Employees e ON d.dept_id = e.dept_id;",
         ["7", "6", "10", "5"],
         0,
         "5 matched pairs + Support (unmatched department, NULL employee) + "
         "Zara (unmatched employee, NULL department) = 7 rows. FULL OUTER "
         "keeps unmatched rows from both sides.",
         ["amazon", "microsoft"]),
    _mkq("dbms-m2-l5-q6", "dbms-m2-l5", "sql", 7,
         "Which department shows headcount 0 in this query?\n"
         "SELECT d.dept_name, COUNT(e.emp_id) AS headcount FROM Departments d "
         "LEFT JOIN Employees e ON d.dept_id = e.dept_id GROUP BY d.dept_name;",
         ["Support", "HR", "Sales", "None — every department has employees"],
         0,
         "Support has no employees: its LEFT JOIN row carries NULL emp_id, "
         "and COUNT(emp_id) skips NULLs, giving an honest 0. Note COUNT(*) "
         "would wrongly show 1 — counting the key of the nullable side is "
         "the correct pattern.",
         ["google", "amazon", "microsoft"]),
    # ---------------- dbms-m2-l6: Subqueries ----------------
    _mkq("dbms-m2-l6-q1", "dbms-m2-l6", "sql", 2,
         "In WHERE salary > (SELECT AVG(salary) FROM Employees), what does the subquery return?",
         ["A single value (the average salary)",
          "One row per employee",
          "A boolean true/false",
          "The list of all salaries"],
         0,
         "This is a scalar subquery — it returns exactly one value, which the "
         "outer > compares against. Multi-row results need IN, ANY or ALL "
         "instead.",
         ["tcs", "infosys"]),
    _mkq("dbms-m2-l6-q2", "dbms-m2-l6", "sql", 3,
         "What does WHERE dept_id IN (SELECT dept_id FROM Departments WHERE location = 'Bengaluru') do?",
         ["Keeps employees whose dept_id appears in the subquery's result list",
          "Keeps employees whose dept_id is greater than every Bengaluru dept",
          "Joins the two tables on location",
          "Returns each Bengaluru department once"],
         0,
         "IN tests membership: the subquery yields {1, 4} (Engineering and "
         "Support are in Bengaluru), and the outer keeps employees in those "
         "departments — Aarav and Kabir.",
         ["wipro", "accenture"]),
    _mkq("dbms-m2-l6-q3", "dbms-m2-l6", "sql", 4,
         "Company average salary is 79000. Which employees does this return?\n"
         "SELECT name FROM Employees WHERE salary > (SELECT AVG(salary) FROM Employees);",
         ["Aarav and Kabir", "Kabir only", "Aarav, Kabir and Zara", "Diya, Aarav and Kabir"],
         0,
         "Above 79000: Aarav (90000) and Kabir (120000). Diya (60000) and the "
         "rest are below; Arjun's NULL is not > anything. 2 rows.",
         ["tcs", "amazon"]),
    _mkq("dbms-m2-l6-q4", "dbms-m2-l6", "sql", 5,
         "Which employees earn MORE than their own department's average?\n"
         "SELECT name FROM Employees e WHERE salary > "
         "(SELECT AVG(salary) FROM Employees WHERE dept_id = e.dept_id);",
         ["Kabir only", "Aarav and Kabir", "Kabir and Diya", "Aarav only"],
         0,
         "Correlated: the inner query re-runs per row. Dept 1 avg = 105000: "
         "Aarav 90000 no, Kabir 120000 YES. Dept 2 avg = 60000: Diya 60000 "
         "not > 60000, Arjun NULL no. Dept 3: Mira 55000 not > 55000. Zara: "
         "inner WHERE is unknown, avg NULL, no. Kabir only.",
         ["amazon", "google", "microsoft"]),
    _mkq("dbms-m2-l6-q5", "dbms-m2-l6", "sql", 6,
         "Using the sample data, how many rows does this return?\n"
         "SELECT name FROM Employees WHERE dept_id NOT IN (1, 2, NULL);",
         ["0", "1 (Mira)", "2 (Mira and Zara)", "5"],
         0,
         "The classic NULL poison: each row is tested as dept_id<>1 AND "
         "dept_id<>2 AND dept_id<>NULL. The last term is always unknown, so "
         "the whole AND is never true — 0 rows, even Mira (dept 3). Never "
         "put NULL in a NOT IN list; use NOT EXISTS.",
         ["google", "microsoft", "amazon"]),
    _mkq("dbms-m2-l6-q6", "dbms-m2-l6", "sql", 7,
         "How many employees does this return?\n"
         "SELECT name FROM Employees e WHERE EXISTS "
         "(SELECT 1 FROM Departments d WHERE d.dept_id = e.dept_id);",
         ["5", "6", "4", "0"],
         0,
         "EXISTS is true when the subquery finds at least one match. Five "
         "employees have a real department; Zara's NULL dept_id matches "
         "nothing, so EXISTS is false for her. 5 rows.",
         ["microsoft", "google"]),
    # ---------------- dbms-m2-l7: Set Operations ----------------
    _mkq("dbms-m2-l7-q1", "dbms-m2-l7", "sql", 2,
         "What does UNION do with the results of two SELECT queries?",
         ["Stacks their rows vertically into one result",
          "Adds their columns side by side",
          "Keeps only rows present in both",
          "Removes rows present in the second"],
         0,
         "UNION concatenates result sets row-wise (more rows). Side-by-side "
         "columns is JOIN; rows-in-both is INTERSECT; rows-not-in-second is "
         "EXCEPT.",
         ["tcs", "infosys"]),
    _mkq("dbms-m2-l7-q2", "dbms-m2-l7", "sql", 3,
         "What is the difference between UNION and UNION ALL?",
         ["UNION removes duplicate rows; UNION ALL keeps them (and is faster)",
          "UNION ALL removes duplicates; UNION keeps them",
          "UNION sorts, UNION ALL does not allow ORDER BY",
          "There is no difference — they are synonyms"],
         0,
         "UNION deduplicates (paying for a sort), UNION ALL skips that step. "
         "Use UNION ALL whenever duplicates are impossible or wanted — it is "
         "strictly cheaper.",
         ["tcs", "wipro", "accenture"]),
    _mkq("dbms-m2-l7-q3", "dbms-m2-l7", "sql", 4,
         "For SELECT a, b ... UNION SELECT c, d ... to be valid, what must hold?",
         ["Both SELECTs return the same number of columns with compatible types",
          "Both tables must have the same name",
          "Both SELECTs must have WHERE clauses",
          "The column names must be identical"],
         0,
         "Set operations align columns positionally: equal count, compatible "
         "types. Names can differ (the first query's names win). Table names "
         "and WHERE clauses are irrelevant.",
         ["infosys", "accenture"]),
    _mkq("dbms-m2-l7-q4", "dbms-m2-l7", "sql", 5,
         "Using the sample data, how many rows does this return?\n"
         "SELECT dept_id FROM Employees UNION SELECT dept_id FROM Departments;",
         ["5", "10", "4", "6"],
         0,
         "Employee dept_ids {1,2,3,NULL} union department ids {1,2,3,4}, "
         "deduped = {1, 2, 3, 4, NULL} = 5 rows. UNION ALL would give 10.",
         ["amazon", "microsoft"]),
    _mkq("dbms-m2-l7-q5", "dbms-m2-l7", "sql", 6,
         "Using the sample data, how many rows does this return?\n"
         "SELECT dept_id FROM Employees INTERSECT SELECT dept_id FROM Departments;",
         ["3", "4", "5", "1"],
         0,
         "INTERSECT keeps values in both sets: {1,2,3,NULL} n {1,2,3,4} = "
         "{1, 2, 3} = 3 rows. NULL is not in Departments, so it drops out.",
         ["microsoft", "google"]),
    _mkq("dbms-m2-l7-q6", "dbms-m2-l7", "sql", 7,
         "Using the sample data, how many rows does this return?\n"
         "SELECT dept_id FROM Employees EXCEPT SELECT dept_id FROM Departments;",
         ["1", "0", "2", "3"],
         0,
         "{1,2,3,NULL} minus {1,2,3,4} leaves only NULL — 1 row. For "
         "duplicate elimination NULL equals NULL, but no department id is "
         "NULL, so the NULL survives the EXCEPT.",
         ["google", "amazon"]),
    # ---------------- dbms-m2-l8: DDL & Constraints ----------------
    _mkq("dbms-m2-l8-q1", "dbms-m2-l8", "sql", 2,
         "What does CREATE TABLE do?",
         ["Defines a new table's structure (columns, types, constraints)",
          "Inserts rows into an existing table",
          "Deletes a table and its data",
          "Grants users permission on a table"],
         0,
         "CREATE TABLE is DDL — it defines structure. INSERT adds rows, DROP "
         "deletes the table, GRANT handles permissions.",
         ["tcs", "infosys"]),
    _mkq("dbms-m2-l8-q2", "dbms-m2-l8", "sql", 3,
         "Which is TRUE about a PRIMARY KEY?",
         ["One per table; values must be unique and never NULL",
          "Many allowed per table; NULLs permitted",
          "It is the same as a FOREIGN KEY",
          "It only speeds up queries and enforces nothing"],
         0,
         "PRIMARY KEY = UNIQUE + NOT NULL, exactly one per table. Multiple "
         "UNIQUE constraints are allowed (each tolerating one NULL), but "
         "there is only one primary key.",
         ["tcs", "wipro", "accenture"]),
    _mkq("dbms-m2-l8-q3", "dbms-m2-l8", "sql", 4,
         "Employees.dept_id is a FOREIGN KEY REFERENCES Departments(dept_id). "
         "What happens on INSERT INTO Employees VALUES (107, 'Rehan', 99, 80000, '2024-02-01') "
         "when no department 99 exists?",
         ["Rejected — violates referential integrity",
          "Inserted, with dept_name set to NULL",
          "Inserted, and department 99 is auto-created",
          "Inserted, but the row is invisible until department 99 exists"],
         0,
         "A foreign key demands the parent row exist (or the value be NULL). "
         "99 matches no department, so the database rejects the insert. This "
         "is referential integrity doing its job.",
         ["infosys", "accenture", "amazon"]),
    _mkq("dbms-m2-l8-q4", "dbms-m2-l8", "sql", 5,
         "The table has CHECK (salary > 0). What happens on "
         "INSERT INTO Employees VALUES (108, 'Sana', 1, -100, '2024-03-01')?",
         ["Rejected — violates the CHECK constraint",
          "Inserted; CHECK only warns",
          "Inserted with salary stored as 100",
          "Inserted with salary stored as NULL"],
         0,
         "CHECK is enforced per row at insert/update time: -100 is not > 0, "
         "so the statement fails. Constraints make bad data impossible "
         "regardless of application bugs.",
         ["amazon", "microsoft"]),
    _mkq("dbms-m2-l8-q5", "dbms-m2-l8", "sql", 6,
         "What does ALTER TABLE Employees ADD email VARCHAR(100) do to existing rows?",
         ["Adds the column; existing rows get NULL in email",
          "Adds the column; existing rows get empty string in email",
          "Fails — you cannot ALTER a table that has data",
          "Deletes all existing rows first"],
         0,
         "ALTER TABLE ADD COLUMN extends the schema; existing rows simply get "
         "NULL for the new column (unless a DEFAULT is specified). Data is "
         "never destroyed by adding a column.",
         ["tcs", "microsoft"]),
    _mkq("dbms-m2-l8-q6", "dbms-m2-l8", "sql", 7,
         "Which statement about UNIQUE vs PRIMARY KEY is TRUE?",
         ["A table can have many UNIQUE columns (each allowing one NULL) but only one PRIMARY KEY (no NULLs)",
          "UNIQUE forbids NULLs but PRIMARY KEY allows them",
          "They are identical; the names are interchangeable",
          "UNIQUE can appear only once per table, PRIMARY KEY many times"],
         0,
         "PRIMARY KEY is singular and NOT NULL by definition. UNIQUE columns "
         "can be plural and, in most databases, each tolerates a single NULL "
         "(NULLs are not considered equal to each other).",
         ["google", "amazon", "microsoft"]),
    # ---------------- dbms-m2-l9: DML, TCL & DCL ----------------
    _mkq("dbms-m2-l9-q1", "dbms-m2-l9", "sql", 2,
         "Which commands belong to DML?",
         ["INSERT, UPDATE, DELETE", "CREATE, ALTER, DROP",
          "COMMIT, ROLLBACK, SAVEPOINT", "GRANT, REVOKE"],
         0,
         "DML manipulates rows: INSERT/UPDATE/DELETE. CREATE/ALTER/DROP are "
         "DDL, COMMIT/ROLLBACK/SAVEPOINT are TCL, GRANT/REVOKE are DCL.",
         ["tcs", "infosys"]),
    _mkq("dbms-m2-l9-q2", "dbms-m2-l9", "sql", 3,
         "You run BEGIN; then two UPDATEs; then ROLLBACK;. What is the database state?",
         ["Both UPDATEs are undone, as if they never ran",
          "The first UPDATE stays, the second is undone",
          "Both UPDATEs are permanently saved",
          "The transaction is paused until COMMIT"],
         0,
         "ROLLBACK discards everything since BEGIN — the transaction is "
         "atomic: all or nothing. COMMIT would have made both permanent.",
         ["wipro", "accenture"]),
    _mkq("dbms-m2-l9-q3", "dbms-m2-l9", "sql", 4,
         "What is a SAVEPOINT used for?",
         ["Rolling back part of a transaction while keeping earlier work",
          "Permanently saving the transaction",
          "Creating a backup of the whole database",
          "Granting a user partial permissions"],
         0,
         "SAVEPOINT marks a checkpoint: ROLLBACK TO savepoint undoes only the "
         "work after it. COMMIT saves; backups and grants are different "
         "concepts.",
         ["tcs", "infosys"]),
    _mkq("dbms-m2-l9-q4", "dbms-m2-l9", "sql", 5,
         "What is the difference between GRANT and REVOKE?",
         ["GRANT gives a privilege; REVOKE takes it away",
          "REVOKE gives a privilege; GRANT takes it away",
          "GRANT is for tables, REVOKE is for databases",
          "Both permanently delete user accounts"],
         0,
         "DCL in two words: GRANT SELECT ON Employees TO analyst gives read "
         "access; REVOKE SELECT ... FROM analyst removes it.",
         ["accenture", "wipro"]),
    _mkq("dbms-m2-l9-q5", "dbms-m2-l9", "sql", 6,
         "Which of DELETE / TRUNCATE / DROP removes the table definition itself?",
         ["DROP", "DELETE", "TRUNCATE", "All three"],
         0,
         "DROP deletes the table structure plus its data — the table no "
         "longer exists. DELETE and TRUNCATE empty the rows but the table "
         "definition survives.",
         ["amazon", "microsoft"]),
    _mkq("dbms-m2-l9-q6", "dbms-m2-l9", "sql", 7,
         "In MySQL/Oracle, which statements auto-commit and typically CANNOT be rolled back?",
         ["TRUNCATE and DROP (DDL auto-commits)",
          "DELETE and UPDATE",
          "INSERT and SELECT",
          "GRANT and COMMIT"],
         0,
         "DDL statements like TRUNCATE and DROP auto-commit in MySQL/Oracle, "
         "so ROLLBACK cannot undo them. DELETE is DML — inside a transaction "
         "it rolls back normally. GRANT is DCL, not DDL.",
         ["google", "amazon"]),
    # ---------------- dbms-m2-l10: Window Functions ----------------
    _mkq("dbms-m2-l10-q1", "dbms-m2-l10", "sql", 2,
         "What is the key difference between AVG(salary) and AVG(salary) OVER ()?",
         ["OVER () keeps every row and adds the average as a new column; plain AVG collapses to one row",
          "OVER () is faster on large tables",
          "Plain AVG ignores NULLs but OVER () includes them",
          "There is no difference"],
         0,
         "Window functions compute without collapsing: 6 rows in, 6 rows out, "
         "each annotated with 79000. The aggregate alone returns a single "
         "row. Both ignore NULLs identically.",
         ["tcs", "infosys"]),
    _mkq("dbms-m2-l10-q2", "dbms-m2-l10", "sql", 3,
         "What does PARTITION BY dept_id do in AVG(salary) OVER (PARTITION BY dept_id)?",
         ["Restarts the average separately for each department",
          "Sorts the output by dept_id",
          "Removes duplicate departments",
          "Joins with the Departments table"],
         0,
         "PARTITION BY divides rows into groups and runs the window function "
         "inside each — Aarav/Kabir see 105000, Diya/Arjun see 60000 — while "
         "still returning every row.",
         ["wipro", "accenture"]),
    _mkq("dbms-m2-l10-q3", "dbms-m2-l10", "sql", 4,
         "Salaries: 120000, 90000, 90000, 60000. What does RANK() OVER (ORDER BY salary DESC) produce?",
         ["1, 2, 2, 4", "1, 2, 2, 3", "1, 2, 3, 4", "1, 1, 2, 3"],
         0,
         "RANK gives ties the same rank then SKIPS: the two 90000s share rank "
         "2, so the next rank is 4, not 3. That skip is RANK's defining "
         "behaviour.",
         ["amazon", "microsoft"]),
    _mkq("dbms-m2-l10-q4", "dbms-m2-l10", "sql", 5,
         "Same salaries: 120000, 90000, 90000, 60000. What does DENSE_RANK() OVER (ORDER BY salary DESC) produce?",
         ["1, 2, 2, 3", "1, 2, 2, 4", "1, 2, 3, 4", "1, 3, 3, 4"],
         0,
         "DENSE_RANK shares ranks on ties but does NOT skip: 1, 2, 2, 3. "
         "'Top 3 including ties' needs DENSE_RANK <= 3 — with RANK the skip "
         "means rank 3 never appears, so results differ.",
         ["google", "amazon"]),
    _mkq("dbms-m2-l10-q5", "dbms-m2-l10", "sql", 6,
         "Same salaries: 120000, 90000, 90000, 60000. What does ROW_NUMBER() OVER (ORDER BY salary DESC) produce?",
         ["1, 2, 3, 4 (ties get arbitrary distinct numbers)",
          "1, 2, 2, 4",
          "1, 2, 2, 3",
          "1, 1, 3, 4"],
         0,
         "ROW_NUMBER never shares: it numbers rows 1-4 sequentially, breaking "
         "the 90000 tie arbitrarily. Use it when you need exactly N rows "
         "(e.g. top-3 per group with ties broken somehow).",
         ["microsoft", "google"]),
    _mkq("dbms-m2-l10-q6", "dbms-m2-l10", "sql", 7,
         "What does LAG(salary) OVER (ORDER BY hire_date) return for Kabir, the earliest hire (2020-01-10)?",
         ["NULL — there is no previous row",
          "0",
          "120000 (his own salary)",
          "90000 (the next hire's salary)"],
         0,
         "LAG reads the previous row in the window ordering; Kabir is first, "
         "so there is no previous row and the result is NULL. (LEAD would "
         "give Aarav's 90000 — the next hire.)",
         ["google", "amazon", "microsoft"]),
    # ---------------- dbms-m3-l1: Data Anomalies ----------------
    _mkq("dbms-m3-l1-q1", "dbms-m3-l1", "normalization", 3,
         "In the Student-Course-Instructor table, a new instructor Dr Iyer is hired for a new course 'AI', "
         "but no student has enrolled yet. The table cannot record her. This is an example of:",
         ["Insertion anomaly", "Update anomaly", "Deletion anomaly", "Referential integrity"],
         0,
         "An insertion anomaly: you cannot insert one fact (instructor/course) "
         "without an unrelated fact (a student), because the table's key "
         "demands a student_id.",
         ["tcs", "infosys"]),
    _mkq("dbms-m3-l1-q2", "dbms-m3-l1", "normalization", 4,
         "Dr Rao moves from office R-201 to R-205, and her office is stored in 2 rows. "
         "If only one row is updated, the database claims she has two offices. This is:",
         ["Update anomaly", "Insertion anomaly", "Deletion anomaly", "Lossless join"],
         0,
         "An update anomaly: one real-world fact stored redundantly in many "
         "rows, so a partial update creates a contradiction. Redundancy is "
         "the update anomaly waiting to happen.",
         ["tcs", "wipro"]),
    _mkq("dbms-m3-l1-q3", "dbms-m3-l1", "normalization", 5,
         "Diya drops OS — her only course — and her row is deleted. The database also loses the fact that "
         "Dr Sen's office is R-105. This is:",
         ["Deletion anomaly", "Insertion anomaly", "Update anomaly", "Transitive dependency"],
         0,
         "A deletion anomaly: removing one fact (Diya's enrollment) destroys "
         "an unrelated fact (Dr Sen's office) that happened to share the row.",
         ["infosys", "accenture"]),
    _mkq("dbms-m3-l1-q4", "dbms-m3-l1", "normalization", 6,
         "A college wants to store a planned course 'Quantum' with its instructor BEFORE admissions open. "
         "The single-table design blocks this. Which anomaly, and what is the root cause?",
         ["Insertion anomaly — course facts cannot exist without a student row",
          "Deletion anomaly — the course will be lost when students graduate",
          "Update anomaly — the instructor name will be spelled inconsistently",
          "No anomaly — planned courses do not need storing"],
         0,
         "Insertion anomaly: the table's grain is 'enrollment', so anything "
         "that is not an enrollment has nowhere to live. The root cause is "
         "mixing independent facts (courses, instructors, students) in one "
         "table.",
         ["amazon", "microsoft"]),
    _mkq("dbms-m3-l1-q5", "dbms-m3-l1", "normalization", 7,
         "Why is redundancy (e.g. instructor_office repeated per enrollment) considered harmful, "
         "beyond wasting disk space?",
         ["It enables update anomalies — partial updates create contradictions",
          "It makes SELECT queries syntactically invalid",
          "It prevents the use of primary keys",
          "It forces the table out of 1NF"],
         0,
         "Disk is cheap; inconsistency is expensive. Repeating one fact in N "
         "rows means N updates must all succeed — miss one and the database "
         "contradicts itself. Redundancy does not break 1NF (values are "
         "still atomic).",
         ["google", "amazon"]),
    _mkq("dbms-m3-l1-q6", "dbms-m3-l1", "normalization", 8,
         "What single design flaw causes all three anomalies in the Student-Course-Instructor table?",
         ["One table stores facts about three independent things (students, courses, instructors)",
          "The table has no primary key",
          "The table has too few rows",
          "The table uses VARCHAR instead of INT ids"],
         0,
         "All three anomalies share one root cause: multi-theme tables. When "
         "student facts, course facts and instructor facts share rows, "
         "inserting/updating/deleting one theme damages the others. "
         "Normalization splits the themes apart.",
         ["google", "microsoft"]),
    # ---------------- dbms-m3-l2: Functional Dependencies ----------------
    _mkq("dbms-m3-l2-q1", "dbms-m3-l2", "normalization", 3,
         "What does the functional dependency X -> Y mean?",
         ["Whenever two rows agree on X, they must agree on Y",
          "X and Y are always equal",
          "Y determines X",
          "X is the primary key and Y is a foreign key"],
         0,
         "X -> Y is about determination: one X value always pairs with the "
         "same Y value (e.g. one student_id -> one student_name). It says "
         "nothing about keys directly.",
         ["tcs", "infosys"]),
    _mkq("dbms-m3-l2-q2", "dbms-m3-l2", "normalization", 4,
         "In the enrollment table, which FD holds?",
         ["student_id -> student_name",
          "student_name -> student_id",
          "course_name -> instructor",
          "instructor_office -> instructor"],
         0,
         "Each student_id identifies exactly one student_name. The reverse "
         "fails (two students could share a name); course_name does not fix "
         "the instructor if team-teaching exists; two instructors could share "
         "an office.",
         ["wipro", "accenture"]),
    _mkq("dbms-m3-l2-q3", "dbms-m3-l2", "normalization", 5,
         "Armstrong's reflexivity axiom says:",
         ["If Y is a subset of X, then X -> Y",
          "If X -> Y then Y -> X",
          "If X -> Y and Y -> Z then X -> Z",
          "If X -> Y then XZ -> YZ"],
         0,
         "Reflexivity is the trivial rule: a set determines its own subsets, "
         "e.g. {student_id, course_id} -> {student_id}. Transitivity is the "
         "third option; augmentation is the fourth.",
         ["tcs", "amazon"]),
    _mkq("dbms-m3-l2-q4", "dbms-m3-l2", "normalization", 6,
         "Given A -> B and B -> C, what can you infer?",
         ["A -> C (transitivity)", "C -> A", "B -> A", "Nothing — FDs do not compose"],
         0,
         "Transitivity: determination chains. If A fixes B and B fixes C, "
         "then A fixes C. The reverse (C -> A) does not follow.",
         ["infosys", "microsoft"]),
    _mkq("dbms-m3-l2-q5", "dbms-m3-l2", "normalization", 7,
         "R(A, B, C, D, E) with FDs {A->B, B->C, CD->E}. What is the closure A+?",
         ["{A, B, C}", "{A, B, C, D, E}", "{A, B}", "{A}"],
         0,
         "Trace: start {A}; A->B fires -> {A,B}; B->C fires -> {A,B,C}; "
         "CD->E cannot fire (D missing). Closure = {A,B,C} — so A alone is "
         "not a key.",
         ["amazon", "google"]),
    _mkq("dbms-m3-l2-q6", "dbms-m3-l2", "normalization", 8,
         "Same R and FDs {A->B, B->C, CD->E}. Which of A, CD, ACD is a candidate key?",
         ["ACD", "A", "CD", "None of them"],
         0,
         "A+ = {A,B,C} (not all); (CD)+ = {C,D,E} (not all); (ACD)+ starts "
         "{A,C,D}, A->B fires -> {A,B,C,D}, CD->E fires -> all five. ACD "
         "determines everything and is minimal, so it is the candidate key.",
         ["google", "microsoft", "amazon"]),
    # ---------------- dbms-m3-l3: 1NF ----------------
    _mkq("dbms-m3-l3-q1", "dbms-m3-l3", "normalization", 3,
         "What does 1NF require?",
         ["Every cell holds a single atomic value",
          "Every table has a primary key",
          "No transitive dependencies",
          "No partial dependencies"],
         0,
         "1NF = atomic values only: no lists, no comma-separated bundles, no "
         "repeating groups. Keys and dependency rules belong to higher "
         "normal forms.",
         ["tcs", "infosys"]),
    _mkq("dbms-m3-l3-q2", "dbms-m3-l3", "normalization", 4,
         "Orders(order_id, customer, items) with items = 'laptop, mouse, keyboard' in one cell. "
         "What is wrong?",
         ["Violates 1NF — items is not atomic",
          "Violates 2NF — partial dependency",
          "Violates 3NF — transitive dependency",
          "Nothing — this is valid 1NF"],
         0,
         "A packed list in one cell is the textbook 1NF violation: you "
         "cannot count, filter or join individual items without string "
         "surgery.",
         ["wipro", "accenture"]),
    _mkq("dbms-m3-l3-q3", "dbms-m3-l3", "normalization", 5,
         "What is the correct 1NF fix for the packed 'items' column?",
         ["One row per item: OrderItems(order_id, item)",
          "Add more columns: item1, item2, item3",
          "Store the list as JSON text",
          "Delete the items column"],
         0,
         "Give each value its own row — then COUNT(*) answers 'how many "
         "items'. Adding item1..item3 just moves the repeating group into "
         "columns (still not 1NF); JSON keeps the value non-atomic.",
         ["tcs", "amazon"]),
    _mkq("dbms-m3-l3-q4", "dbms-m3-l3", "normalization", 6,
         "Students(student_id, name, phone_numbers) stores '98xx, 97xx' in one cell. The 1NF fix is:",
         ["A separate StudentPhones(student_id, phone) table with one row per number",
          "A wider VARCHAR for phone_numbers",
          "Two columns phone1, phone2",
          "Storing only the first number"],
         0,
         "Multi-valued attributes get their own table with one row per value. "
         "phone1/phone2 caps students at two numbers and repeats the "
         "repeating-group mistake as columns.",
         ["infosys", "microsoft"]),
    _mkq("dbms-m3-l3-q5", "dbms-m3-l3", "normalization", 7,
         "Which table design violates 1NF?",
         ["Marks(student_id, course1, course2, course3)",
          "Marks(student_id, course_id, marks)",
          "Students(student_id, name)",
          "Courses(course_id, title)"],
         0,
         "course1..course3 is a repeating group spread across columns — what "
         "happens at the 4th course? Columns must not multiply to simulate "
         "rows. The (student_id, course_id, marks) shape is properly 1NF.",
         ["google", "amazon"]),
    _mkq("dbms-m3-l3-q6", "dbms-m3-l3", "normalization", 8,
         "A designer argues address = 'Bengaluru, Karnataka' in one column is fine 'because we never query by city'. "
         "Why is this still a 1NF risk?",
         ["The value is composite — any future need to filter/sort by city requires string parsing",
          "It wastes exactly 2 bytes per row",
          "VARCHAR cannot hold commas",
          "It violates 2NF, not 1NF"],
         0,
         "Atomicity is about the value's structure, not today's queries. A "
         "composite value hides independently meaningful parts (city, state); "
         "the day someone asks 'students per city', the design collapses "
         "into string surgery.",
         ["microsoft", "google"]),
    # ---------------- dbms-m3-l4: 2NF ----------------
    _mkq("dbms-m3-l4-q1", "dbms-m3-l4", "normalization", 3,
         "What does 2NF forbid?",
         ["A non-key attribute depending on only part of a composite key (partial dependency)",
          "Any duplicate values in a column",
          "More than one candidate key",
          "NULL values in non-key columns"],
         0,
         "2NF = 1NF + no partial dependencies. It only bites when the key is "
         "composite — a proper subset of the key determining a column.",
         ["tcs", "infosys"]),
    _mkq("dbms-m3-l4-q2", "dbms-m3-l4", "normalization", 4,
         "Registration(student_id, course_id, grade, student_name, course_name), "
         "key = (student_id, course_id). Which FD is a partial dependency?",
         ["student_id -> student_name",
          "(student_id, course_id) -> grade",
          "(student_id, course_id) -> student_name",
          "grade -> course_name"],
         0,
         "student_id alone (a proper part of the key) determines "
         "student_name — that is partial. grade needs the full key (full "
         "dependency). The third option is not even a valid FD here.",
         ["tcs", "wipro"]),
    _mkq("dbms-m3-l4-q3", "dbms-m3-l4", "normalization", 5,
         "Decompose Registration(student_id, course_id, grade, student_name, course_name) "
         "with FDs student_id->student_name, course_id->course_name into 2NF. Correct split?",
         ["Students(student_id, student_name), Courses(course_id, course_name), "
          "Grades(student_id, course_id, grade)",
          "Students(student_id, course_id), Courses(course_name, grade)",
          "One table: Registration(student_id, grade) only",
          "Students(student_name, course_name), Grades(student_id, course_id)"],
         0,
         "Each FD gets its own table keyed by its determinant; the full-key "
         "FD (grade) keeps the composite key table. All FDs preserved, "
         "nothing repeats, join recovers the original.",
         ["infosys", "accenture", "amazon"]),
    _mkq("dbms-m3-l4-q4", "dbms-m3-l4", "normalization", 6,
         "In the Registration table, which FD is a FULL dependency (not partial)?",
         ["(student_id, course_id) -> grade",
          "student_id -> student_name",
          "course_id -> course_name",
          "student_id -> course_id"],
         0,
         "grade needs the whole composite key — neither student_id nor "
         "course_id alone determines it. The other two use only part of the "
         "key, which is precisely the 2NF violation.",
         ["amazon", "microsoft"]),
    _mkq("dbms-m3-l4-q5", "dbms-m3-l4", "normalization", 7,
         "A table is in 1NF and its primary key is a single attribute. What can you say about 2NF?",
         ["It is automatically in 2NF — partial dependency needs a composite key",
          "It is automatically in 3NF as well",
          "It still needs checking for partial dependencies",
          "2NF is impossible with a single-column key"],
         0,
         "Partial dependency means 'part of the key determines a column' — "
         "with a single-attribute key there is no 'part' smaller than the "
         "key itself. 3NF (transitive chains) can still fail, though.",
         ["google", "amazon"]),
    _mkq("dbms-m3-l4-q6", "dbms-m3-l4", "normalization", 8,
         "R(A, B, C, D) with key (A, B) and FDs {A->C, B->D}. Is R in 2NF?",
         ["No — both A->C and B->D are partial dependencies",
          "Yes — all FDs use the full key",
          "No — it violates 1NF",
          "Yes — 2NF only cares about transitive dependencies"],
         0,
         "A is a proper subset of key (A,B) yet determines C; same for B->D. "
         "Both are partial dependencies, so R is in 1NF but not 2NF. "
         "(Transitive chains are 3NF's concern, not 2NF's.)",
         ["google", "microsoft"]),
    # ---------------- dbms-m3-l5: 3NF ----------------
    _mkq("dbms-m3-l5-q1", "dbms-m3-l5", "normalization", 3,
         "What does 3NF forbid?",
         ["A non-key attribute depending transitively on the key (key -> X -> Y)",
          "Any composite primary key",
          "Storing the same value twice in any column",
          "Foreign keys referencing non-key columns"],
         0,
         "3NF = 2NF + no transitive dependencies of non-key attributes on the "
         "key. The chain key -> X -> Y (X not a superkey) is the violation.",
         ["tcs", "infosys"]),
    _mkq("dbms-m3-l5-q2", "dbms-m3-l5", "normalization", 4,
         "Employees(emp_id, dept_id, dept_name) with emp_id->dept_id and dept_id->dept_name. "
         "What is the transitive dependency?",
         ["emp_id -> dept_name via dept_id",
          "dept_name -> emp_id via dept_id",
          "emp_id -> dept_id",
          "dept_id -> emp_id"],
         0,
         "emp_id determines dept_name only through the middleman dept_id — "
         "the chain emp_id -> dept_id -> dept_name. emp_id -> dept_id alone "
         "is direct, not transitive.",
         ["tcs", "wipro"]),
    _mkq("dbms-m3-l5-q3", "dbms-m3-l5", "normalization", 5,
         "In the unnormalized Employees(emp_id, dept_id, dept_name) table, what anomaly does the "
         "transitive dependency cause?",
         ["Update anomaly — renaming a department means updating every employee row",
          "Insertion anomaly for new employees",
          "The table cannot have a primary key",
          "Queries become syntactically invalid"],
         0,
         "dept_name repeats once per employee: rename 'Engineering' and you "
         "must touch N rows — miss one and the database contradicts itself. "
         "It also blocks storing a department with no employees yet.",
         ["infosys", "accenture"]),
    _mkq("dbms-m3-l5-q4", "dbms-m3-l5", "normalization", 6,
         "Correct 3NF decomposition of Employees(emp_id, dept_id, dept_name)?",
         ["Employees(emp_id, dept_id) and Departments(dept_id, dept_name)",
          "Employees(emp_id, dept_name) and Departments(dept_id)",
          "Employees(emp_id) and Departments(dept_id, dept_name, emp_id)",
          "A single table with a composite key (emp_id, dept_id)"],
         0,
         "Each FD lives in its own table: emp_id->dept_id in Employees, "
         "dept_id->dept_name in Departments. The join on dept_id recovers the "
         "original — this is exactly the SQL module's schema.",
         ["amazon", "microsoft"]),
    _mkq("dbms-m3-l5-q5", "dbms-m3-l5", "normalization", 7,
         "After the 3NF decomposition, where is the FD dept_id -> dept_name enforced, "
         "and how do you get an employee's dept_name?",
         ["Enforced in Departments (dept_id is its key); recovered via JOIN on dept_id",
          "Enforced in Employees; no join needed",
          "Enforced by the application; the database cannot do it",
          "It is lost — decomposition destroys FDs"],
         0,
         "dept_id is the primary key of Departments, so the FD is enforced "
         "there by the key itself. The original view is rebuilt with a join "
         "— decomposition preserves both data and FDs.",
         ["google", "amazon"]),
    _mkq("dbms-m3-l5-q6", "dbms-m3-l5", "normalization", 8,
         "R(A, B, C) with FDs {A->B, B->C} and A as the key. What is the highest normal form of R?",
         ["2NF — the transitive chain A->B->C violates 3NF",
          "3NF",
          "BCNF",
          "1NF only"],
         0,
         "Key A is single-attribute so no partial dependency (2NF holds). But "
         "A->B->C is a transitive chain with B a non-superkey middleman — "
         "3NF fails. Highest = 2NF.",
         ["google", "microsoft", "amazon"]),
    # ---------------- dbms-m3-l6: BCNF ----------------
    _mkq("dbms-m3-l6-q1", "dbms-m3-l6", "normalization", 3,
         "What is the BCNF rule?",
         ["Every determinant (left side of every FD) must be a superkey",
          "Every table must have exactly one candidate key",
          "No FD may have more than one attribute on the left",
          "All non-key attributes must be mutually independent"],
         0,
         "BCNF: for every X -> Y, X must be a superkey — no exceptions. 3NF "
         "relaxes this when Y is a prime attribute; BCNF does not.",
         ["tcs", "infosys"]),
    _mkq("dbms-m3-l6-q2", "dbms-m3-l6", "normalization", 4,
         "Takes(student, course, instructor) with FDs (student, course)->instructor and "
         "instructor->course (each instructor teaches one course). Which FD violates BCNF?",
         ["instructor -> course, because instructor is not a superkey",
          "(student, course) -> instructor, because the left side is composite",
          "Both — composite left sides are banned in BCNF",
          "Neither — the table is in BCNF"],
         0,
         "instructor determines course but instructor alone does not identify "
         "a row (one instructor teaches many students), so it is a "
         "non-superkey determinant — the BCNF violation. Composite left "
         "sides are perfectly legal.",
         ["tcs", "wipro", "amazon"]),
    _mkq("dbms-m3-l6-q3", "dbms-m3-l6", "normalization", 5,
         "Why does the Takes table above still satisfy 3NF despite the BCNF violation?",
         ["All attributes are prime — each belongs to some candidate key",
          "3NF does not check functional dependencies",
          "The table has only three columns",
          "instructor -> course is a partial dependency, which 3NF allows"],
         0,
         "Candidate keys are (student, course) and (student, instructor), so "
         "every attribute is prime. 3NF permits a non-superkey determinant "
         "when the dependent is prime — BCNF's stricter rule is what fails.",
         ["infosys", "microsoft"]),
    _mkq("dbms-m3-l6-q4", "dbms-m3-l6", "normalization", 6,
         "Which anomaly survives in the 3NF-but-not-BCNF Takes table?",
         ["Insertion anomaly — a new instructor's course cannot be stored until they get a student",
          "The table cannot be queried with JOIN",
          "Primary key violation on every insert",
          "None — 3NF eliminates all anomalies"],
         0,
         "The instructor->course fact repeats per student row, so a new "
         "instructor has nowhere to live until enrolled with a student — the "
         "same insertion anomaly 3NF was supposed to kill. This gap is why "
         "BCNF exists.",
         ["amazon", "google"]),
    _mkq("dbms-m3-l6-q5", "dbms-m3-l6", "normalization", 7,
         "Correct BCNF decomposition of Takes(student, course, instructor)?",
         ["Teaching(instructor, course) and Enrollment(student, instructor)",
          "Teaching(student, course) and Enrollment(course, instructor)",
          "Teaching(instructor) and Enrollment(student, course)",
          "No decomposition is possible without losing information"],
         0,
         "Put the violating FD instructor->course in its own table with "
         "instructor as key; keep (student, instructor) to rejoin. Since "
         "instructor is a key of Teaching, the join is lossless and both "
         "FDs are preserved.",
         ["google", "microsoft"]),
    _mkq("dbms-m3-l6-q6", "dbms-m3-l6", "normalization", 8,
         "Which statement about BCNF and 3NF is TRUE?",
         ["Every BCNF table is in 3NF, but a 3NF table need not be in BCNF",
          "Every 3NF table is in BCNF, but not vice versa",
          "They are equivalent — just two names for one form",
          "BCNF is weaker than 3NF"],
         0,
         "BCNF's rule (every determinant a superkey) strictly implies 3NF's "
         "rule, so BCNF => 3NF. The Takes example is 3NF but not BCNF, "
         "proving the converse false.",
         ["microsoft", "google", "amazon"]),
    # ---------------- dbms-m3-l7: 4NF/5NF & Denormalization ----------------
    _mkq("dbms-m3-l7-q1", "dbms-m3-l7", "normalization", 3,
         "What is a multivalued dependency X ->-> Y?",
         ["Each X value is associated with a set of Y values, independently of the other attributes",
          "X determines exactly one Y value",
          "X and Y determine each other",
          "Y contains duplicate values for each X"],
         0,
         "MVDs are about independent sets: Aarav's skills {Java, Python} have "
         "nothing to do with his languages {Hindi, English} — yet the table "
         "stores their cross product. That independence is the ->-> "
         "signature.",
         ["tcs", "infosys"]),
    _mkq("dbms-m3-l7-q2", "dbms-m3-l7", "normalization", 4,
         "Aarav's 2 skills x 2 languages produce 4 rows. What is the problem, and what happens "
         "when he learns a 3rd language?",
         ["Cross-product redundancy — adding one language needs 2 new rows (one per skill)",
          "The table violates 1NF",
          "Queries on the table become impossible",
          "The primary key stops working"],
         0,
         "Independent multi-valued facts multiply: M skills x N languages = "
         "M*N rows. One new language must pair with every existing skill — "
         "pure redundancy with update-anomaly risk, all while in BCNF.",
         ["wipro", "accenture"]),
    _mkq("dbms-m3-l7-q3", "dbms-m3-l7", "normalization", 5,
         "What is the 4NF fix for the name/skill/language cross-product table?",
         ["Split into PersonSkills(name, skill) and PersonLanguages(name, language)",
          "Add a composite primary key (name, skill, language)",
          "Merge skill and language into one column",
          "Delete all but one row per person"],
         0,
         "Separate the independent facts: one row per skill, one row per "
         "language. Adding a language is now one row. 4NF = BCNF + no "
         "non-trivial multivalued dependencies.",
         ["tcs", "amazon"]),
    _mkq("dbms-m3-l7-q4", "dbms-m3-l7", "normalization", 6,
         "What is the idea behind 5NF (join dependency)?",
         ["A table that splits losslessly into 3+ tables (but no 2) should be split",
          "Tables must have at most 5 columns",
          "Every table needs 5 candidate keys",
          "Joins with more than 5 tables are forbidden"],
         0,
         "5NF handles the rare case where redundancy hides in a three-way "
         "split: the table decomposes losslessly into three projections but "
         "into no pair of them. Practically, you meet it when a 3+ way split "
         "kills redundancy.",
         ["infosys", "microsoft"]),
    _mkq("dbms-m3-l7-q5", "dbms-m3-l7", "normalization", 7,
         "When is denormalization the RIGHT call?",
         ["Read-heavy reporting where join/aggregation cost dominates and writes are rare",
          "Always — normalization is purely academic",
          "Never — it is always a design failure",
          "Only when the database has fewer than 100 rows"],
         0,
         "Denormalization trades write-safety for read-speed. When a query "
         "runs 10,000x/day and the underlying data barely changes, "
         "precomputing is engineering, not laziness — done consciously, with "
         "disciplined refresh.",
         ["amazon", "google"]),
    _mkq("dbms-m3-l7-q6", "dbms-m3-l7", "normalization", 8,
         "A dashboard shows department-wise headcount, queried 10,000x/day; departments change twice a year. "
         "Best design?",
         ["A denormalized headcount column/summary refreshed when departments change",
          "Fully normalized schema with the join + COUNT computed on every dashboard load",
          "Store headcount in the application code as a constant",
          "Delete the Departments table"],
         0,
         "The read/write ratio (~10,000:2/year) overwhelmingly favors "
         "precomputation: refresh the redundant count on the rare write, "
         "serve reads instantly. Normalizing first and denormalizing where "
         "measured is the professional sequence.",
         ["google", "microsoft", "amazon"]),
]
