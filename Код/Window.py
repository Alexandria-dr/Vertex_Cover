import tkinter as tk
from tkinter import Tk
from functools import partial
from Graph import Graph
from tkinter import messagebox
from Metods import *


class Window:
    def __init__(self, width, height, title='My window', resizable=(False, False), icon=None):
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(f'{width}x{height}+200+200')
        self.root.resizable(resizable[0], resizable[1])
        if icon:
            self.root.iconbitmap(icon)
        self.root.configure(background='light blue')
        self.actions = ('вершина', 'ребро', 'переміщення', 'видалення', 'approx', 'greedy')
        self.start = None  # координати
        self.action = None
        self.current = None
        self.canvX = 800
        self.canvY = 450
        self.canvas = tk.Canvas(self.root, bg="white", width=self.canvX, height=self.canvY)
        self.canvas.grid(row=0, columnspan=4)
        self.dnd_item = ()

        for i in range(4):
            btn = tk.Button(self.root, text=self.actions[i], font=('Consolas', 16))
            btn.config(command=partial(self.set_selection, btn, self.actions[i]))
            btn.grid(column=i, row=1, sticky=tk.W + tk.E + tk.S + tk.N)
        self.frame = tk.Frame(background='light blue')
        for i in range(4, 6):
            btn = tk.Button(self.frame, text=self.actions[i], font=('Consolas', 16))
            btn.config(command=partial(self.set_selection, btn, self.actions[i]))
            btn.grid(column=i - 4, row=0, sticky=tk.W + tk.E + tk.S + tk.N, pady=20, padx=23)
        btn = tk.Button(self.frame, text='вирішити', font=('Consolas', 16), command=lambda:
            self.draw_item(0) if (self.action == 'approx' or self.action == 'greedy') else None)
        btn.grid(columnspan=2, column=0, row=1, padx=35, pady=20)

        self.info_text = tk.StringVar(value='')
        self.info_label = tk.Label(self.frame, textvariable=self.info_text, bg='white', height=15, relief=tk.RAISED,
                                   wraplength=200, justify=tk.LEFT)
        self.info_label.grid(columnspan=2, column=0, row=2, padx=25, pady=20, sticky=tk.W + tk.E)

        self.frame.grid(columnspan=2, column=5, rowspan=3, row=0, sticky=tk.W + tk.S + tk.N)
        self.canvas.bind("<Motion>", self.mouse_motion)
        self.canvas.bind("<Button-1>", self.draw_item)
        self.canvas.tag_bind("draggable", "<ButtonPress-1>", self.button_press)
        self.graph = Graph()

    def mouse_motion(self, event):
        if self.action != "greedy" and self.action != 'approx':
            self.canvas.itemconfig(self.current, fill="red")
            self.current = self.canvas.find_closest(event.x, event.y)
            self.canvas.itemconfig(self.current, fill="yellow")

    def button_press(self, event):
        item = self.canvas.find_withtag(tk.CURRENT)
        self.dnd_item = (item, event.x, event.y)
        self.canvas.tag_bind("draggable", "<Button1-Motion>", self.button_motion)

    def button_motion(self, event):
        x, y = event.x, event.y
        try:
            vertex_id, x0, y0 = self.dnd_item
        except TypeError:
            return
        if x - 15 <= 0 or y - 15 <= 0 or x + 15 >= self.canvas.winfo_width() or y + 15 >= self.canvas.winfo_height():
            if x - 5 <= 0:
                x = 15
            elif x + 5 >= self.canvas.winfo_width():
                x = self.canvX - 15
            elif y - 5 <= 0:
                y = 15
            elif y + 5 >= self.canvas.winfo_height():
                y = self.canvY - 15
        else:
            self.canvas.move(vertex_id, x - x0, y - y0)
            for ed in self.graph.get_edges():
                x, y = event.x, event.y
                if ed.get_id_first() == vertex_id[0]:
                    coord = ed.get_coord(vertex_id[0])
                    self.canvas.coords(ed.get_id(), x, y, *coord)
                    self.graph.change_edge(ed.get_id(), vertex_id[0], x, y)
                elif ed.get_id_second() == vertex_id[0]:
                    coord = ed.get_coord(vertex_id[0])
                    self.canvas.coords(ed.get_id(), *coord, x, y)
                    self.graph.change_edge(ed.get_id(), vertex_id[0], x, y)

            self.dnd_item = (vertex_id, x, y)
            self.graph.get_vertexes()[vertex_id[0]][0].changeXY(x, y)  # словник вершин[id вершини][0] = об'єкт вершина
            self.graph.add_vertex(self.graph.get_vertexes()[vertex_id[0]][0])

    def set_selection(self, widget, action):
        if self.frame in widget.master.winfo_children():  # якщо рамка знаходиться на одному рівні з віджетом
            for w in widget.master.winfo_children():
                w.config(relief=tk.RAISED)
            for w in self.frame.winfo_children():
                w.config(relief=tk.RAISED)
            widget.config(relief=tk.SUNKEN)
        else:
            for w in self.frame.master.winfo_children():
                w.config(relief=tk.RAISED)
            for w in widget.master.winfo_children():
                w.config(relief=tk.RAISED)
            widget.config(relief=tk.SUNKEN)
        self.canvas.itemconfig(tk.ALL, fill="red")
        self.action = action  # передаємо змінній текст вибраної кнопки

    def draw_vertex(self, event):
        x, y = event.x, event.y
        if self.current:
            if self.current[0] in self.graph.get_vertexes_id():
                cur_x, cur_y = self.graph.get_vertexes()[self.current[0]][1:3]
                if abs(cur_x - x) >= 35 or abs(cur_y - y) >= 35:
                     self.graph.add_vertex(Graph.Vertex(self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15,
                                                fill="red", activefill="yellow", tags=("draggable", "circle")), x, y))
            else:
                self.graph.add_vertex(Graph.Vertex(self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="red",
                                                            activefill="yellow", tags=("draggable", "circle")), x, y))
        else:
            self.graph.add_vertex(Graph.Vertex(self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="red",
                                                            activefill="yellow", tags=("draggable", "circle")), x, y))

    def draw_edge(self):
        if self.current:
            if not self.start:
                if self.current[0] in self.graph.get_vertexes_id():
                    cv = self.graph.get_vertexes()[self.current[0]]
                    self.name1 = self.current[0]
                    self.start = (cv[1], cv[2])
                if self.current[0] in self.graph.get_edges_id():
                    tk.messagebox.showinfo('ребро', "не можна проводити ребра із ребер")
                    return
            else:
                flag = 0
                if self.current[0] in self.graph.get_edges_id():
                    flag = tk.messagebox.showinfo('ребро', "не можна проводити ребро в ребро")
                elif self.name1 == self.current[0]:
                    flag = tk.messagebox.showinfo('ребро', "ребро виходить та входить в одну вершину")
                elif self.graph.check_edge(self.name1, self.current[0]):
                    flag = tk.messagebox.showinfo('ребро', "ребро вже існує")
                if flag:
                    self.start = None
                    self.name1 = ''
                    return
                else:
                    x2, y2 = self.start
                    self.start = None
                    cv = self.graph.get_vertexes()[self.current[0]]
                    bbox = (cv[1], cv[2], x2, y2)
                    edge = Graph.Edge(self.canvas.create_line(*bbox, fill="red", activefill="yellow", width=2),
                                      *bbox, self.name1, self.current[0])
                    self.graph.add_edge(edge, self.name1, self.current[0])

    def del_click(self):
        for elem in self.graph.get_vertexes().values():  # якщо елемент належить вершинам
            if self.current[0] == elem[0].get_id():
                edges = elem[0].get_edge()
                for i in range(len(edges) - 1, -1, -1):
                    if edges[i].get_id_first() == elem[0].get_id():
                        self.graph.get_vertexes()[edges[i].get_id_second()][0].remove_edge(
                            edges[i].get_id())  # з об'єкта "вершина" видаляємо ребро
                    elif edges[i].get_id_second() == elem[0].get_id():
                        self.graph.get_vertexes()[edges[i].get_id_first()][0].remove_edge(edges[i].get_id())
                    self.canvas.delete(edges[i].get_id())
                    self.graph.del_edge(edges[i].get_id())
                self.graph.del_vert(elem[0].get_id())

        for elem in self.graph.get_edges():  # якщо елемент належить ребрам
            if self.current[0] == elem.get_id():
                self.graph.get_vertexes()[elem.get_id_first()][0].remove_edge(elem.get_id())
                self.graph.get_vertexes()[elem.get_id_second()][0].remove_edge(elem.get_id())
                self.graph.del_edge(elem.get_id())
        self.canvas.delete(self.current[0])

    def draw_item(self, event):

        self.dnd_item = None
        if self.action == "вершина":
            self.draw_vertex(event)
        elif self.action == "ребро":
            self.draw_edge()
        elif self.action == "переміщення":
            self.button_press(event)
        elif self.action == "видалення":
            self.del_click()
        elif self.action == 'greedy':
            self.info_text = tk.StringVar(value=greedy(self.graph, self.canvas))
        elif self.action == 'approx':
            self.info_text = tk.StringVar(value=approx(self.graph, self.canvas))

        self.info_label.config(textvariable=self.info_text)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    window = Window(1075, 495, 'tkinter', resizable=(False, False))
    window.run()
