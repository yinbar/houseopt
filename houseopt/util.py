import random

rand = random.SystemRandom()

def shuffled(x):
    l = list(x)
    rand.shuffle(l)
    return l

def throw(x):
    raise x
