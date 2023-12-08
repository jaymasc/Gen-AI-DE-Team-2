import os
import redis
from langchain.memory.chat_message_histories import RedisChatMessageHistory
import json  # for serialization
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

# Setting up Redis connection
redis_client = redis.Redis(host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"], password=os.environ["REDIS_PASSWORD"], decode_responses=True)

def generate_session_id():
    return str(uuid.uuid4())  # Generate a UUID as a session ID

def get_chat_history_obj(session_id):
    return RedisChatMessageHistory( url=os.environ["REDIS_URL"], session_id=session_id )