# Csv format to document format
import pandas as pd
from langchain_core.documents import Document
import os


def data_converter():
    # Define the data directory and file name
    data_dir = "data"
    file_name = "Flipkart_Product.csv"

    # Use os.path.join to construct the full file path
    file_path = os.path.join(data_dir, file_name)

    # Read the data from the CSV file
    data = pd.read_csv(file_path)

    
    # Convert to desired data format
    product_list=[]

    # Iterate over the rows of the data frame
    for index,row in data.iterrows():
        # Construct an object with the column, convert to dictionary
        obj = {
            'ProductName': row['ProductName'], 
            'Price':row['Price'], 
            'Rate':row['Rate'], 
            'Review':row['Review'], 
            'Summary':row['Summary']    
        }
        # Append the object to list
        product_list.append(obj)

    # Create LangChain documents
    docs = []
    for item in product_list:
        if isinstance(item, dict):  
            ProductName = item.get('ProductName', '')
            text = f"ProductName: {item.get('ProductName', '')} \n Price: {item.get('Price', '')} \n Rating: {item.get('Rate', '')} \n Review: {item.get('Review', '')} \n Summary: {item.get('Summary', '')}"
            metadata = {"ProductName": ProductName}
            document = Document(page_content=text, metadata=metadata)
            docs.append(document)

    return docs


