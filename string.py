from typing import Dict, List

# word_replace(str, word_dict) Replaces every instance of the
#   keys from 'word_dict' that are found in 'str' with its 
#   corresponding value in 'word_dict'
def word_replace(str: str, word_dict: Dict[str, str]) -> str:
  for w in word_dict:
    replace_word = word_dict[w]
    str = str.replace(w, replace_word)

  return str


# format_lst(lst) Formats all the elements in 'lst' into a 
#   single string
def format_lst(lst: List[str]) -> str:
  lst_len = len(lst)
  result_str = ""

  for i in range(lst_len):
    if (not i):
      result_str += lst[i]
    else:
      result_str += f", {lst[i]}"

  return result_str
