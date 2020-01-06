import math
import time

upper = int(input("Enter the upper bound of the search: "))

start = time.time()

counter = 0

if upper >= 2:
    counter +=1
    print(counter, 2)

for num in range(3, upper+1, 2):
    num_is_prime = True
    for test in range(3, math.floor(math.sqrt(num))+1, 2):
        if num%test == 0:
            num_is_prime = False
            break
    if num_is_prime:
        counter +=1
        print(counter, num) 
        #print(counter, num, num/math.log(num))

print("There are", counter, "prime numbers smaller than", upper)
end = time.time()
print("Search time taken: ", end - start)