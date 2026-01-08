import argparse
from calculator import Calculator

def main():
    """ Setup argparse """
    parser = argparse.ArgumentParser()

    """ Add number arguments """
    parser.add_argument("number1", type = float)
    parser.add_argument("number2", type = float)

    """ Parse arguments from command line """
    args = parser.parse_args()

    """ Perform calculation """
    calc = Calculator(num1 = args.number1, num2 = args.number2)
    result = calc.get_quotient()
    print(f"Result: {args.number1} divided by {args.number2} is {result}")

if __name__ == "__main__":
    main()