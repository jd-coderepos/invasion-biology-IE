# Full-text Retrieval for Invasion Biology WikiProject Publications

The [**scripts/invasion-biology-full_text-search.py**](https://github.com/jd-coderepos/invasion-biology-ask-dataset/blob/main/scripts/invasion-biology-full_text-search.py) queries the [ASK ORKG API](https://ask.orkg.org/) to retrieve metadata and full texts (where available) of publications listed in the [Invasion Biology WikiProject](https://www.wikidata.org/wiki/Wikidata:WikiProject_Invasion_biology). Specifically, it uses the [explore document GET request](https://api.ask.orkg.org/docs#tag/Semantic-Neural-Search/operation/explore_documents_index_explore_get), with each publication’s DOI as the document ID, to build a dataset for text data mining.

The source for these DOIs is a dataset of 49,716 publications, compiled from the Invasion Biology WikiProject published at DOI [10.5281/zenodo.12518036](https://www.doi.org/10.5281/zenodo.12518036).

### Output Data Files
1. [**data/publications-with-full_text.csv**](https://github.com/jd-coderepos/invasion-biology-ask-dataset/blob/main/data/publications-with-full_text.csv) – Contains records for publications where full text is available.
2. [**data/publications-no_full_text.csv**](https://github.com/jd-coderepos/invasion-biology-ask-dataset/blob/main/data/publications-no_full_text.csv) - Contains records for publications where the DOI is in the ASK datastore but the full text is not available.
3. [**data/publications-error_log.csv**](https://github.com/jd-coderepos/invasion-biology-ask-dataset/blob/main/data/publications-error_log.csv) – Contains records for publications whose DOIs were not found in the ASK datastore.


# Hypothesis-based Publication Retrieval

The [**scripts/hypothesis-search.py**](https://github.com/jd-coderepos/invasion-biology-ask-dataset/blob/main/scripts/hypothesis-search.py) uses the [ASK ORKG API’s](https://ask.orkg.org/) [semantic search GET request](https://api.ask.orkg.org/docs#tag/Semantic-Neural-Search/operation/semantic_search_index_search_get) to retrieve the top 50 publications relevant to a set of expert-curated hypotheses. These hypotheses are derived from the original dataset published at DOI [10.5281/zenodo.12518036](https://www.doi.org/10.5281/zenodo.12518036).

### Output File Structure
Each output record includes the following fields: `hypothesis`, `publication_id`, `title`, `doi`, `authors`, `year`, `abstract`, `full_text`, `subjects`, `topics`, `journals`, and `publisher`.

### Extracted Data Files
1. [**data/hypotheses-based-publications.csv**](https://github.com/jd-coderepos/invasion-biology-ask-dataset/blob/main/data/hypotheses-based-publications.csv) – Publications relevant to hypotheses, without date restrictions.
2. [**data/hypotheses-based-publications-after-2010.csv**](https://github.com/jd-coderepos/invasion-biology-ask-dataset/blob/main/data/hypotheses-based-publications-after-2010.csv) – Publications relevant to hypotheses, filtered to include only those published after 2010.

## Publications with Full Text Available by Hypothesis

| Hypothesis                                          | Publications (No Date Filter) | Publications (Post-2010) |
|-----------------------------------------------------|-------------------------------|---------------------------|
| Antarctic climate-diversity-invasion hypothesis     | 2                             | 3                         |
| Anthropogenically induced adaptation to invade      | 4                             | 2                         |
| Enhanced Mutualism Hypothesis                       | 4                             | 4                         |
| Intermediate Disturbance Hypothesis                 | 1                             | 1                         |
| Biotic Resistance Hypothesis                        | 0                             | 3                         |
| Disturbance Hypothesis                              | 2                             | 2                         |
| Enemy Release Hypothesis                            | 2                             | 0                         |
| Habitat Amount Hypothesis                           | 1                             | 2                         |
| Invasional Meltdown Hypothesis                      | 3                             | 5                         |
| Island Susceptibility Hypothesis                    | 2                             | 2                         |
| Limiting Similarity Hypothesis                      | 1                             | 0                         |
| Novel Weapons Hypothesis                            | 8                             | 6                         |
| Phenotypic Plasticity Hypothesis                    | 3                             | 3                         |
| Propagule Pressure Hypothesis                       | 2                             | 1                         |
| Tens Rule                                           | 2                             | 1                         |

## Publisher Summary for Hypothesis-based Publications Retrieved via ASK

1. [**meta-analysis/total_publisher_counts.csv**](https://github.com/jd-coderepos/invasion-biology-ask-dataset/blob/main/meta-analysis/total_publisher_counts.csv) – Summarizes publisher counts for publications without date restrictions.
2. [**meta-analysis/total_publisher_counts_after_2010.csv**](https://github.com/jd-coderepos/invasion-biology-ask-dataset/blob/main/meta-analysis/total_publisher_counts_after_2010.csv) – Summarizes publisher counts for publications published after 2010.

# Acknowledgements

This repository extends the original [Invasion Biology Corpus](https://zenodo.org/records/12518037), compiled from curated data within the [Invasion Biology WikiProject](https://www.wikidata.org/wiki/Wikidata:WikiProject_Invasion_biology), for text data mining applications.
