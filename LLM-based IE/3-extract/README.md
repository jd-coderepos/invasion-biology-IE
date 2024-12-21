### 🤓 Conduct Information Extraction (IE) from Scientific Papers

This folder contains resources for extracting information from scientific papers using the GPT-4o LLM. The task focuses on mining four key entities—**species**, **location**, **habitat**, and **ecosystem**—and their relationships, guided by a standardized JSON schema.

#### Task Description

This stage fulfills the primary objective of extracting structured information from scientific papers. The system prompt for GPT-4o defines its role as a *"research assistant in invasion biology or ecology tasked with reading and understanding scientific papers to extract relevant information per the given predefined schema."*

The LLM was run over the entire corpus, completing the extraction process in approximately three days. The resulting dataset is released on [Zenodo](https://doi.org/10.5281/zenodo.13956882). 

#### Folder Structure

- **`code/`**: 
  - Scripts for running the GPT-4o model on individual papers or a bulk collection.
  - [Run extraction for a single paper](https://github.com/jd-coderepos/invasion-biology-IE/blob/main/LLM-based%20IE/3-extract/code/gpt-extract.py).
  - [Run extraction for a bulk collection](https://anonymous.4open.science/r/invasion-biology-IE-8658/LLM-based%20IE/3-extract/code/gpt-bulk-extract.py).
- **`data/`**: Contains the extracted JSON data structured according to the predefined schema.
- **`analysis/`**: Contains aggregated extraction data, such as unique species roles, habitats, locations, ecosystems, and relationships identified in the larger IE corpus released on Zenodo. This serves as a starting point for further exploration or curation of the dataset.


#### Usage

1. Use the scripts in the `code/` directory to extract information:
   - Run on a single paper or the entire collection.
2. Access the resulting dataset and analyze entity relationships using the JSON schema.

For additional details or to replicate the extraction process, refer to the provided scripts and dataset.
