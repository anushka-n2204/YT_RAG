## local imports 
from  Pipeline.Retrievel import  load_retriver ,format_doc 
from Models.models import chat_model 
from Prompts.prompt_file import prompt 
from vector_store.VectorStore import load_store
from Indexing.loader import build_path , get_id 

## imports 
from langchain_core.runnables import RunnableParallel  , RunnablePassthrough , RunnableLambda
from langchain_core.output_parsers import StrOutputParser



## build chain  function takes a link of the video as an input and retrun a chain   
def BuildChain(yt_link : str ) : 
    
    video_id = yt_link
    if "youtube.com" in yt_link or "youtu.be" in yt_link:
        video_id = get_id(yt_link)

    if not video_id:
        raise ValueError("Invalid YouTube URL or video ID")

    # building path for to get the vector db collection associated with this link 
    path = build_path(video_id)

    # store 
    store = load_store(path)

    # parser 
    parser = StrOutputParser() 

    ## retriver 
    Retriver = load_retriver(k=3 , store= store  )

    ## Retriver chain 
    retriver_chain = Retriver | RunnableLambda(format_doc)

    ## augmentation chain 
    augmentation_chain = RunnableParallel({ 
        'context' : retriver_chain ,
        'question' : RunnablePassthrough() , 
    })

    ## Generation Chain 
    chain =  augmentation_chain | prompt | chat_model | parser 

    return chain 


def Generate_response( quiry ) : 
    response = chain.invoke( quiry )
    return response


if __name__ == "__main__" : 
    ## link for input demo test 
    link = r"https://youtu.be/geQqpO_AFMo?si=N4DAoSXpbW8cHXAb"
    chain= BuildChain(link)
    quiry = "what is the topic of this podcast "
    print(chain.invoke(quiry))
