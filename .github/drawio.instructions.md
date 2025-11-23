---
description: 'Instructions that improve LLM generation of structurally valid draw.io XML files that open reliably'
applyTo: '**/*.drawio'
---

# Mandatory First Line in Every Generated File

Always begin every `.drawio` file with exactly this line:

```xml
<?xml version="1.0" encoding="UTF-8"?>
```

The rest of the file follows the progressive template structure below.

# Draw.io XML Generation Instructions

These instructions address structural errors in LLM-generated draw.io files by establishing structural, topological, and formatting requirements based on analysis of the mxGraph XML format and observed generation errors.

Recent research demonstrates that LLMs struggle with graph-structured data due to architectural constraints in modeling inter-node relationships (Guan et al., 2025). Additionally, empirical studies show that single-stage diagram generation achieves only 58% accuracy, with multi-stage refinement processes proving significantly more effective (Wei et al., 2024). These instructions compensate for those limitations through explicit structural templates and generation protocols.

**Scope:** These instructions focus on **structural validity** - ensuring generated XML files open reliably in draw.io. Layout optimization and visual aesthetics are separate concerns addressed in future work.

## ZERO-ERROR QUICK START

**Every .drawio file you generate MUST:**

1. **Start with the XML declaration (exact line):**
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   ```

2. **Use infinite canvas (never fixed page):**
   ```xml
   <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" page="0">
   ```
   ❌ NEVER use `page="1"` with `pageWidth`/`pageHeight`

3. **Include root structure (always):**
   ```xml
   <root>
     <mxCell id="0"/>
     <mxCell id="1" parent="0"/>
   ```

**DO:**
- Output ONLY raw XML (no markdown fences like ```xml or ```)
- Use sequential IDs starting at 2 (id="0" and id="1" are reserved)
- Create all vertices before any edges
- For multi-line labels: use `&#xa;` (XML entity) or `<br/>` when `style` contains `html=1`
- For single-line: use hyphens or spaces: `"User Service - Auth"`

**DON'T:**
- Add commentary, explanations, or disclaimers before/after the XML
- Use literal `\n` (backslash-n) in `value` attributes
- Put actual line breaks (physical newlines) inside `value="..."` attributes
- Wrap output in markdown code blocks
- Skip the XML declaration line

## Progressive Template Structure

### Stage 1: Minimal Valid Structure

Every draw.io file requires this foundational structure. Files missing the root cell (id="0") or default layer (id="1") will not open.

```drawio
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram name="Diagram">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" page="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

**Critical attributes:**
- `page="0"`: Creates infinite canvas for web use (not page="1" with fixed pageWidth/pageHeight)
- `id="0"`: Root cell with no parent
- `id="1"`: Default layer, parent of all visible elements

**Note:** All complete `.drawio` files must begin with the XML declaration `<?xml version="1.0" encoding="UTF-8"?>`. This is included in all complete examples below and should be present in generated files (omitted from inline fragments for brevity).

### Stage 2: Adding Vertices

Generate all vertices with sequential IDs before creating any edges. This prevents orphaned references.

```drawio
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram name="Diagram">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" page="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <mxCell id="2" value="Start" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="3" value="Process" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="100" y="200" width="120" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="4" value="End" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="100" y="300" width="120" height="60" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

**Required vertex attributes:**
- `id`: Unique sequential number
- `value`: Label text
- `style`: Semicolon-separated key=value pairs
- `vertex="1"`: Declares this is a vertex (shape)
- `parent="1"`: References the default layer
- `<mxGeometry>`: Must include `as="geometry"` attribute

### Stage 3: Complete Template with Edges

Only after all vertices exist, add edges that reference them. Edges must connect to valid vertex IDs.

