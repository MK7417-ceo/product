"""Seed content: Git & GitHub — Part 2 (Modules 3-4: Remote & Collaboration, GitHub Actions).

ORIGINAL educational content. All git commands and YAML are real and
verifiable; no invented action names or YAML keys.

Exports a single variable ``MODULES``: a list of 2 module dicts
(git-remote, github-actions), each with 7 lessons, each lesson with
exactly 6 MCQs (84 questions total).
"""

from __future__ import annotations

MODULES = [
    {
        "slug": "git-remote",
        "name": "Remote & Collaboration",
        "description": "Work with remotes, forks, pull requests, and branch policies like a professional team member.",
        "lessons": [
            {
                "slug": "git-remote-remotes-origin",
                "title": "Remotes: origin and git remote",
                "theory_md": """## What is a remote?

A **remote** is a named reference to another copy of your repository, usually
hosted on a server like GitHub. Your local clone is a full copy; the remote is
just where you exchange commits with teammates.

## The default remote: origin

When you clone, Git automatically creates a remote called `origin` pointing at
the URL you cloned from. Convention (not magic) names it `origin`; you can
rename it.

## Listing and inspecting remotes

```bash
git remote -v        # list remotes with their URLs (fetch + push)
git remote show origin  # details: URL, tracked branches, pull behavior
```

`git remote -v` output looks like:

```
origin  https://github.com/org/repo.git (fetch)
origin  https://github.com/org/repo.git (push)
```

## Adding, renaming, and removing remotes

```bash
git remote add upstream https://github.com/original/repo.git  # second remote
git remote rename origin destination   # rename a remote
git remote remove upstream             # delete a remote reference
```

Removing a remote deletes only the *reference* — your local commits and
branches stay untouched.

## Changing a remote URL

```bash
git remote set-url origin git@github.com:org/repo.git
```

Useful when switching from HTTPS to SSH, or when a repo moves to a new
owner/org.
""",
                "difficulty_min": 1,
                "difficulty_max": 4,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "What does `git remote -v` display?",
                        "choices": [
                            "The list of remote names with their fetch and push URLs",
                            "The full commit history of every branch",
                            "A visual graph of local branches",
                            "The list of files staged for commit",
                        ],
                        "answer_index": 0,
                        "difficulty": 1,
                        "explanation": "`git remote -v` lists each configured remote along with the URLs used for fetch and push. The `-v` flag means verbose — without it you only see the remote names.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "In a typical `git clone`, what does the remote named `origin` refer to?",
                        "choices": [
                            "The first branch you created locally",
                            "A special merge-only branch on GitHub",
                            "The default name Git gives to the repository you cloned from",
                            "The main author's fork of the project",
                        ],
                        "answer_index": 2,
                        "difficulty": 2,
                        "explanation": "`origin` is simply the conventional name Git assigns automatically to the source you cloned from. It is a convention, not a requirement — you can rename it.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You cloned a repo, then the project moved to a different organization. Which command updates the stored URL?",
                        "choices": [
                            "git remote add origin <new-url>",
                            "git remote set-url origin <new-url>",
                            "git pull --rebase <new-url>",
                            "git clone --replace origin <new-url>",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "`git remote set-url` rewrites the URL stored for an existing remote. `git remote add` fails here because `origin` already exists, and the other options are not real Git commands.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What happens to your local work if you run `git remote remove upstream`?",
                        "choices": [
                            "Your local commits and branches are deleted",
                            "Only the remote reference is deleted; local work is untouched",
                            "All commits are force-pushed to origin",
                            "The repository is re-cloned from origin",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "A remote is just a named pointer to a URL. Removing it deletes the pointer and its tracking refs' configuration — your objects, commits, and branches remain intact.",
                        "company_tags": ["tcs", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why might a repo need two remotes like `origin` and `upstream`?",
                        "choices": [
                            "Git requires two remotes for every repository",
                            "So that two users can share one local clone",
                            "To separate your fork (origin) from the original project (upstream) you sync with",
                            "Because one remote handles fetch and the other handles push only",
                        ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "Fork contributors push to their own fork (`origin`) but pull updates from the original project's `upstream` remote. The two-remotes pattern keeps those flows separate.",
                        "company_tags": ["microsoft", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "`git remote show origin` reports that the remote's default branch is `main`. What does that information actually tell Git to do?",
                        "choices": [
                            "It deletes any other remote-tracking branches",
                            "It sets what `git clone` checks out initially and what HEAD refers to for the remote",
                            "It force-syncs all local branches to match main",
                            "It creates a local branch called origin",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "`git remote show origin` displays the remote's HEAD (default branch), which Git uses when cloning to decide which branch to check out initially. It does not modify anything.",
                        "company_tags": ["amazon", "microsoft"],
                    },
                ],
            },
            {
                "slug": "git-remote-clone-push-pull",
                "title": "Clone, Push, Pull & Fetch",
                "theory_md": """## Cloning a repository

```bash
git clone https://github.com/org/repo.git
git clone https://github.com/org/repo.git my-folder   # custom directory name
```

Clone downloads the *entire* repository — full history, all branches (as
remote-tracking refs), and creates `origin` for you.

## Pushing: sending commits to the remote

```bash
git push origin main            # push local main to origin's main
git push -u origin feature-x    # push AND set upstream tracking
git push                        # push the current branch to its upstream
```

## Pull vs Fetch: the critical difference

- `git fetch origin` — downloads new commits from the remote into
  **remote-tracking branches** (`origin/main`), but does NOT touch your working
  branch. Safe; nothing is merged.
- `git pull origin main` — does `git fetch` **plus** a merge (or rebase with
  `--rebase`) of `origin/main` into your current branch. Changes your working
  tree; can create merge commits or conflicts.

```bash
git fetch origin                 # inspect first
git log --oneline main..origin/main  # see what fetch brought in
git merge origin/main            # then merge deliberately
```

This fetch-then-review flow is exactly what `git pull` does in one step —
understanding it separately makes conflicts far less scary.

## Forcing pushes (handle with care)

```bash
git push --force-with-lease origin main
```

`--force-with-lease` rewrites remote history only if nobody else pushed since
you last fetched — a much safer force push. Use only on your own feature
branches, never on shared branches.
""",
                "difficulty_min": 1,
                "difficulty_max": 6,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "What is the key difference between `git fetch` and `git pull`?",
                        "choices": [
                            "fetch uploads commits; pull downloads them",
                            "fetch only downloads remote changes without merging; pull fetches and merges them into the current branch",
                            "fetch works offline; pull requires internet",
                            "There is no difference — they are aliases",
                        ],
                        "answer_index": 1,
                        "difficulty": 2,
                        "explanation": "Fetch updates remote-tracking branches only and never touches your working tree, while pull does fetch plus a merge into your current branch. Fetch-first is the safe way to review changes before merging.",
                        "company_tags": ["tcs", "infosys", "wipro"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You want to download your teammate's changes but NOT merge them yet so you can inspect them first. Which command?",
                        "choices": [
                            "git pull origin main",
                            "git merge --no-commit",
                            "git fetch origin",
                            "git checkout origin/main",
                        ],
                        "answer_index": 2,
                        "difficulty": 3,
                        "explanation": "Fetch brings the new commits into remote-tracking branches like `origin/main` without touching your branch. You can then `git log main..origin/main` to inspect before merging.",
                        "company_tags": ["accenture", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does `git clone <url>` set up automatically?",
                        "choices": [
                            "Only the working files, without history",
                            "Full history, all branches as remote-tracking refs, and a remote named origin",
                            "A push-only connection to the server",
                            "A fork of the repository under your account",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "Clone copies the entire history and all branch tips into remote-tracking refs (like `origin/main`), checks out the default branch, and creates the `origin` remote. It is a full repo, not just files.",
                        "company_tags": ["tcs", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does `git push -u origin feature-x` do that plain `git push` does not?",
                        "choices": [
                            "It merges feature-x into main on the remote",
                            "It pushes and also sets the upstream, so future plain `git push`/`git pull` know where to go",
                            "It pushes without requiring any network connection",
                            "It undoes the last pushed commit",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "The `-u` (`--set-upstream`) flag records `origin/feature-x` as the tracking upstream for your local branch. After that, bare `git push` and `git pull` know exactly which remote branch to use.",
                        "company_tags": ["amazon", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why is `git push --force-with-lease` preferred over `git push --force` on a personal feature branch?",
                        "choices": [
                            "It pushes faster",
                            "It skips the CI checks",
                            "It refuses to overwrite the remote if someone else pushed since your last fetch",
                            "It automatically rebases your commits",
                        ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "`--force-with-lease` verifies the remote tip still matches what you last fetched before rewriting history, so you cannot accidentally destroy commits pushed by someone else. Plain `--force` overwrites blindly.",
                        "company_tags": ["google", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "After running `git fetch origin`, you run `git log --oneline main..origin/main`. What do the listed commits represent?",
                        "choices": [
                            "Commits you have locally that the remote lacks",
                            "Commits on origin/main that you do not yet have in your local main",
                            "All commits in both branches",
                            "Commits that were deleted from the remote",
                        ],
                        "answer_index": 1,
                        "difficulty": 8,
                        "explanation": "The `A..B` range shows commits reachable from B but not from A. Since fetch updated `origin/main`, this lists exactly the new remote commits waiting to be merged into your local `main`.",
                        "company_tags": ["amazon", "google"],
                    },
                ],
            },
            {
                "slug": "git-remote-tracking-upstream",
                "title": "Tracking Branches & Upstream",
                "theory_md": """## Tracking branches

A **tracking branch** is a local branch that has a direct relationship with a
remote branch (its **upstream**). The upstream is what plain `git push` and
`git pull` use when you give no arguments.

```bash
git branch -vv     # show each local branch + its upstream, e.g. [origin/main]
```

Sample output:

```
* main       abc1234 [origin/main] Initial commit
  feature-x  def5678 [origin/feature-x: ahead 2] Add search
```

## Setting the upstream

```bash
git branch --set-upstream-to=origin/main main     # link existing branches
git checkout -b feature-x origin/feature-x        # checkout auto-tracks
git push -u origin feature-x                      # set upstream on first push
```

`git checkout -b <name> <remote>/<branch>` creates the local branch and
configures tracking automatically.

## Why tracking matters

With tracking configured:

```bash
git status   # now tells you: "Your branch is ahead of 'origin/main' by 2 commits."
git push     # no need to spell out origin feature-x every time
git pull     # knows exactly what to merge
```

## Remote-tracking branches

Branches like `origin/main` are **remote-tracking branches** — read-only
snapshots of the remote's state at your last fetch. You never commit directly
to them; you merge or rebase from them. They update only via `fetch`/`pull`.
""",
                "difficulty_min": 2,
                "difficulty_max": 6,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "What does `git branch -vv` show that plain `git branch` does not?",
                        "choices": [
                            "Each local branch's upstream tracking relationship",
                            "The full commit history",
                            "Deleted branches",
                            "Remote-only branch URLs",
                        ],
                        "answer_index": 0,
                        "difficulty": 2,
                        "explanation": "The `-vv` flag displays each branch's upstream (e.g. `[origin/main]`) plus ahead/behind status. Plain `git branch` lists only branch names.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "`git status` says: \"Your branch is ahead of 'origin/main' by 2 commits.\" What does this mean?",
                        "choices": [
                            "The remote has 2 commits you haven't fetched",
                            "You have 2 local commits on this branch that are not yet pushed",
                            "Your branch has diverged by 2 merge conflicts",
                            "2 of your commits failed CI",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "'Ahead by 2' means your local branch contains 2 commits the upstream does not — the classic un-pushed state. A `git push` would resolve it.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which command links an existing local branch `main` to track `origin/main`?",
                        "choices": [
                            "git branch --set-upstream-to=origin/main main",
                            "git push --track main",
                            "git remote add origin/main main",
                            "git checkout origin/main --track",
                        ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "`git branch --set-upstream-to=<upstream> <branch>` configures the tracking relationship on an existing branch. The other options are not valid Git syntax.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What is a remote-tracking branch like `origin/main`?",
                        "choices": [
                            "A branch you can commit to directly on the server",
                            "A read-only local snapshot of the remote branch's state at your last fetch",
                            "A merge commit between two remotes",
                            "A branch stored only on GitHub, not locally",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "Remote-tracking branches live in your local repo but reflect the remote's tip as of the last fetch — you merge or rebase from them, never commit to them.",
                        "company_tags": ["microsoft", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "After `git push -u origin feature-x` once, why do later pushes on that branch work with plain `git push`?",
                        "choices": [
                            "Git remembers the last arguments typed in the terminal",
                            "The upstream link is stored in the repo config, so Git knows the default destination",
                            "feature-x becomes the default branch of the remote",
                            "Git auto-detects the only remote",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "`-u` writes `branch.feature-x.remote=origin` and `branch.feature-x.merge=refs/heads/feature-x` into `.git/config`. Every later argument-less push reads that stored upstream.",
                        "company_tags": ["google", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You run `git checkout -b hotfix origin/main`. What tracking relationship is created?",
                        "choices": [
                            "No tracking — hotfix is a detached local branch",
                            "hotfix tracks origin/hotfix",
                            "hotfix tracks origin/main, since the start point was a remote-tracking branch",
                            "origin/main is renamed to hotfix on the remote",
                        ],
                        "answer_index": 2,
                        "difficulty": 7,
                        "explanation": "When the start point of a new branch is a remote-tracking branch, Git automatically sets that remote-tracking branch as the upstream. So `hotfix` tracks `origin/main`.",
                        "company_tags": ["amazon", "microsoft"],
                    },
                ],
            },
            {
                "slug": "git-remote-fork-vs-clone",
                "title": "Fork vs Clone",
                "theory_md": """## Clone

```bash
git clone https://github.com/org/repo.git
```

Clone copies the repo to your **machine**. You get the same history, but the
repo still lives in the same GitHub account/org — cloning does nothing on the
GitHub side.

## Fork

Fork copies the repo to **your GitHub account** (a server-side copy). You get
`github.com/YOURNAME/repo`, fully independent of the original. Forks are the
unit of contribution for open source: you own the fork, so you can push
branches to it freely.

## The fork workflow

```bash
# 1. Fork on github.com (button) -> github.com/YOURNAME/repo
# 2. Clone YOUR fork
git clone https://github.com/YOURNAME/repo.git
cd repo

# 3. Add the original as a second remote
git remote add upstream https://github.com/org/repo.git

# 4. Keep your fork's main in sync
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

## Keeping the fork synced

GitHub now offers a "Sync fork" button in the UI, but the `fetch upstream` +
`merge` flow above is what actually happens underneath. Sync before starting
new work so your branch doesn't contain stale code.

## Which to use?

- **Clone**: you have push access to the repo (your own repo, or your team's).
- **Fork**: you do NOT have push access (open source, another team's repo) and
  plan to propose changes via a pull request.
""",
                "difficulty_min": 1,
                "difficulty_max": 5,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "What is the fundamental difference between forking and cloning a repository?",
                        "choices": [
                            "Fork creates a server-side copy under your GitHub account; clone copies it to your local machine",
                            "Clone copies to your account; fork copies to your machine",
                            "They are identical operations with different names",
                            "Fork requires admin access; clone is public",
                        ],
                        "answer_index": 0,
                        "difficulty": 2,
                        "explanation": "Forking is a GitHub-side action that duplicates the repo into your account so you own it; cloning is a Git action that copies a repo (any copy) onto your local disk.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You want to contribute a bug fix to a popular open-source project where you have no write access. What is the correct first step?",
                        "choices": [
                            "git clone the repo and push directly to its main",
                            "Fork the repo on GitHub, then clone your fork",
                            "Download the ZIP and email the maintainer",
                            "git push --force to their repository",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "Without write access you cannot push to the original. Fork gives you a copy you own; you clone your fork, make changes, push to your fork, and open a pull request to the original.",
                        "company_tags": ["wipro", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "After cloning your fork, you run `git remote add upstream <original-url>`. What does `upstream` let you do?",
                        "choices": [
                            "Push directly to the original repo's main",
                            "Delete the original repository",
                            "Fetch updates from the original project into your local repo",
                            "Merge your fork into the original automatically",
                        ],
                        "answer_index": 2,
                        "difficulty": 4,
                        "explanation": "The `upstream` remote points at the original project, so `git fetch upstream` brings in its latest commits. You then merge them into your fork to stay current — it grants no write access.",
                        "company_tags": ["accenture", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "When should you clone directly instead of forking?",
                        "choices": [
                            "When the repo is very large",
                            "When you have push access to the repository",
                            "When you only want to read the code",
                            "When GitHub is down",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "If you already have write access (your own repo, your team's repo), a direct clone plus a feature branch is all you need. Forks exist to enable contribution where you lack push access.",
                        "company_tags": ["tcs", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does GitHub's \"Sync fork\" button do under the hood?",
                        "choices": [
                            "Deletes your fork and re-forks from scratch",
                            "Fetches the upstream's default branch and merges/fast-forwards it into your fork's branch",
                            "Pushes your fork's changes into the original repo",
                            "Rewrites your fork's history",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "Syncing fast-forwards (or merges) the upstream default branch into your fork — the same `git fetch upstream && git merge upstream/main` flow, wrapped in a button.",
                        "company_tags": ["microsoft", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your fork's `main` is 15 commits behind the original, and you open a PR from a branch created off your stale main. What is the most likely consequence?",
                        "choices": [
                            "The PR is rejected automatically by GitHub",
                            "Your PR may show merge conflicts or fail CI because it is based on outdated code",
                            "The fork is deleted",
                            "Your commits are lost",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "Stale bases cause real problems: the diff may be wrong, tests may fail against current upstream code, and conflicts appear on merge. Syncing first keeps the PR diff minimal and accurate.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                ],
            },
            {
                "slug": "git-remote-pr-workflow",
                "title": "The Pull Request Workflow",
                "theory_md": """## The PR lifecycle

1. **PR created** — You push a branch to your fork (or the shared repo) and open
   a pull request: base branch `main` ← your branch `feature-x`. GitHub shows
   the diff and runs CI checks.
2. **Review** — Maintainers and teammates read the diff, leave inline comments,
   and request changes.
3. **Changes requested** — You push new commits to the *same branch*; the PR
   updates automatically. Discussion continues.
4. **Approved** — Reviewers approve; required status checks pass.
5. **Merged** — The PR is merged into `main` (merge commit, squash, or rebase),
   and the feature branch is deleted.

## Opening a PR

```bash
git checkout -b feature-x
# ... work, commit ...
git push -u origin feature-x
# then open the PR on github.com (or: gh pr create)
```

GitHub shows a green **Compare & pull request** banner after the push.

## Draft PRs

Mark a PR as **draft** to signal "work in progress — not ready to merge".
Drafts block merging but still collect CI results and early feedback.

## Keeping the PR branch fresh

```bash
git fetch origin
git rebase origin/main      # replay your commits onto the latest main
git push --force-with-lease # update the PR branch
```

A fresh PR merges cleanly and CI tests the code against current `main`.

## Merge strategies

- **Merge commit** — preserves the full branch history.
- **Squash and merge** — compresses the PR into one commit on `main`; keeps
  `main` history linear and tidy.
- **Rebase and merge** — replays commits onto `main` without a merge commit.

Repos often standardize on one strategy via branch protection rules.
""",
                "difficulty_min": 2,
                "difficulty_max": 7,
                "is_important": True,
                "has_visual": True,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "In a pull request from `feature-x` into `main`, what do the \"base\" and \"compare\" branches refer to?",
                        "choices": [
                            "Base is your branch; compare is main",
                            "Base is main (the target); compare is feature-x (the changes)",
                            "Both must be on the same fork",
                            "Base is the older commit; compare is the newer one",
                        ],
                        "answer_index": 1,
                        "difficulty": 2,
                        "explanation": "The base branch is where changes will land (main); the compare branch holds the new commits (feature-x). Getting them backwards would propose the reverse merge.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A reviewer requests changes on your PR. How do you update the PR?",
                        "choices": [
                            "Open a brand new pull request",
                            "Push new commits to the same branch — the PR updates automatically",
                            "Delete the branch and start over",
                            "Edit the PR's base branch",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "A PR tracks a branch, not a fixed set of commits. Pushing more commits to the same branch appends them to the open PR's diff and re-runs CI automatically.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What is the purpose of marking a pull request as a draft?",
                        "choices": [
                            "To hide the PR from all reviewers",
                            "To signal work-in-progress that collects CI feedback but cannot be merged yet",
                            "To skip code review entirely",
                            "To auto-merge it after 24 hours",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "Draft PRs are explicitly not mergeable, but they still run checks and invite early comments — ideal for getting feedback before the code is final.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your PR shows \"This branch is out-of-date with the base branch.\" What is the safe fix?",
                        "choices": [
                            "Close the PR and recreate it",
                            "Update your branch (merge or rebase main into it) so CI tests current code",
                            "Force-push an empty commit",
                            "Change the base branch to your feature branch",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "An out-of-date PR was tested against old main. Rebasing/merging main into the branch refreshes it, re-runs CI on the real merge result, and prevents surprise conflicts.",
                        "company_tags": ["microsoft", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A repo's policy requires \"squash and merge\". What does this do to the PR's 12 commits?",
                        "choices": [
                            "Deletes the PR without merging",
                            "Combines all 12 into a single commit on main, keeping main's history linear",
                            "Merges each commit individually with 12 merge commits",
                            "Rebases them but keeps all 12 separate",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "Squash merge compresses the whole PR into one commit on the target branch. Main stays clean and readable, while the PR page preserves the full discussion history.",
                        "company_tags": ["amazon", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A PR is approved but a required CI check is failing. What happens when you try to merge?",
                        "choices": [
                            "GitHub merges anyway since approval is enough",
                            "The merge is blocked until the required check passes",
                            "The PR is auto-closed",
                            "Approval is revoked automatically",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "Required status checks are a hard gate in branch protection: neither approvals nor admin habit bypass them. Fix the failing check, then merge.",
                        "company_tags": ["google", "flipkart"],
                    },
                ],
            },
            {
                "slug": "git-remote-code-review",
                "title": "Code Review Best Practices",
                "theory_md": """## Why code review matters

Reviews catch bugs, spread knowledge across the team, and enforce standards.
Every PR deserves at least one careful read — it's the cheapest quality gate
in software engineering.

## For reviewers

- **Review the diff, not the person.** Comment on code: "This loop is O(n²);
  consider a map lookup" instead of "You wrote this badly."
- **Ask questions, don't command.** "What happens if `items` is empty here?"
  invites discussion; "Fix this" shuts it down.
- **Distinguish blocking vs nit.** Prefix optional polish with `nit:` so the
  author knows it isn't required.
- **Approve what you reviewed.** Don't rubber-stamp 2,000-line diffs. If the
  diff is too big, ask the author to split it.
- **Check behavior, not just style.** Ask: does it handle errors? Are there
  tests? Does the naming explain intent?

## For authors

- **Small PRs get reviewed fast.** Aim for < 400 lines changed; one PR = one
  logical change.
- **Write a good PR description:** what changed, why, and how to test it.
- **Respond to every comment** — fix it, or explain why not. Never resolve
  someone else's thread silently.
- **Don't take feedback personally.** The goal is better code, not judgment.

## Review checklist

1. Does it solve the stated problem?
2. Edge cases and error handling?
3. Tests added/updated?
4. No secrets, debug prints, or dead code?
5. Follows the repo's style and conventions?
""",
                "difficulty_min": 2,
                "difficulty_max": 6,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "What is the single most effective way to get your pull request reviewed quickly?",
                        "choices": [
                            "Make it as large as possible so reviewers see everything",
                            "Keep it small and focused — one logical change, ideally under ~400 lines",
                            "Skip the description to save time",
                            "Assign it to the whole company",
                        ],
                        "answer_index": 1,
                        "difficulty": 2,
                        "explanation": "Small, focused PRs are easier to understand and approve, so they move through review fast. Large PRs get deferred because reviewing them is cognitively expensive.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A reviewer writes \"nit: rename `tmp` to `pendingOrders`.\" What does the `nit:` prefix communicate?",
                        "choices": [
                            "The code is broken and must be fixed before merge",
                            "A minor, optional suggestion that does not block approval",
                            "The reviewer is rejecting the PR",
                            "The change requires a security audit",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "`nit:` marks a trivial polish comment — the author can accept or decline it without it blocking the review. Separating nits from blockers keeps reviews efficient.",
                        "company_tags": ["accenture", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which reviewer behavior best matches code-review best practices?",
                        "choices": [
                            "Approving a 2,000-line diff in 30 seconds to unblock the team",
                            "Asking \"What happens if items is empty here?\" on unhandled input",
                            "Commenting \"Fix this\" on every line",
                            "Resolving the author's threads for them",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "Good reviews ask probing questions about behavior and edge cases. Rubber-stamping, commanding tone, and resolving others' threads all undermine the review's value.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "As a PR author, a reviewer leaves a comment you disagree with. What should you do?",
                        "choices": [
                            "Ignore it and merge anyway",
                            "Reply explaining your reasoning and discuss; don't silently resolve their thread",
                            "Delete the comment",
                            "Close the PR and open a new one",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "Disagreement is normal — discuss it in the thread with your reasoning. Silently resolving someone's comment hides the disagreement and breaks trust in the review process.",
                        "company_tags": ["microsoft", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What should every good PR description include?",
                        "choices": [
                            "Only the Jira ticket number",
                            "What changed, why it changed, and how to test it",
                            "The author's resume and contact info",
                            "A copy of the entire diff",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "What/why/how-to-test gives reviewers context to evaluate the change instead of guessing intent. A ticket number alone forces them to go hunting for context.",
                        "company_tags": ["amazon", "wipro"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "During review you spot a hardcoded API key in the diff. What is the correct response?",
                        "choices": [
                            "Approve and let the author rotate it later",
                            "Block the PR, flag the secret, and require it removed and rotated before merge",
                            "Merge it and open a cleanup ticket for next sprint",
                            "Comment \"nit:\" and approve",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "Secrets in git history are permanent once merged — they must be purged from history and rotated. This is always a blocking issue, never a nit or a later cleanup.",
                        "company_tags": ["google", "microsoft"],
                    },
                ],
            },
            {
                "slug": "git-remote-protected-branches",
                "title": "Protected Branches & Branch Policies",
                "theory_md": """## What is branch protection?

**Branch protection rules** are GitHub settings that prevent direct pushes to
important branches (usually `main`) and enforce quality gates before a merge.
Settings → Branches → Add branch protection rule.

## Common protections on main

- **Require a pull request before merging** — nobody pushes directly; every
  change goes through a PR.
- **Require approvals** — e.g. at least 1-2 approving reviews.
- **Require status checks to pass** — CI must be green (tests, lint, build).
- **Require conversation resolution** — all review threads must be resolved.
- **Require linear history** — no merge commits; PRs must be squashed or
  rebased.
- **Restrict who can push** — limit bypass to specific teams.

## CODEOWNERS

A `CODEOWNERS` file at the repo root (or `.github/CODEOWNERS`) auto-assigns
reviewers by path:

```
# .github/CODEOWNERS
*.js        @org/frontend-team
/docs/      @org/tech-writers
/db/        @org/db-admins
```

Anyone touching those paths automatically requests review from the owners.

## Why teams enforce this

Protection rules make the PR workflow *mandatory* rather than optional:
main stays green, every change is reviewed and tested, and history stays
clean. Bypass permissions are kept rare and audited.

## Checking the rules

If a push is rejected with "protected branch hook declined", check the
repo's Settings → Branches or ask a maintainer — the rule set, not your
credentials, is usually the cause.
""",
                "difficulty_min": 3,
                "difficulty_max": 7,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "What is the main purpose of branch protection rules on `main`?",
                        "choices": [
                            "To hide the code from contributors",
                            "To prevent direct pushes and enforce review + CI gates before merging",
                            "To make the branch read-only forever",
                            "To delete old branches automatically",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "Protection rules turn the PR workflow into an enforced policy: every change to main must be reviewed and pass checks, which keeps the default branch stable.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your `git push origin main` is rejected with \"protected branch hook declined\". What does this most likely mean?",
                        "choices": [
                            "Your SSH key is expired",
                            "A branch protection rule forbids direct pushes to main — use a PR",
                            "GitHub is down",
                            "Your local repo is corrupted",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "That specific message comes from GitHub's server-side protection hooks, not from auth. It means the repo policy blocks direct pushes; the fix is a pull request.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does a `CODEOWNERS` file do?",
                        "choices": [
                            "Lists who wrote each line of code historically",
                            "Auto-requests reviews from specified users/teams based on changed file paths",
                            "Grants admin access to the repo",
                            "Defines the license of the project",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "CODEOWNERS maps path patterns to owners, so PRs touching those paths automatically request review from the right people — the domain experts for that code.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A repo requires \"linear history\" on main. Which merge approach does this rule forbid?",
                        "choices": [
                            "Squash and merge",
                            "Rebase and merge",
                            "Merge commits",
                            "Fast-forward-only pushes",
                        ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "Linear history means no merge commits — every commit on main has exactly one parent. Squash and rebase merges satisfy this; regular merge commits violate it.",
                        "company_tags": ["microsoft", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why would a team enable \"Require conversation resolution\" before merging?",
                        "choices": [
                            "To make PRs merge faster",
                            "To ensure no reviewer concern is left unaddressed when code lands",
                            "To reduce the number of reviewers",
                            "To skip CI checks",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "Unresolved threads often hide real objections. Requiring resolution forces every concern to be answered or fixed before the code reaches main.",
                        "company_tags": ["amazon", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "In `CODEOWNERS`, you write `*.js @org/frontend-team`. A PR changes `app/main.py` and `ui/app.js`. Who is auto-requested?",
                        "choices": [
                            "Nobody — patterns only match the repo root",
                            "Only @org/frontend-team, because ui/app.js matches *.js",
                            "@org/frontend-team for both files",
                            "The PR author",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "CODEOWNERS patterns match anywhere in the repo unless anchored with `/`, so `*.js` matches `ui/app.js`. `main.py` matches no rule, so only the frontend team is requested.",
                        "company_tags": ["google", "microsoft"],
                    },
                ],
            },
        ],
    },
    {
        "slug": "github-actions",
        "name": "GitHub Actions",
        "description": "Automate CI/CD with workflows: triggers, jobs, secrets, caching, and full deployment pipelines.",
        "lessons": [
            {
                "slug": "github-actions-cicd-concepts",
                "title": "CI/CD Concepts",
                "theory_md": """## Continuous Integration (CI)

**CI** means every change is automatically built and tested when pushed or
proposed in a PR. Instead of discovering breakage at release time, the team
learns within minutes.

## Continuous Delivery / Deployment (CD)

- **Continuous Delivery**: every passing build is *ready* to release, but a
  human clicks the final deploy button.
- **Continuous Deployment**: every passing build deploys to production
  *automatically* — no human in the loop.

## Why it matters

- **Fast feedback**: failing tests are reported on the PR, not after release.
- **Repeatability**: the same steps run the same way every time — no "works on
  my machine".
- **Confidence**: small, frequent, verified changes are safer than big-bang
  releases.

## CI/CD in GitHub Actions

GitHub Actions runs your pipeline on GitHub-hosted (or self-hosted) machines
called **runners**, triggered by repo events. A passing pipeline typically
runs:

1. **Build** — compile / install dependencies
2. **Test** — unit + integration tests
3. **Lint** — style and static checks
4. **Deploy** — ship to staging or production

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test
```

If any step fails, the whole job fails and the PR shows a red ✗.
""",
                "difficulty_min": 1,
                "difficulty_max": 5,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "What is Continuous Integration (CI)?",
                        "choices": [
                            "Deploying to production every hour",
                            "Automatically building and testing every change when it is pushed or proposed",
                            "Writing code continuously without breaks",
                            "Merging all branches once a year",
                        ],
                        "answer_index": 1,
                        "difficulty": 1,
                        "explanation": "CI automatically builds and tests each change on push/PR, so breakage is caught within minutes rather than at release time.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What distinguishes Continuous Deployment from Continuous Delivery?",
                        "choices": [
                            "Deployment uses more servers",
                            "Deployment releases automatically on every passing build; Delivery keeps a human approval step",
                            "Delivery is faster than Deployment",
                            "They are the same thing",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "Both require every build to be releasable. Delivery pauses for a manual go-ahead; Deployment ships automatically — the human step is the only difference.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why does CI eliminate most \"works on my machine\" problems?",
                        "choices": [
                            "It bans local development",
                            "Every change runs the same steps in a fresh, standardized environment",
                            "It runs tests on the developer's laptop",
                            "It deletes local environments",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "CI runners start clean and follow the workflow file exactly, so environment-specific quirks of a developer's laptop cannot hide broken builds.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "In a typical CI pipeline, what order do build → test → lint → deploy follow, and why?",
                        "choices": [
                            "Deploy first to fail fast",
                            "Build, then test, then lint, then deploy — each stage gates the next so broken code never ships",
                            "Lint last because style doesn't matter",
                            "Order is random and irrelevant",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "Pipeline stages are gates: if build or test fails, the job stops and nothing deploys. Ordering verification before deployment guarantees only proven code ships.",
                        "company_tags": ["microsoft", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A PR shows a red ✗ on its checks. What does that tell a reviewer?",
                        "choices": [
                            "The PR was approved",
                            "At least one CI step failed — the change should not merge until it is green",
                            "The PR is a draft",
                            "The reviewer must merge immediately",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "Red checks mean the automated pipeline failed. Combined with branch protection requiring green checks, the PR is blocked until the failure is fixed.",
                        "company_tags": ["google", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A team moves from monthly big-bang releases to CI with small daily merges. Which risk does this primarily reduce?",
                        "choices": [
                            "Server hardware failure",
                            "The blast radius of each change — bugs are isolated to small diffs and caught fast",
                            "Hiring costs",
                            "Internet outages",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "Small frequent changes mean each failure maps to a tiny diff, making root-causing trivial and rollbacks cheap — the core safety argument for CI/CD.",
                        "company_tags": ["google", "microsoft"],
                    },
                ],
            },
            {
                "slug": "github-actions-yaml-basics",
                "title": "YAML Basics for Workflows",
                "theory_md": """## YAML: the language of workflows

GitHub Actions workflows are YAML files in `.github/workflows/`. YAML is
indentation-sensitive — **spaces only, never tabs** — and structure is defined
by nesting.

## Core syntax

```yaml
name: CI                      # workflow name (string)
on: [push]                    # trigger (list)

env:                          # mapping: key-value pairs
  NODE_VERSION: "20"

jobs:                         # mapping of job id -> job
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Run tests      # list item (dash)
        run: npm test        # a shell command
```

## Key YAML rules

- **Indentation** (2 spaces conventionally) defines nesting. Misaligned lines
  are the #1 cause of "workflow not appearing".
- **Lists** use `- ` (dash + space); **mappings** use `key: value`.
- **Strings**: quote values that look like numbers or booleans:
  `version: \"20\"` not `version: 20` (YAML would parse `20` as a number, and
  `on`/`off`/`yes`/`no` as booleans!).
- **Comments** start with `#`.
- **Multiline strings** use `|` (literal block):

```yaml
run: |
  npm ci
  npm test
```

## The `on` key gotcha

`on` unquoted can be parsed as boolean `true` by some YAML parsers. GitHub
handles `on:` fine in workflow files, but quoting (`\"on\"`) is the safe
habit in reusable YAML snippets.
""",
                "difficulty_min": 1,
                "difficulty_max": 5,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "In YAML, what does indentation control?",
                        "choices": [
                            "Nothing — it is cosmetic",
                            "The nesting/structure of the data",
                            "The execution order of steps",
                            "The font size in the GitHub UI",
                        ],
                        "answer_index": 1,
                        "difficulty": 1,
                        "explanation": "YAML has no braces; indentation alone defines which keys belong to which parent. Wrong indentation silently changes the structure or breaks parsing.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your workflow file doesn't show up in the Actions tab. What is the most likely cause?",
                        "choices": [
                            "The repo is private",
                            "An indentation or syntax error in the YAML",
                            "You need to restart GitHub",
                            "Workflows only appear on weekends",
                        ],
                        "answer_index": 1,
                        "difficulty": 2,
                        "explanation": "GitHub silently ignores workflow files that fail YAML parsing — and the overwhelmingly common cause is bad indentation. Validate the YAML before anything else.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why should you write `NODE_VERSION: \"20\"` with quotes instead of `NODE_VERSION: 20`?",
                        "choices": [
                            "Quotes make it run faster",
                            "Unquoted 20 is parsed as a number, which can break string-only contexts",
                            "GitHub requires all values quoted",
                            "There is no difference",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "YAML auto-types unquoted scalars: `20` becomes an integer. Action inputs expecting strings can then misbehave, so quoting version-like values is the safe habit.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does the `|` (literal block scalar) do in this step?\n```yaml\nrun: |\n  npm ci\n  npm test\n```",
                        "choices": [
                            "Runs the commands in parallel",
                            "Passes both lines as one multiline shell script, preserving line breaks",
                            "Comments out the second line",
                            "Pipes npm ci output into npm test",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "`|` keeps newlines, so the runner receives a two-line shell script executed top to bottom. Without it you'd need awkward quoting to run multiple commands.",
                        "company_tags": ["microsoft", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "In YAML, what is the difference between `- run: npm test` (a list item) and `run: npm test` (a mapping key)?",
                        "choices": [
                            "No difference",
                            "The dash makes it an element of the steps list; without it, it's a key-value pair — steps must be a list of step mappings",
                            "The dash version runs twice",
                            "The dash is only for comments",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "`steps:` must be a sequence, and each step is a mapping inside it. The `-` starts each list element; omitting it breaks the expected schema and the workflow is invalid.",
                        "company_tags": ["google", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why is `on` (the workflow trigger key) considered a YAML gotcha?",
                        "choices": [
                            "It is a reserved GitHub keyword that can't be used",
                            "Some YAML parsers interpret unquoted `on` as boolean true, so quoting it is the safe habit",
                            "It must always be written in uppercase",
                            "It only works on Tuesdays",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "Per YAML 1.1, `on`/`off`/`yes`/`no` are booleans. GitHub's parser tolerates `on:`, but other tools may read it as `true:` — quoting avoids the ambiguity entirely.",
                        "company_tags": ["google", "microsoft"],
                    },
                ],
            },
            {
                "slug": "github-actions-triggers",
                "title": "Workflow Triggers",
                "theory_md": """## Events that start workflows

The `on:` key declares **which events** trigger the workflow. Files live in
`.github/workflows/*.yml`.

## The big four triggers

```yaml
on:
  push:                       # any push to the repo
    branches: [main]          # ...but only to main
  pull_request:               # PR opened, synchronized, reopened
    types: [opened, synchronize]
  schedule:                   # cron — runs on a timer
    - cron: "0 6 * * *"       # daily at 06:00 UTC
  workflow_dispatch:          # manual "Run workflow" button in the UI
```

## Trigger details

- **`push`** — fires on every push. Filter with `branches:`, `tags:`, or
  `paths:` (e.g. only when `src/**` changes) to avoid wasted runs.
- **`pull_request`** — the CI gate for PRs. Common types: `opened`,
  `synchronize` (new commits pushed), `reopened`.
- **`schedule`** — cron syntax, always in **UTC**. Minimum granularity is
  5 minutes; scheduled runs use the default branch.
- **`workflow_dispatch`** — adds a manual Run button; can accept `inputs:`
  (text, choice, boolean) that become `${{ inputs.<name> }}`.

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: "Target environment"
        type: choice
        options: [staging, production]
        default: staging
```

## Combining triggers

Multiple triggers = multiple entry points to the same workflow. `on: [push,
pull_request]` is the classic CI combo: validate every push and every PR.
""",
                "difficulty_min": 2,
                "difficulty_max": 6,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "What does `on: [push, pull_request]` mean?",
                        "choices": [
                            "The workflow runs only when a PR is merged",
                            "The workflow runs on every push and on PR events (opened, updated)",
                            "The workflow pushes code to a PR",
                            "The workflow runs once, then deletes itself",
                        ],
                        "answer_index": 1,
                        "difficulty": 2,
                        "explanation": "Multiple triggers are OR'd: the workflow runs whenever ANY listed event occurs. Push + pull_request is the standard CI combo covering both direct pushes and PRs.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You want a nightly test run at 2 AM. Which trigger do you use, and in which timezone is the schedule evaluated?",
                        "choices": [
                            "schedule with cron, evaluated in UTC",
                            "workflow_dispatch with a timer",
                            "push with a delay",
                            "schedule with cron, evaluated in your local timezone",
                        ],
                        "answer_index": 0,
                        "difficulty": 4,
                        "explanation": "`schedule` uses cron expressions and GitHub always evaluates them in UTC. For 2 AM IST you'd write the equivalent UTC cron (`30 20 * * *`).",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What is `workflow_dispatch` used for?",
                        "choices": [
                            "Automatically dispatching emails",
                            "Adding a manual \"Run workflow\" button in the Actions UI, optionally with inputs",
                            "Dispatching runners to other repos",
                            "Skipping CI on demand",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "workflow_dispatch makes a workflow manually runnable from the GitHub UI/API, with optional typed inputs — perfect for on-demand deploys or maintenance tasks.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your CI runs on every push, including docs-only commits, wasting runner minutes. What is the cleanest fix?",
                        "choices": [
                            "Delete the workflow",
                            "Add a paths filter so it only runs when relevant files change",
                            "Make the repo private",
                            "Run CI on a slower runner",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "`on.push.paths: ['src/**']` (or `paths-ignore` for docs) scopes the trigger to relevant changes — the standard way to cut wasted CI minutes without losing coverage.",
                        "company_tags": ["microsoft", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "In `on: pull_request: types: [opened, synchronize]`, what event does `synchronize` cover?",
                        "choices": [
                            "The PR being merged",
                            "New commits pushed to the PR's branch",
                            "Two PRs being merged together",
                            "The base branch changing",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "`synchronize` fires when the PR's head branch gets new commits. Without it, CI would run on PR creation but never re-run after the author pushes fixes.",
                        "company_tags": ["google", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A scheduled workflow uses the cron `0 6 * * *` but you notice it sometimes runs several minutes late. Why is this expected?",
                        "choices": [
                            "Cron syntax is broken in GitHub Actions",
                            "Scheduled runs are best-effort: GitHub queues them and high load can delay execution",
                            "The workflow file has a syntax error",
                            "Schedule only works on private repos",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "GitHub documents that scheduled workflows may be delayed during periods of high load — cron triggers request a run, they don't guarantee exact start times.",
                        "company_tags": ["google", "microsoft"],
                    },
                ],
            },
            {
                "slug": "github-actions-jobs-steps-runners",
                "title": "Jobs, Steps & Runners",
                "theory_md": """## The hierarchy: workflow → jobs → steps

```yaml
jobs:
  build:                    # job id
    runs-on: ubuntu-latest  # runner image
    steps:
      - uses: actions/checkout@v4
      - name: Install deps
        run: npm ci
      - name: Run tests
        run: npm test
```

- A **workflow** is the whole file.
- A **job** is a set of steps that run on the **same runner**. Jobs run in
  **parallel by default**.
- A **step** is a single task: either `run:` (shell command) or `uses:`
  (a reusable action).

## Runners

`runs-on:` picks the VM image:

```yaml
runs-on: ubuntu-latest    # Linux (most common, cheapest)
runs-on: windows-latest
runs-on: macos-latest
```

Each job gets a **fresh VM** — nothing persists between jobs unless you use
artifacts or caching.

## Job dependencies with needs

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: npm test
  deploy:
    needs: test            # wait for test to succeed
    runs-on: ubuntu-latest
    steps:
      - run: npm run deploy
```

`needs:` makes jobs sequential and skips dependents if the dependency fails.

## Matrix builds

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node: [18, 20, 22]
    steps:
      - run: npm test
        env:
          NODE: ${{ matrix.node }}
```

One job definition × 3 matrix values = 3 parallel jobs. Ideal for testing
across versions or OSes.
""",
                "difficulty_min": 2,
                "difficulty_max": 6,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "By default, how do multiple jobs in a workflow execute?",
                        "choices": [
                            "Sequentially, in file order",
                            "In parallel, each on its own fresh runner",
                            "Only one job ever runs",
                            "Alphabetically by job id",
                        ],
                        "answer_index": 1,
                        "difficulty": 2,
                        "explanation": "Jobs are independent and parallel by default — each gets a fresh runner. You opt into sequencing explicitly with `needs:`.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What is the difference between a step with `run:` and a step with `uses:`?",
                        "choices": [
                            "run executes shell commands; uses runs a reusable published action",
                            "They are identical",
                            "run is faster",
                            "uses only works on Windows",
                        ],
                        "answer_index": 0,
                        "difficulty": 3,
                        "explanation": "`run:` steps execute shell commands inline; `uses:` steps invoke a packaged action (like actions/checkout) that someone published for reuse.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You write a file in job `build` and try to read it in job `deploy`. It is missing. Why?",
                        "choices": [
                            "Files are deleted after 1 minute",
                            "Each job runs on a fresh runner — filesystems are not shared between jobs",
                            "You need sudo to share files",
                            "YAML doesn't support files",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "Jobs are isolated VMs. To pass data between jobs you must upload it as an artifact in one job and download it in the other.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does `needs: test` on the `deploy` job accomplish?",
                        "choices": [
                            "It runs test and deploy at the same time",
                            "It makes deploy wait for test to succeed, and skips deploy if test fails",
                            "It copies test's logs into deploy",
                            "It renames the job to test",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "`needs` creates a dependency: deploy only starts after test completes successfully, and is skipped entirely if test fails — the standard build→test→deploy gate.",
                        "company_tags": ["microsoft", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A matrix strategy lists `node: [18, 20, 22]`. How many jobs run, and how?",
                        "choices": [
                            "1 job that tests 3 versions sequentially",
                            "3 parallel jobs, one per Node version",
                            "22 jobs",
                            "0 — matrix is documentation only",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "The matrix fans out: GitHub creates one job per combination (here 3), running in parallel, with `${{ matrix.node }}` resolving to each value.",
                        "company_tags": ["google", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why is `runs-on: ubuntu-latest` the most common choice for CI jobs?",
                        "choices": [
                            "It is the only free option",
                            "Linux runners are the cheapest/fastest for most build toolchains and match typical deployment targets",
                            "GitHub requires Linux for all workflows",
                            "Windows runners cannot run YAML",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "Most server toolchains are Linux-first, ubuntu runners are the most economical, and testing on the same OS family you deploy to catches environment bugs early.",
                        "company_tags": ["google", "microsoft"],
                    },
                ],
            },
            {
                "slug": "github-actions-using-actions",
                "title": "Using Actions (checkout, setup-*)",
                "theory_md": """## Reusable actions

An **action** is a packaged, reusable step published to the GitHub
Marketplace (or any repo). You reference it with `uses:` plus a version:

```yaml
steps:
  - uses: actions/checkout@v4
```

**Always pin to a version** (`@v4`, or a full SHA for maximum safety).
Unpinned (`@main`) actions can change behavior under you.

## The essential actions

```yaml
steps:
  # 1. Check out your code (without this, the runner has an empty workspace!)
  - uses: actions/checkout@v4

  # 2. Set up a language toolchain
  - uses: actions/setup-node@v4
    with:
      node-version: "20"
      cache: npm

  - uses: actions/setup-python@v5
    with:
      python-version: "3.12"

  - uses: actions/setup-java@v4
    with:
      distribution: temurin
      java-version: "21"
```

## `with:` — action inputs

`with:` passes parameters defined by the action. Each action documents its
inputs; unknown keys are ignored (a common source of "why isn't this
working").

## Third-party actions

```yaml
- uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKER_USER }}
    password: ${{ secrets.DOCKER_PASS }}
```

Prefer actions from verified creators, pin versions, and review what a
third-party action does — it runs with your repo's permissions.

## Why checkout is always first

Runners start with an **empty workspace**. Without `actions/checkout`, there
is no code to build or test — the most common beginner workflow bug.
""",
                "difficulty_min": 2,
                "difficulty_max": 6,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Why is `actions/checkout` almost always the first step in a job?",
                        "choices": [
                            "It installs Git on the runner",
                            "Runners start with an empty workspace — checkout clones your repo so there is code to work on",
                            "It is required by GitHub's terms of service",
                            "It speeds up the runner",
                        ],
                        "answer_index": 1,
                        "difficulty": 2,
                        "explanation": "A fresh runner has no files. Without checkout, build/test steps run against an empty directory and fail — the classic beginner mistake.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does the `with:` block do in a `uses:` step?",
                        "choices": [
                            "It lists the files to ignore",
                            "It passes input parameters to the action",
                            "It defines environment variables for all jobs",
                            "It sets the runner OS",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "`with:` supplies the action's declared inputs (like `node-version`). Each action documents its own inputs; misspelled keys are silently ignored.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why should you write `actions/checkout@v4` instead of `actions/checkout@main`?",
                        "choices": [
                            "main is slower",
                            "Pinning to a version prevents unexpected breaking changes when the action's default branch updates",
                            "v4 is required for private repos",
                            "There is no reason; both are identical",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "Branches like `main` move. Pinning `@v4` (or a SHA) locks the behavior you tested, so an upstream change can't silently break your pipeline.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does `actions/setup-node@v4` with `node-version: \"20\"` actually do on the runner?",
                        "choices": [
                            "It deploys your app to Node hosting",
                            "It installs the specified Node.js toolchain and adds it to PATH",
                            "It writes your package.json",
                            "It opens a Node REPL",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "Setup actions provision the language runtime on the fresh runner (download, install, PATH configuration) so subsequent `run:` steps can use `node`/`npm`.",
                        "company_tags": ["microsoft", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You pass `with: { nod-version: \"20\" }` (typo) to setup-node and the workflow uses the wrong Node version with no error. Why no error?",
                        "choices": [
                            "GitHub auto-corrects typos",
                            "Unknown `with:` keys are silently ignored by actions",
                            "Typos are only warnings in YAML",
                            "The action defaults to v20 anyway",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "Actions only read the inputs they declare; anything else in `with:` is ignored without complaint. This silent behavior makes typos in input names notoriously hard to spot.",
                        "company_tags": ["google", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Before using a third-party action like `docker/login-action@v3`, what security practice matters most?",
                        "choices": [
                            "Forking it first",
                            "Verifying the publisher, pinning the version, and checking what permissions it needs — it runs with your repo's credentials",
                            "Only using it on weekends",
                            "Renaming it",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "Third-party actions execute arbitrary code with your workflow's token. A compromised or over-permissioned action can exfiltrate secrets — vet the source and pin the version.",
                        "company_tags": ["google", "microsoft"],
                    },
                ],
            },
            {
                "slug": "github-actions-secrets-environments",
                "title": "Secrets & Environments",
                "theory_md": """## Secrets

**Secrets** store sensitive values (API keys, tokens, passwords) encrypted.
Set them in Settings → Secrets and variables → Actions. Reference them as:

```yaml
steps:
  - run: npm run deploy
    env:
      API_KEY: ${{ secrets.API_KEY }}
```

Secrets are **masked in logs** — if a step prints one, GitHub shows `***`.

## Rules of secrets

- **Never echo secrets** or put them in code. Masking is a safety net, not a
  guarantee (crafted output can sometimes leak them).
- Secrets are **not passed to workflows from fork PRs** by default — a
  security measure against exfiltration via malicious PRs.
- Use the **least-privilege `GITHUB_TOKEN`**: the automatic token's
  permissions default broadly, so scope them down per job:

```yaml
permissions:
  contents: read
```

## Environments

**Environments** (Settings → Environments) group secrets/variables per
deployment target (`staging`, `production`) and add **protection rules**:

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production   # uses production's secrets + rules
    steps:
      - run: ./deploy.sh
```

- **Required reviewers**: a human must approve before the job runs.
- **Wait timer**: delay before deployment proceeds.
- **Deployment branches**: only `main` may deploy to production.

## Secrets vs variables

- **Secrets**: encrypted, masked in logs (tokens, keys).
- **Variables**: plain config, visible in logs (region names, feature flags).
""",
                "difficulty_min": 3,
                "difficulty_max": 7,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "How do you reference a repository secret named `API_KEY` inside a workflow?",
                        "choices": [
                            "$API_KEY",
                            "${{ secrets.API_KEY }}",
                            "secrets.API_KEY",
                            "{{ secrets[API_KEY] }}",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "The `${{ }}` expression syntax evaluates contexts; `secrets.API_KEY` reads the encrypted secret. The other forms are not valid GitHub expressions.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A workflow step accidentally prints a secret to the log. What does GitHub show?",
                        "choices": [
                            "The raw secret value",
                            "The secret masked as ***",
                            "An empty line",
                            "The workflow is deleted",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "GitHub scans logs for known secret values and replaces them with `***`. Still, don't rely on masking — avoid printing secrets at all.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why are secrets NOT available to workflows triggered by pull requests from forks?",
                        "choices": [
                            "Forks don't support YAML",
                            "To prevent a malicious PR from exfiltrating secrets via modified workflow code",
                            "It is a bug in GitHub Actions",
                            "Secrets only work on main",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "Anyone can fork and open a PR; if secrets were exposed, an attacker could edit the workflow to print them. Withholding secrets from fork PRs closes that exfiltration path.",
                        "company_tags": ["amazon", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What protection can a GitHub Environment add that plain repository secrets cannot?",
                        "choices": [
                            "Stronger encryption",
                            "Required human reviewers and wait timers before deployment jobs run",
                            "Unlimited secret storage",
                            "Faster runners",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "Environments add deployment gates — manual approvals, delays, branch restrictions — around the secrets they hold. Plain repo secrets have no such gating.",
                        "company_tags": ["microsoft", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "When should a value be a Variable rather than a Secret?",
                        "choices": [
                            "When it is a password",
                            "When it is non-sensitive config (like a region name) that is fine to appear in logs",
                            "When it is an API key",
                            "Variables and secrets are interchangeable",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "Variables are for plain configuration visible in logs; secrets are for sensitive values that get encrypted and masked. Using secrets for everything hides useful debugging info.",
                        "company_tags": ["google", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why set `permissions: contents: read` on a job that only runs tests?",
                        "choices": [
                            "It makes tests run faster",
                            "Least privilege: the auto-issued GITHUB_TOKEN gets only the access the job needs, limiting damage if compromised",
                            "It is required for npm",
                            "It enables fork PRs to see secrets",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "The default GITHUB_TOKEN is broader than most jobs need. Scoping permissions down means a compromised step or action can't push code or modify releases.",
                        "company_tags": ["amazon", "microsoft"],
                    },
                ],
            },
            {
                "slug": "github-actions-caching-artifacts",
                "title": "Caching Dependencies & Artifacts",
                "theory_md": """## Caching: skip redundant downloads

**Caching** stores files (like `node_modules` or `~/.m2`) between runs so
`npm ci` doesn't re-download the world every time. The classic action:

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: npm-${{ runner.os }}-${{ hashFiles('package-lock.json') }}
    restore-keys: |
      npm-${{ runner.os }}-
```

- **`key`**: cache identity. Include a hash of the lockfile so the cache
  invalidates exactly when dependencies change.
- **`restore-keys`**: fallback prefixes — reuse an older cache if no exact
  match (better than starting cold).

Many setup actions have caching built in:

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: "20"
    cache: npm        # enables npm caching automatically
```

## Artifacts: pass files between jobs

**Artifacts** persist files beyond a single job/run for download or for
later jobs:

```yaml
# job 1: build
- uses: actions/upload-artifact@v4
  with:
    name: dist
    path: dist/

# job 2: deploy (needs: build)
- uses: actions/download-artifact@v4
  with:
    name: dist
    path: dist/
```

Artifacts also let humans download build outputs (zips, test reports, APKs)
from the run's page.

## Cache vs artifact

| | Cache | Artifact |
|---|---|---|
| Purpose | Speed up repeat runs | Share outputs between jobs / with humans |
| Lifetime | Until key changes or evicted | 90 days default retention |
| Mutability | Immutable per key | New upload per run |

## Cache invalidation

Caches are **immutable**: writing to an existing key is a no-op. Change the
key (via the lockfile hash) to get a fresh cache.
""",
                "difficulty_min": 3,
                "difficulty_max": 7,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "What problem does dependency caching solve in CI?",
                        "choices": [
                            "It fixes failing tests",
                            "It avoids re-downloading dependencies on every run, making builds faster",
                            "It deploys the app",
                            "It encrypts secrets",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "Fresh runners start empty, so installs re-download everything. A warm cache restores dependencies in seconds, cutting build times dramatically.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why does the cache key include `hashFiles('package-lock.json')`?",
                        "choices": [
                            "To encrypt the cache",
                            "So the cache automatically invalidates when dependencies change",
                            "It is required syntax with no effect",
                            "To make the key shorter",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "The key identifies the cache. Hashing the lockfile means any dependency change produces a new key (fresh install), while unchanged deps hit the existing cache.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What are `restore-keys` for in actions/cache?",
                        "choices": [
                            "They delete old caches",
                            "Fallback prefixes: if no exact key match, restore the newest cache with a matching prefix instead of starting cold",
                            "They encrypt the cache",
                            "They list files to cache",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "On a lockfile change there's no exact cache. restore-keys fall back to the previous cache — mostly right, and the job then updates the changed packages only.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Job `build` produces `dist/` and job `deploy` (a different runner) needs it. What is the correct mechanism?",
                        "choices": [
                            "Caching dist/ with actions/cache",
                            "Upload dist/ as an artifact in build and download it in deploy",
                            "Commit dist/ to the repo",
                            "Runners share a filesystem, so just use the path",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "Jobs run on isolated runners, so files must be explicitly transferred. Artifacts are designed for this; caches are for speed, not reliable job-to-job transfer.",
                        "company_tags": ["microsoft", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Caches in GitHub Actions are immutable. What does that imply when dependencies change?",
                        "choices": [
                            "The old cache is updated in place",
                            "You must use a new key — writes to an existing key are ignored",
                            "Caches are deleted automatically",
                            "The workflow fails",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "You cannot overwrite a cache entry; saving with an existing key is a silent no-op. Key rotation (via lockfile hash) is the only way to refresh cached content.",
                        "company_tags": ["google", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A developer caches `node_modules` directly instead of npm's cache directory (`~/.npm`). What is the main risk?",
                        "choices": [
                            "It is always faster",
                            "node_modules contains OS-specific binaries — a cache restored on a different runner OS/arch can break the build",
                            "Caches cannot store node_modules",
                            "There is no risk",
                        ],
                        "answer_index": 1,
                        "difficulty": 8,
                        "explanation": "node_modules may hold platform-specific native bindings. Caching the package manager's download cache (~/.npm) and reinstalling is portable; caching node_modules couples the cache to one OS/arch.",
                        "company_tags": ["google", "microsoft"],
                    },
                ],
            },
            {
                "slug": "github-actions-deployment-pipeline",
                "title": "Deployment Pipeline Example (Build → Test → Deploy)",
                "theory_md": """## Putting it all together

A complete pipeline: build once, test, then deploy to staging and production
with an approval gate.

```yaml
name: Release pipeline

on:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: npm
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: npm
      - run: npm ci
      - run: npm test

  deploy-staging:
    needs: test
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/
      - run: ./deploy.sh staging
        env:
          API_KEY: ${{ secrets.STAGING_API_KEY }}

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production   # required reviewers gate this
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/
      - run: ./deploy.sh production
        env:
          API_KEY: ${{ secrets.PROD_API_KEY }}
```

## Reading the pipeline

1. **build** compiles and uploads `dist/` as an artifact.
2. **test** runs only after build succeeds (`needs:`).
3. **deploy-staging** auto-deploys with staging secrets.
4. **deploy-production** waits for staging, then pauses for a **required
   reviewer** (environment protection) before shipping.

One artifact flows through every stage — the exact bits tested are the bits
deployed. If any job fails, downstream jobs are skipped.
""",
                "difficulty_min": 4,
                "difficulty_max": 8,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "In the example pipeline, why does `deploy-production` use `needs: deploy-staging`?",
                        "choices": [
                            "To run both deploys at the same time",
                            "To enforce order: production only deploys after staging succeeds",
                            "To share the same runner",
                            "It is just documentation",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "`needs` sequences the jobs and gates them: if staging fails, production is skipped. This is the progressive-delivery pattern — prove it in staging first.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why does the pipeline upload `dist/` as an artifact in `build` instead of rebuilding in each deploy job?",
                        "choices": [
                            "Artifacts are free",
                            "So the exact tested bits are what gets deployed — rebuilding risks shipping untested code",
                            "Rebuilding is not possible in Actions",
                            "It saves YAML lines",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "Build-once/deploy-many guarantees the artifact that passed tests is the artifact that ships. Rebuilding per environment could introduce differences (new dependency versions, nondeterminism).",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does `environment: production` add to the deploy-production job?",
                        "choices": [
                            "A faster runner",
                            "Access to production-scoped secrets plus protection rules like required reviewers",
                            "Automatic rollback",
                            "Free unlimited minutes",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "The environment binding injects that environment's secrets and enforces its protection rules — e.g. pausing for a human approval before production deploys.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "If the `test` job fails, what happens to `deploy-staging` and `deploy-production`?",
                        "choices": [
                            "They run anyway",
                            "They are skipped, because needs: chains propagate failure",
                            "Only deploy-production is skipped",
                            "They retry automatically",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "A failed job causes all jobs that `need` it (directly or transitively) to be skipped. The pipeline halts before anything broken can deploy.",
                        "company_tags": ["microsoft", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why does the workflow set top-level `permissions: contents: read`?",
                        "choices": [
                            "To speed up checkout",
                            "Least privilege — the GITHUB_TOKEN gets only read access since no job needs to write",
                            "It is mandatory for all workflows",
                            "To allow fork PRs to push",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "This pipeline only reads code and deploys via its own secrets, so read-only token scope is sufficient. Narrow permissions limit what a compromised step could do.",
                        "company_tags": ["google", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A teammate suggests deploying straight from the `build` job to production to \"save time\". What is the strongest argument against it?",
                        "choices": [
                            "It uses more YAML",
                            "It removes the test gate and the staging verification, so untested code can reach production with no human checkpoint",
                            "Build jobs can't access secrets",
                            "Production deploys must use Windows runners",
                        ],
                        "answer_index": 1,
                        "difficulty": 8,
                        "explanation": "Skipping test and staging destroys the pipeline's safety properties: no verification gate and no progressive rollout. Speed gained is far outweighed by the risk of shipping broken code to users.",
                        "company_tags": ["google", "microsoft"],
                    },
                ],
            },
        ],
    },
]
