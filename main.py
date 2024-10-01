# price DECIMAL(10, 2) 99999999.99

import sys

from PyQt5.QtWidgets import \
    QApplication, QWidget, \
    QVBoxLayout, QLineEdit, \
    QPushButton, QTableWidget, \
    QTableWidgetItem, QMessageBox, \
    QDoubleSpinBox, QSpinBox, QHBoxLayout, QLabel
import mysql.connector

# MySQL database-ga ulash
conn = mysql.connector.connect(
    host="localhost",
    user="javod",
    password="hHh(26Y2%C~w",
    database="inventory_management"
)
cursor = conn.cursor()


# main window class yaratish
class ProductInventoryManagementApp(QWidget):
    name_input: QLineEdit
    price: QDoubleSpinBox
    quantity: QSpinBox
    table: QTableWidget

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Product Inventory Management")

        # Layout
        layout = QVBoxLayout()

        # product name, product price, product quantity
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter name")
        layout.addWidget(self.name_input)

        price_h_layout = QHBoxLayout()
        price_label = QLabel("Price:")
        self.price = QDoubleSpinBox()  #
        self.price.setRange(0.00, 99999999.99)  #
        self.price.setDecimals(2)  #
        self.price.setSingleStep(0.1)
        price_h_layout.addWidget(price_label)
        price_h_layout.addWidget(self.price)
        layout.addLayout(price_h_layout)

        quantity_h_layout = QHBoxLayout()
        quantity_label = QLabel("Quantity:")
        self.quantity = QSpinBox()
        self.quantity.setRange(1, 1000000)
        self.quantity.setSingleStep(1)
        quantity_h_layout.addWidget(quantity_label)
        quantity_h_layout.addWidget(self.quantity)
        layout.addLayout(quantity_h_layout)

        # product qo'shish button-i
        add_button = QPushButton("Add Product", self)
        add_button.clicked.connect(self.add_product)
        layout.addWidget(add_button)

        # product-ni update qilish button-i
        update_button = QPushButton("Update Selected Product", self)
        update_button.clicked.connect(self.update_product)
        layout.addWidget(update_button)

        # product-ni delete qilish button-i
        delete_button = QPushButton("Delete Selected Product", self)
        delete_button.clicked.connect(self.delete_product)
        layout.addWidget(delete_button)

        # product-larni display qilish uchun table
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Price", "Quantity"])
        self.table.cellClicked.connect(self.select_product)
        layout.addWidget(self.table)

        # app start qilganda product-larni load qilish
        self.load_products()

        self.setLayout(layout)

    def load_products(self):
        self.table.setRowCount(0)  # birinchi
        # navbatda table-ni clear qilish
        cursor.execute("SELECT id, name, price, quantity FROM products")
        for row_idx, (product_id, name, price, quantity) in enumerate(cursor.fetchall()):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(product_id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(str(name)))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(price)))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(quantity)))

    def select_product(self, row, column):
        name = self.table.item(row, 1).text()
        price = self.table.item(row, 2).text()
        quantity = self.table.item(row, 3).text()

        self.name_input.setText(name)
        self.price.setValue(float(price))
        self.quantity.setValue(int(quantity))

    def delete_product(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            product_id = self.table.item(selected_row, 0).text()
            cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
            conn.commit()
            self.load_products()
            self.name_input.clear()
            self.price.clear()
            self.quantity.clear()

    def update_product(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            product_id = self.table.item(selected_row, 0).text()
            new_name = self.name_input.text()
            new_price = float(self.price.text().replace(',', '.')) # self.price.text()
            new_quantity = int(self.quantity.text())

            if new_name and new_price and new_quantity:
                cursor.execute("UPDATE products SET name=%s, price=%s, quantity=%s WHERE id=%s",
                               (new_name, new_price, new_quantity, product_id))
                conn.commit()
                self.load_products()
                self.name_input.clear()
                self.price.clear()
                self.quantity.clear()
            else:
                QMessageBox.warning(self, "Input Error",
                                    "Uchov input field-larni to'ldirish kerak")

    def add_product(self):
        name = self.name_input.text()
        # price = float(self.price.text())
        price = float(self.price.text().replace(',', '.'))
        quantity = int(self.quantity.text())

        if name and price and quantity:
            cursor.execute("INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)",
                           (name, price, quantity))
            try:
                conn.commit()
                self.load_products()
                self.name_input.clear()
                self.price.clear()
                self.quantity.clear()
            except Exception as istisno:
                print(istisno)
        else:
            QMessageBox.warning(self, "Input Error",
                                "Uchov input field-larni to'ldirish kerak")


def main():
    app = QApplication(sys.argv)
    window = ProductInventoryManagementApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
