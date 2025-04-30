from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt6.QtCore import QThread, pyqtSignal
from ai import AIChat

class ChatThread(QThread):
    response_received = pyqtSignal(str)

    def __init__(self, ai_chat, user_input, chat_history_ids):
        super().__init__()
        self.ai_chat = ai_chat
        self.user_input = user_input
        self.chat_history_ids = chat_history_ids

    def run(self):
        # 調用 AI 模塊生成回應
        response, new_chat_history_ids = self.ai_chat.generate_response(self.user_input, self.chat_history_ids)
        self.response_received.emit(response)
        # 更新對話歷史
        self.ai_chat.update_chat_history(new_chat_history_ids)

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Chat Application")
        self.setGeometry(100, 100, 600, 400)

        # 初始化 AI 模塊
        self.ai_chat = AIChat()

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

    def send_message(self):
        user_input = self.input_field.text().strip()
        if not user_input:
            return

        # 顯示用戶輸入
        self.chat_history.append(f"User: {user_input}")
        self.input_field.clear()

        # 啟動線程以生成回應
        self.chat_thread = ChatThread(self.ai_chat, user_input, self.ai_chat.chat_history_ids)
        self.chat_thread.response_received.connect(self.update_chat_history)
        self.chat_thread.start()

    def update_chat_history(self, response):
        # 顯示 AI 回應
        self.chat_history.append(f"AI: {response}")