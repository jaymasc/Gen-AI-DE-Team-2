import os
from backend.db_ops import * 
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import *
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.schema import SystemMessage

load_dotenv()
chatbot = ChatOpenAI(api_key=os.environ["OPEN_API_KEY"], model='gpt-3.5-turbo', temperature=0)
embedding_generator = OpenAIEmbeddings(api_key=os.environ["OPEN_API_KEY"], model="text-embedding-ada-002")

def generate_response(user_input, session_id):

# Prompt    
    prompt_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""You are a chatbot specialized in generating SQL queries from user inputs. 
                        You understand database schemas and can generate SQL queries based on the provided information.
                        If the user provides details of a database schema or tables with fields, use this information to create a SQL query based on the user's question.
                        If no database or table details are given, ask the user to provide this information.
                        Additionally, if the user requests a query that does not match the provided schema or tables, warn them and request a query related to the provided information."""
            ),  # The persistent system prompt
            MessagesPlaceholder( variable_name="chat_history" ),  # Where the memory will be stored.
            HumanMessagePromptTemplate.from_template( "{human_input}"),  # Where the human input will injected
        ]
    )

    #Getting chat_history_obj for session from Redis
    redis_history = get_chat_history_obj(session_id)
    # Memory setup
    memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=redis_history )
    # Create the conversation chain
    chat_chain = LLMChain(llm=chatbot, prompt=prompt_template, verbose=True, memory=memory)
    # After getting response
    response = chat_chain.run(human_input=user_input)
    # Generate and store embeddings in Redis
    #embeddings = embedding_generator.embed_query(user_input)
    #store_embeddings_in_redis(session_id, embeddings)
    return response

def generate_embeddings(text):
    return embedding_generator.embed_query(text)