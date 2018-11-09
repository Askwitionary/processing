import warnings
import random
import string
import time


class Vertex:
    """
    Media class
    """

    def __init__(self, name: str):
        """
        Initialize Media object, takes in 2 points as input
        :param name: Media name
        """

        if name == "":
            raise ValueError("Media name cannot be empty string!")

        self.name = str(name)

    def __repr__(self):
        return "Media: {}".format(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.__repr__())


class Edge:
    """
    Relationship class
    """

    def __init__(self, p1: Vertex, p2: Vertex, dist: float = None, weight=0):
        """
        Initialize Relationship object, takes in 2 points as input
        :param p1: point1
        :param p2: point2
        :param dist: distance, default 1
        """

        # Check for input type
        # if type(p1) is not Media:
        #     if type(p2) is not Media:
        #         raise TypeError("Invalid input type for p1: '{}' and p2: {}. "
        #                         "Expecting '{}'".format(type(p1), type(p2), Media))
        #     else:
        #         raise TypeError("Invalid input type for p1: '{}'"
        #                         "Expecting '{}'".format(type(p1), Media))
        # else:
        #     if type(p2) is not Media:
        #         raise TypeError("Invalid input type for p2: {}. "
        #                         "Expecting '{}'".format(type(p2), Media))

        # Set points in order. The representation of point1 < that of point2
        if p1.name < p2.name:
            self.point1, self.point2 = p1, p2
        else:
            self.point1, self.point2 = p2, p1

        # distance of point1 and point2
        self.distance = self._get_distance(dist)
        self.weight = weight

    def __repr__(self):
        return "Relationship: {}--{} \n".format(self.point1.name, self.point2.name)

    def __eq__(self, other):
        points_chk = self.point1 == other.point1 and self.point2 == other.point2
        dist_chk = self.distance == other.distance
        return points_chk and dist_chk

    def __hash__(self):
        return hash(self.__repr__())

    def __contains__(self, item):
        if type(item) is not Vertex:
            return False
        return self.point1 == item or self.point2 == item

    def _get_distance(self, dist):
        """
        check dist parameter to see if input is valid
        :param dist: distance input
        :return: processed distance input
        """

        if dist is None:
            dist = 1
            default = True
        else:
            default = False

        if self.point1 == self.point2:
            if default:
                return 0
            else:
                raise ValueError("Distance 'between' one single point should be 0, {} given.".format(dist))
        else:
            return dist


class Graph:
    """
    Networks class
    """

    def __init__(self, vertices: [Vertex] = [], edges: [Edge] = []):
        """
        Basic data structure
        """

        self.vertices, self.edges = self._check_inputs_property(vertices, edges)

    def __repr__(self):
        return "Vertices: {}; \n Edges: {}".format(str(self.vertices), str(self.edges))

    def __eq__(self, other):
        return set(self.edges) == set(other.edges) and set(self.vertices) == set(other.vertices)

    def __hash__(self):
        return hash(self.__repr__())

    def __contains__(self, item):
        if type(item) is Vertex:
            return item in self.vertices
        elif type(item) is Edge:
            return item in self.edges
        else:
            return False

    def is_connected(self, vertex_1: Vertex, vertex_2: Vertex):
        """
        check if 2 points are connected
        :param vertex_1: 1st vertex object
        :param vertex_2: 2nd vertex object
        :return: boolean
        """

        # check if the given points are in the graph
        if vertex_1 in self.vertices:
            if vertex_2 in self.vertices:
                return Edge(vertex_1, vertex_2) in self.edges
            else:
                warnings.warn("Media 2 is not in the graph! ")
                return False
        else:
            warnings.warn("Media 1 is not in the graph! ")
            return False

    @staticmethod
    def _check_inputs_type(vertices, edges):
        """
        check if inputs are valid
        :param vertices: input vertices list
        :param edges: input edges list
        :return: checked vertices list and edges list
        """

        # checking data type
        if not all(isinstance(item, Vertex) for item in vertices):
            raise TypeError("Invalid type for vertices input!")
        if not all(isinstance(item, Edge) for item in edges):
            raise TypeError("Invalid type for edges input!")
    
    @staticmethod
    def _check_inputs_property(vertices, edges):
        # checking completeness
        vertices_temp = set()
        for item in edges:
            vertices_temp.add(item.point1)
            vertices_temp.add(item.point2)
        if len(vertices_temp) > len(vertices):
            warnings.warn("Vertices given is not complete. Will automatically add vertices those are "
                          "present in edges but not in vertices.")
            vertices = list(vertices_temp)

        # checking duplicates
        vertices_set = set(vertices)
        if len(vertices_set) < len(vertices):
            warnings.warn("Duplicated vertices found! Total: {}".format(len(vertices) - len(vertices_set)))
        edges_set = set(edges)
        if len(edges_set) < len(edges):
            warnings.warn("Duplicated vertices found! Total: {}".format(len(edges) - len(edges_set)))
        return list(vertices_set), list(edges_set)

    def add_vertex(self, vert: Vertex):
        if vert not in self.vertices:
            self.vertices.append(vert)

    def add_edge(self, edge: Edge):
        if edge not in self.edges:
            self.edges.append(edge)
    
    def _get_connections(self):
        connections = {}
        return connections


