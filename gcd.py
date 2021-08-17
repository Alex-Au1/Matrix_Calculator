#eucli_algo(a, b) Computes the gcd of 'a' and 'b'
def eucli_algo(a: int, b: int) -> int:
  (q, r) = divmod(a, b)

  if (not r):
    return b
  else:
    return eucli_algo(b, r)
