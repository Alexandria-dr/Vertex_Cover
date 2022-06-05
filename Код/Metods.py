from random import randint
from tkinter import ALL

def greedy(graph, canvas):
    canvas.itemconfig(ALL, fill="red")
    res = []
    list_edges = graph.make_list_vert_ed()
    dict_vert = graph.make_dict_vertexes()
    while list_edges or dict_vert != {}:
        max_value = 0
        max_key = 0
        for key in dict_vert:
            if max_value <= dict_vert[key]:
                max_value = dict_vert[key]
                max_key = key
        dict_vert.pop(max_key)
        res.append(max_key)
        canvas.itemconfig(max_key, fill='blue')

        for edge in graph.get_edges():
            edges = edge.get_list_vert()
            if max_key in edges :
                canvas.itemconfig(edge.get_id(), fill="blue")

            if max_key in edges:
                if max_key == edges[0] and edges[1] in dict_vert:
                    if dict_vert[edges[1]]-1 == 0:
                        dict_vert.pop(edges[1])
                    else:
                        dict_vert.update({edges[1]: dict_vert[edges[1]]-1})
                elif max_key == edges[1] and edges[0] in dict_vert:
                    if dict_vert[edges[0]]-1 == 0:
                        dict_vert.pop(edges[0])
                    else:
                        dict_vert.update({edges[0]: dict_vert[edges[0]]-1})

        copy_list = list_edges.copy()
        for edge in list_edges:
            if max_key in edge:
                copy_list.remove(edge)
        list_edges = copy_list.copy()
        copy_dict = dict_vert.copy()
        for vertex in dict_vert:
            if dict_vert[vertex] == 0:
                canvas.itemconfig(vertex, fill="blue")
                res.append(vertex)
                copy_dict.pop(vertex)
        dict_vert = copy_dict.copy()
    return f"результат роботи методу {res}\nкількість вершин:{len(res)}"


def approx(graph, canvas):
    canvas.itemconfig(ALL, fill="red")
    if graph.get_edges() == []:
        return 'для виконання цього методу потрібні ребра'
    for key in graph.make_dict_vertexes():
        if graph.make_dict_vertexes()[key] == 0:
            return "не всі вершини з'єднані ребрами"

    res = []
    list_edges = graph.make_list_vert_ed()
    while list_edges:
        rand = randint(0, len(list_edges)-1)
        del_item = list_edges.pop(rand)
        res.append(del_item)
        copy_list = list_edges.copy()
        for edge in graph.get_edges():
            if del_item[0] in edge.get_list_vert() and del_item[1] in edge.get_list_vert():
                canvas.itemconfig(edge.get_id(), fill="blue")
        for vertex in del_item:
            canvas.itemconfig(vertex, fill='blue')
            for edge in list_edges:
                if vertex in edge:
                    copy_list.remove(edge)
        list_edges = copy_list.copy()
    return f"результат роботи методу {res}\nкількість вершин:{len(res)*2}"