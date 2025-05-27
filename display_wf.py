import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import QTimer

from scan_strongestwf import initialize_wifi_interface, scan_wifi_to_list, akm_to_string

from update2 import Ui_MainWindow  # Giao diện Qt Designer export

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.iface = initialize_wifi_interface()

        # Cấu hình bảng hiển thị
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setHorizontalHeaderLabels(["SSID", "Tín hiệu", "Bảo mật", "MAC"])
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.ui.tableWidget.horizontalHeader().setStyleSheet(
            "QHeaderView::section { color: green; font-weight: bold; }")

        # Tạo QTimer quét WiFi mỗi 5 giây
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_wifi_networks)
        self.timer.start(5000)

        # Quét lần đầu ngay khi chạy
        self.load_wifi_networks()

    def load_wifi_networks(self):
        self.ui.statusbar.showMessage("Đang quét WiFi...")
        wifi_list = scan_wifi_to_list(self.iface)

        self.ui.tableWidget.setRowCount(len(wifi_list))
        for row, ap in enumerate(wifi_list):
            ssid = ap['SSID']
            signal = str(ap['Signal'])
            auth = ", ".join([akm_to_string(a) for a in ap['Auth']]) or "OPEN"
            mac = ap['MAC']

            # Thêm các ô vào bảng
            for col, text in enumerate([ssid, signal, auth, mac]):
                item = QTableWidgetItem(text)
                item.setForeground(QtGui.QColor("black"))
                self.ui.tableWidget.setItem(row, col, item)

        self.ui.statusbar.showMessage(f"Quét xong. Tìm thấy {len(wifi_list)} mạng.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
