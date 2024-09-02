#!/usr/bin/env python3

import argparse
import networkx as nx
import matplotlib.pyplot as plt
from rich import print
from loguru import logger
from rich.progress import track
from networkx import Graph, DiGraph
from typing import Any


def load_graph_with_progress(filepath: str) -> Graph:
    """
    Load a GraphML file into a NetworkX graph with a progress bar.

    This function reads a GraphML file, creates a NetworkX graph, and shows the 
    loading progress using the `rich` library's progress bar.

    Args:
        filepath (str): The path to the GraphML file.

    Returns:
        Graph: The loaded NetworkX graph.
    """

    with Progress() as progress:
        # Initialize a progress task for the GraphML file loading process
        task = progress.add_task("[cyan]Loading GraphML file...", total=100)

        # Load the graph from the GraphML file
        graph: Graph = nx.read_graphml(filepath)
        
        # Get the number of nodes and edges in the graph
        num_nodes: int = graph.number_of_nodes()
        num_edges: int = graph.number_of_edges()

        # Update progress bar less frequently, every 10% of nodes
        for i, node in enumerate(graph.nodes(data=True)):
            if i % (num_nodes // 10 + 1) == 0:  # Avoid division by zero
                progress.update(task, advance=10)

        # Update progress bar less frequently, every 10% of edges
        for i, edge in enumerate(graph.edges(data=True)):
            if i % (num_edges // 10 + 1) == 0:  # Avoid division by zero
                progress.update(task, advance=10)

        # Complete the progress bar
        progress.update(task, advance=100)

    return graph


def compare_node_attributes(graph1, graph2):
    # Iterate over the nodes in graph1
    for node1 in graph1.nodes(data=True):
        node_id = node1[0]
        node_attrs1 = node1[1]

        # Check if the node exists in graph2
        if node_id in graph2.nodes:
            node_attrs2 = graph2.nodes[node_id]

            # Compare the attributes
            for attr_name, attr_value1 in node_attrs1.items():
                if attr_name in node_attrs2:
                    attr_value2 = node_attrs2[attr_name]
                    if attr_value1 != attr_value2:
                        print(f"Node {node_id}: attribute '{attr_name}' differs: {attr_value1} != {attr_value2}")
                else:
                    print(f"Node {node_id}: attribute '{attr_name}' not found in graph2")

            # Check for attributes in graph2 that are not in graph1
            for attr_name, attr_value2 in node_attrs2.items():
                if attr_name not in node_attrs1:
                    print(f"Node {node_id}: attribute '{attr_name}' not found in graph1")

        else:
            print(f"Node {node_id} not found in graph2")


def compare_graphs(graph1, graph2):
    # Determine if graphs are directed
    if isinstance(graph1, DiGraph):
        diff_graph = nx.DiGraph()
        deleted_graph = nx.DiGraph()
        added_graph = nx.DiGraph()
    else:
        diff_graph = nx.Graph()
        deleted_graph = nx.Graph()
        added_graph = nx.Graph()

    # Nodes and edges in graph1 but not in graph2 (deleted)
    deleted_graph.add_nodes_from(set(graph1.nodes()) - set(graph2.nodes()))
    deleted_edges = set(graph1.edges()) - set(graph2.edges())
    deleted_graph.add_edges_from(deleted_edges)

    # Nodes and edges in graph2 but not in graph1 (added)
    added_graph.add_nodes_from(set(graph2.nodes()) - set(graph1.nodes()))
    added_edges = set(graph2.edges()) - set(graph1.edges())
    added_graph.add_edges_from(added_edges)

    # Handle weighted edges
    for edge in deleted_edges:
        if 'weight' in graph1.edges[edge]:
            deleted_graph.edges[edge]['weight'] = graph1.edges[edge]['weight']
            
    for edge in added_edges:
        if 'weight' in graph2.edges[edge]:
            added_graph.edges[edge]['weight'] = graph2.edges[edge]['weight']

    # Add edges with different attributes
    for edge in set(graph1.edges()) & set(graph2.edges()):
        if graph1.edges[edge] != graph2.edges[edge]:
            diff_graph.add_edge(*edge, color='yellow')

    # Add nodes with different attributes
    for node in set(graph1.nodes()) & set(graph2.nodes()):
        if graph1.nodes[node] != graph2.nodes[node]:
            diff_graph.add_node(node, color='yellow')

    # Visualize the difference graph
    pos = nx.spring_layout(diff_graph)
    nx.draw_networkx_nodes(diff_graph, pos, node_color=[diff_graph.nodes[n].get('color', 'blue') for n in diff_graph.nodes])
    nx.draw_networkx_edges(diff_graph, pos, edge_color=[diff_graph.edges[e].get('color', 'black') for e in diff_graph.edges])
    nx.draw_networkx_labels(diff_graph, pos)
    plt.title("Differences Between Graphs")
    plt.show()

    # Visualize deleted graph
    pos_deleted = nx.spring_layout(deleted_graph)
    edge_weights = nx.get_edge_attributes(deleted_graph, 'weight').values()
    nx.draw_networkx(deleted_graph, pos_deleted, with_labels=True, node_color='red', edge_color='red', width=list(edge_weights) if edge_weights else 1)
    plt.title("Deleted Nodes/Edges")
    plt.show()

    # Visualize added graph
    pos_added = nx.spring_layout(added_graph)
    edge_weights = nx.get_edge_attributes(added_graph, 'weight').values()
    nx.draw_networkx(added_graph, pos_added, with_labels=True, node_color='green', edge_color='green', width=list(edge_weights) if edge_weights else 1)
    plt.title("Added Nodes/Edges")
    plt.show()

    # Log the results
    logger.info(f"Number of nodes in graph1: {graph1.number_of_nodes()}")
    logger.info(f"Number of nodes in graph2: {graph2.number_of_nodes()}")
    logger.info(f"Number of edges in graph1: {graph1.number_of_edges()}")
    logger.info(f"Number of edges in graph2: {graph2.number_of_edges()}")
    logger.info(f"Number of nodes in difference graph: {diff_graph.number_of_nodes()}")
    logger.info(f"Number of edges in difference graph: {diff_graph.number_of_edges()}")
    logger.info(f"Number of nodes in deleted graph: {deleted_graph.number_of_nodes()}")
    logger.info(f"Number of edges in deleted graph: {deleted_graph.number_of_edges()}")
    logger.info(f"Number of nodes in added graph: {added_graph.number_of_nodes()}")
    logger.info(f"Number of edges in added graph: {added_graph.number_of_edges()}")

    # Print the results using Rich
    print(f"[bold]Number of nodes in graph1:[/bold] {graph1.number_of_nodes()}")
    print(f"[bold]Number of nodes in graph2:[/bold] {graph2.number_of_nodes()}")
    print(f"[bold]Number of edges in graph1:[/bold] {graph1.number_of_edges()}")
    print(f"[bold]Number of edges in graph2:[/bold] {graph2.number_of_edges()}")
    print(f"[bold]Number of nodes in difference graph:[/bold] {diff_graph.number_of_nodes()}")
    print(f"[bold]Number of edges in difference graph:[/bold] {diff_graph.number_of_edges()}")
    print(f"[bold]Number of nodes in deleted graph:[/bold] {deleted_graph.number_of_nodes()}")
    print(f"[bold]Number of edges in deleted graph:[/bold] {deleted_graph.number_of_edges()}")
    print(f"[bold]Number of nodes in added graph:[/bold] {added_graph.number_of_nodes()}")
    print(f"[bold]Number of edges in added graph:[/bold] {added_graph.number_of_edges()}")

if __name__ == '__main__':
    # Configure Argparse to accept two GraphML files as input
    parser = argparse.ArgumentParser(description='Compare two NetworkX graphs')
    parser.add_argument('graph1', type=str, help='Path to the first GraphML file')
    parser.add_argument('graph2', type=str, help='Path to the second GraphML file')
    args = parser.parse_args()

    logger.info("Reading 1st graphml file {args.graph1}")
    graph1 = nx.read_graphml(args.graph1)
    logger.info("Reading 2nd graphml file {args.graph2}")
    graph2 = nx.read_graphml(args.graph2)
    
    # Compare the graphs visually and by differences
    compare_graphs(graph1, graph2)

    # Compare node attributes 
    compare_node_attributes(graph1, graph2)
