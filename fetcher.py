from typing import List, Dict
from Bio import Entrez
import pandas as pd
import re

Entrez.email = "your-email@example.com"

def is_non_academic(affiliation: str) -> bool:
    if not affiliation:
        return False
    academic_keywords = ["university", "college", "school", "institute", "department", "hospital", "lab"]
    return not any(word.lower() in affiliation.lower() for word in academic_keywords)

def fetch_papers(query: str, debug: bool = False) -> List[Dict]:
    handle = Entrez.esearch(db="pubmed", term=query, retmax=50)
    record = Entrez.read(handle)
    ids = record["IdList"]
    handle.close()

    results = []
    for pmid in ids:
        summary = Entrez.efetch(db="pubmed", id=pmid, retmode="xml")
        data = Entrez.read(summary)
        summary.close()
        article = data['PubmedArticle'][0]['MedlineCitation']

        title = article.get('Article', {}).get('ArticleTitle', '')
        pub_date = article.get('Article', {}).get('Journal', {}).get('JournalIssue', {}).get('PubDate', {})
        pub_date_str = "-".join(str(pub_date.get(k, "")) for k in ['Year', 'Month', 'Day'])

        authors_data = article.get('Article', {}).get('AuthorList', [])
        non_academic_authors = []
        company_affiliations = []
        corresponding_email = ""

        for author in authors_data:
            if 'AffiliationInfo' in author:
                aff = author['AffiliationInfo'][0].get('Affiliation', '')
                if is_non_academic(aff):
                    name = f"{author.get('ForeName', '')} {author.get('LastName', '')}".strip()
                    non_academic_authors.append(name)
                    company_affiliations.append(aff)
                email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", aff)
                if email_match:
                    corresponding_email = email_match.group(0)

        if non_academic_authors:
            results.append({
                "PubmedID": pmid,
                "Title": title,
                "Publication Date": pub_date_str,
                "Non-academic Author(s)": "; ".join(non_academic_authors),
                "Company Affiliation(s)": "; ".join(company_affiliations),
                "Corresponding Author Email": corresponding_email
            })

        if debug:
            print(f"Processed {pmid} - Found: {len(non_academic_authors)} non-academic authors")
    return results



