# 📄 PDF RAG Chatbot

A simple and practical **Retrieval-Augmented Generation (RAG) based PDF Question Answering Chatbot** built with Python, LangChain, ChromaDB, Hugging Face embeddings, Google Gemini, and Streamlit.

The application allows users to upload a PDF document and ask questions about its contents. Instead of relying entirely on the language model's general knowledge, the system retrieves relevant information from the uploaded document and uses that information to generate an answer.

🔗 **Live Demo:**  
https://pdfragchatbot-ifu4ihvxwaxa4dskmwdixc.streamlit.app/

---

## 📌 Project Overview

Large Language Models can generate impressive answers, but they may not have access to the specific information contained in a private or newly uploaded document.

This project demonstrates how **RAG (Retrieval-Augmented Generation)** can be used to solve this problem.

The chatbot follows a pipeline where:

1. The user uploads a PDF.
2. The PDF is loaded and its text is extracted.
3. The extracted text is divided into smaller chunks.
4. Each chunk is converted into a numerical vector using an embedding model.
5. The vectors are stored in a ChromaDB vector database.
6. When the user asks a question, the system converts the question into a searchable representation.
7. Relevant document chunks are retrieved from ChromaDB.
8. The retrieved information is provided to Google Gemini.
9. Gemini generates an answer based only on the retrieved document context.

This helps reduce hallucination and keeps the answers grounded in the uploaded document.

---

# 🏗️ System Architecture

```text
                    ┌──────────────────┐
                    │   User Uploads   │
                    │       PDF        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   PyMuPDFLoader  │
                    │  PDF Text Extract│
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────────────┐
                    │ RecursiveCharacter       │
                    │ TextSplitter              │
                    │                          │
                    │ Chunk Size: 800          │
                    │ Overlap: 100             │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ Hugging Face Embeddings  │
                    │                          │
                    │ all-MiniLM-L6-v2         │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │       ChromaDB           │
                    │    Vector Database       │
                    └────────────┬─────────────┘
                                 │
                         User asks question
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ Query Rewriting           │
                    │ Using Google Gemini       │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ ChromaDB Retriever        │
                    │ Top K = 10                │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ Retrieved Document       │
                    │ Context                  │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │      Google Gemini       │
                    │      LLM Generation      │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────┐
                    │  Final Answer    │
                    │   to the User    │
                    └──────────────────┘
```
---


# ✨ Features

📄 Upload PDF documents through a web interface
🔎 Ask natural-language questions about the uploaded PDF
🧠 Retrieval-Augmented Generation architecture
📚 PDF text extraction using PyMuPDF
✂️ Intelligent document chunking
🔢 Semantic embeddings using Hugging Face
🗄️ Vector storage and similarity search using ChromaDB
🤖 Google Gemini for query rewriting and answer generation
💬 Conversation history support
🔄 Context-aware follow-up questions
🛡️ Answers are instructed to remain grounded in the document
🌐 Streamlit-based web interface
☁️ Deployed online using Streamlit Community Cloud

---

## 🛠️ Technologies Used
1. Python

Python is the primary programming language used to build the complete RAG pipeline.

It is used for:

PDF processing
Text splitting
Embedding generation
Vector database creation
Retrieval
LLM interaction
Conversation management
Streamlit application development

2. Streamlit

Streamlit is used to create the web interface for the application.

It provides:

PDF upload functionality
Chat input
Display of questions and answers
Application state management
Simple and interactive UI

The application is deployed using Streamlit Community Cloud.

3. LangChain

LangChain is used as the main framework for connecting the different components of the RAG pipeline.

It provides abstractions for:

Document loading
Text splitting
Embeddings
Vector stores
Retrievers
Chat models
Message history

The project uses several LangChain integrations including:

langchain
langchain-core
langchain-community
langchain-chroma
langchain-huggingface
langchain-google-genai
langchain-text-splitters

📄 4. PyMuPDFLoader

The project uses:

from langchain_community.document_loaders import PyMuPDFLoader

PyMuPDFLoader is responsible for loading and extracting text from PDF files.
The extracted content is represented as LangChain Document objects.
Each document also contains metadata such as page information.

✂️ 5. RecursiveCharacterTextSplitter

The extracted PDF content is divided into smaller chunks using:

RecursiveCharacterTextSplitter

