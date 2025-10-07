import logging
import math # Import math module for sqrt
logging.basicConfig(level = logging.INFO)
# Operand stack for processing operations
op_stack = []
# Dictionary stack for managing scopes
dict_stack = []
dict_stack.append({})
class ParseFailed(Exception):
    """ Exception while parsing """
    pass # Custom exception for parsing errors
class TypeMismatch(Exception):
    """ Exception with types of operators and operands """
    pass # Custom exception for type mismatches
# Read-Eval-Print Loop
def repl():
    while True:
        user_input = input("REPL> ")
        if user_input.lower() == "quit":
            break
        process_input(user_input)
        logging.debug(f"Operand Stack: {op_stack}")
def process_boolean(input):
    logging.debug(f"Input to process boolean: {input}")
    if input == "true":
        return True
    elif input == "false":
        return False
    else:
        raise ParseFailed("can't parse it into boolean")
def process_number(input):
    logging.debug(f"Input to process number: {input}")
    try:
        float_value = float(input)
        if float_value.is_integer():
            return int(float_value)
        else:
            return float_value
    except ValueError:
        raise ParseFailed("can't parse this into a number")
def process_code_block(input):
    logging.debug(f"Input to process number: {input}")
    if len(input) >= 2 and input.startswith("{") and input.endswith("}"):
        return input[1:-1].strip().split()
    else:
        raise ParseFailed("can't parse this into a code block")
def process_name_constant(input):
    logging.debug(f"Input to process number: {input}")
    if input.startswith("/"):
        return input
    else:
        raise ParseFailed("Can't parse into name constant")
def process_string(input):
    logging.debug(f"Input to process string: {input}")
    if len(input) >= 2 and input.startswith("(") and input.endswith(")"):
        return input[1:-1]
    else:
        raise ParseFailed("can't parse this into a string")
# List of parser functions to try (order matters for parsing precedence)
PARSERS = [
    process_code_block, # Prioritize parsing code blocks
    process_boolean,
    process_number,
    process_name_constant,
    process_string
]
def process_constants(input):
    # Try parsers in order
    for parser in PARSERS:
        try:
            res = parser(input)
            op_stack.append(res)
            return
        except ParseFailed as e:
            logging.debug(e)
            continue
    # If no parser worked, it's not a constant
    raise ParseFailed(f"None of the parsers worked for the input {input}")
def add_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        res = op1 + op2
        op_stack.append(res)
    else:
        raise TypeMismatch("Not enough operands for operation add")
def def_operation():
    if len(op_stack) >= 2:
        value = op_stack.pop()
        name = op_stack.pop()
        if isinstance(name, str) and name.startswith("/"):
            key = name[1:]
            dict_stack[-1][key] = value
        else:
            op_stack.append(name)
            op_stack.append(value)
            raise TypeMismatch("Invalid name for def operation")
    else:
        raise TypeMismatch("Not enough operands for operation def")
def exch_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        op_stack.append(op1)
        op_stack.append(op2)
    else:
        raise TypeMismatch("Not enough operands for operation exch")
def pop_operation():
    if len(op_stack) >= 1:
        op_stack.pop()
    else:
        raise TypeMismatch("Not enough operands for operation pop")
def copy_operation():
    if len(op_stack) >= 1:
        op1 = op_stack[-1]
        op_stack.append(op1)
    else:
        raise TypeMismatch("Not enough operands for operation copy")
def dup_operation():
    if len(op_stack) >= 1:
        op1 = op_stack[-1]
        op_stack.append(op1)
    else:
        raise TypeMismatch("Not enough operands for operation dup")
def clear_operation():
    op_stack.clear()
def count_operation():
    op_stack.append(len(op_stack))
def sub_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        res = op2 - op1
        op_stack.append(res)
    else:
        raise TypeMismatch("Not enough operands for operation sub")
def mul_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        res = op1 * op2
        op_stack.append(res)
    else:
        raise TypeMismatch("Not enough operands for operation mul")
def div_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        if op1 == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        res = op2 / op1
        op_stack.append(res)
    else:
        raise TypeMismatch("Not enough operands for operation div")
def mod_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        res = op2 % op1
        op_stack.append(res)
    else:
        raise TypeMismatch("Not enough operands for operation mod")
