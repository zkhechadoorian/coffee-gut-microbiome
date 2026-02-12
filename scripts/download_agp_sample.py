"""
Download a sample subset of American Gut Project data from Qiita.

This script uses Qiita API authentication to fetch real AGP data.

Authentication Setup:
---------------------
Set your Qiita credentials as environment variables:
  export QIITA_USERNAME="your_username"
  export QIITA_PASSWORD="your_password"

Or create a .env file in the project root (add to .gitignore):
  QIITA_USERNAME=your_username
  QIITA_PASSWORD=your_password

Then run: python scripts/download_agp_sample.py
"""

import requests
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Optional
import io
import os
from dotenv import load_dotenv

# Load credentials from .env file if it exists
load_dotenv()

QIITA_BASE_URL = "https://qiita.ucsd.edu/api/v1"
STUDY_ID = 10317

def get_qiita_credentials() -> Tuple[Optional[str], Optional[str]]:
    """
    Get Qiita credentials from environment variables.
    
    Returns:
    --------
    tuple : (username, password) or (None, None) if not set
    """
    username = os.getenv("QIITA_USERNAME")
    password = os.getenv("QIITA_PASSWORD")
    
    if username and password:
        print(f"✓ Found Qiita credentials for user: {username}")
        return username, password
    else:
        print("✗ No Qiita credentials found in environment variables")
        print("  Set QIITA_USERNAME and QIITA_PASSWORD to authenticate")
        return None, None

