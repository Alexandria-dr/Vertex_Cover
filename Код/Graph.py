class Graph:
    def __init__(self):
        self.__Vertexes = {}
        self.__Edges = []

    def add_vertex(self, obj):
        self.__Vertexes.update(obj._make_dict())

    def add_edge(self, obj, id1, id2):
        self.__Edges.append(obj)
        self.__Vertexes[id1][0]._add_edge_to_vertex(obj)
        self.__Vertexes[id2][0]._add_edge_to_vertex(obj)

    def get_vertexes(self):
        return self.__Vertexes

    def get_vertexes_id(self):
        res = []
        for vertex in self.__Vertexes:
            res.append(vertex)
        return res

    def get_edges(self):
        return self.__Edges

    def get_edges_id(self):
        res = []
        for edge in self.__Edges:
            res.append(edge.get_id())
        return res

    def del_vert(self, vertex):
        cdict = self.__Vertexes.copy()
        for i in self.__Vertexes:
            if vertex == i:
                cdict.pop(vertex)
        self.__Vertexes = cdict

    def del_edge(self, edge_id):
        for i in self.__Edges:
            if edge_id == i.get_id():
                self.__Edges.remove(i)

    def change_edge(self, id, vid, x, y):
        for edge in self.__Edges:
            if edge.get_id() == id:
                edge.change_vertex(vid, x, y)

    def check_edge(self, id1, id2):
        res = []
        for edge in self.__Edges:
            el = edge.get_list_vert()
            if [el[0], el[1]] not in res and [el[1], el[0]] not in res:
                res.append(el)
        if [id1, id2] in res or [id2, id1] in res:
            return True

    def make_list_vert_ed(self):
        res = []
        for edge in self.__Edges:
            el = edge.get_list_vert()
            if [el[0], el[1]] not in res and [el[1], el[0]] not in res:
                res.append(el)
        return res
    def make_dict_vertexes(self):
        res = {}
        for vertex in self.__Vertexes:
            key = vertex
            value = len(self.__Vertexes[vertex][0].get_edge())
            res.update({key: value})
        return res

    class Edge:
        def __init__(self, item_id, x2, y2, x1, y1, name1, name2):
            self.__first_x = x1
            self.__first_y = y1
            self.__second_x = x2
            self.__second_y = y2
            self.__first_name = name1
            self.__second_name = name2
            self.__id = item_id

        def __repr__(self):
            return f'{self.__id}[{self.__first_name},{self.__second_name}]'

        def change_vertex(self, shape_id, x, y):
            if shape_id == self.__first_name:
                self.__first_x = x
                self.__first_y = y
            elif shape_id == self.__second_name:
                self.__second_x = x
                self.__second_y = y

        def get_id(self):
            return self.__id

        def get_coord(self, id):
            if id == self.__first_name:
                return [self.__second_x, self.__second_y]
            elif id == self.__second_name:
                return [self.__first_x, self.__first_y]
            elif id == 0:
                return [self.__first_x, self.__first_y, self.__second_x, self.__second_y]

        def get_id_first(self):
            return self.__first_name

        def get_id_second(self):
            return self.__second_name

        def get_list_vert(self):
            return [self.__first_name, self.__second_name]

    class Vertex:
        def __init__(self, shape, x, y):
            self.__x = x
            self.__y = y
            self.__id = shape
            self.__list_edge = []
            self.__dict = {}
            self.__create_dict()


        def __str__(self):
            return f'x={self.__x}, y={self.__y}, name={self.__id};'

        def __repr__(self):
            return f'{self.__id}({self.__x},{self.__y})[{self.__list_edge}];'

        def __create_dict(self):
            self.__dict.update({self.__id: [self, self.__x, self.__y, self.__list_edge]})

        def _add_edge_to_vertex(self, edge):
            self.__list_edge.append(edge)

        def changeXY(self, x, y):
            self.__x = x
            self.__y = y

        def GetX(self):
            return self.__x

        def GetY(self):
            return self.__y

        def _make_dict(self):
            self.__create_dict()
            return self.__dict

        def get_edge(self):
            return self.__list_edge

        def get_id(self):
            return self.__id

        def remove_edge(self, edge):
            for i in self.__list_edge:
                if edge == i.get_id():
                    self.__list_edge.remove(i)
            return self.__list_edge
