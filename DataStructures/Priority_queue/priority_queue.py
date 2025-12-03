"""
Implementación de una Cola de Prioridad (Priority Queue)
basada en un Heap Binario (mínimo o máximo), utilizando las
funciones definidas en `pq_entry.py`.

Cada elemento del heap es una entrada creada con `new_pq_entry(priority, value)`.
"""

from DataStructures.Priority_queue import pq_entry as entry


def default_compare_lower_value(a, b):
    """True si 'a' tiene menor prioridad que 'b' (para MinPQ)."""
    try: 
        return a < b
    except TypeError:
        return str(a) < str(b)


def default_compare_higher_value(a, b):
    """True si 'a' tiene mayor prioridad que 'b' (para MaxPQ)."""
    try:
        return a > b
    except TypeError:
        return str(a) > str(b)


def new_heap(minimum=True):
    """
    Crea un nuevo heap vacío.
    Si minimum=True, se crea un MinPQ (menor valor = mayor prioridad).
    Si minimum=False, se crea un MaxPQ.
    """
    cmp = default_compare_lower_value if minimum else default_compare_higher_value
    heap = {
        'elements': [None],  # índice 1
        'size': 0,
        'cmp': cmp
    }
    return heap

def priority(heap, i):
    """Retorna la prioridad de la entrada en posición i."""
    return entry.get_priority(heap['elements'][i])


def value(heap, i):
    """Retorna el valor de la entrada en posición i."""
    return entry.get_value(heap['elements'][i])


def exchange(heap, i, j):
    """Intercambia las posiciones i y j del heap."""
    heap['elements'][i], heap['elements'][j] = heap['elements'][j], heap['elements'][i]


def size(heap):
    """Retorna el número de elementos en el heap."""
    return heap['size']


def is_empty(heap):
    """True si el heap está vacío."""
    return heap['size'] == 0


def swim(heap, i):
    """
    Sube (swim) el elemento en la posición i hasta su lugar correcto
    según la función de comparación del heap.
    """
    while i > 1:
        parent = i // 2
        if heap['cmp'](priority(heap, i), priority(heap, parent)):
            exchange(heap, i, parent)
            i = parent
        else:
            break


def sink(heap, i):
    """
    Baja (sink) el elemento en la posición i hasta su lugar correcto
    según la función de comparación del heap.
    """
    n = heap['size']
    while 2 * i <= n:
        j = 2 * i  # hijo izquierdo
        if j < n and heap['cmp'](priority(heap, j + 1), priority(heap, j)):
            j += 1  # elegir el hijo con mayor prioridad
        if heap['cmp'](priority(heap, j), priority(heap, i)):
            exchange(heap, i, j)
            i = j
        else:
            break


def insert(heap, priority_value, value):
    """
    Inserta una nueva entrada (priority, value) en el heap.
    """
    new_entry = entry.new_pq_entry(priority_value, value)
    heap['elements'].append(new_entry)
    heap['size'] += 1
    swim(heap, heap['size'])
    return heap


def remove(heap):
    """
    Elimina y retorna el valor (value) de la entrada con mayor prioridad.
    Retorna None si el heap está vacío.
    """
    if is_empty(heap):
        return None
    root = heap['elements'][1]
    last = heap['elements'].pop()
    heap['size'] -= 1
    if heap['size'] >= 1:
        heap['elements'][1] = last
        sink(heap, 1)
    return entry.get_value(root)


def get_first_priority(heap):
    """
    Retorna el valor del primer elemento sin eliminarlo.
    Retorna None si el heap está vacío.
    """
    if is_empty(heap):
        return None
    return entry.get_value(heap['elements'][1])

def is_present_value(heap, value_to_find):
    """Verifica si existe un 'value' dentro del heap."""
    for i in range(1, heap['size'] + 1):
        if entry.get_value(heap['elements'][i]) == value_to_find:
            return True
    return False


def contains(heap, value_to_find):
    """Alias de is_present_value (usado por la guía del curso)."""
    return is_present_value(heap, value_to_find)


def improve_priority(heap, value_to_find, new_priority):
    """
    Si un valor ya existe en el heap y la nueva prioridad mejora la actual,
    actualiza la prioridad y reordena el heap.
    Retorna True si se actualizó, False si no se encontró.
    """
    for i in range(1, heap['size'] + 1):
        if entry.get_value(heap['elements'][i]) == value_to_find:
            current = entry.get_priority(heap['elements'][i])
            entry.set_priority(heap['elements'][i], new_priority)
            if heap['cmp'](new_priority, current):
                swim(heap, i)
            else:
                sink(heap, i)
            return True
    return False
