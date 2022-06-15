class Graph:
    def __init__(self):
        """Конструктор графа"""
        self.__Vertexes = {}
        self.__Edges = []

    def add_vertex(self, obj):
        """Додати вершину в множину вершин графа"""
        self.__Vertexes.update(obj._make_dict())

    def add_edge(self, obj, id1, id2):
        """Додати ребро в множину ребер графа"""
        self.__Edges.append(obj)
        self.__Vertexes[id1][0]._add_edge_to_vertex(obj)
        self.__Vertexes[id2][0]._add_edge_to_vertex(obj)

    def get_vertexes(self):
        """Повертає множину вершин графа
        :return:словник з вершинами {id:obj, x, y, list of Edge}"""
        return self.__Vertexes

    def get_vertexes_id(self):
        """Повертає список ідентифікаторів вершин
        :return:список id вершин"""
        res = []
        for vertex in self.__Vertexes:
            res.append(vertex)
        return res

    def get_edges(self):
        """Повертає множину ребер
        :return:список об'єктів класу Edge"""
        return self.__Edges

    def get_edges_id(self):
        """Повертає список ідентифікаторів ребер
        :return:список id ребер"""
        res = []
        for edge in self.__Edges:
            res.append(edge.get_id())
        return res

    def del_vert(self, vertex):
        """Видаляє з множини вершин графа вершину
        :param vertex:id вершини
        :type vertex:int"""
        cdict = self.__Vertexes.copy()
        for i in self.__Vertexes:
            if vertex == i:
                cdict.pop(vertex)
        self.__Vertexes = cdict

    def del_edge(self, edge_id):
        """Видаляє з множини ребер графа ребро"""
        for i in self.__Edges:
            if edge_id == i.get_id():
                self.__Edges.remove(i)

    def change_edge(self, id, vid, x, y):
        """змінити координати кінця ребра"""
        for edge in self.__Edges:
            if edge.get_id() == id:
                edge.change_end(vid, x, y)

    def check_edge(self, id1, id2):
        """перевіряє чи наявне ребро в графі із заданими ребрами"""
        res = []
        for edge in self.__Edges:
            el = edge.get_list_vert()
            if [el[0], el[1]] not in res and [el[1], el[0]] not in res:
                res.append(el)
        if [id1, id2] in res or [id2, id1] in res:
            return True

    def make_list_vert_ed(self):
        """Створює список ребер, з елементами виду [id 1ї вершини, id 2ї вершини]"""
        res = []
        for edge in self.__Edges:
            el = edge.get_list_vert()
            if [el[0], el[1]] not in res and [el[1], el[0]] not in res:
                res.append(el)
        return res

    def make_dict_vert_number(self):
        """Створює словник вершин виду {id вершини: кількість ребер}"""
        res = {}
        for vertex in self.__Vertexes:
            key = vertex
            value = len(self.__Vertexes[vertex][0].get_edge())
            res.update({key: value})
        return res

    class _Edge:
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

        def change_end(self, shape_id, x, y):
            """змінити координати одного з кінців ребра"""
            if shape_id == self.__first_name:
                self.__first_x = x
                self.__first_y = y
            elif shape_id == self.__second_name:
                self.__second_x = x
                self.__second_y = y

        def get_id(self):
            """Повертає ідентифікатор ребра"""
            return self.__id

        def get_coord(self, id):
            """Повертає список з координатами"""
            if id == self.__first_name:
                return [self.__second_x, self.__second_y]
            elif id == self.__second_name:
                return [self.__first_x, self.__first_y]
            elif id == 0:
                return [self.__first_x, self.__first_y, self.__second_x, self.__second_y]

        def get_id_first(self):
            """Повертає ідентифікатор першої вершини ребра"""
            return self.__first_name

        def get_id_second(self):
            """Повертає ідентифікатор другої вершини ребра"""
            return self.__second_name

        def get_list_vert(self):
            """Повертає список ідентифікаторів вершин ребра"""
            return [self.__first_name, self.__second_name]

    class _Vertex:
        def __init__(self, shape, x, y):
            self.__x = x
            self.__y = y
            self.__id = shape
            self.__list_edge = []
            self.__dict = {}
            self.__update_dict()

        def __repr__(self):
            return f'{self.__id}({self.__x},{self.__y})[{self.__list_edge}];'

        def __update_dict(self):
            """Створення словника для вершини"""
            self.__dict.update({self.__id: [self, self.__x, self.__y, self.__list_edge]})

        def _add_edge_to_vertex(self, edge):
            """Додати до списку ребер вершини нове ребро"""
            self.__list_edge.append(edge)

        def changeXY(self, x, y):
            """змінити координати вершини"""
            self.__x = x
            self.__y = y

        def _make_dict(self):
            """створити та повернути словник вершини"""
            self.__update_dict()
            return self.__dict

        def get_edge(self):
            """повернути список ребер вершини"""
            return self.__list_edge

        def get_id(self):
            """Повернути ідентифікатор вершини"""
            return self.__id

        def remove_edge(self, edge):
            """Видалити ребро із вершини"""
            for i in self.__list_edge:
                if edge == i.get_id():
                    self.__list_edge.remove(i)
