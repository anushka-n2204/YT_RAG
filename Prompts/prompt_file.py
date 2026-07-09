from langchain_core.prompts import PromptTemplate 
prompt = PromptTemplate( 
    template = """
        You are a helpfull assisatant . 
        Answer  ONLY from the provided transcript context 
        If the context is insufficient , just say i don't know . 
        
        {context} 
        Question: {question}
        """ , 
        input_variables = ["context" , "question"]  , 
)