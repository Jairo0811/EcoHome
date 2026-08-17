from pathlib import Path

path = Path('README.md')
text = path.read_text(encoding='utf-8')
anchor = '''| 📁 Tipo de entrega | **Proyecto Final** |

---

## 🧩 Alcance conceptual
'''
section = '''| 📁 Tipo de entrega | **Proyecto Final** |

## 🧭 Continuidad académica

**EcoHome** forma parte de la trayectoria académica documentada de Francis Jairo Matías Rosario en la Universidad APEC (UNAPEC). Siguiendo el mismo criterio aplicado en EcoSoft, la continuidad se registra únicamente cuando existe una coincidencia verificable por **estudiante** o **profesor**; no se infieren relaciones por similitud de nombres, períodos o referencias aisladas.

### 👥 Continuidad por estudiante

El equipo académico original estuvo compuesto por **Andrés Beltré (A00113462)**, **Rafael Antonio De Leon Dominguez (A00113515)** y **Francis Jairo Matías Rosario (A00115261)**.

Dentro de los proyectos actualmente documentados en esta colección no se ha verificado que Andrés Beltré o Rafael Antonio De Leon Dominguez vuelvan a coincidir con Francis Jairo Matías Rosario en otro equipo académico por **mismo nombre completo y misma matrícula**.

### 👨‍🏫 Continuidad por profesor

El profesor de **Ingeniería de Requisitos (ISO-500)** fue **Ing. Eddy G. Alcantara Solano**. En la colección actual no se ha verificado una segunda asignatura cursada por Francis Jairo Matías Rosario con el mismo profesor.

| Tipo | Estado | Evidencia |
|---|---|---|
| 👥 Estudiante recurrente | No verificado | No existe una segunda coincidencia inequívoca en los proyectos documentados |
| 👨‍🏫 Profesor recurrente | No verificado | Solo se ha documentado ISO-500 con Ing. Eddy G. Alcantara Solano |

EcoHome conserva así su lugar dentro de la trayectoria académica sin atribuirle una continuidad directa que todavía no está demostrada.

---

## 🧩 Alcance conceptual
'''
if anchor not in text:
    raise SystemExit('Academic information anchor not found')
path.write_text(text.replace(anchor, section, 1), encoding='utf-8')
