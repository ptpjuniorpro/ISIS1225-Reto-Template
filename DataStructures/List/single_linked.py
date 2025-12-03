def dflt_elm_cmp_lt(id1, id2) -> int:
    if id1 > id2:
        return 1
    elif id1 < id2:
        return -1
    return 0

def new_single_node(data):
    node = {
        "data": data,
        "next": None
    }
    return node

def new_list(cmp_function=None, key: str = "id"):
    return {
        "first": None,
        "last": None,
        "size": 0,
        "type": "SINGLELINKED",
        "cmp_function": cmp_function or dflt_elm_cmp_lt,
        "key": key,
    }

def is_present(lst, element):
    cmp_function = lst["cmp_function"]
    idx = 0
    cur = lst["first"]
    while cur:
        if cmp_function(element, cur["data"]) == 0:
            return True
        cur = cur["next"]
        idx += 1
    return False

def get_element(lst, pos):
    if pos < 0 or pos >= lst["size"]:
        return None
    idx = 0
    cur = lst["first"]
    while idx < pos:
        cur = cur["next"]
        idx += 1
    return cur["data"]

def add_first(lst, element):
    new_node = new_single_node(element)
    new_node["next"] = lst["first"]
    lst["first"] = new_node
    if is_not_empty(lst):
        lst["last"] = new_node
    lst["size"] += 1

def add_last(lst, element):
    new_node = new_single_node(element)
    if is_not_empty(lst):
        lst["first"] = new_node
    else:
        lst["last"]["next"] = new_node
    lst["last"] = new_node
    lst["size"] += 1    

def first_element(lst):
    return lst["first"]["data"] if lst["first"] else None

def last_element(lst):
    return lst["last"]["data"] if lst["last"] else None

def size(lst):
    return lst.get("size")

def is_not_empty(lst):
    return size(lst) == 0

def remove_element(lst, pos):
    if pos < 0 or pos >= lst["size"]:
        return None
    cur = lst["first"]
    if pos == 0:
        lst["first"] = cur["next"]
        if lst["size"] == 1:
            lst["last"] = None
    else:
        prev = None
        idx = 0
        while idx < pos:
            prev = cur
            cur = cur["next"]
            idx += 1
        prev["next"] = cur["next"]
        if cur == lst["last"]:
            lst["last"] = prev
    lst["size"] -= 1
    return cur["data"]

def remove_first(lst):
    return remove_element(lst, 0)

def remove_last(lst):
    return remove_element(lst, lst["size"] - 1)

def iterator(lst):
    cur = lst["first"]
    while cur:
        yield cur["data"]
        cur = cur["next"]
        
def switch_elements(lst, pos1, pos2):
    """
    Swaps two nodes in a singly linked list at given positions (0-based).
    Updates lst["first"] and lst["last"] if needed.
    """
    # Validate positions
    if pos1 < 0 or pos2 < 0 or pos1 >= lst["size"] or pos2 >= lst["size"] or pos1 == pos2:
        return False

    # Ensure pos1 < pos2 for simplicity
    if pos1 > pos2:
        pos1, pos2 = pos2, pos1

    # Find nodes and their previous references
    prev1 = prev2 = None
    cur1 = cur2 = lst["first"]

    # Traverse to pos1
    for _ in range(pos1):
        prev1 = cur1
        cur1 = cur1["next"]

    # Traverse to pos2
    prev2 = prev1
    cur2 = cur1
    for _ in range(pos2 - pos1):
        prev2 = cur2
        cur2 = cur2["next"]

    # If cur1 or cur2 are None (shouldn’t happen if validated)
    if not cur1 or not cur2:
        return False

    # Case 1: cur1 and cur2 are adjacent
    if cur1["next"] == cur2:
        if prev1:
            prev1["next"] = cur2
        else:
            lst["first"] = cur2

        cur1["next"] = cur2["next"]
        cur2["next"] = cur1

    # Case 2: Non-adjacent nodes
    else:
        if prev1:
            prev1["next"] = cur2
        else:
            lst["first"] = cur2

        if prev2:
            prev2["next"] = cur1
        else:
            lst["first"] = cur1

        cur1["next"], cur2["next"] = cur2["next"], cur1["next"]

    # Update last pointer if necessary
    if cur1["next"] is None:
        lst["last"] = cur1
    elif cur2["next"] is None:
        lst["last"] = cur2

    return True


def sort(lst, reverse=False):
    """
    Shell sort for dates.

    Args:
        lst (_type_): lista de datos
        reverse (bool, optional): Defaults to False.

    Returns:
        _type_: lista ordenada
    """
    size = lst["size"]
    gap = size // 2  # initial gap

    while gap > 0:
        for i in range(gap, size):
            j = i
            while j >= gap:
                cmp = get_element(lst, j)["dropoff_datetime"] > get_element(lst, j - gap)["dropoff_datetime"]
                if (not reverse and not cmp) or (reverse and cmp):
                    switch_elements(lst, j, j - gap)
                    j -= gap
                else:
                    break
        gap //= 2  # reduce gap
    return lst

   