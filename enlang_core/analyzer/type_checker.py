"""Dynamic/Static Type Validation & Inference Engine for EnLang."""

class TypeChecker:
    """Validates operand types and infers expression return types."""
    @staticmethod
    def infer_type(literal_or_node):
        from ..parser.ast_nodes import LiteralNode, BinaryExpressionNode, VariableNode
        if isinstance(literal_or_node, LiteralNode):
            return literal_or_node.type_tag
        elif isinstance(literal_or_node, BinaryExpressionNode):
            left_t = TypeChecker.infer_type(literal_or_node.left)
            right_t = TypeChecker.infer_type(literal_or_node.right)
            if literal_or_node.operator in ('+', '-', '*', '/', '%', '**'):
                if left_t == 'string' or right_t == 'string':
                    return 'string' if literal_or_node.operator == '+' else 'unknown'
                return 'number'
            elif literal_or_node.operator in ('==', '!=', '>', '<', '>=', '<=', 'in', 'not in'):
                return 'boolean'
        return 'unknown'
