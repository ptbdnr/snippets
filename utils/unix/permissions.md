# Permissions and Ownership Command Examples

## chmod
`chmod` is used to change the file mode (permissions) of a file or directory. Examples:

```bash
# Set read, write, and execute permissions for the owner; read and execute for group and others
chmod 755 filename

# Add execute permission for the user (owner) only
chmod u+x filename

# Recursively set permissions for all files in a directory
chmod -R 644 directory/
```

## chown
`chown` changes the owner and/or group of a file or directory. Examples:

```bash
# Change the owner of a file to 'username'
chown username filename

# Change both the owner and the group of a file
chown username:groupname filename

# Recursively change owner and group for all items in a directory
chown -R username:groupname directory/
```

## chgrp
`chgrp` changes the group ownership of a file or directory. Examples:

```bash
# Change the group of a file to 'groupname'
chgrp groupname filename

# Recursively change the group for all items in a directory
chgrp -R groupname directory/
```