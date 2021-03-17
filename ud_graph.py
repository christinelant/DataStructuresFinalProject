# Course: CS261 Data Structures
# Author: Christine Lantigua
# Assignment: 6
# Description: Implementation of undirected graph methods such as: add_vertex,
#              add_edge, remove_edge, remove_vertex, get_vertices, get_edges
#              etc.
#

import heapq
from collections import deque


class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """
        if v in self.adj_list:
            return
        else:
            self.adj_list[v] = []

    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """

        # u and v point to same vertex or u and v already have an edge between one another
        if u == v:
            return

        # key u is not within the graph
        if u not in self.adj_list:
            self.add_vertex(u)

        # key v is not within the graph
        if v not in self.adj_list:
            self.add_vertex(v)

        # append edges into the graph
        if u not in self.adj_list[v]:
            self.adj_list[v].append(u)
        if v not in self.adj_list[u]:
            self.adj_list[u].append(v)

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """

        # keys do not exist in graph
        if v not in self.adj_list:
            return

        if u not in self.adj_list:
            return

        # u or v not present as an edge in either list
        if u not in self.adj_list[v] or v not in self.adj_list[u]:
            return

        # remove edges from respective vertices
        self.adj_list[v].remove(u)
        self.adj_list[u].remove(v)

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        if v not in self.adj_list:
            return

        # grab the edges connected to v
        edges_connected_to_v = self.adj_list[v]

        # remove v from each vertex
        for vertex in edges_connected_to_v:
            self.adj_list[vertex].remove(v)

        # remove v from the graph altogether
        self.adj_list.pop(v, None)

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """

        # initiate an empty list
        vertex_list = []

        for vertex in self.adj_list:
            vertex_list.append(vertex)

        return vertex_list

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """

        edge_list = []
        checked_vertices = set()

        for vertex in self.adj_list:
            for index in self.adj_list[vertex]:

                if index not in checked_vertices:
                    checked_vertices.add(vertex)

                    edge_list.append((vertex, index))

                continue

        return edge_list

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """

        # empty list is automatically true
        if len(path) == 0:
            return True

        # grab the first value
        prev_val = path[0]

        # check if the first value is within the self.adj_list before moving on
        if prev_val not in self.adj_list:
            return False

        # length of path is one
        if len(path) == 1 and prev_val in self.adj_list:
            return True

        # start the counter and grab the next value
        counter = 1
        next_val = path[counter]

        for key in path:

            # store the length of the key's edges
            length_of_edges = len(self.adj_list[key]) - 1

            # grab the specified key's values
            for value in self.adj_list[key]:

                # match is found
                if value == next_val:
                    break

                # we have reached the end of the array
                if length_of_edges == 0:
                    return False

                # decrement length of edges
                length_of_edges -= 1

            # have not yet reached the last key -- increment counter and grab the next value
            # as to check for value as an edge of our next key within path
            if counter + 1 < len(path):
                counter += 1
                next_val = path[counter]
            else:
                return True

    def dfs(self, v_start, v_end=None, check_for_cycle=False) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """

        # initiate empty set and two empty lists
        visited = set()
        check_these_vertices = [v_start]
        output_list = []

        # element is not within graph
        if v_start not in self.adj_list:
            return output_list

        # check_these_vertices is not empty
        while check_these_vertices:
            key = check_these_vertices.pop()

            # values exist within key and key is not yet in visited
            if len(self.adj_list[key]) > 0 and key not in visited:
                key_edges = self.adj_list[key]

                # sort the key's values in lexiographical order and reverse the order
                key_edges.sort()
                key_edges.reverse()

                # add this list onto the check_these_vertices list
                check_these_vertices.extend(key_edges)

                if check_for_cycle:
                    if any(check_these_vertices.count(x) > 1 for x in check_these_vertices):
                        return True

            # add key to visited set and append it to the output list
            if key not in visited:
                visited.add(key)
                output_list.append(key)

            # if v_end exists and v_end is in visited, return output_list
            if v_end and v_end in visited:
                return output_list

        if check_for_cycle:
            return False

        return output_list

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        # initiate empty set and two empty lists
        visited = set()
        check_these_vertices = deque()
        check_these_vertices.append(v_start)
        output_list = []

        # element is not within graph
        if v_start not in self.adj_list:
            return output_list

        # check_these_vertices is not empty
        while check_these_vertices:

            # do not need to reverse this search because we are popping starting from the left
            key = check_these_vertices.popleft()

            # values exist within key and key is not yet in visited
            if len(self.adj_list[key]) > 0 and key not in visited:
                key_edges = self.adj_list[key]

                # sort the key's values in lexiographical order
                key_edges.sort()

                for item in key_edges:
                    # add this list onto the check_these_vertices list
                    check_these_vertices.append(item)

            # add key to visited set and append it to the output list
            if key not in visited:
                visited.add(key)
                output_list.append(key)

            # if v_end exists and v_end is in visited, return output_list
            if v_end and v_end in visited:
                return output_list

        return output_list

    def count_connected_components(self):
        """
        Return number of connected componets in the graph
        """
        vertices = self.get_vertices()
        connected_components = set()

        for vertex in vertices:
            dfs = self.dfs(vertex)
            dfs.sort()

            key = ''.join(dfs)

            if key not in connected_components:
                connected_components.add(key)

        return len(connected_components)

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """

        vertices = self.get_vertices()

        if len(vertices) < 3:
            return False

        for index in range(0, len(vertices)):
            has_cycle = self.dfs(vertices[idx], None, True)

            if has_cycle:
                return True

        return False

