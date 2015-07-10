#PropL project

**PropL** is a project of bugs prediction with machine learning, following works of *Vincenzo Musco*.  
The **PropL** software is written with Python2.7 and Python3.4.

Published article soon.

###Results

| Project     | Mutant operator | F-score init. | F-score learn. | \% Increase |
|-------------|-----------------|---------------|----------------|-------------|
| Codec       | ABS             | 0.00          | 0.56           | +560\%      |
| Codec       | AOR             | 0.19          | 0.75           | +39\%       |
| Codec       | LCR             | 0.11          | 0.66           | +60\%       |
| Codec       | ROR             | 0.19          | 0.74           | +39\%       |
| Codec       | UOI             | 0.20          | 0.77           | +39\%       |
| Collections | ABS             | 0.26          | 0.20           | -23\%       |
| Collections | AOR             | 0.0.67        | 0.27           | -59.7\%     |
| Collections | LCR             | 0.25          | 0.29           | -13.8\%     |
| Collections | ROR             | 0.24          | 0.23           | -4.2\%      |
| Collections | UOI             | 0.63          | 0.36           | -42.86\%    |
| Gson        | ABS             | 0.00          | 0.79           | +790\%      |
| Gson        | AOR             | 0.03          | 0.73           | +2330\%     |
| Gson        | LCR             | 0.02          | 0.76           | +3700\%     |
| Gson        | ROR             | 0.05          | 0.82           | +1540\%     |
| Gson        | UOI             | 0.05          | 0.83           | +1560\%     |
| Io          | ABS             | 0.06          | 0.57           | +95\%       |
| Io          | AOR             | 0.32          | 0.66           | +106\%      |
| Io          | LCR             | 0.29          | 0.74           | +255\%      |
| Io          | ROR             | 0.50          | 0.71           | +42\%       |
| Io          | UOI             | 0.42          | 0.7            | +67\%       |
| Lang        | ABS             | 0.00          | 0.39           | +390\%      |
| Lang        | AOR             | 0.60          | 0.60           | +0\%        |
| Lang        | LCR             | 0.40          | 0.53           | +32\%       |
| Lang        | ROR             | 0.67          | 0.56           | -16.41\%    |
| Lang        | UOI             | 0.67          | 0.79           | +18\%       |
| Shindig     | ABS             | 0.00          | 0.55           | +550\%      |
| Shindig     | AOR             | 0.50          | 0.62           | +24\%       |
| Shindig     | LCR             | 0.33          | 0.57           | +73\%       |
| Shindig     | ROR             | 0.40          | 0.66           | +65\%       |
| Shindig     | UOI             | 0.50          | 0.65           | +30\%       |
| Sonar       | ABS             | 0.40          | 0.00           | -400\%      |
| Sonar       | AOR             | 0.17          | 0.60           | +252\%      |
| Sonar       | LCR             | 0.67          | 0.54           | -19.4\%     |
| Sonar       | ROR             | 0.67          | 0.00           | -670\%      |
| Sonar       | UOI             | 0.17          | 0.67           | +294\%      |
| Spojo       | ABS             | 0.00          | 0.00           | +0\%        |
| Spojo       | AOR             | 0.00          | 0.00           | +0\%        |
| Spojo       | LCR             | 0.32          | 0.64           | +200\%      |
| Spojo       | ROR             | 0.29          | 0.80           | +275\%      |
| Spojo       | UOI             | 0.00          | 0.65           | +650\%      |

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
