import time
import random
from data_structure.graph.graph import Vertex, Edge, Graph, gen_vertices, gen_edges, gen_vertices_


# ================================================== Media ==================================================
def vertex_test():
    """
    testing vertex class
    :return: nothing
    """

    print("================ Testing Media class ===================")
    num = [i**3 * 10000 for i in range(1, 11)]

    vertices = []
    for n in num:
        vertex_name = gen_vertices_(n)

        print("Generating {} vertices ...".format(n), end="")
        tic = time.clock()
        for name in vertex_name:
            vertices.append(Vertex(name))
        toc = time.clock()
        print("Done! \n === Time elapsed: {}".format(toc - tic))

    print("\n")

    print("Printing sample vertices ...")
    sample = random.sample(vertices, 15)
    for item in sample:
        print(item)

    print("\n")

    print("Testing for empty string input ... ", end="")
    try:
        _ = Vertex("")
    except ValueError:
        print("Passed")
        pass


if __name__ == "__main__":
    vertex_test()
