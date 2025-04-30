import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt6.QtCore import QThread, pyqtSignal

class ChatThread(QThread):
    response_received = pyqtSignal(str)

    def __init__(self, process):
        super().__init__()
        self.process = process

    def run(self):
        # 從 Docker 容器讀取回應
        response = self.process.stdout.readline().strip()
        self.response_received.emit(response)

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Chat Application")
        self.setGeometry(100, 100, 600, 400)

        # 設置主窗口部件和佈局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 對話歷史顯示區域
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        layout.addWidget(self.chat_history)

        # 用戶輸入框
        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.send_message)
        layout.addWidget(self.input_field)

        # 發送按鈕
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        layout.addWidget(self.send_button)

        # 啟動 Docker 容器
        self.process = subprocess.Popen(
            ["docker", "run", "-i", "--rm", "chatbot"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )

    def send_message(self):
        user_input = self.input_field.text().strip()
        if not user_input:
            return

        # 顯示用戶輸入
        self.chat_history.append(f"User: {user_input}")
        self.input_field.clear()

        # 將輸入發送到 Docker 容器
        self.process.stdin.write(user_input + "\n")
        self.process.stdin.flush()

        # 啟動線程以讀取回應
        self.chat_thread = ChatThread(self.process)
        self.chat_thread.response_received.connect(self.update_chat_history)
        self.chat_thread.start()

    def update_chat_history(self, response):
        # 顯示 AI 回應
        self.chat_history.append(f"AI: {response}")

    def closeEvent(self, event):
        # 關閉應用程式時終止 Docker 容器
        self.process.stdin.write("exit\n")
        self.process.stdin.flush()
        self.process.terminate()
        event.accept()

def main():
    # 構建 Docker 映像
    subprocess.run(["docker", "build", "-t", "chatbot", "."])

    # 啟動 PyQt 應用程式
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()