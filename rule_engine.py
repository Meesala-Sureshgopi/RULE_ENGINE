import re

class Node:
    # """Class to define a node in the Abstract Syntax Tree (AST)"""
    def __init__(self, node_type, value=None):
        self.node_type = node_type  
        self.value = value  
        self.left = None  
        self.right = None 

    def __repr__(self):
        return self._display_combined_rule()

    def _display_combined_rule(self):
        # """Return a readable format of the rule."""
        if self.node_type == "operand":
            return f"{self.value}"
        else:
            left_str = self.left._display_combined_rule() if self.left else ""
            right_str = self.right._display_combined_rule() if self.right else ""
            return f"({left_str} {self.value} {right_str})"

def create_rule(rule_string):
    # """
    # Parse the rule string into an AST that can handle multi-condition rules with AND/OR.
    # """
    # Improved regex to capture conditions correctly
    tokens = re.findall(r'(\w+)\s*([<>!=]+)\s*(\d+|"[^"]+"|\w+)|\s*(AND|OR)', rule_string)
    stack = []
    operator_stack = []

    def precedence(op):
        return {'AND': 2, 'OR': 1}.get(op, 0)

    def apply_operator():
        if len(stack) < 2:
            raise ValueError("Insufficient operands for operator.")
        right = stack.pop()
        left = stack.pop()
        op = operator_stack.pop()
        node = Node("operator", op)
        node.left = left
        node.right = right
        stack.append(node)

    for token in tokens:
        # Check if we have a condition
        if token[0]:  # Condition like "age > 30"
            operand = f"{token[0]} {token[1]} {token[2]}"
            stack.append(Node("operand", operand))
        elif token[3] in ('AND', 'OR'):
            while (operator_stack and operator_stack[-1] in ('AND', 'OR') and
                   precedence(token[3]) <= precedence(operator_stack[-1])):
                apply_operator()
            operator_stack.append(token[3])

    while operator_stack:
        apply_operator()

    if len(stack) != 1:
        raise ValueError("Invalid rule format.")
    
    return stack[0]

def combine_rules(rule_asts):
    # """Combine multiple rule ASTs into a single condition using AND logic."""
    combined_ast = rule_asts[0]
    for ast in rule_asts[1:]:
        combined_node = Node("operator", "AND")
        combined_node.left = combined_ast
        combined_node.right = ast
        combined_ast = combined_node
    return combined_ast

def evaluate_rule(ast, data):
    # """
    # Evaluate the rule's AST against one or multiple sets of data.
    # If multiple data sets are provided, evaluate each one individually.
    # """
    if isinstance(data, list):
        return [evaluate_single_data(ast, single_data) for single_data in data]
    else:
        return evaluate_single_data(ast, data)

def evaluate_single_data(ast, single_data):
    # """
    # Helper function to evaluate a single set of data against the rule's AST.
    # """
    if ast.node_type == "operand":
        field, operator, value = ast.value.split(' ')
        value = int(value) if value.isdigit() else value

        if field not in single_data:
            raise ValueError(f"Missing data for field: {field}")

        if operator == ">":
            return single_data[field] > value
        elif operator == "<":
            return single_data[field] < value
        elif operator == ">=":
            return single_data[field] >= value
        elif operator == "<=":
            return single_data[field] <= value
        elif operator == "==":
            return single_data[field] == value
        elif operator == "!=":
            return single_data[field] != value
        else:
            raise ValueError(f"Unsupported operator: {operator}")

    elif ast.node_type == "operator":
        left_result = evaluate_single_data(ast.left, single_data)
        right_result = evaluate_single_data(ast.right, single_data)
        if ast.value == "AND":
            return left_result and right_result
        elif ast.value == "OR":
            return left_result or right_result

    return False

