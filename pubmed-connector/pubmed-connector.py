import argparse
import os
import json
from Bio import Entrez
import urllib.request
import requests

cnvrg_workdir = os.environ.get('CNVRG_WORKDIR', '/cnvrg')

parser = argparse.ArgumentParser(description="""Preprocessor""")

parser.add_argument('--max_results', action='store', dest='max_results', required=True,
					help="""int max number of results""")

parser.add_argument('--query', action='store', dest='query', required=True,
					help="""pubmed query""")

parser.add_argument('--email', action='store', dest='email', required=True,
					help="""email address (required for pubmed api access)""")

parser.add_argument('--field', action='store', dest='field', required=True,
					help="""Whether to return the abstract, the title, both, or full articles only""")

args = parser.parse_args()
max_results = args.max_results
query = args.query
email = args.email
field = args.field

def search(query, selected_db):
    Entrez.email = email
    handle = Entrez.esearch(db=selected_db,
                            sort='relevance',
                            retmax=max_results,
                            retmode='xml',
                            term=query,
                            journal="science")
    results = Entrez.read(handle)
    return results

def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = email
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)

    results = Entrez.read(handle)
    return results

def fetch_full_articles(records):
    for paper in records['PubmedArticle']:
        if paper['MedlineCitation']:
            print(paper['MedlineCitation']['PMID'])
            paper_id = paper['MedlineCitation']['PMID']
            r = requests.get('https://www.ncbi.nlm.nih.gov/pmc/articles/PMC' + paper_id + '/pdf/' + paper_id + '.pdf')
            url = r.url
            opener = urllib.request.URLopener()
            opener.addheader('User-Agent', 'agent')
            if not os.path.exists('pdfs'):
                os.mkdir('pdfs')
            filename, headers = opener.retrieve(url, 'pdfs/' + paper_id + '.pdf')

def fetch_all_articles(papers):
    response = []
    for i, paper in enumerate(papers['PubmedArticle']):
        paper['MedlineCitation']['Article']['ArticleTitle'] = ' '.join(paper['MedlineCitation']['Article']['ArticleTitle'].split())
        entry = {"id": id_list[i]}
        if field == 'title':
            entry["title"] = paper['MedlineCitation']['Article']['ArticleTitle']
        elif field == 'abstract':
            if 'Abstract' in paper['MedlineCitation']['Article'].keys():
                entry["abstract"] = paper['MedlineCitation']['Article']['Abstract']['AbstractText'][0]
            else:
                entry["abstract"] = "MISSING"
        else:
            entry["title"] = paper['MedlineCitation']['Article']['ArticleTitle']
            if 'Abstract' in paper['MedlineCitation']['Article'].keys():
                entry["abstract"] = paper['MedlineCitation']['Article']['Abstract']['AbstractText'][0]
            else:
                entry["abstract"] = "MISSING"
        response.append(entry)
    #cnvrg_workdir + '/
    with open('pubmed.json', 'w') as outfile:
        json.dump(response, outfile)

if __name__ == '__main__':

    if field == "full":
        results = search(query, 'pmc')
        id_list = results['IdList']
        papers = fetch_details(id_list)
        fetch_full_articles(papers)
    else:
        results = search(query, 'pubmed')
        id_list = results['IdList']
        papers = fetch_details(id_list)
        fetch_all_articles(papers)



