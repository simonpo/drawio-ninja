# Draw.io Templates

This directory contains minimal template files for draw.io diagram generation.

## Available Templates

- **basic-structure.drawio** - Minimal valid draw.io file with required root structure and no content. Use this as a starting point for understanding the essential XML skeleton.

## Official Draw.io Examples & Templates

For more comprehensive examples and templates, see the **official draw.io diagrams repository**:

**[jgraph/drawio-diagrams](https://github.com/jgraph/drawio-diagrams)**

This repository contains hundreds of production-quality diagrams demonstrating:

- **Advanced layouts** - Hierarchical, radial, organic, and orthogonal positioning patterns
- **Complex architectures** - Multi-tier systems, cloud infrastructure, network topologies
- **Professional styling** - Consistent color schemes, typography, visual hierarchy
- **Domain-specific patterns** - UML, BPMN, flowcharts, organizational charts, mind maps
- **Real-world examples** - Complete diagrams from actual use cases

### Key Locations in Official Repository

- **[/diagrams](https://github.com/jgraph/drawio-diagrams/tree/dev/diagrams)** - Core example diagrams
- **[/templates](https://github.com/jgraph/drawio-diagrams/tree/dev/templates)** - Reusable template files
- **Various subdirectories** - Examples organized by diagram type and use case

### How to Use Official Examples

1. Browse the repository to find diagrams similar to what you want to create
2. Download the `.drawio` or `.xml` file
3. Open in draw.io to study the structure, styling, and layout patterns
4. Use as reference when crafting prompts for GitHub Copilot

The official examples are authoritative references for:

- Proper spatial layout and spacing conventions
- Standard styling patterns for different diagram types
- Complex parent-child relationships and grouping
- Advanced mxGraph features and attributes

## Local Examples

This project also includes working examples in the `/examples` directory that demonstrate the instruction file's effectiveness at preventing common structural failures. These examples prioritize **structural validity** over visual perfection and serve as test cases for the validation script.

## Relationship to Instruction File

The templates and examples in this project focus on **structural correctness** - ensuring files open reliably in draw.io. The official jgraph repository provides guidance on **visual quality** - optimal layout, professional styling, and aesthetic consistency.

Together, they represent a complete resource for diagram generation.
