from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget, QListWidgetItem, QMessageBox, QFileDialog, QLineEdit, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout, QFrame, QLabel, QSpinBox, QCheckBox, QTextEdit, QPushButton, QStatusBar
from PyQt5 import QtGui, QtCore, uic
import sys
import networkx as nx
import pygraphviz as pgv
import uuid
import os

#Класс графического интерфейса главной формы
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(962, 569)
        MainWindow.setMinimumSize(QtCore.QSize(962, 569))
        MainWindow.setMaximumSize(QtCore.QSize(962, 569))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.table = QTableWidget(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(10, 40, 751, 481))
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.table.horizontalHeader().setDefaultSectionSize(40)
        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(330, 10, 151, 19))
        self.label.setObjectName("label")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(800, 170, 131, 19))
        self.label_2.setObjectName("label_2")
        self.nodeB = QPushButton(self.centralwidget)
        self.nodeB.setGeometry(QtCore.QRect(550, 10, 171, 21))
        self.nodeB.setObjectName("nodeB")
        self.countB = QPushButton(self.centralwidget)
        self.countB.setGeometry(QtCore.QRect(780, 100, 171, 27))
        self.countB.setObjectName("countB")
        self.ngB = QPushButton(self.centralwidget)
        self.ngB.setGeometry(QtCore.QRect(780, 130, 171, 27))
        self.ngB.setObjectName("ngB")
        self.graphB = QPushButton(self.centralwidget)
        self.graphB.setGeometry(QtCore.QRect(780, 10, 171, 27))
        self.graphB.setObjectName("graphB")
        self.result = QTextEdit(self.centralwidget)
        self.result.setGeometry(QtCore.QRect(770, 200, 181, 321))
        self.result.setReadOnly(True)
        self.result.setObjectName("result")
        self.resetB = QPushButton(self.centralwidget)
        self.resetB.setGeometry(QtCore.QRect(450, 10, 88, 21))
        self.resetB.setObjectName("resetB")
        self.loadB = QPushButton(self.centralwidget)
        self.loadB.setGeometry(QtCore.QRect(10, 10, 88, 21))
        self.loadB.setObjectName("loadB")
        self.saveB = QPushButton(self.centralwidget)
        self.saveB.setGeometry(QtCore.QRect(110, 10, 88, 21))
        self.saveB.setObjectName("saveB")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(800, 70, 71, 19))
        self.label_3.setObjectName("label_3")
        self.snode = QSpinBox(self.centralwidget)
        self.snode.setGeometry(QtCore.QRect(870, 70, 49, 21))
        self.snode.setMinimum(1)
        self.snode.setObjectName("snode")
        self.directed = QCheckBox(self.centralwidget)
        self.directed.setGeometry(QtCore.QRect(220, 10, 92, 21))
        self.directed.setChecked(True)
        self.directed.setObjectName("directed")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Пути в бесконтурном графе"))
        self.label.setText(_translate("MainWindow", "Матрица весов"))
        self.label_2.setText(_translate("MainWindow", "Кратчайшие пути:"))
        self.nodeB.setText(_translate("MainWindow", "Добавить вершину"))
        self.countB.setText(_translate("MainWindow", "Рассчитать пути"))
        self.ngB.setText(_translate("MainWindow", "Полученный граф"))
        self.graphB.setText(_translate("MainWindow", "Показать граф"))
        self.resetB.setText(_translate("MainWindow", "Сбросить"))
        self.loadB.setText(_translate("MainWindow", "Загрузить"))
        self.saveB.setText(_translate("MainWindow", "Сохранить"))
        self.label_3.setText(_translate("MainWindow", "Вершина:"))
        self.directed.setText(_translate("MainWindow", "Орграф"))


#Класс элемента матрицы весов
class Cell(QLineEdit):
    def __init__(self, contents='', parent=None, row=0, column=0):
        super(Cell, self).__init__(contents, parent)
        self.row=row
        self.column=column

    def focusOutEvent(self, event):
        if event.reason() != QtCore.Qt.PopupFocusReason:
            self.checkText()
        super(Cell, self).focusOutEvent(event)

    def checkText(self):
        if self.text() == '-' or self.text() == '':
            self.setText('∞')

    def getIndex(self):
        return (self.row, self.column)


