def dflt_elm_cmp_lt(id1, id2) -> int:
    if id1 > id2:
        return 1
    elif id1 < id2:
        return -1
    return 0

def new_list(key: str = "id"):
    new_lt = dict(
        elements=[],
        size = 0,
        type="ARRAYLIST",
        cmp_function = dflt_elm_cmp_lt,
    )
    return new_lt

def size(lst):
    return lst.get("size")

def is_empty(lst):
    return lst["size"] == 0

def get_element(lst, index):
    if 0 <= index < lst["size"]:
        return lst["elements"][index]
    return None

def is_present(lst, element, cmp_function=None):
    cmp_function = cmp_function or lst["cmp_function"]
    for i, info in enumerate(lst["elements"]):
        if cmp_function(element, info) == 0:
            return i
    return -1

def first_element(lst):
    if lst["size"] > 0:
        return lst["elements"][0]
    return None

def last_element(lst):
    if lst["size"] > 0:
        return lst["elements"][-1]
    return None

def add_first(lst, element):
    lst["elements"].insert(0, element)
    lst["size"] += 1

def add_last(lst, element):
    lst['elements'].append(element)
    lst["size"] += 1

def insert_element(lst, index, element):
    if 0 <= index <= lst["size"]:
        lst["elements"].insert(index, element)
        lst["size"] += 1
        return True
    return False

def change_info(lst, old_element, new_element):
    index = is_present(lst, old_element)
    if index != -1:
        lst["elements"][index] = new_element
        return True
    return False

def iterator(lst):
    for pos in range(lst["size"]):
        yield lst["elements"][pos]
        
def exchange(lst, pos1, pos2):
    if 0 <= pos1 < lst["size"] and 0 <= pos2 < lst["size"]:
        lst["elements"][pos1], lst["elements"][pos2] = lst["elements"][pos2], lst["elements"][pos1]
        return True
    return False        
        
def sort(lst):
    """
    Shell sort using a custom sorting criterion.

    Args:
        lst (_type_): lista de datos con tamaño en lst["size"]
        sort_crit (function): función que compara dos elementos. 
            Debe retornar True si se debe intercambiar.

    Returns:
        _type_: lista ordenada
    """
    size = lst["size"]
    gap = size // 2  # initial gap

    while gap > 0:
        for i in range(gap, size):
            j = i
            while j >= gap and get_element(lst, j)["dropoff_datetime"] < get_element(lst, j - gap)["dropoff_datetime"]:
                exchange(lst, j, j - gap)
                j -= gap
        gap //= 2  # reduce the gap after each pass
    return lst
  

def update(lst: dict, pos: int, element) -> None:
    lst["elements"][pos] = element  
    
def sort(lst):
    """
    Shell sort for dates (descending by dropoff_datetime).

    Args:
        lst (_type_): lista de datos con tamaño en lst["size"]

    Returns:
        _type_: lista ordenada
    """
    size = lst["size"]
    gap = size // 2  # initial gap

    while gap > 0:
        for i in range(gap, size):
            j = i
            while j >= gap and get_element(lst, j)["dropoff_datetime"] > get_element(lst, j - gap)["dropoff_datetime"]:
                exchange(lst, j, j - gap)
                j -= gap
        gap //= 2

    return lst

def sub_list(lst, start, end):
    """
    Crea una sublista desde 'start' hasta 'end' (inclusive).

    Args:
        lst (_type_): lista original
        start (int): índice inicial (1-based)
        end (int): índice final (1-based)

    Returns:
        _type_: sublista
    """
    sub_lst = new_list(lst["cmp_function"])
    for i in range(start - 1, end):
        add_last(sub_lst, get_element(lst, i))
    return sub_lst

     