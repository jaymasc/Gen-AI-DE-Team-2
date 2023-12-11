import os
import backend.util as util
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import *
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone

load_dotenv()

pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENVIRONMENT_REGION"],
)

INDEX_NAME = "test-index"

chatbot = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY"], model='gpt-3.5-turbo', temperature=0)

def generate_response(user_input, session_id):

# Prompt    
    template = """You are a chatbot specialized in generating SQL queries from user inputs. 
                        You understand database schemas and can generate SQL queries based on the provided information.
                        You also know about Starfleet policies and you can answer questions about those.
                        If the user provides details of a database schema or tables with fields, use this information to create a SQL query based on the user's question.
                        If no database or table details are given, ask the user to provide this information.
                        Additionally, if the user requests a query that does not match the provided schema or tables, warn them and request a query related to the provided information.
                        If the user asks questions that can be answered from the Starfeet policies, provide the answers
                        
                        Previous Conversation:
                        {chat_history}
                        Current conversation:
                        {context}
                        Human: {question}
                        AI:"""

    prompt = PromptTemplate(input_variables=["question", "context", "chat_history"],template=template)

    embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
    docsearch = Pinecone.from_existing_index(
        embedding=embeddings,
        index_name=INDEX_NAME,
    )
    
    #Getting chat_history_obj for session from Redis
    redis_history = util.get_chat_history_obj(session_id)
    
    # Memory setup
    memory = ConversationBufferMemory(
        memory_key="chat_history", 
        chat_memory=redis_history,
        return_messages=True
    )

    qa = ConversationalRetrievalChain.from_llm(
        llm=chatbot, 
        retriever=docsearch.as_retriever(), 
        memory=memory,
        combine_docs_chain_kwargs={'prompt': prompt}
    )
    
    return qa({"question": user_input, 'chat_history': redis_history})

   
