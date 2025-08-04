import spacy
from spacy import displacy
import re

def chunk_text(text, nlp):
    doc = nlp(text)
    chunks = []
    for sent in doc.sents:
        chunks.append(sent.text)
        print(f"Chunk: {sent.text}")  # Print each chunk
    return chunks

def extract_entities_and_relationships(text, nlp):
    """
    Extract entities and relationships from text using spaCy.
    Returns a list of dictionaries with entity information.
    """
    doc = nlp(text)
    entities = []
    
    # Extract named entities with more detailed information
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'ORG', 'DATE', 'LOC', 'GPE', 'FAC', 'PRODUCT', 'EVENT', 'MONEY', 'PERCENT', 'TIME', 'QUANTITY', 'ORDINAL', 'CARDINAL', 'MISC']:
            entity_info = {
                'text': ent.text.strip(),
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char,
                'description': spacy.explain(ent.label_),
                'sentiment': 'neutral',  # Could be enhanced with sentiment analysis
                'context': ent.sent.text.strip() if ent.sent else ""
            }
            entities.append(entity_info)
    
    # Extract additional entities using pattern matching
    additional_entities = extract_additional_entities(text)
    entities.extend(additional_entities)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_entities = []
    for entity in entities:
        entity_key = (entity['text'].lower(), entity['label'])
        if entity_key not in seen:
            seen.add(entity_key)
            unique_entities.append(entity)
    
    return unique_entities

def extract_additional_entities(text):
    """
    Extract additional entities using pattern matching and rules.
    """
    additional_entities = []
    
    # Extract email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    for match in re.finditer(email_pattern, text):
        additional_entities.append({
            'text': match.group(),
            'label': 'EMAIL',
            'start': match.start(),
            'end': match.end(),
            'description': 'Email address',
            'sentiment': 'neutral',
            'context': text[max(0, match.start()-50):match.end()+50]
        })
    
    # Extract URLs
    url_pattern = r'https?://[^\s]+'
    for match in re.finditer(url_pattern, text):
        additional_entities.append({
            'text': match.group(),
            'label': 'URL',
            'start': match.start(),
            'end': match.end(),
            'description': 'Website URL',
            'sentiment': 'neutral',
            'context': text[max(0, match.start()-50):match.end()+50]
        })
    
    # Extract version numbers (e.g., Python 3.13.5)
    version_pattern = r'\b[A-Za-z]+\s+\d+\.\d+(?:\.\d+)?\b'
    for match in re.finditer(version_pattern, text):
        additional_entities.append({
            'text': match.group(),
            'label': 'VERSION',
            'start': match.start(),
            'end': match.end(),
            'description': 'Software version',
            'sentiment': 'neutral',
            'context': text[max(0, match.start()-50):match.end()+50]
        })
    
    # Extract years
    year_pattern = r'\b(19|20)\d{2}\b'
    for match in re.finditer(year_pattern, text):
        additional_entities.append({
            'text': match.group(),
            'label': 'YEAR',
            'start': match.start(),
            'end': match.end(),
            'description': 'Year',
            'sentiment': 'neutral',
            'context': text[max(0, match.start()-50):match.end()+50]
        })
    
    return additional_entities

def extract_relationships(doc):
    relationships = []
    for token in doc:
        if token.dep_ in ("nsubj", "dobj", "pobj", "iobj"):
            subject = [w for w in token.head.lefts if w.dep_ == "nsubj"]
            if subject:
                subject = subject[0]
                relationships.append((subject.text, token.head.text, token.text))
    return relationships