# webScrapping (PT1)
Extracción de datos para el estudio de mareas a lo largo de la vía fluvial.

## Requirements
* Python 3.6
* requests 2.23.0
* beautifulsoup4 4.8.2

## Installation
Clone this repository
```
$git clone https://github.com/adions025/webScrapping.git
```

## Usage
usage:
```
$python main.py [--h] [--location]
```
argumentos opcionales
* --h: ayuda
* --location: nombre del puerto

Lista completa de puertos:

```
['ATAL', 'AGUI', 'SUCE', 'CROS', 'SANB', 'SSEB', 'SCOT', 'THET', 'USHU', 'BROW', 'CAMA',
'JUBA', 'ESPE', 'CBRE', 'LAMI', 'CPAU', 'SPAB', 'BBLA', 'OYAR', 'PCOL', 'EMAG', 'SROM',
'CALD', 'MAGA', 'NENY', 'ANUE', 'MAJO', 'MHER', 'TURB', 'PINA', 'PARG', 'BELG', 'BSAS',
'COMO', 'CHAR', 'PDES', 'FOST', 'IWHI', 'LPLA', 'MADR', 'MARD', 'MELC', 'NEKO', 'QUEQ',
'RAWS', 'RIOG', 'ROSA', 'SANT', 'SJUA', 'SJUL', 'SELE', 'VANC', 'LOYO', 'QUIL', 'RION',
'SCLE', 'SANF', 'STER']
```

## Content

+ **src/scrapping.py**

Clase Scrapping, contiene los métodos necesarios para la extracción de datos del estudio de mareas a lo largo de la vida 
fluvial. Esta clase permite la configuración del header, de los componentes de selección de la página como 
selectOptions, se encarga de devolver el objeto beautiful soup con los datos sin los tags html,  calcular el tiempo en 
que tarda en completar  la request y añadir un valor proporcional. Y permite guardar
los datos en formato .CSV.

+ **src/main.py**

Funcion principal del programa, necesita como argumento el puerto del cual se quiere extraer la informacion. Los puertos
se los identifica por sus siglas.

+ **src/agents.py**

Contiene los user-agents que seran incoportados de manera aleatoria en el header de la request.

+ **res/dataset.csv**

Es el dataset resultado en formado csv.

+ **mareas.pdf**

Documento pdf con las respuestas y tabla de contribución.

# Wiki

En la wiki se describe con detalles el dataset.

+ [Wiki Github](https://github.com/adions025/webScrapping.wiki.git)

## Authors

* [Adonis González Godoy](adions025@uoc.edu)
* [Eduard Tremps](etremps@uoc.edu)
