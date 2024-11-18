import os

import dotenv

from datasets import load_dataset

from langchain_openai.chat_models import AzureChatOpenAI
from langchain_openai.embeddings import AzureOpenAIEmbeddings

from ragas.run_config import RunConfig
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas import (
    EvaluationDataset,
    evaluate
)
from ragas.metrics import (
    LLMContextRecall, 
    Faithfulness, 
    FactualCorrectness, 
    SemanticSimilarity
)

dotenv.load_dotenv()


# Initiate LLM and Embeddings clients
llm = AzureChatOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_deployment=os.environ["AZURE_OPENAI_LLM_DEPLOYMENT_NAME"],
    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)

embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_deployment=os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"],
    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)


# Configure ragas
run_config = RunConfig(max_workers=1, timeout=3600)
ragas_llm = LangchainLLMWrapper(llm)
ragas_embeddings = LangchainEmbeddingsWrapper(embeddings)


# Load data
hf_dataset = load_dataset("explodinggradients/amnesty_qa", "english_v3")
ragas_dataset = EvaluationDataset.from_hf_dataset(hf_dataset["eval"])

# Evaluate
results = evaluate(
    dataset=ragas_dataset, 
    metrics=[
        SemanticSimilarity(embeddings=ragas_embeddings),
        LLMContextRecall(llm=ragas_llm), 
        FactualCorrectness(llm=ragas_llm), 
        Faithfulness(llm=ragas_llm),
    ], 
    run_config=run_config
)
