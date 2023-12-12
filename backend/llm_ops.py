import os
import backend.util as util
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import *
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.callbacks import get_openai_callback
from langchain.utilities import SQLDatabase
from langchain.vectorstores import Pinecone
import pinecone

# Load environment variables from a .env file
load_dotenv()

# Initialize Pinecone with API key and environment settings from .env file
pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENVIRONMENT_REGION"],
)

# Define a constant for the Pinecone index name
INDEX_NAME = "test-index"

# Template for the chatbot interaction. It includes SQL schema and conversation context
TEMPLATE = """You are a chatbot specialized in generating SQL queries from user inputs. 
                You understand database schemas and can generate SQL queries.
                
                Here is the schema for the starfleet academy database:
                {schema}
                ###
                You can answer questions and generate sql for the starfleet academy database.
                You also know about Starfleet policies and you can answer questions about those.  If my question about the policies is vague, you can 
                give me a summary of what's available
                
                You can also help to generate sql for tables that are not in the starfleet database.  Help the user along but be flexible.
                It's OK to work with partial information.  
                
                Previous Conversation:
                {chat_history}
                Current conversation:
                {context}
                Human: {question}
                AI:"""
          
              
# Initialize the ChatOpenAI model with API key and model specifications
chatbot = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY"], model='gpt-3.5-turbo', temperature=0)

# Create a connection to the SQL database and retrieve the schema
db = SQLDatabase.from_uri("sqlite:///starfleet.sqlite")
db_schema = db.get_table_info()

# Function to return the database schema
def get_schema():
    return db_schema

# Function to generate a response based on user input and session ID
def generate_response(user_input, session_id):
    # Initialize Pinecone vector store with the OpenAI embeddings
    docsearch = Pinecone.from_existing_index(
        embedding=OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"]),
        index_name=INDEX_NAME,
    )
        
    # Retrieve chat history from Redis for the current session
    redis_history = util.get_chat_history_obj(session_id)
    
    # Initialize memory for conversation context
    memory = ConversationBufferMemory(
        memory_key="chat_history", 
        chat_memory=redis_history,
        return_messages=True
    )

    # Set up the prompt template with input variables and the chatbot template
    prompt = PromptTemplate(
        input_variables=["question", "context", "chat_history"], 
        partial_variables={"schema": get_schema},
        template=TEMPLATE
    )
    
    # Create a conversational retrieval chain with the chat model, document retriever, and memory
    chain = ConversationalRetrievalChain.from_llm(
        llm=chatbot, 
        retriever=docsearch.as_retriever(), 
        memory=memory,
        combine_docs_chain_kwargs={'prompt': prompt}
    )

    with get_openai_callback() as cb:
        chain({"question": user_input, 'chat_history': redis_history})
        # Populate the log with token and cost details
        log = {
            'Total Tokens': cb.total_tokens, 
            'Prompt Tokens': cb.prompt_tokens,
            'Completion Tokens': cb.completion_tokens,
            'Total Cost(USD)': cb.total_cost
        }          
    # Return the generated response based on the input question and chat history
    return log
   
