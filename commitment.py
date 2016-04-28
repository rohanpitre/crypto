import random

#modular exponentiation
def exp(base, exponent, modulus):
    if exponent == 0:
        return 1
    elif exponent == 1:
        return (base%modulus)
    elif exponent % 2 == 0:
        halfExp = exp(base, exponent/2, modulus)
        return (halfExp*halfExp)%modulus
    elif exponent % 2 == 1:
        halfExp = exp(base, exponent/2, modulus)
        return (halfExp*halfExp*base)%modulus
    else:
        raise ValueError('{}^{} mod {} exponentiation cannot be performed'.format(base, exponent, modulus))

class commitment():
    '''
    voteNum is a randomly generated number that corresponds to the vote
    candNumn is a number corresponding to the candidate. 
    prime is some prime which is used for encryption
    randKey is the random number which is the key to the commitment, revealing randKey 
      "opens" the commitment
    '''
    def __init__(self, voteNum, candNum):
        self.voteNum = voteNum
        self.candNum = candNum
        self.prime = 15485863
        self.randKey = random.randint(2, self.prime-2)
        self.g = 2
        self.h = exp(2, 43, self.prime)

    def getVoteNum(self):
        return self.voteNum

    def getRandKey(self):
        return self.randKey
    '''
    maps the space of random numbers and candidates to a single message
    this message contains all the information about the candidate and the
    random number associated with the vote. 
    '''
    def totalVote(self):
        return ((self.voteNum * self.candNum) % (self.prime))

    '''
    returns the encrypted commitment. This value contains all information about
    the vote without revealing the vote itself
    '''
    def encrypt(self):
        totVote = self.totalVote()
        return (exp(self.g,totVote,self.prime)*exp(self.h,self.randKey,self.prime))%self.prime

    '''
    reveals all information about the commitment
    '''
    def reveal(self):
        return self.voteNum,self.encrypt(), self.randKey

    def recommit(self):
        newRandKey = random.randint(2, self.prime-2)
        totVote = self.totalVote()
        newEncrypt = (exp(self.g,totVote,self.prime)*exp(self.h,newRandKey,self.prime))%self.prime
        powerDiff = (newRandKey - self.randKey)%(self.prime-1)
        self.randKey = newRandKey
        return powerDiff, newEncrypt




