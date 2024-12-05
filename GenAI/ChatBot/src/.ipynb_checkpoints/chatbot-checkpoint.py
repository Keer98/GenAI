from prompts import qa_prompt, contextualize_q_prompt
from vectorstore import load_vectorstore
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains.combine_documents import create_stuff_documents_chain
from utils import format_output

def create_chatbot(llm):
    """Creates a conversational RAG chain."""
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever()

    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    qa_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain )

    store = {}

    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        if session_id not in store:
            store[session_id] = ChatMessageHistory()
        return store[session_id]

    conversational_rag_chain = RunnableWithMessageHistory(rag_chain,get_session_history,input_messages_key="input",history_messages_key="chat_history",output_messages_key="answer")
    return conversational_rag_chain

def run_chatbot(llm):
    """Main chatbot loop."""
    chatbot = create_chatbot(llm)  # Replace with LLM initialization
    while True:
        message = input("User: ")
        if message.lower() in {"exit", "quit","bye"}:
            print("Goodbye!Have a great day")
            break
        response = chatbot.invoke(
            {"input": message},
            config={"configurable": {"session_id": "abc123"}},
        )["answer"]
        
        # Ensure response is a string before formatting
        if isinstance(response, str):
            print(format_output(response))
        else:
            print(format_output(str(response)))  # Convert to string if not already