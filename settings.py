from pydantic import BaseModel, Field

class MultiCatSettings(BaseModel):
    max_users: int = Field(
        title="[CACHE] Maximum number of users",
        default=100
    )
    users_timeout: int = Field(
        title="[CACHE] Timeout for users (in seconds)",
        default=3600
    )
    max_chat_sessions: int = Field(
        title="[CACHE] Maximum number of chat for each user",
        default=100
    )
    chat_session_timeout: int = Field(
        title="[CACHE] Timeout for chat session (in seconds)",
        default=3600
    )