"""
Module to handle a binary search tree (bst) data structure.

This code is based on the implementation proposed by the following authors/books:
    #. Algorithms, 4th Edition, Robert Sedgewick and Kevin Wayne.
    #. Data Structure and Algorithms in Python, M.T. Goodrich, R. Tamassia, M.H. Goldwasser.
"""

# import python modules
from typing import Any, Callable

# import modules for data structures ranges in tree
from DataStructures.List import single_linked as sllt

# import map entry
from DataStructures.Tree import tree_node as trn


def dflt_tree_node_cmp(key1: Any, key2: Any) -> int:
    if key1 == key2:
        return 0
    elif key1 < key2:
        return -1
    else:
        return 1


def new_tree(cmp_func: Callable[[Any, Any], int] = None) -> dict:
    _new_bst = dict(
        root=None,
        size=0,
        cmp_func=cmp_func,
        _type="BST"
    )
    if _new_bst["cmp_func"] is None:
        _new_bst["cmp_func"] = dflt_tree_node_cmp
    return _new_bst


def insert(tree: dict, k: Any, v: Any) -> dict:
    _root = tree["root"]
    _cmp = tree["cmp_func"]
    _root = _insert(_root, k, v, _cmp)
    tree["root"] = _root
    return tree


def _insert(node: dict, k: Any, v: Any, cmp_func: Callable) -> dict:
    if node is None:
        node = trn.new_bst_node(k, v, 1)
    else:
        _cmp = cmp_func(k, node["key"])
        if _cmp < 0:
            node["left"] = _insert(node["left"], k, v, cmp_func)
        elif _cmp > 0:
            node["right"] = _insert(node["right"], k, v, cmp_func)
        else:
            node["value"] = v
    _left_n = _size(node["left"])
    _right_n = _size(node["right"])
    node["size"] = _left_n + _right_n + 1
    return node


def get(tree: dict, k: Any) -> dict:
    _root = tree["root"]
    _cmp = tree["cmp_func"]
    return _get(_root, k, _cmp)


def _get(node: dict, k: Any, cmp_func: Callable) -> dict:
    _node = None
    if node is not None:
        _cmp = cmp_func(k, node["key"])
        if _cmp == 0:
            _node = node
        elif _cmp < 0:
            _node = _get(node["left"], k, cmp_func)
        elif _cmp > 0:
            _node = _get(node["right"], k, cmp_func)
    return _node


def remove(tree: dict, k: Any) -> dict:
    _root = tree["root"]
    _cmp = tree["cmp_func"]
    tree["root"] = _remove(_root, k, _cmp)
    return tree


def _remove(node: dict, k: Any, cmp_func: Callable) -> dict:
    if node is None:
        return None
    _cmp = cmp_func(k, node["key"])
    if _cmp == 0:
        if node["right"] is None:
            return node["left"]
        elif node["left"] is None:
            return node["right"]
        else:
            _node = node
            node = _minimum(node["right"])
            node["right"] = _delete_min(_node["right"])
            node["left"] = _node["left"]
    elif _cmp < 0:
        node["left"] = _remove(node["left"], k, cmp_func)
    elif _cmp > 0:
        node["right"] = _remove(node["right"], k, cmp_func)
    _left_n = _size(node["left"])
    _right_n = _size(node["right"])
    node["size"] = _left_n + _right_n + 1
    return node


def contains(tree: dict, k: Any) -> bool:
    _root = tree["root"]
    _cmp = tree["cmp_func"]
    return _contains(_root, k, _cmp, False)


def _contains(node: dict, k: Any, cmp_func: Callable, found: bool) -> bool:
    if node is None:
        return found
    _cmp = cmp_func(k, node["key"])
    if _cmp == 0:
        return True
    elif _cmp < 0:
        return _contains(node["left"], k, cmp_func, found)
    else:
        return _contains(node["right"], k, cmp_func, found)


def size(tree: dict) -> int:
    return _size(tree["root"])


def _size(node: dict) -> int:
    if node is None:
        return 0
    return node["size"]


def is_empty(tree: dict) -> bool:
    return tree["root"] is None


def minimum(tree: dict) -> dict:
    _min_node = _minimum(tree["root"])
    return _min_node["key"] if _min_node else None


def _minimum(node: dict) -> dict:
    if node is None:
        return None
    if node["left"] is None:
        return node
    return _minimum(node["left"])


def delete_min(tree: dict) -> dict:
    return _delete_min(tree["root"])


def _delete_min(node: dict) -> dict:
    if node is not None:
        if node["left"] is None:
            return node["right"]
        node["left"] = _delete_min(node["left"])
        node["size"] = _size(node["left"]) + _size(node["right"]) + 1
    return node


def maximum(tree: dict) -> dict:
    _max_node = _maximum(tree["root"])
    return _max_node["key"] if _max_node else None


def _maximum(node: dict) -> dict:
    if node is None:
        return None
    if node["right"] is None:
        return node
    return _maximum(node["right"])


def delete_max(tree: dict) -> dict:
    return _delete_max(tree["root"])


