import enum
import math
import copy
import complex
import lcm
import gcd
import validate
from typing import Union


DENOM_0_ERR = 2


# NumberType: Sets of Numbers
class NumberType(enum.Enum):
   RealNum = "r"
   ComplexNum = "c"


# RealFractions: Fractions where the numerator and denominator
#   are both real numbers
class RealFraction:
  def __init__(self, num: int, denom: int):
    self.num = num;
    if (denom):
      self.denom = denom
      self.normalize()
    else:
      validate.validation_error(DENOM_0_ERR, fraction_type = "Real")


  # simplify() Simplifies a fraction to its lowest form
  # effects: modifies 'self.num' and 'self.denom'
  def simplify(self):
    if (self.num):
      gcd_val = gcd.eucli_algo(self.denom, self.num)
      self.num /= gcd_val
      self.denom /= gcd_val
      self.normalize()


  # is_neg_zero(n) Checks if n is a negative zero
  # required: n = 0
  def is_neg_zero(self, n: int) -> float:
    return math.copysign(1, n)


  # normalize() Sets all negatives to the numerator
  # effects: modifies 'self.num' and 'self.denom'
  def normalize(self):
    if (self.denom < 0):
      self.denom *= -1
      self.num*= -1


  # reciprocal() Computes the reciprocal of the fraction
  # effects: modifies 'self.num' and 'self.denom'
  def reciprocal(self):
    temp_num = self.num
    self.num = self.denom
    self.denom = temp_num
    self.normalize()


  # is_zero() Determines if the fraction is 0
  def is_zero(self) -> bool:
    if (self.num):
      return False
    else:
      return True


  # is_one() Determines if the fraction is 1
  def is_one(self) -> bool:
    if (self.num == self.denom):
      return True
    else:
      return False


  # print_frac() prints the fraction
  # effects: prints output
  def print_frac(self):
    print("(", end="")
    if ((not self.num) or (self.denom == 1)):
      if (not self.num and self.is_neg_zero(self.num) == -1):
        self.num *= -1

      print(self.num, end="")
    elif (self.denom == -1):
      self.num *= -1
      print(self.num, end="")
    else:
      print(f"{self.num}/{self.denom}", end="")
    print(")", end="")



# ComplexFraction: A complex number where the real and
#   imaginary parts are both fractions
class ComplexFraction:
  def __init__(self, num: Union[complex.Complex_Num, RealFraction], 
              denom: Union[complex.Complex_Num, RealFraction], divided: bool = False):
    if (not divided):
      if ((not denom.r) and (not denom.i)):
        validate.validation_error(DENOM_0_ERR, fraction_type = "Complex")
      else:
        result = complex.complex_divide(num, denom)
        self.r = RealFraction(result[0].r, result[1])
        self.i = RealFraction(result[0].i, result[1])
        self.simplify()
        self.normalize()
    else:
      self.r = num
      self.i = denom
      self.simplify()
      self.normalize()


  # simplify() Simplifies the fraction to its lowest form
  # effects: modifies 'self.r' and 'self.i'
  def simplify(self):
    self.r.simplify()
    self.i.simplify()
    self.normalize()


  # normalize() Sets the negative for the fractions only on the numerator
  # effects: modifies 'self.r' and 'self.i'
  def normalize(self):
    self.i.normalize()
    self.r.normalize()


  # conjugate() Computes the conjugate of the Complex fraction
  # effects: modifies 'self.i'
  def conjugate(self):
    self.i.num *= -1


  # is_zero() Determines if the complex fraction has the value of 0
  def is_zero(self) -> bool:
    if (self.i.is_zero() and self.r.is_zero()):
      return True
    else:
      return False


  # is_one() Determines if the complex fraction has the value of 1
  def is_one(self) -> bool:
    if (self.i.is_zero() and self.r.is_one()):
      return True
    else:
      return False


  # print_frac() prints the fraction
  # effects: prints output
  def print_frac(self):

    if (self.i.num):
      print("(", end="")

    self.r.print_frac()
    if (self.i.num):
      print(" + ", end="")
      self.i.print_frac()
      print("i", end="")

    if (self.i.num):
      print(")", end="")



