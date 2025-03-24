import json
import logging
import os
from pathlib import Path

import dotenv
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.core.credentials import AzureKeyCredential


# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
log_handler = logging.StreamHandler()
log_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(log_handler)

dotenv.load_dotenv(".env.local")

OCR_ENDPOINT = os.getenv("AZURE_OCR_DOCUMENT_INTELLIGENCE_ENDPOINT", "")
OCR_KEY = os.getenv("AZURE_OCR_DOCUMENT_INTELLIGENCE_KEY", "")
PATH_TO_DIR = "local_store"
OUTPUT_FILE_JSON = "manuals_ocr.json"

def parse_files(
        path_to_dir: str,
        ocr_client: DocumentIntelligenceClient,
) -> dict:
    """Parse PDF files in a directory and return a list of items."""
    processed_files = {}
    pdf_files = [f for f in Path(path_to_dir).iterdir() if f.name.lower().endswith(".pdf")]
    logger.info("pdf_files: %s", pdf_files)
    for filepath in pdf_files:
        logger.info("filepath: %s", filepath)

        with Path(filepath).open("rb") as f:
            # load pdf file
            poller = ocr_client.begin_analyze_document(
                model_id="prebuilt-layout",
                body=f,
            )
            result: AnalyzeResult = poller.result()
            if result.styles and any(style.is_handwritten for style in result.styles):
                logger.debug("Document contains handwritten content")
            else:
                logger.debug("Document does not contain handwritten content")
            processed_files[filepath.name] = result

    return processed_files


# Initialize the OCR client
ocr_client = DocumentIntelligenceClient(
    endpoint=OCR_ENDPOINT,
    credential=AzureKeyCredential(OCR_KEY),
)

# Parse files
processed_files = parse_files(
    path_to_dir=PATH_TO_DIR,
    ocr_client=ocr_client,
)

# Export
with Path(f"{PATH_TO_DIR}/{OUTPUT_FILE_JSON}").open("w") as f:
    for filepath, parsed_content in processed_files.items():
        logger.debug("File: %s", filepath)
        for page in parsed_content.pages:
            logger.debug("----Analyzing layout from page #%s----", page.page_number)
            logger.debug(
                "Page has width: %d and height: %d, measured with unit: %s",
                float(page.width), float(page.height), str(page.unit),
            )

            if page.selection_marks:
                logger.debug("----Extracted selection marks from document----")
                for selection_mark in page.selection_marks:
                    if selection_mark:
                        logger.debug("Selection mark is found at %s", selection_mark.state)
                        # json.dump({"selection_mark": selection_mark.state}, f)

            if page.lines:
                logger.debug("----Extracted lines from document----")
                for line in page.lines:
                    if line:
                        logger.debug("Line: '%s'", line.content)
                        # json.dump(line.content, f)

        if parsed_content.paragraphs:
            print("----Extracted paragraphs from document----")
            for paragraph in parsed_content.paragraphs:
                if paragraph:
                    logger.debug("Paragraph: '%s'", paragraph.content)
                    json.dump(paragraph.content, f)

        if parsed_content.tables:
            logger.debug("----Extracted tables from document----")
            for table in parsed_content.tables:
                for cell in table.cells:
                    logger.debug("Cell[%d][%d]: %s", cell.row_index, cell.column_index, cell.content)

        if parsed_content.key_value_pairs:
            logger.debug("----Key-value pairs found in document----")
            for kv_pair in parsed_content.key_value_pairs:
                if kv_pair:
                    msg = f"Key: '{kv_pair.key.content}' has value: '{kv_pair.value.content}'"
                    logger.debug(msg=msg)