Configuration used:

chunk_size = 800
chunk_overlap = 100
Why RecursiveCharacterTextSplitter?

A complete PDF can contain a large amount of text, which should not be directly passed to the LLM.

Splitting the document into smaller chunks makes retrieval more efficient.

RecursiveCharacterTextSplitter attempts to split the content using increasingly smaller separators while trying to preserve meaningful text boundaries.

The overlap helps prevent important information from being lost between two consecutive chunks.

Example:
```
Chunk 1
--------------------------------
...information about machine
learning and artificial...
--------------------------------

Chunk 2
--------------------------------
...artificial intelligence
and neural networks...
--------------------------------
```
The overlap provides some shared context between chunks.

🔢 6. Hugging Face Embeddings

The project uses:

HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

The embedding model converts text into numerical vectors.

For example:
```
"Python is a programming language"
                 ↓
          Embedding Model
                 ↓
       [0.12, -0.45, 0.78, ...]
```
These vectors allow the system to compare the semantic similarity between the user's question and document chunks.

Embedding Model
sentence-transformers/all-MiniLM-L6-v2

This model was selected because it is lightweight and suitable for a small-to-medium scale RAG application.

It also allows embeddings to be generated locally rather than requiring an external embedding API for every document chunk.

🗄️ 7. ChromaDB

ChromaDB is used as the vector database.

The document chunks and their embeddings are stored in ChromaDB.

The project uses cosine similarity:

collection_metadata={"hnsw:space": "cosine"}

Cosine similarity measures how similar two vectors are based on their direction.

When the user asks a question, the system searches the vector database for document chunks that are semantically similar to the question.

🔍 8. Retrieval

The vector database is converted into a LangChain retriever:
```
retriever = db.as_retriever(
    search_kwargs={"k": 10}
)
```
The system retrieves the top 10 relevant document chunks.

These retrieved documents become the context provided to the LLM.

🤖 9. Google Gemini

Google Gemini is used as the Large Language Model.

It is responsible for two important tasks.

Query Rewriting

When conversation history exists, the system rewrites the latest user question into a standalone search query.

For example:
```
User:
What is his CGPA?

Previous question:
Tell me about Madhav's education.

          ↓

Query Rewriting

          ↓

What is Madhav's CGPA?
```
This improves retrieval for follow-up questions.

Answer Generation

After retrieving relevant chunks, the document context is passed to Gemini.

The model is instructed to:

Use only the provided document context
Avoid outside knowledge
Avoid inventing information
Preserve terminology from the document
Say that there is not enough information when the answer is unavailable

This makes the response more suitable for a document-based question-answering system.

💬 10. Conversation History

The application maintains conversation history using LangChain message objects:

HumanMessage
AIMessage
SystemMessage

The history allows the chatbot to understand follow-up questions.

For example:
```
User:
What projects has Madhav worked on?

Assistant:
He has worked on ...

User:
Which technologies were used in the first one?
```
The second question depends on the previous conversation.

The system uses previous user questions during query rewriting to resolve references.

🧠 Query Rewriting

One of the important concepts implemented in this project is query rewriting.

Instead of directly sending every user question to the vector database, the system checks whether conversation history exists.

If history exists, previous human messages are extracted:
```
previous_questions = [
    message
    for message in chat_history
    if isinstance(message, HumanMessage)
]
```
This ensures that the query rewriting component primarily receives previous user questions.

The latest question is then rewritten into a standalone search query.

This is especially useful for questions containing references such as:

"What about it?"
"Which one?"
"What technologies were used there?"
"What is his CGPA?"
"Tell me more about that project."
🔐 Prompt Engineering

Prompt engineering is an important part of this project.

The system uses separate instructions for:

Query Rewriting

The query rewriting prompt instructs the model to:

Rewrite only the latest question
Never answer the question
Never invent information
Use previous user questions to resolve references
Return only the rewritten query
Answer Generation

The answer-generation prompt instructs the model to:

Use only the retrieved document context
Avoid outside knowledge
Avoid hallucinating
Preserve document terminology
State when the document does not contain enough information

This separation makes the RAG pipeline easier to understand and control.

