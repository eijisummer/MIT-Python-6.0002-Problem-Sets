###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name: Eijiro Asada
# Collaborators: None
# Time: Probably a long time

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here
    
    #file_content = open(filename)
    # print(file_content.read())
    
    dictionary = {}
    with open(filename) as file_content:
        for line in file_content:
            (key, value) = line.split(',')
            dictionary[key] = int(value)   
    return dictionary    
    
cows = load_cows('ps1_cow_data.txt')  


# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    import copy
    
    sorted_cows = sorted(cows.items(), key=lambda x:x[1], reverse = True)
     
    all_flights = []
    each_flight = []
    each_flight2 = []
    total_weight = 0
    trip_limit = limit
    remaining_cows = copy.deepcopy(sorted_cows)
    while len(remaining_cows) > 0:
        for i in range(len(remaining_cows)):         
            if (total_weight + remaining_cows[i][1]) <= trip_limit:
                each_flight.append(remaining_cows[i][0])
                each_flight2.append(remaining_cows[i]) #each_flight2 is like each_flight except that it contains tuplets
                total_weight += remaining_cows[i][1]
        all_flights.append(each_flight)
        
        for i in each_flight2:
            remaining_cows.remove(i)
        each_flight = []
        each_flight2 = []
        total_weight = 0   
    return f'greedy: {len(all_flights)} trips with the list {all_flights}'  
print(greedy_cow_transport(cows))
print(' ')  
    
# Problem 3
def partitions(set_):
    if not set_:
        yield []
        return
    for i in range(2**len(set_)//2):
        parts = [set(), set()]
        for item in set_:
            parts[i&1].add(item)
            i >>= 1
        for b in partitions(parts[1]):
            yield [parts[0]]+b

def get_partitions(set_):
    for partition in partitions(set_):
        yield [list(elt) for elt in partition]


def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """

    cows_list = cows.items()
    for partition in get_partitions(cows_list):
        #print(partition)
        all_flights = []
        for i in partition:
            each_flight = []
            weight_subtotal = 0
            for cow in i:
                weight_subtotal += cow[1]
                each_flight.append(cow[0])
            if weight_subtotal > limit:
                break
            elif weight_subtotal <= limit:
                all_flights.append(each_flight)
                # print(all_flights)
            if len(all_flights) == len(partition):
                return f'brute force:  {len(all_flights)} trips with the list {all_flights}'
  

print(brute_force_cow_transport(cows))

        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    
    # TODO: Your code here
    
    
    cows = load_cows('ps1_cow_data.txt')
    start = time.time()
    ##code to be timed
    greedy_cow_transport(cows)
    end = time.time()
    print('')
    print(f'greedy algorithm time: {end - start}')
    
    start = time.time()
    ##code to be time
    brute_force_cow_transport(cows)
    end = time.time()
    print('')
    print(f'brute force algorithm time: {end - start}')
    
    

compare_cow_transport_algorithms()


"""Q1:  What were your results for compare_cow_transport_algorithms?  
Which algorithm runs faster?  Why?  A1:  the greedy algorithm runs faster with time of 0.000079 seconds,
compared to brute force algorithm of 0.65 seconds.  The reason the greedy algorithm runs faster is that
the efficiency of greedy algorithm is O(n^2), whereas the efficiency of brute force algort¡ithms is O(n^n).

Q2: Does the greedy algorithm return the optimal solution?  WHy/Why not?  No because the greedy algorithm
returns the local optimal solution.






Q3:  Does the brute force algorithm return the optimal solution?  Yes becasue it searches all possible 
options."""



