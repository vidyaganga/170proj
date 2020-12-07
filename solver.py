import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness, convert_dictionary
import sys
import pandas as pd
import numpy as np
import random
from math import factorial


def comb(n, r):
    return factorial(n) // factorial(r) // factorial(n-r)



def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """

    # TODO: your code here!
    pass

def use_greedy_happystress(G,s):
    best = {}
    i = 1
    while i <= len(G.nodes):
        G_cop = G.copy()
        possible = greedy_happystress(G, G_cop, s, i)
        if is_valid_solution(possible, G, s, i) and not list(G_cop.nodes):
            if not best or calculate_happiness(best, G) < calculate_happiness(possible, G):
                best = possible
        i+=1
    return best


def greedy_happystress(G, G_cop, s, rooms):
    dic = {}
    current_room = 0
    while G_cop.nodes and current_room < rooms:
        dic[current_room] = room_maker(G, G_cop, s/rooms)
        current_room += 1
    return convert_dictionary(dic)

def room_maker(G, G_copy,thresh):
    room = []
    room.append(list(G_copy.nodes)[random.randint(0, len(G_copy.nodes) - 1)])
    G_copy.remove_node(room[0])
    room_stress = 0
    while room_stress <= thresh and list(G_copy.nodes):
        next = max(list(G_copy.nodes), key=lambda x: happiness_over_stress(G,room, x))
        room_stress1 = stress(G, room, next)
        if room_stress + room_stress1 <= thresh:
            room.append(next)
            G_copy.remove_node(next)
            room_stress += room_stress1
        else:
            return room
    return room

def happiness_over_stress(G, room, candidate):
    happiness = 0
    stress = 0
    for kid in room:
        happiness += G[kid][candidate]['happiness']
        stress += G[kid][candidate]['stress']
    if stress == 0:
        return happiness/0.01
    return happiness/stress

def happiness(G, room, candidate):
    happiness = 0
    for kid in room:
        happiness += G[kid][candidate]['happiness']
    return happiness

def stress(G, room, candidate):
    stress = 0
    for kid in room:
        stress += G[kid][candidate]['stress']
    return stress
    
def kcluster_beef(G, s):
    best = {}
    best_happiness= 0 
    for i in range(1, len(G.nodes)):
        local_best = {}
        j = 0 
        valid = 0 
        total_combos = []
        while j <= 400:
            # if (not valid) and j>=70:
            #     j=200
            init_centroids = random.sample(range(0, len(list(G.nodes))), i)
            if (len(total_combos) < comb(len(G.nodes), i)):
                while (init_centroids in total_combos):
                    init_centroids = random.sample(range(0, len(list(G.nodes))), i)
            total_combos.append(init_centroids)
            classes = making_classes_beef(init_centroids, G, s/i)
            for c in classes:
                d = making_dic(c)
                dic = convert_dictionary(d)
                if is_valid_solution(dic, G, s, i):
                    valid = 1
                    local_best[calculate_happiness(dic, G)] = dic 
                if len(local_best)!=0:
                    local = max(local_best.keys())
                    if len(best)!=0:
                        if best_happiness < local:
                            best_happiness = local 
                            best = local_best[local]
                    else:
                        best_happiness = local
                        best = local_best[local]
            j+=1
    h = calculate_happiness(best, G)
    return best

def making_classes_beef(centroids, G, S_per_room):
    clasS= [[c] for c in centroids] 
    clasH= [[c] for c in centroids] 
    clasHS= [[c] for c in centroids] 
    clasBeef= [[0, [c]] for c in centroids] 
    x = random.sample(range(0, len(list(G.nodes))), len(G.nodes))
    for node in x:
        if any([c[0] > S_per_room for c in clasBeef]):
            return []
        if not any([(node in already[1]) for already in clasBeef]):
            added_stress = []
            added_hs = []
            added_happy = []
            for existing in range(len(centroids)):
                total_hs = 0 
                total_stress = 0
                total_happy = 0
                for stud in clasBeef[existing][1]:
                    if not G[stud][node]['stress']:
                        total_hs += G[stud][node]['happiness'] / 0.001
                    else:
                        total_hs += G[stud][node]['happiness'] / G[stud][node]['stress']
                    total_stress +=  G[stud][node]['stress']
                    total_happy +=  G[stud][node]['happiness']
                added_stress.append(total_stress)
                added_hs.append(total_hs)
                added_happy.append(total_happy)
            # clas[np.argmax(added_hs)].append(node)    
            min_stress = np.argmin(added_stress)
            max_hs = np.argmax(added_hs)
            max_happy = np.argmax(added_happy)
            clasS[np.argmax(min_stress)].append(node)  
            clasH[np.argmax(max_happy)].append(node)  
            clasHS[np.argmax(max_hs)].append(node)  

            if (min_stress == max_hs) or ((added_stress[max_hs] + clasBeef[max_hs][0]) > S_per_room):
                clasBeef[min_stress][1].append(node) 
                clasBeef[min_stress][0] += added_stress[min_stress]
            else: 
                if max_happy == min_stress:
                    clasBeef[min_stress][1].append(node) 
                    clasBeef[min_stress][0] += added_stress[min_stress]
                elif max_happy == max_hs:
                    clasBeef[max_hs][1].append(node) 
                    clasBeef[max_hs][0] += added_stress[max_hs] 
                else:
                    rando = [min_stress, max_hs]
                    x = random.randint(0, 1)
                    clasBeef[rando[x]][1].append(node)  
                    clasBeef[rando[x]][0] += added_stress[rando[x]] 
    rv = [c[1] for c in clasBeef]
    return [rv, clasHS, clasS, clasH]

def making_dic(biglist):
    dic = {}
    for b in range(len(biglist)):
        dic[b]= biglist[b]
    return dic 

def take_both(num):
    G, s = read_input_file('inputs/medium-' + str(num) + '.in')
    sree = kcluster_beef(G, s)
    m = max([use_greedy_happystress(G, s) for i in range(100)], key=lambda x: calculate_happiness(x, G))
    if calculate_happiness(sree, G) > calculate_happiness(m, G):
        print(calculate_happiness(sree, G))
        write_output_file(sree, 'outputs/medium-' + str(num) + '.out')
    else:
        print(calculate_happiness(m, G))
        write_output_file(m, 'outputs/medium-' + str(num) + '.out')

for i in [90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 106, 107, 108, 112, 119, 124, 126, 130, 133, 134, 135, 139, 142, 143, 146, 147, 148, 149, 150, 152, 155, 158, 159, 163, 164, 167, 168, 170, 173, 179, 182, 183, 185, 186, 188, 189, 190, 191, 195, 197, 198, 200, 205, 210, 212, 214, 215, 216, 223, 224, 230, 232, 234, 236, 238, 239, 240]:
    take_both(i)


# def take_both(num):
#     G, s = read_input_file('inputs/large-' + str(num) + '.in')
#     m = max([use_greedy_happystress(G, s) for i in range(10)], key=lambda x: calculate_happiness(x, G))
#     print(calculate_happiness(m, G))
#     write_output_file(m, 'outputs/large-' + str(num) + '.out')

# for i in range(236, 243):
#     take_both(i)


# for i in range(1, 243):
#     G, s = read_input_file('./inputs/small-' + str(i) + '.in')
#     m = use_greedy_happystress(G,s)
#     x = calculate_happiness(m, G)
#     x = max([(calculate_happiness(use_greedy_happystress(G, s), G)) for i in range(50)])
#     print("Total Happiness: {}".format(x))

#  x = max([(calculate_happiness(use_greedy_happystress(G, s), G)) for i in range(50)])

# def greedy(G, s):
#     sorted_happiness = [G[x][y] for ] 
#     for i in range(len(G.nodes)):
#         stress = s/i

# def clearGraph(G, s):
#     edges = list(G.edges)
#     i = 0
#     while i < len(edges):
#         element = edges[i]
#         if (element['stress'] > s):
#             del element

# def kcluster_stress(G, s):
#     best = {}
#     best_happiness= 0 
#     for i in range(1, len(G.nodes)):
#         local_best = {}
#         j = 0 
#         valid = 0 
#         while j <= 400:
#             if (not valid) and j>=70:
#                 j=400
#             init_centroids = random.sample(range(0, len(list(G.nodes))), i)
#             classes = making_classes_stress(init_centroids, G)
#             d = making_dic(classes)
#             dic = convert_dictionary(d)
#             if is_valid_solution(dic, G, s, i):
#                 valid = 1
#                 local_best[calculate_happiness(dic, G)] = dic 
#             if len(local_best)!=0:
#                 valid = 1 
#                 local = max(local_best.keys())
#                 if len(best)!=0:
#                     if best_happiness < local:
#                         best_happiness = local 
#                         best = local_best[local]
#                 else:
#                    best_happiness = local
#                    best = local_best[local]
#             j+=1
#     h = calculate_happiness(best, G)
#     print("Stress: Total Happiness: {}".format(calculate_happiness(best, G)))
#     return best
        

# def making_classes_stress(centroids, G):
#     clas= [[c] for c in centroids] 
#     x = random.sample(range(0, len(list(G.nodes))), len(G.nodes))
#     for node in x:
#         if not any([(node in already) for already in clas]):
#             added_stress = []
#             for existing in range(len(centroids)):
#                 total = 0 
#                 for stud in clas[existing]:
#                     total+= G[stud][node]['stress'] 
#                 added_stress.append(total)
#             clas[np.argmin(added_stress)].append(node)    
#     return clas
    

# def kcluster_happy(G, s):
#     best = {}
#     best_happiness= 0 
#     for i in range(1, len(G.nodes)):
#         local_best = {}
#         valid = 0
#         j = 0 
#         while j <= 400:
#             if (not valid) and j>=70:
#                 j==400
#             init_centroids = random.sample(range(0, len(list(G.nodes))), i)
#             # centroids = [G.nodes[j] for j in init_centroids]
#             classes = making_classes_stress(init_centroids, G)
#             d = making_dic(classes)
#             dic = convert_dictionary(d)
#             if is_valid_solution(dic, G, s, i):
#                 valid = 1
#                 local_best[calculate_happiness(dic, G)] = dic 
#             if len(local_best)!=0:
#                 local = max(local_best.keys())
#                 if len(best)!=0:
#                     if best_happiness < local:
#                         best_happiness = local 
#                         best = local_best[local]
#                 else:
#                    best_happiness = local
#                    best = local_best[local]
#             j+=1
#     h = calculate_happiness(best, G)
#     print("Happy: Total Happiness: {}".format(calculate_happiness(best, G)))
#     return best
        

# def making_classes_happy(centroids, G):
#     clas= [[c] for c in centroids] 
#     x = random.sample(range(0, len(list(G.nodes))), len(G.nodes))
#     for node in x:
#         if not any([(node in already) for already in clas]):
#             added_stress = []
#             for existing in range(len(centroids)):
#                 total = 0 
#                 for stud in clas[existing]:
#                     total+= G[stud][node]['happiness'] 
#                 added_stress.append(total)
#             clas[np.argmax(added_stress)].append(node)    
#     return clas


# def kcluster_hs(G, s):
#     best = {}
#     best_happiness= 0 
#     for i in range(1, len(G.nodes)):
#         local_best = {}
#         j = 0 
#         valid = 0 
#         while j <= 400:
#             if (not valid) and j>=70:
#                 j==400
#             init_centroids = random.sample(range(0, len(list(G.nodes))), i)
#             classes = making_classes_stress(init_centroids, G)
#             d = making_dic(classes)
#             dic = convert_dictionary(d)
#             if is_valid_solution(dic, G, s, i):
#                 valid = 1
#                 local_best[calculate_happiness(dic, G)] = dic 
#             if len(local_best)!=0:
#                 local = max(local_best.keys())
#                 if len(best)!=0:
#                     if best_happiness < local:
#                         best_happiness = local 
#                         best = local_best[local]
#                 else:
#                    best_happiness = local
#                    best = local_best[local]
#             j+=1
#     h = calculate_happiness(best, G)
#     print("Stress/Happy: Total Happiness: {}".format(calculate_happiness(best, G)))
#     return best
        

# def making_classes_hs(centroids, G):
#     clas= [[c] for c in centroids] 
#     x = random.sample(range(0, len(list(G.nodes))), len(G.nodes))
#     for node in x:
#         if not any([(node in already) for already in clas]):
#             added_stress = []
#             for existing in range(len(centroids)):
#                 total = 0 
#                 for stud in clas[existing]:
#                     total+= (G[stud][node]['happiness'] / G[stud][node]['stress'])
#                 added_stress.append(total)
#             clas[np.argmax(added_stress)].append(node)    
#     return clas






# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G, s = read_input_file(path)
#     D, k = solve(G, s)
#     assert is_valid_solution(D, G, s, k)
#     print("Total Happiness: {}".format(calculate_happiness(D, G)))
#     write_output_file(D, 'out/test.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('file_path/inputs/*')
#     for input_path in inputs:
#         output_path = 'file_path/outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G, s = read_input_file(input_path, 100)
#         D, k = solve(G, s)
#         assert is_valid_solution(D, G, s, k)
#         cost_t = calculate_happiness(T)
#         write_output_file(D, output_path)
