import argparse
from ingestor_factory import IngestorFactory
from updater_factory import UpdaterFactory

from dotenv import load_dotenv
import os
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", type=str, required=True,
                        help="directory to update data from and ingest to")
    parser.add_argument("-i", "--inception_date", type=str,
                        required=True, help="inception date for updating data")

    args = parser.parse_args()

    load_dotenv()
    pinecone_key = os.environ["PINECONE_API_KEY"]
    pinecone_env = os.environ["PINECONE_ENV"]
    pinecone.init(api_key=pinecone_key, environment=pinecone_env)
    embeddings = OpenAIEmbeddings(
        openai_api_key=os.environ["OPENAI_API_KEY"])

    updater_factory = UpdaterFactory(
        args.inception_date, args.directory, "./updaters_info.json")
    updaters = updater_factory.get_updaters()
    for updater in updaters:
        updater.update()

    ingestor_factory = IngestorFactory(args.directory, embeddings)
    ingestors = ingestor_factory.get_ingestors()
    for ingestor in ingestors:
        ingestor.ingest()

    # python main.py -d ./docs/history -i 2013-01-01
    # python main.py -d ./docs/daily/20230711 -i 2023-07-11
