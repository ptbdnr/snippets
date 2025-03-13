# System Monitoring Command Examples

## top
`top` is used to display and update sorted information about system processes. Examples:

```bash
# Open top to monitor system processes in real-time
top

# In top, press 'q' to exit
```

## ps
`ps` displays information about active processes. Examples:

```bash
# Display processes for the current shell
ps

# Display a full-format listing of all processes
ps -ef

# Display processes in a user-defined format (e.g., user, PID, and command)
ps -eo user,pid,cmd
```

## df
`df` reports file system disk space usage. Examples:

```bash
# Display disk space usage in blocks for all mounted filesystems
df

# Display disk space usage in a human-readable format (e.g., MB or GB)
df -h

# Display inode information instead of block usage
df -i
``` 

## htop
`htop` is an enhanced, interactive process viewer. Examples:

```bash
# Launch htop to monitor system processes with a colorized interface
htop

# In htop, use F10 or 'q' to quit the application
```

## vtop
`vtop` provides a visually engaging overview of system metrics. Examples:

```bash
# Launch vtop to display graphical resource usage
vtop

# Exit vtop by pressing 'q'
```