def dict_operation():
    if len(op_stack) >= 1:
        op1 = op_stack.pop()
        if isinstance(op1, int):
            new_dict = {}
            op_stack.append(new_dict)
        else:
            raise TypeMismatch("Operand must be an integer")
    else:
        raise TypeMismatch("Not enough operands for operation dict")
def length_operation():
    if len(op_stack) >= 1:
        op1 = op_stack.pop()
        if isinstance(op1, dict):
            op_stack.append(len(op1))
        elif isinstance(op1, str):
            op_stack.append(len(op1))
        else:
            raise TypeMismatch("Operand must be a dictionary or a string")
    else:
        raise TypeMismatch("Not enough operands for operation length")
def begin_operation():
    if len(op_stack) >= 1:
        op1 = op_stack.pop()
        if isinstance(op1, dict):
            dict_stack.append(op1)
        else:
            raise TypeMismatch("Operand must be a dictionary")
    else:
        raise TypeMismatch("Not enough operands for operation begin")
def end_operation():
    if len(dict_stack) > 1:
        dict_stack.pop()
    else:
        raise TypeMismatch("Cannot end the last dictionary")
def eq_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        op_stack.append(op1 == op2)
    else:
        raise TypeMismatch("Not enough operands for operation eq")
def lt_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        if isinstance(op1, (int, float)) and isinstance(op2, (int, float)):
            op_stack.append(op2 < op1)
        else:
            op_stack.append(op2)
            op_stack.append(op1)
            raise TypeMismatch("Operands for lt operation must be numbers")
    else:
        raise TypeMismatch("Not enough operands for operation lt")
def gt_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        if isinstance(op1, (int, float)) and isinstance(op2, (int, float)):
            op_stack.append(op2 > op1)
        else:
            op_stack.append(op2)
            op_stack.append(op1)
            raise TypeMismatch("Operands for gt operation must be numbers")
    else:
        raise TypeMismatch("Not enough operands for operation gt")
def ne_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        op_stack.append(op1 != op2)
    else:
        raise TypeMismatch("Not enough operands for operation ne")
def or_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        if isinstance(op1, bool) and isinstance(op2, bool):
            op_stack.append(op1 or op2)
        else:
            op_stack.append(op2)
            op_stack.append(op1)
            raise TypeMismatch("Operands for or operation must be booleans")
    else:
        raise TypeMismatch("Not enough operands for operation or")
def not_operation():
    if len(op_stack) >= 1:
        op1 = op_stack.pop()
        if isinstance(op1, bool):
            op_stack.append(not op1)
        else:
            op_stack.append(op1)
            raise TypeMismatch("Operand for not operation must be a boolean")
    else:
        raise TypeMismatch("Not enough operands for operation not")
def abs_operation():
    if len(op_stack) >= 1:
        op1 = op_stack.pop()
        if isinstance(op1, (int, float)):
            op_stack.append(abs(op1))
        else:
            op_stack.append(op1)
            raise TypeMismatch("Operand for abs operation must be a number")
    else:
        raise TypeMismatch("Not enough operands for operation abs")
def ceiling_operation():
    if len(op_stack) >= 1:
        op1 = op_stack.pop()
        if isinstance(op1, (int, float)):
            op_stack.append(math.ceil(op1))
        else:
            op_stack.append(op1)
            raise TypeMismatch("Operand for ceiling operation must be a number")
    else:
        raise TypeMismatch("Not enough operands for operation ceiling")
def floor_operation():
    if len(op_stack) >= 1:
        op1 = op_stack.pop()
        if isinstance(op1, (int, float)):
            op_stack.append(math.floor(op1))
        else:
            op_stack.append(op1)
            raise TypeMismatch("Operand for floor operation must be a number")
    else:
        raise TypeMismatch("Not enough operands for operation floor")
def round_operation():
    if len(op_stack) >= 1:
        op1 = op_stack.pop()
        if isinstance(op1, (int, float)):
            op_stack.append(round(op1))
        else:
            op_stack.append(op1)
            raise TypeMismatch("Operand for round operation must be a number")
    else:
        raise TypeMismatch("Not enough operands for operation round")
