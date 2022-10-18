This library is made to connect to PubMed and retrieve information about scientific articles.
## Parameters
```--max_results``` - integer, required. Max number of results to return.

```--query``` - string, required. The text that is used to query PubMed.

```--email``` - string, required. The user's email. Required for PubMed API access.

```--field``` - string, required. The field that will be extracted from the articles. This can be the main title (-'title'), the abstract (-'abstract'), both ('title+abstract'), or full articles only ('full').

In the full-articles-only mode, a folder named "pdfs" which contains the articles files will be created as an output artifact.  
In the other modes, a json file named "pubmed.json" which contains the specified fields will be created as an output artifact.  

See information about how to build the query [here](https://dataguide.nlm.nih.gov/classes/edirect-for-pubmed/samplecode1.html#esearch).

