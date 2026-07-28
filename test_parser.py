from app.ai.pert_parser import PertParser


texto = """
TABLA DE ACTIVIDADES DEL PROYECTO
ID
DURACIÓN
ACTIVIDAD
DESCRIPCIÓN
(días)
PREDECESORES

A
Actividad A
3
-

B
Actividad B
5
A

C
Actividad C
2
A
"""


resultado = PertParser.parse_ocr_text(
    texto
)


print(resultado)