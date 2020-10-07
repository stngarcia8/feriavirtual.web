Preparación del ambiente para maipogrande:
a. Opcional, actualizar gestores de paquetes y librerias base del entorno.
actualizar conda:
conda update conda --yes

actualizar pip:
python -m pip install --upgrade pip


a. crear el ambiente virtual.
conda create --name maipogrande python=3.7 --yes

b. activar el ambiente virtual.
conda activate maipogrande

c. Cargar las librerías necesarias, se debe estar dentro del ambiente virtual.
pip install -r requirements.txt

d. desactivar el ambiente virtual.
conda deactivate

e. Eliminar el ambiente virtual, primero debe desactivar el ambiente virtual antes de eliminarlo.
conda remove --yes --name maipogrande --all


Notas de ejecucion:
1. en la carpeta donde se encuentra el archivo manage.py y estando dentro del ambiente virtual ejecutar lo siguiente:
- python manage.py makemigrations.
- python manage.py migrate
- python manage.py poblarbase
- python manage.py runserver

2. abrir un navegador y en la barra de direcciones escribir:
localhost:8000

el usuario admin es fv_user
contraseña: fv_pwd

