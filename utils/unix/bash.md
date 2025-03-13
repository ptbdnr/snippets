# Bash Shell

https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html#Special-Parameters

## Variable
create foo.sh 
```bash
touch foo.sh
```

add content:
```bash
#!/bin/bash
numberVar=10
echo $numberVar

charVar='a'
echo "This is a charVar: $charVar"

textVar="hello"
echo "This is a textVar: $textVar"
```
## Parameters
create foo.sh with following content:

```bash
#!/bin/bash
echo $1
echo "This is a char param: $2"
echo "This is a text param: $3"
echo "This is all params: $@"
```

invoke `./foo.sh 10 a hello`
