import tkinter as tk
from tkinter import Tk
from functools import partial
from Graph import Graph
from tkinter import messagebox
from Metods import *
import sys



class Window:
    def __init__(self, width, height, title='My window', resizable=(False, False), icon=None):
        self.__root = Tk()
        self.__root.title(title)
        self.__root.geometry(f'{width}x{height}+200+200')
        self.__root.resizable(resizable[0], resizable[1])
        if icon:
            self.__root.iconbitmap(icon)
        self.__root.configure(background='light blue')
        self.__actions = ('вершина', 'ребро', 'переміщення', 'видалення', 'approx', 'greedy')
        self.__start = None  # координати
        self.__action = None
        self.__current = None
        self.__canvX = 800
        self.__canvY = 450
        self.__canvas = tk.Canvas(self.__root, bg="white", width=self.__canvX, height=self.__canvY)
        self.__canvas.grid(row=0, columnspan=4)
        self.__dnd_item = ()

        for i in range(4):
            __btn = tk.Button(self.__root, text=self.__actions[i], font=('Consolas', 16))
            __btn.config(command=partial(self.__set_selection, __btn, self.__actions[i]))
            __btn.grid(column=i, row=1, sticky=tk.W + tk.E + tk.S + tk.N)
        self.__frame = tk.Frame(background='light blue')
        for i in range(4, 6):
            __btn = tk.Button(self.__frame, text=self.__actions[i], font=('Consolas', 16))
            __btn.config(command=partial(self.__set_selection, __btn, self.__actions[i]))
            __btn.grid(column=i - 4, row=0, sticky=tk.W + tk.E + tk.S + tk.N, pady=20, padx=23)
        __btn = tk.Button(self.__frame, text='вирішити', font=('Consolas', 16), command=lambda:
            self.__do_action(0) if (self.__action == 'approx' or self.__action == 'greedy') else None)
        __btn.grid(columnspan=2, column=0, row=1, padx=35, pady=20)

        self.__info_text = tk.StringVar(value='')
        self.__info_label = tk.Label(self.__frame, textvariable=self.__info_text, bg='white', height=15, relief=tk.RAISED,
                                     wraplength=200, justify=tk.LEFT)
        self.__info_label.grid(columnspan=2, column=0, row=2, padx=25, pady=20, sticky=tk.W + tk.E)

        self.__frame.grid(columnspan=2, column=5, rowspan=3, row=0, sticky=tk.W + tk.S + tk.N)
        self.__canvas.bind("<Motion>", self.__mouse_motion)
        self.__canvas.bind("<Button-1>", self.__do_action)
        self.__canvas.tag_bind("draggable", "<ButtonPress-1>", self.__button_press)
        self.__graph = Graph()

    def __mouse_motion(self, event):  # зафарбовує в жовтий ближню фігуру до вказівника
        if self.__action != "greedy" and self.__action != 'approx':
            self.__canvas.itemconfig(self.__current, fill="red")
            self.__current = self.__canvas.find_closest(event.x, event.y)
            self.__canvas.itemconfig(self.__current, fill="yellow")

    def __button_press(self, event):    # зберігає данні теперішнього об'єкта та викликає функцію його переміщення
        item = self.__canvas.find_withtag(tk.CURRENT)
        self.__dnd_item = (item, event.x, event.y)
        self.__canvas.tag_bind("draggable", "<Button1-Motion>", self.__button_motion)

    def __button_motion(self, event):   # функція переміщення об'єкта
        x, y = event.x, event.y
        try:
            vertex_id, x0, y0 = self.__dnd_item
        except TypeError:
            return
        if x - 15 <= 0 or y - 15 <= 0 or x + 15 >= self.__canvas.winfo_width() or y + 15 >= self.__canvas.winfo_height():
            if x - 5 <= 0:
                x = 15
            elif x + 5 >= self.__canvas.winfo_width():
                x = self.__canvX - 15
            elif y - 5 <= 0:
                y = 15
            elif y + 5 >= self.__canvas.winfo_height():
                y = self.__canvY - 15
        else:
            self.__canvas.move(vertex_id, x - x0, y - y0)
            for ed in self.__graph.get_edges():
                x, y = event.x, event.y
                if ed.get_id_first() == vertex_id[0]:
                    coord = ed.get_coord(vertex_id[0])
                    self.__canvas.coords(ed.get_id(), x, y, *coord)
                    self.__graph.change_edge(ed.get_id(), vertex_id[0], x, y)
                elif ed.get_id_second() == vertex_id[0]:
                    coord = ed.get_coord(vertex_id[0])
                    self.__canvas.coords(ed.get_id(), *coord, x, y)
                    self.__graph.change_edge(ed.get_id(), vertex_id[0], x, y)

            self.__dnd_item = (vertex_id, x, y)
            self.__graph.get_vertexes()[vertex_id[0]][0].changeXY(x, y)  # словник вершин[id вершини][0] = об'єкт вершина
            self.__graph.add_vertex(self.__graph.get_vertexes()[vertex_id[0]][0])

    def __set_selection(self, widget, action):    # функція надання активній кнопці натиснутого вигляду
        if self.__frame in widget.master.winfo_children():  # якщо рамка знаходиться на одному рівні з віджетом
            for w in widget.master.winfo_children():
                w.config(relief=tk.RAISED)
            for w in self.__frame.winfo_children():
                w.config(relief=tk.RAISED)
            widget.config(relief=tk.SUNKEN)
        else:
            for w in self.__frame.master.winfo_children():
                w.config(relief=tk.RAISED)
            for w in widget.master.winfo_children():
                w.config(relief=tk.RAISED)
            widget.config(relief=tk.SUNKEN)
        self.__canvas.itemconfig(tk.ALL, fill="red")
        self.__action = action  # передаємо змінній текст вибраної кнопки

    def __draw_vertex(self, event):  # функція створення вершини
        x, y = event.x, event.y
        if self.__current:
            if self.__current[0] in self.__graph.get_vertexes_id():
                cur_x, cur_y = self.__graph.get_vertexes()[self.__current[0]][1:3]
                if abs(cur_x - x) >= 35 or abs(cur_y - y) >= 35:
                     self.__graph.add_vertex(Graph._Vertex(self.__canvas.create_oval(x - 15, y - 15, x + 15, y + 15,
                                                                                     fill="red", activefill="yellow", tags=("draggable")), x, y))
            else:
                self.__graph.add_vertex(Graph._Vertex(self.__canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="red",
                                                                                activefill="yellow", tags=("draggable")), x, y))
        else:
            self.__graph.add_vertex(Graph._Vertex(self.__canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="red",
                                                                            activefill="yellow", tags=("draggable")), x, y))

    def __draw_edge(self):    # функція створення ребра
        if self.__current:
            if not self.__start:
                if self.__current[0] in self.__graph.get_vertexes_id():
                    cv = self.__graph.get_vertexes()[self.__current[0]]
                    self.name1 = self.__current[0]
                    self.__start = [cv[1], cv[2]]
                if self.__current[0] in self.__graph.get_edges_id():
                    tk.messagebox.showinfo('ребро', "не можна проводити ребра із ребер")
                    return
            else:
                flag = 0
                if self.__current[0] in self.__graph.get_edges_id():
                    flag = tk.messagebox.showinfo('ребро', "не можна проводити ребро в ребро")
                elif self.name1 == self.__current[0]:
                    flag = tk.messagebox.showinfo('ребро', "ребро виходить та входить в одну вершину")
                elif self.__graph.check_edge(self.name1, self.__current[0]):
                    flag = tk.messagebox.showinfo('ребро', "ребро вже існує")
                if flag:
                    self.__start = None
                    self.name1 = ''
                    return
                else:
                    x2, y2 = self.__start
                    self.__start = None
                    cv = self.__graph.get_vertexes()[self.__current[0]]
                    bbox = (cv[1], cv[2], x2, y2)
                    edge = Graph._Edge(self.__canvas.create_line(*bbox, fill="red", activefill="yellow", width=2),
                                       *bbox, self.name1, self.__current[0])
                    self.__graph.add_edge(edge, self.name1, self.__current[0])

    def __del_click(self):   # функція видалення об'єкта
        for elem in self.__graph.get_vertexes().values():  # якщо елемент належить вершинам
            if self.__current[0] == elem[0].get_id():
                edges = elem[0].get_edge()
                for i in range(len(edges) - 1, -1, -1):
                    if edges[i].get_id_first() == elem[0].get_id():
                        self.__graph.get_vertexes()[edges[i].get_id_second()][0].remove_edge(
                            edges[i].get_id())  # з об'єкта "вершина" видаляємо ребро
                    elif edges[i].get_id_second() == elem[0].get_id():
                        self.__graph.get_vertexes()[edges[i].get_id_first()][0].remove_edge(edges[i].get_id())
                    self.__canvas.delete(edges[i].get_id())
                    self.__graph.del_edge(edges[i].get_id())
                self.__graph.del_vert(elem[0].get_id())

        for elem in self.__graph.get_edges():  # якщо елемент належить ребрам
            if self.__current[0] == elem.get_id():
                self.__graph.get_vertexes()[elem.get_id_first()][0].remove_edge(elem.get_id())
                self.__graph.get_vertexes()[elem.get_id_second()][0].remove_edge(elem.get_id())
                self.__graph.del_edge(elem.get_id())
        self.__canvas.delete(self.__current[0])

    def __do_action(self, event):    # функція яка викликає задані функції
        self.__dnd_item = None
        if self.__action == "вершина":
            self.__draw_vertex(event)
        elif self.__action == "ребро":
            self.__draw_edge()
        elif self.__action == "переміщення":
            self.__button_press(event)
        elif self.__action == "видалення":
            self.__del_click()
        elif self.__action == 'greedy':
            self.__info_text = tk.StringVar(value=greedy(self.__graph, self.__canvas))
        elif self.__action == 'approx':
            self.__info_text = tk.StringVar(value=approx(self.__graph, self.__canvas))

        self.__info_label.config(textvariable=self.__info_text)

    def run(self):
        self.__root.mainloop()


if __name__ == '__main__':
    window = Window(1075, 495, 'Вершинне покриття', resizable=(False, False), icon=f'{sys.path[0]}\ico\graph2.ico')
    window.run()
