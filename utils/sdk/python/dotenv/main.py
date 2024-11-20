import os
import dotenv

env_name = "sample_env_file.env"

# Find the .env file
print(dotenv.find_dotenv())

# Load the .env file to a dictionary
config = dotenv.dotenv_values(env_name)
print(config.get('SECRET'))

# Load the .env file to OS environment
dotenv.load_dotenv(env_name)
print(os.environ.get('SECRET'))

# Get the value of a key from the .env file
print(dotenv.get_key(env_name, 'SECRET'))
