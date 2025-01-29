# SGLang

## Install
ref. https://docs.sglang.ai/start/install.html

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
pip install --upgrade pip
pip install sgl-kernel --force-reinstall --no-deps
pip install "sglang[all]" --find-links https://flashinfer.ai/whl/cu124/torch2.4/flashinfer/
```

SGLang deployment fetches the model weights from Hugging Face.
No need to add token to github config.
You might also load model from local storage.

```bash
pip install --upgrade huggingface_hub
huggingface-cli login
```

## Launch a Server
https://docs.sglang.ai/start/send_request.html#Launch-A-Server

Example supported models: https://docs.sglang.ai/references/supported_models.html

* LLaMa 3
* DeepSeek
* Qwen 2 VL
* Mixtral Nemo

Create a virtual environment (if not already done) and activate it
```bash
mkdir workspace
cd workspace
python3 -m venv .venv
source .venv/bin/activate
```

Start serving the model, binding to port 30000 on all interfaces (0.0.0.0)
```bash
export MODEL_PATH=meta-llama/Meta-Llama-3.1-8B-Instruct
python -m sglang.launch_server --model-path $MODEL_PATH --port 30000 --host 0.0.0.0
```

### Connect remotely

(This might not work behind firewall.)

Open the Azure portal and navigate to the VM
Select Networking
Select Network Settings
Add inbound port rule

* protocol: any (default)
* source: any (default)
* destination: any (default)
* post: 30000
* name: sglang

Test connection from local machine
```bash
nc -zv <$VM_IP_ADDRESS> 30000
```
expected output: Connection to <$VM_IP_ADDRESS> 30000 port [tcp/*] succeeded!

Send a request to generate text
```bash
curl -s http://<$VM_IP_ADDRESS>:30000/v1/chat/completions \
  -d '{
    "model": "meta-llama/Meta-Llama-3.1-8B-Instruct", 
    "messages": [{"role": "user", "content": "What is the capital of France?"}]
    }'
```


## Offline inferece

```bash
touch offline_inference.py
```

insert in offline_inference.py

```python
# launch the offline engine
from sglang.utils import stream_and_merge, async_stream_and_merge
import sglang as sgl
import asyncio

llm = sgl.Engine(model_path="meta-llama/Meta-Llama-3.1-8B-Instruct")

prompts = [
    "Hello, my name is",
    "The president of the United States is",
    "The capital of France is",
    "The future of AI is",
]

sampling_params = {"temperature": 0.8, "top_p": 0.95}

outputs = llm.generate(prompts, sampling_params)

# Print the outputs.
for prompt, output in zip(prompts, outputs):
    print(f"Prompt: {prompt}\nGenerated text: {output['text']}")
```

Run code
```bash
python offline_inference.py
```