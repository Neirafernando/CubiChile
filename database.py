import sqlite3
from pathlib import Path

DB_PATH = Path("data/cubichile.db")


def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            client TEXT,
            location TEXT,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cubicaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            largo REAL NOT NULL,
            ancho REAL NOT NULL,
            espesor REAL NOT NULL,
            volumen REAL NOT NULL,
            unidad TEXT DEFAULT 'm3',
            precio_unitario REAL DEFAULT 0,
            total REAL DEFAULT 0,
            criterio TEXT,
            norma TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(project_id) REFERENCES projects(id)
        )
    """)

    conn.commit()
    conn.close()


def create_project(name, client, location, description):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO projects (name, client, location, description)
        VALUES (?, ?, ?, ?)
    """, (name, client, location, description))

    conn.commit()
    conn.close()


def get_projects():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, client, location, created_at
        FROM projects
        ORDER BY id DESC
    """)

    projects = cursor.fetchall()
    conn.close()
    return projects


def create_cubicacion(project_id, tipo, largo, ancho, espesor, volumen, criterio, norma, unidad="m3"):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO cubicaciones (
            project_id, tipo, largo, ancho, espesor, volumen, criterio, norma, unidad
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (project_id, tipo, largo, ancho, espesor, volumen, criterio, norma, unidad))

    conn.commit()
    conn.close()


def get_cubicaciones_by_project(project_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, tipo, largo, ancho, espesor, volumen, unidad, criterio, norma, created_at
        FROM cubicaciones
        WHERE project_id = ?
        ORDER BY id DESC
    """, (project_id,))

    cubicaciones = cursor.fetchall()
    conn.close()
    return cubicaciones


def get_project_totals(project_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*), COALESCE(SUM(volumen), 0)
        FROM cubicaciones
        WHERE project_id = ?
    """, (project_id,))

    result = cursor.fetchone()
    conn.close()
    return result


def get_project_by_id(project_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, client, location, description, created_at
        FROM projects
        WHERE id = ?
    """, (project_id,))

    project = cursor.fetchone()
    conn.close()
    return project


def update_project(project_id, name, client, location, description):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE projects
        SET name = ?, client = ?, location = ?, description = ?
        WHERE id = ?
    """, (name, client, location, description, project_id))

    conn.commit()
    conn.close()


def delete_cubicacion(cubicacion_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM cubicaciones
        WHERE id = ?
    """, (cubicacion_id,))

    conn.commit()
    conn.close()



def update_cubicacion_price(cubicacion_id, precio_unitario):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT volumen
        FROM cubicaciones
        WHERE id = ?
    """, (cubicacion_id,))

    row = cursor.fetchone()

    if not row:
        conn.close()
        return

    volumen = row[0]
    total = volumen * precio_unitario

    cursor.execute("""
        UPDATE cubicaciones
        SET precio_unitario = ?, total = ?
        WHERE id = ?
    """, (precio_unitario, total, cubicacion_id))

    conn.commit()
    conn.close()


def get_presupuesto_by_project(project_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, tipo, volumen, unidad, precio_unitario, total, created_at
        FROM cubicaciones
        WHERE project_id = ?
        ORDER BY id DESC
    """, (project_id,))

    items = cursor.fetchall()
    conn.close()
    return items


def get_budget_total(project_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(total), 0)
        FROM cubicaciones
        WHERE project_id = ?
    """, (project_id,))

    total = cursor.fetchone()[0]
    conn.close()
    return total


def update_cubicacion_dimensions(cubicacion_id, largo, ancho, espesor, volumen):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT precio_unitario
        FROM cubicaciones
        WHERE id = ?
    """, (cubicacion_id,))

    row = cursor.fetchone()
    precio_unitario = row[0] if row else 0
    total = volumen * precio_unitario

    cursor.execute("""
        UPDATE cubicaciones
        SET largo = ?, ancho = ?, espesor = ?, volumen = ?, total = ?
        WHERE id = ?
    """, (largo, ancho, espesor, volumen, total, cubicacion_id))

    conn.commit()
    conn.close()
