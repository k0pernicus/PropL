#PropL project

**PropL** is a project of bugs prediction with machine learning, following works of *Vincenzo Musco*.  
The **PropL** software is written with Python2.7 and Python3.4.
The stochastic software is being developed.

*   [Results](#results)
*   [Scientific papers](#scientific_papers)
*   [Files](#files)
*   [Dependencies](#dependencies)
*   [How to use it?](#how_to_use_it)
*   [Contacts](#contacts)

###<a name="results"></a>Results

| Java Project     | Mutant operator | F-score init. | F-score learn.     |
|-------------|-----------------|---------------|--------------------|
| Codec       | ABS             | 0.00          | **0.56**           |
| Codec       | AOR             | 0.19          | **0.75**           |
| Codec       | LCR             | 0.11          | **0.66**           |
| Codec       | ROR             | 0.19          | **0.74**           |
| Codec       | UOI             | 0.20          | **0.77**           |
| Collections | ABS             | **0.26**      | 0.20           |
| Collections | AOR             | **0.67**          | 0.27           |
| Collections | LCR             | 0.25          | **0.29**           |
| Collections | ROR             | **0.24**          | 0.23           |
| Collections | UOI             | **0.63**          | 0.36           |
| Gson        | ABS             | 0.00          | **0.79**           |
| Gson        | AOR             | 0.03          | **0.73**           |
| Gson        | LCR             | 0.02          | **0.76**           |
| Gson        | ROR             | 0.05          | **0.82**           |
| Gson        | UOI             | 0.05          | **0.83**           |
| Io          | ABS             | 0.06          | **0.57**           |
| Io          | AOR             | 0.32          | **0.66**           |
| Io          | LCR             | 0.29          | **0.74**           |
| Io          | ROR             | 0.50          | **0.71**           |
| Io          | UOI             | 0.42          | **0.7**            |
| Lang        | ABS             | 0.00          | **0.39**           |
| Lang        | AOR             | 0.60          | 0.60           |
| Lang        | LCR             | 0.40          | **0.53**           |
| Lang        | ROR             | **0.67**          | 0.56           |
| Lang        | UOI             | 0.67          | **0.79**           |
| Shindig     | ABS             | 0.00          | **0.55**           |
| Shindig     | AOR             | 0.50          | **0.62**           |
| Shindig     | LCR             | 0.33          | **0.57**           |
| Shindig     | ROR             | 0.40          | **0.66**           |
| Shindig     | UOI             | 0.50          | **0.65**           |
| Sonar       | ABS             | **0.40**          | 0.00           |
| Sonar       | AOR             | 0.17          | **0.60**           |
| Sonar       | LCR             | **0.67**          | 0.54           |
| Sonar       | ROR             | **0.67**          | 0.00           |
| Sonar       | UOI             | 0.17          | **0.67**           |
| Spojo       | ABS             | 0.00          | 0.00           |
| Spojo       | AOR             | 0.00          | 0.00           |
| Spojo       | LCR             | 0.32          | **0.64**           |
| Spojo       | ROR             | 0.29          | **0.80**           |
| Spojo       | UOI             | 0.00          | **0.65**           |

###<a name="scientific_papers"></a>Scientific papers

*   [Initial work of *Vincenzo Musco*](https://hal.inria.fr/hal-01120913)
*   [The learning approach - **soon**]()

###<a name="files"></a>Files

*   **compute-basename.py** : Program to compute f-scores with the algorithm of *Vincenzo Musco* (F-score init.).
*   **propl.py** : Program to compute f-scores with the learning approach (F-score learn.).
*   ***libs/***
    *   **basic_stat_lib.py** : Some functions to make some stats (compute precision, recall, f-score, etc...)
    *   **graph_visualization.py** : Program (Python2.7) to visualize impacted nodes in a .graphml file
    *   **learning_lib.py** : Some learning algorithms
    *   **testing_lib.py** : Some functions to test the learning algorithm choose on tests sample
    *   **tex_lib.py** : Library to write results in a tex file
    *   **use_graph_lib.py** : Object which represents a use graph (see the definition of a use graph in the recent paper of *Vincenzo Musco*)
    *   **utils_lib.py** : Some functions to chunk a list, write into a CSV file, etc...
    *   **xml_lib.py** : Personal XML library to load and give an appreciation on the XML document (valid or not)
    *   **xml_parsing_lib.py** : Personal XML library to parse XML documents from *Vincenzo Musco*
    *   ***exceptions/***
        *   **FailToLoad.py**
        *   **NoArgument.py**
        *   **RunError.py**

###<a name="dependencies"></a>Dependencies

*   **networkx** (*Python2.7*/*Python3.4*)
*   **numpy** (*Python2.7*/*Python3.7*)
*   **matplotlib** (*Python2.7* only)

###<a name="how_to_use_it"></a>How to use it?

You can use the script written in **bash** : ```chmod +x run.sh && ./run.sh directory_test usegraph_x.graphml directory_to_store_results```, or...

*   In the root directory : ```python3.4 propl.py <your_test_directory> <number_of_tests> [--option]```
*   For help : ```python3.4 prop.py --help```

###<a name="contacts"></a>Contacts

*   **Developer** : *Antonin Carette* (antonin[dot]carette[at]etudiant[dot]univ-lille1[dot]fr)
*   **First supervisor** : *Philippe Preux* (philippe[dot]preux[at]inria[dot]fr)
*   **Second supervisor** : *Martin Monperrus* (martin[dot]monperrus[at]univ-lille1[dot]fr)
*   **Third supervisor** : *Vincenzo Musco* (vincenzo[dot]musco[at]inria[dot]fr)
