# Editors Command Examples

## nano
`nano` is a simple command-line text editor. Examples:

```bash
# Open or create a file named "example.txt" in nano
nano example.txt

# Open a file with line numbers enabled (if configured in your .nanorc)
nano -l example.txt
```

To exit nano, you follow these steps:
- Press Ctrl + X.
- If you made changes, nano will ask whether to save the file.
    - Press Y to save (then confirm the file name) or N to discard changes.
- Nano will then close the editor.

## vim
`vim` is a powerful text editor. Examples:

```bash
# Open a file named "example.txt" in vim
vim example.txt

# Open vim and edit a file, starting in insert mode
vim -c "startinsert" example.txt
```

To exit `vim`, you switch to Normal mode (pressing <kbd>Esc</kbd>) and then entering one of the following commands:

To quit if there are no unsaved changes:
<kbd>:q</kbd> then press <kbd>Enter</kbd>

To save changes and quit:
<kbd>:wq</kbd> then press <kbd>Enter</kbd>

To exit without saving any changes (force quit):
<kbd>:q!</kbd> then press <kbd>Enter</kbd>

Select the command that fits your workflow.


## less
`less` is used for viewing file contents. Examples:

```bash
# View the contents of a file with paging
less example.txt

# Open a file and search for a term (case insensitive by default)
less -p "searchTerm" example.txt
```
To exit `less`, you press the q key to quit the less utility.

## more
`more` is another pager program. Examples:

```bash
# View the contents of a file one screen at a time
more example.txt

# Use the space bar to scroll down one page at a time
more example.txt
```

To exit `more`, you press the <kbd>q</kbd> key.