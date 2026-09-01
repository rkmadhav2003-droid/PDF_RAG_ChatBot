from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage , HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

# loading llm to the pipeline.
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0
)


def ask_question(user_question,db,chat_history):
    
    if chat_history:
        
        previous_questions = [
        message
        for message in chat_history
            if isinstance(message, HumanMessage)
        ]

        rewrite_message = [
        SystemMessage(
        content="""
        You are a query rewriting component in a RAG system.

        Your ONLY task is to rewrite the user's latest question
        into a standalone search query.

        Rules:
        1. NEVER answer the question.
        2. NEVER provide facts or information.
        3. NEVER invent entities, skills, numbers, technologies,
        companies, or other details.
        4. Use previous USER QUESTIONS only to resolve references
        such as "it", "they", "those", "which ones", etc.
        5. If the latest question is already standalone,
        return it unchanged.
        6. Return ONLY the rewritten question.
        7. Do not add explanations.
        """
            )
        ] + previous_questions + [
            HumanMessage(content=user_question)
        ]

        result = llm.invoke(rewrite_message)

        content = result.content

        if isinstance(content, list):
            search_question = "".join(
                block.get("text", "")
                for block in content
                if isinstance(block, dict)
            ).strip()
        else:
            search_question = content.strip()

        print(f"Searching for: {search_question}")
        
    else:
        search_question = user_question
        
    
    #Retriver creation
    retriver = db.as_retriever(
        search_kwargs = {"k":10}
        )
    docs = retriver.invoke(search_question)
    # results = db.similarity_search_with_score(
    #     search_question,
    #     k=10
    # )
    
    # for i, (document, score) in enumerate(results):
    #     print(f"Finding {i}")
    #     print(document.page_content)
    #     print(f"Score : {score}")
        
    print(f"Found {len(docs)} relevent documents:")
    for i, doc in enumerate(docs,0):
        
        lines = doc.page_content.split('\n')[:2]
        preview = '\n'.join(lines)
        print(f" Doc {i}: {preview}...")
        
        
    #Step 3
    combined_input = f"""
        Answer the user's question using ONLY the information
        provided in the documents below.

        Rules:
        1. Do not use outside knowledge.
        2. Do not invent information.
        3. Preserve the terminology used in the documents.
        4. If the question asks for a list, include all relevant
        information supported by the documents.
        5. If the documents do not contain the answer, say exactly:
        "I don't have enough information in the document."

        Documents:
        ----------------
        {chr(10).join([doc.page_content for doc in docs])}
        ----------------

        Original user question:
        {user_question}

        Standalone retrieval question:
        {search_question}

        Answer:\n
        """

    answer_message = [
        SystemMessage(
            content="""
        You are a PDF question-answering assistant.

        Answer the user's question using ONLY the information
        contained in the document context.

        Rules:
        1. Do not use outside knowledge.
        2. Do not invent information.
        3. Do not mention information that is unrelated to the question.
        4. Answer only what the user asked.
        5. If the question asks for a list, include all relevant items
        supported by the document context.
        6. If the answer is not present in the document context,
        say exactly:

        "I don't have enough information in the document."
        """
            ),
            HumanMessage(content=combined_input)
        ]

    result = llm.invoke(answer_message)
    if isinstance(result.content, list):
        answer = "".join(
            block.get("text", "")
            for block in result.content
            if isinstance(block, dict) and block.get("type") == "text"
        )
    else:
        answer = result.content
    
    
    #Step 4: Remember Conversations
    chat_history.append(HumanMessage(content=user_question))
    chat_history.append(AIMessage(content=answer))
    
    # print(f"Answer: {answer}")
    return answer
        
    

# def start_chat():
#     print("Ask me questions! Type 'quit' to exit.")
    
#     while True:
#         question = input("\n Your qestion: ")
        
#         if question.lower() == 'quit':
#             print("Goodbye!")
#             break
#         ask_question(question)
    


# if __name__ == "__main__":
#     start_chat()