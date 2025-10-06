import sys

from src.calculator import Calculator


def main() -> None:
    """
        Точка входа в приложение.
        """
    print(
        'Калькулятор на основе обратной польской нотации (RPN). '
        'Лабораторная №1. Ларьков Андрей Александрович М8О-103БВ-25'
    )

    user_numbers_after_dot = input(
        'До сколько знаков после запятой округлять дробный результат '
        '(по умолчанию - 2, нажмите enter, чтобы оставить так): '
    )

    while not user_numbers_after_dot.isdecimal() and user_numbers_after_dot != '':
        user_numbers_after_dot = input('Введите корректное число или нажмите enter: ')
    if not user_numbers_after_dot:
        calc = Calculator()
    else:
        calc = Calculator(int(user_numbers_after_dot))
    user_expression = input('Введите выражение (q - выход): ')
    while True:
        res: float | int | None = None
        if user_expression.lower() == 'q':
            print('Спасибо за использование калькулятора!')
            sys.exit(0)
        try:
            res = calc.solve(user_expression)
        except Exception as e:
            print(f'Ошибка: {e}')
        try:
            print(f'Результат: {res}')
        except ValueError:
            sys.set_int_max_str_digits(10**6)
            print(f'Резудьтат: {res}')
        print('-------------------')
        user_expression = input('Введите выражение (q - выход): ')


if __name__ == "__main__":
    main()
