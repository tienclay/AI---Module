from typing import Generator, Optional, List, Dict, Any, Literal
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from phi.assistant import Assistant, AssistantRun
from pydantic import BaseModel
from api.routes.endpoints import endpoints
from ai.assistants.pdf_rag import get_agent_rag_pdf_assistant
from ai.assistants.pdf_auto import get_agent_autonomous_pdf_assistant,get_agent_autonomous_pdf_assistant_together
from ai.storage import pdf_assistant_storage
from utils.log import logger


######################################################
## Router for Serving Assistants
######################################################

assistants_router = APIRouter(prefix=endpoints.AGENT_ASSISTANTS, tags=["Agent-Assistants"])
AssistantType = Literal["AUTO_PDF", "RAG_PDF"]



def get_agent_assistant(
    assistant_type: AssistantType,
    run_id: Optional[str] = None,
    user_id: Optional[str] = None,
    agent_collection_name: Optional[str] = None,
    website_urls: List[str] = [],
    pdf_urls: List[str] = [],
    property: Any = None,
    model: str = "gpt-4o-mini"
):
    print(property)
    """Return the assistant"""
    if assistant_type == "AUTO_PDF":
        if model == "gpt-4o-mini":
            return get_agent_autonomous_pdf_assistant(run_id=run_id, user_id=user_id, agent_collection_name=agent_collection_name, website_urls=website_urls,pdf_urls=pdf_urls,property=property)
        else:
            return get_agent_autonomous_pdf_assistant_together(run_id=run_id, user_id=user_id, agent_collection_name=agent_collection_name, website_urls=website_urls,pdf_urls=pdf_urls,property=property,model=model)
    elif assistant_type == "RAG_PDF":
        return get_agent_rag_pdf_assistant(run_id=run_id, user_id=user_id, agent_collection_name=agent_collection_name, website_urls=website_urls,pdf_urls=pdf_urls,property=property)


class Property:
    prompt: Optional[str]
    description: Optional[str]
    instructions: Optional[List[str]]
    extra_instructions: Optional[List[str]]
    expected_output: str


class LoadAgentKnowledgeBaseRequest(BaseModel):
    assistant: AssistantType = "RAG_PDF"
    agent_collection_name: str
    website_urls: List[str]
    pdf_urls: List[str]
    property: Any
    model: str = "gpt-4o-mini"



@assistants_router.post("/load-agent-knowledge-base")
def load_agent_knowledge_base(body: LoadAgentKnowledgeBaseRequest):
    """Loads the knowledge base for an Assistant"""
    print(body.property)
    assistant = get_agent_assistant(assistant_type=body.assistant,
                                    agent_collection_name=body.agent_collection_name,
                                    website_urls=body.website_urls,
                                    pdf_urls=body.pdf_urls,
                                    property=body.property,
                                    model=body.model
                                    )
    if assistant.knowledge_base:
        assistant.knowledge_base.load(recreate=False)
    return {"message": "Knowledge Base Loaded"}



class CreateRunRequest(BaseModel):
    user_id: Optional[str] = None
    assistant: AssistantType = "RAG_PDF"
    agent_collection_name: Optional[str] = None
    property: Any
    model: str = "gpt-4o-mini"


class CreateRunResponse(BaseModel):
    run_id: str
    user_id: Optional[str] = None
    chat_history: List[Dict[str, Any]]
    


@assistants_router.post("/create", response_model=CreateRunResponse)
def create_assistant_run(body: CreateRunRequest):
    """Create a new Assistant run and returns the run_id"""
    logger.debug(f"CreateRunRequest: {body}")
    assistant: Assistant = get_agent_assistant(assistant_type=body.assistant, 
                                               user_id=body.user_id,
                                               agent_collection_name=body.agent_collection_name,
                                               property=body.property,
                                               model=body.model
                                               )
    # create_run() will log the run in the database and return the run_id
    # which is returned to the frontend to retrieve the run later
    run_id: Optional[str] = assistant.create_run()
    if run_id is None:
        raise HTTPException(status_code=500, detail="Failed to create assistant run")
    logger.debug(f"Created Assistant Run: {run_id}")

    return CreateRunResponse(
        run_id=run_id,
        user_id=assistant.user_id,
        chat_history=assistant.memory.get_chat_history(),        
    )


def chat_response_streamer(assistant: Assistant, message: str) -> Generator:
    for chunk in assistant.run(message):
        yield chunk


class ChatRequest(BaseModel):
    message: str
    stream: bool = True
    run_id: Optional[str] = None
    user_id: Optional[str] = None
    agent_collection_name: Optional[str] = None
    property: Any
    assistant: AssistantType = "RAG_PDF"
    model: str = "gpt-4o-mini"


