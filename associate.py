from commitment import exp

def associate(commList, assocList, h, p):
	newList = [(commList[position[0]-1]*exp(h,position[1], p))%p for position in assocList]
	return newList

