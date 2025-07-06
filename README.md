# LangChain Calendar Booking Agent

A conversational AI agent that books appointments on your Google Calendar using LangChain, Google Gemini, and FastAPI.

This project demonstrates a robust, tool-calling agent that can understand natural language, maintain conversation history, and interact with external APIs in a reliable way.

## Core Features

-   **Conversational Interface:** Interact with the agent through a simple chat API.
-   **Natural Language Understanding:** Parses dates and times from human-like text (e.g., "tomorrow at 9 pm for 2 hours").
-   **Stateful Memory:** Remembers the context of the conversation using a session-based chat history.
-   **Tool-Calling:** Reliably uses custom tools to `check_calendar_availability` and `book_appointment`.
-   **Powered by Google Gemini:** Uses the `gemini-1.5-flash` model for reasoning and function calling.
-   **FastAPI Backend:** Served by a high-performance FastAPI server.

## How It Works

The application uses a tool-calling agent built with LangChain.

1.  A user sends a message to the FastAPI `/chat` endpoint.
2.  The `agent_executor` receives the message, along with the previous conversation history.
3.  The Gemini model, which has been bound to the custom calendar tools, decides if it can respond directly or needs to use a tool.
4.  If a tool is needed, the model generates a structured JSON object specifying the tool and its arguments.
5.  LangChain executes the corresponding Python function (`check_calendar_availability` or `book_appointment`), which interacts with the Google Calendar API.
6.  The result of the function call (the "observation") is fed back to the model.
7.  The model uses this new information to form a final, human-readable answer, which is sent back to the user.

