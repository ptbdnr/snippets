# Process Management Command Examples

## Identify Process on a Port
To find out which process is using a specific port, you can use:

```bash
# Using lsof to identify the process listening on port 8080
sudo lsof -i :8080

# Alternatively, using netstat to display processes using port 8080
sudo netstat -tulpn | grep :8080

# On some systems, you can also use fuser
sudo fuser 8080/tcp
```

## kill
`kill` is used to send signals to a process, most commonly to terminate it.

```bash
# Terminate a process by its Process ID (PID)
kill 1234

# Forcefully terminate a process with signal 9 (SIGKILL)
kill -9 1234
```

## killall
`killall` sends a signal to all processes matching a given name.

```bash
# Terminate all processes with the name "processName"
killall processName

# Forcefully terminate all processes with the name "processName"
killall -9 processName
```

## bg
`bg` resumes a suspended job and runs it in the background.

```bash
# Move the most recent job to the background
bg

# Move a specific suspended job (e.g., job number 1) to the background
bg %1
```

## ps
`ps` displays information about currently running processes.

```bash
# Display processes associated with the current terminal session
ps

# Display all processes with detailed information
ps -ef

# Display processes with a user-defined format (e.g., user, PID, and command)
ps -eo user,pid,cmd
```
