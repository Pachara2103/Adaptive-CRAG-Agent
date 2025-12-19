from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_huggingface import HuggingFaceEmbeddings

import streamlit as st
from pymongo import MongoClient


@st.cache_resource 
def load_embedding_model():
    model_kwargs = {'device': 'cpu'} 
    encode_kwargs = {'normalize_embeddings': True}
    return HuggingFaceEmbeddings(
        model_name="BAAI/bge-m3",
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
)
embeddings = load_embedding_model()
# initialize MongoDB python client
uri = "mongodb+srv://user2103:bas254821@cluster0.x3bz5ht.mongodb.net/?appName=Cluster0"

client = MongoClient(uri)

DB_NAME = "vector_db"
COLLECTION_NAME = "documents"
ATLAS_VECTOR_SEARCH_INDEX_NAME = "langchain-test-index-vectorstores"

MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]

vector_store = MongoDBAtlasVectorSearch(
    collection=MONGODB_COLLECTION,
    embedding=embeddings,
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    relevance_score_fn="cosine", # Similarity function [-1,1] (close to 1 mean very similar)
    text_key="text"
)

vector_store.create_vector_search_index(dimensions=1024)
