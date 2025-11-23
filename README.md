# drawio-ninja
A GitHub Copilot instruction file that improves LLM generation of structurally valid draw.io diagrams, informed by research on graph generation challenges in large language models.

## The Problem

Observation of LLM-generated draw.io files reveals consistent structural failures that prevent files from opening or rendering correctly. Recent research demonstrates that LLMs struggle with graph-structured data due to architectural limitations in modeling inter-node relationships [1]. These failures stem from three primary issues:

1. **Structural errors** - Missing required root cells, invalid parent references, non-unique IDs
2. **Graph topology failures** - Edges referencing non-existent vertices, circular parent chains, orphaned connections
3. **Layout biases** - Defaulting to fixed page sizes unsuitable for web documentation

## Technical Analysis

### Critical Structural Requirements

Draw.io files use the mxGraph XML format with mandatory hierarchical structure:

```
mxfile → diagram → mxGraphModel → root → cells
```

The root must contain exactly two foundation cells:
- `id="0"` - Root cell with no parent
- `id="1"` - Default layer with `parent="0"`

Files missing this structure will not open. LLMs may omit these invisible foundation elements when generating from scratch, as they are not explicitly represented in visual diagrams.

### Graph Topology Challenges

Draw.io diagrams represent directed graphs where:
- Vertices (shapes) are cells with `vertex="1"`
- Edges (connections) are cells with `edge="1"`, `source`, and `target` attributes
- Every cell requires a valid `parent` reference
- Edges must reference existing vertex IDs

LLMs demonstrate consistent difficulty maintaining referential integrity across these relationships. Common failures include:

- Creating edges before their source/target vertices exist (orphaned references)
- Reusing or skipping ID numbers (collisions and gaps)
- Missing parent attributes (cells fail to render)
- Invalid source/target IDs (edges disappear)

The sequential nature of LLM text generation conflicts with the bidirectional reference requirements of graph structures. Research shows that LLMs struggle to model inter-node relationships within graph structures due to inherent architectural constraints [1]. Furthermore, empirical studies demonstrate that achieving accurate diagrams in a single generation step remains a significant challenge, with even state-of-the-art models achieving only 58% accuracy on first attempts [2].

### Layout Bias Towards Print Formats

LLMs default to print-oriented layouts with fixed page dimensions:

```xml
<mxGraphModel page="1" pageScale="1" pageWidth="850" pageHeight="1100">
```

This creates visible page boundaries and artificial size constraints inappropriate for web documentation.

Web-optimized diagrams should use:

```xml
<mxGraphModel page="0" grid="1" gridSize="10">
```

This creates an infinite canvas that scales to content.

## The Solution

The `drawio.instructions.md` file provides GitHub Copilot with:

1. **Zero-Error Quick Start** - Prominent mandatory requirements (XML declaration, infinite canvas, root structure) with clear DO/DON'T list to prevent the most common generation failures
2. **Progressive template structure** - Three-stage demonstration of minimal structure → vertices → complete diagram
3. **Non-negotiable rules** - Ten specific requirements addressing observed failure modes
4. **Generation protocol** - Explicit vertex-before-edges ordering to prevent orphaned references
5. **Style library** - Ready-to-use shape definitions and colour palettes
6. **Working examples** - Four complete, validated diagrams from simple to complex
7. **Final output checklist** - Single authoritative pre-output verification covering all structural, formatting, and encoding requirements

See [CHANGELOG.md](CHANGELOG.md) for detailed history of instruction file improvements.

## Usage

### In GitHub Copilot Chat

The instruction file activates automatically when creating `.drawio` files in this repository. Simply ask:

```
Create a flowchart showing user authentication process
```

Copilot will follow the structural requirements and generate valid XML.

### Example Prompts

**Simple diagrams:**
- "Create a 3-step process flow"
- "Make a network diagram with hub and 4 spokes"

**Complex architectures:**
- "Create Azure architecture with VNet, App Gateway, App Services, SQL Database, and Key Vault"

### Validation

Open generated `.drawio` files in:
- **VS Code**: Install the Draw.io Integration extension
- **Web**: Upload to https://app.diagrams.net
- **Desktop**: Open with draw.io application

Valid files should:
- Open without errors
- Display all shapes and connections
- Use infinite canvas (no page boundaries)
- Maintain proper layout and spacing

## Cloud Provider Shape Libraries

