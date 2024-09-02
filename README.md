# **vc2sng** - visually compare 2 social network graphs

## Description
Given two social network graphs (passed as arguments in the GraphML format) visually and quantitatively compare them.  If you use **diff** to compare two text documents, then use **cv2sng** to compare two network graphs. 

## Table of Contents
- [Problem Statement](#problem-statement)
- [Vision](#vision)
- [Inputs](#inputs)
- [Outputs](#outputs)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Problem Statement
It is hard to compare two social networks.  Using rich visualization techniques at side of know statistical reports can help with the problem.  

## Vision
A world where: 
1. Comparing the social structure of distinct groups is easy. 
2. Comparing the social structure of a cohesive group at two points in time is easy. 

## Inputs

This Python script was developed to compare two social network graphs, which are loaded from GraphML files. The comparison focuses on both structural differences (nodes and edges) and attribute differences between the graphs.

**vc2sgn**  is pure Python code built on top of the NetworkX Python library for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks. It imports GraphML files using the read_graphml() function from NetworkX, therefore it vc2sgn can import and compare the following types of graphs: 

- Undirected graphs: Undirected graphs are graphs in which the edges between nodes are not directed. Using NetworkX Graph class for undirected graphs.

- Directed graphs: Directed graphs are graphs in which the edges between nodes are directed.  Using NetworkX DiGraph class for directed graphs.

- Multigraphs: Multigraphs are graphs that can have multiple edges between the same pair of nodes. Using NetworkX MultiDiGraph class for directed multigraphs.

- Weighted graphs: Weighted graphs are graphs in which the edges between nodes have weights associated with them. NetworkX supports weighted graphs by allowing the edges to have a weight attribute.

- Bipartite graphs: Bipartite graphs are graphs in which the nodes can be divided into two disjoint sets, such that every edge connects a node in one set to a node in the other set. When loading those graphs, the NetworkX bipartite module is uded for modelling them. 

**vc2sng** was initially designed to compare social networks of software developers modelled as two-mode networks mined from Git Repositories with ScrapLogGit2Net (see [https://github.com/jaateixeira/ScrapLogGit2Net](https://github.com/jaateixeira/ScrapLogGit2Net)).  ScrapLogGit2Net accepts _git logs_  as input and provides _GraphML_ files as output. The output of ScrapLogGit2Net captures who works with who (i.e., who co-edits source-code files with who) in a Git repository. Its outputs as _GraphML_ files are ready to use with **vc2sng**. 

## Outputs
A description of the expected results or outputs of the project.

##  How does it work 

## Installation
Instructions on how to install your project.

## Usage
This Python script is designed to compare two NetworkX graphs, which are loaded from GraphML files. The comparison focuses on both structural differences (nodes and edges) and attribute differences between the graphs. The script provides visualizations, stastistical reports and logs results.


## Related work 
- Minjeong Shin, Dongwoo Kim, Jae Hee Lee, Umanga Bista, and Lexing Xie. "Visualizing Graph Differences from Social Media Streams." In *Proceedings of the Twelfth ACM International Conference on Web Search and Data Mining (WSDM '19)*, 806–809. Association for Computing Machinery, New York, NY, USA. 2019. [https://doi.org/10.1145/3289600.3290616](https://doi.org/10.1145/3289600.3290616)
- K. Andrews, M. Wohlfahrt, and G. Wurzinger. "Visual Graph Comparison." In *Proceedings of the 13th International Conference on Information Visualisation (IV 2009)*, pp. 62-67. Barcelona, Spain, 2009. [https://doi.org/10.1109/IV.2009.108](https://doi.org/10.1109/IV.2009.108)
- Tantardini, M., Ieva, F., Tajoli, L. et al. Comparing methods for comparing networks. Nature Scientific Reports 9, 17557 (2019). [https://doi.org/10.1038/s41598-019-53708-y]( https://doi.org/10.1038/s41598-019-53708-y)
- Teixeira, J., Robles, G. & González-Barahona, J.M. Lessons learned from applying social network analysis on an industrial Free/Libre/Open Source Software ecosystem. J Internet Serv Appl 6, 14 (2015). [https://doi.org/10.1186/s13174-015-0028-2](https://doi.org/10.1186/s13174-015-0028-2)
  
**Keywords:** Visualization, Prototypes, Design engineering, Maintenance engineering, Tree graphs, Stacking, Information analysis, Business communication, Cognitive science, graph drawing, graph comparison, visual, side-by-side, node equivalence matrix, merge graph, business process models



## Contributing
If you'd like to contribute to this project, please follow the standard GitHub fork and pull request workflow.

## License
This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.


