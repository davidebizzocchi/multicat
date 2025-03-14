from typing import Optional

from cat.auth.permissions import AuthPermission

from cat.auth.connection import HTTPAuth
from cat.auth.permissions import AuthResource


from typing import Dict
from pydantic import BaseModel
from fastapi import Request, HTTPException, Depends
from cat.mad_hatter.decorators import endpoint
from cat.auth.connection import HTTPAuth
from cat.auth.permissions import AuthPermission, AuthResource

from cat.looking_glass.stray_cat import StrayCat
from cat.log import log

from cat.plugins.multicat.types import Agent
from cat.plugins.multicat.agents.crud import manager as agent_manager


class AgentUpdateRequest(BaseModel):
    name: Optional[str] = None
    instructions: Optional[str] = None
    metadata: Optional[dict] = None

class AgentRequestResponse(AgentUpdateRequest):
    id: str = "default"

class AgentCreateRequest(AgentUpdateRequest):
    id: Optional[str] = "default"


@endpoint.get(path="/agents", prefix="")
async def list_agents(
    request: Request,
    cat: StrayCat=Depends(HTTPAuth(AuthResource.CONVERSATION, AuthPermission.READ)),
) -> Dict:
    """List all available agents"""
        
    return {
        "agents": list(cat.agents())
    }

@endpoint.get(path="/agents/{agent_id}", prefix="")
async def retrieve_agent(
    request: Request,
    agent_id: str,
    cat: StrayCat=Depends(HTTPAuth(AuthResource.CONVERSATION, AuthPermission.READ)),
) -> Dict:
    """Get information about a specific agent"""
    agent = cat.get_agent_by_id(agent_id)
    
    if agent is None:
        raise HTTPException(
            status_code=404,
            detail={"error": "Agent not found"}
        )
    
    return {
        "agent": AgentRequestResponse.model_validate(agent)
    }

@endpoint.post(path="/agents", prefix="")
async def create_agent(
    request: Request,
    data: AgentCreateRequest,
    cat: StrayCat=Depends(HTTPAuth(AuthResource.CONVERSATION, AuthPermission.WRITE)),
) -> Dict:
    """Create a new agent"""
    
    new_agent = cat.create_agent(
        id=data.id,
        name=data.name or "",
        instructions=data.instructions or "",
        metadata=data.metadata or {}
    )
    
    return {
        "success": True,
        "agent": AgentRequestResponse.model_validate(new_agent)
    }

@endpoint.endpoint(path="/agents/{agent_id}", prefix="", methods=["PATCH"])
async def update_agent(
    request: Request,
    data: AgentUpdateRequest,
    agent_id: str = "default",
    cat: StrayCat=Depends(HTTPAuth(AuthResource.CONVERSATION, AuthPermission.WRITE)),
) -> Dict:
    log.debug(f"User ID: {cat.user_id}")
    log.debug(f"Updating agents: {agent_id}")
    log.debug(f"New agent instructions: {data.instructions}")

    agent: Agent = cat.get_agent_by_id(agent_id).cast()

    if agent is None:
        raise HTTPException(
            status_code=400,
            detail={"error": "Agent does not exist."}
        )
    
    if data.name is not None:
        agent.name = data.name

    if data.instructions is not None:
        agent.instructions = data.instructions

    if data.metadata is not None:
        agent.metadata = data.metadata

    agent = cat.update_agent(agent)

    return {
        "success": True,
        "agent": AgentRequestResponse.model_validate(agent)
    }

@endpoint.endpoint(path="/agents/{agent_id}", prefix="", methods=["DELETE"])
async def delete_agent(
    request: Request,
    agent_id: str,
    cat: StrayCat=Depends(HTTPAuth(AuthResource.CONVERSATION, AuthPermission.WRITE)),
) -> Dict:
    """Delete an existing agent"""
    if agent_id == "default":
        raise HTTPException(
            status_code=400,
            detail={"error": "Cannot delete default agent"}
        )
    
    if agent_id not in cat.agents:
        raise HTTPException(
            status_code=404,
            detail={"error": "Agent not found"}
        )
    
    cat.delete_agent(agent_id)
    
    return {
        "success": True,
        "message": f"Agent {agent_id} deleted successfully"
    }
