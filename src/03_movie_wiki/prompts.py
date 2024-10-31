# --- RAG ---

RAG_SYSTEM_PROMPT = """
You are an AI assistant using Retrieval-Augmented Generation (RAG).
RAG enhances your responses by retrieving relevant information from a knowledge base.
You will be provided with a question and relevant context. Use only this context to answer the question.
Do not make up an answer. If you don't know the answer, say so clearly.
Always strive to provide concise, helpful, and context-aware answers.
"""

RAG_USER_PROMPT = """
Given the following question and relevant context, please provide a comprehensive and accurate response:

Instructions:
Use ALL the information provided in the context to answer the question.
For numerical answers, please provide the exact number - do not guess or estimate.

Question: {question}

Relevant context:
{context}

Response:
"""
