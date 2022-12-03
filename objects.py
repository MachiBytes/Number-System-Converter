class Number:
    hex_codes = ["A", "B", "C", "D", "E", "F"]
    def __init__(self, number) -> None:
        """Parent class for number systems. Handles data preparation (splitting the number input into 2 parts).

        Args:
            number (int): the number that will be converted.

        Attributes:
            self.number (int): contains the number
            self.components (list[str]): ["whole", "fraction"] with "whole" being the number before the decimal
                point and "fraction" being the number after the decimal point
            self.whole (int): first element in self.components turned into an integer
            self.fraction (float): second element in self.components turned into a float with "0." on the right
            self.fraction_limit (int): determines the maximum number of digits after the decimal point for the
                end result
            self.hex_codes (list[str]): ["A", "B", "C", "D", "E", "F"] contains the equivalents of 10-15 for
                hexadecimal
        """

        self.number = number
        self.components = str(number).split(".")
        self.whole = int(self.components[0])
        self.fraction = float("0." + self.components[1])
        self.fraction_limit = 6
    
    def show(self):
        print(self.whole + self.fraction)


class Decimal(Number):
    def __init__(self, number) -> None:
        super().__init__(number)
    
    def convert(self, base):
        t_whole = self.whole
        t_fraction = self.fraction
        c_whole = []
        c_fraction = []

        print("\nSolution for Whole number")
        # Converting whole part
        while t_whole > 0:
            quotient, remainder = divmod(t_whole, base)
            if remainder > 9:
                remainder = self.hex_codes[remainder % 10]
            c_whole.insert(0, str(remainder))
            print(f">> {t_whole} / {base} = {quotient} with a remainder of {remainder}\n")
            t_whole = quotient

        print("Solution for Fraction number")
        # Converting fraction part
        digits = 0
        while t_fraction != 0 and digits < self.fraction_limit:
            t_fraction2 = t_fraction * base
            print(f"{t_fraction} * {base} = {t_fraction2}")
            w_fraction = int(t_fraction2)
            t_fraction = t_fraction2 - w_fraction
            if w_fraction > 9:
                w_fraction = self.hex_codes[w_fraction % 10]
            c_fraction.append(str(w_fraction))
            digits += 1

        # Returning result
        return f"{''.join(c_whole)}.{''.join(c_fraction)}\n"
    
    @classmethod
    def revert(cls, num, base, to_print=False):
        num = str(num)
        num_list = [digit.upper() for digit in list(num) if digit != "."]
        sum = 0
        degree = list(num).index(".") - 1

        sum = ""
        for i, n in enumerate(num_list):
            if n == ".":
                continue
            if n in cls.hex_codes:
                n = cls.hex_codes.index(n) + 10
            sum += str(int(n) * (base ** degree))
            degree -= 1
            if i != len(num_list) - 1:
                sum += " + "
        
        if to_print:
            print(f"{num} -> {sum}")

        final_sum = eval(sum)
        if final_sum > 9 and base == 16:
            final_sum = cls.hex_codes[int(final_sum) % 10]
        return final_sum

class Binary(Number):

    bin_db = {
            "0": "000",
            "1": "001",
            "2": "010",
            "3": "011",
            "4": "100",
            "5": "101",
            "6": "110",
            "7": "111",
            "8": "1000",
            "9": "1001",
            "A": "1010",
            "B": "1011",
            "C": "1100",
            "D": "1101",
            "E": "1110",
            "F": "1111"
        }

    def __init__(self, number) -> None:
        super().__init__(number)
        self.whole, self.fraction = list(self.components[0]).copy(), list(self.components[1]).copy()
    
    def convert(self, base):
        if base == 10:
            return Decimal.revert(self.number, 2, True)
        
        # Splitting the whole number
        split = 3 if base == 8 else 4
        t_whole = []
        for i in reversed(range(1, len(self.whole) + 1, split)):
            temp = None
            if i == 1:
                temp = self.whole[-i - split + 1: len(self.whole)]
            else:
                temp = self.whole[-i - split + 1: -(i - 1)]
            
            if len(temp) != split:
                temp = (["0"] * (split - len(temp))) + temp
            if temp[0] == "0" and split == 4:
                temp.remove("0")
            t_whole.append(list(self.bin_db.keys())[list(self.bin_db.values()).index("".join(temp))])

        print(f"Whole number {self.whole} became {', '.join(t_whole)}")

        # Splitting the fraction number
        t_fraction = []
        for i in range(0, len(self.fraction), split):
            temp = self.fraction[i:i+split]
            if len(temp) != split:
                temp += ["0"] * (split - len(temp))
            if temp[0] == "0" and split == 4:
                temp.remove("0")
            t_fraction.append(list(self.bin_db.keys())[list(self.bin_db.values()).index("".join(temp))])
            
        print(f"Fraction number {self.fraction} became {', '.join(t_fraction)}")

        # Finalizing whole and Fraction
        self.whole = "".join(t_whole)
        self.fraction = "".join(t_fraction)

        return f"{self.whole}.{self.fraction}"
    
    @classmethod
    def revert(cls, num, base, to_print=False):
        num = str(num)
        whole, fraction = num.split(".")

        whole = [f"0{cls.bin_db[x]}" if base == 16 and len(list(x)) == 3 else cls.bin_db[x] for x in list(whole)]
        fraction = [f"0{cls.bin_db[x]}" if base == 16 and len(list(x)) == 3 else cls.bin_db[x] for x in list(fraction)]
        
        return f"{''.join([x for x in whole if x != '0'])}.{''.join([x for x in fraction if x != '0'])}"


class Octal(Number):
    def __init__(self, number) -> None:
        super().__init__(number)
    
    def convert(self, base):
        if base == 10:
            return Decimal.revert(self.number, 8, True)
        if base == 2:
            return Binary.revert(self.number, 8, True)
        
        if base == 16:
            num = Binary(Binary.revert(self.number, 8, True))
            return num.convert(16)


class Hexadecimal(Number):
    def __init__(self, number) -> None:
        super().__init__(number)
    
    def convert(self, base):
        if base == 10:
            return Decimal.revert(self.number, 16, True)
        if base == 2:
            return Binary.revert(self.number, 16, True)
        
        if base == 8:
            num = Binary(Binary.revert(self.number, 16, True))
            return num.convert(8)
