# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

from collections import OrderedDict

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    if len(sequence) == 1:
    	return [sequence]
    else:
    	permutations = []
    	first = sequence[0]
    	sequence = sequence[1:]
    	old_perm = get_permutations(sequence)

    	for seq in old_perm:
    		for pos in range(len(seq)+1):
    			permutations.append(seq[0:pos] + first + seq[pos:len(seq)])

    return list(OrderedDict.fromkeys(permutations))








if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    pass #delete this line and replace with your code here


