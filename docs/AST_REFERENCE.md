# EnLang v2.0.0 AST Reference
==============================================================================

## Universal AST Nodes
All EnLang source code is parsed into a tree composed of these core nodes:
1. `ProgramNode(statements)`: Root node representing the file.
2. `AssignmentNode(target, value)`: Variable assignment or indexed mutation.
3. `DisplayNode(expression)`: Output evaluation node.
4. `InputNode(target, prompt)`: Interactive input capture node.
5. `FunctionDefNode(name, params, body, is_async)`: Function definition.
6. `FunctionCallNode(name, args)`: Function invocation expression/statement.
7. `ConditionalNode(branches, else_body)`: If/else conditional control flow.
8. `LoopNode(loop_type, target, iterable, body)`: Iterative loops (for each, repeat, while).
9. `ReturnNode(expression)`: Function return exit point.
10. `LiteralNode(value, type_tag)`: Primitives (number, string, boolean, null).
11. `VariableNode(name, index_expr, slice_expr)`: Symbol access with indexing or slicing.
12. `CollectionNode(coll_type, elements)`: Map or List constructor.
13. `CreateElementNode(tag, name, attributes)`: Frontend component node (`.enlgf`).
14. `StyleNode(selector, rules)`: Styling declaration node (`.enlgd`).
15. `TableNode(name, columns)`: Database table schema definition (`.enlgdb`).
