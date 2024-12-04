from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from EcommerceChatbot.ingest import ingestdata
from EcommerceChatbot.prompt import PROMPT


def generate_product_bot(vectorstore):
    """
    Create a product bot chain using the provided vector store.

    Args:
        vstore: AstraDB vector store object.

    Returns:
        chain: A product bot chain.
    """

    # Create a retriever from the vector store
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # Define the product bot template
    product_bot_template =PROMPT # Imported

    # Create a chat prompt template
    prompt = ChatPromptTemplate.from_template(product_bot_template)

    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

    # Create the product bot chain
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


if __name__ == "__main__":
    # Ingest data into the vector store
    vstore = ingestdata("done")

    # Create the product bot chain
    chain = generate_product_bot(vstore)

    # Test the chain
    question = "can you tell me the most expensive sound basshead."
    answer = chain.invoke(question)
    print(answer)