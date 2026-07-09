from Indexing.loader import get_transcript , get_id , build_path
from Indexing.chunking import get_chunks
from vector_store.VectorStore import CreateStore , load_store  
from pathlib import Path 



async def ingestion_pipeline( url : str ) :  # input the id of the video 
    try : 
        video_id = get_id(url)
        document  =  get_transcript(video_id=video_id)    # get transcript 
        db_path = build_path(video_id)          # if the folder with the id is not exist then create a new collection of the vector_store 
        if not Path(db_path).exists() :                  # check if the foldes with the same not id is exist or not (same id folder  same video already present )     
            chunks = get_chunks(document )              # get chunkss 
            store = CreateStore(chunks , db_path= db_path )        # store creating 

    except  Exception as e : 
        return e 


if __name__ == "__main__"  : 
    url = r"https://youtu.be/7ARBJQn6QkM?si=HjbkFpO2LxDITGWY"
    url_1 = r"https://youtu.be/geQqpO_AFMo?si=N4DAoSXpbW8cHXAb"
    url_2 = r"https://youtu.be/HAnw168huqA?si=lMoVO2XcZuPXjo_0"
    # db_path = Path(f"D:\programing\AI-ML\Projects\Youtube chatbot using RAG\\vector_store\\faiss_db\{get_id(url_1)}")
    # # create a functionto build a path 
    ingestion_pipeline(url_2)