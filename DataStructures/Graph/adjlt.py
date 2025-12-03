from typing import Any, Callable

from DataStructures.List import single_linked as lt
from DataStructures.Map import map as mp
from DataStructures.Graph import edge as edg


def dflt_graph_edge_cmp(key1: Any, key2: Any) -> int:
    if key1 == key2:
        return 0
    elif key1 < key2:
        return -1
    else:
        return 1


def new_graph(cmp_func: Callable = dflt_graph_edge_cmp,
              directed: bool = False,
              size: int = 10) -> dict:

    _new_al = dict(
        vertices=mp.new_map(capacity=5000),
        edges=lt.new_list(),
        size=0,
        order=0,
        directed=directed,
        cmp_func=cmp_func,
        _type="adj_lt",
    )

    if not directed:
        _new_al["deg"] = mp.new_map(capacity=5000)
    else:
        _new_al["indeg"] = mp.new_map(capacity=5000)
        _new_al["outdeg"] = mp.new_mp(capacity=5000)

    return _new_al


def add_vertex(grf: dict, vtx: Any) -> None:
    if not contain_vertex(grf, vtx):
        _edges = lt.new_list()
        mp.put(grf["vertices"], vtx, _edges)

    grf["size"] += 1

    if not grf["directed"]:
        mp.put(grf["deg"], vtx, 0)
    else:
        mp.put(grf["indeg"], vtx, 0)
        mp.put(grf["outdeg"], vtx, 0)


def remove_vertex(grf: dict, vtx: Any) -> None:
    if contain_vertex(grf, vtx):
        _edges = mp.get(grf["vertices"], vtx)
        for e in lt.iterator(_edges):
            remove_edge(grf, edg.either(e), edg.other(e, vtx))

        mp.remove(grf["vertices"], vtx)
        grf["size"] -= 1

        if not grf["directed"]:
            mp.remove(grf["deg"], vtx)
        else:
            mp.remove(grf["indeg"], vtx)
            mp.remove(grf["outdeg"], vtx)


def get_vertex(grf: dict, vtx: Any) -> dict:
    return mp.get(grf["vertices"], vtx)


def add_edge(grf: dict, vtx_a: Any, vtx_b: Any, weight: int = 0) -> None:
    _vtx_a = mp.get(grf["vertices"], vtx_a)
    _vtx_b = mp.get(grf["vertices"], vtx_b)

    if _vtx_a is None or _vtx_b is None:
        raise Exception("One of the vertices does not exist")

    _edge = get_edge(grf, vtx_a, vtx_b)

    if _edge is None:
        _edge = edg.new_edge(vtx_a, vtx_b, weight)
        lt.add_last(_vtx_a, _edge)
        lt.add_last(_vtx_b, _edge)

        grf["order"] += 1

        if not grf["directed"]:
            mp.put(grf["deg"], vtx_a, mp.get(grf["deg"], vtx_a) + 1)
            mp.put(grf["deg"], vtx_b, mp.get(grf["deg"], vtx_b) + 1)
        else:
            mp.put(grf["indeg"], vtx_b, mp.get(grf["indeg"], vtx_b) + 1)
            mp.put(grf["outdeg"], vtx_a, mp.get(grf["outdeg"], vtx_a) + 1)


def remove_edge(grf: dict, vtx_a: Any, vtx_b: Any) -> None:
    # debes implementar la eliminación en lt y actualizar deg/indeg/outdeg
    pass


def get_edge(grf: dict, vtx_a: Any, vtx_b: Any) -> dict:
    # debes iterar sobre la adjacency list del vtx_a
    # y buscar una arista donde other(e, vtx_a) == vtx_b
    pass


def size(grf: dict) -> int:
    return grf["size"]


def order(grf: dict) -> int:
    return grf["order"]


def is_directed(grf: dict) -> bool:
    return grf["directed"]


def is_empty(grf: dict) -> bool:
    return grf["size"] == 0


def is_weighted(grf: dict) -> bool:
    # depende de tu estructura de edges
    pass


def edges(grf: dict) -> list:
    return grf["edges"]


def vertices(grf: dict) -> list:
    return grf["vertices"]


def degree(grf: dict, vtx: Any) -> int:
    if not grf["directed"]:
        return mp.get(grf["deg"], vtx)
    else:
        return mp.get(grf["outdeg"], vtx)


def contain_edge(grf: dict, vtx_a: Any, vtx_b: Any) -> bool:
    return get_edge(grf, vtx_a, vtx_b) is not None


def contain_vertex(grf: dict, vtx: Any) -> bool:
    return mp.contains(grf["vertices"], vtx)


def adjacent_vertices(grf: dict, vtx: Any) -> list:
    # debes iterar sobre edges de vtx y retornar lista de vtx vecinos
    pass


def adjacent_edges(grf: dict, vtx: Any) -> list:
    return mp.get(grf["vertices"], vtx)
