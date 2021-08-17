import matrix
import validate
import complex
import fraction as frac
from typing import Union
import string as StringTools

FRACTION_ERR_CODE = 1
MATRIX_COL_ERR_CODE = 3

FIELD_VALS = ["r", "c"]
YES_NO_VALS = ["y", "n"]

FRAC_PT_ONE = {frac.NumberType.RealNum.value: 1,
               frac.NumberType.ComplexNum.value: "1 + 0i"}


# fraction_input(input, field) Organizes the input for a fraction
# required: 'field' is either "R", "r", "C" or "c"
# effects: may end the program if there is an invalid input
def fraction_input(input: str, field: str) -> Union[frac.RealFraction, frac.ComplexFraction]:
  temp_frac_pt = input.split("/")
  temp_frac_pt_len = len(temp_frac_pt)
  field = field.lower()

  if(temp_frac_pt_len > 2 or temp_frac_pt_len <= 0):
    validate.validation_error(FRACTION_ERR_CODE, input = input, type_article = "a", 
                              type = "valid fraction input")
  elif (temp_frac_pt_len == 1):
    temp_frac_pt.append(FRAC_PT_ONE[field])

  if (field.lower() == frac.NumberType.RealNum.value):
    temp_frac_pt = validate.validate_lst(temp_frac_pt, validate.DataTypes.Integer)
    temp_frac = frac.RealFraction(temp_frac_pt[0], temp_frac_pt[1])

  elif (field.lower() == frac.NumberType.ComplexNum.value):
    temp_frac_pt[0] = temp_frac_pt[0].replace("i", "")
    temp_frac_pt[0] = temp_frac_pt[0].split("+")
    temp_frac_pt[1] = temp_frac_pt[1].replace("i", "")
    temp_frac_pt[1] = temp_frac_pt[1].split("+")

    temp_frac_pt[0] = validate.validate_lst(temp_frac_pt[0], validate.DataTypes.Integer)
    temp_frac_pt[1] = validate.validate_lst(temp_frac_pt[1], validate.DataTypes.Integer)

    temp_frac = frac.ComplexFraction(complex.Complex_Num(temp_frac_pt[0][0], temp_frac_pt[0][1]),
                                     complex.Complex_Num(temp_frac_pt[1][0], temp_frac_pt[1][1]))

  return temp_frac


# matrix_input(field) Organizes the input for a matrix
# required: 'field' is either "R", "r", "C" or "c"
# effects: asks for input
#          prints out output
#          may end the program if there is an incorrect input
#             in the client's input
def matrix_input(field: str, augumented: str ,no: int = 1, m_type:str = "matrix") -> matrix.Matrix:
  print(f"\n----- Matrix {no} -----\n")

  row = input(f"Enter the number of rows in the {m_type}:\t")
  row = validate.validate_nat(row)
  col = input(f"Enter the number of columns in the {m_type}:\t")
  col = validate.validate_nat(col)

  if (augumented.lower() == "y"):
    is_augumented = True
  elif (augumented.lower() == "n"):
    is_augumented = False

  matrix_eq = []

  for i in range(row):
    temp_input_co = input(f"\nEnter the coefficients for Equation {i + 1}:\t")
    temp_input_co = (temp_input_co.strip()).split(",")

    temp_co= []
    temp_co_len = len(temp_input_co)

    # format the coefficients for each equation in the matrix
    for i in range(temp_co_len):
      temp_frac = fraction_input(temp_input_co[i], field)
      temp_co.append(temp_frac) 

    if (len(temp_co) == col):
      # format the answer for each equation in the matrix
      if (is_augumented):
        temp_ans = input(f"Enter the answer for Equation {i + 1}:\t")
        temp_ans = fraction_input(temp_ans, field)

      else:
        if (field.lower() == frac.NumberType.RealNum.value):
          temp_ans = frac.r_get_zero()
        elif (field.lower() == frac.NumberType.ComplexNum.value):
          temp_ans = frac.c_get_zero()

      temp_eq = matrix.LinearEquation(temp_co, temp_ans, field)
      matrix_eq.append(temp_eq)
    else:
      validate.validation_error(MATRIX_COL_ERR_CODE)

  # make the matrix
  print("\n--------------------\n")
  matrix_input = matrix.Matrix(matrix_eq, field, is_augumented)
  return matrix_input





