import copy
import complex
import fraction as frac
import sys
import enum
import vector as vect
import counting as count
from typing import Union, List, Dict, Callable, Optional

# OperationSym: Current Available Operations
class OperationSym(enum.Enum):
  Add = "+"
  Subtract = "-"
  ScalarMultiply = "*"
  Multiply = "x"
  GaussJordan = "gj"
  Inverse = "inv"
  Determinant = "det"
  Basis = "bas"
  Independent = "ind"
  BasisConvert = "bas_conv"
  TransBasisConvert = "tbas_conv"
  GenTransBasisConvert = "gen_tbas_conv"
  ChangeOfBasis = "cob"


# LinearEquation: Represents a linear equation
# requires: 'coefficients' is not empty
class LinearEquation:
  def __init__(self, coefficients: Union[List[frac.RealFraction], List[frac.ComplexFraction]], 
               answer: Union[frac.RealFraction, frac.ComplexFraction], num_type: frac.NumberType):
    self.coefficients = coefficients
    self.answer = answer
    self.num_type = num_type


  # scale_eq(index, factor) Scales the equation by 'factor'
  # effects: modifies 'self.answer' and 'self.coefficients'
  def scale_eq(self, factor: Union[frac.RealFraction, frac.ComplexFraction]):
    if (self.num_type == frac.NumberType.RealNum.value):
      self.answer = frac.rf_multiply(factor, self.answer)

      for i in range(len(self.coefficients)):
        self.coefficients[i] = frac.rf_multiply(factor, self.coefficients[i])

    elif (self.num_type == frac.NumberType.ComplexNum.value):
      self.answer = frac.cf_multiply(factor, self.answer)

      for i in range(len(self.coefficients)):
        self.coefficients[i] = frac.cf_multiply(factor, self.coefficients[i])


  #is_trivial(check_right) Determines whether the equation is trivial
  def is_trivial(self, check_right: bool = True) -> bool:
    co_all_zero = True

    for c in self.coefficients:
      if (not (c.is_zero())):
        co_all_zero = False
        break
    
    if (check_right):
      return co_all_zero and self.answer.is_zero()
    else:
      return co_all_zero


  # is_valid() Determines whether the equation is valid
  def is_valid(self) -> bool:
    lh_zero = self.is_trivial(False)
    rh_zero = self.answer.is_zero()
    
    if (lh_zero and not rh_zero):
      return False
    else:
      return True


  # print_eq() Prints the equation
  # effects: prints output
  def print_eq(self, print_rh: bool):
    for i in range(len(self.coefficients)):
      self.coefficients[i].print_frac()

      if (i < len(self.coefficients) - 1):
        print(" , ", end="")

    if (print_rh):
      print("\t|\t", end="")
      self.answer.print_frac()



