# entelai-pdf

## Setup 
El código de este repo está pensado para ser usado con python `3.6.3`

Es recomendado usar un virtualenv e instalar las dependencias dentro via:
```bash
virtualenv -p python3 venv
. venv/bin/activate
pip install -r src/requirements.txt
```

En ubuntu es necesario tener instaladas las librerias `python3-dev, libffi-dev, libjpeg-dev 
y zlib1g-dev` antes de instalar los requirements 

## Casos de ejemplo

Para correr los cass de ejemplo basta con ejecutar

```bash
python examples_4_reports.py
```

dentro de la carpeta `pdfreport`. 

## Uso

El script principal del proyecto se encuentra en `src/report_generator.py`. 
Este script expone una clase que puede usarse para generar reportes cómo en el siguiente snippet

```python 
from report_generator import ReportGenerator

out_path = "./some_folder/filename.pdf"

report = {
    ...
}

ReportGenerator.generate_report(out_path, report)
```

Dentro del repo se encuentra el script `src/example.py` a modo de ejemplo. 
Este script genera un pdf `example.pdf` a partir de datos generados aleatoreamente en el 
script `src/example_data_faker.py`.


### Server de desarrollo

Dentro del archivo `src/server.py` se encuentra un server de Flask para ser usado a modo de debugger del
pdf a generar. Para levantar el server ejecutar `python src/server.py` y entrar a 
[localhost:5000](http://localhost:5000/) para ver un ejemplo del pdf final 


# AWS Lambda

Code was adapted to run as a lambda function. An AWS lambda function called entelai-pdf is created automatically.
You need to verify that the runtime is python 3.7. Necessary files are copied as part of the bitbucket pipeline.

## Development
The package python lambda local is included to test the function call in the same manner as it
will be later called in the lambda environment. To use it type:

```bash
 $ python-lambda-local -f generate_reports pdfreport/lambda_handler.py event.json -t 60
``` 
For this to work locally you must have configured you aws credentials with access to the staging-temp bucket
defined in the event message. You can specify an aws profile in the event message using key: "profile_name"
 
### Test event message
A sample event json message is included which mimics all the information needed to run the lambda function
 
