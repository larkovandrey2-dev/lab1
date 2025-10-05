import re
import sys
import warnings
from src.constants import WARN_RESULT

warnings.filterwarnings('always')


def custom_warn(message, category, filename, lineno, file=None, line=None):
    """
        Кастомный вывод предупреждений в stdout вместо stderr.

        Args:
            message (str): текст предупреждения
            category (Warning): тип предупреждения
            filename (str): имя файла
            lineno (int): номер строки
            file (optional): поток (не используется)
            line (optional): строка (не используется)
        """
    sys.stdout.write(f"\033[33m{message}\033[0m\n")


warnings.showwarning = custom_warn


class Calculator:
    """
        Калькулятор на основе обратной польской нотации (RPN).
    """

    def __init__(self):
        """
                Инициализация калькулятора.
        """
        self.priority = {'(': 0, '+': 1, '-': 1, '*': 2, '/': 2, '$': 2, '%': 2, '^': 3, '~': 4, '@': 4}
        self.expression = None
        self.rpn = None
        self.BIG_WARN = False
        self.NUMBERS_AFTER_DOT = 2
        self.OPERATION_WARN = False

    def tokenize(self):
        """
        Разбивает исходное выражение на токены.

        Returns:
            list[str]: список токенов (числа, операторы, скобки).

        Raises:
            Exception: если в выражении присутствуют недопустимые символы или некорректная запись числа.
        """
        self.expression = self.expression.replace('**', '^').replace('//', '$')
        tokens = re.findall(r'\d+\.\d+|\.\d+|\d+|[-+/%*()^$]', self.expression.replace(' ', ''))
        rebuild_exp = ''.join(i for i in tokens)
        if rebuild_exp != self.expression.replace(' ', ''):
            raise Exception('Invalid symbols in expression')
        if re.search(r'\d+\s+\d+|\d+\s+\.\s+\d+', self.expression):
            raise Exception(
                'Invalid expression: two numbers in a row with space between them/float digit with space between parts')
        return tokens

    def is_number(self, token):
        """
        Проверяет, является ли токен числом.

        Args:
            token (str): токен выражения.

        Returns:
            bool: True, если токен — число, иначе False.
        """
        try:
            float(token)
            return True
        except ValueError:
            return False

    def check_operation(self, op1, op2, op_name):
        """
        Проверяет возможность выполнения целочисленных операций.

        Args:
            op1 (int | float): первый операнд.
            op2 (int | float): второй операнд.
            op_name (str): название операции (// или %).

        Raises:
            Exception: если хотя бы один операнд не int.
            Exception: если попытка деления на ноль.
        """
        if not all(isinstance(x, int) for x in (op1, op2)):
            raise Exception(f'Invalid action for float digits in {op_name}')
        if op2 == 0:
            raise Exception('Division by zero')

    def should_pop(self, token, top_stack):
        """
        Проверяет, нужно ли выталкивать оператор из стека с учетом правоассоциативности.

        Args:
            token (str): текущий оператор.
            top_stack (str): оператор на вершине стека.

        Returns:
            bool: True, если нужно выталкивать, иначе False.
        """
        if token == '^':
            return self.priority[top_stack] > self.priority[token]
        return self.priority[top_stack] >= self.priority[token]

    def apply_result(self, op_result):
        """
        Обрабатывает результат операции: проверяет на превышение лимита
        и приводит число к int, если возможно.

        Args:
            op_result (int | float): результат операции.

        Returns:
            int | float: приведенный результат.
        """
        if op_result >= WARN_RESULT and not self.BIG_WARN:
            warnings.warn('Слишком большое значение вычисляемого значения. Программа может работать некорректно.')
            self.BIG_WARN = True
        ##Этот момент добавляем, чтобы по возможности результат был целым, без этого, например 5%1**(1.5-0.5) выдаст ошибку, что неверное, так как при проценте оба оператора будут целыми
        try:
            return int(op_result) if int(op_result) == op_result else op_result
        except ValueError:
            return op_result

    def to_rpn(self):
        """
        Переводит инфиксное выражение в обратную польскую нотацию (RPN).

        Returns:
            list: выражение в виде списка токенов RPN.

        Raises:
            Exception: если скобки некорректные или встречена
                       неверная последовательность операторов.
        """
        tokens = self.tokenize()
        stack = []
        output = []
        prev_token = None
        self.OPERATION_WARN = False
        for i, token in enumerate(tokens):
            if prev_token in self.priority and token in self.priority:
                if prev_token not in '()' and token not in '()' and not self.OPERATION_WARN:
                    warnings.warn(
                        'Два или более знаков подряд. Выражение продолжит обработку, но проверьте корректность введенных данных')
                    self.OPERATION_WARN = True
                    if token not in '+-':
                        raise Exception('Invalid sequence operators in expression')
            prev_token = token
            if self.is_number(token):
                if '.' in token:
                    output.append(float(token))
                else:
                    output.append(int(token))

            if token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack:
                    raise Exception("Invalid parentheses")
                stack.pop()
            elif token in self.priority:
                if (token == '-') and (i == 0 or tokens[i - 1] in self.priority):
                    token = '~'
                if (token == '+') and (i == 0 or tokens[i - 1] in self.priority):
                    token = '@'
                while stack and self.should_pop(token, stack[-1]):
                    output.append(stack.pop())
                stack.append(token)

        while stack:
            if stack[-1] == '(':
                raise Exception("Invalid parentheses")
            output.append(stack.pop())
        return output

    def solve_rpn(self):
        """
        Вычисляет выражение, представленное в обратной польской нотации.

        Returns:
            int | float: результат вычисления.

        Raises:
            Exception: если выражение некорректное или недостаточно операндов.
        """
        output = self.to_rpn()
        stack = []
        self.BIG_WARN = False
        for token in output:
            if isinstance(token, float) or isinstance(token, int):
                stack.append(token)
            else:
                if token == '~':
                    try:
                        op = stack.pop()
                        stack.append(-op)
                    except Exception:
                        pass
                elif token == '@':
                    op = stack.pop()
                    stack.append(op)
                else:
                    if len(stack) < 2:
                        print(stack)
                        print('-----')
                        raise Exception("Invalid expression")
                    op2 = stack.pop()
                    op1 = stack.pop()
                    if token == '-':
                        stack.append(self.apply_result(op1 - op2))
                    elif token == '+':
                        stack.append(self.apply_result(op1 + op2))
                    elif token == '*':
                        stack.append(self.apply_result(op1 * op2))
                    elif token == '/':
                        stack.append(self.apply_result(op1 / op2))
                    elif token == '^':
                        stack.append(self.apply_result(op1 ** op2))
                    elif token == '$':
                        self.check_operation(op1, op2, '//')
                        stack.append(self.apply_result(op1 // op2))
                    elif token == '%':
                        self.check_operation(op1, op2, '%')
                        stack.append(self.apply_result(op1 % op2))
        if len(stack) != 1:
            raise Exception("Invalid expression")
        if stack[0] == int(stack[0]):
            return int(stack[0])
        return round(stack[0], self.NUMBERS_AFTER_DOT)
