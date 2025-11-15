from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from agents.graph import create_graph

app = FastAPI(title="Agent Template")
graph = create_graph()


class ChatRequest(BaseModel):
    user_id: str
    message: str


class ChatResponse(BaseModel):
    user_id: str
    message: str
    response: str
    timestamp: str


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        state = {
            "user_id": req.user_id,
            "user_message": req.message,
        }
        result = graph.invoke(state)
        return ChatResponse(
            user_id=req.user_id,
            message=req.message,
            response=result.get("response", ""),
            timestamp=datetime.utcnow().isoformat(),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

