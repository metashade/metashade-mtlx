# metashade-mtlx

This project prototypes extending [MaterialX](https://github.com/AcademySoftwareFoundation/MaterialX) shader code generation with [Metashade](https://github.com/metashade/metashade), a Pythonic shader EDSL.

## Node Implementations as a Plugin Mechanism

To understand how Metashade can extend MaterialX codegen, it is crucial to distinguish between MaterialX concepts of Node **Definitions** and Node **Implementations**.

* **NodeDef (`<nodedef>`):** The interface. It defines inputs, outputs, and types (e.g., `ND_burley_diffuse_bsdf`).
* **Implementation (`<implementation>`):** The logic. It points to source code or a nodegraph that implements the computations.

Crucially, **Implementations reference NodeDefs, not the other way around.**

This architecture allows Metashade to generate either new MaterialX node definitions complete with implementations, or new MaterialX node implementations for existing MaterialX nodes, without modifying the core MaterialX definitions.

## MaterialX Node Implementation Code Generation mechanisms

In order to understand how Metashade's codegen can integrate with MaterialX's, let's first discuss how MaterialX generates code for individual nodes.

MaterialX uses [4 different codegen approaches](https://github.com/AcademySoftwareFoundation/MaterialX/blob/main/documents/DeveloperGuide/ShaderGeneration.md#13-node-implementations):

1. **Inline Expression** — The node implementation is specified as a simple inline expression directly in the node definition. This is used for straightforward operations that can be expressed in a single line (e.g., `{{in1}} + {{in2}}` for an add node). The expression uses the target shading language syntax with input ports wrapped in double curly brackets.

2. **Shading Language Function** — The node is implemented as a function written in the target language (GLSL, OSL, etc.), with the source code stored in a separate file. The function signature matches the nodedef's interface of typed inputs and outputs.

3. **Nodegraph Implementation** — The node is implemented as a compound nodegraph composed of other nodes. This is useful for creating reusable compound operations or compatibility graphs for unknown/proprietary nodes.

4. **Dynamic Code Generation (C++)** — A C++ class derived from `ShaderNodeImpl` handles the implementation, emitting code programmatically during shader generation. This is used when static source code isn't sufficient — for example, when code needs to be customized based on node parameters, or when vertex streams and uniforms need to be created dynamically.

### Key Implementation Classes

The following diagram shows how the four code generation methods map to `ShaderNodeImpl` subclasses:

```mermaid
classDiagram
    class ShaderNodeImpl {
        +emitFunctionDefinition()
        +emitFunctionCall()
    }
    
    ShaderNodeImpl <|-- SourceCodeNode : "1. Inline + 2. Function"
    ShaderNodeImpl <|-- CompoundNode : "3. Nodegraph"
    ShaderNodeImpl <|-- CustomImpl : "4. Dynamic C++"
    
    note for SourceCodeNode "Reads .inline files or
    function source (.osl, .glsl)"
    note for CompoundNode "Wraps a nodegraph,
    recursively emits nodes"
    note for CustomImpl "User-defined subclass
    for dynamic code emission"
```
