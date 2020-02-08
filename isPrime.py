def countPrimes(n):
    """
    :type n: int
    :rtype: int
    """
    if n <= 1:
        return 0
    # if n == 2:
    #     return 1
    num_primes = 0
    is_prime = False

    for j in range(2, n):
        # print('j = {}'.format(j))
        is_prime = True

        for i in range(2, j):
            # print('i = {}'.format(i))
            # print('j%i = {}'.format(j % i))
            if j % i == 0:
                is_prime = False
            else:
                is_prime = True
        if is_prime:
            # print('num_primes = {}'.format(num_primes))
            num_primes = num_primes + 1
            # print('num_primes = {}'.format(num_primes))

    return num_primes


print(countPrimes(10))
