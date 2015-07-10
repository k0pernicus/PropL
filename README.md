#PropL project

**PropL** is a project of bugs prediction with machine learning, following works of *Vincenzo Musco*.  
The **PropL** software is written with Python2.7 and Python3.4.

Published article soon.

###Results

| Project     | Mutant operator | F-score init. | F-score learn. |   Increase  |
|-------------|-----------------|---------------|----------------|-------------|
| Codec       | ABS             | 0.00          | 0.56           | +0.56       |
| Codec       | AOR             | 0.19          | 0.75           | +0.56       |
| Codec       | LCR             | 0.11          | 0.66           | +0.55       |
| Codec       | ROR             | 0.19          | 0.74           | +0.55       |
| Codec       | UOI             | 0.20          | 0.77           | +0.57       |
| Collections | ABS             | 0.26          | 0.20           | -0.06       |
| Collections | AOR             | 0.67          | 0.27           | -0.40       |
| Collections | LCR             | 0.25          | 0.29           | +0.04       |
| Collections | ROR             | 0.24          | 0.23           | -0.01       |
| Collections | UOI             | 0.63          | 0.36           | -0.27       |
| Gson        | ABS             | 0.00          | 0.79           | +0.79       |
| Gson        | AOR             | 0.03          | 0.73           | +0.70       |
| Gson        | LCR             | 0.02          | 0.76           | +0.74       |
| Gson        | ROR             | 0.05          | 0.82           | +0.77       |
| Gson        | UOI             | 0.05          | 0.83           | +0.78       |
| Io          | ABS             | 0.06          | 0.57           | +0.51       |
| Io          | AOR             | 0.32          | 0.66           | +0.34       |
| Io          | LCR             | 0.29          | 0.74           | +0.45       |
| Io          | ROR             | 0.50          | 0.71           | +0.21       |
| Io          | UOI             | 0.42          | 0.7            | +0.28       |
| Lang        | ABS             | 0.00          | 0.39           | +0.39       |
| Lang        | AOR             | 0.60          | 0.60           | +0.00       |
| Lang        | LCR             | 0.40          | 0.53           | +0.13       |
| Lang        | ROR             | 0.67          | 0.56           | -0.11       |
| Lang        | UOI             | 0.67          | 0.79           | +0.12       |
| Shindig     | ABS             | 0.00          | 0.55           | +0.55       |
| Shindig     | AOR             | 0.50          | 0.62           | +0.12       |
| Shindig     | LCR             | 0.33          | 0.57           | +0.24       |
| Shindig     | ROR             | 0.40          | 0.66           | +0.26       |
| Shindig     | UOI             | 0.50          | 0.65           | +0.15       |
| Sonar       | ABS             | 0.40          | 0.00           | -0.40       |
| Sonar       | AOR             | 0.17          | 0.60           | +0.43       |
| Sonar       | LCR             | 0.67          | 0.54           | -0.13       |
| Sonar       | ROR             | 0.67          | 0.00           | -0.67       |
| Sonar       | UOI             | 0.17          | 0.67           | +0.50       |
| Spojo       | ABS             | 0.00          | 0.00           | +0.00       |
| Spojo       | AOR             | 0.00          | 0.00           | +0.00       |
| Spojo       | LCR             | 0.32          | 0.64           | +0.32       |
| Spojo       | ROR             | 0.29          | 0.80           | +0.51       |
| Spojo       | UOI             | 0.00          | 0.65           | +0.65       |

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
