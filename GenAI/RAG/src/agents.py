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

# Agent 1: Generate the answer
def generate_answer_with_agent1(query, related_chunks):
    # Combine chunks into a single context
    print("Agent1: Generating answer to the query")
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

# Agent 2: Validate and format the answer
def validate_and_format_with_agent2(answer):

    print("Agent2: Validating and Formatting the above generated answer")
    prompt_answer = PromptTemplate.from_template(
        "Review the following answer for correctness and format it into bullet points and also show the sources at last:\n\n"
        "Answer:\n{answer}\n\n"
        "Formatted Response:"
    )
    chain_answer = prompt_answer | llm
    answer_res = chain_answer.invoke(
        input={
            "answer": answer
        }
    )

    return answer_res
