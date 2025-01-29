# vLLM

## Install
ref. https://docs.vllm.ai/en/latest/getting_started/installation.html

```bash
sudo apt install python3-pip
sudo apt install python3-venv
python3 --version
pip3 --version

```

```bash
mkdir workspace
cd workspace
python3 -m venv .venv
source .venv/bin/activate
```

```bash
pip install vllm
```

## Launch a Server
ref. https://docs.vllm.ai/en/latest/models/supported_models.html

Example model_tags:

* facebook/opt-125m
* GPT2
* Qwen
* Qwen2
* Nemotron
* LLaMa 2: meta-llama/Llama-2-70b-hf # requires Huggingface token
* LLaMa 3: meta-llama/Meta-Llama-3.1-70B  # requires Huggingface token
* Mixtral: mistralai/Mixtral-8x7B-v0.1 # requires Huggingface token
* microsoft/Phi-3.5-MoE-instruct # fails, requires --trust_remote_code
* google/gemma-2b (completion only)
* google/gemma-2b-it (instruction tuned, e.g. chat)


Create a virtual environment (if not already done) and activate it
```bash
mkdir workspace
cd workspace
python3 -m venv .venv
source .venv/bin/activate
```

Start serving the model, binding to port 23456 on all interfaces (0.0.0.0)
[optional] configure GPU_COUNT (default = 1)
[optional] configure data type, e.g. --dtype=half
```bash
vllm serve $MODEL_TAG --port $PORT --tensor-parallel-size $GPU_COUNT
```

example:
1. vllm serve facebook/opt-125m --port 23456 --tensor-parallel-size 2
2. (not tested) vllm serve microsoft/Phi-3.5-MoE-instruct --port 23456 --trust_remote_code --tensor-parallel-size 2

alternatively try with $MAX_GPU_MEM_UTIL = 0.8
```bash
python3 -m vllm.entrypoints.openai.api_server --model $MODEL_TAG --gpu-memory-utilization $MAX_GPU_MEM_UTIL
```
example:
1. python3 -m vllm.entrypoints.openai.api_server --model microsoft/Phi-3.5-MoE-instruct --port 23456 --trust_remote_code --tensor-parallel-size 2

## Connect remotely

(This might not work behind firewall.)

Open the Azure portal and navigate to the VM
Select Networking
Select Network Settings
Add inbound port rule

* protocol: any (default)
* source: any (default)
* destination: any (default)
* post: 23456
* name: vllm

Test connection from local machine
```bash
nc -zv <$VM_IP_ADDRESS> 23456
```
expected output: Connection to <$VM_IP_ADDRESS> 23456 port [tcp/*] succeeded!

List models
```bash
alias prettyjson='python3 -m json.tool'
curl http://<$VM_IP_ADDRESS>:23456/v1/models | | prettyjson
```
example: curl http://51.12.52.76:23456/v1/models | python3 -m json.tool


Send a request to generate text
```bash
curl http://<$VM_IP_ADDRESS>:23456/v1/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "facebook/opt-125m",
        "prompt": "San Francisco is a"
        "max_tokens": 3000
    }'
```
example:
1. curl -X POST http://51.12.52.76:23456/v1/completions -H "Content-Type: application/json" -d '{"model": "facebook/opt-125m", "prompt":"Fibonacci sequence is:"}'
2. curl -X POST http://51.12.52.76:23456/v1/completions -H "Content-Type: application/json" -d '{"model": "microsoft/Phi-3.5-MoE-instruct", "prompt":"San Francisco is a"}'

```bash
curl http://<$VM_IP_ADDRESS>:23456/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "facebook/opt-125m",
        "messages": [{"role": "user", "content": "Fibonacci sequence in Python"}]
    }'
```
example:
1. curl http://51.12.52.76:23456/v1/chat/completions -H "Content-Type: application/json" -d '{"model": "microsoft/Phi-3.5-MoE-instruct", "messages": [{"role": "user", "content": "Fibonacci sequence in Python"}]}'



## Offline inferece

```bash
touch offline_inference.py
```

insert in offline_inference.py

```python
# launch the offline engine
from vllm import LLM, SamplingParams

llm = LLM(model="facebook/opt-125m")

prompts = [
    "Hello, my name is",
    "The president of the United States is",
    "The capital of France is",
    "The future of AI is",
]
sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

outputs = llm.generate(prompts, sampling_params)

# Print the outputs.
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
```

Run code
```bash
python offline_inference.py
```
