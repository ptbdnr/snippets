import json
import os
from pathlib import Path

import dotenv
from mistralai import Mistral, OCRResponse

dotenv.load_dotenv(".env.local")

API_KEY = os.environ["MISTRAL_API_KEY"]
MODEL_NAME = "mistral-ocr-latest"
IMAGE_FILAPATH = "./path/to/file.pdf"
OUTPUT_FILEPATH = "./path/to/file.txt"

if __name__ == "__main__":

    mistral_client = Mistral(api_key=API_KEY)
    with Path(IMAGE_FILAPATH).open("rb") as img_fp:
        uploaded_pdf = mistral_client.files.upload(
            file={
                "file_name": "uploaded_file.pdf",
                "content": img_fp,
            },
            purpose="ocr",
        )

    print(mistral_client.files.retrieve(file_id=uploaded_pdf.id))
    signed_url = mistral_client.files.get_signed_url(file_id=uploaded_pdf.id)

    ocr_response: OCRResponse = mistral_client.ocr.process(
        model=MODEL_NAME,
        document={
            "type": "document_url",
            "document_url": signed_url.url,
        },
    )

    with Path(OUTPUT_FILEPATH).open("w") as response_file:
        response_file.write(json.dumps(ocr_response.model_dump(), indent=2))
    print(ocr_response)
