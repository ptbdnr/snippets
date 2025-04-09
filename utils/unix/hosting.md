# Hosting

## lsof
`lsof` lists the processes (with PID) running on a host
  
```bash
# lists processes exposing post $PORT_NUMBER
lsof -i :$PORT_NUMBER

```

```bash
# teminate a process with id $PID
kill -9 $PID
```

