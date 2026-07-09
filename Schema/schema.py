from pydantic import BaseModel  , Field 



## user data 
class User_data(BaseModel) : 
    name  : str = Field(... , description = "Enter the name or user name ")
    email : str = Field(... , description = "Enter the email id of user ")
    password : str = Field(... , description = "Enter the password ") 

# login data 
class LoginData (BaseModel) : 
    email   : str = Field(... , description = "Enter the email id ")
    password : str = Field(... , description = "Enter the email id ")

# ingestion pipeline 
class ingestion(BaseModel ) : 
    youtube_url : str = Field(... ,description = "Enter the youtube Url")
    user_id     : str = Field(... , description= "Enter the current user id ") 

## generation pipeline 
class generation(BaseModel) : 
    conversation_id :str = Field(... , description = "this id is stored in the frontend after user insert the youtube url (response from the ingestion pipeline) ") 
    question : str = Field(... , description = "Ask Question related to provided youtube video ")