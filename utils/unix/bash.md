# Bash Shell

[GNU Bash Special Parameters](https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html#Special-Parameters)

## Variable

Create a new text file (`file.yaml`) using the following command:

```bash
cat << EOF > path/to/file.yaml
parameter:
    - value1
    - value2
EOF
```

Create a new script file (`foo.sh`) using the following command:

```bash
# Create foo.sh file
touch foo.sh
```

Add the following content to `foo.sh`:

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

Create or update `foo.sh` with the following content to demonstrate parameter usage:

```bash
#!/bin/bash
echo $1
echo "This is a char param: $2"
echo "This is a text param: $3"
echo "This is all params: $@"
```

Invoke the script using:

```bash
./foo.sh 10 a hello
```

## If Statement and Default Value for User Input

The following example demonstrates how to use an if statement to check user input and apply a default value if no input is provided:

```bash
#!/bin/bash
# Prompt user for input with a hint of the default value
read -p "Enter your name (default: User): " name

# Use a default value if no input is provided
name=${name:-User}

# If statement to check if the default is used
if [ "$name" = "User" ]; then
    echo "No input provided, using default value: $name"
else
    echo "Hello, $name"
fi
```

Run the script and test with and without providing input.

## Loop and Default Value for User Input

```bash
PAYTHON_PATH=$(which python)
for i in {1..15}; do
  echo "Sending request $i..."
  sleep 2
done
```

path/to/

### Using a for Loop (word-by-word)

```bash
# Read file content into a variable (this splits into words)
# IFS = internal field separator
# NB: zsh handles word splitting differently than bash
cat << EOF > file.txt
lineA
lineB
lineC
EOF

LINES=$(cat file.txt)
IFS=$'\n'
for line in $LINES; do
    echo ".. $line .."
done
unset IFS
```

### Using a while Loop (line-by-line)

```bash
# This approach preserves each full line
cat << EOF > file.txt
line1
line2
line3
EOF

while IFS= read -r line; do
  echo ".. $line .."
done < file.txt
```