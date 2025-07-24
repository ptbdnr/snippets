# azure-core==1.35.0
# azure-ai-documentintelligence==1.0.0b4
import json
import os
import logging
from pathlib import Path
from typing_extensions import Literal

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient, AnalyzeDocumentLROPoller
from azure.ai.documentintelligence.models import AnalyzeResult

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

ENDPOINT="https://*******.cognitiveservices.azure.com"
API_KEY="*****************"

class DocIntelligenceExtractor:
    """Client for Document Intelligence API"""
    client: DocumentIntelligenceClient

    def __init__(
            self,
            endpoint: str | None = None, 
            credential: AzureKeyCredential | None = None,
            api_version: str = "2024-11-30",
            logger: logging.Logger = logger,
        ) -> None:
        """Initialize the Document Intelligence client"""
        # Initialize the client
        self.client = DocumentIntelligenceClient(
            endpoint=endpoint,
            credential=credential,
            api_version=api_version,
        )

    def extract_from_docx(
            self, 
            docx_path: str, 
            model_id: Literal["prebuilt-read", "prebuilt-layout"] = "prebuilt-read",
            result_filepath: str | None = None
        ) -> str:
        """Extract text from a DOCX file using the specified model_id"""
        try:
            with Path(docx_path).open("rb") as docx_file:
                # Read the DOCX file content
                docx_bytes = docx_file.read()
                
                # Create the AnalyzeDocumentRequest
                poller : AnalyzeDocumentLROPoller = self.client.begin_analyze_document(
                    model_id=model_id,
                    analyze_request=docx_bytes,
                    content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
                logger.debug(f"Poller status: {poller.status()}")

                # Wait for the analysis to complete
                result: AnalyzeResult = poller.result()

                # Optionally save the poller state
                if result_filepath:
                    with Path(result_filepath).open("w") as rf:
                        result_dict = result.as_dict()
                        json.dump(result_dict, rf, indent=2)

                match model_id:
                    case "prebuilt-read":
                        extracted_content = ""
                        for paragraph in result.paragraphs:
                            extracted_content += paragraph.content + "\n"
                        return extracted_content.strip()
                    case "prebuilt-layout":
                        extracted_content = ""
                        for page in result.pages:
                            logger.info(f"Processing page {page.page_number} with {len(page.words)} words")
                            for word in page.words:
                                extracted_content += word.content + " "
                        for paragraph_idx, paragraph in enumerate(result.paragraphs):
                            logger.info(f"Processing paragraph {paragraph_idx}")
                            extracted_content += paragraph.content + "\n"
                        for table_idx, table in enumerate(result.tables):
                            logger.info(f"Processing table {table_idx} with {len(table.cells)} cells")
                            for cell in table.cells:
                                extracted_content += cell.content + "\n"
                        return extracted_content.strip()
                    case _:
                        logger.error(f"Unsupported model_id: {model_id}")
                        return ""
        except Exception as e:
            msg = f"Failed to extract text from {docx_path} using model_id {model_id}: {e}"
            logger.exception(msg)
            raise e

if __name__ == "__main__":
    
    # Initialize the Document Intelligence client
    doc_intelligence_extractor = DocIntelligenceExtractor(
        endpoint=ENDPOINT,
        credential=AzureKeyCredential(API_KEY)
    )
    
    # Example usage
    path_to_file = "./sample.docx"    
    for model_id in ["prebuilt-read", "prebuilt-layout"]:
        logger.info(f"Extracting with model_id: {model_id}")
        # Extract text from the DOCX file
        extracted_content = doc_intelligence_extractor.extract_from_docx(
            docx_path=path_to_file, 
            model_id=model_id,
            result_filepath=f"./result_{model_id}.json"
        )
        json.dump(extracted_content, open(f"./content_{model_id}.txt", "w"), indent=2)
