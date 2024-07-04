from phi.embedder.openai import OpenAIEmbedder
from phi.knowledge.combined import CombinedKnowledgeBase
from phi.knowledge.pdf import PDFUrlKnowledgeBase, PDFKnowledgeBase
from phi.knowledge.website import WebsiteKnowledgeBase
from phi.knowledge.s3.base import S3KnowledgeBase
from phi.vectordb.pgvector import PgVector2

from ai.settings import ai_settings
from db.session import db_url

def load_agent_knowledge_base(agent_collection_name, website_urls, pdf_urls):
    """Loads the knowledge base for an Assistant"""
    pdf_knowledge_base = CombinedKnowledgeBase(
    sources=[
        WebsiteKnowledgeBase(urls=website_urls if website_urls else []),
        PDFUrlKnowledgeBase(urls=pdf_urls if pdf_urls else []),
    ],
    vector_db=PgVector2(
        db_url=db_url,
        # Store the embeddings in ai.pdf_documents
        collection=agent_collection_name,
        embedder=OpenAIEmbedder(model=ai_settings.embedding_model),
    ),
    # 2 references are added to the prompt
    num_documents=5,
    )
    
    return pdf_knowledge_base


pdf_knowledge_base = CombinedKnowledgeBase(
    sources=[
        WebsiteKnowledgeBase(urls=["https://codelight.co/index.html"]),
        WebsiteKnowledgeBase(urls=["https://codelight.co/about.html"]),
        WebsiteKnowledgeBase(urls=["https://codelight.co/wip-program.html"]),
        WebsiteKnowledgeBase(urls=["https://codelight.co/our-projects.html"]),
        PDFKnowledgeBase(path="data/pdfs"),
    ],
    vector_db=PgVector2(
        db_url=db_url,
        # Store the embeddings in ai.pdf_documents
        collection="codelight",
        embedder=OpenAIEmbedder(model=ai_settings.embedding_model),
    ),
    # 2 references are added to the prompt
    num_documents=5,
)

website_knowledge_base = WebsiteKnowledgeBase(
    # Add URLs to the knowledge base
    # urls=["https://docs.phidata.com/introduction"],
    max_depth=1,
    # Number of links to follow from the seed URLs
    max_links=15,
    vector_db=PgVector2(
        db_url=db_url,
        # Store the embeddings in ai.website_documents
        collection="website_documents",
        embedder=OpenAIEmbedder(model=ai_settings.embedding_model),
    ),
    # 3 references are added to the prompt
    num_documents=3,
)