### Enabling Azure Libraries in VS Code

The Draw.io Integration extension for VS Code includes Azure shape libraries by default. To use specific cloud provider shapes:

1. Open any `.drawio` file in VS Code
2. In the draw.io editor, click the shapes panel "+" button
3. Search for "Azure"
4. Select the relevant library (e.g., "Azure - Compute")

### Using Specific Shape Names

Once enabled, reference cloud provider shapes using the `shape` attribute:

**Azure shapes:**
```xml
<mxCell id="2" value="Virtual Machine" 
  style="shape=mxgraph.azure.compute.virtual_machine;fillColor=#0078D4;strokeColor=#ffffff;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="50" height="50" as="geometry"/>
</mxCell>
```

**Note:** The instruction file uses generic styled shapes that work without specific libraries, ensuring compatibility. For production architecture diagrams, consider using official cloud provider shapes for authenticity.

## Common Failure Examples

### Failure 1: Missing Root Structure

**Broken XML:**
```xml
<mxfile host="app.diagrams.net">
  <diagram name="Broken">
    <mxGraphModel>
      <root>
        <!-- Missing id="0" and id="1" -->
        <mxCell id="2" value="Box" vertex="1">
          <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

**Result:** File fails to open with "Invalid file structure" error.

**Fix:** Always include root cells:
```xml
<root>
  <mxCell id="0"/>
  <mxCell id="1" parent="0"/>
  <!-- Content here -->
</root>
```

### Failure 2: Orphaned Edge References

**Broken XML:**
```xml
<mxCell id="2" value="Start" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
</mxCell>

<mxCell id="3" edge="1" parent="1" source="2" target="5">
  <!-- References id="5" which doesn't exist yet -->
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<mxCell id="4" value="End" vertex="1" parent="1">
  <mxGeometry x="100" y="200" width="120" height="60" as="geometry"/>
</mxCell>
```

**Result:** Edge disappears or causes rendering errors.

**Fix:** Generate all vertices before edges, ensure target exists:
```xml
<!-- All vertices first -->
<mxCell id="2" value="Start" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
</mxCell>
<mxCell id="3" value="End" vertex="1" parent="1">
  <mxGeometry x="100" y="200" width="120" height="60" as="geometry"/>
</mxCell>

<!-- Edges second, with valid references -->
<mxCell id="4" edge="1" parent="1" source="2" target="3">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### Failure 3: Fixed Page Size for Web Diagrams

**Suboptimal XML:**
```xml
<mxGraphModel page="1" pageScale="1" pageWidth="850" pageHeight="1100">
```

**Result:** Diagram confined to A4-sized page with scroll bars, looks cramped in web documentation.

**Fix:** Use infinite canvas for web:
```xml
<mxGraphModel page="0" grid="1" gridSize="10">
```

## Testing

The `examples/` directory contains test diagrams of increasing complexity:

- **simple-flowchart.drawio** - Basic 3-node linear flow
- **network-diagram.drawio** - Hub-spoke topology with multiple edges
- **workflow-decision.drawio** - Branching logic with decision points
- **azure-architecture.drawio** - Multi-layer architecture with containers
- **complex-microservices.drawio** - 34-cell diagram with 16 edges testing ID management
- **nested-architecture.drawio** - 3-level nested groups testing parent references

Each diagram validates specific aspects of the instruction file requirements and tests failure modes observed during development.

### Automated Validation

**Setup:**
```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run validation
python validate.py examples/simple-flowchart.drawio
```

**Validation checks:**
- XML declaration present as first line
- Root structure (id="0" and id="1") exists
- All IDs are unique
- All parent references are valid
- All edge source/target IDs exist
- Geometry elements have `as="geometry"` attribute
- Cell type attributes (vertex/edge) are present
- No literal `\n` sequences in value attributes
- Multi-line value attributes flagged (should be single-line with entities)
- `<br/>` tags validated against `html=1` requirement
- Page settings (warns about fixed page sizes)

All example diagrams pass validation, demonstrating the instruction file's effectiveness at preventing common LLM failures. Our validation rules are informed by structural patterns observed in the [official draw.io diagrams repository](https://github.com/jgraph/drawio-diagrams), ensuring alignment with authoritative implementations from the draw.io creators.

## Project Structure

