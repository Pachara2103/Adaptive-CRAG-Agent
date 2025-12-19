from src.utils.vector_store import vector_store
from langchain_core.documents import Document

retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5},  #
        #  search_kwargs={"k": 3, "pre_filter": {"category": "news"}} # Hybrid Search ! pros of mongodb
    )

docs = retriever.invoke('print')
print(docs)
# doc = Document(page_content='hello word')
# vector_store.add_documents([doc])
