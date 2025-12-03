"""
Module to handle single linked list nodes (slln) and tree node structures.

This code is based on the implementation proposed by the following authors/books:
    #. Algorithms, 4th Edition, Robert Sedgewick and Kevin Wayne.
    #. Data Structure and Algorithms in Python, M.T. Goodrich, R. Tamassia, M.H. Goldwasser.
"""

RED = "red"
BLACK = "black"


def new_bst_node(k: object, v: object, n: int = 1) -> dict:
    """
    Creates a new node for a binary search tree (BST) and returns it.

    Args:
        k (object): Key of the key-value pair.
        v (object): Value of the key-value pair.
        n (int, optional): Size of the subtree to which the node belongs. Defaults to 1.

    Returns:
        dict: A new BST node containing the key-value pair.
    """
    return {
        "key": k,
        "value": v,
        "size": n,
        "left": None,
        "right": None,
        "_type": "BST"
    }


def new_rbt_node(k: object, v: object, n: int, color: str) -> dict:
    """
    Creates a new node for a Red-Black Tree (RBT).

    Args:
        k (object): Key of the node.
        v (object): Value of the node.
        n (int): Size of the subtree.
        color (str): Color of the node ("red" or "black").

    Returns:
        dict: A new RBT node.
    """
    return {
        "key": k,
        "value": v,
        "size": n,
        "parent": None,
        "left": None,
        "right": None,
        "color": color,
        "_type": "LLRBT"
    }


def is_red(node: dict) -> bool:
    """
    Checks whether a node is red.

    Args:
        node (dict): The node to check.

    Returns:
        bool: True if the node is red, False otherwise.
    """
    return node is not None and node.get("color") == RED


def get_value(node: dict) -> object:
    """
    Gets the value from a node.

    Args:
        node (dict): The node.

    Returns:
        object: The value stored in the node, or None if the node is None.
    """
    return node.get("value") if node is not None else None


def set_value(node: dict, value: object) -> dict:
    """
    Sets the value of a node.

    Args:
        node (dict): The node.
        value (object): The new value.

    Returns:
        dict: The modified node.
    """
    if node is not None:
        node["value"] = value
    return node


def get_key(node: dict) -> object:
    """
    Gets the key from a node.

    Args:
        node (dict): The node.

    Returns:
        object: The key stored in the node, or None if the node is None.
    """
    return node.get("key") if node is not None else None


def set_key(node: dict, key: object) -> dict:
    """
    Sets the key of a node.

    Args:
        node (dict): The node.
        key (object): The new key.

    Returns:
        dict: The modified node.
    """
    if node is not None:
        node["key"] = key
    return node
