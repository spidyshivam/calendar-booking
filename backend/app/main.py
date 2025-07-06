from fastapi import FastAPI
from pydantic import BaseModel
from app.agent import get_agent_response

app = FastAPI()

class UserInput(BaseModel):
    message: str
    session_id: str

@app.post("/chat")
async def chat(user_input: UserInput):
    """
    Endpoint to handle chat interactions.
    """
    response = get_agent_response(user_input.message, user_input.session_id)
    return {"response": response}