# Matrix: represents a matrix
# requires: 'eqautions' is not empty
#           each LinearEquation in 'eqautions' has the same number of coefficients
class Matrix:
  def __init__(self, equations: List[LinearEquation], num_type: frac.NumberType, augumented: bool = True):
    self.equations = equations
    self.num_type = num_type
    self.augumented = augumented
    self.pivots = 0
    self.pivot_vects = []

    self.cols = len(self.equations[0].coefficients)
    self.rows = len(self.equations)

    self.inv_equations = []
    if (self.is_square() and not self.augumented):
      self.get_identity()


  # is_square() Determines if the matrix is a square matrix
  def is_square(self) -> bool:
    return (len(self.equations) == len(self.equations[0].coefficients))


  # get_identity() Gets the identity Matrix
  # effects: modifies 'self.inv_equations'
  def get_identity(self):
    if (self.is_square() and not self.augumented):
      len_m = len(self.equations)
      num_type = self.num_type
      real_num = frac.NumberType.RealNum.value
      complex_num = frac.NumberType.ComplexNum.value
      equation_arr = []

      real_f_0 = frac.r_get_zero()
      real_f_1 = frac.r_get_one()

      complex_f_0 = frac.c_get_zero()
      complex_f_1 = frac.c_get_one()

      for i in range(len_m):
        ans = None
        temp_coeff = [];

        if (self.num_type == real_num):
          temp_coeff = [copy.deepcopy(real_f_0)] * len_m
          temp_coeff[i] = copy.deepcopy(real_f_1)
          ans = copy.deepcopy(real_f_0)

        elif (self.num_type == complex_num):
          temp_coeff = [copy.deepcopy(complex_f_0)] * len_m
          temp_coeff[i] = copy.deepcopy(complex_f_1)
          ans = copy.deepcopy(complex_f_0)

        equation_arr.append(LinearEquation(temp_coeff, ans, num_type))

      self.inv_equations = copy.deepcopy(equation_arr)

    else:
      self.matrix_err(2)


  # get_rank() Gets the rank of the matrix
  def get_rank(self) -> int:
    rank = 0
    for e in self.equations:
      if (not e.is_trivial(False)):
        rank += 1

    return rank


  # matrix_err(err_code, pivot_row) error message about a specific matrix
  # requires: 0 <= row < len(self.equations)
  #           1 <= err_code <= 4
  # effects: ends the program after displaying the error message
  def matrix_err(self, err_code: int, row: int = 0):
    message = "ERROR: "
    after_message = ""
    if (err_code == 1):
      message += f"Equation {row + 1}, where\n"
      after_message += "\n\nis not consistent\n\n"
    elif (err_code == 2):
      message += "The Following Matrix, where\n"
      after_message += "\n\nis not a square matrix\n\n"
    elif (err_code == 3):
      message += "The Following Matrix, where\n"
      after_message += "\n\nis Singular (Not Invertible)\n\n"
    elif (err_code == 4):
      message += "The Following Matrix, where\n"
      after_message += "\n\nis an Augumented Matrix"
    
    print(message)

    if (err_code == 1):
      self.equations[row].print_eq(True)
    elif (err_code == 2 or err_code == 4):
      self.print_matrix()
    elif (err_code == 3):
      self.print_inverse()

    after_message += "Ending Program..."
    print(after_message)

    sys.exit()


  # get_column(col) Gets all the entries from column 'col' in the
  #   matrix
  # requires: 0 <= col < len(self.equations[0].coefficients)
  def get_column(self, col: int) -> int:
    column = []

    for i in range(len(self.equations)):
      column.append(self.equations[i].coefficients[col])

    return column


  # do_ero(type, **kwargs) Performs Elementary Row operation type 'type' 
  #   on the matrix
  # requires: 1 <= ero_type <= 3
  # effects: modifies 'self.equations' and 'self.inv_equations'
  #          may print output
  def do_ero(self, ero_type: int, **kwargs):
    if (ero_type == 1):
      self.swap_eq(self.equations, kwargs["current_i"], kwargs["i_to_swap"], kwargs["verbose"])

      if (self.inv_equations):
        self.swap_eq(self.inv_equations, kwargs["current_i"], kwargs["i_to_swap"], False)

    elif (ero_type == 2):
      self.scale_eq(self.equations, kwargs["index"], kwargs["factor"], kwargs["verbose"])

      if (self.inv_equations):
        self.scale_eq(self.inv_equations, kwargs["index"], kwargs["factor"], False)

    elif (ero_type == 3):
      self.difference(self.equations, kwargs["i_1"], kwargs["i_2"], kwargs["factor_2"], kwargs["verbose"])

      if (self.inv_equations):
        self.difference(self.inv_equations, kwargs["i_1"], kwargs["i_2"], kwargs["factor_2"], False)


  # swap_eq(equations, current_i, i_to_swap, verbose) Swaps 2 rows/equations in the matrix
  # requires: 'equations' is not empty
  #           0 <= current_i < len(equations)
  #           0 <= i_to_swap < len(equations)
  # effects: modifies 'equations'
  #          may print output
  def swap_eq(self, equations: List[LinearEquation], current_i: int, i_to_swap: int, verbose: bool = True):
    temp_eq = copy.deepcopy(equations[current_i])
    equations[current_i] = copy.deepcopy(equations[i_to_swap])
    equations[i_to_swap] = copy.deepcopy(temp_eq)

    if (verbose):
      print(f"ERO Type I: R{current_i + 1} <--> R{i_to_swap + 1}")


  # scale_eq(equations, index, factor, verbose) Scales an an equation by 'factor'
  # requires: 'equations' is not empty
  #           0 <= index < len(equations)
  # effects: modifies 'equations'
  #          may print output
  def scale_eq(self, equations: List[LinearEquation], index: int, 
              factor: Union[frac.RealFraction, frac.ComplexFraction], verbose = True):

    if (not factor.is_one()):
      equations[index].scale_eq(factor)

      if (verbose):
        print(f"ERO Type II: R{index + 1} --> ", end="")
        factor.print_frac()
        print(f"R{index + 1}")


  # difference(equations, i_i, i_2, factor_2, verbose) Computes the difference between equation i_1 and 
  #   equation i_2 that is scaled by 'factor_2'
  # requires: 'equations' is not empty
  #           0 <= i_1 < len(equations)
  #           0 <= i_2 < len(equations)
  # effects: modifies 'equations'
  #          may print output
  def difference(self, equations: List[LinearEquation], i_1: int, i_2: int, 
                 factor_2: Union[frac.RealFraction, frac.ComplexFraction], verbose: bool = True):
    if (not factor_2.is_zero()):
      scaled_subtrahend = copy.deepcopy(equations[i_2])
      scaled_subtrahend.scale_eq(factor_2)

      if (self.num_type == frac.NumberType.RealNum.value):
        equations[i_1].answer = frac.rf_add(equations[i_1].answer, scaled_subtrahend.answer, "-")

        for i in range(len(scaled_subtrahend.coefficients)):
          equations[i_1].coefficients[i] = frac.rf_add(equations[i_1].coefficients[i], scaled_subtrahend.coefficients[i], "-")

      elif (self.num_type == frac.NumberType.ComplexNum.value):
        equations[i_1].answer = frac.cf_add(equations[i_1].answer, scaled_subtrahend.answer, "-")

        for i in range(len(scaled_subtrahend.coefficients)):
          equations[i_1].coefficients[i] = frac.cf_add(equations[i_1].coefficients[i], scaled_subtrahend.coefficients[i], "-")

      if (verbose):
        print(f"ERO Type III: R{i_1 + 1} --> R{i_1 + 1} - ", end="")
        factor_2.print_frac()
        print(f"R{i_2 + 1}")


  # normalize(index, pivot, verbose) Scales the 'index'th equation by a factor in order to make the 'pivot' 1
  # requires: 0 <= index < len(self.equations)
  #           0 <= pivot <= len(self.equations[0].coefficients)
  # effects: modifies 'self.equations'
  #          may print output
  def normalize(self, index: int, pivot: int, verbose: bool = True):
    if (self.num_type == frac.NumberType.RealNum.value):
      factor = copy.deepcopy(self.equations[index].coefficients[pivot])
      factor.reciprocal()
    elif (self.num_type == frac.NumberType.ComplexNum.value):
      num = frac.ComplexFraction(complex.Complex_Num(1, 0), complex.Complex_Num(1, 0))
      factor = frac.cf_divide(num, self.equations[index].coefficients[pivot])

    kwargs = {"index": index, "factor": factor, "verbose": verbose}
    self.do_ero(2, **kwargs)


  # eliminate(index, pivot_row, pivot_col, verbose) Turns the 'pivot_col'th coefficient of the 'index'th 
  #   equation to 0
  # requires: 0 <= index < len(self.equations)
  #           0 <= pivot_row <= len(self.equations[0].coefficients)
  #           0 <= pivot_col <= len(self.equations[0].coefficients)
  # effects: modifies 'self.equations'
  #          may print output
  def eliminate(self, index: int, pivot_row: int, pivot_col: int, verbose: bool = True):
    if (self.num_type == frac.NumberType.RealNum.value):
      factor = frac.rf_divide(self.equations[index].coefficients[pivot_col], 
                              self.equations[pivot_row].coefficients[pivot_col])
    elif (self.num_type == frac.NumberType.ComplexNum.value):
      factor = frac.cf_divide(self.equations[index].coefficients[pivot_col],
                              self.equations[pivot_row].coefficients[pivot_col]) 
    kwargs = {"i_1": index, "i_2": pivot_row, "factor_2": factor, "verbose": verbose}
    self.do_ero(3, **kwargs)


  # find_pivot(pivot_row, pivot_col, verbose) Finds a pivot in the column 'pivot_col'
  # requires: 0 <= pivot_row <= len(self.equations[0].coefficients)
  #           0 <= pivot_col <= len(self.equations[0].coefficients) 
  # effects:  may print output
  def find_pivot(self, pivot_row: int, pivot_col: int, verbose: bool = True) -> Dict[str, int]:
    for i in range(pivot_row + 1, len(self.equations)):
      if (not self.equations[i].coefficients[pivot_col].is_zero()):
        kwargs = {"current_i": pivot_row, "i_to_swap": i, "verbose": verbose}
        self.do_ero(1, **kwargs)
        return {"row": pivot_row, "col": pivot_col}

    return {}


  # get_pivot(pivot_row, algorithm) Gets the pivot for 'pivot_row' for the specific algorithm
  # requires: 0 <= pivot_row <= len(self.equations[0].coefficients)
  #           'algorithm' is either "gauss" or "jordan"
  # effects: may print output
  def get_pivot(self, pivot_row: int, algorithm: str, verbose: bool = True) -> Dict[str, int]:
    pivot_found = False;
    found_pivot = {};

    if (algorithm == "gauss"):
      while (pivot_row <= len(self.equations) - 1):
        if (not self.equations[pivot_row].is_valid()):
          self.matrix_err(1, pivot_row)

        # retrieve the pivot
        if (not self.equations[pivot_row].is_trivial()):
          for pivot_col in range(len(self.equations[0].coefficients)):
            if (not(self.equations[pivot_row].coefficients[pivot_col].is_zero())):
              found_pivot["row"] = pivot_row
              found_pivot["col"] = pivot_col;
              pivot_found = True;
              break
            
            else:
              found_pivot = self.find_pivot(pivot_row, pivot_col, verbose)

              if(found_pivot):
                pivot_found = True;
                break

          if(pivot_found):
            break

        # find for a non-trivial equation to swap with the trivial equation
        else:
          eq_found = False
          for i in range(pivot_row + 1, len(self.equations)):
            if (not self.equations[i].is_trivial()):
              eq_found = True
              kwargs = {"current_i": pivot_row, "i_to_swap": i, "verbose": verbose}
              self.do_ero(1, **kwargs)
              break

          if (eq_found):
            pivot_row -= 1
              
        pivot_row += 1;

    elif (algorithm == "jordan"):
      while (pivot_row > 0):
        if (not self.equations[pivot_row].is_valid()):
          self.matrix_err(1, pivot_row)

        if (not self.equations[pivot_row].is_trivial()):
          for pivot_col in range(len(self.equations[0].coefficients)):
            if (not(self.equations[pivot_row].coefficients[pivot_col].is_zero())):
              found_pivot["row"] = pivot_row
              found_pivot["col"] = pivot_col;
              pivot_found = True;
              break

          if(pivot_found):
            break

        pivot_row -= 1;

    return found_pivot


  # gaussian_elimination(get_inv, verbose) Computes the Gauss part of the Gauss-Jordan Algorithm for Matrices
  # effects: may print output
  #          modifies 'self.equations' and 'self.inv_equations'
  def gaussian_elimination(self, get_inv: bool = False, verbose: bool = True):
    pivot_col = 0
    pivot_row = 0

    while (pivot_row < len(self.equations) - 1):
      
      if (verbose):
        print("")
        if (not get_inv):
          self.print_matrix()
        else:
          self.print_inverse()
        print("\n")

      if (pivot_col >= len(self.equations[0].coefficients)):
        break;

      pivot = self.get_pivot(pivot_row, "gauss", verbose)

      if (pivot):
        pivot_row = pivot["row"]
        pivot_col = pivot["col"]
        self.normalize(pivot_row, pivot_col, verbose)

        for i in range(pivot_row + 1, len(self.equations)):
          self.eliminate(i, pivot_row, pivot_col, verbose) 
      else:
        break

      pivot_row += 1
      pivot_col += 1

    if (not self.equations[pivot_row].is_trivial() and self.equations[pivot_row].is_valid()):
      pivot = self.get_pivot(pivot_row, "gauss", verbose)

      if (pivot):
        pivot_row = pivot["row"]
        pivot_col = pivot["col"]
        self.normalize(pivot_row, pivot_col, verbose)


  # jordan_algo(get_inv, verbose) Computes the Jordan Algorithm for the back substitution of the matrix
  # effects: may print output
  #          modifies 'self.equations' and 'self.inv_equations'
  def jordan_algo(self, get_inv: bool = False, verbose: bool = True):
    pivot_row = len(self.equations) - 1
    pivot_col = 0

    while (pivot_row > 0):
      pivot = self.get_pivot(pivot_row, "jordan", verbose)

      if (pivot):
        pivot_row = pivot["row"]
        pivot_col = pivot["col"]
        self.pivots += 1
        self.pivot_vects.insert(0, pivot_col)
        for i in range(pivot_row - 1, -1, -1):
          self.eliminate(i, pivot_row, pivot_col, verbose)

      if (verbose):
        print("")
        if (not get_inv):
          self.print_matrix()
        else:
          self.print_inverse()
        print("\n")

      pivot_row -= 1
      pivot_col -= 1

    self.pivots += 1
    self.pivot_vects.insert(0, 0)


  # gauss_jordan(get_inv, verbose) computes the gauss-jordan algorithm
  # effects: may print output
  #          modifies 'self.equations' and 'self.inv_equations'
  def gauss_jordan(self, get_inv = False, verbose = True):
    if (verbose):
      print("\n------- Gaussian Elimination ---------")
    self.gaussian_elimination(get_inv, verbose)
    
    if (verbose):
      print()

    if (verbose):
      if (not get_inv):
        self.print_matrix()
      else:
        self.print_inverse()

    if (get_inv and (self.get_rank() != len(self.equations))):
      self.matrix_err(3)
    
    if (verbose):
      print("\n-------- Jordan's Algorithm ----------\n")
    self.jordan_algo(get_inv, verbose)

    if (verbose):
      if (not get_inv):
        self.print_matrix()
      else:
        self.print_inverse()


  # print_matrix() Prints out the matrix
  # effects: prints output
  def print_matrix(self):
    for e in self.equations:
      e.print_eq(self.augumented)
      print("")


  # print_inver() Prints a matrix and its inverse
  def print_inverse(self):
    if (self.is_square and not self.augumented):
      for i in range(len(self.equations)):
        self.equations[i].print_eq(self.augumented)
        print(" | ", end="")
        self.inv_equations[i].print_eq(self.augumented)
        print("")
  
    else:
      self.matrix_err(2)



