from PyQt5.QtGui import QPixmap
import sys
from PyQt5.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)

pixmap = QPixmap(r"C:\Users\dell\Desktop\cscomer\.vscode\logo.png")

if pixmap.isNull():
    print("❌ Image failed to load")
else:
    print("✅ Image loaded successfully")

label = QLabel()
label.setPixmap(pixmap)
label.show()

sys.exit(app.exec_())