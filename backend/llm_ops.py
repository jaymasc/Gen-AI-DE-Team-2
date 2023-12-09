import os
import backend.db_ops as dbops
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import *
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chains import StuffDocumentsChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
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
                        If the user provides details of a database schema or tables with fields, use this information to create a SQL query based on the user's question.
                        If no database or table details are given, ask the user to provide this information.
                        Additionally, if the user requests a query that does not match the provided schema or tables, warn them and request a query related to the provided information.
                        
                        Current conversation:
                        {context}
                        Human: {question}
                        AI:"""

    prompt = PromptTemplate(input_variables=["question", "context"],template=template)

    embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
    docsearch = Pinecone.from_existing_index(
        embedding=embeddings,
        index_name=INDEX_NAME,
    )
    
    #Getting chat_history_obj for session from Redis
    redis_history = dbops.get_chat_history_obj(session_id)
    
    # Memory setup
    memory = ConversationBufferMemory(
        memory_key="chat_history", 
        chat_memory=redis_history,
        return_messages=True
    )
    
    # Create the conversation chain
    chat_chain = LLMChain(llm=chatbot, prompt=prompt)
    doc_chain = load_qa_with_sources_chain(chatbot, chain_type="stuff")
    
    qa = RetrievalQA.from_chain_type(chatbot, 
                                     retriever=docsearch.as_retriever(), 
                                     memory=memory,
                                     chain_type_kwargs={'prompt': prompt}
    )

    return qa({"query": user_input})

   
