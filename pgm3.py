import sys
import json
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QTextEdit, QLineEdit, QPushButton, 
                             QComboBox,QGroupBox, QFrame, QScrollArea, QSizePolicy)
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QFont, QColor, QPalette, QTextCursor, QIcon,QPixmap
import os
print("Current working directory:", os.getcwd())
print("Files in this directory:", os.listdir())

class MessageWidget(QWidget):
    def __init__(self, text, is_user=True, timestamp=None):
        super().__init__()
        self.is_user = is_user
        self.timestamp = timestamp or QDateTime.currentDateTime().toString("hh:mm AP")
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Message bubble
        bubble = QFrame()
        bubble_layout = QVBoxLayout(bubble)
        bubble.setLayout(bubble_layout)
        
        # Message text
        message_label = QLabel(text)
        message_label.setWordWrap(True)
        message_label.setTextFormat(Qt.RichText)
        message_label.setStyleSheet("padding: 20px; color: black;")
        
        # Timestamp
        time_label = QLabel(self.timestamp)
        time_label.setAlignment(Qt.AlignRight)
        time_label.setStyleSheet("color: black; font-size: 30px; padding: 0px 4px 2px 4px;")
        
        msg_time_layout = QHBoxLayout()
        msg_time_layout.addWidget(message_label)
        msg_time_layout.addStretch()
        msg_time_layout.addWidget(time_label)
        bubble_layout.addLayout(msg_time_layout)
        
        # Styling
        if is_user:
            bubble.setStyleSheet("""
                QFrame {
                    background-color: #dcf8c6;
                    border-radius: 10px;
                    padding: 5px;
                    margin: 2px;
                }
            """)
            layout.setAlignment(Qt.AlignRight)
        else:
            bubble.setStyleSheet("""
                QFrame {
                    background-color: #ffffff;
                    border-radius: 10px;
                    padding: 5px;
                    margin: 2px;
                    border: 1px solid #e0e0e0;
                }
            """)
            layout.setAlignment(Qt.AlignLeft)
        
        layout.addWidget(bubble)