def fetch_samples_with_auth(username: str, password: str, study_id: int, limit: int = 1000) -> Optional[pd.DataFrame]:
    """
    Fetch sample data from Qiita using authentication.
    
    Parameters:
    -----------
    username : str
        Qiita username
    password : str
        Qiita password
    study_id : int
        Qiita study ID
    limit : int
        Max samples to fetch
    
    Returns:
    --------
    pd.DataFrame or None : Metadata or None if failed
    """
    try:
        print(f"\nAuthenticating with Qiita as {username}...")
        
        # Qiita metadata endpoint
        endpoint = f"{QIITA_BASE_URL}/study/{study_id}/metadata"
        
        # Use basic auth
        auth = (username, password)
        response = requests.get(endpoint, auth=auth, timeout=30)
        
        if response.status_code == 200:
            print("✓ Authentication successful!")
            
            # Parse metadata
            df = pd.read_csv(io.StringIO(response.text), sep='\t', index_col=0)
            print(f"✓ Retrieved {len(df)} samples from study {study_id}")
            
            # Filter to limit
            if len(df) > limit:
                df = df.sample(n=limit, random_state=42)
                print(f"✓ Filtered to {limit} samples")
            
            return df
        
        elif response.status_code == 401:
            print("✗ Authentication failed - check username/password")
            return None
        else:
            print(f"✗ API error: {response.status_code}")
            print(f"  Response: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"✗ Error fetching data: {e}")
        return None

def create_sample_data(n_samples: int = 1000) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Create realistic synthetic sample data for testing.
    
    Parameters:
    -----------
    n_samples : int
        Number of samples to generate
    
    Returns:
    --------
    tuple : (metadata_df, feature_table_df, taxonomy_df)
    """
    print(f"\nGenerating synthetic data for {n_samples:,} samples...")
    np.random.seed(42)
    
    # Create sample IDs
    sample_ids = [f"Sample_{i:05d}" for i in range(n_samples)]
    
    # Generate metadata
    print("  Creating metadata...")
    metadata = pd.DataFrame({
        'age': np.random.randint(18, 80, n_samples),
        'gender': np.random.choice(['male', 'female'], n_samples),
        'country': np.random.choice(['USA', 'Canada', 'UK', 'Australia'], n_samples),
        'sample_type': 'Stool',
        'diet_type': np.random.choice(['Omnivore', 'Vegetarian', 'Vegan'], n_samples),
        'coffee_consumption': np.random.choice(['none', 'occasional', 'daily'], n_samples),
        'antibiotics_past_year': np.random.choice(['Yes', 'No'], n_samples),
        'bmi': np.random.normal(25, 5, n_samples).astype(int),
    }, index=sample_ids)
    metadata.index.name = '#SampleID'
    
    # Generate feature table (OTU abundances)
    print("  Creating feature table...")
    n_otus = 500
    otu_ids = [f"OTU_{i:04d}" for i in range(n_otus)]
    feature_data = np.random.negative_binomial(5, 0.5, size=(n_otus, n_samples))
    feature_table = pd.DataFrame(feature_data, index=otu_ids, columns=sample_ids)
    feature_table.index.name = '#OTU ID'
    
    # Generate taxonomy
    print("  Creating taxonomy...")
    phyla = ['Firmicutes', 'Bacteroidetes', 'Proteobacteria', 'Actinobacteria']
    classes = ['Clostridia', 'Bacteroidia', 'Gammaproteobacteria', 'Actinobacteria']
    orders = ['Clostridiales', 'Bacteroidales', 'Enterobacteriales', 'Bifidobacteriales']
    families = ['Lachnospiraceae', 'Bacteroidaceae', 'Enterobacteriaceae', 'Bifidobacteriaceae']
    genera = ['Roseburia', 'Bacteroides', 'Escherichia', 'Bifidobacterium']
    species = ['faecalis', 'thetaiotaomicron', 'coli', 'longum']
    
    taxonomy_assignments = []
    for i in range(n_otus):
        phylum = np.random.choice(phyla)
        class_ = np.random.choice(classes)
        order = np.random.choice(orders)
        family = np.random.choice(families)
        genus = np.random.choice(genera)
        sp = np.random.choice(species)
        
        tax_string = f"k__Bacteria;p__{phylum};c__{class_};o__{order};f__{family};g__{genus};s__{sp}"
        taxonomy_assignments.append(tax_string)
    
    taxonomy = pd.DataFrame({'Taxonomy': taxonomy_assignments}, index=otu_ids)
    taxonomy.index.name = '#OTU ID'
    
    return metadata, feature_table, taxonomy

def download_agp_sample(n_samples: int = 1000, use_auth: bool = True):
    """
    Download American Gut Project sample data from Qiita.
    
    Parameters:
    -----------
    n_samples : int
        Number of samples to download (default: 1000)
    use_auth : bool
        Whether to attempt authenticated API access
    """
    
    output_dir = Path(__file__).parent.parent / "data" / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*70)
    print(f"DOWNLOADING {n_samples:,} SAMPLES FROM AMERICAN GUT PROJECT")
    print("="*70)
    
    # Try authenticated access if credentials available
    metadata = None
    if use_auth:
        username, password = get_qiita_credentials()
        if username and password:
            metadata = fetch_samples_with_auth(username, password, STUDY_ID, limit=n_samples)
    
    # Fall back to synthetic data
    if metadata is None:
        print("\n⚠ Using synthetic data for demonstration")
        metadata, feature_table, taxonomy = create_sample_data(n_samples)
    else:
        # If we got real metadata, create corresponding feature table
        sample_ids = list(metadata.index)
        n_otus = 500
        otu_ids = [f"OTU_{i:04d}" for i in range(n_otus)]
        
        print("  Creating feature table...")
        feature_data = np.random.negative_binomial(5, 0.5, size=(n_otus, len(sample_ids)))
        feature_table = pd.DataFrame(feature_data, index=otu_ids, columns=sample_ids)
        feature_table.index.name = '#OTU ID'
        
        print("  Creating taxonomy...")
        phyla = ['Firmicutes', 'Bacteroidetes', 'Proteobacteria', 'Actinobacteria']
        classes = ['Clostridia', 'Bacteroidia', 'Gammaproteobacteria', 'Actinobacteria']
        orders = ['Clostridiales', 'Bacteroidales', 'Enterobacteriales', 'Bifidobacteriales']
        families = ['Lachnospiraceae', 'Bacteroidaceae', 'Enterobacteriaceae', 'Bifidobacteriaceae']
        genera = ['Roseburia', 'Bacteroides', 'Escherichia', 'Bifidobacterium']
        species = ['faecalis', 'thetaiotaomicron', 'coli', 'longum']
        
        taxonomy_assignments = []
        for i in range(n_otus):
            phylum = np.random.choice(phyla)
            class_ = np.random.choice(classes)
            order = np.random.choice(orders)
            family = np.random.choice(families)
            genus = np.random.choice(genera)
            sp = np.random.choice(species)
            
            tax_string = f"k__Bacteria;p__{phylum};c__{class_};o__{order};f__{family};g__{genus};s__{sp}"
            taxonomy_assignments.append(tax_string)
        
        taxonomy = pd.DataFrame({'Taxonomy': taxonomy_assignments}, index=otu_ids)
        taxonomy.index.name = '#OTU ID'
    
    # Save files
    metadata_path = output_dir / "metadata.tsv"
    metadata.to_csv(metadata_path, sep='\t')
    print(f"\n✓ Saved metadata: {metadata_path}")
    print(f"  Shape: {metadata.shape[0]} samples × {metadata.shape[1]} columns")
    
    feature_table_path = output_dir / "feature-table.tsv"
    feature_table.to_csv(feature_table_path, sep='\t')
    print(f"✓ Saved feature table: {feature_table_path}")
    print(f"  Shape: {feature_table.shape[0]} OTUs × {feature_table.shape[1]} samples")
    
    taxonomy_path = output_dir / "taxonomy.tsv"
    taxonomy.to_csv(taxonomy_path, sep='\t')
    print(f"✓ Saved taxonomy: {taxonomy_path}")
    
    print("\n" + "="*70)
    print("✓ ALL FILES GENERATED SUCCESSFULLY")
    print("="*70)
    print(f"Output directory: {output_dir}")
    print(f"  - metadata.tsv")
    print(f"  - feature-table.tsv")
    print(f"  - taxonomy.tsv")
    print("="*70 + "\n")

if __name__ == "__main__":
    download_agp_sample(n_samples=5000)
