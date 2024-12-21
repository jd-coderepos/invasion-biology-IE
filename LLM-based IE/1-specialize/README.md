### 🧐 Extracting Initial Schemas for Information Extraction (IE) from Scientific Paper Abstracts

This folder contains resources for a task focused on extracting initial schemas for Information Extraction (IE) from scientific paper abstracts using a Large Language Model (LLM), specifically GPT-4o. The extracted schemas relate key entities, including **species**, **location**, **habitat**, and **ecosystem**.

#### Task Description

- The LLM is prompted with a single paper at a time to generate a schema connecting the targeted entities.
- **10 unique papers** were selected for this task:
  - All 10 cases used the **title** and **abstract** of the paper for prompting.
  - In case 2, the **full text** of the paper was also used to enhance schema generation.

#### Folder Structure

- **`code/`**: Contains scripts for prompting the LLM and processing the extracted schemas.
- **`data/`**: Includes the input paper data (titles, abstracts, and full texts where applicable) and the resulting schemas.

#### Usage

Refer to the `code/` directory for scripts to replicate the schema extraction process and analyze the outputs.
