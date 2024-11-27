import os

import ell
import lancedb
from dotenv import load_dotenv
from openai import OpenAI

import prompts


class VectorRAG:
    def __init__(self, db_path: str, table_name: str = "vectors"):
        load_dotenv()
        self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.db = lancedb.connect(db_path)
        self.table = self.db.open_table(table_name)

    def query(self, query_vector: list, limit: int = 10) -> list:
        search_result = (
            self.table.search(query_vector).metric("cosine").select(["text"]).limit(limit)
        ).to_list()
        return search_result if search_result else None

    def embed(self, query: str) -> list:
        # For now just using an OpenAI embedding model
        response = self.openai_client.embeddings.create(model="text-embedding-3-small", input=query)
        return response.data[0].embedding

    @ell.simple(model="gpt-4o-mini", temperature=0.3, seed=42)
    def retrieve(self, question: str, context: str) -> str:
        return [
            ell.system(prompts.RAG_SYSTEM_PROMPT),
            ell.user(prompts.RAG_USER_PROMPT.format(question=question, context=context)),
        ]

    def run(self, question: str) -> str:
        question_embedding = self.embed(question)
        context = self.query(question_embedding)
        return self.retrieve(question, context)


if __name__ == "__main__":
    vector_rag = VectorRAG("./test_lancedb")

    # The first three questions are well answered by vector search
    question = "What were the names of the AI robots in the movie Interstellar?"
    response = vector_rag.run(question)
    print(f"Q1: {question}\n\n{response}")

    question = "On which planet did the crew of the Endurance meet Mann?"
    response = vector_rag.run(question)
    print(f"---\nQ2: {question}\n\n{response}")

    question = "What happened inside the tesseract?"
    response = vector_rag.run(question)
    print(f"---\nQ3: {question}\n\n{response}")

    # The next three questions are not well answered by vector search because the information isn't
    # in the raw text.
    question = "Who wrote the movie Interstellar?"
    response = vector_rag.run(question)
    print(f"---\nQ4: {question}\n\n{response}")

    question = "What is Tom Cooper's character known for in Interstellar? Which actor played him?"
    response = vector_rag.run(question)
    print(f"---\nQ5: {question}\n\n{response}")

    question = "Which movies did Jessica Chastain act in that were directed by Christopher Nolan?"
    response = vector_rag.run(question)
    print(f"---\nQ6: {question}\n\n{response}")
