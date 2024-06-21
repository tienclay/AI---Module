from typing import Optional

from phi.assistant import Assistant
from phi.llm.openai import OpenAIChat

from ai.settings import ai_settings
from ai.storage import pdf_assistant_storage
from ai.knowledge_base import pdf_knowledge_base


def get_autonomous_pdf_assistant(
    run_id: Optional[str] = None,
    user_id: Optional[str] = None,
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
            "Keep your answers under 5 sentences.",
        ],
        assistant_data={"assistant_type": "autonomous"},
    )
