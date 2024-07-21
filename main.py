import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QHeaderView, QMessageBox, QInputDialog
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import Qt

class MessageApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.loadMessages()

    def initUI(self):
        # Layout ve widgetları oluştur
        self.layout = QVBoxLayout()
        
        self.searchBar = QLineEdit(self)
        self.searchBar.setPlaceholderText("Ara...")
        self.searchBar.textChanged.connect(self.filterMessages)
        
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Mesaj", "Kopyala", "Düzenle", "Sil"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        
        self.refreshButton = QPushButton("Yenile", self)
        self.refreshButton.clicked.connect(self.loadMessages)
        
        self.addButton = QPushButton("Ekle", self)
        self.addButton.clicked.connect(self.addMessage)

        self.layout.addWidget(self.searchBar)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.refreshButton)
        self.layout.addWidget(self.addButton)
        
        self.setLayout(self.layout)
        
        self.setWindowTitle("Mesaj Yönetimi")
        self.setGeometry(300, 300, 600, 400)

    def loadMessages(self):
        try:
            with open('mesajlar.txt', 'r', encoding='utf-8') as file:
                self.messages = file.readlines()
        except FileNotFoundError:
            self.messages = []

        self.displayMessages(self.messages)

    def displayMessages(self, messages):
        self.table.setRowCount(len(messages))
        for row, message in enumerate(messages):
            message_item = QTableWidgetItem(message.strip())
            copy_button = QPushButton("Kopyala")
            copy_button.clicked.connect(lambda ch, msg=message: self.copyMessage(msg))
            
            edit_button = QPushButton("Düzenle")
            edit_button.clicked.connect(lambda ch, r=row: self.editMessage(r))
            
            delete_button = QPushButton("Sil")
            delete_button.clicked.connect(lambda ch, r=row: self.deleteMessage(r))
            
            self.table.setItem(row, 0, message_item)
            self.table.setCellWidget(row, 1, copy_button)
            self.table.setCellWidget(row, 2, edit_button)
            self.table.setCellWidget(row, 3, delete_button)

    def filterMessages(self):
        search_term = self.searchBar.text().lower()
        filtered_messages = [msg for msg in self.messages if search_term in msg.lower()]
        self.displayMessages(filtered_messages)

    def addMessage(self):
        new_message, ok = QInputDialog.getText(self, 'Yeni Mesaj Ekle', 'Mesajınızı girin:')
        if ok and new_message:
            with open('mesajlar.txt', 'a', encoding='utf-8') as file:
                file.write(new_message + '\n')
            self.loadMessages()

    def editMessage(self, row):
        old_message = self.messages[row].strip()
        new_message, ok = QInputDialog.getText(self, 'Mesajı Düzenle', 'Mesajınızı düzenleyin:', text=old_message)
        if ok and new_message:
            self.messages[row] = new_message + '\n'
            with open('mesajlar.txt', 'w', encoding='utf-8') as file:
                file.writelines(self.messages)
            self.loadMessages()

    def deleteMessage(self, row):
        reply = QMessageBox.question(self, 'Silme Onayı', 'Bu mesajı silmek istediğinize emin misiniz?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            del self.messages[row]
            with open('mesajlar.txt', 'w', encoding='utf-8') as file:
                file.writelines(self.messages)
            self.loadMessages()

    def copyMessage(self, message):
        QGuiApplication.clipboard().setText(message.strip())
        #QMessageBox.information(self, "Kopyalandı", "Mesaj kopyalandı!")

# Uygulamayı başlat
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MessageApp()
    ex.show()
    sys.exit(app.exec())
