from phi.agent import Agent
from phi.model.groq import Groq
from agents import generate_answer_with_agent1, validate_and_format_with_agent2

# Initialize the LLM with an updated model
groq_model = Groq(
    model="mixtral-8x7b-32768",  # Replace with the currently supported model
    api_key="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",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Define the Generate Agent
generate_agent = Agent(
    name="Generate Agent",
    role="Provide answers to user queries based on provided context",
    model=groq_model,
    tools=[generate_answer_with_agent1],
    instructions=[
        "Generate an answer based on the query and related chunks.",
        "Use the following steps:",
        "1. Combine the chunks into a coherent context.",
        "2. Analyze the context using the LLM to generate an answer.",
        "3. Provide a concise and accurate response to the query.",
    ],
    show_tool_calls=True,
    markdown=True,
)

# Define the Validate and Format Agent
validate_format_agent = Agent(
    name="Validate and Format Agent",
    role="Validate and format the answer",
    model=groq_model,
    tools=[validate_and_format_with_agent2],
    instructions=[
        "Validate the correctness of the generated answer and format it.",
        "Steps to follow:",
        "1. Review the answer for correctness and consistency with the context.",
        "2. Format the response into clear and concise bullet points.",
        "3. Include references to sources at the end of the response.",
        "4. Ensure the final response is easy to read and understand.",
    ],
    show_tool_calls=True,
    markdown=True,
)

# Define the Agent Manager
agent_manager = Agent(
    model=groq_model,
    team=[generate_agent, validate_format_agent],  # Use Agent objects
    instructions=[
        "Handle user queries by generating and validating responses based on relevant documents.",
        "First, use the Generate Answer Agent to retrieve relevant chunks and create a concise response.",
        "Then, pass the generated answer to the Validation Agent to ensure correctness and format it into bullet points.",
        "Include sources or references in the final output.",
        "Ensure seamless collaboration between agents and provide a clear, actionable response to the user.",
    ],
    show_tool_calls=True,
    markdown=True,
)

# Function to initialize and handle the query
def initialize_agent(query, related_chunks):
    input_data = {"query": query, "related_chunks": related_chunks}
    return agent_manager.print_response(input_data, stream=True)
