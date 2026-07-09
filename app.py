from fastapi import FastAPI 
from fastapi.responses import JSONResponse
from APIS.Auth_apis import auth_router 
from APIS.Chat_apis import chat_router 
from fastapi.middleware.cors import CORSMiddleware



app  = FastAPI()



@app.get("/") 
def home() : 
    return JSONResponse("Youtube Transcrpt bot API is live ")



## --------------- allow communication between forntend and  backends running on  diffrent ports  ---------------- 

origins = [

    "http://127.0.0.1:5500",

    "http://localhost:5500"

]

app.add_middleware(

    CORSMiddleware,

    allow_origins=origins,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)

# ------------------- including different routess in app  ---------------------------------------------- 

app.include_router(auth_router)
app.include_router(chat_router)