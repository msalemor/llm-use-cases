import os
import json
from datetime import datetime
from typing import Dict, Any

import click
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import StructuredTool
from langchain import hub

load_dotenv()
llm = AzureChatOpenAI(
    api_key=os.getenv("OPENAI_KEY"),
    api_version=os.getenv("OPENAI_VERSION"),
    azure_endpoint=os.getenv("OPENAI_ENDPOINT"),
    azure_deployment=os.getenv("OPENAI_GPT_DEPLOYMENT", "gpt-4o"),
)

# Document storage (simulating a document management system)
DOCUMENTS = {}
REVIEW_HISTORY = {}

writer_reviewer_prompt_template = """
You are a Technical Documentation Specialist working in a collaborative environment. You have access to tools for creating, reviewing, and revising technical documents.

Your goal is to create high-quality technical documentation through an iterative process of writing and reviewing.

You have access to the following tools:

{tools}

Use the following format for your work:

Question: the documentation task you need to complete
Thought: you should always think about what step to take next in the documentation process
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now have completed the documentation task
Final Answer: Provide a summary of the final document and the improvement process

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""


async def generate_technical_document(topic: str, document_type: str = "guide") -> str:
    """
    Generates a technical document on the specified topic.
    
    Args:
        topic: The subject matter for the document
        document_type: Type of document (guide, api-reference, tutorial, architecture, etc.)
    """
    
    # Create a specialized prompt for document generation
    doc_prompt = f"""
    Create a comprehensive technical document about "{topic}" in the format of a {document_type}.
    
    The document should include:
    1. Executive Summary
    2. Introduction and Scope
    3. Technical Details
    4. Implementation Guidelines
    5. Best Practices
    6. Troubleshooting
    7. Conclusion
    
    Make it professional, technically accurate, and well-structured with proper headings.
    """
    
    try:
        response = await llm.ainvoke(doc_prompt)
        content = response.content if hasattr(response, 'content') else str(response)
        
        # Store the document
        doc_id = f"doc_{len(DOCUMENTS) + 1}_{topic.replace(' ', '_').lower()}"
        DOCUMENTS[doc_id] = {
            "id": doc_id,
            "topic": topic,
            "type": document_type,
            "content": content,
            "version": 1,
            "created_at": datetime.now().isoformat(),
            "status": "draft"
        }
        
        return f"Document created successfully!\n\nDocument ID: {doc_id}\n\nContent:\n{content}"
    
    except Exception as e:
        return f"Error generating document: {str(e)}"


async def review_document(document_id: str, review_focus: str = "general") -> str:
    """
    Reviews a technical document and provides detailed feedback.
    
    Args:
        document_id: The ID of the document to review
        review_focus: Focus area for review (general, technical-accuracy, clarity, completeness, etc.)
    """
    
    if document_id not in DOCUMENTS:
        return f"Document {document_id} not found. Available documents: {list(DOCUMENTS.keys())}"
    
    document = DOCUMENTS[document_id]
    
    review_prompt = f"""
    As a senior technical reviewer, please review the following technical document and provide constructive feedback.
    
    Focus area: {review_focus}
    
    Document Topic: {document['topic']}
    Document Type: {document['type']}
    
    Document Content:
    {document['content']}
    
    Please provide:
    1. Overall Assessment (score 1-10)
    2. Strengths
    3. Areas for Improvement
    4. Specific Suggestions
    5. Missing Content
    6. Technical Accuracy Issues (if any)
    7. Clarity and Readability Issues
    8. Structure and Organization Feedback
    
    Be specific and actionable in your feedback.
    """
    
    try:
        response = await llm.ainvoke(review_prompt)
        feedback = response.content if hasattr(response, 'content') else str(response)
        
        # Store the review
        review_id = f"review_{len(REVIEW_HISTORY) + 1}"
        REVIEW_HISTORY[review_id] = {
            "id": review_id,
            "document_id": document_id,
            "focus": review_focus,
            "feedback": feedback,
            "reviewed_at": datetime.now().isoformat()
        }
        
        return f"Review completed!\n\nReview ID: {review_id}\n\nFeedback:\n{feedback}"
    
    except Exception as e:
        return f"Error reviewing document: {str(e)}"


async def revise_document(document_id: str, review_id: str = "") -> str:
    """
    Revises a document based on review feedback.
    
    Args:
        document_id: The ID of the document to revise
        review_id: The ID of the review to base revisions on (optional)
    """
    
    if document_id not in DOCUMENTS:
        return f"Document {document_id} not found. Available documents: {list(DOCUMENTS.keys())}"
    
    document = DOCUMENTS[document_id]
    
    # Get the most recent review if no specific review_id provided
    if review_id:
        if review_id not in REVIEW_HISTORY:
            return f"Review {review_id} not found."
        review = REVIEW_HISTORY[review_id]
    else:
        # Find the most recent review for this document
        doc_reviews = [r for r in REVIEW_HISTORY.values() if r['document_id'] == document_id]
        if not doc_reviews:
            return f"No reviews found for document {document_id}. Please review the document first."
        review = max(doc_reviews, key=lambda x: x['reviewed_at'])
    
    revision_prompt = f"""
    Please revise the following technical document based on the provided review feedback.
    
    Original Document:
    Topic: {document['topic']}
    Type: {document['type']}
    Content: {document['content']}
    
    Review Feedback:
    {review['feedback']}
    
    Please create an improved version that addresses all the feedback points while maintaining the document's original purpose and technical accuracy.
    """
    
    try:
        response = await llm.ainvoke(revision_prompt)
        revised_content = response.content if hasattr(response, 'content') else str(response)
        
        # Update the document
        document['content'] = revised_content
        document['version'] += 1
        document['revised_at'] = datetime.now().isoformat()
        document['status'] = 'revised'
        
        return f"Document revised successfully!\n\nDocument ID: {document_id}\nNew Version: {document['version']}\n\nRevised Content:\n{revised_content}"
    
    except Exception as e:
        return f"Error revising document: {str(e)}"


async def get_document_status(document_id: str = "all") -> str:
    """
    Retrieves the status and metadata of documents.
    
    Args:
        document_id: Specific document ID or "all" for all documents
    """
    
    if document_id == "all":
        if not DOCUMENTS:
            return "No documents found."
        
        status_info = []
        for doc_id, doc in DOCUMENTS.items():
            status_info.append({
                "id": doc_id,
                "topic": doc['topic'],
                "type": doc['type'],
                "version": doc['version'],
                "status": doc['status'],
                "created_at": doc['created_at']
            })
        
        return json.dumps(status_info, indent=2)
    
    elif document_id in DOCUMENTS:
        doc = DOCUMENTS[document_id]
        return json.dumps({
            "document": doc,
            "reviews": [r for r in REVIEW_HISTORY.values() if r['document_id'] == document_id]
        }, indent=2)
    
    else:
        return f"Document {document_id} not found. Available documents: {list(DOCUMENTS.keys())}"


async def compare_document_versions(document_id: str) -> str:
    """
    Shows the evolution of a document through its versions (simulated).
    
    Args:
        document_id: The ID of the document to analyze
    """
    
    if document_id not in DOCUMENTS:
        return f"Document {document_id} not found. Available documents: {list(DOCUMENTS.keys())}"
    
    document = DOCUMENTS[document_id]
    doc_reviews = [r for r in REVIEW_HISTORY.values() if r['document_id'] == document_id]
    
    evolution_info = {
        "document_id": document_id,
        "topic": document['topic'],
        "current_version": document['version'],
        "total_reviews": len(doc_reviews),
        "status": document['status'],
        "improvement_summary": f"Document has been through {document['version']} versions with {len(doc_reviews)} reviews"
    }
    
    if doc_reviews:
        evolution_info["review_timeline"] = [
            {
                "review_id": r['id'],
                "focus": r['focus'],
                "reviewed_at": r['reviewed_at']
            } for r in sorted(doc_reviews, key=lambda x: x['reviewed_at'])
        ]
    
    return json.dumps(evolution_info, indent=2)


async def main():
    tools = [
        StructuredTool.from_function(
            coroutine=generate_technical_document,
            name="generate_technical_document",
            description="Generates a comprehensive technical document on the specified topic and type.",
        ),
        StructuredTool.from_function(
            coroutine=review_document,
            name="review_document",
            description="Reviews a technical document and provides detailed constructive feedback.",
        ),
        StructuredTool.from_function(
            coroutine=revise_document,
            name="revise_document",
            description="Revises a document based on review feedback to improve quality.",
        ),
        StructuredTool.from_function(
            coroutine=get_document_status,
            name="get_document_status",
            description="Retrieves the status and metadata of documents.",
        ),
        StructuredTool.from_function(
            coroutine=compare_document_versions,
            name="compare_document_versions",
            description="Shows the evolution of a document through its versions and reviews.",
        ),
    ]

    prompt = ChatPromptTemplate.from_template(writer_reviewer_prompt_template)
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=15,
        handle_parsing_errors=True,
    )
    
    # Example: Create a technical document, review it, and revise based on feedback
    result = await agent_executor.ainvoke(
        {"input": "Create a comprehensive technical guide about 'Microservices Architecture Best Practices', then review it for technical accuracy and completeness, and finally revise it based on the feedback to create a high-quality final document."},
    )

    click.echo(click.style("=== TECHNICAL DOCUMENTATION WORKFLOW COMPLETE ===", fg="green", bold=True))
    click.echo(click.style(result["output"], fg="cyan"))
    
    # Show final document status
    click.echo(click.style("\n=== FINAL DOCUMENT STATUS ===", fg="yellow", bold=True))
    if DOCUMENTS:
        for doc_id in DOCUMENTS:
            status_result = await get_document_status(doc_id)
            click.echo(click.style(status_result, fg="white"))


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
    # main()
