"""Seed content: Git & GitHub — Modules 1-2 (Git Fundamentals, Git Branching).

Part-file for the SkillForge curriculum seed. All content is original:
every lesson theory and every question is written from scratch with
real, verifiable git CLI commands in code blocks.

Exports a single variable, ``MODULES``: a list of 2 module dicts, each
with nested lesson dicts and, inside those, question dicts.

Module 1 ``git-fundamentals``      — 8 lessons (VCS concepts, install &
config, init, staging area, add/commit, status/log, .gitignore, undoing).
Module 2 ``git-branching``         — 8 lessons (branches, create/switch,
branching model with visual, merging, conflicts, rebase vs merge, stash,
detached HEAD).
"""
from __future__ import annotations

MODULES = [
    {
        "slug": "git-fundamentals",
        "name": "Git Fundamentals",
        "description": (
            "Version control from zero: what Git is, installing and "
            "configuring it, creating repositories, the staging area, "
            "commits, history, ignoring files, and undoing mistakes."
        ),
        "lessons": [
            {
                "slug": "git-fundamentals-what-is-vcs",
                "title": "What is Version Control?",
                "theory_md": """## What is Version Control?

A **version control system (VCS)** records changes to files over time so
you can recall any specific version later. Think of it as a detailed,
searchable undo history for your whole project — who changed what, when,
and why.

Before version control, developers renamed folders like `project-final`,
`project-final2`, `project-final-FINAL`. A VCS replaces that mess with a
clean, timestamped history.

### The three jobs of a VCS

1. **History** — every change is recorded with an author, date, and message.
2. **Collaboration** — many people can work on the same project without
   overwriting each other.
3. **Recovery** — deleted a file? Broke the build? Go back to the last
   good state in one command.

### Centralized vs distributed

The key distinction every interviewer asks about:

| | Centralized (e.g. SVN, Perforce) | Distributed (e.g. Git, Mercurial) |
|---|---|---|
| History lives... | on one server | in **every** clone |
| Commit offline? | No | **Yes** — commit locally any time |
| Speed | limited by network | local operations are instant |
| Single point of failure | the server | everyone has the full history |

**Git is distributed.** When you `git clone` a project, you download the
*entire* history, not just the latest snapshot. That is why commands like
this work on a plane with no internet:

```bash
git log --oneline     # show local history — no network needed
git status            # compare working tree against the local repo
git diff              # show uncommitted changes
```

A distributed model also changes how teams collaborate: instead of
everyone committing to one server, you commit locally, then push your
finished work up (`git push`) and pull others' work down (`git pull`).

### Real-world analogy

- **Centralized VCS** = a single shared Google Doc. No internet, no work.
- **Distributed VCS** = everyone has their own full copy of the document
  with its own edit history; copies sync up when people are ready.

### What Git does not do

Git tracks **content changes in files** — it does not:

- build your code,
- deploy anything,
- back up files it was never told to track (`git add` first!),
- track empty directories (it tracks file content, not folders).

```bash
git --version    # check that git is installed, e.g. git version 2.43.0
```

**Takeaway:** version control = history + collaboration + recovery. Git is
the distributed leader because everything you do day-to-day happens
locally and fast.
""",
                "difficulty_min": 1,
                "difficulty_max": 5,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "What is the PRIMARY purpose of a version control system?",
                        "choices": [
                            "To compile source code into executable programs",
                            "To record changes to files over time so any version can be recalled later",
                            "To deploy applications to production servers automatically",
                            "To encrypt source code so only team members can read it",
                        ],
                        "answer_index": 1,
                        "difficulty": 1,
                        "explanation": "A VCS records who changed what, when, and why, letting you recall or restore any earlier version. Compilation, deployment, and encryption are separate tools' jobs, not the VCS's purpose.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which statement BEST describes the difference between Git and SVN (Subversion)?",
                        "choices": [
                            "Git is distributed (every clone has the full history), while SVN is centralized (history lives on one server)",
                            "Git can only track Python files while SVN tracks any file type",
                            "SVN is faster than Git because it keeps all data on a central server",
                            "Git requires a paid license while SVN is always free",
                        ],
                        "answer_index": 0,
                        "difficulty": 3,
                        "explanation": "Git is distributed: `git clone` copies the entire history, so local operations like `git log` work offline. SVN is centralized: most operations need to reach the server. The other options mix up facts — both track any file type and both are free.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You are on a flight with no internet. Which of these git commands can you still run successfully in a cloned repository?",
                        "choices": [
                            "git log --oneline and git status",
                            "git push origin main",
                            "git fetch --all",
                            "git clone https://github.com/user/repo.git",
                        ],
                        "answer_index": 0,
                        "difficulty": 2,
                        "explanation": "`git log` and `git status` only read your LOCAL clone, which contains the full history — the whole point of a distributed VCS. Push, fetch, and clone all need network access to a remote server.",
                        "company_tags": ["tcs", "wipro"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A teammate says: \"I committed my changes but my coworker can't see them.\" What is the most likely explanation?",
                        "choices": [
                            "They need to run `git config` again before committing",
                            "A local commit stays on their machine until they `git push` it to the shared remote",
                            "Git automatically pushes every commit within 5 minutes",
                            "The coworker needs to delete their local repository first",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "In Git, `commit` writes to the LOCAL repository only; `push` publishes commits to the remote. This is the direct consequence of the distributed model — local history and shared history are separate until you sync them.",
                        "company_tags": ["infosys", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which of the following is NOT something Git does?",
                        "choices": [
                            "Records who changed which lines and when",
                            "Lets you restore a file to an earlier version",
                            "Tracks an empty directory that contains no files",
                            "Merges work from multiple contributors",
                        ],
                        "answer_index": 2,
                        "difficulty": 3,
                        "explanation": "Git tracks file CONTENT, not directories — an empty folder is invisible to Git (people add a placeholder `.gitkeep` file as a workaround). Recording history, restoring versions, and merging collaboration are core VCS jobs.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why is there no single point of failure in a distributed VCS like Git, unlike a centralized system?",
                        "choices": [
                            "Git stores everything in the cloud instead of on a server",
                            "Every clone contains the complete history, so any developer's machine can restore the project",
                            "Git never deletes old versions of files",
                            "Distributed systems use a blockchain for every commit",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "Because each clone carries the full history (all commits, branches, tags), the project survives even if the central server is lost — anyone's clone can become the new source of truth. That's the resilience advantage of distributed version control.",
                        "company_tags": ["microsoft", "google"],
                    },
                ],
            },
            {
                "slug": "git-fundamentals-installing-and-config",
                "title": "Installing & Configuring Git",
                "theory_md": """## Installing & Configuring Git

Before your first commit, Git needs two things: to be **installed**,
and to know **who you are** (every commit records its author).

### Install and verify

```bash
# Debian/Ubuntu
sudo apt install git

# macOS (with Homebrew)
brew install git

# Windows: download from https://git-scm.com and run the installer

# Verify the install worked
git --version
# git version 2.43.0
```

### Tell Git who you are (required!)

Git bakes your identity into every commit. Set it once per machine:

```bash
git config --global user.name "Mohit Baghel"
git config --global user.email "mohit@example.com"
```

- `--global` writes to `~/.gitconfig` — applies to **all** your repos.
- Omit `--global` to set identity for **just the current repo**
  (useful when work and personal emails differ):

```bash
cd ~/workspace/work-project
git config user.email "mohit@company.com"
```

### Check what is actually set

```bash
git config --list            # show everything git currently uses
git config user.name         # show just the name
git config --global --list   # show only global-level settings
```

Git reads settings in layers — **local beats global beats system**:
`system (/etc/gitconfig)` < `global (~/.gitconfig)` < `local (.git/config)`.

### Useful first-day settings

```bash
# Set main as the default branch name for new repos (avoid 'master')
git config --global init.defaultBranch main

# Make git diff / log output readable with colors
git config --global color.ui auto

# A friendlier editor for commit messages (if you dislike vim)
git config --global core.editor "code --wait"
```

### Common interview gotcha

Forgetting `user.name`/`user.email` means commits get authored by
whoever the machine thinks you are (or Git refuses to commit and prints
an error). When every commit on a team shows `root@localhost`, someone
skipped `git config`.

**Takeaway:** install Git, run the two `git config --global` commands,
and verify with `git config --list`. Two minutes now saves confusing
history later.
""",
                "difficulty_min": 1,
                "difficulty_max": 5,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Which two commands set your identity for every Git repository on the machine?",
                        "choices": [
                            "`git config --global user.name \"Name\"` and `git config --global user.email \"a@b.com\"`",
                            "`git set identity --name \"Name\" --email \"a@b.com\"`",
                            "`git init --author \"Name <a@b.com>\"`",
                            "`git user --add \"Name\" \"a@b.com\"`",
                        ],
                        "answer_index": 0,
                        "difficulty": 1,
                        "explanation": "`git config --global user.name` and `user.email` are THE real commands — every commit embeds these as author metadata. The other three commands do not exist in Git.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does the `--global` flag in `git config --global user.email` mean?",
                        "choices": [
                            "The setting applies to all users on the computer",
                            "The setting is pushed to GitHub for all repositories",
                            "The setting is stored in ~/.gitconfig and applies to every repo of the current user",
                            "The setting is valid for only the next 24 hours",
                        ],
                        "answer_index": 2,
                        "difficulty": 2,
                        "explanation": "`--global` writes to `~/.gitconfig`, the current user's machine-wide config. It's not per-system, not synced to GitHub, and never expires.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You want your work laptop to use `mohit@company.com` for the current project only, but keep your personal email everywhere else. Which command does this?",
                        "choices": [
                            "`git config --global user.email \"mohit@company.com\"`",
                            "`git config user.email \"mohit@company.com\"` (run inside the project)",
                            "`git config --system user.email \"mohit@company.com\"`",
                            "`git email --set-local \"mohit@company.com\"`",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "Without `--global` (run inside a repo), the setting is written to that repo's `.git/config` and overrides the global value just there — Git's precedence is local > global > system. `--system` would affect all users, and the last option doesn't exist.",
                        "company_tags": ["amazon", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which command shows you the effective Git configuration Git will actually use right now?",
                        "choices": [
                            "`git config --list`",
                            "`git show config`",
                            "`git config --display`",
                            "`git status --config`",
                        ],
                        "answer_index": 0,
                        "difficulty": 3,
                        "explanation": "`git config --list` prints every key=value Git has resolved across system, global, and local files — exactly what commands will use. The other three are not real git commands.",
                        "company_tags": ["infosys", "tcs"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why does it matter if a developer never sets `user.name` and `user.email`?",
                        "choices": [
                            "Git will refuse to push but still commits fine",
                            "Commits get authored with wrong or placeholder identity, making history untrustworthy",
                            "Git repositories become read-only",
                            "It has no effect; Git fills in correct values automatically",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "Author identity is baked into each commit object permanently — `git log` will show `root@localhost` or the machine username forever on those commits. This breaks accountability in team history; in fact, modern Git errors out on commit if identity is entirely unset.",
                        "company_tags": ["google", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A fresh `git init` on your machine creates new repos with branch `master`, but your team standard is `main`. Which setting fixes this permanently?",
                        "choices": [
                            "`git config --global init.defaultBranch main`",
                            "`git config --global branch.default main`",
                            "`git branch --rename master main` run in every repo",
                            "`git init --branch main --global`",
                        ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "`init.defaultBranch` (added in Git 2.28) sets the initial branch name for all future `git init` calls — the real, persistent fix. The other commands either don't exist or only fix one repo at a time.",
                        "company_tags": ["microsoft", "flipkart"],
                    },
                ],
            },
            {
                "slug": "git-fundamentals-git-init",
                "title": "Starting a Repository: git init",
                "theory_md": """## Starting a Repository: git init

A Git repository is just a folder whose history Git is tracking. You
create one in two ways: **`git init`** (start tracking an existing
folder) or **`git clone`** (copy an existing remote repo).

### git init — start from scratch

```bash
mkdir my-app && cd my-app
git init
# Initialized empty Git repository in /home/mohit/my-app/.git/
```

What happened? Git created a hidden `.git/` directory. That directory
**is** the repository — all commits, branches, and history live there.
Your files stay right where they are; `.git/` sits alongside them.

```bash
ls -la          # you will see a .git/ directory now
git status      # "No commits yet" — an empty repo with zero history
```

### Set the first branch name

New repos on older Git versions start on `master`. Standard practice
today is `main`:

```bash
git init -b main        # init AND name the first branch main (Git 2.28+)
```

Or rename afterwards:

```bash
git branch -M main      # force-rename the current branch to main
```

### What NOT to do

- **Never `git init` inside an existing repo.** Running `git init` in a
  subfolder creates a *nested* repository — the outer repo will ignore
  the inner one (or treat it oddly). One repo per project root.
- **Never commit the `.git/` directory itself** or edit files inside it
  by hand. It is Git's private database; use Git commands to change it.

### git clone — the other way in

```bash
git clone https://github.com/user/skillforge.git
# creates ./skillforge with full history, remote 'origin' configured
```

`clone` = `init` + download entire history + set up the remote for you.

### Bare minimum first-repo flow

```bash
git init -b main
git add .
git commit -m "Initial commit"
```

**Takeaway:** `git init` turns any folder into a repo by creating `.git/`.
Treat `.git/` as Git's private database — talk to it only through Git
commands.
""",
                "difficulty_min": 1,
                "difficulty_max": 6,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "What does `git init` actually do?",
                        "choices": [
                            "Downloads the latest code from GitHub",
                            "Creates a hidden `.git/` directory that will hold the repo's history and metadata",
                            "Commits all files in the folder automatically",
                            "Creates a new branch called main",
                        ],
                        "answer_index": 1,
                        "difficulty": 1,
                        "explanation": "`git init` creates the `.git/` directory — Git's private database for commits, branches, and history — in the current folder. It doesn't download anything, commit anything, or create branches by itself.",
                        "company_tags": ["tcs", "wipro"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "How do you initialize a new repository whose first branch is named `main` in one command?",
                        "choices": [
                            "`git init -b main`",
                            "`git init --first-branch main`",
                            "`git create --branch main`",
                            "`git init` followed by `git branch main`",
                        ],
                        "answer_index": 0,
                        "difficulty": 2,
                        "explanation": "`git init -b main` (Git 2.28+) initializes the repo and names the unborn first branch `main` in one step — a real flag. The alternatives are invented or produce an extra branch.",
                        "company_tags": ["infosys", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A developer runs `git init` inside `my-app/`, then again inside `my-app/backend/`. What is wrong with this?",
                        "choices": [
                            "Nothing — nested repositories are the recommended structure",
                            "It creates a nested repository; the inner repo's files become invisible to the outer repo's tracking",
                            "Git deletes the outer repository automatically",
                            "The inner init overwrites the outer repo's entire history",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "Nested repos are a classic mistake: the outer Git treats `backend/` as an untracked item containing its own `.git/`, so its files never show in outer commits. One project root = one repository (submodules exist for real multi-repo setups, but that's deliberate).",
                        "company_tags": ["amazon", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "After `git init`, you run `git status` and see \"No commits yet\". What does this mean?",
                        "choices": [
                            "Git failed to initialize the repository",
                            "The repository exists but has zero commits — its history is empty so far",
                            "All files are already committed",
                            "The working directory is corrupted",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "`git init` creates an empty repo — no commits yet, just a `.git/` directory waiting for history. `git status` is simply reporting that correctly.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which statement about the `.git/` directory is TRUE?",
                        "choices": [
                            "It should be committed and pushed so teammates get your branches",
                            "It is Git's private database (commits, branches, config) and should only be changed via Git commands",
                            "It contains a plain-text copy of your latest files",
                            "Deleting it only removes the current branch, not history",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "`.git/` stores the object database, refs, and config — everything Git knows. Committing it makes no sense (it holds machine-specific state), editing it by hand corrupts history, and deleting it destroys the ENTIRE repo history, leaving plain files behind.",
                        "company_tags": ["google", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which sequence correctly turns an existing folder into a repo with a first commit?",
                        "choices": [
                            "`git add .` → `git init` → `git commit -m \"init\"`",
                            "`git init -b main` → `git add .` → `git commit -m \"Initial commit\"`",
                            "`git commit -m \"Initial commit\"` → `git init`",
                            "`git init` → `git commit -m \"Initial commit\"` → `git add .`",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "Order matters: initialize the repo first, stage files with `git add` (there's nothing to commit before staging), then commit. Committing before `init` fails (not a repo), and committing before `add` commits nothing.",
                        "company_tags": ["microsoft", "accenture"],
                    },
                ],
            },
            {
                "slug": "git-fundamentals-the-staging-area",
                "title": "The Staging Area: Working Directory → Staging → Repository",
                "theory_md": """## The Staging Area: Working Directory → Staging → Repository

Git's most distinctive idea is the **staging area** (also called the
*index*). A file lives in one of three states, and understanding this
flow is what separates Git beginners from confident users.

```
Working Directory  →   Staging Area (index)  →   Repository (.git)
   (your files)         (proposed commit)         (permanent history)
        |  git add                |  git commit
        v                         v
```

### The three states, in practice

```bash
echo "hello" > notes.txt

# 1. WORKING DIRECTORY — file exists, Git is NOT tracking it yet
git status
# Untracked files:
#   notes.txt

# 2. STAGING AREA — git add proposes the file for the next commit
git add notes.txt
git status
# Changes to be committed:
#   new file:   notes.txt

# 3. REPOSITORY — git commit writes the snapshot into history
git commit -m "Add notes.txt"
git status
# nothing to commit, working tree clean
```

### Why does the staging area exist?

It lets you **craft precise commits** instead of snapshotting everything
at once. Edited 5 files but only 2 belong to this bug fix? Stage just
those:

```bash
git add login.py tests/test_login.py
git commit -m "Fix login redirect bug"
# other 3 files stay unstaged for a separate commit
```

You can even stage part of a file interactively:

```bash
git add -p login.py    # pick hunks one by one — surgical commits
```

### Untracked vs modified vs staged

| `git status` section | Meaning | Next step |
|---|---|---|
| Untracked files | Git has never seen these | `git add` to start tracking |
| Changes not staged | tracked file was edited | `git add` to stage the edit |
| Changes to be committed | staged, awaiting commit | `git commit` |

### Peeking at each layer

```bash
git diff            # working directory vs staging area
git diff --staged   # staging area vs last commit (what WILL be committed)
```

**Takeaway:** `git add` = "include this in the next commit". The staging
area is a loading dock: you decide exactly what goes into each commit
before sealing it into history.
""",
                "difficulty_min": 1,
                "difficulty_max": 6,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "What is the staging area (index) in Git?",
                        "choices": [
                            "A backup folder where Git copies your files every hour",
                            "An intermediate area holding a proposed snapshot of what will go into the next commit",
                            "The remote server where you push finished work",
                            "A temporary branch created automatically before each merge",
                        ],
                        "answer_index": 1,
                        "difficulty": 1,
                        "explanation": "The staging area is the middle step of the flow: `git add` puts changes there, and `git commit` snapshots exactly what's staged. It exists so you can craft precise commits rather than committing everything blindly.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You edit `app.py` (already tracked) and run `git status`. Under which heading will it appear?",
                        "choices": [
                            "Changes to be committed",
                            "Changes not staged for commit",
                            "Untracked files",
                            "It won't appear; tracked files are always clean",
                        ],
                        "answer_index": 1,
                        "difficulty": 2,
                        "explanation": "Editing a tracked file puts it in \"Changes not staged\" — Git noticed the modification but you haven't proposed it yet. `git add app.py` moves it to \"Changes to be committed\". New, never-added files show as \"Untracked\".",
                        "company_tags": ["wipro", "tcs"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You changed 5 files but only 2 belong to the bug fix you're committing now. What is the correct workflow?",
                        "choices": [
                            "`git commit -m \"fix\"` — Git figures out which files belong",
                            "`git add` only the 2 relevant files, then `git commit`; the rest stay unstaged for a later commit",
                            "Delete the other 3 files temporarily, commit, then recreate them",
                            "`git stash` everything and start the fix over",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "This is exactly why the staging area exists: `git add file1 file2` stages only those, so the commit contains precisely the bug fix. The other 3 files remain modified-but-unstaged, ready for their own commit.",
                        "company_tags": ["amazon", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What is the difference between `git diff` and `git diff --staged`?",
                        "choices": [
                            "`git diff` compares working directory vs staging area; `git diff --staged` compares staging area vs the last commit",
                            "They are identical; --staged is just an alias",
                            "`git diff --staged` compares against the remote server",
                            "`git diff` only works on untracked files",
                        ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "`git diff` (no args) shows unstaged changes — what you'd ADD next. `git diff --staged` shows what's staged — what the next COMMIT will contain. Checking both is how you verify a commit before sealing it.",
                        "company_tags": ["microsoft", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which command lets you stage changes hunk-by-hunk within a single file, for surgical commits?",
                        "choices": [
                            "`git add -p <file>`",
                            "`git add --whole <file>`",
                            "`git stage --partial <file>`",
                            "`git commit --hunks <file>`",
                        ],
                        "answer_index": 0,
                        "difficulty": 6,
                        "explanation": "`git add -p` (patch mode) walks you through each hunk of a file asking whether to stage it — the real command for crafting minimal, reviewable commits from a messy working tree. The other flags don't exist.",
                        "company_tags": ["google", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A new file `report.txt` was created but never added. What does `git commit -m \"save\"` do with it?",
                        "choices": [
                            "Commits it automatically since it's in the working directory",
                            "Ignores it — only staged changes are committed, and untracked files are never staged by a plain commit",
                            "Moves it to the staging area but doesn't commit",
                            "Deletes it as a safety measure",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "A plain `git commit` snapshots ONLY the staging area. Untracked files aren't staged, so they're silently left out — the #1 beginner surprise. (Note: `git commit -a` auto-stages MODIFIED tracked files, but still never new untracked ones.)",
                        "company_tags": ["infosys", "wipro"],
                    },
                ],
            },
            {
                "slug": "git-fundamentals-git-add-and-commit",
                "title": "Recording Changes: git add & git commit",
                "theory_md": """## Recording Changes: git add & git commit

You already met the staging area. This lesson is the daily bread and
butter: **`git add` proposes, `git commit` records.** You will run these
dozens of times a day.

### git add — propose changes

```bash
git add app.py                # stage one file
git add src/                  # stage a whole directory
git add .                     # stage everything changed under here
git add -A                    # stage everything, including deletions
```

Handy variants:

```bash
git add -p app.py             # interactively pick hunks to stage
git add -u                    # stage tracked-file changes only (skip new files)
```

### git commit — seal it into history

```bash
git commit -m "Fix crash when username is empty"
```

A commit is a **snapshot** of everything staged, plus metadata: author,
timestamp, message, and a unique SHA-1 hash like `a3f9c21`.

### Writing messages people will thank you for

Bad: `git commit -m "fix"`, `-m "update"`, `-m "asdf"`.
Good: imperative mood, what + why:

```bash
git commit -m "Fix login redirect for empty usernames

The session middleware assumed a non-empty username, which crashed
the redirect handler. Guard added in auth/session.py."
```

A good message answers: **what changed, and why** — the diff already
shows *how*.

### Shortcuts and fixes

```bash
git commit -am "Update pricing page"
# -a auto-stages MODIFIED tracked files (never new untracked ones!)

git commit --amend -m "Better message"
# rewrite the LAST commit (message or add forgotten staged files)

git commit --allow-empty -m "Trigger CI rebuild"
# a commit with zero changes — real, used to re-trigger pipelines
```

### The golden habits

1. **Commit early, commit often.** Small commits = easy reviews, easy reverts.
2. **One logical change per commit.** A commit should do one thing.
3. **Never commit secrets.** API keys, `.env` files, passwords — once in
   history, they're there forever (removal = rewriting history for
   everyone).

### Amend: fixing the last commit

```bash
git add forgotten.py
git commit --amend --no-edit   # folds it into the last commit
```

Safe only if you **haven't pushed** that commit yet (rewriting shared
history is the topic of a later lesson).

**Takeaway:** `git add` stages, `git commit` snapshots. Small,
well-described commits are a professional superpower — future you (and
your reviewers) will be grateful.
""",
                "difficulty_min": 1,
                "difficulty_max": 6,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "What does `git commit -m \"Fix bug\"` snapshot?",
                        "choices": [
                            "Every file in the working directory",
                            "Exactly what is currently in the staging area",
                            "Only the files changed in the last hour",
                            "All tracked files, staged or not",
                        ],
                        "answer_index": 1,
                        "difficulty": 1,
                        "explanation": "A commit snapshots the STAGING AREA — nothing more, nothing less. Files you changed but didn't `git add` are left out, which is why staging deliberately is a core Git skill.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does the `-a` flag do in `git commit -am \"msg\"`?",
                        "choices": [
                            "Adds ALL files including new untracked ones",
                            "Auto-stages modified TRACKED files before committing, but never stages new untracked files",
                            "Amends the previous commit automatically",
                            "Aborts the commit if tests fail",
                        ],
                        "answer_index": 1,
                        "difficulty": 2,
                        "explanation": "`-a` is shorthand for staging all modifications/deletions of files Git already tracks — convenient, but brand-new files still need an explicit `git add`. It's the most common interview trap about `commit -a`.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You just committed, then realized you forgot to include `fix.py` and the message has a typo. Nothing is pushed yet. What's the cleanest fix?",
                        "choices": [
                            "`git add fix.py` then `git commit --amend -m \"Correct message\"`",
                            "Delete the repo and start over",
                            "`git revert HEAD` and redo everything manually",
                            "Make a second commit titled \"fix previous commit\"",
                        ],
                        "answer_index": 0,
                        "difficulty": 4,
                        "explanation": "`git commit --amend` rewrites the last commit — adding newly staged files and/or fixing the message — keeping history to one clean commit. It's safe because nothing is pushed yet; never amend already-shared commits.",
                        "company_tags": ["amazon", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which commit message style follows professional convention?",
                        "choices": [
                            "`git commit -m \"asdf final\"`",
                            "`git commit -m \"Fix crash when username is empty\"`",
                            "`git commit -m \"updated stuff today, see diff\"`",
                            "`git commit -m \"changes\"`",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "Good messages use imperative mood and say WHAT and WHY — the diff already shows how. Vague messages like \"update\" or \"fix\" make `git log` useless for future debugging and code review.",
                        "company_tags": ["google", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What is `git commit --allow-empty -m \"Trigger CI\"` used for?",
                        "choices": [
                            "It is an error — Git refuses empty commits",
                            "Creating a commit with no file changes, commonly to re-trigger a CI pipeline",
                            "Committing only empty files",
                            "Deleting all staged changes safely",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "`--allow-empty` is a real flag that creates a commit object with no content changes. Teams use it to force CI/CD reruns or mark deployment events without touching code — Git normally blocks changeless commits.",
                        "company_tags": ["microsoft", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A developer accidentally committed a `.env` file containing an API key. What is the critical lesson?",
                        "choices": [
                            "Just delete the file in the next commit — the key becomes safe immediately",
                            "Secrets in a commit are in history forever; you must rotate/revoke the key and rewrite history (or filter it out) — prevention via .gitignore is the real fix",
                            "Git encrypts committed secrets automatically",
                            "`git add` skips `.env` files by default",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "Deleting the file later doesn't erase it from earlier commits — anyone with the history can still read it. The key must be revoked, and the file should have been in `.gitignore` from the start. This is the #1 real-world Git security lesson.",
                        "company_tags": ["amazon", "accenture"],
                    },
                ],
            },
            {
                "slug": "git-fundamentals-git-status-and-log",
                "title": "Reading State & History: git status & git log",
                "theory_md": """## Reading State & History: git status & git log

Two commands answer "what's going on?" — `git status` for the **present**,
`git log` for the **past**. Run them constantly; they are your dashboard.

### git status — the present

```bash
git status
```

Output sections to recognize:

- **Untracked files** — Git has never seen these; `git add` to track.
- **Changes not staged for commit** — tracked files you edited.
- **Changes to be committed** — staged; the next commit will include them.
- **nothing to commit, working tree clean** — all synced with HEAD.

Short form for scripts and quick glances:

```bash
git status --short     # or: git status -s
# M app.py       <- modified, staged
#  M utils.py    <- modified, unstaged (right column)
# ?? notes.txt   <- untracked
```

Two-column legend: left = staged, right = unstaged. `??` = untracked.

### git log — the past

```bash
git log                    # full history, newest first
git log --oneline          # compact: short hash + message, one line each
git log -n 5               # last 5 commits only
git log --graph --oneline --all   # ASCII branch graph — beautiful
git log -- app.py          # history of ONE file
git log --since="2 weeks ago"    # time-filtered history
git log --author="Mohit"   # filter by author
```

Example `--oneline` output:

```
a3f9c21 Fix crash when username is empty
7d2e4aa Add login page layout
f1b88c0 Initial commit
```

### Inspect a single commit

```bash
git show a3f9c21        # full diff + metadata of that commit
git show --stat HEAD    # which files the last commit touched
```

### Who wrote this line? (blame)

```bash
git blame app.py        # every line annotated with commit + author
git blame -L 10,20 app.py   # blame just lines 10-20
```

Useful, but use it for **understanding**, not for pointing fingers.

### Daily workflow rhythm

```bash
git status        # before doing anything — know your state
# ... work ...
git status        # what changed?
git diff          # review the changes
git add -p .      # stage deliberately
git diff --staged # verify the commit
git commit -m "..."
git log --oneline -3   # confirm it landed
```

**Takeaway:** `git status` tells you where you stand; `git log` tells
you how you got here. Check status before every action and read logs
like a story — they are one.
""",
                "difficulty_min": 1,
                "difficulty_max": 6,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "What is the difference in purpose between `git status` and `git log`?",
                        "choices": [
                            "`git status` shows the current working-tree/staging state; `git log` shows the commit history",
                            "They show the same information in different colors",
                            "`git log` shows uncommitted changes; `git status` shows old commits",
                            "`git status` requires internet; `git log` works offline",
                        ],
                        "answer_index": 0,
                        "difficulty": 1,
                        "explanation": "`git status` = the present (untracked/modified/staged files right now). `git log` = the past (the chain of commits). Both are purely local — neither needs the network.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "In `git status --short` output, what does ` M utils.py` (space then M) mean?",
                        "choices": [
                            "utils.py is staged for commit",
                            "utils.py is modified but NOT staged",
                            "utils.py is untracked",
                            "utils.py was merged",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "Short status has two columns: LEFT = staged, RIGHT = working tree. `M ` (M in left column) means staged; ` M` (M in right column) means modified but unstaged. `??` marks untracked files.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which command shows a compact one-line-per-commit history with an ASCII branch graph?",
                        "choices": [
                            "`git log --graph --oneline --all`",
                            "`git status --graph`",
                            "`git log --full --pretty`",
                            "`git branch --graph`",
                        ],
                        "answer_index": 0,
                        "difficulty": 2,
                        "explanation": "`--oneline` compresses each commit to hash + message, `--graph` draws the branch/merge structure in ASCII, and `--all` includes every branch. It's the standard \"see the whole repo at a glance\" command.",
                        "company_tags": ["tcs", "wipro"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "How do you see the commit history of just ONE file, `app.py`?",
                        "choices": [
                            "`git log -- app.py`",
                            "`git status app.py --history`",
                            "`git show --file app.py`",
                            "`git blame --log app.py`",
                        ],
                        "answer_index": 0,
                        "difficulty": 4,
                        "explanation": "`git log -- <path>` filters history to commits that touched that path — the `--` separates options from the path so filenames starting with `-` aren't misread. The other commands don't exist or do different things.",
                        "company_tags": ["amazon", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does `git blame app.py` tell you?",
                        "choices": [
                            "Which developer introduced bugs in the file",
                            "For each line, the commit hash, author, and date that last modified it",
                            "A list of everyone who ever cloned the repository",
                            "Which lines have merge conflicts",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "`git blame` annotates every line with the last commit that changed it — perfect for understanding WHY code looks the way it does (then `git show` that commit). It's an archaeology tool, not an accusation tool.",
                        "company_tags": ["google", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which command shows the full diff and metadata of a specific commit `a3f9c21`?",
                        "choices": [
                            "`git show a3f9c21`",
                            "`git log a3f9c21 --diff`",
                            "`git status a3f9c21`",
                            "`git diff a3f9c21`",
                        ],
                        "answer_index": 0,
                        "difficulty": 6,
                        "explanation": "`git show <commit>` displays that commit's message, author, date, and complete diff. (`git diff a3f9c21` compares that commit against the working tree — related but different.) It's the fastest way to inspect what one commit actually did.",
                        "company_tags": ["flipkart", "accenture"],
                    },
                ],
            },
            {
                "slug": "git-fundamentals-gitignore-patterns",
                "title": ".gitignore: Keeping Junk Out of History",
                "theory_md": """## .gitignore: Keeping Junk Out of History

Not everything belongs in version control: build artifacts, dependency
folders, logs, editor files, secrets. **`.gitignore`** lists patterns
Git should pretend don't exist.

### Create and use it

```bash
# .gitignore in the repo root
*.log
*.tmp
__pycache__/
node_modules/
.env
.DS_Store
```

Then:

```bash
git add .gitignore
git commit -m "Add .gitignore"
# the .gitignore file itself IS committed — teammates need it too
```

### Pattern language

| Pattern | Matches |
|---|---|
| `*.log` | any file ending in `.log`, any directory |
| `debug/*.log` | `.log` files only inside `debug/` |
| `build/` | the `build` directory and everything in it |
| `*.pyc` | all `.pyc` files |
| `!important.log` | exception: DO track this one (`!` negates) |
| `doc/**/*.txt` | `.txt` files at any depth under `doc/` |
| `/config.json` | only the root-level `config.json` |

Order matters: later lines can re-include with `!`.

### The classic beginner trap

`.gitignore` only affects **untracked** files. If you already committed
`debug.log` and THEN add `*.log` to `.gitignore`, Git keeps tracking it:

```bash
# Already-tracked file ignores .gitignore — stop tracking it:
git rm --cached debug.log
git commit -m "Stop tracking debug.log"
# --cached removes from the index but KEEPS your local file
```

### Quick checks

```bash
git check-ignore -v debug.log   # which rule ignores this file?
git status --ignored            # show ignored files too
```

### Force-adding an ignored file

Sometimes a rule is too broad and one file really should be tracked:

```bash
git add -f config/production.json   # -f overrides .gitignore for this add
```

Prefer fixing the pattern with `!` instead — `-f` is a one-off.

### What belongs in .gitignore (per language)

- Python: `__pycache__/`, `*.pyc`, `.venv/`, `*.egg-info/`
- Node: `node_modules/`, `dist/`, `.next/`
- Java: `target/`, `*.class`
- Everyone: `.env`, `*.log`, `.DS_Store`, `Thumbs.db`, IDE folders like `.idea/`, `.vscode/`

**Takeaway:** create `.gitignore` in your FIRST commit. It only stops
*untracked* files — for already-tracked ones use `git rm --cached`.
Your history should contain source, not build output or secrets.
""",
                "difficulty_min": 1,
                "difficulty_max": 6,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "What is the purpose of a `.gitignore` file?",
                        "choices": [
                            "To delete files from the repository permanently",
                            "To list patterns of files Git should not track (build output, logs, secrets, dependencies)",
                            "To encrypt sensitive files before committing",
                            "To ignore merge conflicts automatically",
                        ],
                        "answer_index": 1,
                        "difficulty": 1,
                        "explanation": "`.gitignore` tells Git which paths to skip — so `git add .` doesn't sweep up `node_modules/`, logs, or `.env`. It neither deletes nor encrypts anything; it's a filter on what gets tracked.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "In `.gitignore`, what does the pattern `!important.log` mean?",
                        "choices": [
                            "Delete important.log from the repository",
                            "Comment out the pattern for documentation",
                            "Negation: track important.log even though an earlier `*.log` rule ignores it",
                            "Mark important.log as a binary file",
                        ],
                        "answer_index": 2,
                        "difficulty": 3,
                        "explanation": "Leading `!` negates a pattern — it's how you carve exceptions (\"ignore all logs EXCEPT this one\"). Later lines take precedence, so the `!` rule must come after the rule it overrides.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "`debug.log` was committed last week. Today you add `*.log` to `.gitignore`, but `git status` still shows `debug.log` as tracked. Why, and how do you fix it?",
                        "choices": [
                            ".gitignore is broken; you must delete and recreate the repo",
                            ".gitignore only applies to untracked files; run `git rm --cached debug.log` to stop tracking it while keeping the local file",
                            "You need `git add .gitignore --force` for it to take effect",
                            "Git ignores .gitignore until the next clone",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "Once tracked, always tracked — `.gitignore` can't untrack. `git rm --cached` removes the file from the INDEX (so future commits skip it) but leaves your working-tree copy intact. A plain `git rm` would delete your local file too.",
                        "company_tags": ["amazon", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which `.gitignore` pattern ignores the `build/` directory everywhere in the repo, but only the root-level `/config.json`?",
                        "choices": [
                            "`build/` and `/config.json`",
                            "`build/*` and `config.json`",
                            "`**/build` and `config.json/`",
                            "`build` and `*/config.json`",
                        ],
                        "answer_index": 0,
                        "difficulty": 4,
                        "explanation": "Trailing `/` marks a directory (`build/` matches at any depth); leading `/` anchors to the repo root (`/config.json`). Bare `config.json` would match at ANY depth — the anchor is the whole point.",
                        "company_tags": ["microsoft", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "How do you find out WHICH rule in `.gitignore` is ignoring `debug.log`?",
                        "choices": [
                            "`git check-ignore -v debug.log`",
                            "`git ignore --why debug.log`",
                            "`git status --explain debug.log`",
                            "`git log --ignored debug.log`",
                        ],
                        "answer_index": 0,
                        "difficulty": 6,
                        "explanation": "`git check-ignore -v <path>` prints the exact file, line number, and pattern that ignores a path — the real debugging tool when a file mysteriously won't stage. The others aren't real commands.",
                        "company_tags": ["google", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Should the `.gitignore` file itself be committed to the repository?",
                        "choices": [
                            "No — it's personal config and must stay local",
                            "Yes — teammates need the same ignore rules so everyone's history stays clean",
                            "Only on public repositories",
                            "Only if it contains more than 10 lines",
                        ],
                        "answer_index": 1,
                        "difficulty": 2,
                        "explanation": "`.gitignore` is shared project policy — committing it means every clone ignores the same junk. Personal-only ignores (your editor's temp files) belong in the global `~/.gitignore` via `core.excludesFile`, not the repo's file.",
                        "company_tags": ["infosys", "tcs"],
                    },
                ],
            },
            {
                "slug": "git-fundamentals-undoing-changes",
                "title": "Undoing Mistakes: restore, reset, revert",
                "theory_md": """## Undoing Mistakes: restore, reset, revert

Everyone breaks things. Git's undo toolkit has three tools — pick by
**where the mistake lives** and **whether it's shared**.

### Decision map

| Mistake location | Command | Shared history safe? |
|---|---|---|
| Working directory (unstaged edit) | `git restore <file>` | Yes |
| Staging area (staged, not committed) | `git restore --staged <file>` | Yes |
| Last commit(s), NOT pushed | `git reset` | Yes (only yours) |
| Commit(s), already PUSHED | `git revert` | **Yes — the only safe one** |

### 1. Discard unstaged working-tree edits

```bash
git restore app.py        # app.py back to its last committed state
# old equivalent: git checkout -- app.py
```

Irreversible — Git can't recover edits it never saw. Double-check with
`git diff` first.

### 2. Unstage (keep the edits)

```bash
git restore --staged app.py   # moves app.py staging -> working dir
# old equivalent: git reset HEAD app.py
```

Your edits stay in the file; they're just no longer proposed for commit.

### 3. git reset — move the branch pointer (local history)

Reset moves HEAD/branch to an older commit. Three flavors — what happens
to your files differs:

```bash
git reset --soft HEAD~1    # keep changes STAGED (redo the commit message)
git reset --mixed HEAD~1   # keep changes UNSTAGED (default; redo add+commit)
git reset --hard HEAD~1    # DISCARD all changes (dangerous!)
```

`HEAD~1` = "one commit before HEAD". `--hard` permanently deletes
uncommitted work — the nuclear option.

### 4. git revert — safe undo for pushed commits

```bash
git revert a3f9c21
# creates a NEW commit that undoes a3f9c21's changes
```

History stays intact (everyone else's work is untouched) — this is why
`revert` is the professional choice for shared branches.

### Realistic scenarios

```bash
# "I staged the wrong file"
git restore --staged wrong.py

# "My last two local commits are a mess, start the commit over"
git reset --soft HEAD~2     # files stay staged, commits gone

# "I want the file exactly as it was 3 commits ago"
git restore --source=HEAD~3 app.py

# "That pushed commit broke production"
git revert <bad-commit-hash>   # then push the revert commit
```

### The golden rule of undoing

> **Never `reset --hard` or `amend` commits you've already pushed.**
> Rewriting shared history breaks every teammate's clone. `revert` adds
> history instead of rewriting it.

**Takeaway:** uncommitted mess → `restore`; local commits → `reset`;
pushed commits → `revert`. Match the tool to the blast radius.
""",
                "difficulty_min": 2,
                "difficulty_max": 7,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "You edited `app.py` but haven't staged anything, and want to throw away those edits. Which command?",
                        "choices": [
                            "`git restore app.py`",
                            "`git revert app.py`",
                            "`git reset app.py`",
                            "`git clean app.py`",
                        ],
                        "answer_index": 0,
                        "difficulty": 2,
                        "explanation": "`git restore <file>` discards unstaged working-tree changes, returning the file to its last committed state. `revert` undoes commits, and `reset` moves the branch pointer — different tools for different layers.",
                        "company_tags": ["tcs", "wipro"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What's the difference between `git reset --soft HEAD~1` and `git reset --hard HEAD~1`?",
                        "choices": [
                            "No difference; both delete the last commit permanently",
                            "`--soft` keeps the changes staged (you can re-commit); `--hard` discards all changes in working tree and staging permanently",
                            "`--soft` works on pushed commits; `--hard` only works locally",
                            "`--soft` deletes the file; `--hard` keeps it",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "`--soft` moves the branch pointer back but leaves index and working tree alone (changes stay staged). `--hard` also wipes the index and working tree — unrecoverable. `--mixed` (the default) sits between: unstaged but kept.",
                        "company_tags": ["infosys", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A bad commit was already pushed to the team's shared branch and broke the build. What's the SAFE fix?",
                        "choices": [
                            "`git reset --hard HEAD~1` then `git push --force`",
                            "`git revert <bad-commit>` to create a new commit that undoes it, then push normally",
                            "Delete the remote branch and recreate it",
                            "`git commit --amend` to rewrite the pushed commit",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "`git revert` ADDS history (a new undo commit) instead of rewriting it, so teammates' clones stay valid — the only safe option on shared branches. Force-pushing a reset rewrites public history and breaks everyone's checkout.",
                        "company_tags": ["amazon", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You staged `secrets.py` by accident but haven't committed. How do you unstage it while KEEPING your edits?",
                        "choices": [
                            "`git restore --staged secrets.py`",
                            "`git restore secrets.py`",
                            "`git revert HEAD`",
                            "`git rm secrets.py`",
                        ],
                        "answer_index": 0,
                        "difficulty": 3,
                        "explanation": "`git restore --staged` moves the file from staging back to the working directory — edits intact, just no longer proposed. Plain `git restore` would also discard the edits (too destructive here), and `git rm` deletes the file.",
                        "company_tags": ["microsoft", "tcs"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does `git restore --source=HEAD~3 app.py` do?",
                        "choices": [
                            "Deletes app.py from the last 3 commits",
                            "Restores app.py's working-tree copy to its content as of 3 commits ago, without touching history",
                            "Reverts the last 3 commits that touched app.py",
                            "Shows a diff of app.py across the last 3 commits",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "`--source` picks which commit to restore FROM — a real, surgical flag. It only rewrites the working-tree file (unstaged change you can review); history is untouched. Perfect for \"give me the old version of this one file.\"",
                        "company_tags": ["google", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why is `git reset --hard` on an already-pushed branch considered dangerous in a team?",
                        "choices": [
                            "It permanently deletes the remote repository",
                            "It rewrites shared history, so teammates' clones diverge and their next pull/merge breaks",
                            "It locks the branch for 24 hours",
                            "It emails the admin about your mistake",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "Reset moves YOUR branch pointer; teammates still have the old history. When they pull, Git sees divergent histories and forces painful reconciliations — or they unknowingly re-push the \"removed\" commits. Shared history is append-only: use `revert`.",
                        "company_tags": ["accenture", "amazon"],
                    },
                ],
            },
        ],
    },
    {
        "slug": "git-branching",
        "name": "Git Branching",
        "description": (
            "Work in parallel without breaking main: what branches are, "
            "creating and switching, the feature-branch model, merging, "
            "resolving conflicts, rebase vs merge, stashing, and detached HEAD."
        ),
        "lessons": [
            {
                "slug": "git-branching-what-is-a-branch",
                "title": "What is a Branch? (A Pointer to a Commit)",
                "theory_md": """## What is a Branch? (A Pointer to a Commit)

A **branch** in Git is nothing more than a **lightweight movable pointer
to a commit**. That's the whole secret — and it's why Git branching is
instant while other VCSs treat branches as expensive copies.

### Commits form a chain

Each commit stores a pointer to its parent (except the first):

```
A <-- B <-- C
```

A branch is just a label stuck on one of these commits:

```
A <-- B <-- C   <-- main
```

When you commit on `main`, Git creates commit D and **moves the `main`
pointer forward**:

```
A <-- B <-- C <-- D   <-- main
```

### HEAD — "where am I?"

`HEAD` is a special pointer that says which branch you're currently on:

```bash
git branch            # list branches; * marks the current one
# * main

cat .git/HEAD         # usually: ref: refs/heads/main
```

Committing moves the branch that HEAD points to. That's it. No magic.

### Why this design is fast

Creating a branch = writing a 41-byte file with a commit hash. No file
copying, no server round-trip:

```bash
git branch              # instant, even in a 100k-commit repo
```

Contrast with old VCSs where a branch duplicated the whole tree.

### Branches are local until shared

```bash
git branch feature-x    # creates a LOCAL branch only
git push -u origin feature-x   # -u publishes it and sets upstream
```

Your branches don't exist for teammates until you push them.

### See the pointers

```bash
git log --oneline --decorate --graph --all
# * a3f9c21 (HEAD -> main, origin/main) Fix crash
# | * 7d2e4aa (feature-x) Add dark mode
# |/
# * f1b88c0 Initial commit
```

`--decorate` shows which branches/tags point at each commit — the
pointer model made visible.

**Takeaway:** branch = sticky note on a commit. Committing moves the
sticky note you're standing on (HEAD). Internalizing this makes merging,
rebasing, and detached HEAD all click.
""",
                "difficulty_min": 1,
                "difficulty_max": 6,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "What IS a Git branch, technically?",
                        "choices": [
                            "A full copy of all project files",
                            "A lightweight movable pointer (reference) to a commit",
                            "A separate repository stored on the server",
                            "A backup of the working directory",
                        ],
                        "answer_index": 1,
                        "difficulty": 1,
                        "explanation": "A branch is literally a tiny file containing a commit hash — a pointer. That's why creating branches is instant and cheap in Git, unlike older VCSs that copied whole trees.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "When you make a new commit while on branch `main`, what happens to the `main` pointer?",
                        "choices": [
                            "It stays where it was; you must move it manually",
                            "Git creates the new commit and automatically moves `main` forward to point at it",
                            "It moves back one commit",
                            "A new branch is created automatically",
                        ],
                        "answer_index": 1,
                        "difficulty": 2,
                        "explanation": "Committing advances the current branch pointer (the one HEAD points to) to the new commit. The pointer-follows-commit rule is the entire mechanism behind branching.",
                        "company_tags": ["wipro", "tcs"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does HEAD represent in Git?",
                        "choices": [
                            "The first commit ever made in the repository",
                            "A pointer to the currently checked-out branch (or commit) — i.e., \"where you are\"",
                            "The remote server's main branch",
                            "The largest file in the repository",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "HEAD points at your current branch (normally) — new commits advance whichever branch HEAD references. That's why `git log` shows `(HEAD -> main)`: you're on main.",
                        "company_tags": ["accenture", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why is creating a branch in Git nearly instantaneous even in huge repositories?",
                        "choices": [
                            "Git compresses all files before branching",
                            "A branch is just a 41-byte file holding a commit hash — no files are copied",
                            "Branches are created on a remote server with more power",
                            "Git skips creating a branch until the first commit",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "Because a branch = one tiny ref file with a SHA, creation is O(1) regardless of repo size. This cheapness is exactly what makes feature-branch workflows practical.",
                        "company_tags": ["google", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does `git log --oneline --decorate` add compared to plain `git log --oneline`?",
                        "choices": [
                            "It shows ref names (branches, tags, HEAD) next to the commits they point to",
                            "It downloads missing commits from the remote",
                            "It colors the output based on author",
                            "It shows file sizes for each commit",
                        ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "`--decorate` annotates each commit line with the pointers referencing it, e.g. `(HEAD -> main, origin/main)` — making the branch-as-pointer model visible. It's the fastest way to see where every branch sits.",
                        "company_tags": ["microsoft", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You run `git branch feature-x` but never push it. Which statement is TRUE?",
                        "choices": [
                            "Teammates can see and checkout feature-x immediately",
                            "feature-x exists only in your local repository until you push it",
                            "Git auto-pushes new branches within an hour",
                            "The branch is deleted when you switch away",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "Branches are local refs until published with `git push -u origin feature-x`. This locality is a feature — experiment freely without polluting the shared repo.",
                        "company_tags": ["accenture", "wipro"],
                    },
                ],
            },
            {
                "slug": "git-branching-creating-and-switching",
                "title": "Creating & Switching Branches",
                "theory_md": """## Creating & Switching Branches

Two operations, done constantly: **make** a branch, **move** to it. Git
offers classic and modern spellings — know both, because you'll read
both in the wild.

### Create a branch

```bash
git branch feature-login        # create, but STAY on current branch
git branch                      # list local branches
git branch -a                   # list local AND remote-tracking branches
git branch -v                   # list with last commit on each
```

### Switch branches

```bash
git switch feature-login        # modern, clear (Git 2.23+)
git checkout feature-login      # classic — still everywhere
```

### Create AND switch in one step (the daily driver)

```bash
git switch -c feature-login     # modern
git checkout -b feature-login   # classic equivalent
```

You will type one of these two commands more than almost any other.

### Branch from a specific starting point

```bash
git switch -c hotfix main       # branch hotfix starting at main's tip
git switch -c experiment a3f9c21  # start from a specific commit
```

Default start point is HEAD (wherever you are now) — so check
`git status`/`git branch` BEFORE branching, or you'll branch from the
wrong place.

### Rename and delete

```bash
git branch -m old-name new-name   # rename current branch
git branch -m new-name             # (one-arg form renames current)
git branch -d feature-login       # delete — only if fully merged (safe)
git branch -D feature-login       # force delete, merged or not (careful!)
```

`-d` refuses if the branch has unmerged work — a safety net. `-D`
skips the check.

### The uncommitted-changes dance

Switching branches with uncommitted changes: Git carries them along IF
they don't conflict with the target branch; otherwise it refuses and
tells you to commit or stash first.

```bash
git switch main
# error: Your local changes would be overwritten... Commit or stash them.
git stash        # park changes safely (next lessons cover this)
git switch main
```

### Typical feature workflow

```bash
git switch main
git pull                    # make sure you're starting fresh
git switch -c feature-login
# ... work, commit, work, commit ...
git push -u origin feature-login
```

**Takeaway:** `git switch -c <name>` (or `checkout -b`) is your daily
driver. Always confirm your starting point before branching, and use
`-d` (safe delete) unless you mean `-D`.
""",
                "difficulty_min": 1,
                "difficulty_max": 6,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Which command creates a new branch `feature-x` AND switches to it in one step?",
                        "choices": [
                            "`git branch feature-x`",
                            "`git switch -c feature-x`",
                            "`git switch feature-x`",
                            "`git checkout -- feature-x`",
                        ],
                        "answer_index": 1,
                        "difficulty": 1,
                        "explanation": "`git switch -c` (create) both creates and checks out the branch — the modern daily driver. (`git checkout -b feature-x` is the classic equivalent.) Plain `git branch` creates without switching.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What is the difference between `git branch feature-x` and `git switch -c feature-x`?",
                        "choices": [
                            "No difference at all",
                            "`git branch` only creates the branch (you stay where you are); `git switch -c` creates it AND moves you onto it",
                            "`git branch` creates a remote branch; `git switch -c` creates a local one",
                            "`git switch -c` deletes the old branch",
                        ],
                        "answer_index": 1,
                        "difficulty": 2,
                        "explanation": "Creation vs creation+checkout: `git branch <name>` leaves HEAD untouched, so your next commit still lands on the old branch — a classic beginner trap. `-c` moves you onto the new branch immediately.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You want a `hotfix` branch starting from the tip of `main`, but you're currently on `feature-x`. Which command is correct?",
                        "choices": [
                            "`git switch -c hotfix main`",
                            "`git switch -c hotfix`",
                            "`git branch hotfix` then merge main",
                            "`git checkout main -- hotfix`",
                        ],
                        "answer_index": 0,
                        "difficulty": 4,
                        "explanation": "`git switch -c <new> <start-point>` branches from an explicit start point — here `main`'s tip. Without the start-point argument, the branch would fork from your current spot on `feature-x`, which is wrong for a hotfix.",
                        "company_tags": ["amazon", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What's the difference between `git branch -d old` and `git branch -D old`?",
                        "choices": [
                            "`-d` deletes only if the branch is fully merged (safe); `-D` force-deletes even with unmerged work",
                            "`-d` deletes remote branches; `-D` deletes local ones",
                            "They are identical; -D is just the long form",
                            "`-d` archives the branch; `-D` deletes it",
                        ],
                        "answer_index": 0,
                        "difficulty": 3,
                        "explanation": "Lowercase `-d` is the safety net — it refuses to delete a branch containing commits not merged elsewhere. Uppercase `-D` overrides that check. Reach for `-d` by habit.",
                        "company_tags": ["google", "tcs"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Git refuses `git switch main` saying your local changes would be overwritten. What's the proper handling?",
                        "choices": [
                            "Run `git switch --force main` to discard the warning",
                            "Commit the changes or `git stash` them, then switch",
                            "Delete the changed files and switch",
                            "Run `git pull` first — that always fixes it",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "Git blocks the switch to protect your uncommitted work from being clobbered. The correct responses are committing (work is done) or stashing (work is in progress) — then switching cleanly.",
                        "company_tags": ["flipkart", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which command lists BOTH local branches and remote-tracking branches?",
                        "choices": [
                            "`git branch -a`",
                            "`git branch`",
                            "`git branch -l`",
                            "`git remote --branches`",
                        ],
                        "answer_index": 0,
                        "difficulty": 6,
                        "explanation": "`git branch -a` (all) shows local branches plus `remotes/origin/...` tracking refs — essential for seeing what exists on the server. Plain `git branch` shows locals only.",
                        "company_tags": ["accenture", "wipro"],
                    },
                ],
            },
