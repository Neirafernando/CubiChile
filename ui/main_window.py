from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QStackedWidget, QFrame
)

from ui.dashboard import Dashboard
from ui.projects_page import ProjectsPage
from ui.project_view import ProjectView


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(34, 30, 34, 30)
        layout.setSpacing(18)

        title = QLabel("Ajustes")
        title.setStyleSheet("font-size: 30px; font-weight: bold; color: white;")

        subtitle = QLabel("Configuración general de CubiChile.")
        subtitle.setStyleSheet("font-size: 14px; color: #94A3B8;")

        card = QFrame()
        card.setObjectName("card")

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(22, 22, 22, 22)
        card_layout.setSpacing(10)

        card_title = QLabel("Aplicación")
        card_title.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")

        card_text = QLabel(
            "Versión MVP de CubiChile. Más adelante aquí podemos agregar logo, empresa, moneda, tema visual y datos del usuario."
        )
        card_text.setWordWrap(True)
        card_text.setStyleSheet("font-size: 14px; color: #94A3B8;")

        card_layout.addWidget(card_title)
        card_layout.addWidget(card_text)

        card.setLayout(card_layout)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(card)
        layout.addStretch()

        self.setLayout(layout)
        self.setStyleSheet("background-color: #0F172A;")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CubiChile")
        self.setMinimumSize(1200, 800)

        self.root = QWidget()
        self.setCentralWidget(self.root)

        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.sidebar = self.build_sidebar()

        self.stack = QStackedWidget()

        self.dashboard = Dashboard(open_project_callback=self.open_project)
        self.projects_page = ProjectsPage(open_project_callback=self.open_project)
        self.settings_page = SettingsPage()

        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.projects_page)
        self.stack.addWidget(self.settings_page)

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.stack)

        self.root.setLayout(self.main_layout)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #0F172A;
            }

            QWidget {
                font-family: Arial;
            }

            QLabel {
                color: #F8FAFC;
            }

            QPushButton {
                background-color: #111827;
                color: #E2E8F0;
                border: 1px solid #334155;
                border-radius: 10px;
                padding: 10px 16px;
                font-size: 14px;
                font-weight: 600;
                text-align: center;
            }

            QPushButton:hover {
                background-color: #1E293B;
                border: 1px solid #475569;
                color: white;
            }

            QPushButton:pressed {
                background-color: #2563EB;
                border: 1px solid #3B82F6;
            }

            QPushButton#primaryButton {
                background-color: #2563EB;
                color: white;
                border: 1px solid #3B82F6;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
                text-align: center;
            }

            QPushButton#primaryButton:hover {
                background-color: #1D4ED8;
                border: 1px solid #60A5FA;
            }

            QPushButton#sidebarButton {
                background-color: transparent;
                color: #CBD5E1;
                border: 1px solid transparent;
                border-radius: 10px;
                padding: 11px 14px;
                text-align: left;
                font-size: 14px;
                font-weight: 500;
            }

            QPushButton#sidebarButton:hover {
                background-color: #111827;
                border: 1px solid #1E293B;
                color: white;
            }

            QPushButton#sidebarButtonActive {
                background-color: #111827;
                color: white;
                border: 1px solid #2563EB;
                border-radius: 10px;
                padding: 11px 14px;
                text-align: left;
                font-size: 14px;
                font-weight: 700;
            }

            QPushButton#tabButton {
                background-color: #111827;
                color: #CBD5E1;
                border: 1px solid #334155;
                border-radius: 10px;
                padding: 10px 18px;
                text-align: center;
                font-size: 14px;
                font-weight: 600;
            }

            QPushButton#tabButton:hover {
                background-color: #1E293B;
                color: white;
                border: 1px solid #475569;
            }

            QLineEdit, QTextEdit {
                background-color: #020617;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 10px;
                color: white;
                font-size: 14px;
            }

            QFrame#card {
                background-color: #111827;
                border: 1px solid #1F2937;
                border-radius: 16px;
            }
        """)

        self.set_active_sidebar(self.btn_dashboard)

    def build_sidebar(self):
        sidebar = QWidget()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet("background-color: #020617;")

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 22, 18, 18)
        layout.setSpacing(10)

        logo = QLabel("CubiChile")
        logo.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: white;
            margin-bottom: 8px;
        """)

        subtitle = QLabel("Gestión de proyectos")
        subtitle.setStyleSheet("""
            color: #64748B;
            font-size: 12px;
            margin-bottom: 18px;
        """)

        section_general = QLabel("GENERAL")
        section_general.setStyleSheet("""
            color: #475569;
            font-size: 11px;
            font-weight: bold;
            margin-top: 10px;
            margin-bottom: 4px;
        """)

        self.btn_dashboard = QPushButton("▣  Inicio")
        self.btn_dashboard.setObjectName("sidebarButton")
        self.btn_dashboard.clicked.connect(self.show_dashboard)

        self.btn_projects = QPushButton("▤  Proyectos")
        self.btn_projects.setObjectName("sidebarButton")
        self.btn_projects.clicked.connect(self.show_projects)

        layout.addWidget(logo)
        layout.addWidget(subtitle)
        layout.addWidget(section_general)
        layout.addWidget(self.btn_dashboard)
        layout.addWidget(self.btn_projects)

        layout.addStretch()

        section_system = QLabel("SISTEMA")
        section_system.setStyleSheet("""
            color: #475569;
            font-size: 11px;
            font-weight: bold;
            margin-bottom: 4px;
        """)

        self.btn_config = QPushButton("⚙  Ajustes")
        self.btn_config.setObjectName("sidebarButton")
        self.btn_config.clicked.connect(self.show_settings)

        layout.addWidget(section_system)
        layout.addWidget(self.btn_config)

        sidebar.setLayout(layout)
        return sidebar

    def set_active_sidebar(self, active_btn):
        for btn in [self.btn_dashboard, self.btn_projects, self.btn_config]:
            btn.setObjectName("sidebarButton")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        active_btn.setObjectName("sidebarButtonActive")
        active_btn.style().unpolish(active_btn)
        active_btn.style().polish(active_btn)

    def show_dashboard(self):
        self.dashboard.rebuild_dashboard()
        self.stack.setCurrentWidget(self.dashboard)
        self.set_active_sidebar(self.btn_dashboard)

    def show_projects(self):
        self.projects_page.rebuild_page()
        self.stack.setCurrentWidget(self.projects_page)
        self.set_active_sidebar(self.btn_projects)

    def show_settings(self):
        self.stack.setCurrentWidget(self.settings_page)
        self.set_active_sidebar(self.btn_config)

    def open_project(self, project):
        project_view = ProjectView(project)
        self.stack.addWidget(project_view)
        self.stack.setCurrentWidget(project_view)

        for btn in [self.btn_dashboard, self.btn_projects, self.btn_config]:
            btn.setObjectName("sidebarButton")
            btn.style().unpolish(btn)
            btn.style().polish(btn)
