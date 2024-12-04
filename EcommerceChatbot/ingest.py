# Ingest the data invector store database
from langchain_astradb import AstraDBVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings # Embedding Model
from dotenv import load_dotenv
import os
import pandas as pd
from EcommerceChatbot.data_converter import data_converter

# Load env
load_dotenv() 

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
ASTRA_DB_API_ENDPOINT=os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN=os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_KEYSPACE=os.getenv("ASTRA_DB_KEYSPACE")


embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def ingestdata(status):
    # Config of astra db
    vstore = AstraDBVectorStore(
            embedding=embeddings,
            collection_name="chatbotecom",
            api_endpoint=ASTRA_DB_API_ENDPOINT,
            token=ASTRA_DB_APPLICATION_TOKEN,  
            namespace=ASTRA_DB_KEYSPACE,  
        )
    
    storage=status
    
    # If data is not present, store the data and else if it is present then no need to store it again
    # None :- i havenot passed any thing
    if storage==None:
        docs=data_converter()
        inserted_ids = vstore.add_documents(docs)
    # If i have passed ehten it will return
    else:
        return vstore
    return vstore, inserted_ids

if __name__=='__main__':
    vstore,inserted_ids=ingestdata(None)
    print(f"\nInserted {len(inserted_ids)} documents.")
    results = vstore.similarity_search("can you tell me the low budget sound basshead.")  # checking
    for res in results:
            print(f"* {res.page_content} [{res.metadata}]")

            