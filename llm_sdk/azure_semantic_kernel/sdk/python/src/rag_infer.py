import os
import asyncio

import dotenv

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.memory.chroma import ChromaMemoryStore
from semantic_kernel.core_plugins.text_memory_plugin import TextMemoryPlugin
from semantic_kernel.memory.semantic_text_memory import SemanticTextMemory
from semantic_kernel.prompt_template import PromptTemplateConfig
from semantic_kernel.functions import KernelArguments
from semantic_kernel.connectors.ai.prompt_execution_settings import (
    PromptExecutionSettings
)

from mockup_embedding import MockupEmbedding

dotenv.load_dotenv()


# constants
CHROMA_PESIST_DIR_PATH = "./chroma_cache"
CHROMA_COLLECTION_NAME = "<ADD_COLLECTION_NAME>"


kernel = Kernel()  # Initialize the kernel

llm_service_id = 'chat-gpt'
llm = AzureChatCompletion(
    service_id=llm_service_id,
    # base_url=os.environ["AZURE_OPENAI_ENDPOINT"],  # bug
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    deployment_name=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)
kernel.add_service(llm)

prompt_execution_settings = kernel.\
    get_prompt_execution_settings_from_service_id(llm_service_id)

embedding_service_id = 'embedding_gen'
embedding_gen = MockupEmbedding(service_id=embedding_service_id)
kernel.add_service(embedding_gen)

vectorstore = ChromaMemoryStore(persist_directory=CHROMA_PESIST_DIR_PATH)
memory = SemanticTextMemory(
    storage=vectorstore,
    embeddings_generator=embedding_gen
)
memory_plugin = TextMemoryPlugin(memory)
kernel.add_plugin(memory_plugin, "memory_plugin")


async def main(
    kernel: Kernel,
    memory: SemanticTextMemory,
    memory_plugin: TextMemoryPlugin,
    prompt_execution_settings: PromptExecutionSettings
) -> None:

    # Query and retrieve data
    results = await memory.search(
        collection=CHROMA_COLLECTION_NAME,
        query="What is farthest space object from here?",
        limit=999,
        with_embeddings=True
    )
    print('=' * 16 + '\n' + 'MEMORY OUTPUT')
    print([(mem_query_result.text, mem_query_result.embedding[:5])
           for mem_query_result in results])

    results = await memory_plugin.recall(
        ask="farthest space object",
        collection=CHROMA_COLLECTION_NAME,
        limit=999)
    print('=' * 16 + '\n' + 'MEMORY PLUGIN OUTPUT')
    print(results)

    # Generate response
    prompt_template_config = PromptTemplateConfig(
        template="""
            {{memory_plugin.recall 'farthest space object'}} {{$request}}
        """.strip(),
        execution_settings=prompt_execution_settings
    )
    rag_func = kernel.add_function(
        function_name="rag_function",
        plugin_name="rag_plugin",
        prompt_template_config=prompt_template_config,
    )
    result = await kernel.invoke(
        function=rag_func,
        arguments=KernelArguments(
            request="What is farthest space object from here?",
            collection=CHROMA_COLLECTION_NAME
        )
    )
    print('=' * 16 + '\n' + 'LLM OUTPUT')
    print(str(result))


# Run the main function
if __name__ == "__main__":
    asyncio.run(main(
        kernel=kernel,
        memory=memory,
        memory_plugin=memory_plugin,
        prompt_execution_settings=prompt_execution_settings
    ))
