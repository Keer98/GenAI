from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

llm = ChatGroq(
        model="llama-3.1-70b-versatile",
        api_key="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",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

def generate_answer_with_llm(query, related_chunks):
    # Combine chunks into a single context
    context = "\n\n".join([chunk["metadata"]["text"] for chunk in related_chunks])

    prompt_answer = PromptTemplate.from_template(
       """The following are relevant content from documents related to the user's query:

        {context}

        User Query: {query}

        Based on the information above, please provide a brief answer to the user's question."""
    )

    chain_answer = prompt_answer | llm
    answer_res = chain_answer.invoke(
        input={
            "context": context,
            "query":query
        }
    )
    # Extract metadata from related chunks
    metadata_list = [chunk["metadata"] for chunk in related_chunks if chunk is not None]

    # Combine answer with metadata
    result = {
        "answer": answer_res,
        "metadata": metadata_list
    }

    return result

