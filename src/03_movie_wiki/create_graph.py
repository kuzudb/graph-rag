"""
Create a graph in Kùzu
"""
import shutil
import kuzu

shutil.rmtree("test_kuzudb", ignore_errors=True)
db = kuzu.Database("test_kuzudb")
conn = kuzu.Connection(db)

# Define schema
conn.execute("CREATE NODE TABLE Actor(name STRING, age INT64, PRIMARY KEY(name))")
conn.execute("CREATE NODE TABLE Movie(title STRING, year INT64, PRIMARY KEY(title))")
conn.execute("CREATE NODE TABLE Director(name STRING, age INT64, PRIMARY KEY(name))")
conn.execute("CREATE NODE TABLE Character(name STRING, description STRING, PRIMARY KEY(name))")
conn.execute("CREATE NODE TABLE Writer(name STRING, age INT64, PRIMARY KEY(name))")
conn.execute("CREATE REL TABLE ACTED_IN(FROM Actor TO Movie)")
conn.execute("CREATE REL TABLE PLAYED(FROM Actor TO Character)")
conn.execute("CREATE REL TABLE DIRECTED(FROM Director TO Movie)")
conn.execute("CREATE REL TABLE PLAYED_ROLE_IN(FROM Character TO Movie)")
conn.execute("CREATE REL TABLE RELATED_TO(FROM Character TO Character, relationship STRING)")
conn.execute("CREATE REL TABLE WROTE(FROM Writer TO Movie)")

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

# Query
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


