import time
import csv
import os
from math import radians, cos, sin, asin, sqrt
from DataStructures.List import single_linked as ll
from DataStructures.List import array_list as lt
from DataStructures.Map import map as mp
from DataStructures.Tree import bst
from DataStructures.Graph import adjlt as gr
from DataStructures.Graph import dfs

data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'
csv.field_size_limit(2147483647)


def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO: Llama a las funciónes de creación de las estructuras de datos
    catalog = lt.new_list()
    return catalog


# Funciones para la carga de datos

def parse_timestamp(ts):
    date, time = ts.split(" ")
    Y, M, D = date.split("-")
    h, m, s = time.split(":")
    s = float(s)
    return (
        int(Y) * 31536000 +
        int(M) * 2592000 +
        int(D) * 86400 +
        int(h) * 3600 +
        int(m) * 60 +
        s
    )

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    return R * c

def sort(lst, cmp):
    n = lt.size(lst)
    for i in range(1, n):
        key = lt.get_element(lst, i)
        j = i - 1
        while j >= 0 and cmp(key, lt.get_element(lst, j)):
            lt.update(lst, j + 1, lt.get_element(lst, j))
            j -= 1
        lt.update(lst, j + 1, key)
    return lst

def cmp_timestamp(a, b):
    return a["ts"] < b["ts"]

def load_data(catalog):
    file = data_dir + '1000_cranes_mongolia_30pct.csv'
    input_file = csv.DictReader(open(file, encoding="utf-8"))
    a = get_time()

    events = lt.new_list()
    for ev in input_file:
        ev["ts"] = parse_timestamp(ev["timestamp"])
        lt.add_last(events, ev)

    events = sort(events, cmp_timestamp)

    nodes = mp.new_map(capacity=10000)
    nodes_list = lt.new_list()
    event_to_node = mp.new_map(capacity=50000)

    last_node = None

    for ev in lt.iterator(events):
        lat = float(ev["location-lat"])
        lon = float(ev["location-long"])
        ts = ev["ts"]
        eid = ev["event-id"]
        gid = ev["tag-local-identifier"]
        water = float(ev["comments"]) / 1000.0

        if last_node is None:
            node = {
                "id": eid,
                "lat": lat,
                "lon": lon,
                "creation_time": ts,
                "events": [ev],
                "events_count": 1,
                "grullas": {gid},
                "prom_water": water
            }
            mp.put(nodes, eid, node)
            lt.add_last(nodes_list, node)
            mp.put(event_to_node, eid, eid)
            last_node = node
            continue

        d = haversine(lat, lon, last_node["lat"], last_node["lon"])
        dt = abs(ts - last_node["creation_time"]) / 3600

        if d < 3 and dt < 3:
            last_node["events"].append(ev)
            last_node["events_count"] += 1
            last_node["grullas"].add(gid)
            n = last_node["events_count"]
            last_node["prom_water"] = (last_node["prom_water"]*(n-1) + water) / n
            mp.put(event_to_node, eid, last_node["id"])
        else:
            node = {
                "id": eid,
                "lat": lat,
                "lon": lon,
                "creation_time": ts,
                "events": [ev],
                "events_count": 1,
                "grullas": {gid},
                "prom_water": water
            }
            mp.put(nodes, eid, node)
            lt.add_last(nodes_list, node)
            mp.put(event_to_node, eid, eid)
            last_node = node

    catalog["nodes"] = nodes
    catalog["nodes_list"] = nodes_list
    catalog["event_to_node"] = event_to_node

    total = lt.size(nodes_list)
    first_5 = lt.sub_list(nodes_list, 0, min(5, total))
    last_5 = lt.sub_list(nodes_list, max(0, total-5), total)
    
    b = get_time()
    time = delta_time(a, b)
    count = lt.size(events)

    return first_5, last_5, time, count, catalog

def build_graph_distance(catalog):
    """
    Construye el grafo del nicho biológico:
    - Cada nodo migratorio es un vértice.
    - Se conectan nodos consecutivos visitados por la misma grulla.
    - El peso del arco es la distancia Haversine.
    """

    nodes_list = catalog["nodes_list"]
    graph = gr.new_graph()

    # 1. Insertar todos los nodos migratorios como vértices
    for node in lt.iterator(nodes_list):
        gr.add_vertex(graph, node["id"])

    # 2. Crear índice: grulla_id → lista lt de nodos
    grullas = mp.new_map(capacity=5000)

    for node in range(lt.size(nodes_list)):
        for gid in lt.get_element(nodes_list, node)["grullas"]:
            lista = mp.get(grullas, gid)

            if lista is None:
                lista = lt.new_list()
                mp.put(grullas, gid, lista) 
                    
                print("lista")
                print(lista)  
                print(lt.get_element(nodes_list, node))   
            
            lt.add_last(lista, lt.get_element(nodes_list, node))

    # 3. Para cada grulla, ordenar sus nodos por creation_time (INTERNAL INSERTION SORT)
    for pair in mp.iterator(grullas):

        gid = pair["key"]
        lista = pair["value"]

        # insertion sort manual usando lt
        n = lt.size(lista)
        for i in range(n):
            key = lt.get_element(lista, i)
            j = i - 1

            while j >= 0 and lt.get_element(lista, j)["creation_time"] > key["creation_time"]:
                lt.update(lista, j + 1, lt.get_element(lista, j))
                j -= 1

            lt.update(lista, j + 1, key)

        # 4. Crear arcos entre nodos consecutivos ya ordenados
        for i in range(lt.size(lista) - 2):

            a = lt.get_element(lista, i)
            b = lt.get_element(lista, i+1)

            w = haversine(a["lat"], a["lon"], b["lat"], b["lon"])

            gr.add_edge(graph, a["id"], b["id"], w)

    # guardar en el catálogo
    catalog["graph_distance"] = graph



