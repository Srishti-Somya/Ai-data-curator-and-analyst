# minor/nlp_backend/main.py

from file_utils import read_text_file, save_to_csv
from text_processing import chunk_text, extract_entities_and_relationships
from visualization import visualize_relationships, convert_to_table
import spacy
import os
import pandas as pd

# Load the transformer-based model
nlp = spacy.load("en_core_web_lg")

# Add necessary components to the pipeline if not already present
if "sentencizer" not in nlp.pipe_names:
    nlp.add_pipe("sentencizer")
if "parser" not in nlp.pipe_names:
    nlp.add_pipe("parser")

def process_nlp(file_path, columns_to_save=None):
    """
    Process NLP on the given file and generate CSV and SVG outputs.
    """
    print(f"Processing NLP for file: {file_path}")
    
    # Read the text file
    text_content = read_text_file(file_path)
    print(f"Text content length: {len(text_content)} characters")
    
    # Load spaCy model
    nlp = spacy.load("en_core_web_lg")
    
    # Increase max_length to handle longer texts
    nlp.max_length = 2000000  # 2 million characters
    
    # If text is too long, chunk it into smaller pieces
    if len(text_content) > 500000:  # 500k characters
        print("Text is very long, chunking into smaller pieces...")
        chunk_size = 400000  # 400k characters per chunk
        chunks = [text_content[i:i+chunk_size] for i in range(0, len(text_content), chunk_size)]
        print(f"Split text into {len(chunks)} chunks")
        
        all_entities = []
        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i+1}/{len(chunks)}...")
            chunk_entities = extract_entities_and_relationships(chunk, nlp)
            all_entities.extend(chunk_entities)
        
        entities = all_entities
    else:
        # Extract entities with improved extraction
        entities = extract_entities_and_relationships(text_content, nlp)
    print(f"Extracted {len(entities)} entities")
    
    # Group entities by type
    entity_groups = {}
    for entity in entities:
        label = entity['label']
        if label not in entity_groups:
            entity_groups[label] = []
        entity_groups[label].append(entity)
    
    # Create structured data for CSV
    structured_data = []
    
    # Create rows with meaningful entity combinations
    max_entities = max(len(entities) for entities in entity_groups.values()) if entity_groups else 0
    
    for i in range(max_entities):
        row = {}
        for label in ['PERSON', 'ORG', 'DATE', 'GPE', 'LOC', 'PRODUCT', 'VERSION', 'YEAR', 'EMAIL', 'URL', 'MONEY', 'PERCENT', 'TIME', 'QUANTITY', 'ORDINAL', 'CARDINAL', 'MISC']:
            if label in entity_groups and i < len(entity_groups[label]):
                row[label] = entity_groups[label][i]['text']
            else:
                row[label] = ""
        structured_data.append(row)
    
    # If no entities found, create at least one row
    if not structured_data:
        structured_data = [{'PERSON': '', 'ORG': '', 'DATE': '', 'GPE': '', 'LOC': '', 'PRODUCT': '', 'VERSION': '', 'YEAR': '', 'EMAIL': '', 'URL': '', 'MONEY': '', 'PERCENT': '', 'TIME': '', 'QUANTITY': '', 'ORDINAL': '', 'CARDINAL': '', 'MISC': ''}]
    
    # Convert to DataFrame
    df = pd.DataFrame(structured_data)
    
    # Filter columns based on user request
    if columns_to_save:
        # Map user-friendly names to actual column names
        column_mapping = {
            'Person': 'PERSON',
            'Org': 'ORG', 
            'Date': 'DATE',
            'Loc': 'GPE',  # Use GPE (Geo-Political Entity) for locations
            'Misc': 'MISC',
            'Money': 'MONEY',
            'Percent': 'PERCENT',
            'Time': 'TIME',
            'Quantity': 'QUANTITY',
            'Ordinal': 'ORDINAL',
            'Cardinal': 'CARDINAL',
            'Product': 'PRODUCT'
        }
        
        available_columns = []
        for col in columns_to_save:
            if col in column_mapping and column_mapping[col] in df.columns:
                available_columns.append(column_mapping[col])
        
        if available_columns:
            df = df[available_columns]
        else:
            # If requested columns not found, use default
            df = df[['PERSON', 'ORG', 'DATE', 'GPE']]
    else:
        # Default columns
        df = df[['PERSON', 'ORG', 'DATE', 'GPE']]
    
    # Ensure all requested columns exist
    if columns_to_save:
        for col in columns_to_save:
            if col not in df.columns:
                df[col] = ""
    
    # Save to CSV
    csv_path = "structured_data.csv"
    save_to_csv(df, csv_path, list(df.columns))
    print(f"CSV saved to: {csv_path}")
    print(f"CSV shape: {df.shape}")
    
    # Generate visualization
    svg_path = "relationships.svg"
    visualize_relationships(text_content, entities, svg_path)
    print(f"SVG saved to: {svg_path}")
    
    return {
        "csv_file": csv_path,
        "svg_file": svg_path,
        "entities_found": len(entities),
        "data_rows": len(df)
    }
