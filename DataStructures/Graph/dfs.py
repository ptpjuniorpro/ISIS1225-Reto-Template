from typing import Any
from DataStructures.Graph import adjlt as g
from DataStructures.List import single_linked as lt
from DataStructures.Map import map as mp
from DataStructures.Graph import edge as edg


def dfs(grf: dict, src: Any) -> dict:
    search = dict(
        algorithm="DFS",
        _type=grf["_type"],
        source=src,
        visited=mp.new_mp(g.size(grf), grf["cmp_func"])
    )

    # El nodo inicial se marca como visitado
    mp.put(search["visited"], src, dict(marked=True, edgeto=None))

    _dfs(grf, src, search)
    return search


def _dfs(grf: dict, src: Any, search: dict) -> dict:
    adj_st = g.adjacent_vertices(grf, src)

    for w in lt.iterator(adj_st):
        visited_w = mp.get(search["visited"], w)

        # Si no está visitado, marcar y continuar DFS
        if visited_w is None:
            mp.put(search["visited"], w, dict(marked=True, edgeto=src))
            _dfs(grf, w, search)

    return search
