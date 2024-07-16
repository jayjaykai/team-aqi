from pydantic import BaseModel

class response_message_200_list(BaseModel):
  data: list

class response_message_200_dict(BaseModel):
  data: dict

class response_message_error(BaseModel):
  error: str