```drawio
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram name="Diagram">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" page="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <mxCell id="2" value="Start" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="3" value="Process" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="100" y="200" width="120" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="4" value="End" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="100" y="300" width="120" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="5" edge="1" parent="1" source="2" target="3">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="6" edge="1" parent="1" source="3" target="4">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

**Required edge attributes:**
- `id`: Unique sequential number (continue from last vertex ID)
- `edge="1"`: Declares this is an edge (connection)
- `parent="1"`: References the default layer
- `source`: ID of source vertex (must exist)
- `target`: ID of target vertex (must exist)
- `<mxGeometry relative="1">`: Edge geometry uses relative positioning

## FINAL OUTPUT CHECKLIST (must all be true)

Before generating your final .drawio file, verify:

- [ ] First line is exactly: `<?xml version="1.0" encoding="UTF-8"?>`
- [ ] `<mxGraphModel>` has `page="0"` (infinite canvas)
- [ ] Root cells `id="0"` and `id="1" parent="0"` are present
- [ ] All cell IDs are unique sequential integers (2, 3, 4...)
- [ ] All vertices created before any edges
- [ ] Every edge `source` and `target` reference existing vertex IDs
- [ ] No literal `\n` (backslash-n) or physical newlines in `value` attributes
- [ ] Multi-line labels use `&#xa;` or `<br/>` (when `html=1` in style)
- [ ] No `<` or `>` except `<br/>` when `html=1` is in `style`
- [ ] Hex color values have NO quotes: `fillColor=#0078D4` not `fillColor="#0078D4"`
- [ ] No markdown code fences (```xml) wrapping the output
- [ ] No explanatory text before or after the XML

**Output ONLY raw XML starting with `<?xml version="1.0" encoding="UTF-8"?>`. Do not wrap in markdown. Do not add commentary.**

## NON-NEGOTIABLE RULES

### Rule 1: Always Include Root Structure

Files will not open without both root cells in this exact configuration.

```drawio
<mxCell id="0"/>
<mxCell id="1" parent="0"/>
```

**Why this fails:**
```drawio
<!-- WRONG: Missing root structure -->
<root>
  <mxCell id="2" value="Box" vertex="1">
    <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
  </mxCell>
</root>
```

### Rule 2: Use Sequential Numeric IDs Starting at 2

- `id="0"`: Reserved for root
- `id="1"`: Reserved for default layer
- `id="2"` onwards: Your content (vertices first, then edges)
- Never reuse IDs
- Never skip numbers in sequence

### Rule 3: Generate All Vertices Before Any Edges

This prevents orphaned edge references.

**Correct order:**
1. Root structure (id="0", id="1")
2. All vertices (id="2", id="3", id="4"...)
3. All edges (id="5", id="6", id="7"...)

**Why this fails:**
```drawio
<!-- WRONG: Edge created before target vertex exists -->
<mxCell id="2" value="Start" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
</mxCell>

<mxCell id="3" edge="1" parent="1" source="2" target="4">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<mxCell id="4" value="End" vertex="1" parent="1">
  <!-- Edge above references id="4" before it exists -->
  <mxGeometry x="100" y="200" width="120" height="60" as="geometry"/>
</mxCell>
```

### Rule 4: Every Cell Needs parent="1" Unless Grouped

All top-level vertices and edges must reference the default layer.

```drawio
<mxCell id="2" value="Box" vertex="1" parent="1">
```

For grouped cells, the parent is the group container's ID.

### Rule 5: Edges Must Reference Valid source and target IDs

Both source and target must be IDs of existing vertices.

```drawio
<mxCell id="5" edge="1" parent="1" source="2" target="3">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

Verify both id="2" and id="3" exist as vertices before creating this edge.

### Rule 6: Geometry Requires as="geometry" Attribute

```drawio
<mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
```

**Why this fails:**
```drawio
<!-- WRONG: Missing as="geometry" -->
<mxGeometry x="100" y="100" width="120" height="60"/>
```

### Rule 7: Use page="0" for Web Layouts

For diagrams embedded in documentation, use infinite canvas without page boundaries.

```drawio
<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" page="0">
```

**Avoid for web use:**
```drawio
<!-- WRONG for web: Fixed page size creates artificial constraints -->
<mxGraphModel page="1" pageScale="1" pageWidth="850" pageHeight="1100">
```

### Rule 8: Specify vertex="1" or edge="1" on Each Cell

Every cell after id="1" must declare its type.

```drawio
<mxCell id="2" value="Box" vertex="1" parent="1">  <!-- Shape -->
<mxCell id="3" edge="1" parent="1" source="2" target="4">  <!-- Connection -->
```

### Rule 9: Never Quote Hex Colour Values in Style Attributes

The style attribute is already quoted, so values inside must not use additional quotes.

```drawio
<!-- CORRECT: No quotes on hex values -->
<mxCell id="2" value="Box" style="fillColor=#0078D4;strokeColor=#001E4E" vertex="1" parent="1">
```

**Why this fails:**
```drawio
<!-- WRONG: Quote after = closes the style attribute prematurely -->
<mxCell id="2" value="Box" style="fillColor="#0078D4;strokeColor=#001E4E" vertex="1" parent="1">
<!--                              ↑ This quote ends style here, leaving #0078D4;strokeColor=#001E4E as invalid -->

<!-- WRONG: Inconsistent quoting breaks XML structure -->
<mxCell id="2" value="Box" style="fillColor="#e1d5e7;strokeColor=#9673a6" vertex="1" parent="1">
```

**Result:** File fails to open with "Not a diagram file" or "attributes construct error".

### Rule 10: Use Safe Characters in Labels

Prefer alphanumeric characters (letters, numbers), spaces, hyphens, and underscores in label values. Unicode text (Korean, Japanese, Chinese, emoji, etc.) is fully supported. Avoid these XML special characters: `& < > " '`

For common symbols, use word alternatives:
- Instead of `&`, use `and`
- Instead of `<`, use `less than` or `←`
- Instead of `>`, use `greater than` or `→`
- For multi-line text, use spaces or hyphens as separators, not newlines

```drawio
<!-- CORRECT: Word alternative for ampersand -->
<mxCell id="2" value="Search and Rescue" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
</mxCell>

<!-- CORRECT: Unicode text works perfectly -->
<mxCell id="3" value="データベース" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="250" y="100" width="120" height="60" as="geometry"/>
</mxCell>

<!-- CORRECT: Hyphen for multi-line concept -->
<mxCell id="4" value="User Service - Authentication" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="200" width="120" height="60" as="geometry"/>
</mxCell>
```

**Why this fails:**
```drawio
<!-- WRONG: Unescaped ampersand breaks XML parser -->
<mxCell id="2" value="Search & Rescue" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
<!--                      ↑ XML parser expects entity like &amp; -->

<!-- WRONG: Newline entity in attribute value -->
<mxCell id="3" value="User DB&#xa;(Primary)" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
<!--                    ↑ Invalid entity reference -->

<!-- WRONG: Less-than symbol -->
<mxCell id="4" value="Load < 50%" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
<!--                     ↑ Starts a tag, breaks parsing -->
```

**Result:** File fails with "xmlParseEntityRef: no name" or "attributes construct error".

## Style & Shape Library

| Shape | Style String | Dimensions | Use Case |
|-------|-------------|------------|----------|
| Rectangle | `rounded=0;whiteSpace=wrap;html=1;` | 120×60 | Process, component, generic box |
| Rounded Rectangle | `rounded=1;whiteSpace=wrap;html=1;` | 120×60 | Start/end, user action |
| Ellipse | `ellipse;whiteSpace=wrap;html=1;` | 100×100 | Event, state |
| Rhombus (Decision) | `rhombus;whiteSpace=wrap;html=1;` | 100×80 | Decision point, gateway |
| Hexagon | `shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;` | 120×80 | Preparation, configuration |
| Parallelogram | `shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;` | 120×60 | Input/output, data |
| Cylinder | `shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;` | 80×100 | Database, storage |
| Cloud | `ellipse;shape=cloud;whiteSpace=wrap;html=1;` | 140×100 | Cloud service, external system |
| Swimlane | `swimlane;whiteSpace=wrap;html=1;` | 200×200 | Grouping, lanes |
| Azure Cloud Service | `rounded=0;whiteSpace=wrap;html=1;fillColor=#0078D4;strokeColor=#001E4E;fontColor=#ffffff;` | 120×60 | Azure service (generic) |
| Azure Database | `shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;fillColor=#0078D4;strokeColor=#001E4E;fontColor=#ffffff;` | 80×100 | Azure SQL, databases |
| AWS Service | `rounded=0;whiteSpace=wrap;html=1;fillColor=#FF9900;strokeColor=#232F3E;fontColor=#232F3E;` | 120×60 | AWS service (generic) |

**Style syntax rules:**
- Semicolon-separated key=value pairs
- No spaces around equals signs
- **CRITICAL: Never quote hex colour values** - `fillColor=#0078D4` not `fillColor="#0078D4"`
- The style attribute itself uses quotes: `style="fillColor=#0078D4;strokeColor=#001E4E"`
- Nested quotes break XML parsing: `style="fillColor="#0078D4"` causes parse errors
- Common keys: shape, rounded, strokeColor, fillColor, fontColor, whiteSpace, html

## Colour Palettes

### Azure / Professional
```
fillColor=#0078D4;strokeColor=#001E4E;fontColor=#ffffff;
fillColor=#50E6FF;strokeColor=#0078D4;fontColor=#000000;
fillColor=#ffffff;strokeColor=#0078D4;fontColor=#0078D4;
```

### Success / Operational
```
fillColor=#107C10;strokeColor=#0E5A0E;fontColor=#ffffff;
fillColor=#5DB75D;strokeColor=#107C10;fontColor=#000000;
fillColor=#D5F5D5;strokeColor=#107C10;fontColor=#107C10;
```

### Warning / Error
```
fillColor=#D83B01;strokeColor=#8A2700;fontColor=#ffffff;
fillColor=#F7630C;strokeColor=#D83B01;fontColor=#000000;
fillColor=#FFE5D9;strokeColor=#D83B01;fontColor=#D83B01;
```

### Dark Mode
```
fillColor=#1E1E1E;strokeColor=#3E3E3E;fontColor=#FFFFFF;
fillColor=#2D2D2D;strokeColor=#555555;fontColor=#FFFFFF;
fillColor=#3E3E3E;strokeColor=#1E1E1E;fontColor=#CCCCCC;
```

## Prompts That Work Every Time

### Example 1: Minimal Flowchart

**Prompt:** "Create a simple 3-step flowchart: Start → Process Data → End"

```drawio
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram name="Simple Flowchart">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" page="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <mxCell id="2" value="Start" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="200" y="80" width="120" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="3" value="Process Data" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="200" y="180" width="120" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="4" value="End" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
          <mxGeometry x="200" y="280" width="120" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="5" edge="1" parent="1" source="2" target="3">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="6" edge="1" parent="1" source="3" target="4">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### Example 2: Network Hub-Spoke

**Prompt:** "Create a hub-and-spoke network diagram with central router and 4 connected devices"

```drawio
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram name="Network Diagram">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" page="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <mxCell id="2" value="Core Router" style="ellipse;whiteSpace=wrap;html=1;fillColor=#0078D4;strokeColor=#001E4E;fontColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="280" y="200" width="120" height="120" as="geometry"/>
        </mxCell>
        
        <mxCell id="3" value="Device 1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="100" y="80" width="100" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="4" value="Device 2" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="480" y="80" width="100" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="5" value="Device 3" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="100" y="380" width="100" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="6" value="Device 4" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="480" y="380" width="100" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="7" edge="1" parent="1" source="2" target="3">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="8" edge="1" parent="1" source="2" target="4">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="9" edge="1" parent="1" source="2" target="5">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="10" edge="1" parent="1" source="2" target="6">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### Example 3: Process Workflow with Decision

**Prompt:** "Create a workflow: Receive Request → Validate → Decision (Valid?) → Yes: Process → No: Reject → End"

```drawio
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram name="Workflow">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" page="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <mxCell id="2" value="Receive Request" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="200" y="40" width="120" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="3" value="Validate" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="200" y="140" width="120" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="4" value="Valid?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="220" y="240" width="80" height="80" as="geometry"/>
        </mxCell>
        
        <mxCell id="5" value="Process" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="80" y="360" width="120" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="6" value="Reject" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
          <mxGeometry x="320" y="360" width="120" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="7" value="End" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
          <mxGeometry x="200" y="480" width="120" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="8" edge="1" parent="1" source="2" target="3">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="9" edge="1" parent="1" source="3" target="4">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="10" value="Yes" edge="1" parent="1" source="4" target="5">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="11" value="No" edge="1" parent="1" source="4" target="6">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="12" edge="1" parent="1" source="5" target="7">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="13" edge="1" parent="1" source="6" target="7">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### Example 4: Azure Architecture

**Prompt:** "Create Azure architecture: Virtual Network containing Application Gateway → App Services → Azure SQL Database → Key Vault"

```drawio
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram name="Azure Architecture">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" page="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <mxCell id="2" value="Virtual Network" style="swimlane;whiteSpace=wrap;html=1;fillColor=#E6F3FF;strokeColor=#0078D4;fontColor=#0078D4;" vertex="1" parent="1">
          <mxGeometry x="40" y="40" width="600" height="400" as="geometry"/>
        </mxCell>
        
        <mxCell id="3" value="Application Gateway" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#0078D4;strokeColor=#001E4E;fontColor=#ffffff;" vertex="1" parent="2">
          <mxGeometry x="40" y="60" width="140" height="80" as="geometry"/>
        </mxCell>
        
        <mxCell id="4" value="App Services" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#0078D4;strokeColor=#001E4E;fontColor=#ffffff;" vertex="1" parent="2">
          <mxGeometry x="240" y="60" width="140" height="80" as="geometry"/>
        </mxCell>
        
        <mxCell id="5" value="Azure SQL Database" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;fillColor=#0078D4;strokeColor=#001E4E;fontColor=#ffffff;" vertex="1" parent="2">
          <mxGeometry x="260" y="220" width="100" height="120" as="geometry"/>
        </mxCell>
        
        <mxCell id="6" value="Key Vault" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#50E6FF;strokeColor=#0078D4;fontColor=#000000;" vertex="1" parent="2">
          <mxGeometry x="440" y="60" width="120" height="80" as="geometry"/>
        </mxCell>
        
        <mxCell id="7" value="" edge="1" parent="2" source="3" target="4">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="8" value="" edge="1" parent="2" source="4" target="5">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="9" value="" edge="1" parent="2" source="4" target="6">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## NEVER DO THESE

Common LLM failures that break draw.io files:

1. **Omitting root structure** - Files will not open without `id="0"` and `id="1" parent="0"`
2. **Reusing or skipping IDs** - Each cell must have a unique sequential ID
3. **Creating edges before vertices** - All source/target vertices must exist before edges reference them
4. **Using page="1" with pageWidth/pageHeight** - For web diagrams, use `page="0"` for infinite canvas
5. **Missing as="geometry"** - All `<mxGeometry>` elements require this attribute
6. **Circular parent references** - A cell cannot be its own ancestor in the parent chain
7. **Invalid source/target IDs** - Edge source and target must reference existing vertex IDs
8. **Forgetting vertex="1" or edge="1"** - Every cell must declare its type

## Final Reminder

When asked to create a .drawio file, output ONLY the raw XML. Do not wrap it in markdown code blocks. Do not add explanations before or after. The output must be valid XML that can be saved directly as a .drawio file.