def idiv_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        if isinstance(op1, (int, float)) and isinstance(op2, (int, float)):
            if op1 == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            op_stack.append(int(op2 // op1))
        else:
            op_stack.append(op2)
            op_stack.append(op1)
            raise TypeMismatch("Operands for idiv operation must be numbers")
    else:
        raise TypeMismatch("Not enough operands for operation idiv")
def if_operation():
    if len(op_stack) >= 2:
        code_block = op_stack.pop()
        bool_value = op_stack.pop()
        if bool_value:
            for item in code_block:
                process_input(item)
    else:
        raise TypeMismatch("Not enough operands for operation if")
def ifelse_operation():
    if len(op_stack) >= 3:
        else_block = op_stack.pop()
        if_block = op_stack.pop()
        bool_value = op_stack.pop()
        if isinstance(bool_value, bool) and isinstance(if_block, list) and \
isinstance(else_block, list):
            if bool_value:
                process_input(if_block)
            else:
                process_input(else_block)
        else:
            op_stack.append(bool_value)
            op_stack.append(if_block)
            op_stack.append(else_block)
            raise TypeMismatch("Operands for ifelse operation must be a boolean and \
two code blocks")
    else:
        raise TypeMismatch("Not enough operands for operation ifelse")
def for_operation():
    if len(op_stack) >= 4:
        code_block = op_stack.pop()
        increment = op_stack.pop()
        limit = op_stack.pop()
        initial = op_stack.pop()
        if isinstance(initial, (int, float)) and isinstance(limit, (int, float)) \
and isinstance(increment, (int, float)) and isinstance(code_block, list):
            current = initial
            while (increment > 0 and current <= limit) or (increment < 0 and 
current >= limit):
                op_stack.append(current)
                process_input(code_block)
                current += increment
        else:
            op_stack.append(initial)
            op_stack.append(limit)
            op_stack.append(increment)
            op_stack.append(code_block)
            raise TypeMismatch("Operands for for operation must be initial, limit, increment (numbers) and a code block")
    else:
        raise TypeMismatch("Not enough operands for operation for")
def repeat_operation():
    if len(op_stack) >= 2:
        code_block = op_stack.pop()
        count = op_stack.pop()
        if isinstance(count, int) and isinstance(code_block, list) and count >= 0:
            for _ in range(count):
                process_input(code_block)
        else:
            op_stack.append(count)
            op_stack.append(code_block)
            raise TypeMismatch("Operands for repeat operation must be an integer \
count and a code block")
    else:
        raise TypeMismatch("Not enough operands for operation repeat")
def get_operation():
    if len(op_stack) >= 2:
        index = op_stack.pop()
        string = op_stack.pop()
        if isinstance(string, str) and isinstance(index, int):
            if 0 <= index < len(string):
                op_stack.append(ord(string[index]))
            else:
                op_stack.append(string)
                op_stack.append(index)
                raise TypeMismatch("Index out of bounds for get operation")
        else:
            op_stack.append(string)
            op_stack.append(index)
            raise TypeMismatch("Operands for get operation must be a string and an \
integer")
    else:
            raise TypeMismatch("Not enough operands for operation get")
def getinterval_operation():
    if len(op_stack) >= 3:
        count = op_stack.pop()
        index = op_stack.pop()
        string = op_stack.pop()
        if isinstance(string, str) and isinstance(index, int) and isinstance(count, 
int):
            if 0 <= index <= len(string) and 0 <= count <= len(string) - index:
                op_stack.append(string[index : index + count])
            else:
                op_stack.append(string)
                op_stack.append(index)
                op_stack.append(count)
                raise TypeMismatch("Index or count out of bounds for getinterval 
operation")
        else:
            op_stack.append(string)
            op_stack.append(index)
            op_stack.append(count)
            raise TypeMismatch("Operands for getinterval operation must be a \
string, an integer index, and an integer count")
    else:
        raise TypeMismatch("Not enough operands for operation getinterval")
def putinterval_operation():
    if len(op_stack) >= 3:
        source_string = op_stack.pop()
        index = op_stack.pop()
        target_string = op_stack.pop()
        if isinstance(target_string, str) and isinstance(index, int) and 
isinstance(source_string, str):
            if 0 <= index <= len(target_string) and index + len(source_string) <= 
len(target_string):
                op_stack.append(target_string[:index] + source_string + 
target_string[index + len(source_string):])
            else:
                op_stack.append(target_string)
                op_stack.append(index)
                op_stack.append(source_string)
                raise TypeMismatch("Index or source string length out of bounds for 
putinterval operation")
        else:
            op_stack.append(target_string)
            op_stack.append(index)
            op_stack.append(source_string)
            raise TypeMismatch("Operands for putinterval operation must be a target 
string, an integer index, and a source string")
    else:
        raise TypeMismatch("Not enough operands for operation putinterval")
def and_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        if isinstance(op1, bool) and isinstance(op2, bool):
            op_stack.append(op1 and op2)
        else:
            op_stack.append(op2)
            op_stack.append(op1)
            raise TypeMismatch("Operands for and operation must be booleans")
    else:
        raise TypeMismatch("Not enough operands for operation and")
def sqrt_operation():
    if len(op_stack) >= 1:
        op1 = op_stack.pop()
        if isinstance(op1, (int, float)) and op1 >= 0:
            op_stack.append(math.sqrt(op1))
        else:
            op_stack.append(op1)
            raise TypeMismatch("Operand for sqrt operation must be a non-negative 
number")
    else:
        raise TypeMismatch("Not enough operands for operation sqrt")
def lookup_in_dictionary(input):
    for d in reversed(dict_stack):
        if input in d:
            value = d[input]
            if callable(value):
                value()
            elif isinstance(value, list):
                for item in value:
                    process_input(item)
            else:
                op_stack.append(value)
            return
    raise ParseFailed(f"input {input} is not in dictionary")
def tokenize(input_string):
    tokens = []
    i = 0
    while i < len(input_string):
        if input_string[i].isspace():
            i += 1
            continue
        elif input_string[i] == '{':
            j = i
            brace_count = 0
            while j < len(input_string):
                if input_string[j] == '{':
                    brace_count += 1
                elif input_string[j] == '}':
                    brace_count -= 1
                if brace_count == 0:
                    tokens.append(input_string[i : j + 1])
                    i = j + 1
                    break
                j += 1
            if brace_count != 0:
                raise ParseFailed("Unmatched braces in code block")
        else:
            j = i
        while j < len(input_string) and not input_string[j].isspace() and \
input_string[j] != '{' and input_string[j] != '}':
                j += 1
            tokens.append(input_string[i:j])
            i = j
    return tokens
# Process user input (string from REPL or list from code block)
def process_input(user_input):
    if isinstance(user_input, str):
        try:
            tokens = tokenize(user_input)
        except ParseFailed as e:
            logging.error(e)
            return
    elif isinstance(user_input, list):
        tokens = user_input
    else:
        logging.error(f"Invalid input type to process_input: {type(user_input)}")
        return
    for token in tokens:
        if isinstance(token, str) and token.startswith("{") and 
token.endswith("}"):
            try:
                code_block_tokens = process_code_block(token)
                op_stack.append(code_block_tokens)
            except ParseFailed as e:
                logging.error(e)
        else:
            try:
                process_constants(token)
            except ParseFailed as e:
                logging.debug(e)
                try:
                    lookup_in_dictionary(token)
                except Exception as e:
                    logging.error(e)
def pop_and_print():
    if len(op_stack) >= 1:
        op1 = op_stack.pop()
        print(op1)
    else:
        raise TypeMismatch("Stack is empty! nothing to print") # Reverted to 
original error
dict_stack[-1].update({
    "add": add_operation, "sub": sub_operation, "mul": mul_operation, "div": 
div_operation, "mod": mod_operation,
    "exch": exch_operation, "pop": pop_operation, "copy": copy_operation, "dup": 
dup_operation,
    "clear": clear_operation, "count": count_operation, "eq": eq_operation,
    "length": length_operation, "dict": dict_operation, "begin": begin_operation, 
"end": end_operation,
    "def": def_operation, "=": pop_and_print, # Print top of stack
    "and": and_operation, "sqrt": sqrt_operation, "get": get_operation, 
"getinterval": getinterval_operation, "putinterval": putinterval_operation,
    "lt": lt_operation, "gt": gt_operation, "ne": ne_operation, "or": or_operation, 
"not": not_operation,
    "abs": abs_operation, "ceiling": ceiling_operation, "floor": floor_operation, 
"round": round_operation, "idiv": idiv_operation,
    "if": if_operation, # Conditional execution
    "ifelse": ifelse_operation, # Conditional execution with else
    "for": for_operation, # Loop with counter
    "repeat": repeat_operation # Loop a fixed number of times
})
lexical_scoping = False
# Main execution block
if __name__ == "__main__":
    repl()