# rf_add(a, b) Computes the operation of a + b or a - b for real fractions
# requires: 'sign' is either "+" or "-"
def rf_add(a: RealFraction, b: RealFraction, sign: str) -> RealFraction:
  if ((not a.num) and (not b.num)):
    lcm_denom = 1

  elif (not a.num):
    lcm_denom = b.denom

  elif ((not b.num) or (a.denom == b.denom)):
    lcm_denom = a.denom

  elif (a.denom != b.denom):
    lcm_denom = lcm.lcm(a.denom, b.denom)
    a_factor = lcm_denom / a.denom
    b_factor = lcm_denom / b.denom

    a.num *= a_factor
    b.num *= b_factor

  if (sign == "+"):
    result = RealFraction(a.num + b.num, lcm_denom)
  elif(sign == "-"):
    result = RealFraction(a.num - b.num, lcm_denom)

  result.simplify() 
  return result


# cf_add(a, b. sign) Computes the operation of a + b or a - b for complex fractions
# requires: 'sign' is either "+" or "-"
def cf_add(a: ComplexFraction, b: ComplexFraction, sign: str) -> ComplexFraction:
  result = ComplexFraction(rf_add(a.r, b.r, sign), rf_add(a.i, b.i, sign), True)
  result.simplify()
  return result


# rf_multiply(a, b) Computes the operation of a * b for real fractions
def rf_multiply(a: RealFraction, b: RealFraction) -> RealFraction:
  result = RealFraction(a.num * b.num, a.denom * b.denom)
  result.simplify()
  return result


#cf_multiply(a, b) Computes the operation of a * b for complex fractions
def cf_multiply(a: ComplexFraction, b: ComplexFraction) -> ComplexFraction:
  real_part = rf_add(rf_multiply(a.r, b.r), rf_multiply(a.i, b.i), "-")
  imaginary_part = rf_add(rf_multiply(a.r, b.i), rf_multiply(a.i, b.r), "+")
  result = ComplexFraction(real_part, imaginary_part, True)
  result.simplify()
  return result


# rf_multiply(a, b) Computes the operation of a / b for real fractions
# effects: may modify 'b'
def rf_divide(a: RealFraction, b: RealFraction) -> RealFraction:
  b.reciprocal()
  return rf_multiply(a, b)


# cf_multiply(a, b) Computes the operation of a / b for complex fractions
# effects: may modify 'b'
def cf_divide(a: ComplexFraction, b: ComplexFraction) -> ComplexFraction:
  temp_b = copy.deepcopy(b)
  b.conjugate()
  num_result = cf_multiply(a, b)
  denom_result = cf_multiply(temp_b, b)
  result_r = rf_divide(num_result.r, denom_result.r)
  denom_result.r.reciprocal()
  result_i = rf_divide(num_result.i, denom_result.r)
  b.conjugate()
  return ComplexFraction(result_r, result_i, True)


# r_get_zero() Makes the RealFraction with value 0
def r_get_zero() -> RealFraction:
  real_f_0 = RealFraction(0, 1)
  return real_f_0


# r_get_one() Makes the RealFraction with value 1
def r_get_one() -> RealFraction:
  real_f_1 = RealFraction(1, 1)
  return real_f_1


# c_get_zero() Makes the ComplexFraction with value 0
def c_get_zero() -> ComplexFraction:
  complex_1 = complex.Complex_Num(1, 0)
  complex_0 = complex.Complex_Num(0, 0)
  complex_f_0 = ComplexFraction(complex_0, complex_1)
  return complex_f_0


# c_get_one() Makes the ComplexFraction with value 1
def c_get_one() -> ComplexFraction:
  complex_1 = complex.Complex_Num(1, 0)
  complex_f_1 = ComplexFraction(complex_1, complex_1)
  return complex_f_1
