from collections import deque

''' MATH EXPRESSION PARSER

    It creates reversed polish notation and than use calculator, which works with RPN
 '''


def create_rpn(string):
    # treat edge case when negative number is read from shortname and have minus sign before it
    string = string.replace("--", "")
    # possible operators could be extended with Associativity (need for power op)
    dOperators = {"*": 2,
                  "/": 2,
                  "+": 1,
                  "-": 1}
    output = deque()
    operators_stack = deque()
    test_stack = deque(string.split())
    if test_stack[0] == "-": test_stack.appendleft("0")
    if test_stack[0] == "(" and test_stack[1] == "-":
        test_stack.popleft()
        test_stack.appendleft("0")
        test_stack.appendleft("(")

    # SHUNTING YARD ALGORITHM #
    while len(test_stack):
        token = test_stack.popleft()
        if token.replace('.', '').replace('-', '').isdigit():
            output.append(float(token))
        elif token in dOperators:
            while (len(operators_stack) and operators_stack[0] != "(" and dOperators[operators_stack[0]] >=
                   dOperators[token]):
                output.append(operators_stack.popleft())
            operators_stack.appendleft(token)
        elif token == "(":
            operators_stack.appendleft(token)
        elif token == ")":
            while operators_stack[0] != "(":
                if not len(operators_stack):
                    raise ValueError
                output.append(operators_stack.popleft())
            if operators_stack[0] == "(":
                operators_stack.popleft()
    # pop last of the operators to output
    while len(operators_stack):
        output.append(operators_stack.popleft())

    return output


def rpn_calculator(reverse_polish_notation):
    dOperations = {'*': multiply_operands,
                   '/': divide_operands,
                   '+': add_operands,
                   '-': subtract_operands}
    stack = []

    # REVERSE POLISH NOTATION CALCULATOR #
    for token in reverse_polish_notation:
        if token in dOperations:
            dOperations[token](stack)
        else:
            try:
                stack.append(float(token))
            except ValueError as e:
                print(f"{e}\nExpected token is not convertable to Float")
    return stack[0]


def get_operands(stack):
    # pop 2 operands and return them
    return stack.pop(), stack.pop()


def multiply_operands(stack):
    x, y = get_operands(stack)
    stack.append(x * y)


def divide_operands(stack):
    x, y = get_operands(stack)
    stack.append(y / x)


def add_operands(stack):
    x, y = get_operands(stack)
    stack.append(x + y)


def subtract_operands(stack):
    x, y = get_operands(stack)
    stack.append(y - x)


def main():
    math_expression = "-30 + ( ( -40 + 50 ) ) / 2"
    result = rpn_calculator(create_rpn(math_expression))
    print(f"Result of the: ({math_expression}) = {result}")


if __name__ == "__main__":
    main()