#####################
# Enter Input Here #
####################

field = input("Enter a field (R, C) :\t")
field = field.strip()
field = validate.validate_str(field, FIELD_VALS)


num_of_matrices = input("Enter the number of matrices to calculate:\t")
num_of_matrices = validate.validate_nat(num_of_matrices)


# ask if the matrices are augumented
augumented = input("Are the Matrices Augumented? (y,n):\t")
augumented = augumented.strip()
augumented = augumented.lower()
augumented = validate.validate_str(augumented, YES_NO_VALS)

#ask the user the operation they would like to enter
question = "Enter an operation ("
all_operation = [e.value for e in matrix.OperationSym]

single_matrix_operations = [matrix.OperationSym.GaussJordan.value,
                            matrix.OperationSym.ScalarMultiply.value, matrix.OperationSym.Inverse.value, matrix.OperationSym.Determinant.value,
                            matrix.OperationSym.Basis.value,
                            matrix.OperationSym.Independent.value]

duo_matrix_operations = [matrix.OperationSym.ChangeOfBasis.value]
trip_matrix_operations = [matrix.OperationSym.BasisConvert.value,
                          matrix.OperationSym.TransBasisConvert.value] 

non_augumented_operations = [matrix.OperationSym.Multiply.value, 
                             matrix.OperationSym.Determinant.value]
quint_matrix_operations = [matrix.OperationSym.GenTransBasisConvert.value]

valid_operations = []
for i in range(len(all_operation)):
  single_operation = (all_operation[i] in single_matrix_operations)
  non_aug_operation = (all_operation[i] in non_augumented_operations)
  duo_operation = (all_operation[i] in duo_matrix_operations)
  trip_operation = (all_operation[i] in trip_matrix_operations)
  quint_operation = (all_operation[i] in quint_matrix_operations)

  if ((num_of_matrices == 1) and not single_operation):
    continue
  elif (num_of_matrices > 1 and single_operation):
    continue
  elif (num_of_matrices != 2 and duo_operation):
    continue
  elif (num_of_matrices != 3 and trip_operation):
    continue
  elif (num_of_matrices != 5 and quint_operation):
    continue
  elif (augumented == YES_NO_VALS[0] and non_aug_operation):
    continue
    
  valid_operations.append(all_operation[i])

question += f"{StringTools.format_lst(valid_operations)}) :\t"

operation = input(question)
operation = operation.strip()
operation = operation.lower()
operation = validate.validate_str(operation, valid_operations)

lo_matrices = []
for i in range(num_of_matrices):
  if ((operation == matrix.OperationSym.BasisConvert.value or 
       operation == matrix.OperationSym.TransBasisConvert.value) and 
       i):
    if (i == 1):
      temp_matrix = matrix_input(field, augumented, i+1, "original basis")
    elif (i == 2):
      temp_matrix = matrix_input(field, augumented, i+1, "new basis")
  elif (operation == matrix.OperationSym.ChangeOfBasis.value):
    if (i == 0):
      temp_matrix = matrix_input(field, augumented, i+1, "original basis")
    elif (i == 1):
      temp_matrix = matrix_input(field, augumented, i+1, "new basis")

  elif (operation == matrix.OperationSym.GenTransBasisConvert.value):
    print("\nfor the equation:\nD_[T]_C = D_[I]_B (B_[T]_A)(A_[I]_C)");
    if (i == 0):
      temp_matrix = matrix_input(field, augumented, i+1, "original transformation, B_[T]_A")
    elif (i == 1):
      temp_matrix = matrix_input(field, augumented, i+1, "basis A")
    elif (i == 2):
      temp_matrix = matrix_input(field, augumented, i+1, "basis B")
    elif (i == 3):
      temp_matrix = matrix_input(field, augumented, i+1, "basis C")
    elif (i == 4):
      temp_matrix = matrix_input(field, augumented, i+1, "basis D")
  else:
    temp_matrix = matrix_input(field, augumented, i+1)

  lo_matrices.append(temp_matrix)


