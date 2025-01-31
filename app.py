import streamlit as st  # Importing Streamlit for building the app
from langchain_community.document_loaders import WebBaseLoader  # For loading web content
from langchain.text_splitter import RecursiveCharacterTextSplitter  # To split text into manageable chunks
from langchain_google_genai import GoogleGenerativeAIEmbeddings  # For embeddings using Google Generative AI
import google.generativeai as genai  # Google Generative AI library
from langchain_community.vectorstores import FAISS  # For similarity search and vector database
from dotenv import load_dotenv  # To load environment variables from a .env file
import os  # For operating system-related tasks like accessing environment variables

# Load environment variables from a .env file
load_dotenv()

# Configure the Google Generative AI API using the API key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Streamlit App
st.title("Question-Answering from Any URL")  # Display the app title

# User inputs the URL and query
url = st.text_input("Enter the URL of the website:")  # Input field for the website URL
query = st.text_input("Enter your question:")  # Input field for the user's question

# Process the inputs only if both URL and query are provided, and the "Submit" button is clicked
if st.button("Submit") and url and query:
    try:
        # Load documents from the provided URL
        st.write("Loading content from the URL...")
        loader = WebBaseLoader(url)  # Initialize the web loader with the given URL
        docs = loader.load()  # Load the content of the website as documents

        # Split the loaded documents into smaller chunks for processing
        st.write("Processing the content...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)  
        # Splits text into chunks of 1000 characters with 200 characters overlapping
        documents = text_splitter.split_documents(docs)

        # Create a vector database from the document chunks using Google Generative AI embeddings
        vectordb = FAISS.from_documents(documents, GoogleGenerativeAIEmbeddings(model="models/embedding-001"))

        # Perform a similarity search in the vector database using the user's query
        st.write("Finding the answer to your question...")
        retrieved_results = vectordb.similarity_search(query)

        # Display the result if relevant content is found
        if retrieved_results:
            st.success("Answer:")  # Display success message
            st.write(retrieved_results[0].page_content)  # Show the content of the most relevant result
        else:
            # Warn the user if no relevant content is found
            st.warning("No relevant content found for your query.")
    except Exception as e:
        # Display an error message in case of an exception
        st.error(f"An error occurred: {e}")
