import os
from langchain.agents import AgentExecutor, create_react_agent
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.calendar_tools import check_calendar_availability, book_appointment
from dotenv import load_dotenv
from langchain_community.chat_message_histories import ChatMessageHistory
from datetime import datetime

chat_histories = {}

# --- A NEW, SIMPLER PROMPT FOR TOOL CALLING ---
# This prompt is designed for a more advanced agent type that relies on the model's
# native tool-calling ability rather than text parsing.
template = """You are a helpful Google Calendar booking assistant.
You have access to a set of tools to help users.
Today's date is {today}.
"""

# We now use ChatPromptTemplate to handle history and placeholders correctly
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", template),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

tools = [
    check_calendar_availability,
    book_appointment,
]

google_api_key = os.getenv("GEMINI_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key, convert_system_message_to_human=True)

# --- BIND THE TOOLS TO THE LLM ---
# This tells the LLM that these tools are available and forces it to output
# structured JSON when it wants to use them.
llm_with_tools = llm.bind_tools(tools)


# --- A NEW AGENT TYPE: create_openai_tools_agent ---
# This agent type is specifically designed to work with models that have been
# enabled for tool calling (like our llm_with_tools).
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
        "chat_history": lambda x: x["chat_history"],
        "today": lambda x: x["today"],
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)


agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


def get_agent_response(user_message: str, session_id: str):
    if session_id not in chat_histories:
        chat_histories[session_id] = ChatMessageHistory()
    
    chat_history = chat_histories[session_id]

    # The input variables must now match the ones in our new agent chain
    response = agent_executor.invoke({
        "input": user_message,
        "chat_history": chat_history.messages,
        "today": datetime.now().strftime("%A, %B %d, %Y")
    })

    chat_history.add_user_message(user_message)
    chat_history.add_ai_message(response["output"])
    
    return response["output"]
