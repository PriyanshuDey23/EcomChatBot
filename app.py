from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
from EcommerceChatbot.ingest import ingestdata
from EcommerceChatbot.retrieval_generation import generate_product_bot

app = Flask(__name__)

load_dotenv()

# First, ingest data if not already present( YOu can also run EcommerceChatbot/ingest.py)
# vstore, inserted_ids = ingestdata(None)
# print(f"Inserted {len(inserted_ids)} documents.")

# If ALready Present
vstore = ingestdata("done")

# Use the vector store for retrieval
chain = generate_product_bot(vstore)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input_text = msg
    result = chain.invoke(input_text)
    print("Response : ", result)
    return str(result)

if __name__ == '__main__':
    # Run the app
    app.run(debug=True)
