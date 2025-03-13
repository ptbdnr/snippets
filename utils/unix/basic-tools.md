# Basic Tools Command Examples

## echo
`echo` outputs the given text to the terminal.

```bash
# Print a simple message
echo "Hello, world!"

# Print a variable's value
name="Joe"
echo "Hello, $name"
```

## touch
`touch` creates an empty file or updates the timestamp of an existing file.

```bash
# Create an empty file named example.txt
touch example.txt

# Update the timestamp of example.txt
touch example.txt
```

## uname
`uname` displays system information.

```bash
# Display all available system information
uname -a

# Display only the kernel name
uname -s
```

## find
`find` searches for files and directories in a directory hierarchy.

```bash
# Find all files named "example.txt" starting from the current directory
find . -name "example.txt"

# Find all files larger than 1MB in /var/log
find /var/log -type f -size +1M
```

## ls
`ls` lists directory contents.

```bash
# List files and directories in the current directory
ls

# List in long format with human-readable sizes
ls -lh

# List all files, including hidden ones
ls -la
```

## pwd
`pwd` prints the current working directory.

```bash
# Display your current directory path
pwd
```

## top
`top` provides a dynamic view of the running system processes.

```bash
# Run top to monitor processes in real-time
top

# In top, press 'q' to quit monitoring
```