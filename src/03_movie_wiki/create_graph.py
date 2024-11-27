"""
Create a graph in Kùzu
"""

import shutil

import kuzu

shutil.rmtree("test_kuzudb", ignore_errors=True)
db = kuzu.Database("test_kuzudb")
conn = kuzu.Connection(db)

# Define schema
conn.execute("""
    CREATE NODE TABLE IF NOT EXISTS Actor(name STRING, age INT64, PRIMARY KEY(name));
    CREATE NODE TABLE IF NOT EXISTS Movie(title STRING, year INT64, PRIMARY KEY(title));
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
