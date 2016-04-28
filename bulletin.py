from commitment import commitment
import random

class bulletin():
    def __init__(self, numPeople, numCandidates):
        self.numPeople = numPeople
        self.candidateDict = numCandidates
        self.dummyVotes = []
        self.dummyVoteIndices = {cand:[] for cand in range(1,numCandidates+1)}
        dummyVoteCount = [item for candidate in range(1,numCandidates+1) for item in [candidate]*numPeople]
        for i in range(numPeople*numCandidates):
            dummyVoteNum = random.randint(1,10000000)
            randInd = random.randint(0,len(dummyVoteCount)-1)
            dummyCandNum = dummyVoteCount.pop(randInd)
            self.dummyVotes.append(commitment(dummyVoteNum, dummyCandNum))
            self.dummyVoteIndices[dummyCandNum].append(i)

    def getVotes(self):
        return self.dummyVotes

    def getIndices(self):
        return self.dummyVoteIndices

    def writeToFile(self, filename):
        with open(filename, 'w') as f:
            for vote in self.dummyVotes:
                __,maskedVote,__ = vote.reveal()
                f.write(str(maskedVote)+'\n')
