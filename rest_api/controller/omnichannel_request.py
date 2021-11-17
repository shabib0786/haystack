from pydantic import BaseModel

class OmniChannelRequest(BaseModel):
    message: str
    sender: str