#perform operation
if (operation == matrix.OperationSym.GaussJordan.value):
  lo_matrices[0].gauss_jordan()
elif (operation == matrix.OperationSym.ScalarMultiply.value):
  constant = input("Enter a constant:\t")
  constant = constant.strip()
  constant_frac = fraction_input(constant, field)
  matrix.m_smultiply(lo_matrices[0], constant_frac)

elif (operation == matrix.OperationSym.Inverse.value):
  lo_matrices[0].gauss_jordan(True)

elif (operation == matrix.OperationSym.Determinant.value):
  result = matrix.det(lo_matrices[0])

elif (operation == matrix.OperationSym.Basis.value):
  matrix.print_original_vect_set(lo_matrices[0])
  print("\n\n")
  result = matrix.get_lin_indep(lo_matrices[0], lo_matrices[0].rows, [])

elif (operation == matrix.OperationSym.Independent.value):
  result = matrix.get_lin_indep_combo(lo_matrices[0], [])

elif (operation == matrix.OperationSym.BasisConvert.value):
  result = matrix.basis_convert(lo_matrices[0], lo_matrices[1], lo_matrices[2])

elif (operation == matrix.OperationSym.ChangeOfBasis.value):
  result = matrix.get_cob_matrix(lo_matrices[0], lo_matrices[1])

elif (operation == matrix.OperationSym.TransBasisConvert.value):
  result = matrix.t_basis_convert(lo_matrices[0], lo_matrices[1], lo_matrices[2])

elif (operation == matrix.OperationSym.GenTransBasisConvert.value):
  result = matrix.gen_t_basis_convert(lo_matrices[0], lo_matrices[1], lo_matrices[2], lo_matrices[3], lo_matrices[4])

else:
  for i in range(len(lo_matrices) - 1):
    if (not i):
      result = None
      m_a = lo_matrices[0]
      m_b = lo_matrices[1]
    else:
      m_a = result
      m_b = lo_matrices[i + 1]

    if (operation == matrix.OperationSym.Add.value):
      result = matrix.m_arith(matrix.m_add, m_a, m_b, "size", True)
    elif (operation == matrix.OperationSym.Subtract.value):
      result = matrix.m_arith(matrix.m_add, m_a, m_b, "size", True, "-")
    elif (operation == matrix.OperationSym.Multiply.value):
      result = matrix.m_arith(matrix.m_multiply, m_a, m_b, "col-row")


# Print the result
if (operation != matrix.OperationSym.GaussJordan.value):
  print("\n------ Answer -------\n\n")

  if (operation == matrix.OperationSym.ScalarMultiply.value):
    lo_matrices[0].print_matrix()
  elif (operation == matrix.OperationSym.Inverse.value):
    lo_matrices[0].print_inverse()
  elif (operation == matrix.OperationSym.Determinant.value):
    result.print_frac()
  elif (operation == matrix.OperationSym.Basis.value or 
        operation == matrix.OperationSym.Independent.value):
    
    result_txt = f"Number of Bases: {len(result)}\n"
    result_no_txt = "The vectors for each basis are:\n"

    if (operation == matrix.OperationSym.Independent.value):
      result_txt = result_txt.replace("Bases", "Sets")
      result_no_txt = result_no_txt.replace("basis", "set")

    matrix.print_original_vect_set(lo_matrices[0])
    print(f"\n\n{result_txt}")

    if (result):
      print(result_no_txt)
      for c in result:
        print(c)
  else:
    result.print_matrix()
