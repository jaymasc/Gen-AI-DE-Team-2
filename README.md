Gen-AI-DE Team 2 Project Repository
Introduction

Welcome to the Gen-AI-DE Team 2 Project repository! This repository is part of a training course focused on AI-driven data engineering solutions. It contains a collection of scripts, database files, and documentation designed to provide a hands-on experience in managing and understanding AI-based data engineering projects.

Contents Overview

main.py: The central script that integrates various components of the project.
ingestion.py: Handles the ingestion of data into our system.  Primarily of fictional policy documents into a Pinecone vector database.
sqlDatabaseSetup.py: Script for setting up and initializing an example of a preloaded database of fictional Starfleet students 
util.py: Contains utility functions used across the project.
JSON logs: Files containing outputs or data processed by the scripts.
Knowledge directory : Policy documents and SQL schema files that are the source of ingestion into the vector database for the RAG functionality

Detailed File Descriptions
main.py
Purpose: Serves as the entry point for the project, orchestrating various functionalities.
Usage: Executed as the primary script to run the project.

ingestion.py
Purpose: Handles the ingestion of data into the system.
Usage: Invoked to load and preprocess data before further processing or analysis.

sqlDatabaseSetup.py
Purpose: Sets up and configures the SQL database environment.
Usage: Run as needed to prepare the sqlite database before any data ingestion or processing.

util.py
Purpose: Provides utility functions used across the project.
Usage: Functions are called by other scripts as needed.

Setup prior to use:

The proper operation of this demo requires having accounts on several external platforms:

1. An OpenAI account in order to support the creation of embeddings and to perform LLM inference
2. A Pinecone account using the free tier and having an index named 'test-index' where vector embedding records for fictional 'policy' docs can be stored
3. A Redis account where the app stores conversation session history

Keys for these accounts will need to be stored locally in a .env file which is not being checked into the repo in order to prevent key leakage.  The format of the .env file should be:

PINECONE_API_KEY=<YOUR KEY>
PINECONE_ENVIRONMENT_REGION=gcp-starter
OPENAI_API_KEY=<YOUR KEY>
EMBEDDING_LOG_DIR="backend/logs/embedding_logs"
CHATBOT_LOG_DIR="backend/logs/chat_logs"
REDIS_USERNAME = "default"
REDIS_PASSWORD="<YOUR PASSWORD>"
REDIS_HOST="<YOUR REDIS HOST>"
REDIS_PORT="<YOUR REDIS PORT>"
REDIS_DB ="text2sql"
REDIS_URL = "<YOUR REDIS URL>"

You will want to load the sample policy docs into redis by executing the following on a command line:

> python ingestion.py setup

You will want to generate the internal sample sqlite db by executing the following on a command line:

> python sqlDatabaseSetup.py



