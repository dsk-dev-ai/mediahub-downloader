def get_dark_theme():
    return """
    QWidget {
        background-color: #0b0f19;
        color: #e5e7eb;
        font-family: Segoe UI;
    }

    QWidget#sidebar {
        background-color: #111827;
    }

    QPushButton {
        background: transparent;
        border: none;
        padding: 12px;
        border-radius: 10px;
        text-align: left;
    }

    QPushButton:hover {
        background-color: #1f2937;
    }

    QPushButton:checked {
        background-color: #22c55e;
        color: black;
    }

    QLineEdit, QComboBox, QTextEdit {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 10px;
        padding: 10px;
    }

    QPushButton#primary {
        background-color: #22c55e;
        color: black;
        font-weight: bold;
    }

    QPushButton#primary:hover {
        background-color: #16a34a;
    }

    QFrame#card {
        background-color: #111827;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #1f2937;
    }

    QProgressBar {
        background: #111827;
        border-radius: 6px;
        height: 10px;
    }

    QProgressBar::chunk {
        background-color: #22c55e;
    }
    """