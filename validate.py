#!/usr/bin/env python3
"""
Validation script for draw.io XML files.
Tests structural requirements identified in the research.
"""

import sys
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Tuple


def validate_drawio_file(filepath: Path) -> Tuple[bool, List[str]]:
    """
    Validate a draw.io file against structural requirements.
    
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    try:
        # Read file to check XML declaration
        with open(filepath, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if not first_line.startswith('<?xml'):
                errors.append("Missing XML declaration (<?xml version=\"1.0\" encoding=\"UTF-8\"?>)")
        
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        # Check 1: Root structure exists
        mxfile = root if root.tag == 'mxfile' else root.find('mxfile')
        if mxfile is None:
            errors.append("Missing <mxfile> root element")
            return False, errors
        
        diagram = mxfile.find('diagram')
        if diagram is None:
            errors.append("Missing <diagram> element")
            return False, errors
        
        model = diagram.find('mxGraphModel')
        if model is None:
            errors.append("Missing <mxGraphModel> element")
            return False, errors
        
        graph_root = model.find('root')
        if graph_root is None:
            errors.append("Missing <root> element")
            return False, errors
        
        # Check 2: Required root cells exist
        cells = {cell.get('id'): cell for cell in graph_root.findall('mxCell')}
        
        if '0' not in cells:
            errors.append("Missing root cell (id='0')")
        
        if '1' not in cells:
            errors.append("Missing default layer (id='1')")
        elif cells['1'].get('parent') != '0':
            errors.append("Default layer (id='1') must have parent='0'")
        
        # Check 3: All IDs are unique
        all_ids = [cell.get('id') for cell in graph_root.findall('mxCell')]
        if len(all_ids) != len(set(all_ids)):
            duplicates = [id for id in all_ids if all_ids.count(id) > 1]
            errors.append(f"Duplicate IDs found: {set(duplicates)}")
        
        # Check 4: All parent references are valid
        for cell in graph_root.findall('mxCell'):
            cell_id = cell.get('id')
            parent = cell.get('parent')
            
            if parent and parent not in cells:
                errors.append(f"Cell '{cell_id}' references non-existent parent '{parent}'")
        
        # Check 5: All edge source/target references are valid
        for cell in graph_root.findall('mxCell'):
            if cell.get('edge') == '1':
                cell_id = cell.get('id')
                source = cell.get('source')
                target = cell.get('target')
                
                if source and source not in cells:
                    errors.append(f"Edge '{cell_id}' references non-existent source '{source}'")
                
                if target and target not in cells:
                    errors.append(f"Edge '{cell_id}' references non-existent target '{target}'")
        
        # Check 6: All geometry elements have as="geometry"
        for cell in graph_root.findall('mxCell'):
            geometry = cell.find('mxGeometry')
            if geometry is not None and geometry.get('as') != 'geometry':
                cell_id = cell.get('id')
                errors.append(f"Cell '{cell_id}' geometry missing as='geometry' attribute")
        
        # Check 7: Page setting (warning, not error)
        page = model.get('page')
        if page == '1':
            errors.append("WARNING: page='1' with fixed dimensions - consider page='0' for web use")
        
        # Check 8: All content cells have vertex or edge attribute
        for cell in graph_root.findall('mxCell'):
            cell_id = cell.get('id')
            if cell_id not in ['0', '1']:
                if cell.get('vertex') != '1' and cell.get('edge') != '1':
                    errors.append(f"Cell '{cell_id}' missing vertex='1' or edge='1' attribute")
        
        # Check 9: Label values should not contain unescaped XML special characters
        # Pattern matches & not followed by valid entity (amp, lt, gt, quot, apos, or numeric)
        unsafe_char_pattern = re.compile(r'&(?!amp;|lt;|gt;|quot;|apos;|#\d+;|#x[0-9a-fA-F]+;)')
        for cell in graph_root.findall('mxCell'):
            cell_id = cell.get('id')
            value = cell.get('value', '')
            
            # Check for unescaped ampersand
            if unsafe_char_pattern.search(value):
                errors.append(f"Cell '{cell_id}' value contains unescaped '&' - use 'and' instead")
            
            # Check for other problematic characters
            if '<' in value:
                errors.append(f"Cell '{cell_id}' value contains '<' - use 'less than' instead")
            if '>' in value and not value.startswith('<') and not value.endswith('>'):
                # Allow > in HTML-like content but warn otherwise
                errors.append(f"WARNING: Cell '{cell_id}' value contains '>' - consider using 'greater than'")
            
            # Check for newline entities in attributes (common error)
            if '&#xa;' in value or '&#xA;' in value or '&#10;' in value:
                errors.append(f"Cell '{cell_id}' value contains newline entity - use hyphen or space instead")
        
    except ET.ParseError as e:
        errors.append(f"XML parsing error: {e}")
        return False, errors
    except Exception as e:
        errors.append(f"Unexpected error: {e}")
        return False, errors
    
    return len(errors) == 0, errors


def main():
    """Validate all draw.io files in examples directory."""
    
    script_dir = Path(__file__).parent
    examples_dir = script_dir / 'examples'
    
    if not examples_dir.exists():
        print(f"Error: {examples_dir} not found")
        sys.exit(1)
    
    # Support .drawio, .drawio.png, and .drawio.svg formats
    drawio_files = (list(examples_dir.glob('*.drawio')) + 
                    list(examples_dir.glob('*.drawio.png')) + 
                    list(examples_dir.glob('*.drawio.svg')))
    
    if not drawio_files:
        print(f"No .drawio, .drawio.png, or .drawio.svg files found in {examples_dir}")
        sys.exit(1)
    
    print(f"Validating {len(drawio_files)} draw.io files...\n")
    
    all_valid = True
    results = []
    
    for filepath in sorted(drawio_files):
        is_valid, errors = validate_drawio_file(filepath)
        results.append((filepath.name, is_valid, errors))
        
        if not is_valid:
            all_valid = False
    
    # Print results
    for filename, is_valid, errors in results:
        status = "✓ VALID" if is_valid else "✗ INVALID"
        print(f"{status}: {filename}")
        
        if errors:
            for error in errors:
                prefix = "  WARNING: " if error.startswith("WARNING") else "  ERROR: "
                print(f"{prefix}{error}")
            print()
    
    # Summary
    valid_count = sum(1 for _, is_valid, _ in results if is_valid)
    print(f"\nResults: {valid_count}/{len(results)} files valid")
    
    sys.exit(0 if all_valid else 1)


if __name__ == '__main__':
    main()
