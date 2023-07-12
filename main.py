import argparse
from ingestor_factory import IngestorFactory
from updaters import edgar_updater

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
    parser.add_argument("-f", "--form_types", nargs='+',
                        required=True, help="array of form types for updating data")
    parser.add_argument("-s", "--symbols", nargs='+',
                        required=True, help="array of symbols for updating data")

    args = parser.parse_args()

    load_dotenv()
    pinecone_key = os.environ["PINECONE_API_KEY"]
    pinecone_env = os.environ["PINECONE_ENV"]
    pinecone.init(api_key=pinecone_key, environment=pinecone_env)
    embeddings = OpenAIEmbeddings(
        openai_api_key=os.environ["OPENAI_API_KEY"])

    edgar_updater.process_reports(
        args.form_types, args.symbols, args.inception_date, args.directory)

    ingestor_factory = IngestorFactory(args.directory, embeddings)
    ingestors = ingestor_factory.get_ingestors()
    for ingestor in ingestors:
        ingestor.ingest()

    # python main.py -d ./docs/history -i 2013-01-01 -f 8-K 10-K 10-Q -s AAPL MSFT GOOG
    # python main.py -d ./docs/daily/20230711 -i 2023-07-11 -f 8-K 10-K 10-Q -s AAPL MSFT GOOG AMZN NVDA TSLA BRK-B META V UNH LLY JPM XOM JNJ WMT MA PG AVGO ORCL HD CVX MRK KO PEP ABBV COST BAC ADBE MCD CSCO CRM
