
#from hutil.Qt import QtCore
from PySide2 import QtCore,QtWidgets

class SnipFuzz(QtWidgets.QWidget):

    def __init__(self):
       
        QtWidgets.QWidget.__init__(self)

        self.resize(600,400)
 
        self.name_text = QtWidgets.QLabel("name")
        self.name_field = QtWidgets.QLineEdit()        
        self.desc_text = QtWidgets.QLabel("description")
        self.desc_field = QtWidgets.QLineEdit()        
        self.tags_text = QtWidgets.QLabel("tags")
        self.tags_field = QtWidgets.QLineEdit()        
        self.button = QtWidgets.QPushButton("Save Snippet")

        layout = QtWidgets.QFormLayout(self)
        layout.addWidget(self.name_text)
        layout.addWidget(self.name_field)
        layout.addWidget(self.desc_text)
        layout.addWidget(self.desc_field)
        layout.addWidget(self.tags_text)
        layout.addWidget(self.tags_field)
        layout.addWidget(self.button)
        
        self.setLayout(layout)
        self.button.pressed.connect(self.buttonpress)


    def buttonpress(self):
       
        name = self.name_field.displayText()
        desc = self.desc_field.displayText()
        tags = self.tags_field.displayText()
        
        print(name,desc,tags)

dialog = SnipFuzz()
dialog.setParent(hou.qt.mainWindow(), QtCore.Qt.Window)
dialog.show()
