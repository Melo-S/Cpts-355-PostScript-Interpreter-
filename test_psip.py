import psip
# Helper function to initialize the dictionary stack for tests
def setup_test_dict_stack():
    psip.dict_stack.clear()
    # Manually add the initial global dictionary with all operations
    global_dict = {
        "add": psip.add_operation, "sub": psip.sub_operation, "mul": 
psip.mul_operation, "div": psip.div_operation, "mod": psip.mod_operation,
        "exch": psip.exch_operation, "pop": psip.pop_operation, "copy": 
psip.copy_operation, "dup": psip.dup_operation,
        "clear": psip.clear_operation, "count": psip.count_operation, "eq": 
psip.eq_operation,
        "length": psip.length_operation, "dict": psip.dict_operation, "begin": 
psip.begin_operation, "end": psip.end_operation,
        "def": psip.def_operation, "=": psip.pop_and_print, # Include pop_and_print
        "and": psip.and_operation, "sqrt": psip.sqrt_operation, "get": 
psip.get_operation, "getinterval": psip.getinterval_operation, "putinterval": 
psip.putinterval_operation,
        "lt": psip.lt_operation, "gt": psip.gt_operation, "ne": psip.ne_operation, 
"or": psip.or_operation, "not": psip.not_operation,
        "abs": psip.abs_operation, "ceiling": psip.ceiling_operation, "floor": 
psip.floor_operation, "round": psip.round_operation, "idiv": psip.idiv_operation,
        "if": psip.if_operation,
        "ifelse": psip.ifelse_operation,
        "for": psip.for_operation,
        "repeat": psip.repeat_operation
    }
    psip.dict_stack.append(global_dict)
# Test for the add operation
def test_add_operation():
    psip.op_stack.clear()
    setup_test_dict_stack()
    psip.process_input("1")
    psip.process_input("2")
    psip.process_input("add")
    assert psip.op_stack[-1] == 3
# Test for looking up values in dictionaries
def test_lookup_operation():
    psip.op_stack.clear()
    setup_test_dict_stack()
    psip.process_input("/x")
    psip.process_input("2")
    psip.process_input("def")
    psip.process_input("x")
    assert psip.op_stack[-1] == 2
# Test for the exch (exchange) operation
def test_exch_operation():
    psip.op_stack.clear()
    setup_test_dict_stack()
    psip.process_input("1")
    psip.process_input("2")
    psip.process_input("exch")
    assert psip.op_stack[-1] == 1
    assert psip.op_stack[-2] == 2
def test_pop_operation():
    psip.op_stack.clear()
    setup_test_dict_stack()
    psip.process_input("1")
    psip.process_input("pop")
    assert len(psip.op_stack) == 0
# Test for the copy operation
def test_copy_operation():
    psip.op_stack.clear()
    setup_test_dict_stack()
    psip.process_input("1")
    psip.process_input("copy")
    assert psip.op_stack[-1] == 1
    assert psip.op_stack[-2] == 1
def test_dict_operation():
    psip.op_stack.clear()
    setup_test_dict_stack()
    psip.process_input("10")
    psip.process_input("dict")
    assert isinstance(psip.op_stack[-1], dict)
def test_length_operation():
    psip.op_stack.clear()
    setup_test_dict_stack()
    psip.process_input("10")
    psip.process_input("dict")
    psip.op_stack.append({"a": 1, "b": 2})
    psip.process_input("length")
    assert psip.op_stack[-1] == 2
def test_begin_operation():
    psip.op_stack.clear()
    setup_test_dict_stack()
    psip.process_input("1")
    psip.process_input("dict")
    psip.process_input("begin")
    assert len(psip.dict_stack) == 2
def test_end_operation():
    psip.op_stack.clear()
    setup_test_dict_stack()
    psip.dict_stack.append({}) # Add a dictionary to the stack for the test
    psip.process_input("end")
    assert len(psip.dict_stack) == 1
def test_clear_operation():
    psip.op_stack.clear()
    setup_test_dict_stack()
    psip.process_input("1")
    psip.process_input("2")
    psip.process_input("clear")
    assert len(psip.op_stack) == 0
def test_count_operation():
    psip.op_stack.clear()
    setup_test_dict_stack()
    psip.process_input("1")
    psip.process_input("2")
    psip.process_input("count")
    assert psip.op_stack[-1] == 2
def test_sub_operation():
    psip.op_stack.clear()
    setup_test_dict_stack()
    psip.process_input("5")
    psip.process_input("2")
    psip.process_input("sub")
    assert psip.op_stack[-1] == 3
def test_mul_operation():
    psip.op_stack.clear()
    setup_test_dict_stack()
    psip.process_input("5")
    psip.process_input("2")
    psip.process_input("mul")
    assert psip.op_stack[-1] == 10
def test_div_operation():
    psip.op_stack.clear()
    setup_test_dict_stack()
    psip.process_input("10")
    psip.process_input("2")
    psip.process_input("div")
    assert psip.op_stack[-1] == 5.0
def test_mod_operation():
    psip.op_stack.clear()
    setup_test_dict_stack()
    psip.process_input("10")
    psip.process_input("3")
    psip.process_input("mod")
    assert psip.op_stack[-1] == 1
def test_dup_operation():
    psip.op_stack.clear()
    setup_test_dict_stack()
    psip.process_input("1")
    psip.process_input("dup")
    assert psip.op_stack[-1] == 1
    assert psip.op_stack[-2] == 1
def test_eq_operation():
    psip.op_stack.clear()
    setup_test_dict_stack()
    psip.process_input("1")
    psip.process_input("1")
    psip.process_input("eq")
    assert psip.op_stack[-1] == True