```
.github/
  drawio.instructions.md             # Main instruction file
  instructions.instructions.md       # Meta-instructions for writing instructions
  markdown.instructions.md           # Markdown formatting standards
docs/
  reference/                         # Reference materials (gitignored)
examples/
  *.drawio                           # Test diagrams
templates/
  basic-structure.drawio             # Minimal valid template
validate.py                          # Structural validation script
requirements.txt                     # Python dependencies (none currently)
requirements-dev.txt                 # Development dependencies
CONTRIBUTING.md                      # Development setup guide
README.md                            # This file
```

## Limitations

The instruction file cannot guarantee:

- **Optimal spatial layout** - LLMs lack inherent spatial reasoning; coordinates may require adjustment
- **Complex nested hierarchies** - Groups within groups beyond 2-3 levels may have parent reference errors
- **XML special character handling** - LLMs may use unescaped `&` or stray `<`, `>` in labels, causing XML parse errors. The instruction file recommends word alternatives ("and" instead of "&") and validates against these patterns
- **Style consistency** - Colour choices and styling may vary between generations
- **Large diagrams** - Graphs with >20 nodes risk ID tracking failures despite instructions

For production diagrams, validate structure and test in draw.io. The validator detects common encoding and structural issues automatically.

## Future Work: Multi-Stage Diagram Workflow

While this instruction file successfully generates **structurally valid** diagrams (as demonstrated by our validation script testing 8 structural requirements), recent research on text-to-diagram generation reveals inherent limitations in single-stage approaches [2].

### Current Scope: Structural Validity

The `drawio.instructions.md` file focuses on preventing XML parsing errors and ensuring draw.io can open files reliably. Our validation confirms this works:

- ✅ Root structure correctly formed
- ✅ Unique sequential IDs maintained
- ✅ Valid parent references throughout
- ✅ Edges reference existing vertices
- ✅ Required geometry attributes present

However, structural validity does not guarantee optimal **visual presentation**.

### Identified Limitation: Spatial Layout

Wei et al.'s DiagramAgent research demonstrates that diagram generation requires multiple refinement stages to achieve both logical correctness and visual quality. Their multi-agent architecture separates concerns:

1. **Plan Agent** - Interprets user intent
2. **Code Agent** - Generates diagram structure
3. **Check Agent** - Validates and debugs
4. **Diagram-to-Code Agent** - Enables iterative refinement

Critically, their findings show that "diagram editing...is comparatively easier" than generation from scratch, with editing tasks achieving 98% accuracy compared to 58% for initial generation. This suggests a two-stage approach would be more effective than attempting perfect single-pass generation.

### Proposed Second Stage: `drawio-prettifier.instructions.md`

A future instruction file could handle visual refinement as a separate concern:

**Input:** Structurally valid `.drawio` file from first stage  
**Output:** Visually optimized diagram with improved:

- **Spatial layout** - Proper spacing, alignment, symmetry
- **Visual hierarchy** - Size relationships, grouping, emphasis
- **Aesthetic consistency** - Unified colour schemes, typography, styling
- **Layout algorithms** - Automatic positioning based on diagram type (hierarchical, radial, force-directed)

**Key principle:** Preserve validated XML structure while transforming only coordinate and style attributes.

### Separation of Concerns Benefits

1. **Reduced cognitive load** - Each stage solves one problem well
2. **Higher success rate** - Two simpler tasks easier than one complex task
3. **Iterative refinement** - Users can regenerate layout without revalidating structure
4. **Testability** - Each stage has clear success criteria

This aligns with Wei et al.'s observation that "challenges persist in diagram generation, where achieving consistent and precise coding remains critical" - by separating structural generation from visual refinement, we address these challenges incrementally.

### Implementation Considerations

Before developing the prettifier:

