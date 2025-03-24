# Text Processing Command Examples

## cat
Display file contents.

The name "cat" is short for "concatenate," which refers to its original purpose of joining files together. Over time, it became a common Unix command to simply display file contents in the terminal, making it a handy tool for quickly viewing files.

Examples:

```bash
# Display the contents of a file
cat file.txt

# Display multiple files one after the other
cat file1.txt file2.txt
```

## grep
Search for a pattern in files.

Examples:

```bash
# Search for the term "error" in file.txt (case-sensitive)
grep "error" file.txt

# Search for "error" in a case-insensitive manner
grep -i "error" file.txt

# Search recursively in a directory for "error"
grep -r "error" /path/to/directory

# Search recursively in a directory filtering for files filename.ext for "error"
grep -r --include="filename.ext" "error" /path/to/directory

# Search using a regular expression for lines starting with "start"
grep "^start" file.txt
```

## sort
Sort lines in a file.

Examples:

```bash
# Sort lines alphabetically
sort file.txt

# Sort lines in reverse (descending) order
sort -r file.txt

# Sort a file numerically by the second column
sort -k2 -n file.txt
```

## head
Display the beginning of a file.

Examples:

```bash
# Display the first 10 lines of file.txt (default)
head file.txt

# Display the first 5 lines of file.txt
head -n 5 file.txt
```

## tail
Display the end of a file.

Examples:

```bash
# Display the last 10 lines of file.txt (default)
tail file.txt

# Display the last 5 lines of file.txt
tail -n 5 file.txt

# Follow the file in real time (useful for log files)
tail -f file.txt
```