# m_error(signal) Error messages for operations between matrices
# effects: prints output
#          ends the program after displaying error message
def m_error(signal: int):
  message = "ERROR "

  if (signal == 1):
    message += "The columns in both matrices do not match"
  elif (signal == 2):
    message += "The rows in both matrices do not match"
  elif (signal == 3):
    message += "Both matrices do not have the same size"
  elif (signal == 4):
    message += "The number of columns in the first matrix does not match the number of rows in the second matrix"
  elif (signal == 5):
    message += "The size of the vectors do not match"

  print(f"\n\n{message}\n\n\n\nEnding Program...")
  sys.exit()


# check(a, b, check_type) Error check for matrix arithmetic
# requires: 'check_type' is either "col", "row", "size" or "col-row"
# effects: may end the program
def check(a: Matrix, b: Matrix, check_type: str):
  a_col = len(a.equations[0].coefficients)
  b_col = len(b.equations[0].coefficients)
  a_row = len(a.equations)
  b_row = len(b.equations)

  row_check = a_row != b_row
  col_check = a_col != b_col

  if (check_type == "col" and col_check):
    m_error(1)
  elif(check_type == "row" and row_check):
    m_error(2)
  elif(check_type == "size" and (row_check or col_check)):
    m_error(3)
  elif(check_type == "col-row" and (a_col != b_row)):
    m_error(4)


