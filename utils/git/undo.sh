# # Revert a change

# ## Undo local change (before staging)
# see https://gitimmersion.com/lab_14.html

# ## Undo staged change (before committing)
# see https://gitimmersion.com/lab_15.html (using git >= 2.24)
git reset --soft HEAD~1 git reset HEAD <file>
# delete file from index, then commit your changes again
git rm --cached <file>
git commit --amend

# ## Undo committed changes
# see https://gitimmersion.com/lab_16.html

# ## Return to older commit in a branch
# see https://gitimmersion.com/lab_17.html 
# Note: commits don't disappear, remain in the repo
# References: https://devconnected.com/how-to-remove-files-from-git-commit/

 