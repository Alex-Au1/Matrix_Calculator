import math
from typing import List, Union


# Complex_Num: Represents a complex number
class Complex_Num:
  def __init__(self, r: float, i: float):
    self.r = r
    self.i = i

  # printc() Prints out the complex number
  # effects: prints output
  def printc(self):
    print(f"{self.r} + {self.i}i",end="")


# modulus(c) Computes the modulus of the complex number, 'c'
def modulus(c: Complex_Num) -> float:
  return math.sqrt((c.r ** 2) + (c.i ** 2))


# conjugate(c) Computes the conjugate of the complex number, 'c'
def conjugate(c: Complex_Num) -> Complex_Num:
  return Complex_Num(c.r, (-1 * c.i))


# complex_divide(c, d) Computes the division of the complex number 'c' and 'd'
def complex_divide(c: Complex_Num, d: Complex_Num) -> List[Union[Complex_Num, float]]:
  conj_d = conjugate(d)
  denom = complex_multiply(d, conj_d).r
  num = complex_multiply(c, conj_d)
  return [Complex_Num(num.r, num.i), denom]


# complex_multiply(a, b) Computes the multiplication between the 
#   complex numbers, 'a' and 'b'
def complex_multiply(a: Complex_Num, b: Complex_Num) -> Complex_Num:
  return Complex_Num((a.r * b.r - a.i * b.i), (a.r * b.i + a.i * b.r))


# complex_add(a,b, sign) Computes either the addition or subtraction
#   of the complex numbers, 'a' and 'b'
# required: 'sign' is either "+" or "-"
def complex_add(a: Complex_Num, b: Complex_Num, sign: str = "+"):
  if (sign == "+"):
    return Complex_Num(a.r + b.r, a.i + b.i);
  elif (sign == "-"):
    return Complex_Num(a.r - b.r, a.i - b.i);
