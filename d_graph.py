# Course: CS261 - Data Structures
# Author: Christine Lantigua
# Assignment: 6
# Description: Directed Graph methods created from scratch

import heapq
from collections import deque


class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Method adds a new vertex to the graph. Vertex name does not need to be provided,
        instead vertex will be assigned to a reference index (int).
        """

        # add one to self.v_count
        self.v_count += 1
        self.adj_matrix.append([0] * self.v_count)

        # append value to matrix within the range of count
        for i in range(self.v_count - 1):
            self.adj_matrix[i].append(0)

        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Adds an edge to a directed graph
        """

        # src or dst is equal to one another or >= the graph
        if src >= self.v_count or src < 0:
            return

        if dst >= self.v_count or dst < 0:
            return

        if src == dst:
            return

        # weight is not a positive integer
        if weight <= 0:
            return

        self.adj_matrix[src][dst] = weight

        pass

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Removes an edge from a directed graph
        """

        # does not exist on graph
        if src >= self.v_count or src < 0:
            return

        if dst >= self.v_count or dst < 0:
            return

        # change the weight to 0 at specified matrix position
        self.adj_matrix[src][dst] = 0

        pass

    def get_vertices(self) -> []:
        """
        This method returns a list of vertices of the graph.
        """

        # empty list to add vertices into
        vertices = []

        # loop through range of v_count to append values from 0 - self.v_count
        for num in range(self.v_count):
            vertices.append(num)

        return vertices

    def get_edges(self) -> []:
        """
        This method returns a list of edges in the graph

        Each edge is returned as a tuple of two incident vertex indices and weight

        first el = source vertex (row)
        second el = destination vertex (col)
        third el = weight
        """

        # get the vertices (0-len of v_count)
        vertices = self.get_vertices()

        # create an empty list and start destination at 0
        edges = []
        destination = 0

        # grab the row
        for src in vertices:
            # grab the col
            for weight in self.adj_matrix[src]:

                # where weight != 0, append the respective values
                if weight != 0:
                    edges.append((src, destination, weight))

                # add one to the col
                destination += 1

            # reset col to 0 once we reach a new row
            destination = 0

        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        This method takes a list of vertex indices and returns True if the
        sequence of vertices represents a valid path in the graph (so one can travel from the first vertex
        in the list to the last vertex in the list, at each step traversing over an edge in the graph)
        """

        length_of_path = len(path)

        # empty path is automatically true
        if length_of_path == 0:
            return True

        # path has one value, check if that value exists within vertices before returning True
        if length_of_path == 1 and path[0] in self.get_vertices():
            return True

        # grab the list of edges
        edges = self.get_edges()

        # loop through each index of path
        for index in range(0, length_of_path - 1):

            vertex_to_look_for = path[index]
            found_match = False

            # loop through each edge tuple within edges list
            for edge in edges:
                v, e, w = edge[0], edge[1], edge[2]

                # vertex within tuple matches the vertex we're looking for
                if v == vertex_to_look_for:

                    # edge matches the next index to look for within path
                    if e == path[index + 1]:
                        found_match = True

            if not found_match:
                return False

        return True

    def dfs(self, v_start, v_end=None, check_for_cycle=False) -> []:
        """
        Method preforms a depth-first-search (DFS) in the graph and returns a list of vertices
        visited during the search in the order they were visited

        It takes one required parameter index of the vertex from which starts the search from that point
        """
        # initiate empty set and two empty lists
        visited = set()
        check_vertex = [v_start]
        output_list = []
        vertex_edges = []
        vertex_list = self.get_vertices()

        # element is not within graph
        if v_start not in vertex_list:
            return output_list

        edges = self.get_edges()

        # check_vertex is not empty
        while check_vertex:
            vertex = check_vertex.pop()

            # values exist within key and key is not yet in visited
            if vertex not in visited:

                # grab each edge associated with value
                for edge in edges:
                    if edge[0] == vertex:
                        vertex_edges.append(edge[1])

                    # sort the key's values in reverse sorted order
                        vertex_edges.sort()
                        vertex_edges.reverse()

                # add this list onto the check_these_vertices list
                check_vertex.extend(vertex_edges)
                vertex_edges = []

                if check_for_cycle:
                    for value in check_vertex:
                        if value in visited:
                            return True

            # add key to visited set and append it to the output list
            if vertex not in visited:
                visited.add(vertex)
                output_list.append(vertex)

            # if v_end exists and v_end is in visited, return output_list
            if v_end and v_end in visited:
                return output_list

        if check_for_cycle:
            return False

        return output_list

    def bfs(self, v_start, v_end=None) -> []:
        """
        TODO: Write this implementation
        """
        # initiate empty set and two empty lists
        visited = set()
        check_vertex = deque()
        check_vertex.append(v_start)
        output_list = []
        vertex_edges = []
        vertex_list = self.get_vertices()

        # element is not within graph
        if v_start not in vertex_list:
            return output_list

        edges = self.get_edges()

        # check_vertex is not empty
        while check_vertex:
            vertex = check_vertex.popleft()

            # values exist within key and key is not yet in visited
            if vertex not in visited:

                # grab each edge associated with value
                for edge in edges:
                    if edge[0] == vertex and edge[0] not in visited:
                        vertex_edges.append(edge[1])

                    # sort the key's values in reverse sorted order
                vertex_edges.sort()

                # add this list onto the check_these_vertices list
                check_vertex.extend(vertex_edges)

            # add key to visited set and append it to the output list
            if vertex not in visited:
                visited.add(vertex)
                output_list.append(vertex)

            # if v_end exists and v_end is in visited, return output_list
            if v_end and v_end in visited:
                return output_list

        return output_list

    def make_graph_dict(self):
        """makes the graph into a dictionary with keys and values"""
        graph_dict = dict()

        edges = self.get_edges()

        for edge in edges:
            key, val = edge[0], edge[1]

            graph_dict[key] = val

        return graph_dict

    def has_cycle(self):
        """
        This method returns True if there is at least one cycle in the graph. If the graph is acyclic,
        the method returns False.
        """

        for index in range(0, len(self.get_vertices())):
            has_cycle = self.dfs(self.get_vertices()[index], None, True)

            if has_cycle is True:
                return True

        return False

    def __find_minimum(self, weight, output_list):
        """
        helper function for dijkstra's algorithm

        method returns the index with the lowest weight
        """

        # initialize minimum values
        min_index = 0
        min_val = 2147483646  # infinity

        # loop through each index in self.v_counter until absolute minimum value reached
        for number in range(self.v_count):

            # check if distance of specified number is less than the current minimum value
            # and the current slot is empty
            if weight[number] < min_val and output_list[number] is False:
                # reassign minimum values
                min_val = weight[number]
                min_index = number

        return min_index

    def dijkstra(self, src: int) -> []:
        """
        This method implements the Dijkstra algorithm to compute the length of the shortest path
        from a given vertex to all other vertices in the graph. It returns a list with one value per
        each vertex in the graph, where value at index 0 is the length of the shortest path from
        vertex SRC to vertex 0, value at index 1 is the length of the shortest path from vertex SRC
        to vertex 1 etc. If a certain vertex is not reachable from SRC, returned value should be
        INFINITY (in Python, use float(???inf???)).

        **utilized help from geeks for geeks to put this algorithm together
        https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/

        ** tried to add as many notes as possible to make sure i understood what was going on with
        the help from geeksforgeeks
        """

        # set each value to numbers outside of src value to be reassigned to infinity later
        dist = [2147483646] * self.v_count

        # set the first value equal to 0 and create shortest path list with iterations of false
        dist[src] = 0
        shortest_path = [False] * self.v_count

        for each_num in range(self.v_count):

            # determine the vertex within the list with the least amount of weight (shortest path)
            min_vertex = self.__find_minimum(dist, shortest_path)

            # place the value within the shortest path tree by replacing the false value with true
            shortest_path[min_vertex] = True

            for index in range(self.v_count):
                vertex = self.adj_matrix[min_vertex][index]

                # past the first index
                if vertex > 0:

                    # no value currently assigned in shortest path, distance of index is greater than curr min vertex
                    if shortest_path[index] is False and dist[index] > (dist[min_vertex] + vertex):
                        # update the distance value
                        dist[index] = dist[min_vertex] + vertex

        # reassign value of 2147483646 to float of inf as it could not be assigned initially
        # before returning dist
        for index in range(0, len(dist)):
            if dist[index] == 2147483646:
                dist[index] = float('inf')

        return dist


if __name__ == '__main__':

    # print("\nPDF - method add_vertex() / add_edge example 1")
    # print("----------------------------------------------")
    # g = DirectedGraph()
    # print(g)
    # for _ in range(5):
    #     g.add_vertex()
    # print(g)
    #
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # for src, dst, weight in edges:
    #     g.add_edge(src, dst, weight)
    # print(g)

    # print("\nPDF - method get_edges() example 1")
    # print("----------------------------------")
    # g = DirectedGraph()
    # print(g.get_edges(), g.get_vertices(), sep='\n')
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # print(g.get_edges(), g.get_vertices(), sep='\n')

    # print("\nPDF - method is_valid_path() example 1")
    # print("--------------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    # for path in test_cases:
    #     print(path, g.is_valid_path(path))

    #
    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')
    #
    #
    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)
    #
    #
    # print("\nPDF - dijkstra() example 1")
    # print("--------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # for i in range(5):
    #     print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    # g.remove_edge(4, 3)
    # print('\n', g)
    # for i in range(5):
    #     print(f'DIJKSTRA {i} {g.dijkstra(i)}')
