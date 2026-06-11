CUBICACION_RULES = {
    "Radier / Losa": {
        "title": "Radier / Losa de hormigón",
        "formula": "Volumen = Largo × Ancho × Espesor",
        "labels": ("Largo (m)", "Ancho (m)", "Espesor (m)"),
        "placeholders": ("Ej: 10", "Ej: 5", "Ej: 0.12"),
        "default_espesor": "0.12",
        "default_perdida": "0",
        "unit": "m3",
        "tipo_guardado": "Radier / Losa de hormigón",
        "criterio": "Cubicación por volumen: largo × ancho × espesor.",
        "show_ancho": True,
        "show_espesor": True,
    },

    "Excavación": {
        "title": "Excavación",
        "formula": "Volumen = Largo × Ancho × Profundidad",
        "labels": ("Largo zanja/excavación (m)", "Ancho (m)", "Profundidad (m)"),
        "placeholders": ("Ej: 12", "Ej: 0.60", "Ej: 0.80"),
        "default_espesor": "",
        "default_perdida": "0",
        "unit": "m3",
        "tipo_guardado": "Excavación",
        "criterio": "Cubicación por volumen de excavación: largo × ancho × profundidad.",
        "show_ancho": True,
        "show_espesor": True,
    },

    "Muro": {
        "title": "Muro",
        "formula": "Superficie = Largo × Alto",
        "labels": ("Largo del muro (m)", "Alto del muro (m)", ""),
        "placeholders": ("Ej: 8", "Ej: 2.40", ""),
        "default_espesor": "1",
        "default_perdida": "0",
        "unit": "m2",
        "tipo_guardado": "Muro",
        "criterio": "Cubicación por superficie: largo × alto.",
        "show_ancho": True,
        "show_espesor": False,
    },

    "Pintura": {
        "title": "Pintura",
        "formula": "Superficie = Largo × Alto",
        "labels": ("Largo superficie (m)", "Alto superficie (m)", ""),
        "placeholders": ("Ej: 10", "Ej: 2.50", ""),
        "default_espesor": "1",
        "default_perdida": "5",
        "unit": "m2",
        "tipo_guardado": "Pintura",
        "criterio": "Cubicación por superficie pintada: largo × alto.",
        "show_ancho": True,
        "show_espesor": False,
    },

    "Cerámicos": {
        "title": "Cerámicos",
        "formula": "Superficie = Largo × Ancho",
        "labels": ("Largo sector (m)", "Ancho sector (m)", ""),
        "placeholders": ("Ej: 4", "Ej: 3", ""),
        "default_espesor": "1",
        "default_perdida": "10",
        "unit": "m2",
        "tipo_guardado": "Cerámicos",
        "criterio": "Cubicación por superficie revestida: largo × ancho.",
        "show_ancho": True,
        "show_espesor": False,
    },

    "Moldajes": {
        "title": "Moldajes",
        "formula": "Superficie = Largo × Alto",
        "labels": ("Largo elemento (m)", "Alto moldaje (m)", ""),
        "placeholders": ("Ej: 12", "Ej: 0.50", ""),
        "default_espesor": "1",
        "default_perdida": "5",
        "unit": "m2",
        "tipo_guardado": "Moldajes",
        "criterio": "Cubicación por superficie de contacto: largo × alto.",
        "show_ancho": True,
        "show_espesor": False,
    },

    "Enfierradura / Acero kg": {
        "title": "Enfierradura / Acero",
        "formula": "Peso = Largo total × Cantidad × kg/m",
        "labels": ("Largo barra/tramo (m)", "Cantidad", "Peso kg/m"),
        "placeholders": ("Ej: 6", "Ej: 20", "Ej: 0.888"),
        "default_espesor": "",
        "default_perdida": "5",
        "unit": "kg",
        "tipo_guardado": "Enfierradura / Acero",
        "criterio": "Cubicación por peso estimado: largo × cantidad × kg/m.",
        "show_ancho": True,
        "show_espesor": True,
    },

    "Radier con dosificación": {
        "title": "Radier con dosificación",
        "formula": "Volumen = Largo × Ancho × Espesor",
        "labels": ("Largo (m)", "Ancho (m)", "Espesor (m)"),
        "placeholders": ("Ej: 10", "Ej: 5", "Ej: 0.12"),
        "default_espesor": "0.12",
        "default_perdida": "5",
        "unit": "m3",
        "tipo_guardado": "Radier con dosificación",
        "criterio": "Volumen de hormigón para radier. Dosificación debe verificarse según especificación técnica.",
        "show_ancho": True,
        "show_espesor": True,
    },

    "Hormigón fundaciones": {
        "title": "Hormigón fundaciones",
        "formula": "Volumen = Largo × Ancho × Alto",
        "labels": ("Largo fundación (m)", "Ancho (m)", "Alto (m)"),
        "placeholders": ("Ej: 8", "Ej: 0.50", "Ej: 0.40"),
        "default_espesor": "",
        "default_perdida": "5",
        "unit": "m3",
        "tipo_guardado": "Hormigón fundaciones",
        "criterio": "Cubicación por volumen de fundación: largo × ancho × alto.",
        "show_ancho": True,
        "show_espesor": True,
    },

    "Sobrecimiento": {
        "title": "Sobrecimiento",
        "formula": "Volumen = Largo × Ancho × Alto",
        "labels": ("Largo sobrecimiento (m)", "Ancho (m)", "Alto (m)"),
        "placeholders": ("Ej: 10", "Ej: 0.20", "Ej: 0.40"),
        "default_espesor": "",
        "default_perdida": "5",
        "unit": "m3",
        "tipo_guardado": "Sobrecimiento",
        "criterio": "Cubicación por volumen: largo × ancho × alto.",
        "show_ancho": True,
        "show_espesor": True,
    },

    "Estuco": {
        "title": "Estuco",
        "formula": "Superficie = Largo × Alto",
        "labels": ("Largo muro (m)", "Alto muro (m)", ""),
        "placeholders": ("Ej: 8", "Ej: 2.40", ""),
        "default_espesor": "1",
        "default_perdida": "5",
        "unit": "m2",
        "tipo_guardado": "Estuco",
        "criterio": "Cubicación por superficie estucada: largo × alto.",
        "show_ancho": True,
        "show_espesor": False,
    },

    "Yeso cartón": {
        "title": "Yeso cartón",
        "formula": "Superficie = Largo × Alto",
        "labels": ("Largo tabique/cielo (m)", "Alto/Ancho (m)", ""),
        "placeholders": ("Ej: 6", "Ej: 2.40", ""),
        "default_espesor": "1",
        "default_perdida": "10",
        "unit": "m2",
        "tipo_guardado": "Yeso cartón",
        "criterio": "Cubicación por superficie: largo × alto/ancho.",
        "show_ancho": True,
        "show_espesor": False,
    },

    "Cielos": {
        "title": "Cielos",
        "formula": "Superficie = Largo × Ancho",
        "labels": ("Largo recinto (m)", "Ancho recinto (m)", ""),
        "placeholders": ("Ej: 5", "Ej: 4", ""),
        "default_espesor": "1",
        "default_perdida": "10",
        "unit": "m2",
        "tipo_guardado": "Cielos",
        "criterio": "Cubicación por superficie de cielo: largo × ancho.",
        "show_ancho": True,
        "show_espesor": False,
    },

    "Guardapolvos / Molduras": {
        "title": "Guardapolvos / Molduras",
        "formula": "Longitud = Largo tramo × Cantidad",
        "labels": ("Largo tramo (m)", "Cantidad de tramos", ""),
        "placeholders": ("Ej: 2.4", "Ej: 8", ""),
        "default_espesor": "1",
        "default_perdida": "10",
        "unit": "ml",
        "tipo_guardado": "Guardapolvos / Molduras",
        "criterio": "Cubicación por longitud lineal: largo de tramo × cantidad.",
        "show_ancho": True,
        "show_espesor": False,
    },

    "Puertas y ventanas": {
        "title": "Puertas y ventanas",
        "formula": "Cantidad = Unidades",
        "labels": ("Cantidad de unidades", "", ""),
        "placeholders": ("Ej: 6", "", ""),
        "default_espesor": "1",
        "default_perdida": "0",
        "unit": "un",
        "tipo_guardado": "Puertas y ventanas",
        "criterio": "Cubicación por unidad.",
        "show_ancho": False,
        "show_espesor": False,
    },

    "Cubierta / Techumbre": {
        "title": "Cubierta / Techumbre",
        "formula": "Superficie = Largo × Ancho",
        "labels": ("Largo cubierta (m)", "Ancho / desarrollo (m)", ""),
        "placeholders": ("Ej: 10", "Ej: 6", ""),
        "default_espesor": "1",
        "default_perdida": "10",
        "unit": "m2",
        "tipo_guardado": "Cubierta / Techumbre",
        "criterio": "Cubicación por superficie de cubierta: largo × ancho/desarrollo.",
        "show_ancho": True,
        "show_espesor": False,
    },
}


def get_rule(tipo):
    return CUBICACION_RULES.get(tipo, CUBICACION_RULES["Radier / Losa"])


def calculate_result(tipo, largo, ancho, espesor, perdida):
    rule = get_rule(tipo)

    if rule["unit"] == "un":
        base = largo
    else:
        base = largo * ancho * espesor

    resultado = base * (1 + perdida / 100)
    return base, resultado
