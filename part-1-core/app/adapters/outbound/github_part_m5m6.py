"""Seed content: Git & GitHub curriculum — PART 3.

Modules 5 (Advanced Git) and 6 (GitHub Ecosystem). All theory is original
educational prose with real git/GitHub commands and flags — no invented
syntax. Each lesson carries exactly 6 MCQs with varied answer positions,
difficulty spread >= 4 within the lesson, and WHY-style explanations.

Exports a single variable: MODULES (list of 2 module dicts).
"""

MODULES = [
    {
        "slug": "git-advanced",
        "name": "Advanced Git",
        "description": (
            "Power-user Git: cherry-pick single commits, recover lost work "
            "with the reflog, bisect regressions, rewrite history safely "
            "with interactive rebase, automate with hooks, and manage "
            "submodules and worktrees."
        ),
        "lessons": [
            {
                "slug": "git-advanced-cherry-pick",
                "title": "Cherry-Picking Commits",
                "theory_md": """## Cherry-Picking Commits

Sometimes you need exactly **one commit** from another branch — not the whole
branch. A hotfix landed on `main` but your release branch needs it too; a
teammate's branch has one useful commit buried among experiments.
`git cherry-pick` copies a commit onto your current HEAD.

```bash
# find the commit you want on the other branch
git log --oneline feature/sso
# 9f3ac21 Add SAML callback validation

git checkout release/2.4
git cherry-pick 9f3ac21
```

Git replays the diff of `9f3ac21` on top of your branch and creates a **new
commit with a new SHA** — the parent and timestamp changed, so the hash must
change. The commit message is preserved.

### Useful flags

- `git cherry-pick -x 9f3ac21` — appends `(cherry picked from commit
  9f3ac21...)` to the message. Use it: six months later, `git log` tells you
  exactly where the backport came from.
- `git cherry-pick -n 9f3ac21` (`--no-commit`) — applies the changes to your
  working tree without committing, so you can inspect or combine them first.
- Ranges: `git cherry-pick a1b2c3d..f9e8d7c` copies everything *after*
  `a1b2c3d` up to and including `f9e8d7c`. To include the start commit, use
  the caret: `a1b2c3d^..f9e8d7c`.
- Multiple commits at once: `git cherry-pick a1b2c3d d4e5f6a`.

### Merge commits need `-m`

A merge commit has two parents, so git doesn't know which diff to replay.
`-m 1` says "diff against the first parent (the branch you merged into)":

```bash
git cherry-pick -m 1 7d2e9aa
```

### When it conflicts

Cherry-pick pauses, exactly like a merge. Resolve the files, stage them, then:

```bash
git cherry-pick --continue   # finish the pick
git cherry-pick --abort      # give up, restore the pre-pick state
```

**Rule of thumb:** cherry-pick is for *exceptions* — one-off backports. If you
find yourself cherry-picking whole branches regularly, your branching strategy
needs fixing, not your git commands.
""",
                "difficulty_min": 4,
                "difficulty_max": 9,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "You are on `release/2.4` and run `git cherry-pick 9f3ac21`. What happens?",
                        "choices": [
                            "Commit 9f3ac21 is deleted from its original branch",
                            "The changes from 9f3ac21 are replayed as a new commit on release/2.4",
                            "The entire branch containing 9f3ac21 is merged into release/2.4",
                            "Commit 9f3ac21 is reverted on release/2.4",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "Cherry-pick copies the diff, not the commit object. The original commit stays untouched on its branch; you get a brand-new commit (with a new SHA) carrying the same changes and message on your current branch.",
                        "company_tags": ["google", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why does a cherry-picked commit get a NEW SHA instead of keeping the original?",
                        "choices": [
                            "Git compresses the diff, which changes the hash",
                            "The author name is replaced with yours",
                            "Cherry-pick always rebases onto main first",
                            "The parent commit and timestamp differ, and the SHA hashes those",
                        ],
                        "answer_index": 3,
                        "difficulty": 6,
                        "explanation": "A commit's SHA is a hash of its content, parents, author, and timestamp. Since the cherry-picked commit has a different parent (your branch tip) and a new timestamp, the hash must change — same changes, different identity.",
                        "company_tags": ["amazon", "atlassian"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does `git cherry-pick -x 9f3ac21` add compared to a plain cherry-pick?",
                        "choices": [
                            "A '(cherry picked from commit 9f3ac21...)' trailer in the commit message",
                            "The original author's GPG signature to the new commit",
                            "An extra parent pointer to the original commit",
                            "A tag named after the original commit",
                        ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "The -x flag records provenance in the message. Months later, `git log` shows exactly which upstream commit a backport came from, making audits and duplicate-fix detection far easier.",
                        "company_tags": ["microsoft", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does `git cherry-pick a1b2c3d..f9e8d7c` copy?",
                        "choices": [
                            "Only the two endpoint commits a1b2c3d and f9e8d7c",
                            "Every commit from a1b2c3d through f9e8d7c, inclusive",
                            "Every commit after a1b2c3d up to and including f9e8d7c",
                            "Every commit reachable from f9e8d7c but not from main",
                        ],
                        "answer_index": 2,
                        "difficulty": 8,
                        "explanation": "The `A..B` range means 'reachable from B, excluding A and its ancestors' — so A itself is excluded. To include A, write `A^..B`. This matches exactly how `git log A..B` works.",
                        "company_tags": ["google", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Mid-cherry-pick, git stops with a conflict. After editing the files, what finishes the operation?",
                        "choices": [
                            "`git commit` — the pick is already staged",
                            "`git cherry-pick --skip` to accept the conflict markers",
                            "`git rebase --continue`",
                            "`git add <files>` then `git cherry-pick --continue`",
                        ],
                        "answer_index": 3,
                        "difficulty": 7,
                        "explanation": "Like a merge, cherry-pick pauses and waits for you. Marking files resolved with `git add` tells git the conflict is handled; `--continue` then completes the new commit. `--skip` would drop the commit entirely — wrong when you want its changes.",
                        "company_tags": ["atlassian", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You need to cherry-pick merge commit 7d2e9aa. Which command is correct?",
                        "choices": [
                            "`git cherry-pick 7d2e9aa` — git picks the larger parent automatically",
                            "`git cherry-pick -m 1 7d2e9aa` to diff against the first parent",
                            "`git cherry-pick --mainline 7d2e9aa`",
                            "Merge commits cannot be cherry-picked; use `git merge` instead",
                        ],
                        "answer_index": 1,
                        "difficulty": 9,
                        "explanation": "A merge has two parents, so git can't know which diff to replay. `-m 1` selects the first parent (the branch you were on when you merged) as the baseline, replaying 'what the merged branch introduced.' Merge commits absolutely can be cherry-picked.",
                        "company_tags": ["google", "microsoft"],
                    },
                ],
            },
            {
                "slug": "git-advanced-reflog",
                "title": "Recovering Lost Commits with the Reflog",
                "theory_md": """## The Reflog: Git's Safety Net

Git almost never truly deletes commits right away. Every time a reference
moves — `HEAD`, a branch tip — git appends an entry to the **reflog**
(reference log). It's a private, local diary of where your refs have been.

```bash
git reflog
# d4e5f6a HEAD@{0}: reset: moving to HEAD~3
# 9f3ac21 HEAD@{1}: commit: Add SAML callback validation
```

### The classic disaster: `git reset --hard` gone wrong

You meant `HEAD~1`, typed `HEAD~5`, and five commits vanished from your branch.
They're not gone — the reflog still points at them:

```bash
git reflog                    # find the SHA from before the reset
git branch rescue 9f3ac21     # resurrect it as a branch — nothing lost
```

Or jump straight back in one move:

```bash
git reset --hard HEAD@{1}     # HEAD@{1} = where HEAD was one move ago
```

### Deleted a branch by accident?

```bash
git branch -D feature/sso          # oops
git reflog                         # find its last commit SHA
git branch feature/sso 9f3ac21     # branch reborn, history intact
```

### Reading the reflog

- `git reflog --date=iso` — human-readable timestamps.
- `git reflog show main` — the log for one specific ref.
- `HEAD@{yesterday}`, `main@{2.days.ago}` — time-based shortcuts.
- `git log -g` — same data in `git log` format.

### Limits you must know

1. **Local only.** The reflog is never pushed, fetched, or cloned. It can't
   save a teammate's repo — or a fresh clone of your own.
2. **It expires.** Unreachable entries are garbage-collected after ~30 days
   (reachable ones after ~90). Recovery is a "sooner is better" operation.
3. **It only tracks commits.** Uncommitted working-tree changes wiped by
   `reset --hard` were never objects in git's database — the reflog has no SHA
   to point at, so it can't bring them back. (Commit early, commit often.)

One more safety net: if the commit was ever **pushed**, the remote still has
it — `git fetch origin` plus the reflog of `origin/main` can save you.
""",
                "difficulty_min": 4,
                "difficulty_max": 9,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "What does `git reflog` show?",
                        "choices": [
                            "All commits ever pushed to the remote",
                            "A graph of every branch in the repository",
                            "A local log of every movement of HEAD and branch tips",
                            "The diff of the most recent commit",
                        ],
                        "answer_index": 2,
                        "difficulty": 4,
                        "explanation": "The reflog is a private diary: each entry records 'ref X moved from SHA-old to SHA-new' with the action (commit, reset, checkout). It's how git remembers history that no branch points to anymore.",
                        "company_tags": ["amazon", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You ran `git reset --hard HEAD~5` by mistake and lost commits. What is the correct FIRST step?",
                        "choices": [
                            "Run `git reflog` to find the SHA from before the reset",
                            "Run `git pull` to restore the commits from the remote",
                            "Run `git stash pop` to recover the lost work",
                            "Re-create the commits manually — reset --hard is irreversible",
                        ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "The commits still exist as objects; only the branch pointer moved. The reflog shows exactly where HEAD was before the reset, giving you the SHA to restore from. Pull and stash are irrelevant here.",
                        "company_tags": ["microsoft", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does `git reset --hard HEAD@{1}` do?",
                        "choices": [
                            "Deletes the most recent commit permanently",
                            "Moves HEAD (and the branch) back to where it was one reflog entry ago",
                            "Shows a diff between the last two reflog entries",
                            "Creates a backup branch named HEAD@{1}",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "`HEAD@{n}` addresses the reflog by position: `@{0}` is now, `@{1}` is one move ago. If your last move was the bad reset, this single command undoes it — no SHA hunting required.",
                        "company_tags": ["google", "atlassian"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You deleted branch `feature/sso` with `git branch -D`, but it had unmerged commits. How do you resurrect it?",
                        "choices": [
                            "`git checkout -b feature/sso` — git remembers deleted branches",
                            "`git revert` the deletion commit",
                            "`git branch --restore feature/sso`",
                            "Find its tip SHA in `git reflog`, then `git branch feature/sso <sha>`",
                        ],
                        "answer_index": 3,
                        "difficulty": 6,
                        "explanation": "`-D` only deletes the pointer; the commits remain until garbage collection. The reflog entry for the branch's last checkout gives you the tip SHA, and `git branch <name> <sha>` recreates the pointer exactly.",
                        "company_tags": ["amazon", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why can't the reflog recover uncommitted changes wiped by `git reset --hard`?",
                        "choices": [
                            "Because reflog only works on pushed branches",
                            "Because --hard also wipes the reflog",
                            "Because uncommitted changes were never stored as git objects, so there's no SHA to point at",
                            "Because the reflog expires after 24 hours",
                        ],
                        "answer_index": 2,
                        "difficulty": 8,
                        "explanation": "The reflog records movements between commits (object SHAs). Working-tree edits that were never committed or stashed exist only as files; once overwritten, git has no snapshot to restore. This is why 'commit early, commit often' is real advice.",
                        "company_tags": ["microsoft", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which TWO limitations of reflog-based recovery matter most?",
                        "choices": [
                            "It's local-only (never cloned/pushed) and entries expire via garbage collection",
                            "It requires admin rights and only works on main",
                            "It can't track merges and stops at 100 entries",
                            "It only works with GitHub Desktop, not the CLI",
                        ],
                        "answer_index": 0,
                        "difficulty": 9,
                        "explanation": "Because the reflog lives in `.git/logs` locally, no teammate or fresh clone can see it — and unreachable entries are pruned after ~30 days. So recovery is a race against the clock on the same machine. Pushed commits are the real backup.",
                        "company_tags": ["atlassian", "amazon"],
                    },
                ],
            },
            {
                "slug": "git-advanced-bisect",
                "title": "Finding Bugs with git bisect",
                "theory_md": """## git bisect: Binary-Search Your Bugs

A feature worked in v2.3 and is broken now, with 400 commits in between.
Reading them one by one is hopeless — `git bisect` turns the hunt into a
**binary search**, cutting the suspect range in half at each step.

```bash
git bisect start
git bisect bad                  # current checkout is broken
git bisect good v2.3.0           # last known-good commit/tag

# git checks out a commit halfway between the two
# ... you test it ...
git bisect good                 # this one works -> bug is newer
# git checks out the new midpoint
# ... you test it ...
git bisect bad                  # this one is broken -> bug is older
# ... repeat until git names a single commit:
# "9f3ac21 is the first bad commit"

git bisect reset                 # back to where you started
```

With 400 commits you test ~9 times (log2); with 4,000, ~12. The cost grows
**logarithmically**, not linearly — that's the whole point.

### Automate it: `git bisect run`

If you have a script that reproduces the bug, let git drive:

```bash
git bisect start
git bisect bad HEAD
git bisect good v2.3.0
git bisect run ./repro.sh
git bisect reset
```

Exit-code contract for your script: **0 = good**, **1-124 (except 125) = bad**,
**125 = skip** this commit (can't build or test it — try its neighbors).

### Survival tips

- `git bisect skip` — manually skip an untestable commit.
- `git bisect log > bisect.log` saves the session;
  `git bisect replay bisect.log` restores it (handy when the run crashes
  overnight).
- Test the **same thing** at every step — a flaky check poisons the search.
- **Always finish with `git bisect reset`**, or you'll stay parked on a
  detached HEAD in the middle of history wondering where your branch went.

Bisect shines on regressions ("it used to work"). For brand-new features that
never worked, it still applies as long as you can define good vs. bad at some
earlier commit — often the commit right before the feature landed.
""",
                "difficulty_min": 4,
                "difficulty_max": 9,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "What problem is `git bisect` designed to solve?",
                        "choices": [
                            "Merging two branches with thousands of conflicts",
                            "Splitting one large commit into smaller ones",
                            "Rewriting commit messages across history",
                            "Finding which commit introduced a regression, using binary search",
                        ],
                        "answer_index": 3,
                        "difficulty": 4,
                        "explanation": "Given a known-good and a known-bad commit, bisect repeatedly checks out the midpoint and asks you to label it good/bad, halving the suspect range each time until exactly one commit remains: the culprit.",
                        "company_tags": ["google", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A bug appeared somewhere in ~1000 commits. Roughly how many test rounds does bisect need?",
                        "choices": [
                            "About 1000 — it checks each commit once",
                            "About 10 — it halves the range each round",
                            "About 500 — it checks every other commit",
                            "Exactly 2 — one for good, one for bad",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "Binary search needs log2(n) steps: log2(1000) is about 10. That's the entire value proposition — debugging effort grows logarithmically with history size instead of linearly.",
                        "company_tags": ["amazon", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "In `git bisect run ./repro.sh`, what does an exit code of 0 mean?",
                        "choices": [
                            "The checked-out commit is GOOD (bug not present)",
                            "The checked-out commit is BAD (bug present)",
                            "The script crashed — bisect aborts",
                            "Skip this commit and try a neighbor",
                        ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "The contract is: 0 = good, 1-124 (except 125) = bad, 125 = skip. Your repro script must be deterministic and follow this convention, or the search gets poisoned with wrong labels.",
                        "company_tags": ["microsoft", "atlassian"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Bisect has identified the culprit commit. What returns your repo to normal?",
                        "choices": [
                            "`git checkout main` — bisect cleans up automatically",
                            "`git bisect good` one final time",
                            "`git bisect reset`",
                            "`git bisect stop`",
                        ],
                        "answer_index": 2,
                        "difficulty": 7,
                        "explanation": "During bisect you're on a detached HEAD hopping between midpoints. `reset` ends the session and returns you to the branch/commit where you started. Forgetting it leaves you stranded mid-history — a classic beginner trap.",
                        "company_tags": ["flipkart", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why does `git bisect start` require you to mark BOTH a good and a bad commit?",
                        "choices": [
                            "Git needs two commits to create a merge base",
                            "Binary search needs both bounds to know where to halve the range",
                            "The good commit becomes the fix; the bad one is deleted",
                            "It's optional — bisect works fine with only a bad commit",
                        ],
                        "answer_index": 1,
                        "difficulty": 8,
                        "explanation": "Without a known-good lower bound, git can't compute a midpoint — the range is unbounded. The good/bad pair defines the search interval; every verdict then discards half of it.",
                        "company_tags": ["google", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "During `git bisect run`, your script exits 125 on a commit that fails to build. What does bisect do?",
                        "choices": [
                            "Treats it as bad and continues",
                            "Aborts the entire session",
                            "Marks it good and moves on",
                            "Skips it and tests a neighboring commit instead",
                        ],
                        "answer_index": 3,
                        "difficulty": 9,
                        "explanation": "125 is the 'untestable' signal. Bisect picks an adjacent commit rather than guessing good/bad, because a wrong label would corrupt the binary search. Use `git bisect skip` for the manual equivalent.",
                        "company_tags": ["microsoft", "google"],
                    },
                ],
            },
            {
                "slug": "git-advanced-interactive-rebase",
                "title": "Interactive Rebase: Reword, Squash, Drop",
                "theory_md": """## Interactive Rebase: Editing History Before You Share It

`git rebase -i` opens your recent commits in an editor and lets you rewrite
them: fix messages, squash fixups, drop mistakes, reorder. The golden rule:
**only rewrite history that exists solely on your machine** — never commits
others have already pulled.

```bash
git rebase -i HEAD~3
```

```
pick a1b2c3d Add login form
pick d4e5f6a Fix typo in login form
pick f9e8d7c Add login tests
```

Change the verbs, save, and git replays the list:

- **pick** — keep as-is.
- **reword** — keep the changes, edit the message (typos, missing ticket IDs).
- **edit** — stop at this commit so you can amend it (`git commit --amend`),
  then `git rebase --continue`.
- **squash** — meld into the previous commit, combining messages (goodbye,
  fourteen "wip" commits).
- **fixup** — like squash, but **discards** this commit's message. Perfect for
  "oops, forgot a file" commits.
- **drop** — remove the commit entirely.

Squash example — fold the typo fix into the original commit:

```
pick a1b2c3d Add login form
fixup d4e5f6a Fix typo in login form
pick f9e8d7c Add login tests
```

### Reordering

Just move the lines. Want tests first? Move the line. (Conflicts may appear if
the new order doesn't apply cleanly — resolve, `git add`,
`git rebase --continue`.)

### The force-push question

Rewriting history changes SHAs, so pushing needs a force. On *your own* PR
branch, use the safe variant:

```bash
git push --force-with-lease
```

Unlike `--force`, it refuses if someone else pushed since your last fetch — it
won't silently nuke a teammate's work. Never force-push `main`.

### Autosquash shortcut

```bash
git commit --fixup=a1b2c3d          # mark a fix for a specific commit
git rebase -i --autosquash HEAD~3  # git pre-arranges the fixup lines
```

Clean history isn't vanity — `git log`, `git blame`, and `git bisect` all get
dramatically more useful when each commit is one logical change with a clear
message.
""",
                "difficulty_min": 4,
                "difficulty_max": 9,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "What does `git rebase -i HEAD~3` do?",
                        "choices": [
                            "Opens the last 3 commits in an editor so you can reorder, edit, squash, or drop them",
                            "Merges the last 3 commits into one immediately",
                            "Shows an interactive diff of the last 3 commits",
                            "Reverts the last 3 commits one by one",
                        ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "The -i flag lists the commits as `pick` lines; you rewrite the verbs (reword/squash/fixup/drop) and reorder lines, and git replays history according to your script. Nothing happens until you save and exit the editor.",
                        "company_tags": ["google", "atlassian"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What is the difference between `squash` and `fixup` in an interactive rebase?",
                        "choices": [
                            "squash deletes the commit; fixup keeps it",
                            "There is no difference — they are aliases",
                            "Both meld into the previous commit, but fixup discards the commit's message",
                            "fixup works only on merge commits",
                        ],
                        "answer_index": 2,
                        "difficulty": 4,
                        "explanation": "Use squash when both messages deserve preserving (you'll get a combined-message editor); use fixup for trivial follow-ups ('forgot a file', 'typo') whose messages add noise. Both produce one resulting commit.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why should you never rebase commits that teammates have already pulled?",
                        "choices": [
                            "Rebase is slower on shared branches",
                            "It rewrites SHAs, so teammates' histories diverge and merging becomes painful",
                            "GitHub blocks all rebases on shared branches",
                            "Rebased commits lose their author information",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "Rebase creates brand-new commit objects. Your teammates still have the old SHAs; when they pull, git sees two divergent histories with 'the same' changes and forces everyone into conflict resolution. Rewrite only private history.",
                        "company_tags": ["microsoft", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You only want to fix a typo in an old commit's message. Which verb do you use?",
                        "choices": [
                            "edit",
                            "squash",
                            "drop",
                            "reword",
                        ],
                        "answer_index": 3,
                        "difficulty": 6,
                        "explanation": "`reword` keeps the commit's changes byte-identical and just reopens the message editor. `edit` would stop for a full amend (overkill); squash/drop change the commit set itself.",
                        "company_tags": ["zoho", "atlassian"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A conflict appears during `git rebase -i`. After resolving the files, what continues the rebase?",
                        "choices": [
                            "`git add <files>` then `git rebase --continue`",
                            "`git commit` then `git rebase --next`",
                            "`git cherry-pick --continue`",
                            "`git rebase --skip` to keep the conflict markers",
                        ],
                        "answer_index": 0,
                        "difficulty": 8,
                        "explanation": "Rebase pauses at each conflicting commit like a checkpoint. Staging the resolutions and running `--continue` replays the commit and moves to the next step. `--skip` would drop the commit — only right if its changes are truly unwanted.",
                        "company_tags": ["google", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You must push rewritten history on your own PR branch. Why prefer `--force-with-lease` over `--force`?",
                        "choices": [
                            "It's faster on large repositories",
                            "It works without write access to the branch",
                            "It refuses if the remote moved since you last fetched, so you can't silently overwrite a teammate's push",
                            "It preserves the original commit SHAs",
                        ],
                        "answer_index": 2,
                        "difficulty": 9,
                        "explanation": "`--force` blindly replaces the remote ref. The lease variant compares against your last-known remote state and aborts on mismatch — a safety net for the common case where someone pushed to your PR branch while you were rebasing.",
                        "company_tags": ["microsoft", "atlassian"],
                    },
                ],
            },
            {
                "slug": "git-advanced-hooks",
                "title": "Git Hooks: Automating pre-commit and pre-push",
                "theory_md": """## Git Hooks: Automation That Runs Itself

Hooks are scripts git executes automatically at certain events. They live in
`.git/hooks/` — `pre-commit`, `pre-push`, `post-commit`, and more. A hook that
exits **non-zero blocks** the operation; zero lets it through.

```bash
ls .git/hooks/
# pre-commit.sample  pre-push.sample  commit-msg.sample  ...
```

### Anatomy of a hook

Hooks are plain executables — any language, no file extension:

```bash
cp .git/hooks/pre-commit.sample .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit   # the executable bit is what activates it
```

A real pre-commit hook that refuses lint failures:

```bash
#!/bin/sh
# .git/hooks/pre-commit
npm run lint --silent
if [ $? -ne 0 ]; then
  echo "Lint failed - commit blocked. Fix it or bypass with --no-verify."
  exit 1
fi
```

### The two workhorses

- **pre-commit** — fast checks: formatting, lint, no leftover `console.log` /
  debugger statements, no secrets sneaking into the diff. Keep it under a few
  seconds or developers will hate it.
- **pre-push** — the heavier gate: run the test suite before code leaves your
  machine.

```bash
#!/bin/sh
# .git/hooks/pre-push
npm test --silent || { echo "Tests failed - push blocked."; exit 1; }
```

### Escape hatch and limits

- `git commit --no-verify` / `git push --no-verify` skips the hooks.
  Legitimate for emergencies — suspicious as a habit.
- **Hooks are not cloned.** A fresh `git clone` gets sample files only; every
  developer must install them. Teams solve this by committing hook
  *definitions* and installing via tools like Husky (npm) or the `pre-commit`
  framework, wired into `package.json` / `.pre-commit-config.yaml`.
- Server-side enforcement on GitHub uses **branch protection + Actions**, not
  client hooks — because client hooks can always be bypassed.

### Hook design economics

Fast checks in pre-commit (they run constantly), slow suites in pre-push (they
run rarely but still gate what others see). A 5-minute pre-commit trains
developers to `--no-verify` everything — and then you have no gate at all.
""",
                "difficulty_min": 4,
                "difficulty_max": 9,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Where do git hooks live, and what activates them?",
                        "choices": [
                            "In `.github/hooks/`; they run on every push to GitHub",
                            "In `.git/hooks/` as executable files named after the event (e.g. `pre-commit`)",
                            "In `/etc/git-hooks/`; they require root to install",
                            "In the repo root as `.githooks/` YAML files",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "Git looks for an executable file matching the event name in `.git/hooks/`. The sample files ending in `.sample` are inert templates — the executable bit plus the exact name is what makes a hook live.",
                        "company_tags": ["amazon", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "How does a `pre-commit` hook BLOCK a commit?",
                        "choices": [
                            "By exiting with a non-zero status code",
                            "By deleting the staged files",
                            "By printing the word BLOCK to stdout",
                            "By opening an editor asking for confirmation",
                        ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "The contract is purely the exit code: 0 = allow, anything else = abort the operation. That's why hook scripts end with explicit `exit 1` on failure — output text is just for the human.",
                        "company_tags": ["microsoft", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You wrote `.git/hooks/pre-commit` but it never runs. What's the most likely cause?",
                        "choices": [
                            "Hooks only run on the main branch",
                            "The repo needs `git hooks --enable` first",
                            "pre-commit is deprecated in favor of pre-push",
                            "The file isn't executable — it needs `chmod +x`",
                        ],
                        "answer_index": 3,
                        "difficulty": 6,
                        "explanation": "Git silently ignores non-executable hook files. This is the number-one hook debugging answer: the script is perfect, but without the executable bit git treats it as absent.",
                        "company_tags": ["flipkart", "atlassian"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why can't client-side hooks be your team's ONLY quality gate?",
                        "choices": [
                            "They slow down clones too much",
                            "They don't work on Windows",
                            "They aren't cloned — each developer must install them, and `--no-verify` bypasses them",
                            "GitHub deletes custom hooks on push",
                        ],
                        "answer_index": 2,
                        "difficulty": 7,
                        "explanation": "Hooks live in `.git/`, which is never pushed. A developer with a fresh clone has no hooks until something installs them, and anyone can bypass with `--no-verify`. Real enforcement belongs server-side: branch protection + CI.",
                        "company_tags": ["google", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does `git commit --no-verify` do?",
                        "choices": [
                            "Commits without running `git status` first",
                            "Skips the pre-commit (and commit-msg) hooks",
                            "Disables GPG signing for this commit",
                            "Commits directly to the remote, skipping local checks",
                        ],
                        "answer_index": 1,
                        "difficulty": 8,
                        "explanation": "It's the escape hatch for emergencies ('production is down, the linter config is broken'). Useful rarely; if your team uses it daily, the hook is miscalibrated — probably too slow or too flaky.",
                        "company_tags": ["microsoft", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Where should a 5-minute test suite run — pre-commit or pre-push — and why?",
                        "choices": [
                            "pre-push: keeps every commit fast while still stopping broken code from leaving the machine",
                            "pre-commit: tests must run before code is even committed",
                            "post-commit: so it doesn't block anything",
                            "Neither — hooks can't run test suites",
                        ],
                        "answer_index": 0,
                        "difficulty": 9,
                        "explanation": "Hook design is about feedback-loop economics. Fast checks (lint, format) belong in pre-commit where they run constantly; slow suites belong in pre-push where they run rarely but still gate what others see. A 5-minute pre-commit trains developers to `--no-verify` everything.",
                        "company_tags": ["atlassian", "amazon"],
                    },
                ],
            },
            {
                "slug": "git-advanced-submodules-worktrees",
                "title": "Submodules, Subtrees & Worktrees",
                "theory_md": """## Submodules, Subtrees & Worktrees

### Submodules: a repo inside your repo

When your project depends on another repository (a shared library, a theme),
a submodule pins it to an exact commit:

```bash
git submodule add https://github.com/org/shared-lib.git vendor/shared-lib
git commit -m "Add shared-lib submodule"
```

Your repo stores a **gitlink** — just the child repo's SHA, not its files.
Cloning needs an extra step because the contents aren't fetched by default:

```bash
git clone --recurse-submodules <url>      # clone with submodules populated
# or, after a plain clone:
git submodule update --init --recursive
```

Updating the pin: `cd` into the submodule, check out the version you want,
then commit the changed gitlink in the parent:

```bash
cd vendor/shared-lib && git checkout v2.1 && cd ../..
git add vendor/shared-lib
git commit -m "Bump shared-lib to v2.1"
```

Gotcha: collaborators must remember `--recurse-submodules` on pull too
(`git pull --recurse-submodules`), or the submodule silently stays stale.

### Subtrees: merge it in instead

`git subtree` merges the other repo's history *into* yours under a directory:

```bash
git subtree add --prefix=vendor/shared-lib \\
  https://github.com/org/shared-lib.git main --squash
```

Trade-off: **submodules** keep histories separate and the pin explicit, but
everyone must learn the submodule dance. **Subtrees** give contributors one
normal repo, at the cost of a noisier history and trickier upstream sync
(`git subtree pull`).

### Worktrees: two branches, zero stashing

A worktree is a second working tree attached to the same `.git` — a different
branch, no stash dance:

```bash
git worktree add ../hotfix main   # new directory, on branch main
cd ../hotfix                       # fix the production bug here
# ... your feature branch stays untouched in the original dir ...
git worktree list
git worktree remove ../hotfix     # clean up when done
```

Your half-finished feature keeps its uncommitted changes exactly where they
were. If you ever delete the folder manually instead, `git worktree prune`
cleans up git's bookkeeping so the path can be reused.
""",
                "difficulty_min": 4,
                "difficulty_max": 9,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "After `git submodule add <url> vendor/lib`, what does your repo actually record?",
                        "choices": [
                            "A full copy of the library's files at that moment",
                            "The library's URL; the commit is resolved at clone time",
                            "A gitlink — the exact commit SHA of the submodule",
                            "A zip archive of the submodule's main branch",
                        ],
                        "answer_index": 2,
                        "difficulty": 5,
                        "explanation": "The parent stores only a pointer (gitlink) to a specific child commit. That's why submodules give reproducible builds — the pin is exact — and why updating means committing a new pointer.",
                        "company_tags": ["google", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You cloned a repo and the submodule directory is empty. What populates it?",
                        "choices": [
                            "`git pull --all`",
                            "`git submodule add` again with the same URL",
                            "`git fetch --recurse-submodules`",
                            "`git submodule update --init --recursive`",
                        ],
                        "answer_index": 3,
                        "difficulty": 6,
                        "explanation": "A plain clone fetches the gitlinks but not the submodule contents. `update --init --recursive` clones each submodule at its pinned SHA (recursively for nested ones). `clone --recurse-submodules` does this in one step for fresh clones.",
                        "company_tags": ["amazon", "atlassian"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What is a git worktree?",
                        "choices": [
                            "A backup copy of the `.git` directory",
                            "An additional working tree attached to the same repo, checked out on a different branch",
                            "A GUI tool for visualizing branches",
                            "A temporary branch that auto-deletes after merging",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "`git worktree add ../hotfix main` gives you a second directory on another branch sharing one object database. Two branches, both with live working trees, zero stashing — ideal for urgent hotfixes mid-feature.",
                        "company_tags": ["flipkart", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What is the key trade-off between submodules and subtrees?",
                        "choices": [
                            "Submodules keep the child history separate and pinned; subtrees merge it into your history",
                            "Submodules are faster; subtrees are slower",
                            "Subtrees require a paid GitHub plan",
                            "Submodules work only with public repos",
                        ],
                        "answer_index": 0,
                        "difficulty": 7,
                        "explanation": "Submodules = exact pins, separate histories, but every collaborator must learn the submodule commands. Subtrees = one normal repo for contributors, but the merged history is noisier and syncing upstream (`subtree pull`) is fiddlier.",
                        "company_tags": ["google", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why use a worktree instead of `git stash` when a hotfix interrupts your feature work?",
                        "choices": [
                            "Stash doesn't work with untracked files",
                            "Worktrees are faster than stashing",
                            "Stash requires a commit first",
                            "Both branches keep live working trees — no stash/unstash cycle and no risk of stash conflicts",
                        ],
                        "answer_index": 3,
                        "difficulty": 8,
                        "explanation": "Stash is a stack you must remember to pop, and popping onto changed files can conflict. A worktree sidesteps the problem entirely: the feature's dirty state sits undisturbed in its own directory while you fix production in another.",
                        "company_tags": ["microsoft", "atlassian"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You deleted a worktree's folder with `rm -rf` instead of `git worktree remove`. What cleans up git's stale metadata?",
                        "choices": [
                            "`git worktree remove --force`",
                            "`git gc` — it detects missing worktrees automatically",
                            "`git worktree prune`",
                            "Nothing — the metadata is harmless and permanent",
                        ],
                        "answer_index": 2,
                        "difficulty": 9,
                        "explanation": "Git tracks worktrees in `.git/worktrees/`; a manually deleted folder leaves a stale entry that blocks re-adding the same path. `prune` scans for missing directories and removes their bookkeeping. (`remove` would have done both steps.)",
                        "company_tags": ["google", "zoho"],
                    },
                ],
            },
        ],
    },
    {
        "slug": "github-ecosystem",
        "name": "GitHub Ecosystem",
        "description": (
            "Go beyond the CLI: ship static sites with Pages, develop in "
            "cloud Codespaces, pair-program with Copilot, run teamwork with "
            "Projects and automation, and lock repos down with Dependabot, "
            "secret scanning, and code scanning."
        ),
        "lessons": [
            {
                "slug": "github-ecosystem-pages",
                "title": "GitHub Pages: Free Static Site Hosting",
                "theory_md": """## GitHub Pages: Free Hosting for Static Sites

GitHub Pages turns a repository into a live website — free, with HTTPS.
Perfect for portfolios, project docs, and landing pages. Two deployment modes:

**1. Deploy from a branch** — Settings → Pages → pick a branch (`main`) and a
folder (`/` or `/docs`). Push, and your site is live at
`https://<user>.github.io/<repo>/` (or `<user>.github.io` for a repo named
`<user>.github.io`).

**2. GitHub Actions** — full control: build with any static generator, then
deploy:

```yaml
# .github/workflows/pages.yml (essentials)
- run: npm run build        # your framework: React, Astro, Hugo...
- uses: actions/upload-pages-artifact@v3
  with: { path: ./dist }
- uses: actions/deploy-pages@v4
```

### Custom domains

Add a `CNAME` file with your domain at the site root (or set it in
Settings → Pages), then point DNS at GitHub:

```
# CNAME file content:
www.mohitbaghel.dev
```

- Apex domain → A records to GitHub's IPs; subdomain → CNAME to
  `<user>.github.io`.
- Tick **Enforce HTTPS** — GitHub provisions the certificate automatically.

### Know the limits

- **Static only** — no server code, no databases, no secrets. Need a backend?
  Pair Pages with serverless APIs; the frontend just calls them.
- Public repos: free and unlimited. Private repos: Pages needs Pro/Team+.
- Jekyll builds in automatically on branch mode; everything else goes through
  Actions.
- Watch the **base path**: project sites are served under `/<repo>/`, so
  absolute `/assets/...` URLs break — set your framework's base (e.g. Vite's
  `base: '/<repo>/'`) or use relative paths.
""",
                "difficulty_min": 4,
                "difficulty_max": 9,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "How do you publish a static site with GitHub Pages' branch mode?",
                        "choices": [
                            "Push to any branch — Pages auto-detects index.html",
                            "Run `gh pages deploy` from the CLI",
                            "Email GitHub support with the repo URL",
                            "Settings → Pages → select branch and folder, then push",
                        ],
                        "answer_index": 3,
                        "difficulty": 4,
                        "explanation": "Pages serves whatever static files are in the chosen branch/folder. The setting is per-repo under Settings → Pages; after pushing, the site appears at `<user>.github.io/<repo>/` within a minute or two.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your repo is `mohit/portfolio`. What URL will Pages serve it at?",
                        "choices": [
                            "`portfolio.github.io/mohit/`",
                            "`mohit.github.io/portfolio/`",
                            "`github.io/mohit/portfolio/`",
                            "`mohit.github.io/` — the repo name is ignored",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "Project sites live under `<user>.github.io/<repo>/`. Only a repo literally named `<user>.github.io` gets the bare domain — that's the special 'user site' case.",
                        "company_tags": ["zoho", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "How do you point a custom domain at your Pages site?",
                        "choices": [
                            "Add an `A` record to your repo's README",
                            "Rename the repo to the domain name",
                            "Add a `CNAME` file with the domain and point DNS at GitHub",
                            "Custom domains require GitHub Enterprise",
                        ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "The CNAME file (or the Settings → Pages field) tells GitHub which Host header to expect; your DNS (CNAME to `<user>.github.io` for subdomains, A records for apex) routes traffic there. Then 'Enforce HTTPS' gets you a free certificate.",
                        "company_tags": ["microsoft", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "When should you choose the GitHub Actions Pages mode over branch mode?",
                        "choices": [
                            "When you need a build step — e.g. React/Astro/Hugo generating the static files",
                            "When the site has more than 10 pages",
                            "When you want the site to be private",
                            "Actions mode is deprecated — always use branch mode",
                        ],
                        "answer_index": 0,
                        "difficulty": 7,
                        "explanation": "Branch mode serves files as-is (plus built-in Jekyll). Anything needing `npm run build` must build in Actions first, then deploy the artifact with `upload-pages-artifact` + `deploy-pages`. That's the modern, flexible path.",
                        "company_tags": ["google", "atlassian"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which of these can GitHub Pages NOT do?",
                        "choices": [
                            "Serve a portfolio built with Astro",
                            "Run server-side code or a database",
                            "Serve docs from the `/docs` folder",
                            "Enforce HTTPS with a custom domain",
                        ],
                        "answer_index": 1,
                        "difficulty": 8,
                        "explanation": "Pages is a static file host — no Node/Python runtime, no databases, no secrets. Dynamic needs go to serverless functions or an external API; the frontend on Pages just calls them.",
                        "company_tags": ["amazon", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Actions-built Pages site deploys but shows a blank page with 404s for `/assets/*`. What's the most likely cause?",
                        "choices": [
                            "GitHub Pages deleted the assets folder",
                            "The repo must be public for assets to load",
                            "You need a paid plan for asset hosting",
                            "Wrong base path — the site is served under `/<repo>/`, so absolute `/assets` paths break",
                        ],
                        "answer_index": 3,
                        "difficulty": 9,
                        "explanation": "Project sites live in a subdirectory, so `/assets/app.js` resolves to `<user>.github.io/assets/app.js` (missing) instead of `<user>.github.io/<repo>/assets/app.js`. Fix: set the framework's base path (e.g. Vite's `base: '/<repo>/'`) or use relative URLs.",
                        "company_tags": ["google", "flipkart"],
                    },
                ],
            },
            {
                "slug": "github-ecosystem-codespaces",
                "title": "Codespaces: Cloud Dev Environments",
                "theory_md": """## Codespaces: Your Dev Environment, in the Cloud

A Codespace is a full VS Code environment running on GitHub's servers,
launched from any repo in one click (Code → Codespaces → "+"). No "works on
my machine" — the environment is **defined in the repo itself**.

### devcontainer.json — infrastructure as code for dev setups

```jsonc
// .devcontainer/devcontainer.json
{
  "image": "mcr.microsoft.com/devcontainers/python:3.12",
  "features": { "ghcr.io/devcontainers/features/node:1": {} },
  "customizations": { "vscode": { "extensions": ["ms-python.python"] } },
  "postCreateCommand": "pip install -r requirements.txt"
}
```

Commit this, and every contributor — and every future you — gets the identical
toolchain, extensions, and dependencies on first launch. It also works locally
in VS Code with the Dev Containers extension: same file, same environment.

### Daily workflow

- **Prebuilds** (repo Settings → Codespaces) pre-bake the container so new
  codespaces start in seconds instead of running installs from scratch.
- **Port forwarding** — run `npm run dev` in the terminal and the forwarded
  port opens in your browser automatically; set each port's visibility to
  private (requires GitHub auth) or public.
- **Secrets** — Codespaces secrets (Settings → Codespaces) are injected as
  environment variables at creation time. Never commit `.env` files.
- **Dotfiles repo** — point Codespaces at your dotfiles repo and your shell
  aliases follow you everywhere.

### Costs and hygiene

Billed per compute-hour plus storage; the free tier includes monthly hours.
Codespaces auto-timeout when idle, but idle ones still burn storage — stop or
delete stale ones from github.com/codespaces. One codespace per task, deleted
when merged, keeps the bill (and the list) sane.
""",
                "difficulty_min": 4,
                "difficulty_max": 9,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "What is a GitHub Codespace?",
                        "choices": [
                            "A cloud-hosted VS Code development environment launched from a repo",
                            "A GitHub-hosted CI runner for tests",
                            "A static site hosting service",
                            "A desktop app for managing repos offline",
                        ],
                        "answer_index": 0,
                        "difficulty": 4,
                        "explanation": "One click (Code → Codespaces) provisions a container with the repo checked out and VS Code (browser or desktop) attached. It's a full dev machine — terminal, extensions, debugger — not just an editor.",
                        "company_tags": ["microsoft", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does `.devcontainer/devcontainer.json` do?",
                        "choices": [
                            "Configures GitHub Actions workflows",
                            "Defines issue templates for the repo",
                            "Declares the container image, tools, extensions, and setup commands for the environment",
                            "Stores encrypted secrets for production",
                        ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "It's infrastructure-as-code for dev environments: committed to the repo, it guarantees every contributor gets the identical toolchain and extensions. `postCreateCommand` handles dependency installation on first boot.",
                        "company_tags": ["amazon", "atlassian"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "How should API keys be provided to a codespace?",
                        "choices": [
                            "Committed in a `.env` file so the team shares them",
                            "Hardcoded in `devcontainer.json`",
                            "Pasted into the terminal each session",
                            "Via Codespaces secrets, injected as environment variables",
                        ],
                        "answer_index": 3,
                        "difficulty": 5,
                        "explanation": "Codespaces secrets (account/org/repo settings) are injected at container creation and never touch the repo. Committing keys — even in devcontainer.json — leaks them to every future cloner.",
                        "company_tags": ["microsoft", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What are Codespace prebuilds for?",
                        "choices": [
                            "Running the test suite before each commit",
                            "Pre-baking the dev container image so new codespaces start in seconds",
                            "Building production Docker images",
                            "Pre-compiling the repo's README",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "Without prebuilds, each new codespace runs `postCreateCommand` from scratch (slow for big dependency trees). Prebuilds run on a schedule/trigger and cache the result, trading a little compute for fast developer startup.",
                        "company_tags": ["google", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A teammate's codespace can't reach the API running on port 3000 in the container. What's wrong?",
                        "choices": [
                            "Codespaces block all localhost traffic",
                            "The API must be deployed to production first",
                            "The port isn't forwarded — forward port 3000 (and set visibility) in the Ports view",
                            "Port 3000 is reserved by GitHub",
                        ],
                        "answer_index": 2,
                        "difficulty": 9,
                        "explanation": "Container ports aren't reachable until forwarded; the Ports panel maps them to a public URL. Visibility matters too: 'private' requires GitHub auth, 'public' is open — choose deliberately for webhooks vs. personal preview.",
                        "company_tags": ["amazon", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which habit keeps Codespace costs under control?",
                        "choices": [
                            "Stop/delete idle codespaces; they bill compute-hours and storage even when you're away",
                            "Use the largest machine type to finish faster",
                            "Keep one codespace per branch forever as backup",
                            "Costs are fixed per repo, so usage doesn't matter",
                        ],
                        "answer_index": 0,
                        "difficulty": 8,
                        "explanation": "Billing is usage-based: running compute plus stored volumes. Auto-timeout helps, but stale codespaces accumulate storage charges. The free tier is generous — hygiene keeps it that way.",
                        "company_tags": ["atlassian", "google"],
                    },
                ],
            },
            {
                "slug": "github-ecosystem-copilot",
                "title": "Copilot: AI Pair Programmer",
                "theory_md": """## Copilot: AI Pair Programmer — Superpowers and Guardrails

Muse suggests code as you type (Tab to accept), and **Copilot Chat**
(`/explain`, `/fix`, `/tests`, `/doc`) answers questions about your codebase.
Think of it as a tireless junior dev: fast, knowledgeable, and confidently
wrong often enough that **you stay in charge**.

### Where it genuinely helps

- Boilerplate: tests, getters/setters, API client wrappers.
- Unfamiliar APIs: "how do I do X in this library?" (verify against the docs).
- Explaining legacy code: select a function → `/explain` → readable summary.
- Repetitive refactors across similar files.

### Prompt like you mean it

```python
# fetch all open PRs for owner/repo, handle pagination and rate limits,
# return a list of (number, title) tuples
def list_open_prs(owner, repo):
    # <- Copilot now has a spec to aim at, not a blank slate
```

A comment describing *intent, inputs, edge cases, and output shape* beats a
bare function signature. Prompt quality in, code quality out.

### The limits (interviewers ask about these)

1. **It hallucinates APIs** — plausible-looking functions that don't exist.
   Run the code; check the docs.
2. **Security** — suggestions can include SQL injection, weak crypto, or
   hardcoded secrets. Treat Copilot output like a stranger's PR: review every
   line.
3. **Licensing** — it may reproduce distinctive snippets from its training
   data. For proprietary codebases, enable duplication detection / code
   referencing filters.
4. **No real understanding** — it predicts likely tokens; it doesn't know your
   system's invariants. Architecture decisions stay human.

**Rule:** Copilot writes the first draft; you own the merge.
""",
                "difficulty_min": 4,
                "difficulty_max": 9,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "What is Muse's primary interaction model in the editor?",
                        "choices": [
                            "A chatbot that writes entire applications from one prompt",
                            "Inline gray-text suggestions you accept with Tab as you type",
                            "A linter that auto-fixes all warnings",
                            "A debugger that steps through code for you",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "Copilot predicts the likely continuation of what you're writing — the current line, the function body — based on surrounding context. Tab accepts, Esc dismisses; you're composing with an autocomplete that understands intent-ish.",
                        "company_tags": ["microsoft", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which comment gets the BEST Copilot suggestion?",
                        "choices": [
                            "`# function here`",
                            "`# do the thing`",
                            "`# TODO: fix later`",
                            "`# fetch all open PRs for owner/repo, handle pagination and rate limits, return list of (number, title)`",
                        ],
                        "answer_index": 3,
                        "difficulty": 5,
                        "explanation": "Copilot aims at the target you describe. Vague comments produce vague code; a comment specifying intent, inputs, edge cases, and output shape gives the model a concrete spec to complete — prompt quality in, code quality out.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What is the biggest technical risk of accepting Copilot suggestions unreviewed?",
                        "choices": [
                            "It can hallucinate non-existent APIs and suggest insecure patterns (SQLi, weak crypto)",
                            "It always writes code in the wrong language",
                            "It deletes your existing code",
                            "It bills per accepted suggestion",
                        ],
                        "answer_index": 0,
                        "difficulty": 7,
                        "explanation": "Copilot predicts plausible tokens, not correct ones — `db.query(f\"SELECT * FROM users WHERE id = {uid}\")` looks right and is injectable. Treat every suggestion like a stranger's PR: read it, test it, check the docs.",
                        "company_tags": ["google", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "When is Copilot MOST valuable?",
                        "choices": [
                            "Designing system architecture from scratch",
                            "Debugging race conditions in production",
                            "Boilerplate, tests, docs, and unfamiliar-but-documented APIs",
                            "Writing cryptographic primitives",
                        ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "It excels at high-pattern, low-judgment work — the 80% that's typing, not thinking. Architecture, novel algorithms, and security-critical code need human reasoning; Copilot accelerates everything around those decisions.",
                        "company_tags": ["atlassian", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your company worries about Copilot reproducing licensed code. What mitigates this?",
                        "choices": [
                            "Nothing — Copilot never reproduces training data",
                            "Only using Copilot on weekends",
                            "Writing all code in comments first",
                            "Enabling duplication detection / code referencing filters that block verbatim matches",
                        ],
                        "answer_index": 3,
                        "difficulty": 8,
                        "explanation": "Copilot offers filters that detect when a suggestion matches public code and either block it or surface the match with license info. Combined with policy (review, no pasting secrets), this is how teams use it on proprietary codebases.",
                        "company_tags": ["microsoft", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A junior dev says 'Copilot wrote it, so it must be correct.' What's the flaw in this reasoning?",
                        "choices": [
                            "Copilot is always correct, so there's no flaw",
                            "Copilot predicts likely tokens — it has no model of your system's invariants or runtime behavior",
                            "Copilot code can't be tested",
                            "Copilot only works for Python",
                        ],
                        "answer_index": 1,
                        "difficulty": 9,
                        "explanation": "It's a statistical parrot, not an engineer: it doesn't know your database schema, your concurrency model, or that `is_admin` defaults matter. Correctness comes from tests, reviews, and understanding — Copilot supplies the draft, you supply the judgment.",
                        "company_tags": ["google", "atlassian"],
                    },
                ],
            },
            {
                "slug": "github-ecosystem-projects",
                "title": "Projects, Boards & Automation",
                "theory_md": """## Projects, Boards & Automation

GitHub Projects is the kanban-plus layer over your issues and PRs — the same
tool many teams use instead of Jira or Trello for engineering work.

### Building a board

Projects → New project → choose a layout:

- **Board** — classic kanban (Todo / In Progress / Done).
- **Table** — spreadsheet view with sortable columns.
- **Roadmap** — timeline/Gantt over date fields ("what ships when").

Add **custom fields** (Priority: P0–P3, Size: S/M/L, Sprint) and **views**
(e.g. "My work": `assignee:@me status:open`, "P0 bugs": `priority:P0`).

### Automation that runs the board for you

- **Built-in workflows** (project Settings → Workflows): auto-add items
  matching filters (`is:issue label:bug`), auto-archive closed items.
- **GitHub Actions** for the rest:

```yaml
# add every new PR to the project automatically
- uses: actions/add-to-project@v1
  with:
    project-url: https://github.com/orgs/acme/projects/3
    github-token: ${{ secrets.ADD_TO_PROJECT_PAT }}
```

Note: this needs a PAT with project scope — the default `GITHUB_TOKEN`
can't write to projects.

- **Milestones** group issues toward a release date; Projects track the
  *process*, milestones track the *deadline*. Use both.

### Closing keywords — the cheapest automation

Write `Closes #123` (or `Fixes`, `Resolves`) in the PR body and merging
auto-closes the linked issue. Pair it with auto-archive and done work clears
itself — the board stays truthful with zero dragging.

### Pro habits

- Every issue gets Priority + Size at triage — an unestimated backlog is a
  wishlist, not a plan.
- Use iteration fields for sprints; review the Roadmap view in planning.
- Link PRs to issues always: traceability from code back to the "why" is what
  separates a repo from a file dump.
""",
                "difficulty_min": 4,
                "difficulty_max": 9,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "In GitHub Projects, what does the Roadmap layout show?",
                        "choices": [
                            "A list of all repository contributors",
                            "A burndown chart of story points",
                            "Items on a timeline/Gantt view based on date fields",
                            "The git commit graph",
                        ],
                        "answer_index": 2,
                        "difficulty": 4,
                        "explanation": "Board = kanban columns, Table = spreadsheet, Roadmap = timeline. Roadmap needs date fields (start/target) on items — it's the planning view for 'what ships when.'",
                        "company_tags": ["atlassian", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "How do you auto-add every new `bug`-labeled issue to your project?",
                        "choices": [
                            "Project Settings → Workflows → auto-add with filter `is:issue label:bug`",
                            "Rename the issue to include the project name",
                            "It's automatic — all issues join all projects",
                            "Use `git commit` with the project URL in the message",
                        ],
                        "answer_index": 0,
                        "difficulty": 6,
                        "explanation": "Built-in workflows watch repo events and add matching items. Filters use search syntax, so `is:issue label:bug` or `is:pr author:@me` route work to the right board without manual triage.",
                        "company_tags": ["google", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What is the difference between a milestone and a project board?",
                        "choices": [
                            "Milestones track a deadline/release; the project tracks the workflow process",
                            "They are identical features with different names",
                            "Milestones are for code, projects are for docs",
                            "Projects expire; milestones are permanent",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "A milestone groups issues toward 'v2.4 ships Oct 30' with a progress bar. The project manages state (Todo → In Progress → Done), priorities, and sprints. Teams use both: milestones for the *when*, projects for the *how*.",
                        "company_tags": ["microsoft", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A PR says 'Closes #123'. What happens on merge, and how does the board reflect it?",
                        "choices": [
                            "Nothing — keywords are just comments",
                            "The PR is deleted; the issue stays open",
                            "Only the assignee is notified",
                            "The linked issue auto-closes, and an auto-archive workflow removes it from the board",
                        ],
                        "answer_index": 3,
                        "difficulty": 8,
                        "explanation": "Closing keywords (`Closes`, `Fixes`, `Resolves #123`) close the linked issue when the PR merges. Pair that with the project's auto-archive workflow and done work clears itself — the board stays truthful with zero dragging.",
                        "company_tags": ["atlassian", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why give every issue Priority and Size fields at triage?",
                        "choices": [
                            "An unestimated backlog can't be planned — fields turn a wishlist into a schedule",
                            "GitHub requires them before an issue can be closed",
                            "They make the board load faster",
                            "They're only for managers' reports",
                        ],
                        "answer_index": 0,
                        "difficulty": 7,
                        "explanation": "Custom fields make trade-offs explicit: P0/S sorts itself to the top of sprint planning, and size estimates feed velocity. Without them, 'everything is important' and planning is vibes.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You want 'every new PR added to project #3' without manual work. Which approach?",
                        "choices": [
                            "A pre-push git hook that calls the Projects API",
                            "Asking contributors to drag their PRs in",
                            "A GitHub Actions workflow using `actions/add-to-project` with the project URL",
                            "Projects auto-add PRs by default",
                        ],
                        "answer_index": 2,
                        "difficulty": 9,
                        "explanation": "`actions/add-to-project` runs on `pull_request_target` and files each PR into the project. Hooks can't do this (they're local, pre-push), and it needs a PAT with project scope — the default GITHUB_TOKEN can't write to projects.",
                        "company_tags": ["microsoft", "atlassian"],
                    },
                ],
            },
            {
                "slug": "github-ecosystem-security",
                "title": "Repo Security: Dependabot, Secrets & Code Scanning",
                "theory_md": """## Securing Repos: Dependabot, Secret Scanning & Code Scanning

### Dependabot — your dependency janitor

- **Alerts**: GitHub watches your dependency graph and opens alerts for known
  CVEs (Security tab → Dependabot alerts), with severity ratings.
- **Security updates**: one-click PRs bumping the vulnerable package to the
  patched version.
- **Version updates** (`.github/dependabot.yml`): scheduled PRs keeping
  everything fresh:

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule: { interval: "weekly" }
```

Review these PRs like any other — a major bump can break you. Triage smart:
merge patch/minor bumps fast, scrutinize majors, and use `groups:` plus
schedules to control noise.

### Secret scanning — catching leaked credentials

Scans commits for tokens and API keys (GitHub's partner patterns plus your
custom patterns). **Push protection** goes further: it *blocks* the push
containing a secret and shows you the exact file and line — the leak never
lands on the remote.

If a secret ever lands in history: **revoke it first**. Rewriting history
doesn't un-expose what was already fetched, forked, or cached. Revoke kills
the credential's power; history cleanup is hygiene afterwards.

### Code scanning (CodeQL)

Static analysis that runs on PRs and flags real vulnerability patterns in
*your* code — SQL injection, XSS, path traversal:

```yaml
# .github/workflows/codeql.yml (via starter workflow)
- uses: github/codeql-action/init@v3
  with: { languages: javascript, python }
- uses: github/codeql-action/analyze@v3
```

Findings appear as PR annotations and in the Security tab. Dependabot watches
your **supply chain** (dependencies); CodeQL watches **your code** — you need
both, because a fully patched dependency tree can still serve XSS from your
templates.

### Branch protection — the human gate

Settings → Branches → protect `main`:

- Require PR reviews before merging.
- **Require status checks to pass** (CI green, CodeQL clean) — this is what
  stops "it worked on my machine" merges.
- Dismiss stale approvals when new commits are pushed.
- Block force-pushes.

Automation catches machines' mistakes; reviews catch humans'. Protection
means `main` only moves forward when both agree.
""",
                "difficulty_min": 4,
                "difficulty_max": 9,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "What does Dependabot do when a CVE is found in your dependencies?",
                        "choices": [
                            "Deletes the vulnerable package from your repo",
                            "Opens an issue asking you to fix it someday",
                            "Pauses all CI until you respond",
                            "Raises an alert and can open a PR bumping to the patched version",
                        ],
                        "answer_index": 3,
                        "difficulty": 5,
                        "explanation": "Dependabot alerts surface in the Security tab with severity; 'security updates' go further and propose the fix as a PR. You still review it — a major-version bump can break your build — but the toil of watching CVEs disappears.",
                        "company_tags": ["google", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What is push protection in secret scanning?",
                        "choices": [
                            "It encrypts all pushes with your GPG key",
                            "It requires two reviewers for every push",
                            "It blocks a push containing a detected secret and tells you the exact line",
                            "It scans your code for hardcoded passwords only",
                        ],
                        "answer_index": 2,
                        "difficulty": 4,
                        "explanation": "Detection after the push is already a leak (the commit exists on the remote). Push protection shifts left: the push is rejected *before* the secret lands, with the file and line highlighted so you can remove it and amend.",
                        "company_tags": ["microsoft", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You accidentally committed an AWS key and pushed. What is the FIRST thing to do?",
                        "choices": [
                            "Rewrite history with `git rebase -i` to remove it",
                            "Revoke/rotate the key immediately",
                            "Delete the repository",
                            "Force-push an empty commit",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "Once pushed, the secret is compromised — clones, forks, and caches may already have it. History rewriting doesn't un-expose it. Revoke first (kill the credential's power), then clean history as hygiene.",
                        "company_tags": ["amazon", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does CodeQL code scanning find that Dependabot doesn't?",
                        "choices": [
                            "Vulnerabilities in YOUR code (SQL injection, XSS) vs. vulnerabilities in your DEPENDENCIES",
                            "Vulnerabilities in dependencies vs. in your code",
                            "Only formatting issues",
                            "Nothing — they scan the same things",
                        ],
                        "answer_index": 0,
                        "difficulty": 6,
                        "explanation": "They're complementary layers: Dependabot watches the supply chain (your libs), CodeQL analyzes your own code's data flow for bug patterns. A fully patched dependency tree can still serve XSS from your templates.",
                        "company_tags": ["atlassian", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your `dependabot.yml` opens 40 PRs after enabling version updates. What's the smart response?",
                        "choices": [
                            "Merge them all immediately — Dependabot is always safe",
                            "Disable Dependabot forever",
                            "Triage: merge patch/minor bumps fast, review majors carefully, use groups and schedules to control noise",
                            "Close them all and pin everything to 5-year-old versions",
                        ],
                        "answer_index": 2,
                        "difficulty": 9,
                        "explanation": "Version-update PRs are proposals, not mandates. Configure grouping (`groups:`), schedules, and ignore rules to batch noise; auto-merge patch bumps with CI green if you're confident. Stale dependencies are how CVEs accumulate.",
                        "company_tags": ["google", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which branch protection setting BEST prevents 'it worked on my machine' merges?",
                        "choices": [
                            "Requiring linear history",
                            "Allowing force pushes for speed",
                            "Requiring PR reviews only",
                            "Requiring status checks (CI) to pass before merging",
                        ],
                        "answer_index": 3,
                        "difficulty": 8,
                        "explanation": "Reviews catch human judgment errors; status checks catch machine-verifiable ones — tests, lint, build, CodeQL. Together with 'dismiss stale approvals on new pushes,' protection means main only moves forward when both humans and machines agree.",
                        "company_tags": ["microsoft", "amazon"],
                    },
                ],
            },
        ],
    },
]
