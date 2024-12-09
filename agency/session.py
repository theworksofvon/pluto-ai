from typing import List, Dict, Any, Optional
from datetime import datetime
from uuid import uuid4

class Session:
    """
    Manages state and history for an agent's interactions within a single context.
    """
    def __init__(self, agent_id: str, session_id: Optional[str] = None) -> None:
        self.agent_id = agent_id
        self.session_id = session_id or str(uuid4())
        self.created_at = datetime.now()
        self.last_active = datetime.now()
        self.history: List[Dict[str, Any]] = []
        self.context: Dict[str, Any] = {}
        
    async def add_interaction(self, 
                            message: str, 
                            sender: str, 
                            metadata: Optional[Dict] = None) -> None:
        """Record an interaction in the session history"""
        self.history.append({
            "timestamp": datetime.now(),
            "sender": sender,
            "message": message,
            "metadata": metadata or {}
        })
        self.last_active = datetime.now()
        
    async def get_context(self, key: str) -> Any:
        """Retrieve context data for the session"""
        return self.context.get(key)
        
    async def set_context(self, key: str, value: Any) -> None:
        """Set context data for the session"""
        self.context[key] = value
        
    async def get_recent_history(self, limit: int = 10) -> List[Dict]:
        """Get the most recent interactions"""
        return self.history[-limit:]
    
    async def summarize_session(self) -> Dict[str, Any]:
        """Create a summary of the session state"""
        return {
            "session_id": self.session_id,
            "agent_id": self.agent_id,
            "created_at": self.created_at,
            "last_active": self.last_active,
            "interaction_count": len(self.history),
            "context_keys": list(self.context.keys())
        }