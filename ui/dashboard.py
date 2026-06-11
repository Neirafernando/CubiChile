from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QLineEdit, QTextEdit,
    QDialog, QDialogButtonBox, QFormLayout
)

from database import create_project, get_projects


class NewProjectDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Nuevo Proyecto")
        self.setMinimumWidth(420)

        layout = QVBoxLayout()

        title = QLabel("Crear nuevo proyecto")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")

        self.name = QLineEdit()
        self.name.setPlaceholderText("Ej: Vivienda Los Robles")

        self.client = QLineEdit()
        self.client.setPlaceholderText("Ej: Juan Pérez")

        self.location = QLineEdit()
        self.location.setPlaceholderText("Ej: Rancagua, Chile")

        self.description = QTextEdit()
        self.description.setPlaceholderText("Descripción breve del proyecto")
        self.description.setFixedHeight(90)

        form = QFormLayout()
        form.addRow("Proyecto", self.name)
        form.addRow("Cliente", self.client)
        form.addRow("Ubicación", self.location)
        form.addRow("Descripción", self.description)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(title)
        layout.addLayout(form)
        layout.addWidget(buttons)

        self.setLayout(layout)

        self.setStyleSheet("""
            QDialog {
                background-color: #0F172A;
            }

            QLabel {
                color: #E2E8F0;
            }

            QLineEdit, QTextEdit {
                background-color: #020617;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 10px;
                color: white;
            }

            QPushButton {
                background-color: #2563EB;
                color: white;
                border-radius: 8px;
                padding: 8px 14px;
            }
        """)

    def get_data(self):
        return {
            "name": self.name.text().strip(),
            "client": self.client.text().strip(),
            "location": self.location.text().strip(),
            "description": self.description.toPlainText().strip()
        }


class Dashboard(QWidget):
    def __init__(self, open_project_callback=None):
        super().__init__()

        self.open_project_callback = open_project_callback

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(34, 30, 34, 30)
        self.layout.setSpacing(22)

        self.build_ui()

        self.setLayout(self.layout)
        self.setStyleSheet("background-color: #0F172A;")

    def build_ui(self):
        self.build_header()
        self.build_stats()
        self.build_projects()
        self.layout.addStretch()

    def build_header(self):
        row = QHBoxLayout()

        texts = QVBoxLayout()

        title = QLabel("Dashboard")
        title.setStyleSheet("font-size: 30px; font-weight: bold; color: white;")

        subtitle = QLabel("Gestiona proyectos, cubicaciones, presupuestos e informes técnicos.")
        subtitle.setStyleSheet("font-size: 14px; color: #94A3B8;")

        texts.addWidget(title)
        texts.addWidget(subtitle)

        btn = QPushButton("+ Nuevo Proyecto")
        btn.setObjectName("primaryButton")
        btn.setFixedWidth(180)
        btn.setFixedHeight(44)
        btn.clicked.connect(self.open_new_project_dialog)

        row.addLayout(texts)
        row.addStretch()
        row.addWidget(btn)

        self.layout.addLayout(row)

    def build_stats(self):
        row = QHBoxLayout()
        row.setSpacing(18)

        projects = get_projects()
        total = len(projects)

        cards = [
            ("Proyectos", str(total), "Proyectos registrados"),
            ("Cubicaciones", "0", "Partidas calculadas"),
            ("Presupuesto", "$0", "Total estimado"),
        ]

        for title, value, detail in cards:
            card = QFrame()
            card.setObjectName("card")
            card.setFixedHeight(120)

            card_layout = QVBoxLayout()
            card_layout.setContentsMargins(18, 16, 18, 16)

            lbl_title = QLabel(title)
            lbl_title.setStyleSheet("color: #94A3B8; font-size: 13px;")

            lbl_value = QLabel(value)
            lbl_value.setStyleSheet("color: white; font-size: 30px; font-weight: bold;")

            lbl_detail = QLabel(detail)
            lbl_detail.setStyleSheet("color: #64748B; font-size: 12px;")

            card_layout.addWidget(lbl_title)
            card_layout.addWidget(lbl_value)
            card_layout.addWidget(lbl_detail)

            card.setLayout(card_layout)
            row.addWidget(card)

        self.layout.addLayout(row)

    def build_projects(self):
        title = QLabel("Proyectos recientes")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        self.layout.addWidget(title)

        self.projects_container = QVBoxLayout()
        self.layout.addLayout(self.projects_container)

        self.refresh_projects()

    def refresh_projects(self):
        while self.projects_container.count():
            item = self.projects_container.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        projects = get_projects()

        if not projects:
            empty = QLabel("Aún no hay proyectos. Crea el primero para comenzar.")
            empty.setStyleSheet("color: #64748B; font-size: 14px;")
            self.projects_container.addWidget(empty)
            return

        for project in projects:
            project_id, name, client, location, created_at = project

            card = QFrame()
            card.setObjectName("card")
            card.setFixedHeight(82)

            row = QHBoxLayout()
            row.setContentsMargins(18, 12, 18, 12)

            info = QVBoxLayout()

            lbl_name = QLabel(name)
            lbl_name.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")

            lbl_detail = QLabel(f"{client or 'Sin cliente'} · {location or 'Sin ubicación'} · {created_at}")
            lbl_detail.setStyleSheet("font-size: 12px; color: #94A3B8;")

            info.addWidget(lbl_name)
            info.addWidget(lbl_detail)

            btn_open = QPushButton("Abrir")
            btn_open.setFixedWidth(90)
            btn_open.setObjectName("primaryButton")
            btn_open.clicked.connect(lambda checked=False, p=project: self.open_project(p))

            row.addLayout(info)
            row.addStretch()
            row.addWidget(btn_open)

            card.setLayout(row)
            self.projects_container.addWidget(card)

    def open_project(self, project):
        if self.open_project_callback:
            self.open_project_callback(project)

    def open_new_project_dialog(self):
        dialog = NewProjectDialog()

        if dialog.exec():
            data = dialog.get_data()

            if not data["name"]:
                return

            create_project(
                data["name"],
                data["client"],
                data["location"],
                data["description"]
            )

            self.rebuild_dashboard()

    def rebuild_dashboard(self):
        while self.layout.count():
            item = self.layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

            elif item.layout():
                self.clear_layout(item.layout())

        self.build_ui()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

            elif item.layout():
                self.clear_layout(item.layout())
