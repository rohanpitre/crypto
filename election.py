from bulletin import bulletin
from commitment import commitment
import random
import json

if __name__ == '__main__':
    #prevoting
    numVoters = raw_input('Enter the number of voters: ')
    numVoters = int(numVoters)
    candDict = {}
    i = 0
    with open('candidates', 'r') as f:
        for line in f:
            i += 1
            candDict[i] = line.strip()
    preBulletin = bulletin(numVoters, len(candDict))
    preBulletin.writeToFile('dummyvotes.txt')
    dummyIndices = preBulletin.getIndices()
    dummyVotes = preBulletin.getVotes()

    #voting
    for voter in range(numVoters):
        print 
        idnum = raw_input('Enter your receipt id number: ')
        receipt = {}
        proof = {}
        choice = raw_input('Enter the number corresponding with your candidate: ')
        choice = int(choice)
        freshvote = random.randint(1,1000000)
        print ('Your random number is {}'.format(freshvote))
        print
        print 'Your receipt:'
        print 'id:{}'.format(idnum)
        for j in candDict:
            if j == choice:
                print candDict[j] + ',' + str(freshvote)
                receipt[candDict[j]] = freshvote
                actualVote = commitment(freshvote, j)
                proof[j] = actualVote
            else:
                if len(dummyIndices[j]) == 1:
                    randVote = dummyVotes[dummyIndices[j].pop()]
                else:
                    randInd = random.randint(0, len(dummyIndices[j])-1)
                    randInd = dummyIndices[j].pop(randInd)
                    randVote = dummyVotes[randInd]
                proof[j] = randVote
                receipt[candDict[j]] = randVote.getVoteNum()
                print candDict[j] + ',' + str(randVote.getVoteNum())
        filename = 'receipts/' + str(idnum) + '.json'
        with open(filename, 'w') as f:
            f.write(json.dumps(receipt))
        #50% knowledge proof
        filename = 'proofs/' + str(idnum) + '.txt'
        with open(filename, 'w') as f:
            f.write('Left List\n')
            shuffleOrder = range(len(candDict))
            orderL = []
            while shuffleOrder:
                randInd = random.randint(0, len(shuffleOrder)-1)
                nextElement = shuffleOrder.pop(randInd)
                orderL.append(nextElement)
                f.write(str(proof[nextElement+1].encrypt())+'\n')
            f.write('\nMiddle List\n')
            orderM = []
            shuffleOrder = range(len(candDict))
            associationLM = []
            while shuffleOrder:
                randInd = random.randint(0, len(shuffleOrder)-1)
                nextElement = shuffleOrder.pop(randInd)
                orderM.append(orderL[nextElement])
                diff, newCommit = proof[orderL[nextElement]+1].recommit()
                associationLM.append(( nextElement+1,diff))
                f.write(str(newCommit)+'\n')
            f.write('\nRight List\n')
            f.write('Random Number, Random Key, Committed Value\n')
            associationMR = []
            orderR = []
            shuffleOrder = range(len(candDict))
            while shuffleOrder:
                randInd = random.randint(0, len(shuffleOrder)-1)
                nextElement = shuffleOrder.pop(randInd)
                orderR.append(orderM[nextElement])
                diff, newCommit = proof[orderM[nextElement]+1].recommit()
                associationMR.append((nextElement+1, diff))
                nextVote = proof[nextElement+1]
                f.write('{},{},{}'.format(nextVote.getVoteNum(),nextVote.getRandKey(),newCommit)+'\n')
            f.write('\n')
            if random.random() > 0.5:
                f.write('Association between left and middle\n')
                f.write(str(associationLM)+'\n')
            else:
                f.write('Association between middle and right\n')
                f.write(str(associationMR)+'\n')

    #postvoting
    filename = 'results.txt'
    with open(filename, 'w') as f:
        for candidate in candDict:
            f.write(candDict[candidate]+'\n')
            f.write('{} VOTES'.format(len(dummyIndices[candidate]))+'\n')
            for index in dummyIndices[candidate]:
                unopenedVote = dummyVotes[index]
                voteNumber, encryptedVote, randomCoin = unopenedVote.reveal()
                f.write('{},{},{}\n'.format(voteNumber, randomCoin, encryptedVote))
            f.write('\n')
    print
    print 'Results written'







    