#Класс виджета просмотра изображения графа
class PhotoViewer(QGraphicsView):
    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QGraphicsScene(self)
        self._photo = QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.NoFrame)
        self.setAlignment(QtCore.Qt.AlignCenter)

    def hasPhoto(self):
        return not self._empty

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())

    def wheelEvent(self,event):
        if self.hasPhoto():
            factor = 0
            if event.angleDelta().y() > 0:
                factor = 1.25
            else:
                factor=0.8
            self.scale(factor,factor)


    def toggleDragMode(self):
        if self.dragMode() == QGraphicsView.ScrollHandDrag:
            self.setDragMode(QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QGraphicsView.ScrollHandDrag)


#Класс формы просмотра изображения графа
class GraphView(QWidget):
    def __init__(self, fname, title='Граф'):
        super(GraphView, self).__init__()
        self.view = PhotoViewer(self)
        VBlayout = QVBoxLayout(self)
        VBlayout.addWidget(self.view)
        self.resize(1000, 600)
        if fname:
            self.view.setPhoto(QtGui.QPixmap(fname))
            os.unlink(fname)
        else:
            self.view.setPhoto()
        self.setWindowTitle(title)

    def resizeEvent(self, event):
        self.view.setMaximumSize(self.size().width(), self.size().height())
        self.view.resize(self.size().width(), self.size().height())
        QWidget.resizeEvent(self, event)


