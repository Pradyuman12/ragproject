from dotenv import load_dotenv
load_dotenv()
from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import OllamaEmbeddings,ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import InMemoryVectorStore




embeddings=OllamaEmbeddings(
model="mxbai-embed-large"
)

llm = ChatOllama( model="llama3.2", temperature=0 )

vecter_db=None
#document loader
def process_document(file_path):

   global vecter_db

   loader=PyPDFLoader(file_path)
   docs=loader.load()



#spliting
   spliter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
   docs=spliter.split_documents(docs)

#vecter embbedings and store

   vecter_db=InMemoryVectorStore.from_documents(
    documents=docs,
    embedding=embeddings
)

def ask_question(query):

    if vecter_db is None:
        return "Please upload a PDF first."

    # Similarity search
    documents = vecter_db.similarity_search(
        query=query,
        k=3
    )

    # Create context
    context = ""

    for doc in documents:
        context += doc.page_content + "\n\n"

    # Prompt
    prompt = f"""
You are a helpful medical document assistant.

Answer the question only using the provided context.

If the answer is not present in the context,
say that you could not find the answer in the document.

Context:
{context}

Question:
{query}-

Answer:
"""

    # Ask Ollama
    answer = llm.invoke(prompt)

    return answer.content


