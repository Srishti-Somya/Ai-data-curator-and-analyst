from spacy import displacy
import pandas as pd

def visualize_relationships(text_content, entities, output_path="relationships.svg"):
    """
    Create a comprehensive visualization of entities and their relationships.
    """
    print(f"Creating visualization with {len(entities)} entities")
    
    if not entities:
        # Create a fallback SVG for empty content
        fallback_svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="400" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="#f8f9fa"/>
    <text x="400" y="200" text-anchor="middle" font-family="Arial, sans-serif" font-size="18" fill="#6c757d">
        No entities found in the processed content
    </text>
    <text x="400" y="230" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="#6c757d">
        Try a different query or check the scraped content
    </text>
</svg>'''
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(fallback_svg)
        return
    
    # Group entities by type
    entity_groups = {}
    for entity in entities:
        label = entity['label']
        if label not in entity_groups:
            entity_groups[label] = []
        entity_groups[label].append(entity)
    
    # Create SVG content
    svg_parts = []
    
    # Add CSS styles
    css_styles = '''
    <defs>
        <style>
            .entity-box { fill: #e3f2fd; stroke: #1976d2; stroke-width: 2; rx: 5; }
            .entity-text { font-family: Arial, sans-serif; font-size: 12px; fill: #1565c0; }
            .entity-label { font-family: Arial, sans-serif; font-size: 10px; fill: #666; }
            .relationship-line { stroke: #ff9800; stroke-width: 2; marker-end: url(#arrowhead); }
            .title { font-family: Arial, sans-serif; font-size: 20px; font-weight: bold; fill: #333; }
            .subtitle { font-family: Arial, sans-serif; font-size: 14px; fill: #666; }
        </style>
        <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="#ff9800" />
        </marker>
    </defs>
    '''
    
    svg_parts.append(css_styles)
    
    # Add title
    svg_parts.append('<text x="400" y="30" text-anchor="middle" class="title">Entity Analysis Results</text>')
    svg_parts.append(f'<text x="400" y="50" text-anchor="middle" class="subtitle">Found {len(entities)} entities across {len(entity_groups)} categories</text>')
    
    # Calculate layout
    margin = 80
    box_width = 200
    box_height = 60
    spacing = 20
    start_y = 100
    
    # Create entity boxes
    current_y = start_y
    for label, label_entities in entity_groups.items():
        # Add category title
        svg_parts.append(f'<text x="50" y="{current_y - 10}" class="entity-label" font-weight="bold">{label} ({len(label_entities)})</text>')
        
        # Add entity boxes
        for i, entity in enumerate(label_entities[:5]):  # Limit to 5 per category for readability
            x = 50 + (i * (box_width + spacing))
            y = current_y
            
            # Truncate long text
            display_text = entity['text'][:25] + "..." if len(entity['text']) > 25 else entity['text']
            
            svg_parts.append(f'<rect x="{x}" y="{y}" width="{box_width}" height="{box_height}" class="entity-box"/>')
            svg_parts.append(f'<text x="{x + 10}" y="{y + 20}" class="entity-text">{display_text}</text>')
            svg_parts.append(f'<text x="{x + 10}" y="{y + 35}" class="entity-label">{entity["description"]}</text>')
        
        current_y += box_height + spacing + 30
    
    # Calculate total height
    total_height = current_y + 50
    
    # Create final SVG
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1000" height="{total_height}" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="#ffffff"/>
    {''.join(svg_parts)}
</svg>'''
    
    # Save SVG
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print(f"Visualization saved to {output_path}")
    print(f"SVG size: {len(svg_content)} characters")

def convert_to_table(data):
    rows = []
    for entry in data:
        row = {
            "Person": ", ".join(entry["Person"]),
            "Org": ", ".join(entry["Org"]),
            "Date": ", ".join(entry["Date"]),
            "Loc": ", ".join(entry["Loc"]),
            "Misc": ", ".join(entry["Misc"]),
            "Money": ", ".join(entry["Money"]),
            "Percent": ", ".join(entry["Percent"]),
            "Time": ", ".join(entry["Time"]),
            "Quantity": ", ".join(entry["Quantity"]),
            "Ordinal": ", ".join(entry["Ordinal"]),
            "Cardinal": ", ".join(entry["Cardinal"]),
            "Product": ", ".join(entry["Product"]),
            "Relationships": "; ".join([f"{rel[0]} -> {rel[1]} -> {rel[2]}" for rel in entry["Relationships"]])
        }
        rows.append(row)
    df = pd.DataFrame(rows)
    return df