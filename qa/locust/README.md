# Developer Guider

### Change directory to correct folder and evaluate dependencies
```shell
(ls requirements.txt && echo 'INFO: Found requirements.txt') || echo 'CRITICAL: Missing requirements.txt'
```

### Create Python environment and install dependencies
```shell
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

### Run loadtests

Run all tests in the tests directory (expects access to a local mongodb connection)
```shell
locust
```

and navigate to `http://0.0.0.0:8089`
