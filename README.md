# Graph RAG and Hybrid RAG strategies

Recipes and notebooks to experiment with Graph RAG and Hybrid RAG strategies
using Kùzu. Feel free to clone and adapt for your own projects!

## What is RAG?

RAG stands for Retrieval Augmented Generation. It is a methodology that combines
LLMs with information retrieval (IR) systems to
generate responses to user queries in natural language. It leverages dense vector embeddings 
to represent the text chunks that are most relevant to the user query, and uses similarity
search to find the most relevant chunks in the vector embedding space. Today, there are many advanced
techniques that build on top of these methods to improve the retrieval process, such as query-time
retrieval augmentation, reranking the results from sparse and dense vector search (hybrid search),
query rewriting, corrective RAG (CRAG), and more.

## What is Graph RAG?

Graph RAG is a RAG methodology that incorporates a knowedge graph (or more
simply, a graph) as part of the retrieval process. The graph is constructed from explicitly
linked entities and relationships from the data that are (ideally) stored in a graph database.
The retrieval process leverages the graph to return results based on the explicit
entities and relationships present in the data.

## What is Hybrid RAG?

The term "Hybrid RAG" (not to be confused with hybrid *search*), is used to describe RAG systems that
combine multiple retrieval strategies. Viewed through the Graph RAG lens, Hybrid RAG can be described
as a methodology that combines Graph RAG and traditional RAG (based on vector embeddings) in the
retrieval process. See the paper
*[HybridRAG: Integrating Knowledge Graphs and Vector Retrieval Augmented Generation for Efficient Information Extraction](https://arxiv.org/abs/2408.04948)* by BlackRock and Nvidia [Aug 2024] for an example of
how Hybrid RAG can be used to enhance the retrieval process.

## Steps

In building a Graph RAG or Hybrid RAG application, we must always ask
the following primary questions:

- What is the graph, i.e., what do the nodes and edges represent? How is the graph constructed?
- How is the retrieval process in Graph RAG different from traditional vector-based RAG?

There are multiple architectures in which a knowledge graph can be used in combination with other
retrieval strategies. However, in general, there are two key stages in building any RAG application:

1. Indexing: This stage involves extracting explicit entities and their relationships from
the data and building a graph, and inserting vector embeddings of the chunks of text to build a vector index.
1. Serving: This stage involves sending the user query to the graph and/or the vector index, to enhance the retrieval quality and answer relevance.

## Why Kùzu?

Kùzu is an embedded, highly scalable graph database that supports the property graph data model through a convenient Cypher query language interface. For Graph RAG, Kùzu offers the following benefits:

- Like other systems (e.g., DuckDB, SQLite, LanceDB), Kùzu is designed to be embedded into your application, so you can easily begin building with minimum hassles (no servers or DB admin)
- Interoperability: Graphs are typically constructed from a variety of structured & unstructured sources. Kùzu allows you to seamlessly transform data between various formats while iterating on your graph data model
- Model data as structured property graphs, with strict types and more control over the schema
- Add a persistent graph layer to advanced Graph RAG methods for larger-than-memory graph applications
    - Where many existing implementations of Graph RAG utilize NetworkX, an in-memory graph library, Kùzu can serve as a persistent backend for larger-than-memory graph applications (all graph traversals are performed on disk, so it can easily handle graphs that are too large to fit in memory)
    - Kùzu seamlessly interoperates with NetworkX, so you can use NetworkX for your graph computations, and Kùzu for data storage
    - Kùzu can also serve as a PyTorch Geometric backend for more advanced graph neural network (GNN) use cases
    that involve node embeddings
- Permissively licensed (MIT license)
- Fast! Although retrieval latency is a small fraction of overall RAG application latency, Kùzu is designed to be performant and can handle large (1B node/edge) graphs, so you can move from PoC to production without worries.

