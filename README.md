# Graph RAG strategies

This repo contains recipes and notebooks to experiment with Graph RAG strategies using Kùzu.
Feel free to clone the repo and adapt the code to your own projects!

## What is Graph RAG?

Graph RAG can be thought of as a suite of methodologies that incorporate a knowedge graph (or more
simply, a graph) into the retrieval process to enhance the relevance and factual accuracy of the
generated responses.

In building a Graph RAG application, we must first ask
the following primary questions:

- What is the graph? What do the nodes and edges represent?
- How is the retrieval process different from traditional vector-based retrieval in RAG?

There are multiple strategies that can be used to enhance the retrieval context using a graph. Some
of them are covered in the examples in this repo.

Like in any other RAG, there are two key stages in building a Graph RAG application:

1. Indexing: This stage involves extracting explicit entities and their relationships from
the data and building a graph, and inserting vector embeddings of the chunks of text to build a vector index.
1. Serving: This stage involves sending the user query to the graph and/or the vector index, to enhance the retrieval quality and answer relevance.

## Setting up Kùzu

For Graph RAG, we will largely be using the Python API and testing out ideas using Jupyter notebooks
or Python scripts. You can manage dependencies using `requirements.txt` files, installed via `pip`,
or the `uv` package manager (recommended).

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
