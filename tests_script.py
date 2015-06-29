import sys
import time

from libs.use_graph_lib import UseGraph

from libs.learning_lib import dichotomicOnlineOptimization
from libs.learning_lib import minAndMaxOnlineOptimization
from libs.learning_lib import updateAllEdgesOnlineOptimization
from libs.learning_lib import constraintsBatchOptimization

from libs.testing_lib import doSomeTests

from libs.basic_stat import getSomeStats

from threading import Thread

def run_algorithm(ug, visualization = False):
    """
    Method to run the usegraph
    """

    ug.run()

    if ug.id == "dicho_online_opt":
        dichotomicOnlineOptimization(ug)

    if ug.id == "min_max_online_opt":
        minAndMaxOnlineOptimization(ug)

    if ug.id == "update_all_edges_online_opt":
        updateAllEdgesOnlineOptimization(ug)

    # if ug.id == "constraints_batch_opt":
    #     constraintsBatchOptimization(ug)

    if visualization:
        ug.visualize()
    getSomeStats(ug)
    doSomeTests(ug)

if __name__ == "__main__":

    debugging = False

    visualization = False

    repo_to_test = sys.argv[1]

    if "--debug" in sys.argv:
        debugging = True

    if "--visu" in sys.argv:
        visualization = True

    all_ug = []

    ug_dicho_online_opt = UseGraph("dicho_online_opt", repo_to_test, debug_mode=debugging)
    ug_min_max_online_opt = UseGraph("min_max_online_opt", repo_to_test, debug_mode=debugging)
    ug_update_all_edges_online_opt = UseGraph("update_all_edges_online_opt", repo_to_test, debug_mode=debugging)
    # ug_constraints_batch_opt = UseGraph("constraints_batch_opt", repo_to_test, debug_mode=debugging)

    all_ug.append(ug_dicho_online_opt)
    all_ug.append(ug_min_max_online_opt)
    all_ug.append(ug_update_all_edges_online_opt)
    # all_ug.append(ug_constraints_batch_opt)

    for ug in all_ug:
        Thread(target=run_algorithm, args=(ug,visualization)).start()
        time.sleep(2)