## 🧩 Project Structure
```
PDF_RAG_ChatBot/
│
├── app.py
│
├── ingestion_pipeline.py
│
├── retrieval_pipeline.py
│
├── inspect_layout.py
│
├── test_pdf_loaders.py
│
├── requirements.txt
│
├── .gitignore
│
└── README.md
app.py
```
Main Streamlit application.

Responsible for:

User interface
PDF uploading
Session state
Calling the ingestion pipeline
Calling the retrieval pipeline
Displaying responses
ingestion_pipeline.py

Responsible for processing the PDF.

Main stages:

PDF
 ↓
PyMuPDFLoader
 ↓
Document objects
 ↓
RecursiveCharacterTextSplitter
 ↓
Chunks
 ↓
Hugging Face Embeddings
 ↓
ChromaDB
retrieval_pipeline.py

Responsible for:

Query rewriting
Retrieval
Context construction
LLM answer generation
Conversation history
inspect_layout.py

Used during development to inspect PDF structure/layout and understand how the PDF content is being extracted.

test_pdf_loaders.py

Used during development to test PDF loading behavior and compare/inspect PDF extraction.

## 🔄 Complete RAG Workflow

The complete application can be summarized into two major pipelines.

Ingestion Pipeline
Upload PDF
     ↓
PyMuPDFLoader
     ↓
Extract PDF text
     ↓
Recursive Character Text Splitter
     ↓
Create chunks
     ↓
Generate embeddings
     ↓
Store vectors in ChromaDB
Retrieval & Generation Pipeline
User Question
     ↓
Check Conversation History
     ↓
Query Rewriting
     ↓
Standalone Search Query
     ↓
ChromaDB Similarity Search
     ↓
Retrieve Top 10 Chunks
     ↓
Build Context
     ↓
Google Gemini
     ↓
Final Answer
🧪 Example

Suppose the uploaded PDF is a resume.

The user asks:

What is Madhav's CGPA?

The system retrieves the relevant section:

Bachelor of Technology in Computer Science and Engineering

CGPA: 6.86

The retrieved information is passed to Gemini, which generates:

Madhav's CGPA is 6.86.

The model is instructed not to rely on information outside the retrieved document.

## 📦 Python Packages Used

The major packages used in this project include:

streamlit
langchain
langchain-core
langchain-community
langchain-chroma
langchain-huggingface
langchain-google-genai
langchain-text-splitters
sentence-transformers
chromadb
pymupdf
python-dotenv
Additional Python modules

The project also uses Python standard-library modules such as:

os
tempfile
uuid

These do not need to be installed separately using pip.

## 🔑 Environment Variables

The Google Gemini API key is stored securely using environment variables.

For local development, a .env file can be used:

GOOGLE_API_KEY=your_api_key_here

The .env file is excluded from Git using .gitignore.

For deployment, the API key is stored using Streamlit Secrets instead of exposing it in the source code.

Never commit API keys, passwords, or other credentials to GitHub.

## ☁️ Deployment

The application is deployed using:

Streamlit Community Cloud

## Live application:

👉 https://pdfragchatbot-ifu4ihvxwaxa4dskmwdixc.streamlit.app/

The source code is hosted on GitHub:

👉 https://github.com/rkmadhav2003-droid/PDF_RAG_ChatBot

The deployment process involves:

GitHub Repository
       ↓
Streamlit Community Cloud
       ↓
Install requirements.txt
       ↓
Configure Secrets
       ↓
Run app.py
       ↓
Live Web Application

🔒 Git & GitHub

Git is used for version control and GitHub is used to host the source code.

The project uses a .gitignore file to prevent unnecessary or sensitive files from being uploaded.

Examples of excluded files/directories include:

.venv/
.env
db/
doc/
.vscode/
__pycache__/
*.pyc
.agents/

This keeps the repository clean and prevents sensitive configuration files and local-generated databases from being committed.

## ⚡ Design Decisions

Why RAG?

A normal LLM may not know the contents of a user's private PDF.

RAG provides a way to connect an LLM with external documents.

Instead of asking:

LLM → Answer

the system uses:

Question
   ↓
Retrieve relevant information
   ↓
Provide context to LLM
   ↓
Generate answer

This makes the application more grounded in the uploaded document.

Why ChromaDB?

ChromaDB is lightweight and easy to integrate with LangChain.

It is suitable for this project because it provides:

Vector storage
Similarity search
Local persistence
LangChain integration
Why all-MiniLM-L6-v2?

The embedding model was selected because it provides a good balance between:

Speed
Resource usage
Semantic search capability
Ease of local execution

It is also convenient for a portfolio-level RAG project because embedding generation does not require sending every document chunk to an external embedding API.

Why RecursiveCharacterTextSplitter?

PDF documents can have different structures and text lengths.

RecursiveCharacterTextSplitter attempts to preserve meaningful text boundaries while creating manageable chunks.

The configured overlap also helps maintain context between neighboring chunks.

Why Query Rewriting?

Conversation-based questions are often incomplete by themselves.

For example:

User:
What projects did he work on?

User:
Which technologies were used in the first one?

The second question is not completely standalone.

Query rewriting transforms it into a more useful retrieval query while using previous user questions to resolve references.

--- 

## 🛡️ Hallucination Reduction

The system does not claim that RAG completely eliminates hallucination.

Instead, the project attempts to reduce unsupported answers through:

Retrieval of relevant document chunks
Explicit system instructions
Context-only answer generation
Prohibition of outside knowledge
A fallback response when the information is unavailable

Fallback response:

I don't have enough information in the document.

This approach keeps the chatbot focused on the uploaded document.

🚧 Current Limitations

This is intentionally a basic/portfolio-level RAG implementation, so there are several areas that could be improved.

Current limitations include:
One uploaded PDF is primarily handled per application session.
Retrieval quality depends on chunk size and embedding quality.
There is no dedicated reranking stage.
There is no hybrid keyword + semantic retrieval.
There is no advanced citation/page-reference system in the UI.
Very large documents may require additional optimization.
The application currently uses a relatively simple retrieval strategy.
Conversation history is maintained within the Streamlit session.
The application is not designed as a production-scale multi-user document platform.
 
##🚀 Future Improvements

Possible future improvements include:

1. Multi-document RAG

Allow users to upload multiple PDFs and search across all of them.

2. Source Citations

Display:

Answer
↓
Source: Page 4
Source: Page 7

so users can verify the answer.

3. Hybrid Search

Combine:

Semantic Search
+
Keyword Search

to improve retrieval quality.

4. Reranking

Retrieve a larger number of chunks initially and use a reranker to select the most relevant results.

5. Better Chat UI

Implement a more complete ChatGPT-style interface with:

Message bubbles
Chat history
New conversations
Multiple documents
Conversation management
6. Persistent User Sessions

Introduce proper user/session management so multiple users can independently maintain their documents and conversations.

7. Production Vector Database

For a larger production application, ChromaDB could be replaced or complemented by a scalable vector database such as:

Pinecone
Qdrant
Weaviate
PostgreSQL + pgvector

---
## 📚 Concepts Learned

This project helped demonstrate several important concepts in modern AI application development:

Large Language Models (LLMs)
Retrieval-Augmented Generation (RAG)
Embeddings
Vector databases
Semantic similarity
Document loaders
Text chunking
Retrieval
Prompt engineering
Query rewriting
Conversation history
LangChain
ChromaDB
Hugging Face Sentence Transformers
Google Gemini
Streamlit
Environment variables
API key management
Git
GitHub
Cloud deployment

---

## 🎯 What This Project Demonstrates

This project is more than a simple chatbot. It demonstrates how different components of an AI application can be connected into a complete pipeline:

Python
  +
LangChain
  +
PDF Processing
  +
Text Chunking
  +
Embeddings
  +
Vector Database
  +
Retrieval
  +
Google Gemini
  +
Prompt Engineering
  +
Streamlit
  +
GitHub
  +
Cloud Deployment

The main objective was to understand the fundamentals of building an end-to-end RAG application rather than simply calling an LLM API.

---

## 👨‍💻 Author

Madhav R Krishnan

Computer Engineering Graduate | AI/ML & Generative AI Enthusiast

Connect with me
🌐 Portfolio: https://portfolio-nine-ochre-50.vercel.app/
💼 LinkedIn: https://www.linkedin.com/in/madhavrk03
🐙 GitHub: https://github.com/rkmadhav2003-droid

---

⭐ If You Found This Project Useful

Feel free to explore the repository, try the live application, and provide feedback.

If you find the project useful or interesting, consider giving the repository a ⭐ on GitHub.