# m_arith(op, a, b, check_type) Checks if performing 'op' is valid
#   for matrix 'a' and 'b'
# effects: may end the program
def m_arith(op: Callable[[Matrix, Matrix, Optional[str]], Matrix], a: Matrix, b: Matrix, 
            check_type: str, adding: bool = False, sign: str = "+") -> Matrix:
  check(a, b, check_type)

  if (not adding):
    return op(a, b)
  else:
    return op(a, b, sign)


# m_add(a, b, op) Adds or subtracts 2 matrices
# requires: 'op' is either "+" or "-"
def m_add(a: Matrix, b: Matrix, op: str) -> Matrix:
  equations = []
  augumented = a.augumented
  num_type = a.num_type
  subtract = OperationSym.Subtract.value
  real_num = frac.NumberType.RealNum.value
  complex_num = frac.NumberType.ComplexNum.value

  for i in range(len(a.equations)):
    temp_coeff = []
    answer = None

    for j in range(len(a.equations[0].coefficients)):
      sum = 0
      sign = "+"

      if (op == subtract):
        sign = "-"

      if (num_type == real_num):
        sum = frac.rf_add(a.equations[i].coefficients[j], b.equations[i].coefficients[j], sign)
      elif(num_type == complex_num):
        sum = frac.cf_add(a.equations[i].coefficients[j], b.equations[i].coefficients[j], sign)

      temp_coeff.append(sum)

    if (augumented):
      if (num_type == real_num):
        answer = frac.rf_add(a.equations[i].answer, b.equations[i].answer, sign)
      elif (num_type == complex_num):
        answer = frac.cf_add(a.equations[i].answer, b.equations[i].answer, sign)

    equations.append(LinearEquation(temp_coeff, answer, num_type))

  return Matrix(equations, num_type, augumented)
        

