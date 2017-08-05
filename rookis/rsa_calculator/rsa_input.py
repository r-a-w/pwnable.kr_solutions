import random

MIN_RANGE = 1
MAX_RANGE = 1000

def is_prime(p):
    if(p==2): return True
    if(not(p&1)): return False
    return pow(2,p-1,p)==1


def find_prime(min_range, max_range):
    p = random.randrange(MIN_RANGE, MAX_RANGE, 2)
    while(not(is_prime(p))):
        p = random.randrange(MIN_RANGE, MAX_RANGE, 2)
    return p

def muliplicative_inverse(phi, e):
    d = 1
    while(((d*e)%phi) != 1):
        d+=1
    return d

if __name__ == '__main__':
    p = find_prime(100, 10000)
    q = find_prime(100, 10000)

    phi = (p-1)*(q-1)

    e = find_prime(0, phi)
    while((phi%e) == 0):
        e = find_prime(0, phi)

    d = muliplicative_inverse(phi, e)

    print 'p = ' + str(p)
    print 'q = ' + str(q)
    print 'e = ' + str(e)
    print 'd = ' + str(d)
    print 'phi = ' + str(phi)
    print 'N = ' + str(p*q)
