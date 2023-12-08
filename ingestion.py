import os

from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
import pinecone

from dotenv import load_dotenv, find_dotenv
_= load_dotenv()

pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENVIRONMENT_REGION"],
)
INDEX_NAME = "test-index"


def ingest_docs(path: str):
    loader = DirectoryLoader(path=path, loader_cls=TextLoader)
    raw_documents = loader.load()
    print(f"loaded {len(raw_documents)} documents")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400, chunk_overlap=50, separators=["\n\n", "\n", " ", ""]
    )
    documents = text_splitter.split_documents(raw_documents)
    for doc in documents:
        print(doc)

    embeddings = OpenAIEmbeddings()
    print(f"Going to add {len(documents)} to Pinecone")
    Pinecone.from_documents(documents, embeddings, index_name=INDEX_NAME)
    print("****Loading to vectorestore done ***")

def remove_all_pinecone_records():
    index = pinecone.Index(INDEX_NAME)
    index_description = index.describe_index_stats()
    print(f"Pinecone index before cleanup: {index_description}")
    
    # Note that there will be a delay of several minutes before the Pinecone index is empty
    index.delete(delete_all=True)   
    
    
if __name__ == "__main__":
    ingest_docs("knowledge/policies")