# m_multiply(a, b) Computes matrix multiplication of ab
def m_multiply(a: Matrix, b: Matrix) -> Matrix:
  equations = []
  augumented = a.augumented
  num_type = a.num_type

  for i in range(len(a.equations)):
    temp_coeff = []
    answer = 0

    for j in range(len(b.equations[0].coefficients)):
      temp_a = a.equations[i].coefficients
      temp_b = b.get_column(j)
      dp_result = vect.dot_product(temp_a, temp_b, num_type, False)
      temp_coeff.append(dp_result)

    equations.append(LinearEquation(temp_coeff, answer, num_type))

  return Matrix(equations, num_type, augumented)


# m_smultiply(a, c) Performs scalar matrix multiplication of ca
def m_smultiply(a: Matrix, c: Union[frac.RealFraction, frac.ComplexFraction]) -> Matrix:
  for i in range(len(a.equations)):
    kwargs = {"index": i, "factor": c, "verbose": False}
    a.do_ero(2, **kwargs)


# sub_sq_matrix(a, i, j) Finds the M_ij matrix of a
# requires: 0 <= i_row < len(a.equations)
#           0 <= j_col < len(a.equations[0].coefficients)
# effects: may end the program
def sub_sq_matrix(a: Matrix, i_row: int, j_col: int) -> Matrix:
  is_square = a.is_square()

  if (is_square and not a.augumented):
    equations = [];

    for i in range(len(a.equations)):
      if (i != i_row):

        temp_coeff = [];
        for j in range(len(a.equations[0].coefficients)):
          if (j != j_col):
            temp_coeff.append(a.equations[i].coefficients[j]);

        equations.append(LinearEquation(temp_coeff, 0, a.num_type))

    return Matrix(equations, a.num_type, a.augumented)

  elif (not is_square):
    a.matrix_err(2);

  else:
    a.matrix_err(4);


