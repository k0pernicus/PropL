#PropL project

**PropL** is a project of bugs prediction with machine learning, f of *Vincenzo Musco*.  
The **PropL** software is written with Python2.7 and Python3.4.

Published article soon.

###Results

| Project     | Mutant operator | F-score init. | F-score learn.     |
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

###TODO list

*   [ ] Export weights in XML format
*   [ ] Good Git repository
  *   [x] libs/basic_stat_lib : OK (doc + comments)
  *   [x] libs/graph_visualization : OK (doc + comments)
  *   [x] libs/learning_lib : OK (doc + comments)
  *   [x] libs/testing_lib : OK (doc + comments)
  *   [x] libs/tex_lib : OK (doc + comments)
  *   [x] libs/use_graph_lib
  *   [x] libs/utils_lib
  *   [x] libs/xml_lib
  *   [x] libs/xml_parsing_lib
  *   [x] propl
  *   [ ] compute_basename