1. **Gather layout failure examples** - Collect structurally valid but poorly laid out diagrams
2. **Define quality metrics** - Establish measurable criteria for "good" layout
3. **Analyze reference implementations** - Study spatial patterns in the [official draw.io diagrams repository](https://github.com/jgraph/drawio-diagrams) to learn layout conventions
4. **Research layout algorithms** - Investigate force-directed, hierarchical, and orthogonal approaches
5. **Test compatibility** - Ensure coordinate transformations preserve structural validity

The official draw.io examples provide an authoritative corpus for understanding how the draw.io team approaches spatial layout, styling consistency, and visual hierarchy - valuable guidance for developing automated prettification.

This future work would transform the project from a **structural validator** into a complete **diagram generation pipeline**.

## Troubleshooting Generated Diagrams

**You will likely still encounter errors** despite using the instruction file. LLMs can make subtle XML syntax mistakes that break the parser. Common issues include:

### Error: "Not a diagram file" or "Cannot read properties of null"

This indicates malformed XML. Common causes:

1. **Mismatched quotes in style attributes**
   ```xml
   <!-- WRONG: Quote inside quoted attribute -->
   style="fillColor="#e1d5e7;strokeColor=#9673a6"
   
   <!-- CORRECT: No quotes on hex values -->
   style="fillColor=#e1d5e7;strokeColor=#9673a6"
   ```

2. **Invalid XML characters in values**
   - Unescaped `&` characters (use word "and" instead)
   - Stray `<` or `>` not part of valid `<br/>` tags
   - Use `&#xa;` for line breaks in multi-line labels
   - `<br/>` requires `html=1` in the style attribute

3. **Missing required attributes**
   - Check `as="geometry"` is present on all `<mxGeometry>` elements
   - Verify `vertex="1"` or `edge="1"` on all cells except id="0" and id="1"

### How to Debug

1. **Copy the broken file** to `badexamples/` directory before fixing
2. **Open in a text editor** and check the error line number if provided
3. **Compare with working examples** in the `examples/` directory
4. **Run validation script** to check structural requirements:
   ```bash
   python3 validate.py
   ```
5. **Look for common patterns**:
   - Mismatched quotes
   - Duplicate IDs
   - Missing parent references
   - Edges referencing non-existent vertices

### Reporting Issues

If you find a recurring error pattern that the instruction file doesn't prevent, please open a GitHub issue with:

1. **The broken diagram file** (attach the `.drawio` file or paste XML)
2. **The exact error message** from draw.io
3. **The prompt you used** to generate the diagram
4. **What you changed to fix it** (if you've identified the issue)
5. **Suggestion for instruction file improvement** (optional)

This helps identify gaps in the instruction file so we can add rules or examples to prevent similar failures.

**Known patterns we're tracking:**
- Nested quote issues in style attributes
- HTML entity encoding in label text
- Colour value quoting inconsistencies

Your bug reports improve the instruction file for everyone.

## Contributing

Improvements to the instruction file should:

1. Address documented failure modes
2. Include working examples demonstrating the fix
3. Maintain compatibility with draw.io XML specification
4. Be tested with GitHub Copilot before submission

All notable changes are documented in [CHANGELOG.md](CHANGELOG.md) following [Keep a Changelog](https://keepachangelog.com/) format.

## References

1. Guan, Z., Wu, L., Zhao, H., He, M., & Fan, J. (2025). Attention Mechanisms Perspective: Exploring LLM Processing of Graph-Structured Data. *arXiv preprint arXiv:2505.02130*. https://arxiv.org/abs/2505.02130

2. Wei, J., Tan, C., Chen, Q., Wu, G., Li, S., Gao, Z., Sun, L., Yu, B., & Guo, R. (2024). From Words to Structured Visuals: A Benchmark and Framework for Text-to-Diagram Generation and Editing. *arXiv preprint arXiv:2411.11916*. https://arxiv.org/abs/2411.11916

- [Official draw.io Diagrams Repository](https://github.com/jgraph/drawio-diagrams) - Reference implementations from jgraph
- [mxGraph Documentation](https://jgraph.github.io/mxgraph/)
- [Draw.io XML Format](https://desk.draw.io/support/solutions/articles/16000042487)
- [GitHub Copilot Custom Instructions](https://code.visualstudio.com/docs/copilot/customization)

## Acknowledgements

This project stands on the shoulders of:

- **[jgraph](https://github.com/jgraph)** - For creating and maintaining draw.io, the diagramming tool this project supports
- **[awesome-copilot](https://github.com/myHerbAI/awesome-copilot)** - For the meta-instruction files (`instructions.instructions.md` and `markdown.instructions.md`) that provided the scaffolding for building effective GitHub Copilot custom instructions
- **[Draw.io Integration](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio)** - Henning Dieterichs' unofficial VS Code extension that makes editing draw.io diagrams seamless within the editor

Without these foundations, this project wouldn't exist. *Chapeau* to all.

## License

MIT License - see [LICENSE](LICENSE) file for details.

This project is open source and freely available for use, modification, and distribution. Draw your diagrams with confidence.