if __name__ == '__main__':
    # print("\nPDF - method add_vertex() / add_edge example 1")
    # print("----------------------------------------------")
    # g = UndirectedGraph()
    # print(g)
    #
    # for v in 'ABCDE':
    #     g.add_vertex(v)
    # print(g)
    #
    # g.add_vertex('A')
    # print(g)
    #
    # for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
    #     g.add_edge(u, v)
    # print(g)

    # print("\nPDF - method remove_edge() / remove_vertex example 1")
    # print("----------------------------------------------------")
    # g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    # g.remove_vertex('DOES NOT EXIST')
    # g.remove_edge('A', 'B')
    # g.remove_edge('X', 'B')
    # print(g)
    # g.remove_vertex('D')
    # print(g)

    # print("\nPDF - method get_vertices() / get_edges() example 1")
    # print("---------------------------------------------------")
    # g = UndirectedGraph()
    # print(g.get_edges(), g.get_vertices(), sep='\n')
    # g = UndirectedGraph(['DE', 'DB', 'ED', 'EI', 'JG', 'GJ', 'AK', 'AC', 'KA', 'KC', 'IE', 'BD', 'CK', 'CA'])
    # #
    # # GRAPH: {
    # #     D: ['E', 'B']
    # #     E: ['D', 'I']
    # #     J: ['G']
    # #     G: ['J']
    # #     A: ['K', 'C']
    # #     K: ['A', 'C']
    # #     I: ['E']
    # #     B: ['D']
    # #     C: ['K', 'A']}
    # print(g.get_edges(), g.get_vertices(), sep='\n')

    # print("\nPDF - method is_valid_path() example 1")
    # print("--------------------------------------")
    # g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    # test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    # for path in test_cases:
    #     print(list(path), g.is_valid_path(list(path)))

    # print("\nPDF - method dfs() and bfs() example 1")
    # print("--------------------------------------")
    # edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    # g = UndirectedGraph(edges)
    # test_cases = 'ABCDEGH'
    # for case in test_cases:
    #     print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    # print('-----')
    # for i in range(1, len(test_cases)):
    #     v1, v2 = test_cases[i], test_cases[-1 - i]
    #     print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')

    # print("\nPDF - method count_connected_components() example 1")
    # print("---------------------------------------------------")
    # edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    # g = UndirectedGraph(edges)
    # test_cases = (
    #     'add QH', 'remove FG', 'remove GQ', 'remove HQ',
    #     'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
    #     'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
    #     'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    # for case in test_cases:
    #     command, edge = case.split()
    #     u, v = edge
    #     g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
    #     print(g.count_connected_components(), end=' ')
    # print()

    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
