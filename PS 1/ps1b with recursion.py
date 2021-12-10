###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """

    
    #Method 2 solving recursively
    available_weight = target_weight
    
    if egg_weights == () or available_weight == 0:
        number_of_eggs = 0
    
    elif egg_weights[-1] >available_weight:
        #Explore right branch only
        number_of_eggs = dp_make_weight(egg_weights[:-1], available_weight)
        
    else:
        #Explore left branch
        eggs_to_take = available_weight//egg_weights[-1]
        available_weight -= eggs_to_take*egg_weights[-1]
        memo[egg_weights[-1]] = eggs_to_take
        number_of_eggs = dp_make_weight(egg_weights[:-1], available_weight)
        number_of_eggs += eggs_to_take
    
    #to print the actual dictionary of eggs taken
    sum_of_values = 0
    for values in memo.values():
        sum_of_values += values
    if sum_of_values == number_of_eggs:
        print('Actual dictionary of eggs taken:', memo)
        
    return number_of_eggs    

    
# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()