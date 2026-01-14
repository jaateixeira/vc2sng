#!/usr/bin/env python3

import argparse
import networkx as nx
import matplotlib.pyplot as plt
import json
from matplotlib.patches import Patch
from matplotlib.colors import to_hex
from rich import print
from loguru import logger
from networkx import Graph, DiGraph
from rich.progress import Progress
from pathlib import Path


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


def compare_node_attributes(graph_a: nx.Graph, graph_b: nx.Graph):
    """
    Compare node attributes between two graphs.

    Args:
        graph_a: First graph
        graph_b: Second graph
    """
    # Iterate over the nodes in graph1
    for node1 in graph_a.nodes(data=True):
        node_id = node1[0]
        node_attrs1 = node1[1]

        # Check if the node exists in graph2
        if node_id in graph_b.nodes:
            node_attrs2 = graph_b.nodes[node_id]

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


def load_color_dict(color_dict_path: str = None) -> dict:
    """
    Load color dictionary from JSON file.

    Args:
        color_dict_path: Path to JSON file with color mappings

    Returns:
        Dictionary mapping organization names to colors
    """
    default_colors = {
        "google": "red",
        "nvidia": "limegreen",
        "intel": "lightblue",
        "amd": "black",
        "arm": "steelblue",
        "amazon": "orange",
        "ibm": "darkblue",
        "linaro": "pink",
        "bytedance": "gray"
    }

    if color_dict_path:
        try:
            with open(color_dict_path, 'r') as f:
                color_dict = json.load(f)
                print(f"[green]Loaded color dictionary from {color_dict_path}[/green]")
                return color_dict
        except FileNotFoundError:
            print(
                f"[yellow]Warning: Color dictionary file '{color_dict_path}' not found. Using default colors.[/yellow]")
            return default_colors
        except json.JSONDecodeError:
            print(
                f"[yellow]Warning: Invalid JSON in color dictionary file '{color_dict_path}'. Using default colors.[/yellow]")
            return default_colors
    else:
        return default_colors


def color_to_hex(color):
    """Convert color to hex string for Rich output."""
    if isinstance(color, str):
        return color
    elif isinstance(color, tuple) and len(color) == 4:
        # RGBA tuple - convert to hex (ignoring alpha)
        return to_hex(color[:3])  # Convert RGB to hex
    elif isinstance(color, tuple) and len(color) == 3:
        # RGB tuple
        return to_hex(color)
    else:
        # Return string representation for other types
        return str(color)


def extract_affiliations(graph: nx.Graph, affiliation_key: str = 'affiliation') -> dict:
    """
    Extract unique affiliations from graph nodes.

    Args:
        graph: NetworkX graph
        affiliation_key: Attribute name for affiliation

    Returns:
        Dictionary mapping affiliation names to colors
    """
    affiliations = {}
    # Use tab20 colormap to generate distinct colors
    color_palette = plt.cm.tab20

    # Collect all unique affiliations
    unique_affiliations = set()
    for node, attrs in graph.nodes(data=True):
        # Try the specified affiliation key and other common names
        for attr_name in [affiliation_key, 'd2', 'organization', 'institution', 'affiliation']:
            if attr_name in attrs:
                unique_affiliations.add(str(attrs[attr_name]))
                break

    # Map each affiliation to a color (will be updated later if color dict is provided)
    affiliations_list = sorted(unique_affiliations)
    for i, affiliation in enumerate(affiliations_list):
        # Get color from tab20 colormap (normalized position between 0 and 1)
        color_position = i / max(len(affiliations_list), 1)
        color = color_palette(color_position)
        affiliations[affiliation] = color

    return affiliations


def get_node_color(node_id: str, graph: nx.Graph, affiliations: dict,
                   color_dict: dict = None, default_color: str = 'gray') -> str:
    """
    Get color for a node based on its affiliation.

    Args:
        node_id: Node identifier
        graph: NetworkX graph
        affiliations: Dictionary mapping affiliations to colors
        color_dict: Dictionary with predefined organization colors
        default_color: Default color if no affiliation found

    Returns:
        Color string or tuple
    """
    node_attrs = graph.nodes.get(node_id, {})

    # Check for affiliation attributes
    affiliation_keys = ['affiliation', 'd2', 'organization', 'institution']
    affiliation_value = None

    for attr_name in affiliation_keys:
        if attr_name in node_attrs:
            affiliation_value = str(node_attrs[attr_name])
            break

    if affiliation_value:
        # Check if we have a predefined color for this affiliation
        if color_dict and affiliation_value in color_dict:
            return color_dict[affiliation_value]

        # Check if we have a color in the affiliations dict
        if affiliation_value in affiliations:
            color = affiliations[affiliation_value]
            return color

    return default_color


