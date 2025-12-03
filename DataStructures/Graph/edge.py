def new_edge(va, vb, weight=0):
    return {"vtx_a": va, "vtx_b": vb, "weight": weight}

def weight(edge):
    return edge["weight"]

def either(edge):
    return edge["vtx_a"]

def other(edge, veither):
    return edge["vtx_b"] if veither == edge["vtx_a"] else edge["vtx_a"]

def set_weight(edge, weight):
    edge["weight"] = weight

def cmp_edges(edge1, edge2):
    e1v, e2v = either(edge1), either(edge2)
    if e1v == e2v:
        a = other(edge1, e1v)
        b = other(edge2, e2v)
        if a == b:
            return 0
        return 1 if a > b else -1
    return 1 if e1v > e2v else -1
