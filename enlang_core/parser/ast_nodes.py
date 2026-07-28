"""Universal First-Class Abstract Syntax Tree (AST) for EnLang v2.0.0."""

class ASTNode:
    """Base class for all EnLang AST nodes."""
    def __init__(self, line_num=0):
        self.line_num = line_num

    def to_dict(self):
        """Convert AST node to serializable dictionary representation."""
        res = {"type": self.__class__.__name__, "line": self.line_num}
        for k, v in self.__dict__.items():
            if k == "line_num":
                continue
            if isinstance(v, ASTNode):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [i.to_dict() if isinstance(i, ASTNode) else i for i in v]
            elif isinstance(v, dict):
                res[k] = {ik: iv.to_dict() if isinstance(iv, ASTNode) else iv for ik, iv in v.items()}
            else:
                res[k] = v
        return res

class ProgramNode(ASTNode):
    """Root node representing an entire EnLang script/module."""
    def __init__(self, statements=None, line_num=0):
        super().__init__(line_num)
        self.statements = statements or []

class AssignmentNode(ASTNode):
    """Variable assignment or mutation node (e.g., set x to 10 or set x[i] to 20)."""
    def __init__(self, target, value, line_num=0):
        super().__init__(line_num)
        self.target = target
        self.value = value

class DisplayNode(ASTNode):
    """Console print/display statement node."""
    def __init__(self, expression, line_num=0):
        super().__init__(line_num)
        self.expression = expression

class InputNode(ASTNode):
    """Interactive input prompt node."""
    def __init__(self, target, prompt_expr, line_num=0):
        super().__init__(line_num)
        self.target = target
        self.prompt_expr = prompt_expr

class FunctionDefNode(ASTNode):
    """Function definition node with optional parameters and body."""
    def __init__(self, name, params=None, body=None, is_async=False, line_num=0):
        super().__init__(line_num)
        self.name = name
        self.params = params or []
        self.body = body or []
        self.is_async = is_async

class FunctionCallNode(ASTNode):
    """Function call expression or statement node."""
    def __init__(self, name, args=None, line_num=0):
        super().__init__(line_num)
        self.name = name
        self.args = args or []

class ReturnNode(ASTNode):
    """Return statement node."""
    def __init__(self, expression=None, line_num=0):
        super().__init__(line_num)
        self.expression = expression

class ConditionalNode(ASTNode):
    """If / Else If / Else branch node."""
    def __init__(self, branches=None, else_body=None, line_num=0):
        super().__init__(line_num)
        # branches is a list of tuples: (condition_expr, body_statements)
        self.branches = branches or []
        self.else_body = else_body or []

class LoopNode(ASTNode):
    """Universal loop node (for each, repeat, while)."""
    def __init__(self, loop_type, target=None, iterable=None, body=None, line_num=0):
        super().__init__(line_num)
        self.loop_type = loop_type  # 'foreach', 'repeat', 'while', 'range'
        self.target = target        # variable name in loop
        self.iterable = iterable    # list/range expression or repeat count
        self.body = body or []

class LiteralNode(ASTNode):
    """Primitive literal value node (Number, String, Boolean, Null)."""
    def __init__(self, value, type_tag, line_num=0):
        super().__init__(line_num)
        self.value = value
        self.type_tag = type_tag    # 'number', 'string', 'boolean', 'null'

class VariableNode(ASTNode):
    """Variable symbol access node with optional indexing/slicing."""
    def __init__(self, name, index_expr=None, slice_expr=None, line_num=0):
        super().__init__(line_num)
        self.name = name
        self.index_expr = index_expr
        self.slice_expr = slice_expr

class BinaryExpressionNode(ASTNode):
    """Binary arithmetic, relational, or logical expression node."""
    def __init__(self, left, operator, right, line_num=0):
        super().__init__(line_num)
        self.left = left
        self.operator = operator
        self.right = right

class CollectionNode(ASTNode):
    """Map or List collection literal node."""
    def __init__(self, coll_type, elements=None, line_num=0):
        super().__init__(line_num)
        self.coll_type = coll_type  # 'list', 'map'
        self.elements = elements or []  # items for list, tuples (k, v) for map

class CreateElementNode(ASTNode):
    """Frontend HTML component creation node (.enlgf)."""
    def __init__(self, tag, name=None, attributes=None, line_num=0):
        super().__init__(line_num)
        self.tag = tag              # 'hero', 'nav', 'button', 'form', 'table', etc.
        self.name = name
        self.attributes = attributes or {}

class StyleNode(ASTNode):
    """CSS styling block or theme node (.enlgd)."""
    def __init__(self, selector, rules=None, line_num=0):
        super().__init__(line_num)
        self.selector = selector
        self.rules = rules or {}

class TableNode(ASTNode):
    """Database table schema definition node (.enlgdb)."""
    def __init__(self, name, columns=None, line_num=0):
        super().__init__(line_num)
        self.name = name
        self.columns = columns or []  # list of (col_name, col_type)
