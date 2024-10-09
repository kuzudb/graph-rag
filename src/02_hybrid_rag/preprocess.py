import argparse
import os
from pathlib import Path

import ell
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def main(files: list[str]) -> None:
    for filename in files:
        # Read the text from a file
        with open(filename, "r") as file:
                text = file.read()
        assert text


        @ell.simple(
            model="gpt-4o-mini",
            client=OpenAI(api_key=OPENAI_API_KEY),
            temperature=0.3,
        )
        def extract(text: str):
            """
            You are a helpful assistant that rewrites a given text using simple sentencesto help extract facts from it.
            """
            return f"""
                Rewrite the text for factual information extraction: {text}

                1. Do not use pronouns ("it", "they", "he", "she", etc.). Always refer to the entity
                2. Remove all commas, semicolons and colons from the extracted text.
                3. Rewrite the relationships "cofounder" as "founder", and "cofounded" as "founded".
                4. For cities, e.g. "Cupertino, California", rewrite as "Cupertino is a city in California".
                5. For states, e.g. "New York, USA", rewrite as "New York is a state in the USA".
                6. Rewrite all instances of "BlackRock" as "BlackRock Inc."
            """

        new_path = Path("../../data/blackrock/processed")
        new_path.mkdir(parents=True, exist_ok=True)

        with open(new_path/ f"{Path(filename).stem}_processed.txt", "w") as file:
            file.write(extract(text))

        print(f"Processed {filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_name", "-f", type=str, default="")
    args = parser.parse_args()

    data_dir = Path("../../data/blackrock")
    if not args.file_name:
        files = list(data_dir.glob("*.txt"))
    else:
        files = [data_dir / args.file_name]

    main(files)
