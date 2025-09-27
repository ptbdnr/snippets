from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI

AZURE_LLM_ENDPOINT: str = 'foo'
AZURE_LLM_API_KEY: str = 'bar'
AZURE_LLM_API_VERSION: str = '2025-03-01-preview'
AZURE_LLM_DEPLOYMENT_NAME: str = 'gpt-5'


def get_llm_client(use_identity: bool = True) -> AzureOpenAI:
    """Initialise the client."""
    if use_identity:
        # Auth: running in Azure host; using DefaultAzureCredential without interactive sources.
        # alternative to narrow it down to AzureDeveloperCliCredential only
        credential = DefaultAzureCredential(
            exclude_cli_credential=False, # allow CLI auth
            exclude_managed_identity_credential=False, # allow MSI auth

            exclude_interactive_browser_credential=True,
            exclude_visual_studio_code_credential=True,
            exclude_shared_token_cache_credential=True,
            exclude_environment_credential=True,
            exclude_powershell_credential=True,
            exclude_developer_cli_credential=True,
        )
        token_provider = get_bearer_token_provider(
             credential,
             "https://cognitiveservices.azure.com/.default",
        )
        return AzureOpenAI(
            azure_endpoint=AZURE_LLM_ENDPOINT,
            azure_ad_token_provider=token_provider,
            api_version=AZURE_LLM_API_VERSION,
        )

    return AzureOpenAI(
        azure_endpoint=AZURE_LLM_ENDPOINT,
        api_key=AZURE_LLM_API_KEY,
        api_version=AZURE_LLM_API_VERSION,
    )

client = get_llm_client()
completion = client.chat.completions.create(
    messages=[{"role": "user", "content": "1+1=?"}],
    model=AZURE_LLM_DEPLOYMENT_NAME,
    temperature=0.0,
)
