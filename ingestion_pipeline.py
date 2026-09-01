from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv

load_dotenv()

#Load the PDF
def load_doc(doc_path):
    loader = PyMuPDFLoader(doc_path)
    doc = loader.load()

    for i,page in enumerate(doc,1):
        print(f"page no{i} ({len(page.page_content)})" )
        # print(f"Content : {page.page_content}")
        # print(f"\n{page.metadata}")
    print("Successfully Loaded!")
    return doc
    
    
#Chunking
def splitting_chunks(docs):
    print("Splitting documents into chunks")
    textSplitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap = 100
    )

    chunks = textSplitter.split_documents(docs)

    for i,chunk in enumerate(chunks,0):
        print(f"Chunk {i} ({len(chunk.page_content)})")
        print(f"Content : \n {chunk.page_content}")
        print(f"Metadata: {chunk.metadata}")
        
    print("Successfuly completed Chunking!")
    return chunks

#Storing to Chroma DB
def store_chroma(chunks):
    embedding_model = OllamaEmbeddings(
        model="nomic-embed-text"
    )
    persistant_directory = "db/vectore"

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persistant_directory,
        collection_metadata= {"hnsw:space": "cosine"}
    )

    print("---- Finished creating vector store ----")
    print(f"Vector store created and saved tp {persistant_directory}")
    return db
    
    
def main():
    
    doc_path = r"D:\Projects\RAG_Project\doc\MADHAV R KRISHNAN_Resume.pdf"
    document = load_doc(doc_path)
    chunks = splitting_chunks(document)
    vector_store = store_chroma(chunks)
    
    
if __name__ == "__main__":
    main()


