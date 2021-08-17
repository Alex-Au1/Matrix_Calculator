from typing import List, Any

# combination(arr, n, r, result) Stores all combinations from 'arr'
#   with 'r'  elements in 'result'
def combination(arr: List[Any], n: int, r: int) -> List[List[Any]]:
  result = []
  data = [0]*r; 
  result = combinationUtil(arr, data, 0, n - 1, 0, r, result); 
  return result


# combinationUtil(arr, data, start, end, index,r, result) Stores 
#   current combination into 'result'
def combinationUtil(arr: List[Any], data: List[Any], start: int, end: int, index: int, r: int, result: List[Any]) -> List[List[Any]]:         
  if (index == r):  
    new_data = data.copy()
    result.append(new_data)
    return result; 
  
  i = start;  
  while(i <= end and end - i + 1 >= r - index): 
    data[index] = arr[i]; 
    result = combinationUtil(arr, data, i + 1, end, index + 1, r, result);
    i += 1; 

  return result
