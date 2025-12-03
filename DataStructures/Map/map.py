# import python modules
import random as rd
from DataStructures.List import array_list as lt
from DataStructures.Map import entry as me
from DataStructures.Map import numbers as num
from App import logic as lg


def default_mp_entry_cmp(key, entry) -> int:
    if (key == entry["key"]):
        return 0
    elif (key > entry["key"]):
        return 1
    return -1

def is_available(table: dict, _slot: int) -> bool:
    entry = lt.get_element(table, _slot)
    if entry["key"] is None or entry["key"] == "__EMPTY__":
        return True
    return False

def find_slot(mp: dict, key, _idx: int) -> int:
    _table = mp["table"]
    _cmp = mp["cmp_function"]
    _capacity = mp["capacity"]

    _slot = _idx
    _available_slot = -1

    for _ in range(_capacity):
        entry = lt.get_element(_table, _slot)
        if is_available(_table, _slot):
            if _available_slot == -1:
                _available_slot = _slot
            if entry["key"] is None:
                break
        else:
            if _cmp(key, entry) == 0:
                return _slot
        _slot = (_slot + 1) % _capacity
    return -(_available_slot)


def rehash(mp: dict) -> None:
    old_table = mp["table"]
    new_capacity = num.next_prime(mp["capacity"] * 2)
    new_table = lt.new_list()
    for i in range(new_capacity):
        lt.add_last(new_table, me.new_map_entry(None, None))
    mp["table"] = new_table
    mp["capacity"] = new_capacity
    mp["size"] = 0

    for i in range(1, lt.size(old_table) + 1):
        entry = lt.get_element(old_table, i)
        put(mp, entry["key"], entry["value"])
            

def new_map(entries: int = 17, prime: int = 109345121, alpha: float = 0.5, key: str = None, rehashable: bool = True, capacity=100) -> dict:
    capacity = capacity
    scale = rd.randint(1, prime - 1)
    shift = rd.randint(0, prime - 1)
    new_table = dict(
    entries=entries,
    prime=prime,
    max_alpha=alpha,
    cur_alpha=0,
    capacity=capacity,
    scale=scale,
    shift=shift,
    table=None,
    rehashable=rehashable,
    size=0,
    type="LINEAR_PROBING",
    cmp_function=default_mp_entry_cmp,
    key=key
    )
        
    new_table["table"] = lt.new_list()
    i = 0
    while i < capacity:
        entry = me.new_map_entry(None, None)
        lt.add_last(new_table["table"], entry)
        i += 1
    return new_table


def put(mp: dict, key, value) -> None:
    entry = me.new_map_entry(key, value)
    _idx = num.hash_compress(key, mp["scale"], mp["shift"], mp["prime"], mp["capacity"])
    slot = find_slot(mp, key, _idx)
    # arlt.update(mp["table"], slot, entry)
    lt.update(mp["table"], abs(slot), entry)
    if slot < 0:
        mp["size"] += 1
        mp["cur_alpha"] = mp["size"] / mp["capacity"]

    if mp["cur_alpha"] >= mp["max_alpha"]:
        rehash(mp)


def get(mp: dict, key) -> dict:
    entry = None
    _idx = num.hash_compress(key, mp["scale"], mp["shift"], mp["prime"], mp["capacity"])
    _slot = find_slot(mp, key, _idx)
    if _slot > 0:
        entry = lt.get_element(mp["table"], _slot)
    return entry


def remove(mp: dict, key) -> dict:
    _idx = num.hash_compress(key, mp["scale"], mp["shift"], mp["prime"], mp["capacity"])
    _slot = find_slot(mp, key, _idx)
    if _slot > -1:
        dummy = me.new_map_entry("__EMPTY__", "__EMPTY__")
        lt.update(mp["table"], _slot, dummy)
        mp["size"] -= 1
    return mp

def size(mp: dict) -> int:
    return mp.get("size")

def contains(mp: dict, key) -> bool:
    _idx = num.hash_compress(key, mp["scale"], mp["shift"], mp["prime"], mp["capacity"])
    _slot = find_slot(mp, key, _idx)
    if _slot > 0:
        return True
    return False