@assistants_router.post("/chat")
def chat(body: ChatRequest):
    """Sends a message to an Assistant and returns the response"""

    logger.debug(f"ChatRequest: {body}")
    
    print(body)
    
    assistant: Assistant = get_agent_assistant(
        assistant_type=body.assistant, 
        run_id=body.run_id, 
        user_id=body.user_id,
        agent_collection_name=body.agent_collection_name,
        property=body.property,
        model=body.model,
    
    )
    

    if body.stream:
        return StreamingResponse(
            chat_response_streamer(assistant, body.message),
            media_type="text/event-stream",
        )
    else:
        return assistant.run(body.message, stream=False)


class ChatHistoryRequest(BaseModel):
    run_id: str
    user_id: Optional[str] = None
    assistant: AssistantType = "RAG_PDF"
    agent_collection_name: Optional[str] = None
    property: Any
    model: str = "gpt-4o-mini"


@assistants_router.post("/history", response_model=List[Dict[str, Any]])
def get_chat_history(body: ChatHistoryRequest):
    """Return the chat history for an Assistant run"""

    logger.debug(f"ChatHistoryRequest: {body}")
    assistant: Assistant = get_agent_assistant(
        assistant_type=body.assistant, 
        run_id=body.run_id, 
        user_id=body.user_id,
        agent_collection_name=body.agent_collection_name,
        property=body.property,
        model=body.model,
    )
    # Load the assistant from the database
    assistant.read_from_storage()

    return assistant.memory.get_chat_history()


class GetAssistantRunRequest(BaseModel):
    run_id: str
    user_id: Optional[str] = None
    assistant: AssistantType = "RAG_PDF"
    agent_collection_name: Optional[str] = None
    property: str
    model: str = "gpt-4o-mini"
    


@assistants_router.post("/get", response_model=Optional[AssistantRun])
def get_assistant_run(body: GetAssistantRunRequest):
    """Returns the Assistant run"""

    logger.debug(f"GetAssistantRunRequest: {body}")
    assistant: Assistant = get_agent_assistant(
        assistant_type=body.assistant,
        run_id=body.run_id, 
        user_id=body.user_id,
        agent_collection_name=body.agent_collection_name,
        property=body.property,
        model=body.model,
    )

    return assistant.read_from_storage()


class GetAllAssistantRunsRequest(BaseModel):
    user_id: str


@assistants_router.post("/get-all", response_model=List[AssistantRun])
def get_assistants(body: GetAllAssistantRunsRequest):
    """Return all Assistant runs for a user"""

    logger.debug(f"GetAllAssistantRunsRequest: {body}")
    return pdf_assistant_storage.get_all_runs(user_id=body.user_id)


class GetAllAssistantRunIdsRequest(BaseModel):
    user_id: str


@assistants_router.post("/get-all-ids", response_model=List[str])
def get_run_ids(body: GetAllAssistantRunIdsRequest):
    """Return all run_ids for a user"""

    logger.debug(f"GetAllAssistantRunIdsRequest: {body}")
    return pdf_assistant_storage.get_all_run_ids(user_id=body.user_id)


class RenameAssistantRunRequest(BaseModel):
    run_id: str
    run_name: str
    user_id: Optional[str] = None
    assistant: AssistantType = "RAG_PDF"
    agent_collection_name: Optional[str] = None
    property: str
    model: str = "gpt-4o-mini"


class RenameAssistantRunResponse(BaseModel):
    run_id: str
    run_name: str


@assistants_router.post("/rename", response_model=RenameAssistantRunResponse)
def rename_assistant(body: RenameAssistantRunRequest):
    """Rename an Assistant run"""

    logger.debug(f"RenameAssistantRunRequest: {body}")
    assistant: Assistant = get_agent_assistant(
        assistant_type=body.assistant, 
        run_id=body.run_id, 
        user_id=body.user_id,
        agent_collection_name=body.agent_collection_name,
        property=body.property,
        model=body.model,
    )
    assistant.rename_run(body.run_name)

    return RenameAssistantRunResponse(
        run_id=assistant.run_id,
        run_name=assistant.run_name,
    )


class AutoRenameAssistantRunRequest(BaseModel):
    run_id: str
    user_id: Optional[str] = None
    assistant: AssistantType = "RAG_PDF"
    agent_collection_name: Optional[str] = None
    property: str
    model: str = "gpt-4o-mini"


class AutoRenameAssistantRunResponse(BaseModel):
    run_id: str
    run_name: str


@assistants_router.post("/autorename", response_model=AutoRenameAssistantRunResponse)
def autorename_assistant(body: AutoRenameAssistantRunRequest):
    """Rename a assistant using the LLM"""

    logger.debug(f"AutoRenameAssistantRunRequest: {body}")
    assistant: Assistant = get_agent_assistant(
        assistant_type=body.assistant, 
        run_id=body.run_id, 
        user_id=body.user_id,
        agent_collection_name=body.agent_collection_name,
        property=body.property,
        model=body.model,
    )
    assistant.auto_rename_run()

    return RenameAssistantRunResponse(
        run_id=assistant.run_id,
        run_name=assistant.run_name,
    )
