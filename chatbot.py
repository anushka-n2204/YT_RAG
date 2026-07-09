from Pipeline.chains import BuildChain 
from langchain.messages import  SystemMessage , HumanMessage , AIMessage  
from Pipeline.Ingestion_Pipeline import ingestion_pipeline

memory =  [ SystemMessage("you are a helpfull chatbot.")]
youtub_link = r"https://youtu.be/geQqpO_AFMo?si=N4DAoSXpbW8cHXAb"

# build chain function takes a youtuve link as an input 

def ChatBot(youtub_link) : 
    chain = BuildChain(youtub_link)
    while True : 
        User_input = input("Ask : ") 
        if User_input == "exit" : 
            break 
        response = chain.invoke(User_input) 
        memory.append(HumanMessage(User_input))  
        memory.append(AIMessage(response)) 

        print("AI :" , response)


if __name__ == "__main__" : 
    user = input("Enter the link of the video : ")
    print(" link --> transcript ---> Chunking ---> vector store ")
    ingestion_pipeline(user) 
    print("Injestion is Done ! ")
    print("-"*20)
    print("Start Communication ")
    ChatBot(user)