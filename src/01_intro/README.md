# Introduction to Graph RAG

In this intro notebook, we will build a simple vector + graph RAG pipeline using the following stack:

- Graph database: Kùzu
- Vector database: LanceDB
- Retrieval & generation framework: LlamaIndex
- Graph construction: OpenAI GPT-4o-mini
- Embedding model: OpenAI text-embedding-3-small
- Generation model: OpenAI GPT-4o-mini
- Reranking: Cohere reranker

First, we compare results from a vector-only retrieval to those from graph-only retrieval. Then, we
show how to combine the results from the two using a Cohere reranker, whose results are then passed
as context to the generation model.

As demonstrated in the notebook, combining the results from the two retrieval methods
and passing them as context to the generation model can help improve the quality of the response when
either retrieval method would otherwise fail (due to insufficient semantic similarity in the vector
space, or due to an incomplete graph).

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