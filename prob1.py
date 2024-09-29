# Generate list of 1000 odd numbers
import sys
n=int(sys.argv[1])
odd_numbers = [i for i in range(1, 2*n) if i % 2 != 0]
print(f"Number of odd numbers: {len(odd_numbers)}")

# Generate prime numbers less than or equal to max(odd_numbers)
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

max_odd = max(odd_numbers)
prime_numbers = [num for num in range(2, max_odd + 1) if is_prime(num)]
print(f"Number of prime numbers: {len(prime_numbers)}")

# Calculate probability of A given B
def prob_A_given_B(A, B):
    intersection = set(A) & set(B)
    print(len(intersection))
    return len(intersection) / len(B)

probability = prob_A_given_B(prime_numbers,odd_numbers)
print(f"Probability of A given B: {probability:.4f}")