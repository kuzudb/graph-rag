"""
Create a graph in Kùzu
"""
import os
import shutil

import kuzu
import polars as pl
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

shutil.rmtree("test_kuzudb", ignore_errors=True)
db = kuzu.Database("test_kuzudb")
conn = kuzu.Connection(db)

OPENAI_CLIENT = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def embed(query: str) -> list:
    response = OPENAI_CLIENT.embeddings.create(model="text-embedding-3-small", input=query)
    return response.data[0].embedding


# Define schema
conn.execute("""
    CREATE NODE TABLE IF NOT EXISTS Actor(name STRING, age INT64, PRIMARY KEY(name));
    CREATE NODE TABLE IF NOT EXISTS Movie(title STRING, year INT64, summary STRING, PRIMARY KEY(title));
    CREATE NODE TABLE IF NOT EXISTS Director(name STRING, age INT64, PRIMARY KEY(name));
    CREATE NODE TABLE IF NOT EXISTS Character(name STRING, description STRING, PRIMARY KEY(name));
    CREATE NODE TABLE IF NOT EXISTS Writer(name STRING, age INT64, PRIMARY KEY(name));
    CREATE REL TABLE IF NOT EXISTS ACTED_IN(FROM Actor TO Movie);
    CREATE REL TABLE IF NOT EXISTS PLAYED(FROM Actor TO Character);
    CREATE REL TABLE IF NOT EXISTS DIRECTED(FROM Director TO Movie);
    CREATE REL TABLE IF NOT EXISTS PLAYED_ROLE_IN(FROM Character TO Movie);
    CREATE REL TABLE IF NOT EXISTS RELATED_TO(FROM Character TO Character, relationship STRING);
    CREATE REL TABLE IF NOT EXISTS WROTE(FROM Writer TO Movie);
""")

# Ingest data
base_path = "../../data/interstellar"
files = {
    "Actor": "actor.csv",
    "Movie": "movie.csv",
    "Director": "director.csv",
    "Character": "character.csv",
    "Writer": "writer.csv",
    "ACTED_IN": "acted_in.csv",
    "DIRECTED": "directed.csv",
    "PLAYED": "played.csv",
    "PLAYED_ROLE_IN": "played_role_in.csv",
    "RELATED_TO": "related_to.csv",
    "WROTE": "wrote.csv",
}

for table, file in files.items():
    conn.execute(f"COPY {table} FROM '{base_path}/{file}';")
print("Finished ingesting data")

# Use an OpenAI embedding model to store a vector embedding of the "summary" property in the movie node
df = pl.read_csv(
    f"{base_path}/movie.csv",
    has_header=False
).rename({
    "column_1": "title",
    "column_2": "year",
    "column_3": "summary"
})
df.head()
final_df = (
    df.with_columns(
        pl.col("summary").map_elements(embed, return_dtype=pl.List(pl.Float32)).alias("vector")
    )
)
final_df.head()

# Add an embedding column to the `Movie` node table
conn.execute("""
    ALTER TABLE Movie ADD vector DOUBLE[1536];
""")

conn.execute(
    """
    LOAD FROM final_df
    MERGE (m:Movie {title: title})
    ON MATCH SET m.vector = vector
    """
)

# Query the graph to check what we have
print("---\nHere are the actors and the characters they played in Interstellar:")
res = conn.execute(
    """
    MATCH (a:Actor)-[:ACTED_IN]->(m:Movie {title: "Interstellar"}),
          (a)-[:PLAYED]->(c:Character)
    RETURN DISTINCT a.name, c.name
    """
)
while res.has_next():
    data = res.get_next()
    print(f"{data[0]} -> {data[1]}")


# Similarity search to find a movie whose summary embedding is closest to the query embedding
query_item = "space opera sci-fi movie"
query_vector = embed(query_item)
res = conn.execute(
    """
    MATCH (m:Movie)<-[:WROTE]-(w:Writer)
    WITH m, w, array_cosine_similarity(m.vector, $query_vector) AS similarity
    RETURN m.title AS title, similarity, m.summary AS summary, COLLECT(w.name) AS writers
    ORDER BY similarity DESC
    LIMIT 3;
    """,
    parameters={"query_vector": query_vector}
)
result = res.get_as_pl()
print(f"---\nMovies that are closest to the query '{query_item}':\n{result}")
