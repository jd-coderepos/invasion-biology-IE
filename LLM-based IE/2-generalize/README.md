### 🔬 Obtaining a Standardized Schema for Information Extraction (IE) from Scientific Papers

This folder contains resources for developing a standardized JSON schema to capture relationships between four key entities: **species**, **location**, **habitat**, and **ecosystem**, based on information extracted from scientific paper abstracts using GPT-4o.

#### Task Description

The task involves refining and standardizing schemas generated in stage 1 by prompting the LLM to review individual schemas for nine papers and propose a unified schema. The standardized schema is designed as a JSON data structure to capture relationships between entities and serve as the IE objective for extracting relevant information across the paper collection. 

To ensure robustness, the LLM was prompted three times with the same task: *"Read the nine schema instances and generate a standardized schema in the JSON output format."*

#### Folder Structure

- **`code/`**: Contains scripts for generating and processing standardized schemas.
- **`data/`**: Includes input schemas from the earlier stage and the resulting standardized schema.

#### Usage

Refer to the `code/` directory for scripts to replicate the standardization process and analyze the outputs.

