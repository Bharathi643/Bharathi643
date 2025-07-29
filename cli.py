import argparse
from pubmed_fetcher.fetcher import fetch_papers
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with pharma/biotech authors.")
    parser.add_argument("query", help="Search query for PubMed.")
    parser.add_argument("-f", "--file", help="Output CSV file name.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output.")
    args = parser.parse_args()

    papers = fetch_papers(args.query, debug=args.debug)

    df = pd.DataFrame(papers)
    if args.file:
        df.to_csv(args.file, index=False)
        print(f"Results saved to {args.file}")
    else:
        print(df.to_string(index=False))

if __name__ == "__main__":
    main()
