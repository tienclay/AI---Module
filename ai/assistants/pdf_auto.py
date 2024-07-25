from typing import Optional, List, Any

from phi.assistant import Assistant
from phi.llm.openai import OpenAIChat

from ai.settings import ai_settings
from ai.storage import pdf_assistant_storage
from ai.knowledge_base import pdf_knowledge_base,load_agent_knowledge_base
from phi.llm.together import Together

def get_autonomous_pdf_assistant(
    run_id: Optional[str] = None,
    user_id: Optional[str] = None,
    agent_name: Optional[str] = None,

    debug_mode: bool = False,
) -> Assistant:
    """Get an Autonomous Assistant with a PDF knowledge base."""

    return Assistant(
        name="auto_pdf_assistant",
        run_id=run_id,
        user_id=user_id,
        llm=OpenAIChat(
            model=ai_settings.gpt_4,
            max_tokens=ai_settings.default_max_tokens,
            temperature=ai_settings.default_temperature,
        ),
        storage=pdf_assistant_storage,
        knowledge_base=pdf_knowledge_base,
        # Enable monitoring on phidata.app
        # monitoring=True,
        use_tools=True,
        show_tool_calls=True,
        debug_mode=debug_mode,
        description="""
        You are an assistant for Codelight, a technology company.

Your name, if asked, is SophIA.
Never direct the contact to another team member unless specified.

Your goal is to assist clients using the available tools and information.

For support or technical issues, gather necessary details and attempt to resolve them. If the problem persists, transfer to a human agent.

For project inquiries, gather all relevant details and ensure they are complete before transferring to an appropriate team member.

In case of dissatisfaction, swearing, or discovery that it’s not a human service, transfer to a human.

When responding, be objective and concise with a friendly yet professional tone.
If you don’t have some information or don’t know the answer, transfer to a human to continue the service.

Do not make assumptions about the values or details of functions. When in doubt, ask the client for clarification.

For quote requests, gather project details and then transfer to a sales representative.

If any mandatory information is missing, request the missing data from the client.
        """,
        extra_instructions=[
            "Keep your answers under 3 sentences.",
        ],
        assistant_data={"assistant_type": "autonomous"},
    )

def get_agent_autonomous_pdf_assistant(
    run_id: Optional[str] = None,
    user_id: Optional[str] = None,
    debug_mode: bool = True,
    agent_collection_name: Optional[str]= None,
    website_urls: List[str] = [],
    pdf_urls: List[str] = [],
    property: Any = None,
    
) -> Assistant:
    """Get a RAG Assistant with a PDF knowledge base."""
    
    return Assistant(
        name="rag_pdf_assistant",
        run_id=run_id,
        user_id=user_id,
        llm=OpenAIChat(
            model=ai_settings.gpt_4,
            max_tokens=ai_settings.default_max_tokens,
            temperature=ai_settings.default_temperature,
        ),
        storage=pdf_assistant_storage,
        knowledge_base=load_agent_knowledge_base(agent_collection_name,website_urls, pdf_urls),
        
        # Show tool calls in the response
        show_tool_calls=True,
        # Enable the assistant to search the knowledge base
        search_knowledge=True,
        # Enable the assistant to read the chat history
        read_chat_history=True,
        # Enable monitoring on phidata.app
        # monitoring=True,
        debug_mode=debug_mode,
        prompt=property['prompt'] if 'prompt' in property else None,
        description=property['description'] if 'description' in property else "You are an assistant",
        # extra_instructions= property['extra_instructions'] if 'extra_instructions' in property else None,
        extra_instructions=[
            "Keep your answers under 3 sentences.",
        ],
        instructions=property['instructions'] if 'instructions' in property else None,
        expected_output=property['expected_output'] if 'expected_output' in property else None,
        assistant_data={"assistant_type": "rag"},
    )
    
def get_agent_autonomous_pdf_assistant_together(
    run_id: Optional[str] = None,
    user_id: Optional[str] = None,
    debug_mode: bool = True,
    agent_collection_name: Optional[str]= None,
    website_urls: List[str] = [],
    pdf_urls: List[str] = [],
    property: Any = None,
    model: str = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
) -> Assistant:
    """Get a RAG Assistant with a PDF knowledge base."""
    
    return Assistant(
        name="rag_pdf_assistant",
        run_id=run_id,
        user_id=user_id,
        llm=Together(
            model=model,
            max_tokens=ai_settings.default_max_tokens,
            temperature=ai_settings.default_temperature,
        ),
        storage=pdf_assistant_storage,
        knowledge_base=load_agent_knowledge_base(agent_collection_name,website_urls, pdf_urls),
        
        # Show tool calls in the response
        show_tool_calls=True,
        # Enable the assistant to search the knowledge base
        search_knowledge=True,
        # Enable the assistant to read the chat history
        read_chat_history=True,
        # Enable monitoring on phidata.app
        # monitoring=True,
        debug_mode=debug_mode,
        prompt=property['prompt'] if 'prompt' in property else None,
        description=property['description'] if 'description' in property else "You are an assistant",
        # extra_instructions= property['extra_instructions'] if 'extra_instructions' in property else None,
        extra_instructions=[
            "Keep your answers under 3 sentences.",
        ],
        instructions=property['instructions'] if 'instructions' in property else None,
        expected_output=property['expected_output'] if 'expected_output' in property else None,
        assistant_data={"assistant_type": "rag"},
    )