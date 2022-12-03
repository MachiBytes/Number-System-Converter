import sys, os

sys.path.append(os.getcwd())
from objects import *


class Main:
    def __init__(self) -> None:
        pass

    def convert(self) -> str:
        """Converts a number from base 2, 8, 10, 16 to base 2, 8, 10, 16.
        
        Inputs:
            start {string}: This is the base of the number. Accepts the following values: "10", "2", "8", "16".
            end {int}: This is the base of the result. Accepts the following values: 10, 2, 8, 16.
            num {float}: The number that will be converted.

        Returns:
            str: returns "Answer: {result}" with result being the converted number.
        
        Process:
            1. Take start input
            2. Take end input
            3. Take num input
            4. Instantiate the number system provided by 'start' and give 'num' as an argument.
            5. Return the string 'Answer: result' with result being the converted num.
        """

        type_classes = {
            "10": Decimal,
            "2": Binary,
            "8": Octal,
            "16": Hexadecimal
        }

        start = input("Starting base: ")
        end = int(input("Ending base: "))
        num = float(input("Number: "))

        # Assign to their own bases
        num = type_classes[start](num)
        return f"Answer: {num.convert(end)}"


main = Main()

print(main.convert())
