import os
import shutil

import openai
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.lancedb import LanceDBVectorStore

load_dotenv()

# --- Step 1: Chunk and store the vector embeddings in LanceDB ---
shutil.rmtree("./test_lancedb", ignore_errors=True)

openai.api_key = os.environ.get("OPENAI_API_KEY")
assert openai.api_key is not None, "OPENAI_API_KEY is not set"

# Define the vector store
vector_store = LanceDBVectorStore(
    uri="./test_lancedb",
    mode="overwrite",
)
# Load documents
documents = SimpleDirectoryReader("../../data/interstellar/text").load_data()

# Chunk and embed
pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=1024, chunk_overlap=32),
        OpenAIEmbedding(),
    ],
    vector_store=vector_store,
)
pipeline.run(documents=documents)

# Store the vector embeddings in LanceDB
vector_index = VectorStoreIndex.from_vector_store(
    vector_store,
    embed_model=OpenAIEmbedding(model_name="text-embedding-3-small"),
)
