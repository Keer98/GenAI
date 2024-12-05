from scraper import scrape_website
from vectorstore import create_vectorstore, load_vectorstore
from chatbot import create_chatbot
from utils import format_output
from config import BASE_URL, LLM_MODEL, LLM_API_KEY
from langchain_groq import ChatGroq
import streamlit as st
import warnings

warnings.filterwarnings("ignore")

# Streamlit App
st.set_page_config(
    page_title="Ricenoodle Thai Eatery Chatbot",
    page_icon="🍜",
    layout="centered"
)

st.title("🍜 Ricenoodle Thai Eatery Chatbot")

# Sidebar instructions
with st.sidebar:
    st.header("About")
    st.write(
        """
        Welcome to the Ricenoodle Thai Eatery Chatbot!  
        Ask any questions related to our restaurant, menu, or services.  
        """
    )
    st.info("Contact us: (508)-655-2888 | 179 West Central St, Natick, MA")

llm = ChatGroq(
        model=LLM_MODEL,
        api_key=LLM_API_KEY,
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )


website_content=scrape_website(BASE_URL)
# Generate embeddings and metadata
texts = [item['content'] for item in website_content]
urls = [item['url'] for item in website_content]
vectorstore=create_vectorstore(texts, urls, model_name="all-mpnet-base-v2")


chatbot = create_chatbot(llm)  
# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

#while True:
    
    # User input
user_message = st.text_input("Type your message:", key=f"input_{len(st.session_state['messages'])}", placeholder="Ask me something...")
    
    # Display chat history
if st.session_state["messages"]:
    for sender, message in st.session_state["messages"]:
        if sender == "user":
            st.write(f"**You:** {message}")
        else:
            st.write(f"**Chatbot:** {message}")
    # Process the user input
if user_message:
    if user_message.lower() in {"exit", "quit","bye"}:
        st.write("**Chatbot:** Goodbye! Have a great day!")
        st.session_state["messages"].append(("bot", "Goodbye! Have a great day!"))
        st.stop()  # Stop further processing
    else:
        st.session_state["messages"].append(("user", user_message))

        try:
            chatbot = create_chatbot(llm)  
            response = chatbot.invoke(
                {"input": user_message},
                config={"configurable": {"session_id": "abc123"}},
                )["answer"]
                # Append the bot's response to the session state
            st.session_state["messages"].append(("bot", response))
        except Exception as e:
            st.error("Something went wrong. Please try again later.")
st.text_input("Type your message:", key=f"new_input_{len(st.session_state['messages'])}", placeholder="Ask me something...")  # Clear input
    # Clear input field after processing
        #st.text_input("Type your message:", key="new_input", placeholder="Ask me something...")  # Clear input


