import os
import redis
from langchain.memory.chat_message_histories.redis  import RedisChatMessageHistory
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

def store_embeddings_in_redis(session_id, embeddings):
    # Store embeddings as a serialized JSON string
    redis_client.set(f"embeddings:{session_id}", json.dumps(embeddings))

def get_embeddings(session_id):
    # Retrieve and deserialize embeddings
    serialized_embeddings = redis_client.get(f"embeddings:{session_id}")
    return json.loads(serialized_embeddings) if serialized_embeddings else None