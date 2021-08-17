import sys
import enum
import string as StringTools
from typing import Any, List, Optional

ERRORS = {1: "The input ({input}) is not {type_article} {type}",
          10: "The input ({input}) is not in between {left} and {right}",
          2: "Denominator of {fraction_type} Fraction Cannot be 0",
          3: "The Number of Coefficients Does not Match the Entered Number of Columns"}


# DataTypes: type for a parameter
class DataTypes(enum.Enum):
  Integer = "Integer"
  Natural = "Natural"
  Float = "Float"


# validation_error(code) Displays an error
#   for the entered parameter
# effects: ends the program once the error has been displayed
def validation_error(code: int, **kwargs):
  # creates the dictionary to replace all temporary values in the error message
  error_message = ERRORS[code]
  kw_keys = list(kwargs.keys())
  for k in kw_keys:
    new_key = "{" + k + "}"
    kwargs[new_key] = kwargs.pop(k)

  error_message = StringTools.word_replace(error_message, kwargs)

  # prints the error message
  print(f"\nERROR:")
  print(error_message)
  sys.exit()


# validate_int(param) Checks whether 'param' is an
#   integer
# effects: ends the program if 'param' is not an integer
def validate_int(param: Any) -> int:
  try:
    param = int(param)
  except:
    validation_error(1, input = str(param), type_article = "an", type = "integer")
  else:
    return param


# validate_nat(param) Checks whether 'param' is a
#   natural number
# effects: ends the program if 'param' is not a natural number
# note: a natural number is an integer bigger or equal to 1
def validate_nat(param: Any) -> int:
  param = validate_int(param)

  if (param <= 0):
    validation_error(1, input = str(param), type_article = "a", type = "natural")
  else:
    return param


# validate_nat(param) Checks whether 'param' is a
#   floating decimal point
# effects: ends the program if 'param' is not a float
def validate_float(param: Any) -> float:
  try:
    param = float(param)
  except:
    validation_error(1, input = str(param), type_article = "a", type = "floating decimal")
  else:
    return param


# validate_inbetween(param, left, right, inclusive, type)
def validate_inbetween(param: Any, left: Any, right: Any, inclusive: bool = True, type: DataTypes = DataTypes.Integer) -> bool:
  # validates the needed parameter are their proper type
  values_to_compare = {"param": param, "left": left, "right": right}
  for v in values_to_compare:
    if (type == DataTypes.Integer):
      values_to_compare[v] = validate_int(values_to_compare[v])
    elif (type == DataTypes.Natural):
      values_to_compare[v] = validate_nat(values_to_compare[v])

  param = values_to_compare["param"]
  left = values_to_compare["left"]
  right = values_to_compare["right"]

  # checks if 'param' is between 'left' and 'right'
  if (inclusive):
    in_between = (param >= left and param <=  right)
  else:
    in_between = (param > left and param <  right)

  if (not in_between):
    validation_error(2, input = str(param), left = str(left), right = str(right))
  else:
    return in_between


# validate_field(param, specific_vals) Checks whether 'param' is a 
#   valid field
# required: all elements in 'specific_vals' are in lowercase
# note: a field is a string with either the letters, "r" or "c" 
#        (Case does not matter)
# effects: may end the program if 'param' is not a field
def validate_str(param: Any, specific_vals = Optional[List[str]]) -> str:
  type_article = "a"
  type = "string"
  try:
    param = str(param)
  except:
    validation_error(1, input = str(param), type_article = type_article, type = type)
  else:
    param = param.lower()
    if (specific_vals is None or (specific_vals is not None and param in specific_vals)):
      return param
    else:
      type += f" that belongs to the following list of values:\n({StringTools.format_lst(specific_vals)})"
      validation_error(1, input = param, type_article = type_article, type = type)


# validate_lst(lst, type) Checks wheter each element in 'lst' matches
#   with the type specified in 'type'
# required: type is one of the elements specified in the enum 'DataTypes'
#           all elements in 'lst' are of the same type
def validate_lst(lst: List[Any], type: DataTypes = DataTypes.Integer) -> List[Any]:
  lst_len = len(lst)
  for i in range(lst_len):
    if (type == DataTypes.Integer):
      lst[i] = validate_int(lst[i])
    elif (type == DataTypes.Natural):
      lst[i] = validate_nat(lst[i])
    elif (type == DataTypes.Float):
      lst[i] = validate_float(lst[i])

  return lst
