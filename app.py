from flask import Flask, render_template,  request
from dotenv import load_dotenv
import os
from EcommerceChatbot.ingest import ingestdata
from EcommerceChatbot.retrieval_generation import generate_product_bot



app = Flask(__name__)

load_dotenv()

vectorstore=ingestdata("done")
chain=generate_product_bot(vectorstore)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    result=chain.invoke(input)
    print("Response : ", result)
    return str(result)

if __name__ == '__main__':
    app.run(debug= True)