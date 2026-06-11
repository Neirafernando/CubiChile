# CubiChile

**CubiChile** es una aplicación de escritorio desarrollada en Python para apoyar procesos de **cubicación, presupuesto e informes técnicos de obra** en el contexto chileno.

El objetivo del proyecto es entregar una herramienta simple, ordenada y práctica para registrar proyectos, calcular partidas de construcción, generar presupuestos y exportar documentación en formatos útiles como **PDF** y **Excel**.

---

## Estado del proyecto

**Versión actual:** MVP v0.1
**Estado:** En desarrollo activo
**Autor:** Fernando Javier Bueno Neira
**Repositorio:** CubiChile

Esta primera versión corresponde a un producto mínimo viable funcional. La aplicación ya permite trabajar con proyectos reales de prueba, aunque todavía se encuentra en etapa de mejora y validación.

---

## Características principales

* Gestión de proyectos de obra.
* Registro de cliente, ubicación y descripción del proyecto.
* Módulo de cubicaciones por partida.
* Cálculo automático de cantidades.
* Soporte para unidades como m², m³, kg, ml y unidades.
* Aplicación de pérdida o recargo porcentual.
* Nombre personalizado por partida.
* Observaciones por partida.
* Listado de partidas guardadas.
* Edición y eliminación de partidas.
* Presupuesto con precio unitario y total por partida.
* Exportación de presupuesto a Excel.
* Exportación de presupuesto a PDF.
* Exportación de informe técnico completo en PDF.
* Interfaz gráfica de escritorio con PySide6.
* Base de datos local SQLite.

---

## Tipos de partidas disponibles

Actualmente CubiChile permite trabajar con las siguientes partidas:

* Radier / Losa
* Excavación
* Muro
* Pintura
* Cerámicos
* Moldajes
* Enfierradura / Acero kg
* Radier con dosificación
* Hormigón fundaciones
* Sobrecimiento
* Estuco
* Yeso cartón
* Cielos
* Guardapolvos / Molduras
* Puertas y ventanas
* Cubierta / Techumbre

Cada partida utiliza criterios de cálculo específicos según su unidad y tipo de medición.

---

## Tecnologías utilizadas

* **Python 3**
* **PySide6** para la interfaz gráfica
* **SQLite** para almacenamiento local
* **ReportLab** para generación de PDF
* **OpenPyXL** para exportación a Excel

---

## Estructura general del proyecto

```text
CubiChile/
├── main.py
├── database.py
├── calculations.py
├── calc_rules.py
├── pdf_export.py
├── excel_export.py
├── requirements.txt
├── README.md
├── assets/
│   └── styles.qss
├── data/
│   └── .gitkeep
└── ui/
    ├── dashboard.py
    ├── main_window.py
    ├── project_view.py
    ├── projects_page.py
    ├── cubicaciones_view.py
    └── presupuesto_view.py
```

---

## Instalación local

Clonar el repositorio:

```bash
git clone https://github.com/Neirafernando/CubiChile.git
cd CubiChile
```

Crear entorno virtual:

```bash
python3 -m venv venv
```

Activar entorno virtual:

```bash
source venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar la aplicación:

```bash
python3 main.py
```

---

## Base de datos

CubiChile utiliza una base de datos local SQLite ubicada en la carpeta `data/`.

Por seguridad, los archivos de base de datos no se suben al repositorio. El archivo `.gitkeep` solo mantiene la carpeta `data/` dentro del proyecto.

Archivos ignorados:

```text
data/*.db
data/*.sqlite
data/*.sqlite3
```

---

## Exportaciones disponibles

La aplicación permite generar:

### Excel

* Presupuesto por partida.
* Cantidades cubicadas.
* Precios unitarios.
* Totales.

### PDF

* Presupuesto de obra.
* Informe técnico completo.
* Datos generales del proyecto.
* Detalle de cubicaciones.
* Resumen presupuestario.

---

## Objetivo del proyecto

CubiChile nace como una herramienta práctica para apoyar tareas de cubicación y presupuesto en proyectos de construcción, especialmente en etapas de estudio, planificación y revisión de cantidades.

La idea principal es reducir el uso de planillas desordenadas y centralizar la información técnica de un proyecto en una aplicación simple y clara.

---

## Próximas mejoras previstas

* Presupuesto con IVA, utilidad y gastos generales.
* Configuración de datos de empresa.
* Logo personalizado en informes PDF.
* Exportación e importación de proyectos.
* Respaldo automático de base de datos.
* Mejoras visuales en la interfaz.
* Empaquetado como ejecutable.
* Validación avanzada de partidas.
* Historial de versiones de informes.

---

## Advertencia técnica

Los cálculos generados por CubiChile son una herramienta de apoyo y deben ser revisados contra planos, especificaciones técnicas, antecedentes del proyecto y criterios normativos vigentes.

La aplicación no reemplaza la revisión profesional ni la validación técnica correspondiente.

---

## Autor

Desarrollado por **Fernando Javier Bueno Neira**.

Proyecto creado como parte de un proceso de aprendizaje, desarrollo de software y aplicación práctica al área de construcción, cubicaciones y presupuestos.
