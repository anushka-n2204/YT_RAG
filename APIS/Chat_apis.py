## imports 

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from Pipeline.Ingestion_Pipeline import ingestion_pipeline
from Pipeline.chains import BuildChain
from Indexing.loader import get_id
from Database.database import SessionLocal
from Database.model import Conversation
from Schema.schema import ingestion, generation
import uuid


## important functions
chat_router = APIRouter()


## home api to show the chat APIs are live
@chat_router.get("/chat_home")
async def chat_home():
    return {"message": "Chat API's are live.."}


## post method to get the youtube link and create a vector store for the input link
@chat_router.post("/ingestion")
async def ingestion_api(data: ingestion):
    db = SessionLocal()

    try:
        video_id = get_id(data.youtube_url)
        if not video_id:
            return JSONResponse(status_code=400, content={"status": False, "message": "Invalid YouTube URL."})

        await ingestion_pipeline(data.youtube_url)

        conversation_id = str(uuid.uuid4())
        conversation_data = Conversation(
            conversation_id=conversation_id,
            user_id=data.user_id,
            video_id=video_id,
        )

        db.add(conversation_data)
        db.commit()

        return {
            "status": True,
            "message": "Video Loaded Successfully",
            "conversation_id": conversation_id,
        }

    except Exception as e:
        db.rollback()
        print("ingestion error:", e)
        return JSONResponse(status_code=500, content={"status": False, "message": "Unable to process this video right now."})

    finally:
        db.close()


## chatbot API
@chat_router.post("/bot")
async def chatbot_api(quiry: generation):
    db = SessionLocal()

    try:
        conversation = db.query(Conversation).filter(Conversation.conversation_id == quiry.conversation_id).first()
        if not conversation:
            return JSONResponse(status_code=404, content={"status": False, "message": "Conversation not found. Please load a video first."})

        chain = BuildChain(conversation.video_id)
        response = chain.invoke(quiry.question)

        return {"status": True, "BOT": response}

    except Exception as e:
        print("bot error:", e)
        return JSONResponse(status_code=500, content={"status": False, "message": "Unable to generate a response right now."})

    finally:
        db.close()
