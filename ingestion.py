import os
import sys
import logging
import time
from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
import pinecone
from dotenv import load_dotenv

# Set up logging and environment variables
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
load_dotenv()

# Initialize Pinecone vector store
pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENVIRONMENT_REGION"],
)
logging.info('Pinecone initialized')

# Named index for the Pinecone vector store
INDEX_NAME = "test-index"

def ingest_docs(path: str):
    logging.info('Starting document ingestion')
    start_time = time.time()
    loader = DirectoryLoader(path=path, loader_cls=TextLoader)
    raw_documents = loader.load()
    logging.info(f"Loaded {len(raw_documents)} documents")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400, chunk_overlap=50, separators=["\\n\\n", "\\n", " ", ""]
    )
    documents = text_splitter.split_documents(raw_documents)
    embeddings = OpenAIEmbeddings()
    Pinecone.from_documents(documents, embeddings, index_name=INDEX_NAME)
    elapsed_time = time.time() - start_time
    logging.info(f"Document ingestion completed in {elapsed_time:.2f} seconds")

def remove_all_pinecone_records():
    logging.info('Starting removal of all documents from Pinecone')
    start_time = time.time()
    index = pinecone.Index(INDEX_NAME)
    index.delete(delete_all=True)
    elapsed_time = time.time() - start_time
    logging.info(f"All documents removed from Pinecone in {elapsed_time:.2f} seconds")

def setup():
    logging.info('Running setup function')
    ingest_docs("knowledge/policies")

def reset():
    logging.info('Running reset function')
    remove_all_pinecone_records()

def usage():
    logging.info('Displaying usage instructions')
    print("Usage:")
    print("    ingestion setup // to populate Pinecone with policy documents")
    print("    ingestion reset // to delete all records from Pinecone")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        function_name = sys.argv[1]
        if function_name == "setup":
            setup()
        elif function_name == "reset":
            reset()
        else:
            usage()
    else:
        usage()
