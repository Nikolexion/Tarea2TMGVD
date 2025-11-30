# Tarea 2 Tópicos en Manejo de Grandes Volúmenes de Datos
Tarea 2 de la asignatura **Tópicos en Manejo de Grandes Volúmenes de Datos** en el que se implementó la estructura MRL y se realizó una experimentación sobre las consultas rank y select.

## Integrantes
* Nicolás López Cid
* Ricardo Charris Jiménez
* Benjamin Alonso Espinoza

## Estructura del Proyecto
* `/`: Códigos fuente (`main.cpp`, `mrl.h`).
* `Datos/`: Carpeta que debe contener los archivos `.txt` para la experimentación.
* `results/`: Carpeta donde se generarán automáticamente los archivos `.csv`.

## Instrucciones de Compilación y Ejecución

### 1. Requisitos Previos
* Compilador C++ compatible con C++11 (g++).
* Make.

### 2. Compilación
Para compilar el proyecto, se debe ejecutar el siguiente comando en la raíz del directorio:

```bash
make
```

Esto generara un ejecutable llamado `main.out`.

### 3. Ejecución
Para ejecutar la experimentación con un único archivo, usar el comando (Asegurarse de tener creada la carpeta `/results`):

```bash
./main.out <ruta_archivo> 
```

Para ejecutar la experimentación con todos los archivos que se encuentren en la carpeta `/Datos`, usar el comando (Esto generara automáticamente la carpeta `/results` en caso de que no exista):

```bash
bash ./experimentacion.sh
```

Ambas opciones guardaran automáticamente los resultados en la carpeta `/results`.