def compare_graphs(graph_a: nx.Graph, graph_b: nx.Graph,
                   show_affiliation_legend: bool = False,
                   affiliation_key: str = 'affiliation',
                   color_dict: dict = None):
    """
    Compare two graphs and visualize differences.

    Args:
        graph_a: First graph
        graph_b: Second graph
        show_affiliation_legend: Whether to show affiliation legend
        affiliation_key: Attribute name for affiliation
        color_dict: Dictionary with predefined organization colors
    """
    # Determine if graphs are directed
    if isinstance(graph_a, DiGraph):
        diff_graph = nx.DiGraph()
        deleted_graph = nx.DiGraph()
        added_graph = nx.DiGraph()
    else:
        diff_graph = nx.Graph()
        deleted_graph = nx.Graph()
        added_graph = nx.Graph()

    # Nodes and edges in graph1 but not in graph2 (deleted)
    deleted_nodes = set(graph_a.nodes()) - set(graph_b.nodes())
    deleted_edges = set(graph_a.edges()) - set(graph_b.edges())
    deleted_graph.add_nodes_from(deleted_nodes)
    deleted_graph.add_edges_from(deleted_edges)

    # Nodes and edges in graph2 but not in graph1 (added)
    added_nodes = set(graph_b.nodes()) - set(graph_a.nodes())
    added_edges = set(graph_b.edges()) - set(graph_a.edges())
    added_graph.add_nodes_from(added_nodes)
    added_graph.add_edges_from(added_edges)

    # Handle weighted edges
    for edge in deleted_edges:
        if 'weight' in graph_a.edges[edge]:
            deleted_graph.edges[edge]['weight'] = graph_a.edges[edge]['weight']

    for edge in added_edges:
        if 'weight' in graph_b.edges[edge]:
            added_graph.edges[edge]['weight'] = graph_b.edges[edge]['weight']

    # Add edges with different attributes
    for edge in set(graph_a.edges()) & set(graph_b.edges()):
        if graph_a.edges[edge] != graph_b.edges[edge]:
            diff_graph.add_edge(*edge, color='yellow')

    # Add nodes with different attributes
    for node in set(graph_a.nodes()) & set(graph_b.nodes()):
        if graph_a.nodes[node] != graph_b.nodes[node]:
            diff_graph.add_node(node, color='yellow')
        else:
            # Add node with same attributes for context
            diff_graph.add_node(node)

    # Extract affiliations from combined graph data for legend
    combined_graph = nx.compose(graph_a, graph_b)
    affiliations = extract_affiliations(combined_graph, affiliation_key)

    # Update affiliations with color dict if available
    if color_dict:
        for affiliation in affiliations.keys():
            if affiliation in color_dict:
                affiliations[affiliation] = color_dict[affiliation]

    # Visualize the difference graph
    fig1, ax1 = plt.subplots(figsize=(14, 8) if show_affiliation_legend else (10, 8))
    pos = nx.spring_layout(diff_graph)

    # Get colors for nodes based on their affiliation
    node_colors = []
    for node in diff_graph.nodes():
        if 'color' in diff_graph.nodes[node] and diff_graph.nodes[node]['color'] == 'yellow':
            # Nodes with different attributes
            node_colors.append('yellow')
        else:
            # Get color based on affiliation from original graph
            if node in graph_a.nodes():
                node_colors.append(get_node_color(node, graph_a, affiliations, color_dict))
            elif node in graph_b.nodes():
                node_colors.append(get_node_color(node, graph_b, affiliations, color_dict))
            else:
                node_colors.append('gray')

    # Get edge colors
    edge_colors = [diff_graph.edges[e].get('color', 'black') for e in diff_graph.edges()]

    # Draw the graph
    nx.draw_networkx_nodes(diff_graph, pos, node_color=node_colors, ax=ax1)
    nx.draw_networkx_edges(diff_graph, pos, edge_color=edge_colors, ax=ax1)
    nx.draw_networkx_labels(diff_graph, pos, ax=ax1)

    # Add legend if requested
    if show_affiliation_legend:
        # Create legend elements for affiliations
        legend_elements = []

        # Get all affiliations present in this graph
        present_affiliations = set()
        for node in diff_graph.nodes():
            if node in graph_a.nodes():
                for attr_name in [affiliation_key, 'd2', 'organization', 'institution', 'affiliation']:
                    if attr_name in graph_a.nodes[node]:
                        present_affiliations.add(str(graph_a.nodes[node][attr_name]))
                        break
            elif node in graph_b.nodes():
                for attr_name in [affiliation_key, 'd2', 'organization', 'institution', 'affiliation']:
                    if attr_name in graph_b.nodes[node]:
                        present_affiliations.add(str(graph_b.nodes[node][attr_name]))
                        break

        # Add affiliation legend items for present affiliations
        for affiliation, color in affiliations.items():
            if affiliation in present_affiliations:
                legend_elements.append(
                    Patch(facecolor=color, edgecolor='black', label=f'{affiliation}')
                )

        # Add difference legend item if present
        if any(c == 'yellow' for c in node_colors) or any(c == 'yellow' for c in edge_colors):
            legend_elements.append(
                Patch(facecolor='yellow', edgecolor='black', label='Different Attributes')
            )

        ax1.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small')

    plt.title("Differences Between Graphs (Nodes colored by affiliation)")
    plt.tight_layout()
    plt.show()

    # Visualize deleted graph
    fig2, ax2 = plt.subplots(figsize=(14, 8) if show_affiliation_legend else (10, 8))

    if deleted_graph.number_of_nodes() > 0:
        pos_deleted = nx.spring_layout(deleted_graph)

        # Get colors for ALL nodes in deleted_graph (not just deleted_nodes)
        deleted_node_colors = []
        for node in deleted_graph.nodes():
            color = get_node_color(node, graph_a, affiliations, color_dict, 'red')
            deleted_node_colors.append(color)

        edge_weights = nx.get_edge_attributes(deleted_graph, 'weight').values()
        edge_widths = list(edge_weights) if edge_weights else [1] * deleted_graph.number_of_edges()

        nx.draw_networkx_nodes(deleted_graph, pos_deleted, node_color=deleted_node_colors, ax=ax2)
        nx.draw_networkx_edges(deleted_graph, pos_deleted, edge_color='red', width=edge_widths, ax=ax2)
        nx.draw_networkx_labels(deleted_graph, pos_deleted, ax=ax2)

        # Add legend if requested
        if show_affiliation_legend:
            legend_elements = []

            # Add affiliation legend items for nodes in deleted graph
            deleted_affiliations = set()
            for node in deleted_graph.nodes():
                for attr_name in [affiliation_key, 'd2', 'organization', 'institution', 'affiliation']:
                    if attr_name in graph_a.nodes[node]:
                        deleted_affiliations.add(str(graph_a.nodes[node][attr_name]))
                        break

            for affiliation, color in affiliations.items():
                if affiliation in deleted_affiliations:
                    legend_elements.append(
                        Patch(facecolor=color, edgecolor='black', label=f'{affiliation} (Deleted)')
                    )

            ax2.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small')

        plt.title("Deleted Nodes/Edges (Colored by affiliation)")
        plt.tight_layout()
        plt.show()
    else:
        print("[INFO] No deleted nodes/edges to visualize")

    # Visualize added graph
    fig3, ax3 = plt.subplots(figsize=(14, 8) if show_affiliation_legend else (10, 8))

    if added_graph.number_of_nodes() > 0:
        pos_added = nx.spring_layout(added_graph)

        # Get colors for ALL nodes in added_graph (not just added_nodes)
        added_node_colors = []
        for node in added_graph.nodes():
            # If node is truly added (not in graph_a), use green default
            if node in added_nodes:
                color = get_node_color(node, graph_b, affiliations, color_dict, 'green')
            else:
                # Node exists in both graphs but has new edges - use its normal affiliation color
                color = get_node_color(node, graph_b, affiliations, color_dict, 'lightgreen')
            added_node_colors.append(color)

        edge_weights = nx.get_edge_attributes(added_graph, 'weight').values()
        edge_widths = list(edge_weights) if edge_weights else [1] * added_graph.number_of_edges()

        nx.draw_networkx_nodes(added_graph, pos_added, node_color=added_node_colors, ax=ax3)
        nx.draw_networkx_edges(added_graph, pos_added, edge_color='green', width=edge_widths, ax=ax3)
        nx.draw_networkx_labels(added_graph, pos_added, ax=ax3)

        # Add legend if requested
        if show_affiliation_legend:
            legend_elements = []

            # Add affiliation legend items for nodes in added graph
            added_affiliations = set()
            for node in added_graph.nodes():
                for attr_name in [affiliation_key, 'd2', 'organization', 'institution', 'affiliation']:
                    if attr_name in graph_b.nodes[node]:
                        added_affiliations.add(str(graph_b.nodes[node][attr_name]))
                        break

            for affiliation, color in affiliations.items():
                if affiliation in added_affiliations:
                    legend_elements.append(
                        Patch(facecolor=color, edgecolor='black', label=f'{affiliation} (Added/Connected)')
                    )

            ax3.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small')

        plt.title("Added Nodes/Edges (Colored by affiliation)")
        plt.tight_layout()
        plt.show()
    else:
        print("[INFO] No added nodes/edges to visualize")

    # Log the results
    logger.info(f"Number of nodes in graph1: {graph_a.number_of_nodes()}")
    logger.info(f"Number of nodes in graph2: {graph_b.number_of_nodes()}")
    logger.info(f"Number of edges in graph1: {graph_a.number_of_edges()}")
    logger.info(f"Number of edges in graph2: {graph_b.number_of_edges()}")
    logger.info(f"Number of truly added nodes: {len(added_nodes)}")
    logger.info(f"Number of truly deleted nodes: {len(deleted_nodes)}")
    logger.info(f"Number of nodes in added graph (including endpoints): {added_graph.number_of_nodes()}")
    logger.info(f"Number of edges in added graph: {added_graph.number_of_edges()}")
    logger.info(f"Number of nodes in deleted graph (including endpoints): {deleted_graph.number_of_nodes()}")
    logger.info(f"Number of edges in deleted graph: {deleted_graph.number_of_edges()}")

    # Print the results using Rich
    print(f"[bold]Number of nodes in graph1:[/bold] {graph_a.number_of_nodes()}")
    print(f"[bold]Number of nodes in graph2:[/bold] {graph_b.number_of_nodes()}")
    print(f"[bold]Number of edges in graph1:[/bold] {graph_a.number_of_edges()}")
    print(f"[bold]Number of edges in graph2:[/bold] {graph_b.number_of_edges()}")
    print(f"[bold]Number of truly added nodes:[/bold] {len(added_nodes)}")
    print(f"[bold]Number of truly deleted nodes:[/bold] {len(deleted_nodes)}")
    print(f"[bold]Number of added edges:[/bold] {len(added_edges)}")
    print(f"[bold]Number of deleted edges:[/bold] {len(deleted_edges)}")

    # Print affiliation summary
    print("\n[bold cyan]Affiliation Summary:[/bold cyan]")
    for affiliation, color in affiliations.items():
        # Count nodes per affiliation in each graph
        count_a = sum(1 for node in graph_a.nodes()
                      if any(attr in graph_a.nodes[node] and str(graph_a.nodes[node][attr]) == affiliation
                             for attr in ['affiliation', 'd2', 'organization', 'institution', affiliation_key]))
        count_b = sum(1 for node in graph_b.nodes()
                      if any(attr in graph_b.nodes[node] and str(graph_b.nodes[node][attr]) == affiliation
                             for attr in ['affiliation', 'd2', 'organization', 'institution', affiliation_key]))
        if count_a > 0 or count_b > 0:
            hex_color = color_to_hex(color)
            print(f"  [color({hex_color})]█[/color({hex_color})] {affiliation}: Graph1={count_a}, Graph2={count_b}")


