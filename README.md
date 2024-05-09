# Anexo I : Creación entorno virtual desde CMD

Ubicados dentro de la carpeta del proyecto con el CMD

```console
python -m virtualenv .venv
``` 

Activar entorno virtual cada vez que se va a utilizar desde CMD:

```console
.venv/scripts/activate
```

Una vez activado el entorno virtual Instalar las dependencias de librerias:

```console
pip install -r requirements.txt
```

Listo!

# Anexo II : Instalación de librerias

Con el entorno virtual activado se pueden instalar librerías buscando su comando en google, por ejemplo para numpy, pandas o scipy:

```console
pip install numpy
```

```console
pip install pandas
```

```console
pip install scipy
```

Algunos son intuitivos, pero otros no tanto y lo mejor es googlear.

# Anexo III : Actualización de las dependencias

Para que todo funcione bien es bueno tener siempre actualizadas las dependencias que se alojan en el archivo requirements.txt asi no hay fallas cuando se corren los scripts. Las dependencias incluyen el listado de librerias que se van a utilizar y la versión que se utilizó. Por ejemplo: **numpy==1.26.4**

Actualización de dependencias:

```console
pip freeze > requirements.txt
```