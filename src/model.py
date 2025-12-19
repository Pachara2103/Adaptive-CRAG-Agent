from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
load_dotenv()

llama = ChatOllama(model="llama3.2", temperature=0)
gemini = ChatGoogleGenerativeAI(model="gemini-2.5-flash")