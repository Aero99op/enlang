"""Compile-Time Constant Folding Optimizer for EnLang AST and IR."""
from ..parser.ast_nodes import BinaryExpressionNode, LiteralNode

class ConstantFolder:
    """Evaluates arithmetic expressions with constant literals at compile-time."""
    @classmethod
    def fold_ast(cls, node):
        if isinstance(node, BinaryExpressionNode):
            left = cls.fold_ast(node.left)
            right = cls.fold_ast(node.right)
            if isinstance(left, LiteralNode) and isinstance(right, LiteralNode):
                if left.type_tag == 'number' and right.type_tag == 'number':
                    try:
                        if node.operator == '+':
                            return LiteralNode(left.value + right.value, 'number')
                        elif node.operator == '-':
                            return LiteralNode(left.value - right.value, 'number')
                        elif node.operator == '*':
                            return LiteralNode(left.value * right.value, 'number')
                        elif node.operator == '/':
                            if right.value != 0:
                                return LiteralNode(left.value / right.value, 'number')
                    except Exception:
                        pass
            node.left = left
            node.right = right
        return node
