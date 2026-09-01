from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyMuPDFLoader


doc_path = r"D:\Projects\RAG_Project\doc\MADHAV R KRISHNAN_Resume.pdf"

loader1 = PyPDFLoader(doc_path)
doc1 = loader1.load()
print("PyPDFLoader")
for page in doc1:
    
    print(page.page_content[:60])
    
    
loader2 = PyMuPDFLoader(doc_path)
doc2 = loader2.load()
print("PyMuPDFLoader")
for page in doc2:
    print(page.page_content[:60])