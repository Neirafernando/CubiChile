from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QComboBox, QStackedWidget,
    QMessageBox, QDialog, QLineEdit, QTextEdit,
    QDialogButtonBox, QFormLayout, QFileDialog, QScrollArea, QScrollArea,
    QGridLayout
)

from calculations import calcular_radier
from calc_rules import CUBICACION_RULES, get_rule, calculate_result
from database import (
    create_cubicacion,
    get_cubicaciones_by_project,
    get_project_totals,
    get_project_by_id,
    update_project,
    delete_cubicacion,
    update_cubicacion_price,
    update_cubicacion_dimensions,
    get_presupuesto_by_project,
    get_budget_total
)

from excel_export import export_presupuesto_excel
from pdf_export import export_presupuesto_pdf, export_informe_completo_pdf


def format_clp(value):
    try:
        return "$" + f"{float(value):,.0f}".replace(",", ".")
    except Exception:
        return "$0"


def unidad_visible(unidad):
    unidades = {
        "m2": "m²",
        "m3": "m³",
        "kg": "kg",
        "ml": "ml",
        "un": "un"
    }
    return unidades.get(unidad, unidad or "")


class EditProjectDialog(QDialog):
    def __init__(self, project_full):
        super().__init__()

        project_id, name, client, location, description, created_at = project_full

        self.setWindowTitle("Editar Proyecto")
        self.setMinimumWidth(460)

        layout = QVBoxLayout()

        title = QLabel("Editar proyecto")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")

        self.name = QLineEdit(name or "")
        self.client = QLineEdit(client or "")
        self.location = QLineEdit(location or "")

        self.description = QTextEdit()
        self.description.setText(description or "")
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
            QDialog { background-color: #0F172A; }
            QLabel { color: #E2E8F0; }
            QLineEdit, QTextEdit {
                background-color: #020617;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 10px;
                color: white;
                font-size: 14px;
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


class EditCubicacionDialog(QDialog):
    def __init__(self, cubicacion):
        super().__init__()

        (
            self.cub_id,
            self.tipo,
            self.largo,
            self.ancho,
            self.espesor,
            self.volumen,
            self.unidad,
            self.criterio,
            self.norma,
            self.created_at
        ) = cubicacion

        self.setWindowTitle("Editar partida")
        self.setMinimumWidth(460)

        layout = QVBoxLayout()

        title = QLabel("Editar partida guardada")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")

        subtitle = QLabel(self.tipo)
        subtitle.setStyleSheet("font-size: 13px; color: #94A3B8;")

        self.input_largo = QLineEdit(str(self.largo).replace(".", ","))
        self.input_ancho = QLineEdit(str(self.ancho).replace(".", ","))
        self.input_espesor = QLineEdit(str(self.espesor).replace(".", ","))

        self.resultado = QLabel("")
        self.resultado.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")

        for campo in [self.input_largo, self.input_ancho, self.input_espesor]:
            campo.setFixedHeight(44)
            campo.textChanged.connect(self.actualizar_resultado)

        form = QFormLayout()
        form.addRow("Largo (m)", self.input_largo)
        form.addRow("Ancho / Alto (m)", self.input_ancho)

        if self.unidad not in ["m2", "ml", "un", "kg"]:
            form.addRow("Espesor / Profundidad (m)", self.input_espesor)
        elif self.unidad == "kg":
            form.addRow("Peso kg/m", self.input_espesor)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(10)
        layout.addLayout(form)
        layout.addWidget(self.resultado)
        layout.addWidget(buttons)

        self.setLayout(layout)

        self.setStyleSheet("""
            QDialog { background-color: #0F172A; }
            QLabel { color: #E2E8F0; }
            QLineEdit {
                background-color: #020617;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 10px;
                color: white;
                font-size: 14px;
            }
            QPushButton {
                background-color: #2563EB;
                color: white;
                border-radius: 8px;
                padding: 8px 14px;
            }
        """)

        self.actualizar_resultado()

    def leer_datos(self):
        try:
            largo = float(self.input_largo.text().replace(",", "."))
            ancho = float(self.input_ancho.text().replace(",", "."))

            if self.unidad in ["m2", "ml", "un"]:
                espesor = 1
            else:
                espesor = float(self.input_espesor.text().replace(",", "."))

            if largo <= 0 or ancho <= 0 or espesor <= 0:
                return None

            resultado = calcular_radier(largo, ancho, espesor)
            return largo, ancho, espesor, resultado

        except ValueError:
            return None

    def actualizar_resultado(self):
        datos = self.leer_datos()

        if not datos:
            self.resultado.setText(f"Resultado: 0.00 {unidad_visible(self.unidad)}")
            return

        largo, ancho, espesor, resultado = datos
        self.resultado.setText(f"Resultado: {resultado:.2f} {unidad_visible(self.unidad)}")

    def get_data(self):
        return self.leer_datos()


class ProjectView(QWidget):
    def __init__(self, project):
        super().__init__()

        self.project_id = project[0]
        self.current_tipo_cubicacion = "Radier / Losa"

        self.load_project_data()

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(34, 30, 34, 30)
        self.main_layout.setSpacing(22)

        self.build_header()
        self.build_tabs()
        self.build_content()

        self.setLayout(self.main_layout)
        self.setStyleSheet("background-color: #0F172A;")

    def load_project_data(self):
        project = get_project_by_id(self.project_id)
        self.project_full = project

        (
            self.project_id,
            self.name,
            self.client,
            self.location,
            self.description,
            self.created_at
        ) = project

    def build_header(self):
        header = QHBoxLayout()

        title_box = QVBoxLayout()

        self.title_label = QLabel(self.name)
        self.title_label.setStyleSheet("font-size: 30px; font-weight: bold; color: white;")

        self.subtitle_label = QLabel(f"{self.client or 'Sin cliente'} · {self.location or 'Sin ubicación'}")
        self.subtitle_label.setStyleSheet("font-size: 14px; color: #94A3B8;")

        title_box.addWidget(self.title_label)
        title_box.addWidget(self.subtitle_label)

        btn_edit = QPushButton("Editar proyecto")
        btn_edit.setObjectName("primaryButton")
        btn_edit.setFixedWidth(150)
        btn_edit.setFixedHeight(42)
        btn_edit.clicked.connect(self.open_edit_dialog)

        header.addLayout(title_box)
        header.addStretch()
        header.addWidget(btn_edit)

        self.main_layout.addLayout(header)

    def refresh_header(self):
        self.title_label.setText(self.name)
        self.subtitle_label.setText(f"{self.client or 'Sin cliente'} · {self.location or 'Sin ubicación'}")

    def open_edit_dialog(self):
        self.load_project_data()
        dialog = EditProjectDialog(self.project_full)

        if dialog.exec():
            data = dialog.get_data()

            if not data["name"]:
                QMessageBox.warning(self, "Datos incompletos", "El nombre del proyecto es obligatorio.")
                return

            update_project(
                self.project_id,
                data["name"],
                data["client"],
                data["location"],
                data["description"]
            )

            self.load_project_data()
            self.refresh_header()

    def build_tabs(self):
        tabs = QHBoxLayout()
        tabs.setSpacing(12)

        self.btn_resumen = QPushButton("Resumen")
        self.btn_cubicaciones = QPushButton("Cubicaciones")
        self.btn_partidas = QPushButton("Partidas guardadas")
        self.btn_presupuesto = QPushButton("Presupuesto")
        self.btn_informes = QPushButton("Informes")

        self.btn_resumen.clicked.connect(lambda: self.content_stack.setCurrentIndex(0))
        self.btn_cubicaciones.clicked.connect(lambda: self.content_stack.setCurrentIndex(1))
        self.btn_partidas.clicked.connect(self.show_partidas)
        self.btn_presupuesto.clicked.connect(self.show_presupuesto)
        self.btn_informes.clicked.connect(lambda: self.content_stack.setCurrentIndex(4))

        for btn in [
            self.btn_resumen,
            self.btn_cubicaciones,
            self.btn_partidas,
            self.btn_presupuesto,
            self.btn_informes
        ]:
            btn.setObjectName("tabButton")
            btn.setFixedHeight(42)
            btn.setMinimumWidth(120)
            tabs.addWidget(btn)

        tabs.addStretch()
        self.main_layout.addLayout(tabs)

    def show_partidas(self):
        self.refresh_cubicaciones()
        self.content_stack.setCurrentIndex(2)

    def show_presupuesto(self):
        self.refresh_presupuesto()
        self.content_stack.setCurrentIndex(3)

    def build_content(self):
        self.content_stack = QStackedWidget()

        self.summary_page = self.build_summary_page()
        self.cubicaciones_page = self.build_cubicaciones_page()
        self.partidas_page = self.build_partidas_page()
        self.presupuesto_page = self.build_presupuesto_page()
        self.informes_page = self.build_informes_page()

        self.content_stack.addWidget(self.summary_page)
        self.content_stack.addWidget(self.cubicaciones_page)
        self.content_stack.addWidget(self.partidas_page)
        self.content_stack.addWidget(self.presupuesto_page)
        self.content_stack.addWidget(self.informes_page)

        self.main_layout.addWidget(self.content_stack)

    def build_summary_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(18)

        self.summary_cards_layout = QHBoxLayout()
        self.summary_cards_layout.setSpacing(18)
        self.refresh_summary_cards()

        layout.addLayout(self.summary_cards_layout)

        info = QFrame()
        info.setObjectName("card")

        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(22, 22, 22, 22)

        title = QLabel("Resumen del proyecto")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")

        desc = self.description or "Sin descripción registrada."
        text = QLabel(desc)
        text.setStyleSheet("font-size: 14px; color: #94A3B8;")
        text.setWordWrap(True)

        info_layout.addWidget(title)
        info_layout.addWidget(text)

        info.setLayout(info_layout)
        layout.addWidget(info)

        layout.addStretch()
        page.setLayout(layout)
        return page

    def refresh_summary_cards(self):
        while self.summary_cards_layout.count():
            item = self.summary_cards_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        total_partidas, total_volumen = get_project_totals(self.project_id)
        total_presupuesto = get_budget_total(self.project_id)

        cards = [
            ("Partidas guardadas", str(total_partidas), "Cálculos registrados"),
            ("Cantidad total", f"{total_volumen:.2f}", "Suma referencial"),
            ("Presupuesto", format_clp(total_presupuesto), "Total estimado"),
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
            lbl_value.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")

            lbl_detail = QLabel(detail)
            lbl_detail.setStyleSheet("color: #64748B; font-size: 12px;")

            card_layout.addWidget(lbl_title)
            card_layout.addWidget(lbl_value)
            card_layout.addWidget(lbl_detail)

            card.setLayout(card_layout)
            self.summary_cards_layout.addWidget(card)

    def input_box(self, label_text, placeholder, default=""):
        box = QVBoxLayout()
        box.setSpacing(10)

        label = QLabel(label_text)
        label.setStyleSheet("color: #CBD5E1; font-size: 13px;")

        campo = QLineEdit()
        campo.setPlaceholderText(placeholder)
        campo.setText(default)
        campo.setFixedHeight(54)
        campo.setStyleSheet("""
            QLineEdit {
                background-color: #020617;
                color: white;
                border: 1px solid #475569;
                border-radius: 10px;
                padding: 12px 14px;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 2px solid #2563EB;
            }
        """)

        box.addWidget(label)
        box.addWidget(campo)

        return box, campo, label

    def build_cubicaciones_page(self):
        page = QWidget()

        layout = QVBoxLayout()
        layout.setContentsMargins(8, 14, 8, 8)
        layout.setSpacing(14)

        title = QLabel("Cubicaciones")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: white;
        """)

        subtitle = QLabel("Selecciona una partida e ingresa las medidas para calcular.")
        subtitle.setStyleSheet("""
            color: #94A3B8;
            font-size: 14px;
        """)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        card = QFrame()
        card.setObjectName("card")

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(26, 20, 26, 20)
        card_layout.setSpacing(12)

        # =========================
        # FILA 1: TIPO + NOMBRE
        # =========================
        top_row = QHBoxLayout()
        top_row.setSpacing(14)

        tipo_box = QVBoxLayout()
        tipo_box.setSpacing(6)

        tipo_label = QLabel("Tipo de partida")
        tipo_label.setStyleSheet("color: #CBD5E1; font-size: 13px; font-weight: bold;")

        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(list(CUBICACION_RULES.keys()))
        self.tipo_combo.setFixedHeight(44)
        self.tipo_combo.setMinimumWidth(320)
        self.tipo_combo.setStyleSheet("""
            QComboBox {
                background-color: #020617;
                color: white;
                border: 1px solid #334155;
                border-radius: 10px;
                padding: 8px 14px;
                font-size: 14px;
                font-weight: 600;
            }

            QComboBox:hover {
                border: 1px solid #3B82F6;
            }

            QComboBox::drop-down {
                border: none;
                width: 34px;
            }

            QAbstractItemView {
                background-color: #020617;
                color: white;
                border: 1px solid #334155;
                selection-background-color: #2563EB;
                padding: 6px;
            }
        """)

        tipo_box.addWidget(tipo_label)
        tipo_box.addWidget(self.tipo_combo)

        nombre_box = QVBoxLayout()
        nombre_box.setSpacing(6)

        nombre_label = QLabel("Nombre personalizado")
        nombre_label.setStyleSheet("color: #CBD5E1; font-size: 13px; font-weight: bold;")

        self.input_nombre_partida = QLineEdit()
        self.input_nombre_partida.setPlaceholderText("Ej: Radier terraza, Muro baño 1")
        self.input_nombre_partida.setFixedHeight(44)

        nombre_box.addWidget(nombre_label)
        nombre_box.addWidget(self.input_nombre_partida)

        top_row.addLayout(tipo_box, 1)
        top_row.addLayout(nombre_box, 2)

        # =========================
        # FILA 2: TÍTULO + FÓRMULA
        # =========================
        info_box = QFrame()
        info_box.setStyleSheet("""
            QFrame {
                background-color: #0B1220;
                border: 1px solid #1E293B;
                border-radius: 10px;
            }
        """)

        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(14, 10, 14, 10)
        info_layout.setSpacing(4)

        self.form_title = QLabel("Radier / Losa de hormigón")
        self.form_title.setStyleSheet("""
            font-size: 17px;
            font-weight: bold;
            color: white;
            border: none;
            background: transparent;
        """)

        self.formula_label = QLabel("Volumen = Largo × Ancho × Espesor")
        self.formula_label.setStyleSheet("""
            color: #94A3B8;
            font-size: 12px;
            border: none;
            background: transparent;
        """)

        info_layout.addWidget(self.form_title)
        info_layout.addWidget(self.formula_label)
        info_box.setLayout(info_layout)

        # =========================
        # FILA 3: MEDIDAS
        # =========================
        inputs_grid = QGridLayout()
        inputs_grid.setHorizontalSpacing(12)
        inputs_grid.setVerticalSpacing(6)

        self.label_largo = QLabel("Largo (m)")
        self.label_largo.setStyleSheet("color: #CBD5E1; font-size: 12px;")
        self.input_largo = QLineEdit()
        self.input_largo.setPlaceholderText("Ej: 10")
        self.input_largo.setFixedHeight(42)

        self.label_ancho = QLabel("Ancho (m)")
        self.label_ancho.setStyleSheet("color: #CBD5E1; font-size: 12px;")
        self.input_ancho = QLineEdit()
        self.input_ancho.setPlaceholderText("Ej: 5")
        self.input_ancho.setFixedHeight(42)

        self.label_espesor = QLabel("Espesor (m)")
        self.label_espesor.setStyleSheet("color: #CBD5E1; font-size: 12px;")
        self.input_espesor = QLineEdit()
        self.input_espesor.setPlaceholderText("Ej: 0.12")
        self.input_espesor.setFixedHeight(42)

        self.label_perdida = QLabel("Pérdida / recargo (%)")
        self.label_perdida.setStyleSheet("color: #CBD5E1; font-size: 12px;")
        self.input_perdida = QLineEdit()
        self.input_perdida.setPlaceholderText("Ej: 10")
        self.input_perdida.setFixedHeight(42)

        inputs_grid.addWidget(self.label_largo, 0, 0)
        inputs_grid.addWidget(self.label_ancho, 0, 1)
        inputs_grid.addWidget(self.label_espesor, 0, 2)
        inputs_grid.addWidget(self.label_perdida, 0, 3)

        inputs_grid.addWidget(self.input_largo, 1, 0)
        inputs_grid.addWidget(self.input_ancho, 1, 1)
        inputs_grid.addWidget(self.input_espesor, 1, 2)
        inputs_grid.addWidget(self.input_perdida, 1, 3)

        # =========================
        # FILA 4: OBSERVACIÓN
        # =========================
        obs_box = QVBoxLayout()
        obs_box.setSpacing(6)

        observacion_label = QLabel("Observación opcional")
        observacion_label.setStyleSheet("color: #CBD5E1; font-size: 12px;")

        self.input_observacion_partida = QLineEdit()
        self.input_observacion_partida.setPlaceholderText("Ej: Considera pérdida por cortes / revisar en obra")
        self.input_observacion_partida.setFixedHeight(42)

        obs_box.addWidget(observacion_label)
        obs_box.addWidget(self.input_observacion_partida)

        # =========================
        # FILA 5: RESULTADO + BOTÓN
        # =========================
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(14)

        result_box = QVBoxLayout()
        result_box.setSpacing(4)

        self.resultado_label = QLabel("Resultado: 0.00 m³")
        self.resultado_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: white;
        """)

        self.norma_label = QLabel(
            "Referencia técnica de apoyo. Verificar siempre contra planos y especificaciones del proyecto."
        )
        self.norma_label.setWordWrap(True)
        self.norma_label.setStyleSheet("""
            color: #64748B;
            font-size: 11px;
        """)

        result_box.addWidget(self.resultado_label)
        result_box.addWidget(self.norma_label)

        btn_guardar = QPushButton("Guardar partida")
        btn_guardar.setObjectName("primaryButton")
        btn_guardar.setFixedWidth(180)
        btn_guardar.setFixedHeight(44)
        btn_guardar.clicked.connect(self.guardar_radier)

        bottom_row.addLayout(result_box)
        bottom_row.addStretch()
        bottom_row.addWidget(btn_guardar)

        self.tipo_buttons = {}

        card_layout.addLayout(top_row)
        card_layout.addWidget(info_box)
        card_layout.addLayout(inputs_grid)
        card_layout.addLayout(obs_box)
        card_layout.addLayout(bottom_row)

        card.setLayout(card_layout)

        layout.addWidget(card)
        layout.addStretch()

        page.setLayout(layout)

        self.input_largo.textChanged.connect(self.actualizar_resultado_en_vivo)
        self.input_ancho.textChanged.connect(self.actualizar_resultado_en_vivo)
        self.input_espesor.textChanged.connect(self.actualizar_resultado_en_vivo)
        self.input_perdida.textChanged.connect(self.actualizar_resultado_en_vivo)

        self.tipo_combo.currentTextChanged.connect(self.seleccionar_tipo_cubicacion)
        self.seleccionar_tipo_cubicacion("Radier / Losa")

        return page


    def build_partidas_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(18)

        title = QLabel("Partidas guardadas")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")

        subtitle = QLabel("Listado de cubicaciones registradas en este proyecto.")
        subtitle.setStyleSheet("font-size: 14px; color: #94A3B8;")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        card = QFrame()
        card.setObjectName("card")

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.setSpacing(12)

        self.cubicaciones_list = QVBoxLayout()
        self.cubicaciones_list.setSpacing(10)

        card_layout.addLayout(self.cubicaciones_list)

        card.setLayout(card_layout)

        layout.addWidget(card)
        layout.addStretch()

        page.setLayout(layout)

        self.refresh_cubicaciones()
        return page

    def build_presupuesto_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(14)

        title = QLabel("Presupuesto")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")

        subtitle = QLabel("Asigna precios unitarios a las partidas guardadas y calcula el total del proyecto.")
        subtitle.setStyleSheet("font-size: 14px; color: #94A3B8;")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        top_row = QHBoxLayout()
        top_row.setSpacing(18)

        total_card = QFrame()
        total_card.setObjectName("card")
        total_card.setFixedHeight(96)

        total_layout = QVBoxLayout()
        total_layout.setContentsMargins(20, 12, 20, 12)

        total_label = QLabel("Total presupuesto")
        total_label.setStyleSheet("font-size: 13px; color: #94A3B8;")

        self.presupuesto_total_label = QLabel("$0")
        self.presupuesto_total_label.setStyleSheet("font-size: 30px; font-weight: bold; color: white;")

        total_layout.addWidget(total_label)
        total_layout.addWidget(self.presupuesto_total_label)

        total_card.setLayout(total_layout)

        export_card = QFrame()
        export_card.setObjectName("card")
        export_card.setFixedWidth(360)
        export_card.setFixedHeight(96)

        export_layout = QHBoxLayout()
        export_layout.setContentsMargins(18, 18, 18, 18)
        export_layout.setSpacing(12)

        btn_excel = QPushButton("Excel")
        btn_excel.setObjectName("primaryButton")
        btn_excel.setFixedHeight(42)
        btn_excel.clicked.connect(self.exportar_presupuesto_excel)

        btn_pdf = QPushButton("PDF")
        btn_pdf.setObjectName("primaryButton")
        btn_pdf.setFixedHeight(42)
        btn_pdf.clicked.connect(self.exportar_presupuesto_pdf)

        export_layout.addWidget(btn_excel)
        export_layout.addWidget(btn_pdf)

        export_card.setLayout(export_layout)

        top_row.addWidget(total_card, 1)
        top_row.addWidget(export_card)

        layout.addLayout(top_row)

        list_card = QFrame()
        list_card.setObjectName("card")

        list_layout = QVBoxLayout()
        list_layout.setContentsMargins(18, 16, 18, 16)
        list_layout.setSpacing(10)

        header = QHBoxLayout()
        header.setContentsMargins(12, 0, 12, 0)
        header.setSpacing(12)

        h_partida = QLabel("Partida")
        h_cantidad = QLabel("Cantidad")
        h_precio = QLabel("Precio unitario")
        h_total = QLabel("Total")

        for h in [h_partida, h_cantidad, h_precio, h_total]:
            h.setStyleSheet("font-size: 12px; color: #94A3B8; font-weight: bold;")

        h_cantidad.setFixedWidth(120)
        h_precio.setFixedWidth(250)
        h_total.setFixedWidth(150)

        header.addWidget(h_partida, 1)
        header.addWidget(h_cantidad)
        header.addWidget(h_precio)
        header.addWidget(h_total)

        list_layout.addLayout(header)

        self.presupuesto_scroll = QScrollArea()
        self.presupuesto_scroll.setWidgetResizable(True)
        self.presupuesto_scroll.setFrameShape(QFrame.NoFrame)
        self.presupuesto_scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }

            QScrollBar:vertical {
                background: #0F172A;
                width: 10px;
                margin: 0px;
            }

            QScrollBar::handle:vertical {
                background: #334155;
                border-radius: 5px;
            }

            QScrollBar::handle:vertical:hover {
                background: #475569;
            }
        """)

        self.presupuesto_scroll_widget = QWidget()
        self.presupuesto_scroll_widget.setStyleSheet("background: transparent;")

        self.presupuesto_list = QVBoxLayout()
        self.presupuesto_list.setContentsMargins(0, 0, 0, 0)
        self.presupuesto_list.setSpacing(8)

        self.presupuesto_scroll_widget.setLayout(self.presupuesto_list)
        self.presupuesto_scroll.setWidget(self.presupuesto_scroll_widget)

        list_layout.addWidget(self.presupuesto_scroll)

        list_card.setLayout(list_layout)

        layout.addWidget(list_card, 1)

        page.setLayout(layout)

        self.refresh_presupuesto()
        return page

    def build_informes_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(18)

        title = QLabel("Informes")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")

        subtitle = QLabel("Genera documentos técnicos del proyecto.")
        subtitle.setStyleSheet("font-size: 14px; color: #94A3B8;")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        card = QFrame()
        card.setObjectName("card")

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(22, 22, 22, 22)
        card_layout.setSpacing(14)

        card_title = QLabel("Informe completo")
        card_title.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")

        card_text = QLabel(
            "Exporta un PDF con datos del proyecto, cubicaciones, partidas guardadas y presupuesto."
        )
        card_text.setWordWrap(True)
        card_text.setStyleSheet("font-size: 13px; color: #94A3B8;")

        btn_pdf = QPushButton("Exportar informe completo PDF")
        btn_pdf.setObjectName("primaryButton")
        btn_pdf.setFixedHeight(44)
        btn_pdf.setFixedWidth(280)
        btn_pdf.clicked.connect(self.exportar_informe_completo_pdf)

        card_layout.addWidget(card_title)
        card_layout.addWidget(card_text)
        card_layout.addSpacing(8)
        card_layout.addWidget(btn_pdf)

        card.setLayout(card_layout)

        layout.addWidget(card)
        layout.addStretch()

        page.setLayout(layout)
        return page

    def exportar_informe_completo_pdf(self):
        default_name = f"{self.name}_informe_completo.pdf".replace(" ", "_")

        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar informe completo PDF",
            default_name,
            "Archivos PDF (*.pdf)"
        )

        if not filepath:
            return

        if not filepath.endswith(".pdf"):
            filepath += ".pdf"

        try:
            export_informe_completo_pdf(self.project_id, filepath)
            QMessageBox.information(
                self,
                "Exportación completada",
                f"Informe completo exportado correctamente:\n{filepath}"
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Error al exportar",
                f"No se pudo exportar el informe completo:\n{error}"
            )

    def seleccionar_tipo_cubicacion(self, tipo):
        self.current_tipo_cubicacion = tipo
        rule = get_rule(tipo)

        self.form_title.setText(rule["title"])
        self.formula_label.setText(rule["formula"])

        label_largo, label_ancho, label_espesor = rule["labels"]
        ph_largo, ph_ancho, ph_espesor = rule["placeholders"]

        self.label_largo.setText(label_largo)
        self.label_ancho.setText(label_ancho)
        self.label_espesor.setText(label_espesor)

        self.input_largo.setPlaceholderText(ph_largo)
        self.input_ancho.setPlaceholderText(ph_ancho)
        self.input_espesor.setPlaceholderText(ph_espesor)

        self.input_ancho.setVisible(rule["show_ancho"])
        self.label_ancho.setVisible(rule["show_ancho"])

        self.input_espesor.setVisible(rule["show_espesor"])
        self.label_espesor.setVisible(rule["show_espesor"])

        self.input_espesor.setText(rule["default_espesor"])
        self.input_perdida.setText(rule["default_perdida"])

        self.norma_label.setText(
            "Referencia técnica de apoyo. Verificar siempre contra planos y especificaciones del proyecto."
        )

        for nombre, boton in self.tipo_buttons.items():
            boton.setObjectName("primaryButton" if nombre == tipo else "")
            boton.style().unpolish(boton)
            boton.style().polish(boton)

        self.actualizar_resultado_en_vivo()

    def leer_medidas_radier(self, mostrar_error=True):
        rule = get_rule(self.current_tipo_cubicacion)

        try:
            largo_txt = self.input_largo.text().replace(",", ".").strip()
            ancho_txt = self.input_ancho.text().replace(",", ".").strip()
            espesor_txt = self.input_espesor.text().replace(",", ".").strip()
            perdida_txt = self.input_perdida.text().replace(",", ".").strip() or "0"

            largo = float(largo_txt)

            if rule["show_ancho"]:
                ancho = float(ancho_txt)
            else:
                ancho = 1

            if rule["show_espesor"]:
                espesor = float(espesor_txt)
            else:
                espesor = 1

            perdida = float(perdida_txt)

            if largo <= 0 or ancho <= 0 or espesor <= 0 or perdida < 0:
                raise ValueError

            base, resultado = calculate_result(
                self.current_tipo_cubicacion,
                largo,
                ancho,
                espesor,
                perdida
            )

            return largo, ancho, espesor, perdida, base, resultado

        except ValueError:
            if mostrar_error:
                QMessageBox.warning(
                    self,
                    "Datos inválidos",
                    "Revisa los campos. Ingresa solo números mayores que cero. Puedes usar punto o coma decimal."
                )
            return None

    def validar_medidas_absurdas(self, largo, ancho, espesor, perdida):
        avisos = []
        tipo = self.current_tipo_cubicacion
        rule = get_rule(tipo)

        if perdida > 30:
            avisos.append(f"El recargo/pérdida ingresado es {perdida:.1f}%, parece alto.")

        if rule["unit"] in ["m2", "m3", "ml"] and largo > 500:
            avisos.append(f"El largo ingresado ({largo:.2f} m) parece demasiado alto.")

        if rule["unit"] in ["m2", "m3"] and ancho > 500:
            avisos.append(f"El ancho/alto ingresado ({ancho:.2f} m) parece demasiado alto.")

        if tipo in ["Radier / Losa", "Radier con dosificación"] and espesor > 0.50:
            avisos.append(
                f"El espesor del radier/losa es {espesor:.2f} m. "
                "Para un radier común suele ser mucho menor. Revisa si querías escribir 0.10, 0.12 o 0.15."
            )

        if tipo == "Excavación" and espesor > 5:
            avisos.append(f"La profundidad ingresada ({espesor:.2f} m) parece alta.")

        if tipo in ["Hormigón fundaciones", "Sobrecimiento"] and espesor > 3:
            avisos.append(f"El alto/profundidad ingresado ({espesor:.2f} m) parece alto para esta partida.")

        if tipo == "Puertas y ventanas" and largo > 500:
            avisos.append(f"La cantidad de unidades ({largo:.0f}) parece alta.")

        if tipo == "Enfierradura / Acero kg" and ancho > 5000:
            avisos.append(f"La cantidad de barras/tramos ({ancho:.0f}) parece alta.")

        if not avisos:
            return True

        mensaje = "CubiChile detectó valores poco comunes:\n\n"
        mensaje += "\n".join(f"• {a}" for a in avisos)
        mensaje += "\n\n¿Deseas guardar de todas formas?"

        respuesta = QMessageBox.question(
            self,
            "Revisar medidas",
            mensaje,
            QMessageBox.Yes | QMessageBox.No
        )

        return respuesta == QMessageBox.Yes

    def actualizar_resultado_en_vivo(self):
        rule = get_rule(self.current_tipo_cubicacion)
        unidad = unidad_visible(rule["unit"])

        datos = self.leer_medidas_radier(mostrar_error=False)

        if not datos:
            self.resultado_label.setText(f"Resultado: 0.00 {unidad}")
            return

        largo, ancho, espesor, perdida, base, resultado = datos

        if perdida > 0:
            self.resultado_label.setText(
                f"Resultado: {resultado:.2f} {unidad}  |  Base: {base:.2f} + {perdida:.1f}%"
            )
        else:
            self.resultado_label.setText(f"Resultado: {resultado:.2f} {unidad}")

    def calcular_radier_ui(self):
        datos = self.leer_medidas_radier()

        if not datos:
            return 0

        self.actualizar_resultado_en_vivo()
        return datos[-1]

    def guardar_radier(self):
        datos = self.leer_medidas_radier()

        if not datos:
            return

        largo, ancho, espesor, perdida, base, volumen = datos

        if not self.validar_medidas_absurdas(largo, ancho, espesor, perdida):
            return

        rule = get_rule(self.current_tipo_cubicacion)

        nombre_personalizado = self.input_nombre_partida.text().strip()
        observacion = self.input_observacion_partida.text().strip()

        tipo_base = rule["tipo_guardado"]
        tipo_guardado = nombre_personalizado if nombre_personalizado else tipo_base

        criterio = f"{rule['criterio']} Recargo/pérdida aplicada: {perdida:.1f}%. Tipo base: {tipo_base}."

        if observacion:
            criterio += f" Observación: {observacion}"

        norma = "Referencia técnica de apoyo. Verificar contra planos y especificaciones."

        create_cubicacion(
            self.project_id,
            tipo_guardado,
            largo,
            ancho,
            espesor,
            volumen,
            criterio,
            norma,
            rule["unit"]
        )

        self.input_nombre_partida.clear()
        self.input_observacion_partida.clear()

        self.actualizar_resultado_en_vivo()
        self.refresh_summary_cards()
        self.refresh_cubicaciones()
        self.refresh_presupuesto()

        QMessageBox.information(
            self,
            "Partida guardada",
            "La partida fue guardada correctamente."
        )

    def editar_partida(self, cubicacion):
        dialog = EditCubicacionDialog(cubicacion)

        if dialog.exec():
            data = dialog.get_data()

            if not data:
                QMessageBox.warning(
                    self,
                    "Datos inválidos",
                    "Ingresa medidas válidas mayores a cero."
                )
                return

            largo, ancho, espesor, volumen = data

            update_cubicacion_dimensions(
                cubicacion[0],
                largo,
                ancho,
                espesor,
                volumen
            )

            self.refresh_cubicaciones()
            self.refresh_presupuesto()
            self.refresh_summary_cards()

            QMessageBox.information(self, "Actualizado", "Partida actualizada correctamente.")

    def eliminar_partida(self, cubicacion_id):
        respuesta = QMessageBox.question(
            self,
            "Eliminar partida",
            "¿Seguro que quieres eliminar esta partida guardada?",
            QMessageBox.Yes | QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:
            delete_cubicacion(cubicacion_id)
            self.refresh_cubicaciones()
            self.refresh_presupuesto()
            self.refresh_summary_cards()

    def refresh_cubicaciones(self):
        if not hasattr(self, "cubicaciones_list"):
            return

        while self.cubicaciones_list.count():
            item = self.cubicaciones_list.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        cubicaciones = get_cubicaciones_by_project(self.project_id)

        if not cubicaciones:
            empty = QLabel("Aún no hay partidas guardadas para este proyecto.")
            empty.setStyleSheet("color: #64748B; font-size: 14px;")
            self.cubicaciones_list.addWidget(empty)
            return

        for cub in cubicaciones:
            cub_id, tipo, largo, ancho, espesor, volumen, unidad, criterio, norma, created_at = cub
            unidad_txt = unidad_visible(unidad)

            item = QFrame()
            item.setObjectName("card")
            item.setFixedHeight(104)

            row = QHBoxLayout()
            row.setContentsMargins(18, 12, 18, 12)

            info = QVBoxLayout()

            lbl_tipo = QLabel(tipo)
            lbl_tipo.setStyleSheet("font-size: 15px; font-weight: bold; color: white;")

            if unidad == "m2":
                detalle = f"{largo:.2f} m × {ancho:.2f} m · {created_at}"
            else:
                detalle = f"{largo:.2f} m × {ancho:.2f} m × {espesor:.2f} m · {created_at}"

            lbl_detail = QLabel(detalle)
            lbl_detail.setStyleSheet("font-size: 12px; color: #94A3B8;")

            lbl_norma = QLabel(criterio or norma or "")
            lbl_norma.setStyleSheet("font-size: 11px; color: #64748B;")
            lbl_norma.setWordWrap(True)

            info.addWidget(lbl_tipo)
            info.addWidget(lbl_detail)
            info.addWidget(lbl_norma)

            result = QLabel(f"{volumen:.2f} {unidad_txt}")
            result.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")

            btn_edit = QPushButton("Editar")
            btn_edit.setFixedWidth(90)
            btn_edit.setFixedHeight(36)
            btn_edit.setObjectName("primaryButton")
            btn_edit.clicked.connect(lambda checked=False, c=cub: self.editar_partida(c))

            btn_delete = QPushButton("Eliminar")
            btn_delete.setFixedWidth(100)
            btn_delete.setFixedHeight(36)
            btn_delete.setStyleSheet("""
                QPushButton {
                    background-color: #7F1D1D;
                    color: white;
                    border-radius: 8px;
                    font-weight: bold;
                    text-align: center;
                }
                QPushButton:hover {
                    background-color: #991B1B;
                }
            """)
            btn_delete.clicked.connect(lambda checked=False, cid=cub_id: self.eliminar_partida(cid))

            row.addLayout(info)
            row.addStretch()
            row.addWidget(result)
            row.addWidget(btn_edit)
            row.addWidget(btn_delete)

            item.setLayout(row)
            self.cubicaciones_list.addWidget(item)

    def guardar_precio_partida(self, cubicacion_id, precio_input):
        try:
            txt = precio_input.text().strip()
            txt = txt.replace("$", "").replace(".", "").replace(",", ".")
            precio = float(txt)

            if precio < 0:
                raise ValueError

        except ValueError:
            QMessageBox.warning(self, "Precio inválido", "Ingresa un precio válido. Ejemplo: 95000")
            return

        update_cubicacion_price(cubicacion_id, precio)

        self.refresh_presupuesto()
        self.refresh_summary_cards()

    def refresh_presupuesto(self):
        if not hasattr(self, "presupuesto_list"):
            return

        while self.presupuesto_list.count():
            item = self.presupuesto_list.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

            elif item.layout():
                while item.layout().count():
                    sub = item.layout().takeAt(0)
                    if sub.widget():
                        sub.widget().deleteLater()

        items = get_presupuesto_by_project(self.project_id)
        total_presupuesto = get_budget_total(self.project_id)

        if hasattr(self, "presupuesto_total_label"):
            self.presupuesto_total_label.setText(format_clp(total_presupuesto))

        if not items:
            empty = QLabel("Aún no hay partidas guardadas. Primero crea una cubicación.")
            empty.setStyleSheet("color: #64748B; font-size: 14px; padding: 12px;")
            self.presupuesto_list.addWidget(empty)
            self.presupuesto_list.addStretch()
            return

        for item_db in items:
            cub_id, tipo, volumen, unidad, precio_unitario, total, created_at = item_db
            unidad_txt = unidad_visible(unidad)

            row_card = QFrame()
            row_card.setObjectName("card")
            row_card.setFixedHeight(66)

            row = QHBoxLayout()
            row.setContentsMargins(16, 8, 16, 8)
            row.setSpacing(12)

            info = QVBoxLayout()
            info.setSpacing(2)

            lbl_tipo = QLabel(tipo)
            lbl_tipo.setStyleSheet("font-size: 14px; font-weight: bold; color: white;")

            lbl_fecha = QLabel(created_at or "")
            lbl_fecha.setStyleSheet("font-size: 10px; color: #64748B;")

            info.addWidget(lbl_tipo)
            info.addWidget(lbl_fecha)

            lbl_volumen = QLabel(f"{volumen:.2f} {unidad_txt}")
            lbl_volumen.setStyleSheet("font-size: 14px; color: #CBD5E1; font-weight: bold;")
            lbl_volumen.setFixedWidth(120)

            precio_input = QLineEdit()
            precio_input.setPlaceholderText("Ej: 95000")
            precio_input.setFixedWidth(135)
            precio_input.setFixedHeight(36)
            precio_input.setText("" if not precio_unitario else str(int(precio_unitario)))
            precio_input.setStyleSheet("""
                QLineEdit {
                    background-color: #020617;
                    color: white;
                    border: 1px solid #475569;
                    border-radius: 8px;
                    padding: 6px 10px;
                    font-size: 13px;
                }

                QLineEdit:focus {
                    border: 2px solid #2563EB;
                }
            """)

            btn_save = QPushButton("Guardar")
            btn_save.setObjectName("primaryButton")
            btn_save.setFixedWidth(96)
            btn_save.setFixedHeight(36)
            btn_save.clicked.connect(
                lambda checked=False, cid=cub_id, inp=precio_input: self.guardar_precio_partida(cid, inp)
            )

            precio_box = QHBoxLayout()
            precio_box.setSpacing(8)
            precio_box.addWidget(precio_input)
            precio_box.addWidget(btn_save)

            lbl_total = QLabel(format_clp(total))
            lbl_total.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
            lbl_total.setFixedWidth(150)

            row.addLayout(info, 1)
            row.addWidget(lbl_volumen)
            row.addLayout(precio_box)
            row.addWidget(lbl_total)

            row_card.setLayout(row)
            self.presupuesto_list.addWidget(row_card)

        self.presupuesto_list.addStretch()

    def exportar_presupuesto_excel(self):
        default_name = f"{self.name}_presupuesto.xlsx".replace(" ", "_")

        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar presupuesto Excel",
            default_name,
            "Archivos Excel (*.xlsx)"
        )

        if not filepath:
            return

        if not filepath.endswith(".xlsx"):
            filepath += ".xlsx"

        try:
            export_presupuesto_excel(self.project_id, filepath)
            QMessageBox.information(
                self,
                "Exportación completada",
                f"Presupuesto exportado correctamente:\n{filepath}"
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Error al exportar",
                f"No se pudo exportar el presupuesto:\n{error}"
            )

    def exportar_presupuesto_pdf(self):
        default_name = f"{self.name}_presupuesto.pdf".replace(" ", "_")

        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar presupuesto PDF",
            default_name,
            "Archivos PDF (*.pdf)"
        )

        if not filepath:
            return

        if not filepath.endswith(".pdf"):
            filepath += ".pdf"

        try:
            export_presupuesto_pdf(self.project_id, filepath)
            QMessageBox.information(
                self,
                "Exportación completada",
                f"Presupuesto exportado correctamente:\n{filepath}"
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Error al exportar",
                f"No se pudo exportar el presupuesto PDF:\n{error}"
            )
