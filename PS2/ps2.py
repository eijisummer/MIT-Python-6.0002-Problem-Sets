# 6.0002 Problem Set 5
# Graph optimization
# Name: Eijiro Asada
# Collaborators: No one
# Time: a lot of time

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer:  The graph's nodes represent the buildings in the MIT campus.
#          The graph's edges represent the route from the starting building to destination building.
#          The distances are represented in WeightedEdge, which contains the distance in meters between
#          the two buildings, and the distance in meters between the two buildings that must be spent outdoors, 
#


# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """
    map_graph = Digraph()
    
    with open(map_filename) as file_content:
        for line in file_content:
            From, To, TotalDistance, DistanceOutdoors = line.split(' ')
            source = Node(From)
            dest = Node(To)
            weighted_edge = WeightedEdge(source, dest, int(TotalDistance), int(DistanceOutdoors))
            
            if not map_graph.has_node(source):
                map_graph.add_node(source)
            
            if not map_graph.has_node(dest):
                map_graph.add_node(dest)
            
            map_graph.add_edge(weighted_edge)
    
    print("Loading map from file...")
    return map_graph


# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out

#print(load_map('test_load_map.txt'))


# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function:  minimize the total distance
#             Constraint:  distance spent outdoors cannot exceed maximum distance outdoors
#
#
import copy
# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist, best_path):

    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """

#def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist, best_path):    
#  start = a, end = c, path = [[], 0,0], max_dist_outdoors = 10, best_dist = 0, best_path = None
    
    if path[2] > max_dist_outdoors:
        return None
    else:    
        path[0] = path[0] + [start]
        unmutated_path = copy.deepcopy(path)
    if not (digraph.has_node(start) and digraph.has_node(end)):
        raise ValueError ('Node not in map_graph')
    elif start == end:
        return (path[0], path[1])
    else:
        for edge in digraph.get_edges_for_node(start):
            node = edge.get_destination()
            if node not in unmutated_path[0]:  #avoid cycle
                path[0] = unmutated_path[0]
                path[1] = unmutated_path[1] + edge.get_total_distance()
                path[2] = unmutated_path[2] + edge.get_outdoor_distance()
                
                if best_path == None or path[1] < best_dist:
                    new_path = get_best_path(digraph, node, end, path, max_dist_outdoors, best_dist, best_path )
                    if new_path != None:
                        best_path = new_path
                        best_dist = best_path[1]
    
    return best_path
    
    #if start and end are not valid nodes:
    #     raise an error
    # elif start and end are the same node:
    #     update the global variables appropriately
    # else:
    #     for all the child nodes of start:
    #         construct a path including that nodes
    #         recursively solve the  rest of the path, from the child node to the end node
    
    # return the shortest path
            
# map_graph = load_map('test_load_map.txt')  
# print(map_graph)        
# a = Node('a')
# b = Node('b')
# c = Node('c')

# print(get_best_path (map_graph, a, c, [[], 0, 0], 7, 0, None))     


# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    
    (shortest_path, shortest_dist) = get_best_path(digraph, start, end, [[],0,0],max_dist_outdoors, 0, None)
    if shortest_dist > max_total_dist:
        raise ValueError('shortest distance exceeds maximum distance')
    elif shortest_path == None:
        raise ValueError('path is not possible')
    else:
        return shortest_path
    
    
    # if result[1] <= max_total_dist and result[0] != None:
    #     return result[0]
    # else:
    #     raise ValueError('path is not possible!')
        

# print(directed_dfs(map_graph, a, c, 10, 8))

# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                    expectedPath,
                    total_dist=LARGE_DIST,
                    outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    unittest.main()
