from collections import Counter
from collections import OrderedDict
from typing import List
import math

# is_prime(n) Determines whether 'n' is a prime number
def is_prime(n: int) -> bool:

  #return true if smaller than 3
  if (n <= 3): 
    return True;

  #return false if divisible by 2 or 3
  if (n % 2 == 0): 
    #print("divisor is 2");
    return False;

  elif (n % 3 == 0):
    #print ("divisor is 3")
    return False;


  #start value for divisors to check
  d = 5;

  #smart iteration to check if number is prime
  while (d * d <= n):

    #return false as prime if the number is divisible by the divisor group and its ranges
    if (n % d == 0):
      #print("divisor is %i" %d);
      return False;
      
    elif (n % (d+2) == 0): 
      #print("divisor is %i" %(d+2));
      return False;

    #iterate by 6
    d += 6;
  
  #return true as prime if number went through all tests
  return True;



# prime_factorization(n) Computes the prime factorization of 'n'
def prime_factorization(n: int) -> List[int]:
  prime_factors = []
  current_prime = 2

  while (not(is_prime(n))):
    while (current_prime <= math.floor(math.sqrt(n))):
    
      if (is_prime(current_prime) and not (n % current_prime)):
        n = n / current_prime
        prime_factors.append(current_prime)
        current_prime = 2
      
      else:
        current_prime += 1

  #append the last prime factor
  prime_factors.append(n)
  prime_factors.sort()

  return prime_factors


# lcm(a, b) Finds the lcm of 'a' and 'b'
def lcm(a: int, b: int) -> int:
  prime_factors_a = prime_factorization(a)
  prime_factors_b = prime_factorization(b)

  prime_occur_a = Counter(prime_factors_a)
  prime_occur_b = Counter(prime_factors_b)

  #make prime factorization for 'a' and 'b'the same size and sorted by key
  for p in prime_occur_a:
    if (p not in prime_occur_b.keys()):
      prime_occur_b[p] = 0

  for p in prime_occur_b:
    if (p not in prime_occur_a.keys()):
      prime_occur_a[p] = 0

  prime_occur_a = dict(prime_occur_a)
  prime_occur_a = OrderedDict(sorted(prime_occur_a.items(), key=lambda t: t[0]))
  prime_occur_b = dict(prime_occur_b)
  prime_occur_b = OrderedDict(sorted(prime_occur_b.items(), key=lambda t: t[0]))
  
  result = 1;

  for p in prime_occur_a:
    if (prime_occur_a[p] >=  prime_occur_b[p]):
      result *= (p ** prime_occur_a[p])
    else:
      result *= (p ** prime_occur_b[p])

  return result
