# Guía de Uso para el Mapeador de Archivos .dbf en Python

Este proyecto permite mapear archivos `.dbf` mediante el uso de clases Python, lo que facilita la consulta y lectura de datos. Las clases de modelo representan cada archivo `.dbf`, y cada clase se asocia a una tabla específica en la base de datos.

## Creación de Modelos

Para crear un modelo que represente un archivo `.dbf`, sigue los pasos a continuación.

### Paso 1: Crear Clases Modelo

Define una clase Python para cada archivo `.dbf` que quieras mapear. Estas clases deben heredar de la clase `Model`, que proporciona las funcionalidades básicas para la lectura de datos.

Ejemplo:
```python
from core.model import Model
from os import path


class Alumnos(Model):
    # Define el atributo de clase `__ctx__` como la ruta absoluta al archivo .dbf
    __ctx__ = path.abspath("db/alumnostemp.dbf")

    def __init__(self):
        super().__init__(subclass=self)
        # Define los atributos correspondientes a las columnas del archivo .dbf
        self.MATRICULA = None
        self.NOMBRE = None
        self.GRADO = None
        self.GRUPO = None
        self.STADESCRI = None


class Boletas(Model):
    __ctx__ = path.abspath("db/boletas.dbf")

    def __init__(self):
        super().__init__(subclass=self)

        self.CLAVEMAT = None
        # Establecer una llave foránea con la tabla Alumnos. Con la MATRICULA
        self.MATRICULA = Annotated[str, {"foreign_key": [Alumnos]}]
        self.MATERIA = None
        self.PARCIAL_1 = None
        self.FALTAS_1 = None
        self.PARCIAL_2 = None
        self.FALTAS_2 = None
        self.PARCIAL_3 = None
        self.FALTAS_3 = None
        self.PARCIAL_4 = None
        self.FALTAS_4 = None
        self.PARCIAL_5 = None
        self.PROMEDIO = None
        self.STATUS = None
        self.OBSERVA = None
        self.PALABRA = None

if __name__ == "__main__":
    alumno = Alumnos().get(MATRICULA="24A0710217M0010", relates=True)
    print(alumno.BOLETAS)
    print(boleta.get_all(MATRICULA="24A0710217M0010"))
