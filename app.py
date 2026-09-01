import streamlit as st
import tempfile
from ingestion_pipeline import load_doc, splitting_chunks, store_chroma
from retrieval_pipeline import ask_question
import uuid
import os

st.title(" PDF RAG Chatbot")

# if st.button(" New Chat"):

#     # Clear session state
#     st.session_state.db = None
#     st.session_state.chat_history = []
#     st.session_state.uploaded_file_name = None
#     gc.collect()
    
#     # Delete Chroma database
#     if os.path.exists("db/vectore"):
#         shutil.rmtree("db/vectore")

#     st.rerun()
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())   

if "db" not in st.session_state:
    st.session_state.db = None
    
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")
    if st.session_state.db is None:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:
            temp_file.write(uploaded_file.getvalue())
            pdf_path = temp_file.name
         
        documents = load_doc(pdf_path)
        chunks = splitting_chunks(documents)
        
        persist_directory = os.path.join(
            "db",
            st.session_state.session_id)
        
        db = store_chroma(chunks,persist_directory)
        
        st.session_state.db = db
        
        st.success("PDF processed successfully!")
    
    
    question = st.chat_input("Ask a question about the PDF")
    if question:
        st.write("Your question:", question)
        answer = ask_question(question,
                              st.session_state.db,
                              st.session_state.chat_history)
        st.write("Answer: \n", answer)
    else:
        print("Ask a question you Dumbhead!")
    
        
    
    
    # for i, document in enumerate(documents):
    #     st.subheader(f"Page {i + 1}")
    #     st.write(document.page_content)



