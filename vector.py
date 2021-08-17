import fraction as frac
import complex as comp
from typing import List, Union

# dot_product(a, b, num_type) Computes the dot product of the vectors 
#   'a' and 'b'
def dot_product(a: Union[List[frac.RealFraction], List[frac.ComplexFraction]],
                b: Union[List[frac.RealFraction], List[frac.ComplexFraction]], 
                num_type: frac.NumberType, conj: bool = True) -> Union[frac.RealFraction, frac.ComplexFraction]:
  real_num = frac.NumberType.RealNum.value
  complex_num = frac.NumberType.ComplexNum.value

  if (num_type == real_num):
    result = frac.RealFraction(0,1)
  elif (num_type == complex_num):
    result = frac.ComplexFraction(comp.Complex_Num(0,0), comp.Complex_Num(1, 0))

  for i in range(len(a)):
    if (num_type == real_num):
      temp_product = frac.rf_multiply(a[i], b[i])
      result = frac.rf_add(result, temp_product, "+")

    elif(num_type == complex_num):
      if (conj):
        temp_a = a[i]
        temp_b = b[i]
        temp_b.conjugate()

        temp_product = frac.cf_multiply(temp_a, temp_b)
        result = frac.cf_add(result, temp_product, "+")
      else:
        temp_product = frac.cf_multiply(a[i], b[i])
        result = frac.cf_add(result, temp_product, "+")

  return result
