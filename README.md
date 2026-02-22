# Coffee Consumption and the Gut Microbiome

This project investigates whether coffee consumption is associated with
differences in gut microbiome composition using data from the ZOE PREDICT1 study. 
My goal is to reproduce the findings mentioned in the following research paper:
https://www.nature.com/articles/s41564-024-01858-9. 

## Research Question
Do coffee drinkers exhibit differences in gut microbiome diversity or
specific bacterial taxa compared to non-coffee drinkers?

## Dataset: ZOE PREDICT1 ✅

This dataset is hosted at the following URL:
https://www.ebi.ac.uk/ena/browser/view/PRJEB39223?show=reads

However, for the purposes of my study, I chose to download the supplementary data 
provided in the Nature Medicine article. More information is summarized below.

**Source:** Nature Medicine supplementary data  
**Paper:** "Microbiome connections with host metabolism and habitual diet from 1,098 deeply phenotyped individuals"  
**DOI:** 10.1038/s41591-020-01183-8  
**ENA Project:** PRJEB39223

### Data Downloaded:
- ✅ Supplementary Excel file (.xlsx) from Nature Medicine
- Contains processed microbiome and dietary data
- ~1,000 participants with detailed coffee consumption data

**Files:**
- Place the downloaded `.xlsx` file in `data/raw/`
- Will be processed to extract microbiome abundance tables and metadata

## Project Structure
- `data/` – raw and processed data
- `notebooks/` – exploratory analysis notebooks
- `src/` – reusable analysis functions
- `results/` – figures and summary tables

## Methods (Planned)
- Data quality control
- Coffee consumption categorization  
- Alpha and beta diversity analysis
- Differential abundance testing

## References
- Asnicar et al. (2021) Nature Medicine - DOI: 10.1038/s41591-020-01183-8
- Berry et al. (2020) Nature Medicine - DOI: 10.1038/s41591-020-0934-0

## Notes
This is an exploratory, observational analysis and does not imply causation.
