from bisect import bisect_left
from copy import deepcopy

#for a list and a number, returns the index of the value in the list that's closest in log(n) time
def takeClosest(myList, myNumber, round = 'near'):
    """
    Assumes myList is sorted. Returns closest value to myNumber.
    """
    reverse = False
    if ordertest(myList):
        myList = deepcopy(myList)
        myList.reverse()
        reverse = True
    pos = bisect_left(myList, myNumber)

    if pos == 0:
        return 0 if not reverse else len(myList)-1
    elif pos == len(myList):
        return len(myList)-1 if not reverse else 0

    before = myList[pos-1]
    after = myList[pos]

    if round == 'up' or (round == 'near' and after - myNumber < myNumber - before) or after == myNumber:
        return pos if not reverse else len(myList) - 1 - pos
    else:
        return pos-1 if not reverse else len(myList) - pos

def ordertest(A):
    for i in range(len(A) - 1):
        if isinstance(A[i], float) and isinstance(A[i+1], float) and A[i]<A[i+1]:
            return False

    return True