# cofactor(a, i_row, j_col) Gets the cofactor of a
# requires: 0 <= i_row < len(a.equations)
#           0 <= j_col < len(a.equations[0].coefficients)
def cofactor(a: Matrix, i_row: int, j_col: int) -> Matrix:
  if (not (((i_row + 1) + (j_col + 1)) % 2)):
    is_one = True
  else:
    is_one = False

  sign = None
  if (a.num_type == frac.NumberType.RealNum.value):
    sign = frac.r_get_one()
    entry = a.equations[i_row].coefficients[j_col]

    if (not is_one):
      zero = frac.r_get_zero()
      sign = frac.rf_add(zero, sign, "-")

    result = frac.rf_multiply(sign, entry)
    sub_m = sub_sq_matrix(a, i_row, j_col)
    determinant = det(sub_m)

    result = frac.rf_multiply(result, determinant)
    return result
  
  elif (a.num_type == frac.NumberType.ComplexNum.value):
    sign = frac.c_get_one()
    
    if (not is_one):
      zero = frac.c_get_zero()
      sign = frac.cf_add(zero, sign, "-")

    result = frac.cf_multiply(sign, entry)
    sub_m = sub_sq_matrix(a, i_row, j_col)
    determinant = det(sub_m)

    result = frac.cf_multiply(result, determinant)
    return result


