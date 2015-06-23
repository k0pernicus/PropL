from libs.use_graph_lib import UseGraph

from libs.learning_lib import dichotomicOnlineOptimization
from libs.learning_lib import minAndMaxOnlineOptimization
from libs.learning_lib import updateAllEdgesOnlineOptimization
from libs.learning_lib import constraintsBatchOptimization

from libs.basic_stat import getSomeStats

from threading import Thread

def run_algorithm(ug):
    """
    Method to run the usegraph
    """

    ug.run()

    if ug.id == "dicho_online_opt":
        dichotomicOnlineOptimization(ug)
        ug.visualize()
        getSomeStats(ug)

    if ug.id == "min_max_online_opt":
        minAndMaxOnlineOptimization(ug)
        ug.visualize()
        getSomeStats(ug)

    if ug.id == "update_all_edges_online_opt":
        updateAllEdgesOnlineOptimization(ug)
        ug.visualize()
        getSomeStats(ug)

    if ug.id == "constraints_batch_opt":
        constraintsBatchOptimization(ug)
        ug.visualize()
        getSomeStats(ug)

all_ug = []

ug_dicho_online_opt = UseGraph("dicho_online_opt", "tests/test1/")
ug_min_max_online_opt = UseGraph("min_max_online_opt", "tests/test1/")
ug_update_all_edges_online_opt = UseGraph("update_all_edges_online_opt", "tests/test1/")
ug_constraints_batch_opt = UseGraph("constraints_batch_opt", "tests/test1/")

all_ug.append(ug_dicho_online_opt)
all_ug.append(ug_min_max_online_opt)
all_ug.append(ug_update_all_edges_online_opt)
all_ug.append(ug_constraints_batch_opt)

for ug in all_ug:
    Thread(target=run_algorithm, args=(ug,)).start()
