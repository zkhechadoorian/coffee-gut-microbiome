# Coffee Consumption and the Gut Microbiome

This project investigates whether coffee consumption is associated with
differences in gut microbiome composition using data from the American Gut Project.

## Research Question
Do coffee drinkers exhibit differences in gut microbiome diversity or
specific bacterial taxa compared to non-coffee drinkers?

## Dataset
- American Gut Project (16S rRNA sequencing)
- Public feature tables, taxonomy, and metadata

The American Gut Project data was obtained from [Qiita](https://qiita.ucsd.edu/), Study ID 10317.

**Files downloaded:**
- `feature-table.tsv` - OTU/ASV abundance matrix (features × samples)
- `metadata.tsv` - Sample metadata including dietary and lifestyle information
- `taxonomy.tsv` - Taxonomic assignments for each feature

**Download steps:**
1. Create an account at https://qiita.ucsd.edu/
2. Navigate to Study 10317 (American Gut Project)
3. Access the study's processed data artifacts
4. Download the BIOM table and convert to TSV format, or download pre-processed TSV files
5. Download the sample information file (metadata)
6. Download the taxonomy assignments

Place all downloaded files in the `data/raw/` directory.



## Project Structure
- `data/` – raw and processed data
- `notebooks/` – exploratory analysis notebooks
- `src/` – reusable analysis functions
- `results/` – figures and summary tables

## Methods (Planned)
- Data quality control
- Metadata curation (coffee consumption definition)
- Alpha and beta diversity analysis
- Differential abundance testing

## Notes
This is an exploratory, observational analysis and does not imply causation.