#Класс приложения
class App(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.setupUi(self)
        self.ngB.setDisabled(True)
        self.snode.setDisabled(True)
        self.nodeB.clicked.connect(self.addNode)
        self.graphB.clicked.connect(self.showGraph)
        self.countB.clicked.connect(self.check)
        self.ngB.clicked.connect(self.showNewGraph)
        self.resetB.clicked.connect(self.reset)
        self.loadB.clicked.connect(self.fromFile)
        self.saveB.clicked.connect(self.toFile)
        self.directed.stateChanged.connect(self.changeState)
        self.curSize = self.size()
        self.graph = None
        self.newGraph = None
        self.logger = None
        self.show()

    #процедура логгирования для листинга решения
    def log(self,line):
        if self.logger:
            self.logger.write(line+'\n')

    #процедура преобразования орграфа в неоргаф
    def changeState(self):
        if not self.directed.isChecked():
            n = self.table.rowCount()
            for i in range(n):
                for j in range(i+1, n):
                    a = self.table.cellWidget(i,j)
                    b = self.table.cellWidget(j,i)
                    c = float("Inf")
                    d = float("Inf")
                    try:
                        c = int(a.text())
                    except:
                        pass
                    try:
                        d = int(b.text())
                    except:
                        pass
                    if c < d:
                        b.setText(a.text())
                    elif d < c:
                        a.setText(b.text())
    
    #процедура добавления новой вершины в матрицу
    def addNode(self):
        self.snode.setDisabled(False)
        self.ngB.setDisabled(True)
        table = self.table
        table.setRowCount(table.rowCount()+1)
        table.setColumnCount(table.columnCount()+1)
        self.snode.setMaximum(table.rowCount())
        validator = QtGui.QRegExpValidator(QtCore.QRegExp('^(∞|0|-?[1-9]+[0-9]*)$'))#проверяет соответствует ли ввод данному выражению
        for i in range(table.rowCount()-1):
            item = Cell(row=i,column=table.columnCount()-1)
            item.setValidator(validator)
            item.setText('∞')
            item.textChanged.connect(self.cellChanged)
            table.setCellWidget(i,table.columnCount()-1,item)
        for i in range(table.columnCount()-1):
            item = Cell(row=table.rowCount()-1,column=i)
            item.setValidator(validator)
            item.setText('∞')
            item.textChanged.connect(self.cellChanged)
            table.setCellWidget(table.rowCount()-1,i,item)
        item = QLineEdit()
        item.setText('0')
        item.setReadOnly(True)
        table.setCellWidget(table.rowCount()-1,table.columnCount()-1,item)

    #процедура автоматического заполнения веса дуги (u,v) для дуги (v,u) в неоргафе
    def cellChanged(self):
        self.ngB.setDisabled(True)
        if not self.directed.isChecked():
            a = self.sender()
            ind = a.getIndex()
            b = self.table.cellWidget(ind[1],ind[0])
            if a.text() != b.text():
                b.setText(a.text())

    #функция создания объекта графа и добавление к нему параметров визуализации
    def createGraph(self):
        G = None
        if self.directed.isChecked():#если орграф
            G = pgv.AGraph(strict=False, splines="true", overlap="scale")
            G.edge_attr['dir']="forward"
            G.edge_attr['arrowsize']="0.7"
        else:
            G = pgv.AGraph(splines='true', overlap="scale")
        G.node_attr['fontsize']='13'
        G.node_attr['shape']='circle'
        G.node_attr['fillcolor']='orange'
        G.node_attr['style']="filled"
        G.node_attr['color']="white"
        G.edge_attr['fontsize']='13'
        G.edge_attr['minlen']=2
        G.edge_attr['fontcolor']='red'
        G.edge_attr['fontname']="Times-Roman"
        G.edge_attr['len']=2
        G.add_nodes_from(range(1,self.table.rowCount()+1))#Добавление вершин к графу
        return G

    #процедура визуализации графа
    def showGraph(self):
        t = self.table
        N = t.rowCount()
        if N==0:
            self.graph = GraphView(None,'Исходный граф')
            self.graph.show()
            return
        G = self.createGraph()
        for i in range(N):
            for j in range(N):
                if i != j:#Если i и j не одна и та же вершина
                    l = t.cellWidget(i,j).text()
                    if l != '∞':
                        G.add_edge(i+1,j+1, label="<<B>("+l+")</B>>")#Добавление ребра к графу
        prog = "dot" if nx.is_tree(nx.drawing.nx_agraph.from_agraph(G)) else "neato" #Если граф - дерево, используется один алгоритм определения позиций, иначе - другой
        name = str(uuid.uuid4())+".png"
        G.draw(name, prog=prog)
        self.graph = GraphView(name,'Исходный граф')
        self.graph.show()

    #процедура визуализации переименованного графа
    def showNewGraph(self):
        t = self.table
        N = t.rowCount()
        if N==0:
            self.newGraph = GraphView(None,'Переименованный граф')
            self.newGraph.show()
            return
        G = self.createGraph()
        Num = self.Num #Список новых номеров вершин
        for k in range(N):
            i = Num[k] #Получение нового номера вершины
            for f in range(N):
                j = Num[f]
                if i != j:
                    l = t.cellWidget(k,f).text()
                    if l != '∞':
                        G.add_edge(i+1,j+1, label="<<B>("+l+")</B>>")
        prog = "dot" if nx.is_tree(nx.drawing.nx_agraph.from_agraph(G)) else "neato"
        name = str(uuid.uuid4())+".png"
        G.draw(name, prog=prog)
        self.newGraph = GraphView(name,'Переименованный граф')
        self.newGraph.show()

    #процедура топологической сортировки
    def Change_Num(self):
        self.log("Процедура Change_Num:")
        t = self.table#матрица весов
        N = t.rowCount()
        self.log('A = [['+'],\n     ['.join([','.join([t.cellWidget(i,j).text() for j in range(N)]) for i in range(N)])+']]')
        NumIn = [0]*N#Список количеств входящих дуг для каждой вершины
        self.log('NumIn = ['+','.join([str(c) for c in NumIn])+']')
        self.Num = [0]*N#Список новых номеров вершин
        Num = self.Num
        self.log('Num = ['+','.join([str(c) for c in Num])+']')
        St = [0]*N#Хранит номера вершин, в которые заходит нулевой количество дуг
        self.log('St = ['+','.join([str(c) for c in St])+']')
        for i in range(N):
            self.log('i = '+str(i))
            for j in range(N):
                self.log('  j = '+str(j))
                if i != j and t.cellWidget(i,j).text() != '∞':#Если есть дуга (i,j)
                    self.log("  i <> j && A[i,j] <> '∞'")
                    NumIn[j]+=1 #Увеличиваем счетчик для j
                    self.log('    NumIn = ['+','.join([str(c) for c in NumIn])+']')
        yk=-1
        self.log('yk = '+str(yk))
        for k in range(N):
            self.log('k = '+str(k))
            if NumIn[k]==0:#Если нет дуг в вершину k
                self.log('Num[k] == 0')
                yk = yk+1
                self.log('  yk = '+str(yk))
                St[yk]=k
                self.log('  St = ['+','.join([str(c) for c in St])+']')                         
        u=0
        nm=-1
        self.log('nm = '+str(nm))               
        while yk != -1:
            self.log("yk <> -1")
            u = St[yk]
            self.log('  u = '+str(u))
            yk = yk - 1
            self.log('  yk = '+str(yk))
            nm = nm+1
            self.log('  nm = '+str(nm))
            Num[u]=nm
            self.log('  Num = ['+','.join([str(c) for c in Num])+']')
            for f in range(N):
                self.log('  f = '+str(f))
                if u != f and t.cellWidget(u,f).text() != '∞':#Если есть дуга из u в f
                    self.log("'  u <> f && A[u,f] <> '∞'")
                    NumIn[f]=NumIn[f]-1
                    self.log('    NumIn = ['+','.join([str(c) for c in NumIn])+']')
                    if NumIn[f]==0:
                        self.log('    NumIn[f] == 0')
                        yk = yk+1
                        self.log('      yk = '+str(yk))
                        St[yk]=f
                        self.log('      St = ['+','.join([str(c) for c in St])+']') 

    #процедура вычисления кратчайших расстояний
    def Dist(self):
        self.log("\nПроцедура Dist:")
        t = self.table#матрица весов
        N = t.rowCount()
        self.log('A = [['+'],\n     ['.join([','.join([t.cellWidget(i,j).text() for j in range(N)]) for i in range(N)])+']]')
        Num = self.Num
        self.log('Num = ['+','.join([str(c) for c in Num])+']')
        self.log("Start_node = "+str(self.snode.value()))
        D = [0]*N
        self.log('D = ['+','.join([str(c) for c in D])+']')
        Max = self.maxEl()#максимальный элемент матрицы
        maxint = float("Inf")#максимальное возможное значение
        self.log('Max = '+str(Max))
        self.log('maxint = '+str(maxint))
        for i in range(N):#Заполнение массива D максимальными значениями
            self.log('i = '+str(i))
            D[i]=maxint-Max
            self.log('  D = ['+','.join([str(c) for c in D])+']')
        if N>0:
            D[self.snode.value()-1]=0#Установка расстояния 0 для вершины, от которой необходимо найти расстояния
        self.log('D = ['+','.join([str(c) for c in D])+']')
        BN = [Num.index(x) for x in range(N)]#Массив, сопоставляющий новые номера со старыми
        self.log('BN = ['+','.join([str(c) for c in BN])+']')
        for k in range(1,N):
            self.log('k = '+str(k))
            i = BN[k]#Получение старого номера вершины
            self.log('i = '+str(i))
            for f in range(k):
                self.log('  f = '+str(f))
                j = BN[f]#Получение старого номера вершины
                self.log('  j = '+str(j))
                it = t.cellWidget(j,i).text()
                if it != '∞':
                    self.log("  A[j,i] <> '∞'")
                    D[i]=min(D[i], D[j]+int(it))
                    self.log('    D = ['+','.join([str(c) for c in D])+']')
        self.log('D = ['+','.join([str(c) for c in D])+']')
        self.log("\nКратчайшие расстояния:")
        for i in range(N):
            r = D[i] if D[i] < maxint-Max else "∞"#Если D[i] - максимальное возможное значение, выводится бесконечность
            s = "{}-{}={}".format(self.snode.value(), i+1, r)
            self.result.append(s)
            self.log(s)

    #процедура, проверяющая является ли граф бесконтурным
    def check(self):
        self.result.clear()
        t = self.table
        G = nx.DiGraph()
        for i in range(t.rowCount()):
            for j in range(t.columnCount()):
                l = t.cellWidget(i,j).text()
                if i != j and l != '∞':
                    G.add_edge(i+1,j+1)
        if nx.is_directed_acyclic_graph(G):#Если граф бесконтурный, запускаем вычисления
            try:
                self.logger = open('ind.log', 'a')
            except IOError as e:
                self.logger = None
                msg = QMessageBox()
                msg.setText("Невозможно открыть файл для записи решения.")
                msg.exec()
            self.Change_Num()
            self.Dist()
            self.ngB.setDisabled(False)
            if self.logger:
                self.logger.close()
        else:
            msg = QMessageBox()
            msg.setText("Данный граф не является бесконтурным.")
            msg.exec()

    #функция вычисления максимального элемента
    def maxEl(self):
        m = 0
        t = self.table
        for i in range(t.rowCount()):
            for j in range(t.columnCount()):
                e = t.cellWidget(i,j).text()
                if e != '∞' and int(e) > m:
                    m = int(e) 
        return m

    #сбрасывает параметры и очищает матрицу
    def reset(self):
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        self.nn = None
        self.ngB.setDisabled(True)
        self.result.clear()
        self.snode.setValue(1)
        self.snode.setDisabled(True)

    #процедура чтения матрицы из файла
    def fromFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Открыть граф', os.getcwd(),"Файлы графов (*.gr)")
        if not fname:
            return
        t = None
        try:
            t = open(fname[0], "r")
        except:
            msg = QMessageBox()
            msg.setText("Невозможно открыть файл.")
            msg.exec()
        finally:
            if not t:
                return
        m=[]#создание пустого списка
        for l in t:
            m.append(l.strip().split())#разбиение строки на список и добавление его в список m
        t.close()
        N = len(m)
        for i in m:
            if len(i) != N:#Если длина строки не соответствует длине столбца
                msg = QMessageBox()
                msg.setText("Файл поврежден.")
                msg.exec()
                return
        t = self.table
        t.setRowCount(N)
        t.setColumnCount(N)
        if N > 0:
            self.snode.setMaximum(N)
            self.snode.setDisabled(False)
        for i in range(N):#проверка элементов диагонали
            if m[i][i] != '0':
                msg = QMessageBox()
                msg.setText("Графы с петлями не допустимы.")
                msg.exec()
                self.reset()
                return
            else:
                item = QLineEdit()
                item.setText('0')
                item.setReadOnly(True)
                t.setCellWidget(i,i,item)
        validator = QtGui.QRegExpValidator(QtCore.QRegExp('^(∞|0|-?[1-9]+[0-9]*)$'))#проверяет на соответствие регулярному выражению
        directed = False
        for i in range(N):
            for j in range(i+1, N):
                try:
                    if m[i][j] != '∞':
                        int(m[i][j])#проверка на число
                    item = Cell(row=i,column=j)
                    item.setValidator(validator)
                    item.setText(m[i][j])
                    item.textChanged.connect(self.cellChanged)
                    t.setCellWidget(i,j,item)
                    if m[j][i] != '∞':
                        int(m[j][i])
                    item = Cell(row=j,column=i)
                    item.setValidator(validator)
                    item.setText(m[j][i])
                    item.textChanged.connect(self.cellChanged)
                    t.setCellWidget(j,i,item)
                except:
                    msg = QMessageBox()
                    msg.setText("Недопустимый элемент в матрице.")
                    msg.exec()
                    self.reset()
                    return
                if m[i][j] != m[j][i]:#Если вес дуги (v,u) не равняется весу дуги (u,v), граф - ориентированный
                    directed = True 
        self.directed.setChecked(directed)

    #процедура сохранения матрицы в файл
    def toFile(self):
        fname = QFileDialog.getSaveFileName(self, 'Сохранить граф', os.path.join(os.getcwd(), "graph.gr"),"Файлы графов (*.gr)")
        if fname:
            with open(fname[0], "w") as f:
                t = self.table
                for i in range(t.rowCount()):
                    for j in range(t.columnCount()):
                        f.write(t.cellWidget(i,j).text()+" ")
                    f.write("\n")      


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
