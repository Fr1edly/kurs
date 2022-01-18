from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
import sys, os


class Win(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Win, self).__init__(*args, **kwargs)
        
        self.input_label=QLabel('Название критерия',parent=self)
        self.input_label.move(600,10)
        self.crit_name = QLineEdit(parent=self)
        self.crit_name.setGeometry(580, 40, 150, 30)

        self.obj_label=QLabel("Название объекта", parent=self)
        self.obj_label.move(600,300)
        self.obj_name = QLineEdit(parent=self)
        self.obj_name.setGeometry(585,325, 150,30)

        self.boundmin = QLabel('Нижняя граница',parent=self)
        self.boundmin.move(570,120)
        self.minval = QLineEdit(parent=self)
        self.minval.setGeometry(580, 150, 70, 25)
        self.boundmax = QLabel('Верхняя граница',parent=self)
        self.boundmax.move(680,120)
        self.maxval = QLineEdit(parent=self)
        self.maxval.setGeometry(690, 150, 70, 25)

        self.down = QRadioButton('Прямой', parent=self)
        self.down.move(575,80)
        self.up = QRadioButton('Обратный', parent=self)
        self.up.move(655, 80)
        self.input_table = QTableWidget(parent=self)
        self.input_table.setGeometry(10, 100, 500, 200)
        
        self.output_table = QTableWidget(parent=self)
        self.output_table.setGeometry(10, 400, 500, 200)
        
        self.crit_button = QPushButton('Добавить критерий сравнения',parent=self)
        self.crit_button.setGeometry(570, 200, 200, 40)
        self.crit_button.clicked.connect(self.create_crit)

        self.obj_button = QPushButton('Добавить объект сравнения', parent=self)
        self.obj_button.setGeometry(560, 370, 200, 40)
        self.obj_button.clicked.connect(self.create_obj)

        
        self.calc_button = QPushButton('Посчитать', parent=self)
        self.calc_button.setGeometry(220, 360, 70, 30)
        self.calc_button.clicked.connect(self.calc)
        
        #variables
        self.sym =[]
        self.res =[]
        self.granA=[]
        self.granB=[]

        self.show()
    
    def create_obj(self):
        if self.obj_name.text() != '':
            text = self.obj_name.text()
            if self.input_table.rowCount() == 0:
                self.input_table.insertRow(self.input_table.rowCount())
                self.input_table.setVerticalHeaderLabels([text])
            else:
                self.input_table.insertRow(self.input_table.rowCount())
                row=[self.input_table.verticalHeaderItem(i).text() for i in range(self.input_table.rowCount()-1)]
                row.append(text)
                self.input_table.setVerticalHeaderLabels(row)
            self.obj_name.setText('')
        else:
            QMessageBox.warning(self, 'Error', 'Enter object name')

        #rowlabels.append(self.obj_name.text())
        #rowlabels = (['x'+str(i+1) for i in range(self.input_table.rowCount())])
        #self.input_table.setVerticalHeaderLabels(rowlabels)
        
    
    def create_crit(self):
#/--------------------------------------------------------------------------------------\
#\--------------------------------------------------------------------------------------/
        #Для Парето
        if self.up.isChecked():
            self.sym.append(True)
        elif self.down.isChecked():
            self.sym.append(False)
        else:
            QMessageBox.warning(self, 'Error', 'Please, chose criterios type')
            return
#/--------------------------------------------------------------------------------------\
#\--------------------------------------------------------------------------------------/
        if self.crit_name.text() != '' and self.crit_name.text() != None:
            if self.minval.text() == '' and self.minval.text() == None or self.maxval.text() == '' and self.maxval.text() == None:
                QMessageBox.warning(self, 'Error', 'Enter a bounds')
            else:
                if self.minval.text() != '' and self.maxval.text() != '':
                    self.granA.append(float(self.minval.text()))
                    self.granB.append(float(self.maxval.text()))
                else:
                    self.granA.append(-1.0)
                    self.granB.append(-1.0)
                
                text = self.crit_name.text()
                if self.input_table.columnCount() == 0:
                    self.input_table.insertColumn(self.input_table.columnCount())
                    self.input_table.setHorizontalHeaderLabels([text])
                    self.crit_name.setText('')
                
                else:
                    self.input_table.insertColumn(self.input_table.columnCount())
                    self.output_table.insertColumn(self.input_table.columnCount())
                    columnlabels=[self.input_table.horizontalHeaderItem(i).text() for i in range(self.input_table.columnCount()-1)]
                    columnlabels.append(text)
                    self.input_table.setHorizontalHeaderLabels(columnlabels)
                    self.output_table.setHorizontalHeaderLabels(columnlabels)
                    self.crit_name.setText('')
                pass
                
                self.minval.setText('')
                self.maxval.setText('')
                self.crit_name.setText('')       
        else:
            QMessageBox.warning(self,'Error', 'Enter criterion name')
        
    def calc(self):
        f1: bool
        f2: bool

        f2=True
        self.output_table.setColumnCount(self.input_table.columnCount())
        columnlabels=[self.input_table.horizontalHeaderItem(i).text() for i in range(self.input_table.columnCount())]

        #self.output_table.setVerticalHeaderLabels(rowlabels)
        self.output_table.setHorizontalHeaderLabels(columnlabels)

        """
        дальше надо написать то, по какому принципу будут выделяться подходящие критерии
        кароч, реализация метода
        """
        #----------------------------------------------------------------------------
        #метод

        for i in range(self.input_table.rowCount()):
            for p in range(self.input_table.columnCount()):
                if self.granA[p] != -1 and self.granB[p] !=-1:
                    if not (float(self.input_table.item(i,p).text()) >=self.granA[p] and float(self.input_table.item(i,p).text()) < self.granB[p]):
                        f2 = False 
        if f2:
            for i in range(self.input_table.rowCount()):
                for j in range(self.input_table.rowCount()):
                    if i != j:
                        f1 = False
                        for p in range(self.input_table.columnCount()):
                            if self.sym[p] == True:
                                if float(self.input_table.item(i,p).text()) > float(self.input_table.item(j,p).text()):
                                    f1 = True
                                    break
                            else:
                                if float(self.input_table.item(i,p).text()) < float(self.input_table.item(j,p).text()):
                                    f1 = True
                                    break
                        if f1 == False:
                            self.res.append(j)           
            self.res = list(set(self.res))
            k=0
            overlabels=[self.input_table.verticalHeaderItem(self.input_table.rowCount()-i-1).text() for i in range(self.input_table.rowCount())]
            over=[]
            for i in range(self.input_table.rowCount()):
                f1 = True
                for j in self.res:
                    if i == j:
                        f1 = False
                        break
                if f1 == True:
                    over.append(overlabels[len(overlabels)-i-1])
                    self.output_table.insertRow(self.output_table.rowCount())
                    #self.output_table.insertRow(k)
                    for p in range(self.input_table.columnCount()):
                        self.output_table.setItem(k,p, QTableWidgetItem(self.input_table.item(i,p).text()))    
                        #self.output_table.item(p,k) = self.input_table.item(p,i)
                    k+=1
                    self.output_table.setVerticalHeaderLabels(over)
                

        self.output_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #----------------------------------------------------------------------------

        pass