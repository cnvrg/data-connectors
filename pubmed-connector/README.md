# PubMed Connector (Library)
This [connector](https://github.com/cnvrg/data-connectors/tree/pubmed/pubmed-connector) queries and pulls textual data associated with abstracts, citations, and papers, such as the main body, titles, headers, and figure/table titles, from the PubMed National Library of Medicine database and feeds it as input to existing model training and batch-predict blueprints. An email address is required to use this connector library to access the PubMed API.

For information about how to build a query, click [here](https://dataguide.nlm.nih.gov/classes/edirect-for-pubmed/samplecode1.html#esearch).

## Connector Flow
The following list provides this connector's high-level flow:
- The user defines input arguments such as email address. Refer to the [Run Instructions](#run-instructions) later in this document.
- The user accesses PubMed using his/her email address.
- The PubMed Connector (with the email address passed as an argument) pulls the queried textual data from the PubMed website.
- The connector library converts the textual data into one of two formats and stores it as a dataset.

## Inputs
This library assumes the user has an existing email address. The user's email address is used as input, which is required for PubMed API access.
The PubMed Connector requires the following inputs:
- `--email` (string, required) − Provide the user’s email address as an input argument.
- `--field` (string, required) − Provide the field to be extracted from the papers. This can be the main title (`title`), the abstract (`abstract`), or both (`title+abstract`). It can also be full articles only (`full`).
- `--max_results` (integer, required) − Set the maximum number of results to return.
- `--query` (string, required) − Provide the text to query the PubMed database.

## Run Instructions
Refer to the following sample command to run this connector code:

```
python3 pubmed-connector.py  --max_results 5 --query fever --email firstname.lastname@cnvrg.io --field title
```

## Outputs
The PubMed Connector library generates the following outputs:
- The connector library outputs one of the following formats depending on the run mode:
  - In the full-articles-only mode, the connector outputs a folder named `pdfs` containing the articles.
  - In other modes, the connector outputs a JSON file named `pubmed.json` containing the specified `fields`.
- The connector writes all files created to the default path `/cnvrg`.
- The user (optionally) stores the output file in a new or existing cnvrg dataset.

## Troubleshooting
Complete one or more of the following steps to troubleshoot issues that may be encountered with this connector:
- Confirm the user email address is valid.
- Check the Experiments > Artifacts section to confirm this connector has generated the output files.
- Check for an error code, which displays if the experiment fails. If so, quickly check the logs in the Experiments tab, as cnvrg provides limited Debug mode time to resolve the problem.

## Related Blueprints
The PubMed Connector can be used with the following blueprints:
- [PDF Extraction Batch](https://metacloud.cloud.cnvrg.io/marketplace/blueprints/pdf-extraction-batch/)
- [Text Summarization Batch](https://metacloud.cloud.cnvrg.io/marketplace/blueprints/text-summarization-batch/)