# det(a) Finds the determinant of a
def det(a: Matrix) -> Union[frac.RealFraction, frac.ComplexFraction]:
  is_square = a.is_square()

  if (is_square and not a.augumented):
    size = len(a.equations)
    row = 0

    if (size == 1):
      return a.equations[0].coefficients[0]
    elif (size == 2):
      w = a.equations[0].coefficients[0]
      x = a.equations[0].coefficients[1]
      y = a.equations[1].coefficients[0]
      z = a.equations[1].coefficients[1]
      result = None

      if (a.num_type == frac.NumberType.RealNum.value):
        result = frac.rf_add(frac.rf_multiply(w, z), 
                             frac.rf_multiply(x, y), "-")
      elif (a.num_type == frac.NumberType.ComplexNum.value):
        result = frac.cf_add(frac.cf_multiply(w, z), 
                             frac.cf_multiply(x, y), "-")

      return result

    else:
      if (a.num_type == frac.NumberType.RealNum.value):
        sum = frac.r_get_zero()
      elif (a.num_type == frac.NumberType.ComplexNum.value):
        sum = frac.c_get_zero()

      for j in range(size):
        temp_cofact = cofactor(a, row, j)
        
        if (a.num_type == frac.NumberType.RealNum.value):
          sum = frac.rf_add(sum, temp_cofact, "+")
        elif (a.num_type == frac.NumberType.ComplexNum.value):
          sum = frac.cf_add(sum, temp_cofact, "+")

      return sum
  elif (not is_square):
    a.matrix_err(2);

  else:
    a.matrix_err(4);


# matrix_from_vects(lo_vects) Makes a new matrix from a 'lo_vects'
# requires: lo_vects is not empty
def matrix_from_vects(lo_vects: List[List[int]], num_type: frac.NumberType) -> Matrix:
  vect_size = len(lo_vects[0])
  no_of_vects = len(lo_vects)
  equations = []
  
  if (num_type == frac.NumberType.RealNum.value):
    answer = frac.r_get_zero()
  elif (num_type == frac.NumberType.ComplexNum.value):
    answer = frac.c_get_zero()

  for i in range(vect_size):
    temp_coeff = []
    for j in range(no_of_vects):
      try:
        temp_coeff.append(lo_vects[j][i])
      except:
        m_error(5)

    equations.append(LinearEquation(temp_coeff, answer, num_type)) 

  result = Matrix(equations, num_type, augumented = False) 
  return result


# print_original_vect_set(m) Prints m and its columns
# effects: prints output
def print_original_vect_set(m: Matrix):
  columns = [i for i in range(len(m.equations[0].coefficients))]

  print(f"Original Set of Vectors: {columns}\nMatrix:\n")
  m.print_matrix()
      

# get_lin_indep(m, no_vects, result) gets all the linear independent vectors with 'no_vects' of vectors
#   from the matrix 'm'
# requires: 0 <= no_vects <= len(m.equations[0].coefficients)
def get_lin_indep(m: Matrix, no_vects: int, result: List[List[int]]) -> List[List[int]]:
  current_combo = []
  available_vects = []
  num_type = m.num_type
  for i in range(m.cols):
    current_combo.append(i)
    temp_col = copy.deepcopy(m.get_column(i)) 
    available_vects.append(temp_col)


  vect_combos = count.combination(current_combo, m.cols, no_vects)

  for i in range(len(vect_combos)):
    temp_vects = []
    print(f"Set of Vectors: {vect_combos[i]}")
    print("Matrix:")

    for j in range(no_vects):
      current_vect = copy.deepcopy(available_vects[vect_combos[i][j]])
      temp_vects.append(current_vect)

    temp_matrix = matrix_from_vects(temp_vects, num_type)
    temp_matrix.print_matrix()
    print()
    temp_matrix.gauss_jordan(verbose = False)

    print("Conclusion: ", end = "")
    if (temp_matrix.pivots == temp_matrix.cols):
      for j in range(no_vects):
        vect_combos[i][j] += 1
      result.append(vect_combos[i])
      print("Independent")
    else:
      print("Dependent")
    print()
  
  return result


