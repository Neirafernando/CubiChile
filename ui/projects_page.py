from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame
)

from database import get_projects, create_project
from ui.dashboard import NewProjectDialog


class ProjectsPage(QWidget):
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
        self.build_projects_list()
        self.layout.addStretch()

    def build_header(self):
        row = QHBoxLayout()

        texts = QVBoxLayout()

        title = QLabel("Proyectos")
        title.setStyleSheet("font-size: 30px; font-weight: bold; color: white;")

        subtitle = QLabel("Lista completa de proyectos creados en CubiChile.")
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

    def build_projects_list(self):
        title = QLabel("Todos los proyectos")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        self.layout.addWidget(title)

        self.projects_container = QVBoxLayout()
        self.projects_container.setSpacing(12)
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
            empty = QLabel("Aún no hay proyectos creados.")
            empty.setStyleSheet("color: #64748B; font-size: 14px;")
            self.projects_container.addWidget(empty)
            return

        for project in projects:
            project_id, name, client, location, created_at = project

            card = QFrame()
            card.setObjectName("card")
            card.setFixedHeight(86)

            row = QHBoxLayout()
            row.setContentsMargins(18, 12, 18, 12)

            info = QVBoxLayout()

            lbl_name = QLabel(name)
            lbl_name.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")

            lbl_detail = QLabel(
                f"{client or 'Sin cliente'} · {location or 'Sin ubicación'} · {created_at}"
            )
            lbl_detail.setStyleSheet("font-size: 12px; color: #94A3B8;")

            info.addWidget(lbl_name)
            info.addWidget(lbl_detail)

            btn_open = QPushButton("Abrir")
            btn_open.setObjectName("primaryButton")
            btn_open.setFixedWidth(100)
            btn_open.setFixedHeight(40)
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

            self.rebuild_page()

    def rebuild_page(self):
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
