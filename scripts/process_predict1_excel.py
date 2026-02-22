#!/usr/bin/env python3
"""
Process Predict1 supplementary Excel file to extract microbiome and metadata

This script analyzes the downloaded Excel file to do the following:
1. List all available sheets and their structure
2. Identify which sheets contain microbiome data and metadata
3. Extract and save the relevant data for downstream analysis
4. Provide insights for subsequent analysis

Author: Zepyoor Khechadoorian
Date: 21-02-2026
"""

import pandas as pd
from pathlib import Path
import numpy as np

def setup_directories():
    """Create necessary directories"""
    raw_dir = Path("data/raw")
    processed_dir = Path("data/processed")
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)
    return raw_dir, processed_dir

def find_excel_file(data_dir):
    """Find the downloaded Excel file"""
    excel_files = list(data_dir.glob("*.xlsx")) + list(data_dir.glob("*.xls"))
    
    if not excel_files:
        print("❌ No Excel files found in data/raw/")
        print("Please move the downloaded supplementary Excel file to data/raw/")
        return None
    
    if len(excel_files) > 1:
        print("Multiple Excel files found:")
        for i, file in enumerate(excel_files):
            print(f"{i+1}. {file.name}")
        choice = input("Enter the number of the PREDICT1 file: ")
        return excel_files[int(choice)-1]
    
    return excel_files[0]

def explore_excel_sheets(excel_path):
    """Explore what sheets are available in the Excel file"""
    print(f"📊 Exploring Excel file: {excel_path.name}")
    print("="*50)
    
    # Read sheet names
    xlsx_file = pd.ExcelFile(excel_path)
    sheet_names = xlsx_file.sheet_names
    
    print(f"Found {len(sheet_names)} sheets:")
    for i, sheet in enumerate(sheet_names):
        print(f"{i+1}. {sheet}")
        
        # Try to peek at the first few rows
        try:
            df = pd.read_excel(excel_path, sheet_name=sheet, nrows=3)
            print(f"   Shape: {df.shape}")
            print(f"   Columns: {list(df.columns[:5])}{'...' if len(df.columns) > 5 else ''}")
        except Exception as e:
            print(f"   Error reading sheet: {e}")
        print()
    
    return sheet_names

def extract_microbiome_data(excel_path, sheet_names):
    """Extract microbiome abundance data from Excel sheets"""
    print("🔍 Looking for microbiome data...")
    
    microbiome_sheets = []
    metadata_sheets = []
    
    for sheet in sheet_names:
        sheet_lower = sheet.lower()
        if any(word in sheet_lower for word in ['otu', 'asv', 'abundance', 'microbiome', 'taxa', 'species']):
            microbiome_sheets.append(sheet)
        elif any(word in sheet_lower for word in ['metadata', 'sample', 'participant', 'demographic', 'diet']):
            metadata_sheets.append(sheet)
    
    print(f"📊 Potential microbiome sheets: {microbiome_sheets}")
    print(f"📋 Potential metadata sheets: {metadata_sheets}")
    
    return microbiome_sheets, metadata_sheets

def extract_coffee_data(excel_path, sheet_names):
    """Look for coffee consumption data specifically"""
    print("☕ Looking for coffee consumption data...")
    
    coffee_found = False
    
    for sheet in sheet_names:
        try:
            df = pd.read_excel(excel_path, sheet_name=sheet)
            
            # Look for coffee-related columns
            coffee_cols = [col for col in df.columns if 
                          any(word in str(col).lower() for word in ['coffee', 'caffeine', 'beverage'])]
            
            if coffee_cols:
                print(f"☕ Found coffee data in sheet '{sheet}':")
                for col in coffee_cols:
                    print(f"   - {col}")
                    if len(df[col].dropna()) > 0:
                        print(f"     Sample values: {df[col].dropna().head(3).tolist()}")
                coffee_found = True
                print()
                
        except Exception as e:
            continue
    
    if not coffee_found:
        print("❌ No obvious coffee columns found. Manual inspection needed.")

def main():
    """Main processing workflow"""
    print("PREDICT1 Excel File Processor")
    print("="*40)
    
    # Setup
    raw_dir, processed_dir = setup_directories()
    
    # Find Excel file
    excel_path = find_excel_file(raw_dir)
    if excel_path is None:
        return
    
    # Explore the file
    sheet_names = explore_excel_sheets(excel_path)
    
    # Look for specific data types
    microbiome_sheets, metadata_sheets = extract_microbiome_data(excel_path, sheet_names)
    extract_coffee_data(excel_path, sheet_names)
    
    print("="*60)
    print("NEXT STEPS")
    print("="*60)
    print("1. Review the sheet analysis above")
    print("2. Identify which sheets contain:")
    print("   - Microbiome abundance data (OTU/species counts)")
    print("   - Sample metadata (including coffee consumption)")
    print("3. Update the notebook to load the correct sheets")
    print("\n📝 Create a mapping like:")
    print("   feature_table_sheet = 'Sheet_Name_With_OTU_Data'")
    print("   metadata_sheet = 'Sheet_Name_With_Sample_Info'")

if __name__ == "__main__":
    main()