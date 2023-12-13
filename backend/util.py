import os
import redis
import uuid
import pandas as pd
import streamlit as st
from langchain.memory.chat_message_histories import RedisChatMessageHistory
from dotenv import load_dotenv
from textblob import TextBlob
from streamlit_modal import Modal
from PIL import Image
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()
logging.info('Loaded environment variables')

# Setting up Redis connection
redis_client = redis.Redis(host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"], password=os.environ["REDIS_PASSWORD"], decode_responses=True)
logging.info('Redis connection established')

def generate_session_id():
    logging.info('Generating new session ID')
    return str(uuid.uuid4())  # Generate a UUID as a session ID

def get_chat_history_obj(session_id):
    logging.info(f'Retrieving chat history for session ID: {session_id}')
    return RedisChatMessageHistory(url=os.environ["REDIS_URL"], session_id=session_id)
 
def get_insights_from_pandas(session_id):
    logging.info(f'Getting insights from pandas for session ID: {session_id}')
    chat_data = []
    chat_history = get_chat_history_obj(session_id).messages

    if chat_history:
        logging.info('Processing chat history for insights')
        for message in chat_history:
            chat_data.append({
                'session_id': session_id,
                'message_type': message.type,  # 'human' or 'assistant'
                'content': message.content,
            })

        # Convert to DataFrame
        df = pd.DataFrame(chat_data)

        # Analysis
        sentiment_scores = df[df['message_type'] == 'human']['content'].apply(lambda x: TextBlob(x).sentiment.polarity)
        mean_sentiment = sentiment_scores.mean()
        overall_sentiment = categorize_sentiment(mean_sentiment)
        message_count = df['message_type'].value_counts().to_dict()
        user_message_count = message_count.get('human', 0)
        llm_message_count = message_count.get('ai', 0)
        
        # Formatting the results into a report
        result = {
            'User Tone': overall_sentiment, 
            'Human Messages Count': user_message_count,
            'Bot Message Count': llm_message_count
        }       
        return result

def categorize_sentiment(sentiment):
    logging.info('Categorizing sentiment')
    if sentiment > 0.2:
        return 'Positive'
    elif sentiment < -0.2:
        return 'Negative'
    else:
        return 'Neutral'
    
def display_logo():
    logging.info('Displaying logo')
    return Image.open('app_logo.png')

def display_popup(title, value_tab):
    logging.info(f'Displaying popup: {title}')
    modal = Modal(key="Demo Key", title=title, max_width=350)
    with modal.container():
        message = ""
        for key, value in value_tab.items():
            message += f"**{key}:** {value}\n\n"
        st.markdown(message)