# Funciones de consulta sobre el catálogo

def req_1(catalog, lat_o, lon_o, lat_d, lon_d, crane_id):
    """
    Requerimiento 1 (Individual):
    Retorna toda la información solicitada por el enunciado.
    """
    #print(catalog)
    build_graph_distance(catalog)

    nodes_list = catalog["nodes_list"]
    nodes_map = catalog["nodes"]
    graph = catalog["graph_distance"]

    # -----------------------------------------------------------
    # 1. Encontrar nodo migratorio más cercano al punto de origen
    # -----------------------------------------------------------
    origin_node = None
    min_do = float("inf")

    for node in lt.iterator(nodes_list):
        d = haversine(lat_o, lon_o, node["lat"], node["lon"])
        if d < min_do:
            min_do = d
            origin_node = node

    # -----------------------------------------------------------
    # 2. Encontrar nodo migratorio más cercano al punto de destino
    # -----------------------------------------------------------
    destination_node = None
    min_dd = float("inf")

    for node in lt.iterator(nodes_list):
        d = haversine(lat_d, lon_d, node["lat"], node["lon"])
        if d < min_dd:
            min_dd = d
            destination_node = node

    if origin_node is None or destination_node is None:
        return {"msg": "Unknown origin or destination"}

    # -----------------------------------------------------------
    # 3. DFS para obtener el camino entre origen y destino
    # -----------------------------------------------------------
    path_ids = dfs.dfs(graph, origin_node["id"], destination_node["id"])

    if path_ids is None:
        return {"msg": "No hay un camino viable entre los puntos"}

    # -----------------------------------------------------------
    # 4. Encontrar el primer nodo donde aparece el individuo
    # -----------------------------------------------------------
    primer_nodo = "Unknown"
    for nid in path_ids:
        node = mp.get(nodes_map, nid)
        if crane_id in node["grullas"]:
            primer_nodo = nid
            break

    # -----------------------------------------------------------
    # 5. Construir versión expandida del camino (lista de nodos)
    # -----------------------------------------------------------
    ruta = []
    total_dist = 0

    for i in range(lt.size(path_ids)):
        node_id = lt.get_element(path_ids, i)
        node = mp.get(nodes_map, node_id)
        ruta.append(node)

        if i < lt.size(path_ids) - 1:
            next_id = lt.get_element(path_ids, i+1)
            next_node = mp.get(nodes_map, next_id)
            total_dist += haversine(node["lat"], node["lon"], next_node["lat"], next_node["lon"])

    # -----------------------------------------------------------
    # 6. Seleccionar primeros 5 y últimos 5 nodos del camino
    # -----------------------------------------------------------
    n = len(ruta)
    primeros_5 = ruta[:5]
    ultimos_5 = ruta[-5:] if n >= 5 else ruta

    # -----------------------------------------------------------
    # 7. Convertir a formato requerido por el enunciado
    # -----------------------------------------------------------
    def build_section(nodes):
        res = []
        for i in range(len(nodes)):
            n = nodes[i]
            entry = {
                "id": n["id"],
                "lat": n["lat"],
                "lon": n["lon"],
                "num_grullas": len(n["grullas"]),
                "primeras_grullas": list(n["grullas"])[:3],
                "ultimas_grullas": list(n["grullas"])[-3:]
            }

            # distancia al siguiente
            if i < len(nodes) - 1:
                nxt = nodes[i+1]
                entry["distancia_siguiente"] = haversine(n["lat"], n["lon"], nxt["lat"], nxt["lon"])
            else:
                entry["distancia_siguiente"] = "Unknown"

            res.append(entry)

        return res

    # -----------------------------------------------------------
    # 8. Retornar estructura EXACTA solicitada
    # -----------------------------------------------------------
    return {
        "primer_nodo_con_individuo": primer_nodo,
        "distancia_total": total_dist,
        "total_puntos": len(ruta),
        "primeros_5": build_section(primeros_5),
        "ultimos_5": build_section(ultimos_5)
    }





def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
