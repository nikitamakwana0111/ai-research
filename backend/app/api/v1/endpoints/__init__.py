from .research import router as research_router
from .documents import router as documents_router
from .chat import router as chat_router

__all__ = ["research_router", "documents_router", "chat_router"]
