from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb

import os
import sys
from dotenv import load_dotenv
import pandas as pd
import logging
import shutil
import streamlit as st

load_dotenv('.env')  # looks for .env in Python script directory unless path is provided
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Handle SQLite3 import for deployment
deploy = True
if deploy:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


# Document locations (relative to this py file)
folder_paths = ['data']

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_csv_files(folders):
    """
    Process CSV files from specified folders and convert them to a list of LangChain documents.
    """
    all_docs = []
    for folder in folders:
        if not os.path.exists(folder):
            logging.warning(f"Folder '{folder}' does not exist.")
            continue
        
        logging.info(f"Processing folder: {folder}")
        
        # Only process 'processed_data.csv' if it exists in the folder
        file_path = os.path.join(folder, 'processed_data.csv')
        if not os.path.exists(file_path):
            logging.warning(f"File 'processed_data.csv' does not exist in folder '{folder}'.")
            continue
        
        logging.info(f"Processing CSV file: {file_path}")
        
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Process each row as a separate document
        for _, row in df.iterrows():
            content = " ".join([f"{col}: {val}" for col, val in row.items()])
            metadata = {
                "source": 'processed_data.csv',
                "row_index": _,
            }
            doc = Document(page_content=content, metadata=metadata)
            all_docs.append(doc)
        
        logging.info(f"Processed {len(df)} rows from 'processed_data.csv'")
    
    logging.info(f"Total documents created: {len(all_docs)}")
    return all_docs

def insert_into_vector_db(docs):
    """
    Inserts documents into a single vector database collection named 'british_airway'.
    """
    try:
        # Initialize embeddings
        embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY, model='text-embedding-3-large')

        # Initialize the ChromaDB client
        client = chromadb.PersistentClient(path="./chroma_langchain_db")
        
        # Create or get the collection named 'british_airway'
        british_airway_collection = client.get_or_create_collection(
            name='british_airway',
            metadata={'hnsw:space': 'cosine'}
        )

        # Initialize Chroma vector store with the 'british_airway' collection
        british_airway_vectorstore = Chroma(
            client=client,
            collection_name='british_airway',
            embedding_function=embeddings,
        )

        # Insert documents into the 'british_airway' vector store
        british_airway_vectorstore.add_documents(documents=docs)
        
        logging.info(f"Inserted {len(docs)} documents into the 'british_airway' vector store")
    except Exception as e:
        logging.error(f"Error inserting documents into vector store: {str(e)}")
        raise

def delete_vector_db():
    """
    Deletes everything in the chroma_langchain_db directory except for the chroma.sqlite3 file.
    """
    try:
        # Remove all files except for chroma.sqlite3
        for filename in os.listdir("./chroma_langchain_db"):
            if filename != "chroma.sqlite3":
                file_path = os.path.join("./chroma_langchain_db", filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        
        logging.info("All contents in the chroma_langchain_db directory deleted successfully except for chroma.sqlite3")
    except Exception as e:
        logging.error(f"Error deleting contents of chroma_langchain_db directory: {str(e)}")
        raise

def main():
    """
    Main function to process CSV files and populate the vector databases.
    """
   
    try:
        # Delete existing vector databases
        delete_vector_db()
        logging.info("Existing vector databases deleted")

        # Process CSV files
        all_docs = process_csv_files(folder_paths)

        # Insert documents into the vector databases
        insert_into_vector_db(all_docs)

        logging.info("Vector database population completed successfully")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

# Execute the main function when the script is run
if __name__ == "__main__":
    main()
