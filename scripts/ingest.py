import argparse
from backend.graph.ingestor import ingest_document

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest a policy document into PolicyMind.")
    parser.add_argument("--file", required=True, help="Path to PDF or Markdown file")
    parser.add_argument("--name", help="Display name for the source (defaults to filename)")
    args = parser.parse_args()

    source_name = args.name or args.file.split("/")[-1]
    ingest_document(args.file, source_name)