# get_lin_indep_combo(m, result) Get all linear independent vector
#    combinations for matrix 'm'
# effects: prints output
def get_lin_indep_combo(m: Matrix, result: List[List[int]]) -> List[List[int]]:
  print_original_vect_set(m)

  for i in range (m.rows, 0, -1):
    print(f"\nNo. of Vectors in Matrix: {i}\n")
    result = get_lin_indep(m, i, result)

  result.append([])
  return result


# get_cob_matrix(m_1, m_2) Gets the Change of Basis Matrix from 'm_1'
#   to 'm_2'
# effects: prints output
def get_cob_matrix(m_1: Matrix, m_2: Matrix) -> Matrix:
  if (not m_1.is_square()):
    m_1.matrix_err(2)

  if (not m_2.is_square()):
    m_2.matrix_err(2)

  m_1_equations = copy.deepcopy(m_1.equations)
  m_2.inv_equations = m_1_equations
  m_2.gauss_jordan(True, False)

  cob_equations = copy.deepcopy(m_2.inv_equations)
  cob_num_type = m_2.num_type
  cob_augumented = False

  return Matrix(cob_equations, cob_num_type, cob_augumented)


# basis_convert(m_1, basis_1, basis_2) Converts 'm_1' of 'basis_1' to 
#   'basis_2'
# effects: may end the program
#          prints output
def basis_convert(m_1: Matrix, basis_1: Matrix, basis_2: Matrix) -> Matrix:
  if ((basis_1.cols != basis_2.cols) or 
      (basis_1.rows != basis_2.rows)):
    m_error(5)

  cob_m = get_cob_matrix(copy.deepcopy(basis_1), 
                         copy.deepcopy(basis_2))

  print("Change of Basis from old basis A to new basis B (B_[I]_A):")
  cob_m.print_matrix()

  result = m_multiply(cob_m, m_1)
  return result


# t_basis_convert(t, basis_1, basis_2) Converts matrix representation 
#   of transformation 't' of 'basis_1' to 'basis_2' 
# effects: may end the program
#          prints output
def t_basis_convert(t: Matrix, basis_1: Matrix, basis_2: Matrix) -> Matrix:
  if ((basis_1.cols != basis_2.cols) or 
      (basis_1.rows != basis_2.rows)):
    m_error(5)

  cob_m = get_cob_matrix(copy.deepcopy(basis_2), 
                         copy.deepcopy(basis_1))
  print("Change of Basis from new basis B to old basis A (A_[I]_B):")
  cob_m.print_matrix()
  inv_cob_m = get_cob_matrix(copy.deepcopy(basis_1), 
                             copy.deepcopy(basis_2))

  print("\nChange of Basis from old basis A to new basis B (B_[I]_A):")
  inv_cob_m.print_matrix()

  result = m_multiply(inv_cob_m, t)
  result = m_multiply(result, cob_m)
  return result


# gen_t_basis_convert(t, basis_1, basis_2, basis_3, basis_4) Converts matrix representation 
#   of transformation 't' that maps from basis_1 to basis_2 to the matrix representation
#   of the transformation that maps from basis_3 to basis_4
# effects: may end the program
#          prints output
def gen_t_basis_convert(t: Matrix, basis_1: Matrix, basis_2: Matrix, basis_3: Matrix, 
                        basis_4: Matrix) -> Matrix:
  if ((basis_1.cols != basis_3.cols) or 
      (basis_1.rows != basis_3.rows) or
      (basis_2.cols != basis_4.cols) or 
      (basis_2.rows != basis_4.rows)):
    m_error(5)

  cob_m = get_cob_matrix(copy.deepcopy(basis_3), 
                         copy.deepcopy(basis_1))
  print("Change of Basis from basis C to basis A (A_[I]_C):")
  cob_m.print_matrix()
  inv_cob_m = get_cob_matrix(copy.deepcopy(basis_2), 
                             copy.deepcopy(basis_4))

  print("\nChange of Basis from basis B to basis D (D_[I]_B):")
  inv_cob_m.print_matrix()

  result = m_multiply(inv_cob_m, t)
  result = m_multiply(result, cob_m)
  return result
