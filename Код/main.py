import sys
from Window import Window

window = Window(1075, 495, 'Вершинне покриття', resizable=(False, False), icon=f'{sys.path[0]}\ico\graph2.ico')
window.run()