def _delete_max(node: dict) -> dict:
    if node is not None:
        if node["right"] is None:
            return node["left"]
        node["right"] = _delete_max(node["right"])
        node["size"] = _size(node["left"]) + _size(node["right"]) + 1
    return node


def floor(tree: dict, k: Any) -> dict:
    return _floor(tree["root"], k, tree["cmp_func"])


def _floor(node: dict, k: Any, cmp_func: Callable) -> dict:
    if node is None:
        return None
    _cmp = cmp_func(k, node["key"])
    if _cmp == 0:
        return node
    elif _cmp < 0:
        return _floor(node["left"], k, cmp_func)
    _node = _floor(node["right"], k, cmp_func)
    return _node if _node is not None else node


def ceiling(tree: dict, k: Any) -> dict:
    return _ceiling(tree["root"], k, tree["cmp_func"])


def _ceiling(node: dict, k: Any, cmp_func: Callable) -> dict:
    if node is None:
        return None
    _cmp = cmp_func(k, node["key"])
    if _cmp == 0:
        return node
    elif _cmp < 0:
        _node = _ceiling(node["left"], k, cmp_func)
        return _node if _node is not None else node
    return _ceiling(node["right"], k, cmp_func)


def select(tree: dict, k: int) -> dict:
    return _select(tree["root"], k)


def _select(node: dict, k: int) -> dict:
    if node is None:
        return None
    _left_n = _size(node["left"])
    if k < _left_n:
        return _select(node["left"], k)
    elif k > _left_n:
        return _select(node["right"], k - _left_n - 1)
    else:
        return node


def rank(tree: dict, k: Any) -> int:
    return _rank(tree["root"], k, tree["cmp_func"])


def _rank(node: dict, k: Any, cmp_func: Callable) -> int:
    if node is None:
        return 0
    _cmp = cmp_func(k, node["key"])
    if _cmp < 0:
        return _rank(node["left"], k, cmp_func)
    elif _cmp > 0:
        return 1 + _size(node["left"]) + _rank(node["right"], k, cmp_func)
    else:
        return _size(node["left"])


def height(tree: dict) -> int:
    return _height(tree["root"])


def _height(node: dict) -> int:
    if node is None:
        return -1
    left_h = _height(node["left"])
    right_h = _height(node["right"])
    return 1 + max(left_h, right_h)


def range(tree: dict, low: Any, high: Any) -> dict:
    _lt_range = sllt.new_list(cmp_function=tree["cmp_func"])
    return _range(tree["root"], low, high, tree["cmp_func"], _lt_range)


def _range(node: dict, low: Any, high: Any, cmp_func: Callable, lt_range: dict) -> dict:
    if node is not None:
        _cmp_low = cmp_func(low, node["key"])
        _cmp_high = cmp_func(high, node["key"])
        if _cmp_low < 0:
            _range(node["right"], low, high, cmp_func, lt_range)
        elif _cmp_high > 0:
            _range(node["left"], low, high, cmp_func, lt_range)
        else:
            sllt.add_last(lt_range, node["key"])
            _range(node["left"], low, high, cmp_func, lt_range)
            _range(node["right"], low, high, cmp_func, lt_range)
    return lt_range


def keys(tree: dict, low: Any, high: Any) -> dict:
    _keys_lt = sllt.new_list(cmp_function=tree["cmp_func"])
    return _keys(tree["root"], low, high, tree["cmp_func"], _keys_lt)


def _keys(node: dict, low: Any, high: Any, cmp_func: Callable, keys_lt: dict) -> dict:
    if node is not None:
        _cmp_low = cmp_func(low, node["key"])
        _cmp_high = cmp_func(high, node["key"])
        if _cmp_low < 0:
            _keys(node["right"], low, high, cmp_func, keys_lt)
        elif _cmp_high > 0:
            _keys(node["left"], low, high, cmp_func, keys_lt)
        else:
            _keys(node["left"], low, high, cmp_func, keys_lt)
            sllt.add_last(keys_lt, node["key"])
            _keys(node["right"], low, high, cmp_func, keys_lt)
    return keys_lt


def values(tree: dict, low: Any, high: Any) -> dict:
    values_lt = sllt.new_list(cmp_function=tree["cmp_func"])
    return _values(tree["root"], low, high, tree["cmp_func"], values_lt)


def _values(node: dict, low: Any, high: Any, cmp_func: Callable, values_lt: dict) -> dict:
    if node is None:
        return values_lt

    cmp_low = cmp_func(node["key"], low)
    cmp_high = cmp_func(node["key"], high)

    # 1. Recurse left if node key > low
    if cmp_low > 0:
        _values(node["left"], low, high, cmp_func, values_lt)

    # 2. If within range, add node value
    if cmp_low >= 0 and cmp_high <= 0:
        sllt.add_last(values_lt, node["value"])

    # 3. Recurse right if node key < high
    if cmp_high < 0:
        _values(node["right"], low, high, cmp_func, values_lt)

    return values_lt