# ======================================= Methods for testing purposes =================================================


def gen_vertices(count: int):
    """
    generate a list of vertices
    :param count: number of vertices to generate
    :return:
    """

    if type(count) is not int:
        if type(count) is float:
            if int(count) == count:
                count = int(count)
            else:
                raise TypeError("Not supported type '{}' for function gen_vertices. "
                                "Input should be 'int'.".format(type(count)))
        else:
            raise TypeError("Not supported type '{}' for function gen_vertices. "
                            "Input should be 'int'.".format(type(count)))

    letters = string.ascii_uppercase
    if count <= len(letters):
        return [Vertex(letters[i]) for i in range(count)]
    else:
        if count > 26 + 26 ** 2 + 26 ** 3 + 26 ** 4 + 26 ** 5:
            raise ValueError("Too BIG!")
        output = [Vertex(name) for name in letters]
        count = count - len(letters)
        for first in letters:
            for second in letters:
                output.append(Vertex(first + second))
                count -= 1
                if count == 0:
                    return output
        for first in letters:
            for second in letters:
                for third in letters:
                    output.append(Vertex(first + second + third))
                    count -= 1
                    if count == 0:
                        return output
        for first in letters:
            for second in letters:
                for third in letters:
                    for forth in letters:
                        output.append(Vertex(first + second + third + forth))
                        count -= 1
                        if count == 0:
                            return output
        for first in letters:
            for second in letters:
                for third in letters:
                    for forth in letters:
                        for fifth in letters:
                            output.append(Vertex(first + second + third + forth + fifth))
                            count -= 1
                            if count == 0:
                                return output


def gen_vertices_(count: int):
    """
    generate a list of vertices
    :param count: number of vertices to generate
    :return:
    """

    if type(count) is not int:
        if type(count) is float:
            if int(count) == count:
                count = int(count)
            else:
                raise TypeError("Not supported type '{}' for function gen_vertices. "
                                "Input should be 'int'.".format(type(count)))
        else:
            raise TypeError("Not supported type '{}' for function gen_vertices. "
                            "Input should be 'int'.".format(type(count)))

    letters = string.ascii_uppercase
    if count <= len(letters):
        return [letters[i] for i in range(count)]
    else:
        if count > 26 + 26 ** 2 + 26 ** 3 + 26 ** 4 + 26 ** 5:
            raise ValueError("Too BIG!")
        output = [name for name in letters]
        count = count - len(letters)
        for first in letters:
            for second in letters:
                output.append(first + second)
                count -= 1
                if count == 0:
                    return output
        for first in letters:
            for second in letters:
                for third in letters:
                    output.append(first + second + third)
                    count -= 1
                    if count == 0:
                        return output
        for first in letters:
            for second in letters:
                for third in letters:
                    for forth in letters:
                        output.append(first + second + third + forth)
                        count -= 1
                        if count == 0:
                            return output
        for first in letters:
            for second in letters:
                for third in letters:
                    for forth in letters:
                        for fifth in letters:
                            output.append(first + second + third + forth + fifth)
                            count -= 1
                            if count == 0:
                                return output


def gen_edges(vertices, count: int, duplication=False):
    """
    generate a list of edges
    :param vertices: vertices pool to create edges
    :param count: number of edges to generate
    :param duplication: default False, does not allow duplication
    :return: a list of edges with given count within given domain
    """

    if duplication:
        output = []
        for _ in range(count):
            sample = random.sample(vertices, 2)
            output.append(Edge(sample[0], sample[1]))
        return output
    else:
        if count > len(vertices) ** 2 / 2:
            raise ValueError("Not possible to generate {} edges given {} vertices! \n"
                             "Maximum edges possible: {}".format(count, len(vertices), len(vertices) ** 2))
        pool = []
        for i in range(len(vertices)):
            for j in range(i, len(vertices)):
                pool.append(Edge(vertices[i], vertices[j]))
        return random.sample(pool, count)


if __name__ == "__main__":
    v = gen_vertices(500)
    tic = time.clock()
    e = gen_edges(v, 50000)
    toc = time.clock()

    g = Graph(v, e)

    print(toc - tic)
    edge_list = set()
    edge_list.add(Edge(Vertex("A"), Vertex("B")))
    edge_list.add(Edge(Vertex("C"), Vertex("D")))
    edge_list.add(Edge(Vertex("B"), Vertex("A")))
    edge_list = list(edge_list)
