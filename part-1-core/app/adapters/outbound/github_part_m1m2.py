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
                            "To record changes to files over time so any version can be recalled later",
                            "To deploy applications to production servers automatically",
                            "To encrypt source code so only team members can read it",
                            "To compile source code into executable programs",
                        ],
                        "answer_index": 0,
                        "difficulty": 1,
                        "explanation": "A VCS records who changed what, when, and why, letting you recall or restore any earlier version. Compilation, deployment, and encryption are separate tools' jobs, not the VCS's purpose.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which statement BEST describes the difference between Git and SVN (Subversion)?",
                        "choices": [
                            "Git requires a paid license while SVN is always free",
                            "Git is distributed (every clone has the full history), while SVN is centralized (history lives on one server)",
                            "Git can only track Python files while SVN tracks any file type",
                            "SVN is faster than Git because it keeps all data on a central server",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "Git is distributed: `git clone` copies the entire history, so local operations like `git log` work offline. SVN is centralized: most operations need to reach the server. The other options mix up facts — both track any file type and both are free.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You are on a flight with no internet. Which of these git commands can you still run successfully in a cloned repository?",
                        "choices": [
                            "git fetch --all",
                            "git clone https://github.com/user/repo.git",
                            "git log --oneline and git status",
                            "git push origin main",
                        ],
                        "answer_index": 2,
                        "difficulty": 2,
                        "explanation": "`git log` and `git status` only read your LOCAL clone, which contains the full history — the whole point of a distributed VCS. Push, fetch, and clone all need network access to a remote server.",
                        "company_tags": ["tcs", "wipro"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A teammate says: \"I committed my changes but my coworker can't see them.\" What is the most likely explanation?",
                        "choices": [
                            "Git automatically pushes every commit within 5 minutes",
                            "The coworker needs to delete their local repository first",
                            "They need to run `git config` again before committing",
                            "A local commit stays on their machine until they `git push` it to the shared remote",
                        ],
                        "answer_index": 3,
                        "difficulty": 4,
                        "explanation": "In Git, `commit` writes to the LOCAL repository only; `push` publishes commits to the remote. This is the direct consequence of the distributed model — local history and shared history are separate until you sync them.",
                        "company_tags": ["infosys", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which of the following is NOT something Git does?",
                        "choices": [
                            "Tracks an empty directory that contains no files",
                            "Merges work from multiple contributors",
                            "Records who changed which lines and when",
                            "Lets you restore a file to an earlier version",
                        ],
                        "answer_index": 0,
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
                            "`git user --add \"Name\" \"a@b.com\"`",
                            "`git config --global user.name \"Name\"` and `git config --global user.email \"a@b.com\"`",
                            "`git set identity --name \"Name\" --email \"a@b.com\"`",
                            "`git init --author \"Name <a@b.com>\"`",
                        ],
                        "answer_index": 1,
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
                        "explanation": "`--global` writes to `~/.gitconfig`, the current user's machine-wide config, so every repository you touch inherits it. It's not per-system, not synced to GitHub, and never expires — it's simply your identity everywhere on this machine.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You want your work laptop to use `mohit@company.com` for the current project only, but keep your personal email everywhere else. Which command does this?",
                        "choices": [
                            "`git config --system user.email \"mohit@company.com\"`",
                            "`git email --set-local \"mohit@company.com\"`",
                            "`git config --global user.email \"mohit@company.com\"`",
                            "`git config user.email \"mohit@company.com\"` (run inside the project)",
                        ],
                        "answer_index": 3,
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
                            "`git branch --rename master main` run in every repo",
                            "`git init --branch main --global`",
                            "`git config --global init.defaultBranch main`",
                            "`git config --global branch.default main`",
                        ],
                        "answer_index": 2,
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
                            "Creates a new branch called main",
                            "Downloads the latest code from GitHub",
                            "Creates a hidden `.git/` directory that will hold the repo's history and metadata",
                            "Commits all files in the folder automatically",
                        ],
                        "answer_index": 2,
                        "difficulty": 1,
                        "explanation": "`git init` creates the `.git/` directory — Git's private database for commits, branches, and history — in the current folder. It doesn't download anything, commit anything, or create branches by itself.",
                        "company_tags": ["tcs", "wipro"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "How do you initialize a new repository whose first branch is named `main` in one command?",
                        "choices": [
                            "`git init --first-branch main`",
                            "`git create --branch main`",
                            "`git init` followed by `git branch main`",
                            "`git init -b main`",
                        ],
                        "answer_index": 3,
                        "difficulty": 2,
                        "explanation": "`git init -b main` (Git 2.28+) initializes the repo and names the unborn first branch `main` in one step — a real flag. The alternatives are invented or produce an extra branch.",
                        "company_tags": ["infosys", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A developer runs `git init` inside `my-app/`, then again inside `my-app/backend/`. What is wrong with this?",
                        "choices": [
                            "It creates a nested repository; the inner repo's files become invisible to the outer repo's tracking",
                            "Git deletes the outer repository automatically",
                            "The inner init overwrites the outer repo's entire history",
                            "Nothing — nested repositories are the recommended structure",
                        ],
                        "answer_index": 0,
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
                            "Deleting it only removes the current branch, not history",
                            "It should be committed and pushed so teammates get your branches",
                            "It is Git's private database (commits, branches, config) and should only be changed via Git commands",
                            "It contains a plain-text copy of your latest files",
                        ],
                        "answer_index": 2,
                        "difficulty": 3,
                        "explanation": "`.git/` stores the object database, refs, and config — everything Git knows. Committing it makes no sense (it holds machine-specific state), editing it by hand corrupts history, and deleting it destroys the ENTIRE repo history, leaving plain files behind.",
                        "company_tags": ["google", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which sequence correctly turns an existing folder into a repo with a first commit?",
                        "choices": [
                            "`git commit -m \"Initial commit\"` → `git init`",
                            "`git init` → `git commit -m \"Initial commit\"` → `git add .`",
                            "`git add .` → `git init` → `git commit -m \"init\"`",
                            "`git init -b main` → `git add .` → `git commit -m \"Initial commit\"`",
                        ],
                        "answer_index": 3,
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
                            "The remote server where you push finished work",
                            "A temporary branch created automatically before each merge",
                            "A backup folder where Git copies your files every hour",
                            "An intermediate area holding a proposed snapshot of what will go into the next commit",
                        ],
                        "answer_index": 3,
                        "difficulty": 1,
                        "explanation": "The staging area is the middle step of the flow: `git add` puts changes there, and `git commit` snapshots exactly what's staged. It exists so you can craft precise commits rather than committing everything blindly.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You edit `app.py` (already tracked) and run `git status`. Under which heading will it appear?",
                        "choices": [
                            "Changes not staged for commit",
                            "Untracked files",
                            "It won't appear; tracked files are always clean",
                            "Changes to be committed",
                        ],
                        "answer_index": 0,
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
                            "`git diff --staged` compares against the remote server",
                            "`git diff` only works on untracked files",
                            "`git diff` compares working directory vs staging area; `git diff --staged` compares staging area vs the last commit",
                            "They are identical; --staged is just an alias",
                        ],
                        "answer_index": 2,
                        "difficulty": 5,
                        "explanation": "`git diff` (no args) shows unstaged changes — what you'd ADD next. `git diff --staged` shows what's staged — what the next COMMIT will contain. Checking both is how you verify a commit before sealing it.",
                        "company_tags": ["microsoft", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which command lets you stage changes hunk-by-hunk within a single file, for surgical commits?",
                        "choices": [
                            "`git add --whole <file>`",
                            "`git stage --partial <file>`",
                            "`git commit --hunks <file>`",
                            "`git add -p <file>`",
                        ],
                        "answer_index": 3,
                        "difficulty": 6,
                        "explanation": "`git add -p` (patch mode) walks you through each hunk of a file asking whether to stage it — the real command for crafting minimal, reviewable commits from a messy working tree. The other flags don't exist.",
                        "company_tags": ["google", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A new file `report.txt` was created but never added. What does `git commit -m \"save\"` do with it?",
                        "choices": [
                            "Ignores it — only staged changes are committed, and untracked files are never staged by a plain commit",
                            "Moves it to the staging area but doesn't commit",
                            "Deletes it as a safety measure",
                            "Commits it automatically since it's in the working directory",
                        ],
                        "answer_index": 0,
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
                            "Exactly what is currently in the staging area",
                            "Only the files changed in the last hour",
                            "All tracked files, staged or not",
                            "Every file in the working directory",
                        ],
                        "answer_index": 0,
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
                            "`git revert HEAD` and redo everything manually",
                            "Make a second commit titled \"fix previous commit\"",
                            "`git add fix.py` then `git commit --amend -m \"Correct message\"`",
                            "Delete the repo and start over",
                        ],
                        "answer_index": 2,
                        "difficulty": 4,
                        "explanation": "`git commit --amend` rewrites the last commit — adding newly staged files and/or fixing the message — keeping history to one clean commit. It's safe because nothing is pushed yet; never amend already-shared commits.",
                        "company_tags": ["amazon", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which commit message style follows professional convention?",
                        "choices": [
                            "`git commit -m \"updated stuff today, see diff\"`",
                            "`git commit -m \"changes\"`",
                            "`git commit -m \"asdf final\"`",
                            "`git commit -m \"Fix crash when username is empty\"`",
                        ],
                        "answer_index": 3,
                        "difficulty": 3,
                        "explanation": "Good messages use imperative mood and say WHAT and WHY — the diff already shows how. Vague messages like \"update\" or \"fix\" make `git log` useless for future debugging and code review.",
                        "company_tags": ["google", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What is `git commit --allow-empty -m \"Trigger CI\"` used for?",
                        "choices": [
                            "Creating a commit with no file changes, commonly to re-trigger a CI pipeline",
                            "Committing only empty files",
                            "Deleting all staged changes safely",
                            "It is an error — Git refuses empty commits",
                        ],
                        "answer_index": 0,
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
                            "`git status` requires internet; `git log` works offline",
                            "`git status` shows the current working-tree/staging state; `git log` shows the commit history",
                            "They show the same information in different colors",
                            "`git log` shows uncommitted changes; `git status` shows old commits",
                        ],
                        "answer_index": 1,
                        "difficulty": 1,
                        "explanation": "`git status` = the present (untracked/modified/staged files right now). `git log` = the past (the chain of commits). Both are purely local — neither needs the network.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "In `git status --short` output, what does ` M utils.py` (space then M) mean?",
                        "choices": [
                            "utils.py was merged",
                            "utils.py is staged for commit",
                            "utils.py is modified but NOT staged",
                            "utils.py is untracked",
                        ],
                        "answer_index": 2,
                        "difficulty": 3,
                        "explanation": "Short status has two columns: LEFT = staged, RIGHT = working tree. `M ` (M in left column) means staged; ` M` (M in right column) means modified but unstaged. `??` marks untracked files.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which command shows a compact one-line-per-commit history with an ASCII branch graph?",
                        "choices": [
                            "`git status --graph`",
                            "`git log --full --pretty`",
                            "`git branch --graph`",
                            "`git log --graph --oneline --all`",
                        ],
                        "answer_index": 3,
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
                            "`git status a3f9c21`",
                            "`git diff a3f9c21`",
                            "`git show a3f9c21`",
                            "`git log a3f9c21 --diff`",
                        ],
                        "answer_index": 2,
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
                            "To ignore merge conflicts automatically",
                            "To delete files from the repository permanently",
                            "To list patterns of files Git should not track (build output, logs, secrets, dependencies)",
                            "To encrypt sensitive files before committing",
                        ],
                        "answer_index": 2,
                        "difficulty": 1,
                        "explanation": "`.gitignore` tells Git which paths to skip — so `git add .` doesn't sweep up `node_modules/`, logs, or `.env`. It neither deletes nor encrypts anything; it's a filter on what gets tracked.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "In `.gitignore`, what does the pattern `!important.log` mean?",
                        "choices": [
                            "Mark important.log as a binary file",
                            "Delete important.log from the repository",
                            "Comment out the pattern for documentation",
                            "Negation: track important.log even though an earlier `*.log` rule ignores it",
                        ],
                        "answer_index": 3,
                        "difficulty": 3,
                        "explanation": "Leading `!` negates a pattern — it's how you carve exceptions (\"ignore all logs EXCEPT this one\"). Later lines take precedence, so the `!` rule must come after the rule it overrides.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "`debug.log` was committed last week. Today you add `*.log` to `.gitignore`, but `git status` still shows `debug.log` as tracked. Why, and how do you fix it?",
                        "choices": [
                            ".gitignore only applies to untracked files; run `git rm --cached debug.log` to stop tracking it while keeping the local file",
                            "You need `git add .gitignore --force` for it to take effect",
                            "Git ignores .gitignore until the next clone",
                            ".gitignore is broken; you must delete and recreate the repo",
                        ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "Once tracked, always tracked — `.gitignore` can't untrack. `git rm --cached` removes the file from the INDEX (so future commits skip it) but leaves your working-tree copy intact. A plain `git rm` would delete your local file too.",
                        "company_tags": ["amazon", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which `.gitignore` pattern ignores the `build/` directory everywhere in the repo, but only the root-level `/config.json`?",
                        "choices": [
                            "`build` and `*/config.json`",
                            "`build/` and `/config.json`",
                            "`build/*` and `config.json`",
                            "`**/build` and `config.json/`",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "Trailing `/` marks a directory (`build/` matches at any depth); leading `/` anchors to the repo root (`/config.json`). Bare `config.json` would match at ANY depth — the anchor is the whole point.",
                        "company_tags": ["microsoft", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "How do you find out WHICH rule in `.gitignore` is ignoring `debug.log`?",
                        "choices": [
                            "`git status --explain debug.log`",
                            "`git log --ignored debug.log`",
                            "`git check-ignore -v debug.log`",
                            "`git ignore --why debug.log`",
                        ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "`git check-ignore -v <path>` prints the exact file, line number, and pattern that ignores a path — the real debugging tool when a file mysteriously won't stage. The others aren't real commands.",
                        "company_tags": ["google", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Should the `.gitignore` file itself be committed to the repository?",
                        "choices": [
                            "Only on public repositories",
                            "Only if it contains more than 10 lines",
                            "No — it's personal config and must stay local",
                            "Yes — teammates need the same ignore rules so everyone's history stays clean",
                        ],
                        "answer_index": 3,
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
                            "`git revert app.py`",
                            "`git reset app.py`",
                            "`git clean app.py`",
                            "`git restore app.py`",
                        ],
                        "answer_index": 3,
                        "difficulty": 2,
                        "explanation": "`git restore <file>` discards unstaged working-tree changes, returning the file to its last committed state. `revert` undoes commits, and `reset` moves the branch pointer — different tools for different layers.",
                        "company_tags": ["tcs", "wipro"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What's the difference between `git reset --soft HEAD~1` and `git reset --hard HEAD~1`?",
                        "choices": [
                            "`--soft` keeps the changes staged (you can re-commit); `--hard` discards all changes in working tree and staging permanently",
                            "`--soft` works on pushed commits; `--hard` only works locally",
                            "`--soft` deletes the file; `--hard` keeps it",
                            "No difference; both delete the last commit permanently",
                        ],
                        "answer_index": 0,
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
                            "`git revert HEAD`",
                            "`git rm secrets.py`",
                            "`git restore --staged secrets.py`",
                            "`git restore secrets.py`",
                        ],
                        "answer_index": 2,
                        "difficulty": 3,
                        "explanation": "`git restore --staged` moves the file from staging back to the working directory — edits intact, just no longer proposed. Plain `git restore` would also discard the edits (too destructive here), and `git rm` deletes the file.",
                        "company_tags": ["microsoft", "tcs"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does `git restore --source=HEAD~3 app.py` do?",
                        "choices": [
                            "Reverts the last 3 commits that touched app.py",
                            "Shows a diff of app.py across the last 3 commits",
                            "Deletes app.py from the last 3 commits",
                            "Restores app.py's working-tree copy to its content as of 3 commits ago, without touching history",
                        ],
                        "answer_index": 3,
                        "difficulty": 7,
                        "explanation": "`--source` picks which commit to restore FROM — a real, surgical flag. It only rewrites the working-tree file (unstaged change you can review); history is untouched. Perfect for \"give me the old version of this one file.\"",
                        "company_tags": ["google", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why is `git reset --hard` on an already-pushed branch considered dangerous in a team?",
                        "choices": [
                            "It rewrites shared history, so teammates' clones diverge and their next pull/merge breaks",
                            "It locks the branch for 24 hours",
                            "It emails the admin about your mistake",
                            "It permanently deletes the remote repository",
                        ],
                        "answer_index": 0,
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
                            "A lightweight movable pointer (reference) to a commit",
                            "A separate repository stored on the server",
                            "A backup of the working directory",
                            "A full copy of all project files",
                        ],
                        "answer_index": 0,
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
                            "The largest file in the repository",
                            "The first commit ever made in the repository",
                            "A pointer to the currently checked-out branch (or commit) — i.e., \"where you are\"",
                            "The remote server's main branch",
                        ],
                        "answer_index": 2,
                        "difficulty": 3,
                        "explanation": "HEAD points at your current branch (normally) — new commits advance whichever branch HEAD references. That's why `git log` shows `(HEAD -> main)`: you're on main.",
                        "company_tags": ["accenture", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why is creating a branch in Git nearly instantaneous even in huge repositories?",
                        "choices": [
                            "Branches are created on a remote server with more power",
                            "Git skips creating a branch until the first commit",
                            "Git compresses all files before branching",
                            "A branch is just a 41-byte file holding a commit hash — no files are copied",
                        ],
                        "answer_index": 3,
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
                            "`git switch -c` deletes the old branch",
                            "No difference at all",
                            "`git branch` only creates the branch (you stay where you are); `git switch -c` creates it AND moves you onto it",
                            "`git branch` creates a remote branch; `git switch -c` creates a local one",
                        ],
                        "answer_index": 2,
                        "difficulty": 2,
                        "explanation": "Creation vs creation+checkout: `git branch <name>` leaves HEAD untouched, so your next commit still lands on the old branch — a classic beginner trap. `-c` moves you onto the new branch immediately.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You want a `hotfix` branch starting from the tip of `main`, but you're currently on `feature-x`. Which command is correct?",
                        "choices": [
                            "`git switch -c hotfix`",
                            "`git branch hotfix` then merge main",
                            "`git checkout main -- hotfix`",
                            "`git switch -c hotfix main`",
                        ],
                        "answer_index": 3,
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
                            "`git branch -l`",
                            "`git remote --branches`",
                            "`git branch -a`",
                            "`git branch`",
                        ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "`git branch -a` (all) shows local branches plus `remotes/origin/...` tracking refs — essential for seeing what exists on the server. Plain `git branch` shows locals only.",
                        "company_tags": ["accenture", "wipro"],
                    },
                ],
            },
            {
                "slug": "git-branching-branching-model",
                "title": "The Branching Model: main → Feature → Merge",
                "theory_md": """## The Branching Model: main → Feature → Merge

This is THE workflow of professional software teams — the pattern
behind every pull request you'll ever open. Learn it cold.

### The core loop

```
        (feature branch grows here)
       /-- D -- E -- F   <-- feature-login
      /
A -- B -- C             <-- main (stays deployable)
              \\
               G -- H   <-- feature-darkmode
```

1. **`main` is sacred.** It always holds deployable, reviewed code.
   Nobody commits directly to it (enforced by branch protection on
   GitHub).
2. **Branch off for each unit of work.** One branch = one feature, fix,
   or experiment: `feature-login`, `fix-crash-142`, `experiment-cache`.
3. **Work and commit freely** on your branch. Break things — `main`
   doesn't care.
4. **Merge back via review.** Open a pull request; after review + CI,
   merge into `main`.
5. **Delete the branch.** Its commits now live on `main`'s history.

### The commands behind the diagram

```bash
# 1. Start from a fresh main
git switch main
git pull origin main

# 2. Branch off
git switch -c feature-login

# 3. Work: commits D, E, F happen here
git add login.py
git commit -m "Add login form"
git commit -m "Wire up session handling"

# 4. Keep the branch fresh while you work (avoid stale-branch pain)
git fetch origin
git merge origin/main        # or: git rebase origin/main (see later lesson)

# 5. Publish for review
git push -u origin feature-login
# -> open a Pull Request on GitHub: feature-login -> main

# 6. After the merge lands, clean up locally
git switch main
git pull
git branch -d feature-login
```

### Why not just commit to main?

- **Isolation:** half-done work never breaks the deployable branch.
- **Parallelism:** 10 developers, 10 branches, zero stepping on toes.
- **Review:** the pull request is the quality gate — discussion, CI
  tests, required approvals.
- **Revertability:** a bad feature = revert one merge commit, not surgery.

### Naming conventions teams use

```bash
feature/<name>    # feature/login-oauth
fix/<issue>       # fix/142-crash-on-empty-user
hotfix/<name>     # hotfix/payment-timeout
experiment/<name> # experiment/redis-cache
```

Consistent names make `git branch -a` readable at a glance.

### Long-lived vs short-lived

- **Short-lived** (the norm): feature branches live hours to days.
- **Long-lived** (the exceptions): `main`, sometimes `develop` or
  `release/*` — these are integration points, not workspaces.

**Takeaway:** `main` stays green; work happens on short-lived feature
branches; everything returns through review. This single diagram
explains 90% of professional Git usage.
""",
                "difficulty_min": 2,
                "difficulty_max": 7,
                "is_important": True,
                "has_visual": True,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "In the standard feature-branch model, what is the role of the `main` branch?",
                        "choices": [
                            "The branch where merge conflicts are stored",
                            "A scratch area where developers commit half-done experiments",
                            "The always-deployable source of truth; work reaches it only through reviewed merges",
                            "A backup branch updated once a month",
                        ],
                        "answer_index": 2,
                        "difficulty": 2,
                        "explanation": "`main` must always be in a releasable state — that's why direct commits are blocked (branch protection) and every change arrives via a reviewed pull request. Isolation of unfinished work is the model's whole purpose.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What is the correct sequence in the feature-branch workflow?",
                        "choices": [
                            "Push to main → create branch → merge branch into itself",
                            "Delete main → work on feature → recreate main",
                            "Commit to main → branch off → push → delete main",
                            "Update main → create feature branch → commit work → push → pull request → merge → delete branch",
                        ],
                        "answer_index": 3,
                        "difficulty": 3,
                        "explanation": "Start from fresh `main`, branch off, do the work in isolated commits, publish the branch, get it reviewed via PR, merge, then delete the branch. Every step protects `main`'s integrity.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why do teams prohibit committing directly to `main`?",
                        "choices": [
                            "Unreviewed, possibly broken work would land straight in the deployable branch with no quality gate",
                            "It makes `git log` run slower",
                            "Direct commits to main are deleted automatically",
                            "Git technically cannot commit to a branch named main",
                        ],
                        "answer_index": 0,
                        "difficulty": 4,
                        "explanation": "The PR is the quality gate — code review, CI tests, approvals. Direct commits bypass all of it, so one bad commit can break production for everyone. Branch protection rules enforce this on GitHub.",
                        "company_tags": ["amazon", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your feature branch has been open for a week and `main` moved forward. Before opening the PR, what's the best practice?",
                        "choices": [
                            "Nothing — Git handles stale branches automatically",
                            "Sync: `git fetch origin` then merge or rebase `origin/main` into your branch to resolve drift early",
                            "Delete the branch and start over",
                            "Force-push main into your branch",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "Long-lived branches drift from `main`, making the final merge painful. Periodically integrating `main` into your branch surfaces conflicts while they're small — the standard \"keep your branch fresh\" habit.",
                        "company_tags": ["microsoft", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "After your pull request is merged into `main`, what should you do with the feature branch?",
                        "choices": [
                            "Merge main back into it",
                            "Keep it forever as documentation",
                            "Delete it locally (`git branch -d`) and remotely — its commits now live in main's history",
                            "Rename it to main",
                        ],
                        "answer_index": 2,
                        "difficulty": 3,
                        "explanation": "Once merged, the branch's commits are part of `main`'s history — the branch pointer itself is disposable. Deleting keeps `git branch -a` readable; GitHub even offers a one-click delete after merge.",
                        "company_tags": ["infosys", "tcs"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A team needs an URGENT production fix while feature branches are mid-work. How does the branching model handle this?",
                        "choices": [
                            "Pause all feature branches until the fix is tested",
                            "Apply the fix inside someone's feature branch",
                            "Commit the fix directly to main, bypassing review",
                            "Branch `hotfix/<name>` off `main`, fix, review quickly, merge to `main` (and to develop/long-lived branches if they exist), then delete it",
                        ],
                        "answer_index": 3,
                        "difficulty": 7,
                        "explanation": "Hotfixes follow the SAME model at high speed: branch from `main` (production's state), minimal fix, expedited review, merge, delete. The model doesn't break for emergencies — it just runs faster, keeping `main`'s integrity intact.",
                        "company_tags": ["google", "accenture"],
                    },
                ],
            },
            {
                "slug": "git-branching-merging-and-fast-forward",
                "title": "Merging Branches & Fast-Forward",
                "theory_md": """## Merging Branches & Fast-Forward

**Merging** combines two branches' histories. You merge the feature
branch **into** `main` (direction matters — say it that way).

### The basic merge

```bash
git switch main
git merge feature-login
```

What Git does depends on history shape:

### Case 1: Fast-forward (the simple case)

`main` hasn't moved since you branched — its tip is an ancestor of the
feature branch:

```
Before:  A -- B          <-- main
              \\
               C -- D    <-- feature-login

git switch main && git merge feature-login

After:   A -- B -- C -- D   <-- main, feature-login
```

No new commit needed — Git just **slides the `main` pointer forward**.
Clean, linear history.

### Case 2: True merge (3-way)

Both branches moved — Git creates a **merge commit** with two parents:

```
        C -- D   <-- feature-login
       /      \\
A -- B         M   <-- main (merge commit)
       \\      /
        E -- F     (main had moved too)
```

```bash
git switch main
git merge feature-login
# Merge made by the 'ort' strategy.
```

Inspect it:

```bash
git log --graph --oneline
git show M          # a merge commit shows both parents' diffs
```

### Controlling the behavior

```bash
git merge --ff-only feature-login
# merge ONLY if fast-forward is possible; abort otherwise (safe default for some teams)

git merge --no-ff feature-login
# ALWAYS create a merge commit, even when fast-forward is possible
# -> preserves the visual "this was a feature" grouping in history
```

Many teams use `--no-ff` (or GitHub's \"create a merge commit\" PR
option) so each feature is one visible merge bubble.

### Aborting a merge gone wrong

```bash
git merge --abort    # only during an uncommitted conflicted merge
# back to the pre-merge state, as if it never happened
```

### Merge vs pull

```bash
git pull = git fetch + git merge   # (default; configurable to rebase)
```

`git pull` merges the remote branch into yours — which is why pulls can
produce merge commits and conflicts. Understanding merge = understanding
half of what `pull` does.

### Deleting after merge

```bash
git branch -d feature-login   # safe: Git verifies it's fully merged
```

**Takeaway:** fast-forward = pointer slide (linear); true merge = new
merge commit joining two lines. Use `--ff-only` when you demand linear,
`--no-ff` when you want features visible as units, `--abort` as your
escape hatch.
""",
                "difficulty_min": 1,
                "difficulty_max": 6,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "When does Git perform a fast-forward merge?",
                        "choices": [
                            "When there are merge conflicts to resolve",
                            "Only when merging remote branches",
                            "When both branches have diverged with new commits",
                            "When the target branch (e.g. main) hasn't moved since the feature branch was created — its tip is an ancestor of the feature tip",
                        ],
                        "answer_index": 3,
                        "difficulty": 2,
                        "explanation": "Fast-forward needs a straight line: `main`'s tip must be an ancestor of the feature tip. Then Git just slides the `main` pointer forward — no merge commit, perfectly linear history.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What is a merge commit?",
                        "choices": [
                            "A commit with TWO parents, created when Git joins two diverged lines of history",
                            "A commit that is automatically deleted after pushing",
                            "Any commit whose message starts with \"Merge\"",
                            "A commit that only exists on the remote server",
                        ],
                        "answer_index": 0,
                        "difficulty": 1,
                        "explanation": "When both sides moved, Git can't fast-forward, so it creates a commit with two parents tying the histories together. `git log --graph` shows it as the junction point.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does `git merge --ff-only feature-x` do?",
                        "choices": [
                            "Forces a merge commit even when fast-forward is possible",
                            "Merges only if a fast-forward is possible; aborts without changing anything otherwise",
                            "Deletes the feature branch after merging",
                            "Merges without checking for conflicts",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "`--ff-only` is the \"linear history or nothing\" option — great for keeping `main` clean. If the branches diverged, it exits safely instead of creating a surprise merge commit.",
                        "company_tags": ["google", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why do some teams always merge with `--no-ff`?",
                        "choices": [
                            "It's required by GitHub",
                            "It makes merges faster",
                            "It always creates a merge commit, preserving each feature as a visible unit in history even when fast-forward was possible",
                            "It prevents all merge conflicts",
                        ],
                        "answer_index": 2,
                        "difficulty": 5,
                        "explanation": "With `--no-ff`, `git log --graph` shows every feature as a distinct merge bubble — you can see exactly which commits belonged to which feature and revert a whole feature with one commit. Traceability over minimalism.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You started a merge, hit a wall of conflicts, and want to pretend the merge never happened. Which command?",
                        "choices": [
                            "`git reset --hard origin/main`",
                            "`git revert HEAD`",
                            "`git stash --merge`",
                            "`git merge --abort`",
                        ],
                        "answer_index": 3,
                        "difficulty": 3,
                        "explanation": "`git merge --abort` is the dedicated escape hatch — it works only while a merge is in progress and uncommitted, restoring the exact pre-merge state. Reach for it before trying anything destructive.",
                        "company_tags": ["infosys", "tcs"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does `git pull` do by default?",
                        "choices": [
                            "`git fetch` followed by `git merge` of the remote branch into your current branch",
                            "Deletes your local commits and replaces them with remote ones",
                            "Creates a new branch from the remote",
                            "Only downloads objects without changing your branch",
                        ],
                        "answer_index": 0,
                        "difficulty": 6,
                        "explanation": "`git pull` = fetch + merge. That's why pulls can produce merge commits or conflicts — it's literally running a merge under the hood. (It can be configured to rebase instead via `pull.rebase`.)",
                        "company_tags": ["accenture", "wipro"],
                    },
                ],
            },
            {
                "slug": "git-branching-merge-conflicts",
                "title": "Merge Conflicts: Resolve Them Step by Step",
                "theory_md": """## Merge Conflicts: Resolve Them Step by Step

A **conflict** happens when Git can't automatically decide whose change
wins — typically two branches edited the **same lines** of the same file.
Conflicts are normal, not emergencies. Resolve them calmly, every time,
with this recipe.

### Step 0: See the conflict

```bash
git switch main
git merge feature-login
# Auto-merging app.py
# CONFLICT (content): Merge conflict in app.py
# Automatic merge failed; fix conflicts and then commit the result.
```

### Step 1: Find the conflicted files

```bash
git status
# Unmerged paths:
#   both modified:   app.py
```

### Step 2: Open the file — read the markers

```python
<<<<<<< HEAD
timeout = 30          # main's version
=======
timeout = 60          # feature-login's version
>>>>>>> feature-login
```

- `<<<<<<< HEAD` → `=======`: **your** current branch's content.
- `=======` → `>>>>>>> feature-login`: the **incoming** branch's content.

### Step 3: Edit to the correct final content

This is a **human decision**, not a Git decision. Keep one side, keep
both, or write something new entirely:

```python
timeout = 45          # you decide — maybe neither original was right
```

Delete ALL the `<<<<<<<`, `=======`, `>>>>>>>` marker lines. Leftover
markers = broken code (and an embarrassing commit).

### Step 4: Mark resolved and commit

```bash
git add app.py                 # tells Git: "I resolved this"
git status                     # confirm "all conflicts fixed"
git commit                     # completes the merge commit (no -m needed;
                               # Git prepared a default merge message)
```

### The full recipe as a checklist

```bash
git merge feature-x        # 1. attempt
git status                 # 2. list conflicted files
# 3. edit each file, remove markers, choose final content
git add <resolved files>   # 4. stage resolutions
git commit                 # 5. finish the merge
git log --graph --oneline  # 6. verify history looks right
```

### Tools that help

```bash
git diff                   # shows conflict markers with context
git diff --check           # finds LEFTOVER markers / whitespace errors

# For a visual 3-way merge tool (meld, vscode, etc.):
git mergetool              # launches your configured merge tool
```

Configure one once:

```bash
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'
```

### Preventing conflicts (mostly)

- **Pull/merge `main` into your branch often** — small conflicts beat big ones.
- **Communicate:** two people rewriting the same function = conflict guaranteed.
- **Small, focused commits** make conflicts localized and obvious.

**Takeaway:** conflict = Git asking a human to decide. Status → edit
(remove markers) → add → commit. Never fear conflicts; fear committing
unresolved markers.
""",
                "difficulty_min": 2,
                "difficulty_max": 7,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "When does Git report a merge conflict?",
                        "choices": [
                            "When both branches changed the same LINES (or adjacent lines) of the same file and Git can't reconcile them automatically",
                            "Whenever you merge any branch",
                            "Only when merging remote branches",
                            "Whenever two branches touch the same FILE at all",
                        ],
                        "answer_index": 0,
                        "difficulty": 2,
                        "explanation": "Git auto-merges happily when changes are in different parts of a file. Conflicts arise only where both sides edited overlapping regions and Git can't know which intent wins — that's precisely when a human must decide.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "In a conflicted file, what do the sections between `<<<<<<< HEAD` / `=======` / `>>>>>>> feature-x` represent?",
                        "choices": [
                            "Corrupted data that must be deleted entirely",
                            "HEAD's version (your current branch) above `=======`, and the incoming branch's version below it",
                            "The incoming branch's version above, yours below",
                            "Two copies of the same content for backup",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "Markers delimit the two competing versions: from `<<<<<<< HEAD` to `=======` is YOUR branch's content; from `=======` to `>>>>>>> branch` is the incoming branch's. You edit the region into the correct final content and delete all markers.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What is the correct order of steps to resolve a merge conflict?",
                        "choices": [
                            "Delete the conflicted files → `git commit` → restore from backup",
                            "`git commit` → edit files → `git add` → `git merge --continue`",
                            "Edit conflicted files (remove markers, choose final content) → `git add` the resolved files → `git commit` to finish the merge",
                            "`git add` everything → `git reset --hard` → `git merge` again",
                        ],
                        "answer_index": 2,
                        "difficulty": 4,
                        "explanation": "The recipe: 1) `git status` to find conflicted files, 2) edit each into correct final content with markers removed, 3) `git add` marks them resolved, 4) `git commit` seals the merge commit. `git add` BEFORE editing would stage the raw markers — wrong order.",
                        "company_tags": ["amazon", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What happens if you commit a file that still contains `<<<<<<<` conflict markers?",
                        "choices": [
                            "Git strips the markers silently during commit",
                            "The merge is automatically aborted",
                            "Git blocks the commit automatically in all cases",
                            "The markers become part of your code — usually breaking it — because Git trusts your resolution",
                        ],
                        "answer_index": 3,
                        "difficulty": 5,
                        "explanation": "Once you `git add` a file, Git assumes YOU resolved it correctly — markers included. Committed markers mean broken code in history. Always run `git diff --check` before the final commit to catch leftovers.",
                        "company_tags": ["microsoft", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which command checks for leftover conflict markers and whitespace errors before you finalize a merge?",
                        "choices": [
                            "`git diff --check`",
                            "`git status --verify`",
                            "`git merge --dry-run`",
                            "`git log --check`",
                        ],
                        "answer_index": 0,
                        "difficulty": 6,
                        "explanation": "`git diff --check` is the real pre-commit sanity scan — it flags whitespace errors AND leftover conflict markers. The other three commands don't exist in this form.",
                        "company_tags": ["google", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What's the most effective habit for AVOIDING large, painful merge conflicts?",
                        "choices": [
                            "Never merge; always work on main directly",
                            "Frequently merge/rebase the latest `main` into your feature branch so drift stays small",
                            "Commit only once at the very end",
                            "Use `git merge --abort` every time a conflict appears",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "Conflicts grow with divergence: a week-old branch conflicts everywhere. Syncing `main` into your branch daily keeps conflicts tiny and localized. Aborting doesn't resolve anything, and avoiding merges just defers the pain.",
                        "company_tags": ["amazon", "microsoft"],
                    },
                ],
            },
            {
                "slug": "git-branching-rebase-vs-merge",
                "title": "Rebase vs Merge & the Golden Rule",
                "theory_md": """## Rebase vs Merge & the Golden Rule

Merge and rebase both combine histories — but produce **different
history shapes**. Choosing between them is a team-culture decision;
understanding both is an interview requirement.

### Merge: preserve history as it happened

```bash
git switch feature-login
git merge main
```

Keeps every commit exactly as created, joined by merge commits. History
is truthful but can look like spaghetti.

### Rebase: replay commits on a new base

```bash
git switch feature-login
git rebase main
```

Git **re-writes** your branch's commits as if they were created on top
of `main`'s latest tip:

```
Before rebase:          After rebase:
      D -- E  (feature)       D' -- E'  (feature, NEW hashes)
     /                      /
A -- B -- C  (main)    A -- B -- C  (main)
```

D and E become D' and E' — **new commit hashes**, same changes, linear
story. Your feature now applies cleanly onto the latest `main`.

### Side-by-side

| | Merge | Rebase |
|---|---|---|
| History | truthful, with merge commits | linear, rewritten |
| Commit hashes | unchanged | **new hashes** (rewritten!) |
| Conflicts | resolved once in merge commit | resolved **per commit** replayed |
| Best for | shared branches (`main`) | cleaning up YOUR branch before review |

### The golden rule of rebasing

> **Never rebase commits that exist outside your repository**
> (i.e., commits you've pushed to a shared branch).

Why? Rebase creates NEW hashes. Teammates holding the OLD hashes now
have divergent history — merges break, work gets duplicated, people get
angry. Rebase is for **private, local** cleanup only.

### The professional rebase flow

```bash
# On YOUR feature branch, before opening the PR:
git fetch origin
git rebase origin/main      # replay my commits onto latest main
# resolve any conflicts per-commit, then:
git rebase --continue
# (if you already pushed the branch: git push --force-with-lease)
```

`--force-with-lease` (not bare `--force`) refuses to overwrite if someone
else pushed meanwhile — the polite force-push.

### Interactive rebase: history surgery

```bash
git rebase -i HEAD~3
# pick, reword, squash, fixup, drop commits — rewrite your last 3 commits
```

Use it to squash \"wip\" commits into clean ones BEFORE review. Never
on shared history.

### Abort a bad rebase

```bash
git rebase --abort    # back to pre-rebase state
```

**Takeaway:** rebase = replay my private commits onto a fresh base for
a clean linear story; merge = join histories truthfully. Golden rule:
rebase only what you haven't shared.
""",
                "difficulty_min": 2,
                "difficulty_max": 8,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "What does `git rebase main` do while you're on `feature-x`?",
                        "choices": [
                            "Merges main into feature-x with a merge commit",
                            "Rewrites feature-x's commits as new commits replayed on top of main's latest tip",
                            "Deletes feature-x and recreates it from main",
                            "Pushes feature-x to the remote",
                        ],
                        "answer_index": 1,
                        "difficulty": 2,
                        "explanation": "Rebase takes your branch's commits and replays them one by one onto the new base, producing NEW commit hashes (D becomes D'). The result reads as a clean linear story: \"my work, on top of latest main.\"",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What is the Golden Rule of rebasing?",
                        "choices": [
                            "Never rebase more than 3 commits at once",
                            "Always rebase instead of merging",
                            "Never rebase commits that have been pushed to a shared branch (only rebase local/private commits)",
                            "Rebase at least once per day",
                        ],
                        "answer_index": 2,
                        "difficulty": 3,
                        "explanation": "Rebase rewrites hashes; teammates with the old hashes get divergent history, broken merges, and duplicated work. Local-only commits are safe to rewrite because nobody else has them.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Why does rebasing pushed commits break teammates' repositories?",
                        "choices": [
                            "It locks the remote repository",
                            "It changes file permissions on their machines",
                            "It deletes their local branches automatically",
                            "Rebased commits get NEW hashes, so their clones see divergent history and can't cleanly pull/merge anymore",
                        ],
                        "answer_index": 3,
                        "difficulty": 5,
                        "explanation": "Git identifies commits by hash. After a rebase, \"the same\" changes exist under new hashes — Git treats them as different commits, so teammates' history forks from the rewritten one. Recovery means everyone reconciling by hand.",
                        "company_tags": ["google", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "During a rebase you hit conflicts on the second of five replayed commits. How does conflict resolution differ from a merge?",
                        "choices": [
                            "Conflicts are resolved PER COMMIT as each is replayed, running `git rebase --continue` after each",
                            "Rebase never has conflicts",
                            "You must abort and use merge instead",
                            "It's identical — one resolution for everything",
                        ],
                        "answer_index": 0,
                        "difficulty": 6,
                        "explanation": "Rebase replays commits sequentially, so each commit can conflict independently — resolve, `git add`, `git rebase --continue`, repeat. More steps than a merge's single resolution, but each conflict is smaller and attributed to its own commit.",
                        "company_tags": ["microsoft", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does `git rebase -i HEAD~3` let you do?",
                        "choices": [
                            "Ignore the last 3 commits during merge",
                            "Interactively pick, reword, squash, or drop your last 3 commits — rewriting local history before review",
                            "Install 3 plugins for rebasing",
                            "Rebase across 3 different remotes",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "Interactive rebase opens an editor listing the last 3 commits where you can `pick`/`reword`/`squash`/`fixup`/`drop` each — the standard way to turn messy \"wip\" commits into a clean review-ready series. Local-only, per the golden rule.",
                        "company_tags": ["google", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "After rebasing a feature branch you had already pushed (solo branch, no teammates), which push is correct?",
                        "choices": [
                            "You can never push after a rebase",
                            "`git push` — it will work normally",
                            "`git push --force-with-lease` — overwrites the remote branch but refuses if someone else pushed meanwhile",
                            "`git push --delete origin feature-x`",
                        ],
                        "answer_index": 2,
                        "difficulty": 8,
                        "explanation": "Rebase rewrote the hashes, so a normal push is rejected (histories diverged). `--force-with-lease` is the safe overwrite: it pushes your rewritten history but aborts if the remote moved since your last fetch — unlike bare `--force`, which blindly clobbers.",
                        "company_tags": ["amazon", "accenture"],
                    },
                ],
            },
            {
                "slug": "git-branching-git-stash",
                "title": "Stashing: Park Work in Progress",
                "theory_md": """## Stashing: Park Work in Progress

You're mid-feature with dirty files when an urgent fix lands on `main`.
You can't switch branches with conflicting uncommitted changes — and
you don't want a half-baked commit. **`git stash`** shelves your work
safely so the tree goes clean, then restores it later.

### The basic cycle

```bash
# ... half-done work, files modified ...
git stash              # park everything; working tree is clean now
git switch main
# ... do the urgent fix, commit ...
git switch feature-x
git stash pop          # restore the parked changes, drop the stash
```

### What's in the stash?

```bash
git stash list
# stash@{0}: WIP on feature-x: a3f9c21 Add login form
# stash@{1}: WIP on main: 7d2e4aa Fix typo

git stash show -p stash@{0}   # see the DIFF inside a stash entry
```

A stash is a stack — `stash@{0}` is the newest.

### pop vs apply

```bash
git stash pop     # restore AND delete the stash entry (usual choice)
git stash apply   # restore but KEEP the entry (safer if unsure)
git stash drop    # delete an entry without applying
```

`pop` can conflict if the tree changed meanwhile — resolve like a merge,
then the entry is dropped only on clean apply... actually: `pop` drops
the entry only if applying succeeded without conflicts.

### Stashing selectively

```bash
git stash push -m "half-done oauth wiring"   # named stash — do this!
git stash -u                                 # include UNTRACKED files too
git stash --keep-index                        # stash unstaged only, keep staged
```

Default `git stash` ignores untracked files — the #1 stash surprise.
Use `-u` when new files matter.

Named stashes (`-m`) save you from the \"which WIP was which?\" guessing
game in `git stash list`.

### Stash one file only

```bash
git stash push -- app.py    # stash changes to just app.py
```

### Real-world scenario

```bash
git stash push -m "WIP: dark mode toggle"
git switch main
git pull
git switch -c hotfix/payment-timeout
# ... fix, commit, push, PR ...
git switch feature-x
git stash pop
# continue where you left off
```

**Takeaway:** stash = clipboard for uncommitted work. Name your stashes,
remember `-u` for untracked files, and prefer `pop` for the clean
park-and-restore cycle.
""",
                "difficulty_min": 1,
                "difficulty_max": 6,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "What does `git stash` do?",
                        "choices": [
                            "Pushes your work to the remote server",
                            "Commits your changes to a temporary branch",
                            "Temporarily shelves uncommitted changes, restoring a clean working tree, so you can re-apply them later",
                            "Deletes all uncommitted changes permanently",
                        ],
                        "answer_index": 2,
                        "difficulty": 1,
                        "explanation": "Stash records your dirty working-tree state onto a stack and reverts the tree to HEAD — no commit created. `git stash pop` brings it back. It's the tool for \"I need a clean tree RIGHT NOW but my work isn't committable yet.\"",
                        "company_tags": ["tcs", "wipro"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What's the difference between `git stash pop` and `git stash apply`?",
                        "choices": [
                            "They are identical aliases",
                            "`apply` deletes the stash; `pop` keeps it",
                            "`pop` only works on the newest stash",
                            "`pop` restores and REMOVES the stash entry; `apply` restores but KEEPS it on the stack",
                        ],
                        "answer_index": 3,
                        "difficulty": 3,
                        "explanation": "`pop` = apply + drop (the usual park-and-restore). `apply` leaves the entry in place — handy when you want to restore the same changes in two places or aren't sure the restore is safe yet.",
                        "company_tags": ["infosys", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You stashed your work, but a brand-new file `draft.md` is still sitting in your working tree. Why?",
                        "choices": [
                            "By default `git stash` only stashes TRACKED changes; untracked files need `git stash -u`",
                            "New files can never be stashed",
                            "You must commit new files before stashing",
                            "The stash command failed silently",
                        ],
                        "answer_index": 0,
                        "difficulty": 4,
                        "explanation": "Default stash covers modified tracked files only — untracked files are left behind (the classic surprise). `git stash -u` (or `--include-untracked`) includes them in the stash.",
                        "company_tags": ["amazon", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "How do you create a stash with a descriptive name instead of the generic \"WIP\" message?",
                        "choices": [
                            "`git stash --title \"half-done oauth wiring\"`",
                            "`git stash push -m \"half-done oauth wiring\"`",
                            "`git stash --name \"half-done oauth wiring\"`",
                            "`git stash save-name \"half-done oauth wiring\"`",
                        ],
                        "answer_index": 1,
                        "difficulty": 2,
                        "explanation": "`git stash push -m \"message\"` is the real syntax — `push` is the modern subcommand, `-m` the message. Named stashes make `git stash list` actually readable when several are stacked.",
                        "company_tags": ["microsoft", "tcs"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "How do you inspect the diff contained in the second stash entry without applying it?",
                        "choices": [
                            "`git stash view 1`",
                            "`git log stash@{1}`",
                            "`git stash show -p stash@{1}`",
                            "`git diff stash@{1}`",
                        ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "`git stash show -p <entry>` prints the patch stored in that stash — the safe way to peek before popping. The stack is zero-indexed, so `stash@{1}` is the second-newest.",
                        "company_tags": ["flipkart", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You only want to stash changes to `app.py` and leave everything else dirty. Which command?",
                        "choices": [
                            "`git stash --only app.py`",
                            "`git stash app.py --single`",
                            "Stash can't be limited to one file",
                            "`git stash push -- app.py`",
                        ],
                        "answer_index": 3,
                        "difficulty": 5,
                        "explanation": "`git stash push -- <pathspec>` stashes only matching paths — a real, underused form. The `--` separates options from paths, just like with `git log --`.",
                        "company_tags": ["google", "wipro"],
                    },
                ],
            },
            {
                "slug": "git-branching-detached-head",
                "title": "Detached HEAD: Visiting History",
                "theory_md": """## Detached HEAD: Visiting History

Normally HEAD points to a **branch** (`main`), and commits advance that
branch. **Detached HEAD** means HEAD points directly at a **commit**
instead — you're visiting history, not standing on a branch.

### How you get there

```bash
git switch --detach a3f9c21     # modern, explicit
git checkout a3f9c21            # classic — same effect

# Git warns you:
# Note: switching to 'a3f9c21'.
# You are in 'detached HEAD' state...
# HEAD is now at a3f9c21 Fix crash when username is empty
```

### What it looks like

```
Normal:        HEAD -> main -> C
Detached:      HEAD -> B        (main still -> C)
```

### Why it's useful

- **Inspect old code:** build/test exactly what shipped in v1.2.
- **Bisect bugs:** `git bisect` hops between commits in detached HEAD.
- **Review a PR's commits** without creating a branch.

```bash
git switch --detach v2.0.0    # look at the tagged release
# ... run the old code, read files ...
git switch main               # back to normal — nothing lost
```

### The danger: committing while detached

Commits made in detached HEAD belong to **no branch**:

```
HEAD -> X (new commit, floating)
main -> C
```

Switch branches and X becomes **orphaned** — reachable only via the
reflog. To keep such work, create a branch BEFORE leaving:

```bash
git switch -c rescue-branch    # attach a branch to your commits
# or: git branch rescue-branch  (then switch to it)
```

### Getting back to safety

```bash
git switch main        # re-attach HEAD to a branch — done
```

### Recovering orphaned commits (the safety net)

Nothing is truly lost for ~90 days thanks to the **reflog**:

```bash
git reflog
# a3f9c21 HEAD@{0}: commit: experimental fix   <- your orphan!
git switch -c recovery a3f9c21   # resurrect it onto a branch
```

### When you'll see this in real life

- CI systems check out specific commits (detached by design).
- `git checkout <tag>` detaches — tags aren't branches.
- Accidentally: `git checkout a3f9c21` while exploring history.

**Takeaway:** detached HEAD = read-only time travel. Look around freely;
if you commit something worth keeping, give it a branch before you
leave. `git reflog` is your time machine's backup.
""",
                "difficulty_min": 2,
                "difficulty_max": 7,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "What does \"detached HEAD\" state mean?",
                        "choices": [
                            "The main branch was deleted",
                            "Your working tree is corrupted",
                            "The repository has no commits",
                            "HEAD points directly at a commit instead of at a branch — you're visiting history, not standing on a branch",
                        ],
                        "answer_index": 3,
                        "difficulty": 2,
                        "explanation": "Normally HEAD → branch → commit. Detached, HEAD → commit directly (e.g. after `git checkout a3f9c21`). You can look around freely, but new commits won't belong to any branch.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Which command intentionally enters detached HEAD state at commit `a3f9c21`?",
                        "choices": [
                            "`git switch --detach a3f9c21`",
                            "`git branch --detach a3f9c21`",
                            "`git detach a3f9c21`",
                            "`git checkout -b a3f9c21`",
                        ],
                        "answer_index": 0,
                        "difficulty": 3,
                        "explanation": "`git switch --detach <commit>` is the modern explicit spelling (classic: `git checkout <commit>`). `-b` would CREATE a branch named a3f9c21 — the opposite of detaching.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You committed twice while in detached HEAD, then switched back to `main`. What happened to those two commits?",
                        "choices": [
                            "They were merged into main automatically",
                            "They're orphaned — on no branch — but recoverable via `git reflog` for ~90 days",
                            "They were deleted permanently and instantly",
                            "They were pushed to the remote",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "Detached commits belong to no branch, so leaving detaches you from them too — but Git keeps them in the reflog (default 90 days). `git reflog` finds the hash, then `git switch -c recovery <hash>` resurrects them.",
                        "company_tags": ["google", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You're in detached HEAD and just made an experimental commit you want to KEEP. What's the right move before switching away?",
                        "choices": [
                            "Nothing — the commit is safe on its own",
                            "`git stash` the commit",
                            "`git switch -c experiment` to create a branch pointing at your commit",
                            "`git push` immediately",
                        ],
                        "answer_index": 2,
                        "difficulty": 4,
                        "explanation": "Creating a branch attaches a permanent ref to your commit, so it can't be orphaned. Push won't work well (no upstream branch), and stash only handles uncommitted changes — not commits.",
                        "company_tags": ["microsoft", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "How do you get OUT of detached HEAD state and back to normal?",
                        "choices": [
                            "`git head --attach`",
                            "Delete the .git/HEAD file",
                            "`git rebase --abort`",
                            "`git switch main` (or any branch name)",
                        ],
                        "answer_index": 3,
                        "difficulty": 3,
                        "explanation": "Switching to any branch re-attaches HEAD to that branch — that's the entire fix. Nothing is lost; you were only ever \"visiting\" the commit.",
                        "company_tags": ["infosys", "tcs"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A CI pipeline checks out the exact commit `9f2b1aa` to run tests. Why is detached HEAD the CORRECT state there?",
                        "choices": [
                            "The pipeline needs the exact commit's code reproducibly; no branch work happens, so no branch pointer is needed or wanted",
                            "Detached HEAD makes tests run faster",
                            "It's a bug in the CI configuration",
                            "CI servers are not allowed to create branches",
                        ],
                        "answer_index": 0,
                        "difficulty": 7,
                        "explanation": "CI wants byte-exact reproducibility of one commit — checking out the hash directly (detached) guarantees that, with no branch that could move. Detached HEAD isn't an error state; it's the right tool for read-only inspection.",
                        "company_tags": ["accenture", "google"],
                    },
                ],
            },
        ],
    },
]
