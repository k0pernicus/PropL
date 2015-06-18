import sys
from threading import Thread

from test_graph_generation import generate_random_graph
from test_graph_generation import generate_some_examples
from test_graph_generation import resolve_pb
from test_graph_generation import generate_some_tests
from test_graph_generation import is_algorithm_good_between_examples
from test_graph_generation import is_algorithm_good_between_weights
from test_graph_generation import get_first_sources

def run_test(nb_nodes, nb_targets, nb_of_tests, len_examples, i):

    #One target for 3000 nodes
    use_graph = generate_random_graph(nb_nodes, nb_targets)

    examples = generate_some_examples(use_graph, len_examples)

    first_sources = get_first_sources(use_graph)

    weights = resolve_pb(use_graph, examples, first_sources = first_sources)

    tests = generate_some_tests(use_graph, examples, weights, len_examples)

    print("test {0}...".format(i), end='')

    is_algorithm_good_between_examples(examples, tests)

if __name__ == "__main__":

    nb_nodes = int(sys.argv[1])

    nb_targets = int(sys.argv[2])

    nb_of_tests = int(sys.argv[3])

    len_examples = int(sys.argv[4])

    for i in range(0, nb_of_tests):

        Thread(target=run_test, args=(nb_nodes, nb_targets, nb_of_tests, len_examples, i,)).start()
