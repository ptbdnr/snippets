# Git Command Examples

## General Commands

```bash
# Check the status of your repository
git status
```

```bash
# Stage changes for commit
git add filename
```

```bash
# Commit staged changes with a message
git commit -m "Your commit message"
```

```bash
# Push commits to a remote repository
git push origin main
```


## Config Commands

```bash
# Set username (for all repositories, use `--global`)
git config --global user.name "Your Name"
```

```bash
# Read username configuration
git config user.name
```

```bash
# Set email address (for all repositories, use `--global`)
git config --global user.email "your.email@example.com"
```

```bash
# Read email configuration
git config user.email
```


## Listing & Log

```bash
# List files in the git repository
git ls-files
```

```bash
# View commit history with a custom format, see: https://gitimmersion.com/lab_10.html:
git log --pretty=format:'%h %ad | %s%d [%an]' --graph --date=short
```

```bash
# Alternative log view (if alias is set), see https://gitimmersion.com/lab_11.html:
git hist
```


## Undo Changes

Commits don't disappear, remain in the repo
References: https://devconnected.com/how-to-remove-files-from-git-commit/

```bash
# Revert file to a previous commit:
git checkout <COMMIT_ID> -- path/to/file.ext
```

```bash
# Undo staged change (before committing), see [Git Lab 14](https://gitimmersion.com/lab_14.html):
git reset HEAD <file>
```

```bash
# Undo staged change (before committing), see [Git Lab 14](https://gitimmersion.com/lab_15.html) (using git >= 2.24):
git reset --soft HEAD~1 
git reset HEAD <file>
```

```bash
# Remove file from index and amend the commit:
git rm --cached <file>
git commit --amend
```

- **Other Undo Actions:**
  - **Undo local changes (before staging):** Refer to [Git Lab 14](https://gitimmersion.com/lab_14.html).
  - **Undo committed changes:** Refer to [Git Lab 16](https://gitimmersion.com/lab_16.html).
  - **Return to an older commit in a branch:** Refer to [Git Lab 17](https://gitimmersion.com/lab_17.html).


## Learning Resources

* [Pro Git](http://git-scm.com/book), an online version of the Pro Git book. Written by Scott Chacon. Published by Apress.
* [Git Immersion](http://gitimmersion.com/), a try-it-yourself guided tour that walks you through the fundamentals of using Git. Published by Neo Innovation, Inc.
* [Git Reference](http://gitref.org/index.html), an online quick reference that can also be used as a more in-depth Git tutorial. Published by the GitHub team.
* [Git Cheat Sheet](https://github.com/github/training-kit/blob/master/downloads/github-git-cheat-sheet.md) with basic Git command syntax. Published by the GitHub team.
* [Git Pocket Guide](http://www.amazon.com/Git-Pocket-Guide-Richard-Silverman/dp/1449325866). Written by Richard E. Silverman. Published by O'Reilly Media, Inc.
* [Trunk-based development](https://www.atlassian.com/continuous-delivery/continuous-integration/trunk-based-development) is a version control management practice where developers merge small, frequent updates to a code "trunk" or main branch.