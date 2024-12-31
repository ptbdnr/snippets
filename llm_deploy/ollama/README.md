# Ollama: Install
ref.

install Ollama on Linux
```bash
sudo curl -fsSL https://ollama.com/install.sh | sh
```

# Ollama: Serve model
ref. https://ollama.com/library

Llama CodeLlama 7/13/34/70B: https://ollama.com/library/codellama
Mistral Codestral 22B: https://ollama.com/library/codestral
DeepSeek Coder v2 16/236B: https://ollama.com/library/deepseek-coder-v2
Qween 2.5 Coder 0.5/1.5/3/7/14/32/72B: https://ollama.com/library/qwen2.5
Llama 3 8/70B: https://ollama.com/library/llama3

1. Pull the manifest of a Language Model

```bash
# ollama pull codellama:7b
# ollama pull codestral
ollama pull deepseek-coder-v2:16b
# qwen2.5-coder:latest
# # ollama pull llama3:8b
# ollama pull llama3:70b
```

remove with ```ollama rm codellama:7b```

You can download models from HuggingFace (staus: in preview)
```bash
pip install -U "huggingface-hub[cli]"
huggingface-cli --help
huggingface-cli download \
    <$HG_REPO_ID> <$HG_FILENAME> \
    --local-dir . \
    --local-dir-use-symlinks False
```

Create a confile file called `Modelfile` with the following content
```bash
FROM <$HG_FILENAME>
PARAMETER temperature 0.5
SYSTEM """You are a helpful assistant"""
```

Compile and register your model to Ollama
```bash
ollama create -f <$CUSTOM_MODEL_NAME> Modelfile
```

list the models
```bash
ollama list
```

see files on Linux (blobs contain partitions, manifests contain registry)
```bash
sudo ls -lah /usr/share/ollama/.ollama/models/manifests
sudo ls -lah /usr/share/ollama/.ollama/models/blobs
```

2. Test the language model locally
```bash
# ollama run codellama:7b
# ollama run codestral:22b
ollama run deepseek-coder-v2:16b
# ollama run llama3:8b
# ollama run llama3:70b
```

prompt:
```
fibonacci sequence with python
/bye
```

3. Configure the service on the VM

ref. https://github.com/ollama/ollama/blob/main/docs/faq.md#setting-environment-variables-on-linux

Open service configuration
```bash
sudo systemctl edit ollama.service
```

Add and save
OLLAMA_HOST: IP address
CUDA_VISIBLE_DEVICES: GPU index that can be used by Ollama
OLLAMA_NUM_PARALLEL: number of GPUs that can be used by Ollama
```bash
[Service]
Environment="OLLAMA_HOST=0.0.0.0"
Environment="CUDA_VISIBLE_DEVICES=0,1"
Environment="OLLAMA_NUM_PARALLEL=$GPU_COUNT"
```

If using nano-like editor: save with Ctrl+X, confirm with Y, Enter to exit

Reload configuration and restart the service
```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

This automatically invokes `ollama serve`, which serves web request on the TCP port 11434 by default. You can change it with with the env variable OLLAMA_HOST. For example.: `OLLAMA_HOST=127.0.0.1:8080 ollama serve`

Verify that OLLAMA is listening on the port
```bash
sudo apt install net-tools
netstat -tuln | grep 11434
```

```bash
curl 0.0.0.0:11434
```

Troubleshooting: if not already done, start the Ollama service
```bash
ollama serve
```

stop the service
```bash
sudo service ollama stop
```


# Ollama: Connect remotely

## Via Azure network setting

Open the Azure portal and navigate to the VM
Select Networking
Select Network Settings
Add inbound port rule

* protocol: any (default)
* source: any (default)
* destination: any (default)
* post: 11434
* name: ollama

Test connection from local machine
```bash
nc -zv <$VM_IP_ADDRESS> 11434
```
expected output: Connection to <$VM_IP_ADDRESS> 11434 port [tcp/*] succeeded!

```bash
curl <$VM_IP_ADDRESS>:11434
```
expected output: Ollama is running

List models
```bash
alias prettyjson='python3 -m json.tool'
curl http://<$VM_IP_ADDRESS>:11434/api/tags | prettyjson
```

Send a request to generate code from the local machine
```bash
curl -X POST http://<$VM_IP_ADDRESS>:11434/api/generate -d '{
  "model": "deepseek-coder-v2:16b",
  "prompt":"fibonacci sequence with python"
}'
```
example:
1: curl -X POST http://51.12.52.76:11434/api/generate -d '{"model": "deepseek-coder-v2:16b", "prompt":"fibonacci sequence with python"}'
2. curl -X POST http://51.12.52.76:11434/api/generate -d '{"model": "qwen2.5-coder:latest", "prompt":"fibonacci sequence with python"}'
3: curl -X POST http://51.12.52.76:11434/api/generate -d '{"model": "llama3:70b", "prompt":"write a auper long poem"}'


## Via SSH address binding using `-L local_socket:host:hostport`

We specify that connections to the given TCP port
on the local (client) host are to be forwarded to
the given host and port, on the remote side.
This works by allocating a socket to listen to
a TCP port on the local side.
Whenever a connection is made to the local port or
socket, the connection is forwarded over the secure
channel, and a connection is made to the host port
on the remote machine.

On the local machine invoke
```bash
ssh -L 11434:localhost:11434 <$USERNAME>@<$VM_IP_ADDRESS>
```

Test the tunneled API on the local machine
```bash
curl 0.0.0.0:11434
```
expected output: 'Ollama is running'

List models
```bash
alias prettyjson='python3 -m json.tool'
curl http://0.0.0.0:11434/api/tags | prettyjson
```

Send a request to generate code from the local machine

```bash
curl -X POST http://localhost:11434/api/generate -d '{
  "model": "codellama",
  "prompt":"fibonacci sequence with python"
}'
```
