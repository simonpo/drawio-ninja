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
        # Read entire file for raw text scanning
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.splitlines()
        
        # Check 0a: XML declaration must be first line
        if not lines or not lines[0].strip().startswith('<?xml'):
            errors.append("Missing XML declaration (<?xml version=\"1.0\" encoding=\"UTF-8\"?>)")
        
        # Check 0b: Detect literal backslash-n sequences in value attributes
        literal_backslash_n_pattern = re.compile(r'value="[^"]*\\n[^"]*"')
        if literal_backslash_n_pattern.search(content):
            errors.append("Found literal '\\n' in value attribute - use XML entity &#xa; or <br/> with html=1")
        
        # Check 0d: Detect multi-line value attributes (opening quote and closing quote on different lines)
        for i, line in enumerate(lines, 1):
            # Look for value=" without closing " on same line
            if 'value="' in line:
                # Count quotes after value=
                value_start = line.find('value="')
                after_value = line[value_start + 7:]  # Skip 'value="'
                # If we don't find a closing quote (or only find escaped quotes), it's multi-line
                if '"' not in after_value or after_value.count('"') < 1:
                    errors.append(f"Line {i}: Multi-line value attribute detected - keep value on single line")
        
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
        
        # Check 9: Label values should not contain unescaped XML special characters or use <br/> incorrectly
        # Pattern matches & not followed by valid entity (amp, lt, gt, quot, apos, or numeric)
        unsafe_char_pattern = re.compile(r'&(?!amp;|lt;|gt;|quot;|apos;|#\d+;|#x[0-9a-fA-F]+;)')
        for cell in graph_root.findall('mxCell'):
            cell_id = cell.get('id')
            value = cell.get('value', '')
            style = cell.get('style', '')
            
            # Check for unescaped ampersand
            if unsafe_char_pattern.search(value):
                errors.append(f"Cell '{cell_id}' value contains unescaped '&' - use 'and' instead")
            
            # Check for < and > with proper <br/> handling
            has_html = 'html=1' in style
            
            if '<' in value:
                # If html=1, allow only <br/> or <br> tags
                if has_html:
                    # Remove valid <br/> and <br> tags, then check for remaining <
                    cleaned = re.sub(r'<br\s*/?>','', value, flags=re.IGNORECASE)
                    if '<' in cleaned:
                        errors.append(f"Cell '{cell_id}' value contains '<' other than <br/> - use 'less than' instead")
                else:
                    errors.append(f"Cell '{cell_id}' value contains '<' without html=1 in style - use 'less than' or add html=1")
            
            if '>' in value and not value.startswith('<') and not value.endswith('>'):
                # Allow > in HTML-like content but warn otherwise
                if not has_html:
                    errors.append(f"WARNING: Cell '{cell_id}' value contains '>' - consider using 'greater than'")
        
    except ET.ParseError as e:
        errors.append(f"XML parsing error: {e}")
        return False, errors
    except Exception as e:
        errors.append(f"Unexpected error: {e}")
        return False, errors
    
    return len(errors) == 0, errors


def main():
    """Validate all draw.io files in examples directory or specified files."""
    
    script_dir = Path(__file__).parent
    
    # Accept files from command line or default to examples directory
    if len(sys.argv) > 1:
        # Validate specified files
        drawio_files = []
        for arg in sys.argv[1:]:
            path = Path(arg)
            if path.is_file():
                drawio_files.append(path)
            elif path.is_dir():
                drawio_files.extend(list(path.glob('*.drawio')))
                drawio_files.extend(list(path.glob('*.drawio.png')))
                drawio_files.extend(list(path.glob('*.drawio.svg')))
            else:
                print(f"Warning: {arg} not found, skipping")
    else:
        # Default to examples directory
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
