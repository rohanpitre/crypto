Instructions on how to run the program

1. Clear all files in the receipts and proofs folders
2. Run python election.py and follow the instructions in the program
The candidate list is provided in candidates. This can be modified if necessary.
Typing in i corresponds to voting for the candidate on the ith line.
For example entering 3 means you voted for the 3rd candidate in the list or John Kasich

Format of the output
dummyvotes.txt is a shuffled list of all dummy votes.

results.txt is a tally of all unopened dummy votes. Each
vote is represented as a,b,c where a is the output from the RNG,
b is the output from the random coin and c is the encrypted commitment.
With knowledge of p, g, and h anyone can verify that these commitments were
calculated properly and were included in the original dummy votes.

In receipts, there is one file per receipt. The name of the file is id.json where
id is the id you input in the program. For this simplified model, it works best if you
have a different id for everybody. The receipt contains one legitimiate vote and
l-1 dummy votes. The user can verify that the random number for the candidate they voted
for corresponds to the output of the RNG.

Zero-Knowledge Proof
A zero knowledge proof is created for each receipt. The left list is a shuffled version
of the l-1 dummy commitments and the one actually chosen commitment. Since this is published,
everybody can verify that all used commitments appeared on exactly one receipt. The middle list
is a masked and shiffled list corresponding to the same values and the same with the right list.
The contents in the right list are revealed in much the same way as the results except there is the
added condition that the random numbers associated with the commitments are the same as those on
the matching receipt. Additionally, the association between either the left and middle or middle
and right is published. The format of the association is a list. The ith component of the list is a tuple.
The first component of the tuple is the corresponding position in the previous list. For example,
if the 3rd element of the left list was now the 4th element of the middle list, the 4th element
of the association list would be a tuple with a first component of 3. The second element of the tuple
is the difference between the commitments. For example, if the random coin outputted 2 for the left list and 
6 for the right list for a given vote, the second component would be 4 for the ith entry in the association 
list where i is the position of the vote in the middle list. The program associate.py takes in a list of 
commitments and an association list and calculates the next step. The parameter h and p are the same used 
in the commitments.

With the association list provided, anybody can check whether one of the lists was calculated correctly.
Or, there is a 50% chance that for any receipt an error is detected. This procedure can be repeated an 
arbitrary number of times for an arbitrary degree of soundness. 