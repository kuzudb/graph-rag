# Hybrid RAG

This notebook shows an example of the Hybrid RAG methodology, as per the BlackRock and Nvidia paper
*[HybridRAG: Integrating Knowledge Graphs and Vector Retrieval Augmented Generation for Efficient Information Extraction](https://arxiv.org/abs/2408.04948)*
from August 2024.

This is similar to the intro Graph RAG pipeline on the Curie dataset, but with an important difference: the knowledge graph here is constructed in *two* stages:
- First, the text is preprocessed with an LLM that rewrites the text in simple sentences, so that the entities and relationships are more
explicitly represented, and pronouns are replaced with the entities they refer to. This will help the extraction LLM in the second stage by providing a cleaner input.
- Next, the entity and relationship extraction stage uses the preprocessed text to explicitly extract the nodes
and edges that will represent the graph, as per a specified schema.

The rest of the pipeline is similar to the intro RAG pipeline, where we also store the chunk embeddings of the original text in the vector store. At retrieval time, we retrieve from both the vector store and the graph store, and then combine the results using a Cohere reranker that provides the combined context to the generation LLM.

The following stack is used:

- Graph database: Kùzu
- Vector database: LanceDB
- Text preprocessing prompting framework: [ell](https://docs.ell.so/), a language model prompting framework + OpenAI GPT-4o-mini
- Retrieval & generation framework: LlamaIndex
- Graph construction: OpenAI GPT-4o-mini
- Embedding model: OpenAI text-embedding-3-small
- Generation model: OpenAI GPT-4o-mini
- Reranking: Cohere reranker

## Setup

We will be using the Python API of Kùzu and testing out ideas using Jupyter notebooks
or Python scripts along with other dependencies. You can manage dependencies using
`requirements.txt` files, installed via `pip`, or the `uv` package manager (recommended).

The example below shows how to set up a virtual environment using `uv`.

```bash
# Set up a virtual environment using the uv package manager
# https://github.com/astral-sh/uv
uv venv
source .venv/bin/activate
# Install kuzu
uv pip install -r requirements.txt
```

You can then create a new `ipykernel`, so that you can use the virtual environment in the notebook.

```bash
ipython kernel install --user --name=rag_env
```

Locate the new kernel in the list of kernels in Jupyter and select it to begin installing packages
and running the notebooks.