if __name__ == '__main__':
    # Configure Argparse to accept two GraphML files as input
    parser = argparse.ArgumentParser(description='Compare two NetworkX graphs')
    parser.add_argument('graph1', type=str, help='Path to the first GraphML file')
    parser.add_argument('graph2', type=str, help='Path to the second GraphML file')
    parser.add_argument('--legend-affiliations', '-la', action='store_true',
                        help='Show legend on the right side of visualizations with affiliations')
    parser.add_argument('--affiliation-key', '-a', type=str, default='affiliation',
                        help='Attribute name for affiliation (default: "affiliation")')
    parser.add_argument('--color-dict', '-c', type=str,
                        help='Path to JSON file with organization-color mappings')
    args = parser.parse_args()

    logger.info(f"Reading 1st graphml file {args.graph1}")
    graph1 = nx.read_graphml(args.graph1)
    logger.info(f"Reading 2nd graphml file {args.graph2}")
    graph2 = nx.read_graphml(args.graph2)

    # Load color dictionary if provided
    color_dict = load_color_dict(args.color_dict) if args.color_dict else None

    # Compare the graphs visually and by differences
    compare_graphs(graph1, graph2,
                   show_affiliation_legend=args.legend_affiliations,
                   affiliation_key=args.affiliation_key,
                   color_dict=color_dict)

    # Compare node attributes
    compare_node_attributes(graph1, graph2)