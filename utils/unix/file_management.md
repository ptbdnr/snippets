# File Management Commands

## cp — Copy Files and Directories

Examples:

```bash
# Copy a file
cp source.txt destination.txt

# Copy multiple files to a directory
cp file1.txt file2.txt /path/to/destination/

# Copy a directory recursively
cp -r my_directory/ /path/to/destination/
```

## mv — Move or Rename Files and Directories

Examples:

```bash
# Rename a file
mv oldname.txt newname.txt

# Move a file to a different directory
mv file.txt /new/path/

# Move multiple files to a directory
mv file1.txt file2.txt /destination/directory/
```

## rm — Remove Files and Directories

Examples:

```bash
# Remove a file
rm file.txt

# Remove a directory and its contents recursively
rm -r directory_name/

# Force remove a file (without prompting)
rm -f file.txt
```

## mkdir — Create Directories

Examples:

```bash
# Create a single directory
mkdir new_directory

# Create nested directories
mkdir -p parent_directory/child_directory/grandchild_directory
```

## rmdir — Remove Empty Directories

Examples:

```bash
# Remove an empty directory
rmdir empty_directory

# Remove multiple empty directories
rmdir dir1 dir2 dir3
```