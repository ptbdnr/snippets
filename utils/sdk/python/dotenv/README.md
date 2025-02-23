## Getting Started

### Copy the environment variables to the project root (next to .gitignore)

source: <tbc>

create a symbolic link
```bash
ln -s .env.local path_to_project/.env.local
```

### Change directory to correct folder and evaluate dependencies

```shell
cd path_to_project
(ls .env.local && echo 'INFO: Found .env.local') || echo 'CRITICAL: Missing .env.local'
(ls requirements.txt && echo 'INFO: Found requirements.txt') || echo 'CRITICAL: Missing requirements.txt'
```

### Create Python environment and install dependencies

```shell
python -m venv .venv  
source .venv/bin/activate
pip3 install -r requirements.txt
```

### Run Python script to start project

```shell
python path_to/filename.py
```
