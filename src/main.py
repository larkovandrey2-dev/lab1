from src.Calculator import Calculator
import sys


def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """

    print(
        'Калькулятор на основе обратной польской нотации (RPN). Лабораторная №1. Ларьков Андрей Александрович М8О-103БВ-25')
    calc = Calculator()
    user_numbers_after_dot = input(
        'До сколько знаков после запятой округлять дробный результат(по умолчанию - 2, нажмите enter, чтобы оставить так): ')
    while not user_numbers_after_dot.isdecimal() and user_numbers_after_dot != '':
        user_numbers_after_dot = input('Введите корректное число или нажмите enter: ')
    if not user_numbers_after_dot:
        pass
    else:
        calc.NUMBERS_AFTER_DOT = int(user_numbers_after_dot)
    user_expression = input('Введите выражение (q - выход): ')
    while True:
        res = '-'
        if user_expression.lower() == 'q':
            print('Спасибо за использование калькулятора!')
            sys.exit(0)
        try:
            calc.expression = user_expression
            res = calc.solve_rpn()
        except Exception as e:
            print(f'Ошибка: {e}')
        try:
            print(f'Результат: {res}')
        except ValueError:
            print('Ошибка: число слишком большое для отображения')
        print('-------------------')
        user_expression = input('Введите выражение (q - выход): ')


if __name__ == "__main__":
    main()
