# langchain==0.3.7
# langchain-community==0.3.7
# pypdf==5.1.0
# docx2txt==0.8
# unstructured==0.16.5
# python-pptx==1.0.2
# azure-ai-formrecognizer==3.3.3

# from azure.ai.formrecognizer import DocumentAnalysisClient
# from azure.core.credentials import AzureKeyCredential

from langchain.document_loaders import (
  DirectoryLoader,
  PyPDFLoader,
  CSVLoader,
  Docx2txtLoader,
  TextLoader,
  UnstructuredExcelLoader,
  UnstructuredHTMLLoader,
  UnstructuredPowerPointLoader,
  UnstructuredMarkdownLoader,
  JSONLoader,
#   DocumentIntelligenceLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter 

# constants
directory = '/PATH/TO/FILES'

file_type_mappings = {
    '*.txt': [TextLoader],
    '*.pdf': [PyPDFLoader],  # + DocumentIntelligenceLoader
    '*.csv': [CSVLoader],
    '*.docx': [Docx2txtLoader],
    '*.xlss': [UnstructuredExcelLoader],
    '*.xlsx': [UnstructuredExcelLoader],
    '*.html': [UnstructuredHTMLLoader],
    '*.pptx': [UnstructuredPowerPointLoader],  # + DocumentIntelligenceLoader
    '*.ppt': [UnstructuredPowerPointLoader],  # + DocumentIntelligenceLoader
    '*.md': [UnstructuredMarkdownLoader],
    '*.json': [JSONLoader],
}

# docintel_client = DocumentAnalysisClient(
#   endpoint='https://pbhack.cognitiveservices.azure.com/', 
#   credential=AzureKeyCredential('7TXIGdso9twGT8R0wSTZ39U1CKIZh4qLyOHFV1bhJd3yFGgom3maJQQJ99AKACYeBjFXJ3w3AAALACOGVihF')
# )

# iterate over the file type mappings
for glob_pattern, [list_of_loader_cls] in file_type_mappings.items():
    docs = []
    loaded = False

    # iterate over the loader classes
    for loader_cls in list_of_loader_cls:
        try:        
            loader_kwargs = None
            
            if loader_cls == JSONLoader:
                loader_kwargs = {'jq_schema': '.', 'text_content': False}
            
            # elif loader_cls == DocumentIntelligenceLoader:
            #     loader_kwargs = {'client': docintel_client, 'model': 'prebuilt-document'}

            # load the documents with given pattern/extension
            loader_dir = DirectoryLoader(
                path=directory, 
                glob=glob_pattern, 
                loader_cls=loader_cls, 
                loader_kwargs=loader_kwargs
            )
            documents = loader_dir.load_and_split()
            
            # chunking strategy
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=800, 
                chunk_overlap=200
            )
            # for different glob pattern it will split and add texts
            docs += text_splitter.split_documents(documents)
            loaded = True
        except Exception as e:
            print(e)
        
        if loaded:
            break

    print(docs)