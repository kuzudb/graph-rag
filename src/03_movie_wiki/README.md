# Graph RAG: Movie Wiki

We show an example of hybrid vector + graph RAG using a movie wiki dataset. The data consists of a
summary of the movie *Interstellar*, and some structured data about the movie, its cast and characters.

- The structured data is stored in Kùzu, an embedded graph database.
- The unstructured data is chunked and its vector embeddings are stored in LanceDB, an embedded vector database.
- We use the `ell` language model prompting framework to translate natural language questions to
Cypher queries, which are then executed against the graph database (Graph RAG).
- We also use `ell` to query the vector database for relevant chunks (Vector RAG).
- The results of graph + vector RAG are concatenated and passed to a Cohere reranker to rerank them based
on their relevance to the question.
- The combined context is passed to an LLM to formulate responses in natural language.

The following stack is used:

- Graph database: Kùzu
- Vector database: LanceDB
- Text preprocessing prompting framework: [ell](https://docs.ell.so/), a language model prompting framework
- Embedding model: OpenAI `text-embedding-3-small`
- Generation model: OpenAI `gpt-4o-mini`
- Reranking: Cohere reranker

### Key takeaways

Unlike the earlier example, in this case, the same data isn't present in the vector DB and the graph
DB. Instead, the vector DB is used to store chunk vectors of the unstructured text, and the graph DB
is used to store the structured dataset.

The results from the hybrid RAG script (post reranking) show that even in this scenario, where the
two retrievals retrieve from potentially non-overlapping data sources, the combination after reranking
captures the results better than either kind of retrieval alone.

## Setup

You can use the `uv` package manager to install the required dependencies:

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Visualization

Visualization of the graph requires the [Kuzu Explorer](https://github.com/kuzudb/explorer) tool.
You can start an instance of the Explorer using a Docker command.
```bash
docker run -p 8000:8000 \
           -v ./ex_kuzu_db:/database \
           -e MODE=READ_ONLY \
           --rm kuzudb/explorer:latest
```
Alternatively, you can use the provided docker-compose.yml configured with the relative path to your data and start/stop the container as follows:

### Run container

```bash
docker compose up
```

### Stop container

```bash
docker compose down
```

Run the following command to display the graph.

```cypher
MATCH (a)-[r]->(b)
RETURN *
LIMIT 100
```

![](./img/movie-graph.png)

## Running the scripts

### Create the graph

The data for the graph is stored in the `./data/interstellar` folder. The `create_graph.py` script
will create the graph from the data.

```bash
uv run create_graph.py
```

This creates a movie graph with the following schema:

![](./assets/movie-schema.png)

From the shell editor in Kùzu Explorer, you can run the following Cypher query to display all the
nodes and edges in the graph:

```cypher
MATCH (a)-[r]->(b)
RETURN *
LIMIT 100
```

![](./assets/interstellar-graph.png)


### Hybrid RAG

We will use the `ell` language model prompting framework to translate human questions from natural
language to a structured query language (Cypher) that can be executed against the graph in Kùzu. Concurrently, we will also use `ell` to use the query's vector
embeddings to query the vector database in LanceDB. The resulting context from both queries will be concatenated and passed to an LLM to generate a response.

This methodology can be termed "Hybrid RAG".

```bash
uv run hybrid_rag.py
```
To run either vector or graph retrieval alone, you can use the following commands:

```bash
uv run vector_rag.py
uv run graph_rag.py
```

The following answers are generated using the Hybrid RAG methodology:

```
Q1: What were the names of the AI robots in the movie Interstellar?

The names of the AI robots in the movie Interstellar are TARS and CASE.
---
Q2: On which planet did the crew of the Endurance meet Mann?

The crew of the Endurance met Mann on a frigid ice world.
---
Q3: What happened inside the tesseract?

Inside the tesseract, Cooper finds a four-dimensional hypercube made up of infinitely repeated copies of his daughter Murph's childhood bedroom, across different moments in time. He deduces that this tesseract was created by a future advanced humanity to allow him to communicate with the past. Cooper and the robot TARS transmit crucial information from within the black hole through the bookshelf and a wristwatch, enabling Murph to complete a gravity equation necessary for humanity to build space-faring colonies. After this, the tesseract collapses, and Cooper and TARS are ejected out of the wormhole, where they are eventually rescued.
---
Q4: Who wrote the movie Interstellar?

The movie Interstellar was written by Christopher Nolan and Jonathan Nolan.
---
Q5: What is Tom Cooper's character known for in Interstellar? Which actor played him?

Tom Cooper is known for being Joseph Cooper's son and eventually takes charge of his father's farm. He is played by actor Casey Affleck.
---

Q6: Which movies did Jessica Chastain act in that were directed by Christopher Nolan?

Jessica Chastain acted in the movie "Interstellar," which was directed by Christopher Nolan. The film was released in 2014.
---
```

Note how for each of the questions, the LLM (OpenAI `gpt-4o-mini`) in this case, is able to translate
natural language questions into Cypher queries, which are then run on the graph, the results passed
as context to the LLM, following which we get a response in natural language.

## Comparison of results

The following table shows a comparison of the results obtained from the hybrid RAG framework and the
results obtained from the vector or graph retrieval alone.

| Question | Vector RAG | Graph RAG | Hybrid RAG |
| --- | --- | --- | --- |
| Q1 | ✅ | ❌ | ✅ |
| Q2 | ✅ | ❌ | ✅ |
| Q3 | ✅ | ❌ | ✅ |
| Q4 | ❌ | ✅ | ✅ |
| Q5 | ❌ | ✅ | ✅ |
| Q6 | ❌ | ✅ | ✅ |

For cases where you ask questions about data that isn't present in the graph, the LLM will return a
response indicating that it doesn't know the answer. 

The first 3 questions are well answered by vector search, because the information is present in the
unstructured text that represents the plot synopsis of the movie. The last three questions are well
answered by the graph search, because the information is present in the graph nodes and edges that
represent the movie cast, characters and other metadata.

Depending on your use case, you could experiment with different prompts via `ell` to see if you can
improve the quality of the answers.