class ChatBot(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SECAB INSTITUTE OF ENGINEERING AND TECHNOLOGY VIJAYPUR")
        self.setStyleSheet("color:black;font-size:20px;font-weight:bold;")
        self.setGeometry(200, 200, 800, 600)
        
        # Initialize FAQ database
        self.faq_data = self.load_faq_data()
        
        self.setup_ui()
        
    def load_faq_data(self):
        """Load FAQ questions and answers"""
        return {
            "admission": {
                "questions": [
                    "Where is Admission cell Located?",
                    "Where is Principal Office?"
                ],
                "answers": {
                    "default": "It is located at the Enterance of the College."
                }
            },
            "courses": {
                "questions": [
                    "What are  the basic languages required?",
                    "What programming languages are taught?"
                ],
                "answers": {
                    "default": "Python, Java, and C++."
                }
            },
            "Department": {
                "questions": [
                    "Where is Computer Science Department located?",
                    "Where is HOD Cabin Located?",
                ],
                "answers": {
                    "default":"It is Located in Block 4."
                }
            },
            "college":{
                "questions":[
                    "What are department in our college?",
                    "How many department are there in our college?"
                ],
                "answers":{
                    "default":"There are 6 department there are EEE,EC,CSE,AIML,MECH,CIVIL."
                }
            },
            "careers": {
                "questions": [
                    "What job opportunities are there?",
                    "What's the average starting salary?"
                ],
                "answers": {
                    "default": "Tech initator and many startups. The average starting salary is 3LPA with near 75% placement rate."
                }
            }
        }
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Header
        header_widget = QWidget()
        header_layout=QHBoxLayout(header_widget)
        header_widget.setStyleSheet("""
                                    background-color:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #1e3c72,stop:1 #2a5298);
                                    border-radius:8px 8px 0 0;
                                    """)
                                    
        header_layout.setContentsMargins(15,8,15,8)
        header_layout.setSpacing(15)
        
        #College logo(left side)
        logo_label=QLabel()
        logo_pixmap= QPixmap("logo.png").scaled(55,55,Qt.KeepAspectRatio,Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setFixedSize(55,55)

        #Title text
        title_label=QLabel("Computer Science Department Chatbot")
        title_label.setStyleSheet("color:white;font-size:22px;font-weight:bold;")
        title_label.setAlignment(Qt.AlignVCenter)
        
        #Add both to layout
        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        layout.addWidget(header_widget)

        # Chat area
        self.chat_area = QScrollArea()
        self.chat_area.setWidgetResizable(True)
        self.chat_area_widget = QWidget()
        self.chat_area_layout = QVBoxLayout(self.chat_area_widget)
        self.chat_area.setWidget(self.chat_area_widget)
        self.chat_area.setStyleSheet("background-color:; color:#000;padding:10px 15px;border-radius:15px;margin:8px;")
        layout.addWidget(self.chat_area)
        
        # Quick questions
        quick_questions_group = QGroupBox("Quick Questions")
        quick_questions_layout = QHBoxLayout(quick_questions_group)
        quick_questions_group.setStyleSheet("""
            QGroupBox{
                font-size:20px;
                font-weight:bold;
                padding:8px;
                border:1px solid black;
                border-radius:10px;
                margin-top:10px;
            }
        """)
        
        self.quick_question_combo = QComboBox()
        self.quick_question_combo.setMinimumHeight(50)
        self.quick_question_combo.setMinimumWidth(800)
        self.quick_question_combo.setStyleSheet("""
            QComboBox{
                    font-size:20px;
                    padding:10px 15px;
                    border-radius:10px;
                    border:1px solid #999;
                    background-color:#e6f0ff;
                    color:#1e3c72;
                    font-weight:bold;                           
                }
                QComboBox::drop-down{
                        width:30px;                        
                }                                
            """)
        self.quick_question_combo.addItem("Select a common question...")
        
        # Add questions from all categories
        for category, data in self.faq_data.items():
            for question in data["questions"]:
                self.quick_question_combo.addItem(question)
        
        quick_questions_layout.addWidget(self.quick_question_combo)
        
        ask_button = QPushButton("Ask This")
        ask_button.clicked.connect(self.ask_quick_question)
        ask_button.setMinimumHeight(50)
        ask_button.setMinimumWidth(80)
        ask_button.setStyleSheet("""
            QPushButton{
                background-color:#0052CC;
                color: white;
                font-size:22px;
                font-weight:bold;
                border-radius:10px;
                padding:10px 25px;
                border:none;
            }
            QPushButton:hover{
                background-color:#003E99;
            }
        """)
        quick_questions_layout.addWidget(ask_button,stretch=1)
        
        layout.addWidget(quick_questions_group)
        
        # Input area
        input_frame = QFrame()
        input_layout = QHBoxLayout(input_frame)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your question about the CS department...")
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        send_button.setStyleSheet("background-color: #007bff; color: white; font-weight: bold;")
        input_layout.addWidget(send_button)
        
        
        layout.addWidget(input_frame)
        
        # Add welcome message
        self.add_bot_message("Hello! I'm the CS Department FAQ chatbot. I can answer questions about admissions, courses, faculty, and career opportunities. How can I help you today?")
        self.setStyleSheet("color:black;font-size:22px;font-weight:bold;")
    
    def ask_quick_question(self):
        question = self.quick_question_combo.currentText()
        if question != "Select a common question...":
            self.add_user_message(question)
            self.process_message(question)
            self.quick_question_combo.setCurrentIndex(0)
    
    def send_message(self):
        message = self.input_field.text().strip()
        if message:
            self.add_user_message(message)
            self.input_field.clear()
            self.process_message(message)
    
    def add_user_message(self, text):
        message_widget = MessageWidget(text, is_user=True)
        self.chat_area_layout.addWidget(message_widget)
        self.scroll_to_bottom()
    
    def add_bot_message(self, text):
        # Simulate typing delay for more natural interaction
        QTimer.singleShot(500, lambda: self._add_bot_message_delayed(text))
    
    def _add_bot_message_delayed(self, text):
        message_widget = MessageWidget(text, is_user=False)
        self.chat_area_layout.addWidget(message_widget)
        self.scroll_to_bottom()
    
    def scroll_to_bottom(self):
        scrollbar = self.chat_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def process_message(self, message):
        """Process the user message and generate a response"""
        message_lower = message.lower()
        
        # Check for greeting
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            self.add_bot_message("Hello! How can I help you with Computer Science department information today?")
            return
        
        # Check for specific FAQ categories
        response = None
        if any(word in message_lower for word in ['admission','apply','office','application', 'gpa', 'deadline']):
            response = self.faq_data["admission"]["aswers"]["default"]
        elif any(word in message_lower for word in ['course', 'class', 'programming','languages' ,'python', 'java']):
            response = self.faq_data["courses"]["answers"]["default"]
        elif any(word in message_lower for word in ['computer science', 'Department', 'cabin', 'block']):
            response = self.faq_data["Department"]["answers"]["default"]
        elif any(word in message_lower for word in['Department','many','college','CSE']):
            response=self.faq_data["college"]["answers"]["default"]
        elif any(word in message_lower for word in ['job', 'career', 'salary', 'hire', 'placement']):
            response = self.faq_data["careers"]["answers"]["default"]
        elif any(word in message_lower for word in ['thank', 'thanks', 'appreciate']):
            response = "You're welcome! Is there anything else you'd like to know about our Computer Science department?"
        
        if response:
            self.add_bot_message(response)
        else:
            self.add_bot_message(
                "I'm sorry,I don't have an answer for that."
                "Please ask something related to the CS Departmet."
            )
    

    def closeEvent(self, event):
        """Save chat history when closing"""
        try:
            chat_history = []
            for i in range(self.chat_area_layout.count()):
                widget = self.chat_area_layout.itemAt(i).widget()
                if isinstance(widget, MessageWidget):
                    chat_history.append({
                        "text": widget.findChild(QLabel).text(),
                        "is_user": widget.is_user,
                        "timestamp": widget.timestamp
                    })
            
            with open("chat_history.json", "w") as f:
                json.dump(chat_history, f)
                
        except Exception as e:
            print(f"Error saving chat history: {e}")
        
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    window = ChatBot()
    window.show()
    
    sys.exit(app.exec_())
