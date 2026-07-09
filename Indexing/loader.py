from youtube_transcript_api import  YouTubeTranscriptApi , TranscriptsDisabled 
from urllib.parse import urlparse, parse_qs
from pathlib import Path 


BASE_DIR = Path(__file__).resolve().parent.parent


transcripter = YouTubeTranscriptApi() 

## get id 
def get_id(url: str) -> str:
    parsed_url = urlparse(url)

    # youtu.be format
    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]

    # youtube.com/watch?v=
    if parsed_url.hostname in (
        "www.youtube.com",
        "youtube.com",
        "m.youtube.com"
    ):
        if parsed_url.path == "/watch":
            return parse_qs(parsed_url.query).get("v", [None])[0]

        if parsed_url.path.startswith("/embed/"):
            return parsed_url.path.split("/")[2]

        if parsed_url.path.startswith("/shorts/"):
            return parsed_url.path.split("/")[2]

    return None


## transcripter 
def get_transcript(video_id) : 
    try: 
        transcript_list = transcripter.fetch(video_id , languages = ['en' , 'hi'])
        transcripts = "".join([doc.text for doc in transcript_list])
        return transcripts
        
    except TranscriptsDisabled : 
        return "No caption is available for this video "

## build path function 

def build_path(id) : 
    path =  f"D:\programing\AI-ML\Projects\Youtube chatbot using RAG\\vector_store\\faiss_db\{id}"
    return path 

if __name__ == "__main__" : 
    id = get_id(f"https://youtu.be/DgKHBJWYpFs?si=BF2bqwkrE6u4MkQl")
    trans = get_transcript(id)
    print(trans)