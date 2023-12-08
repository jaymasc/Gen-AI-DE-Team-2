import os
from backend.db_ops import * 
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import *
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.llms import OpenAI

load_dotenv()
db = SQLDatabase.from_uri("sqlite:///starfleet.sqlite")

chatbot = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY"], model='gpt-3.5-turbo', temperature=0)

embedding_generator = OpenAIEmbeddings(api_key=os.environ["OPENAI_API_KEY"], model="text-embedding-ada-002")

def generate_response(user_input, session_id):

# Prompt    
    template = """You are a chatbot specialized in generating SQL queries from user inputs. 
                        You understand database schemas and can generate SQL queries based on the provided information.
                        If the user provides details of a database schema or tables with fields, use this information to create a SQL query based on the user's question.
                        If no database or table details are given, ask the user to provide this information.
                        Additionally, if the user requests a query that does not match the provided schema or tables, warn them and request a query related to the provided information.
                        
                        Current conversation:
                        {chat_history}
                        Human: {query}
                        AI:"""
                        
    prompt = PromptTemplate(input_variables=["query", "chat_history"],template=template)

    #Getting chat_history_obj for session from Redis
    redis_history = get_chat_history_obj(session_id)
    # Memory setup
    memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=redis_history )
    # Create the conversation chain 
    # chat_chain = SQLDatabaseChain.from_llm(llm=chatbot, db=db, prompt=prompt, verbose=True, memory=memory, top_k=1000)
    chat_chain = SQLDatabaseChain.from_llm(llm=chatbot, db=db, verbose=True, memory=memory, top_k=1000)
    
    # After getting response
    response = chat_chain.run(query=user_input)

    return response
