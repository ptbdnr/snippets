# Bash Shell

[GNU Bash Special Parameters](https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html#Special-Parameters)

## Variable

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
