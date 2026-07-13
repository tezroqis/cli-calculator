# create a calc

def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Деление на ноль невозможно.")
    return a / b


operations = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}


def main():
    print("=== CLI Калькулятор ===")

    while True:
        print("\nДоступные операции: +  -  *  /")
        operation = input("Введите операцию (или 'q' для выхода): ").strip()

        if operation.lower() == "q" or operation.lower() == "quit":
            print("До свидания!")
            break

        if operation not in operations:
            print("Неизвестная операция.")
            continue

        try:
            num1 = float(input("Введите первое число: "))
            num2 = float(input("Введите второе число: "))

            result = operations[operation](num1, num2)
            print(f"Результат: {result}")

        except ValueError:
            print("Ошибка: некорректное число. Попробуйте снова.")
        except ZeroDivisionError as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nДо свидания!")