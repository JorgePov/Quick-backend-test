
# Prueba Backend[Quick] - Jorge Poveda



## Breve explicacion

Se solicito el desarrollo de un backend basados en un base de datos relacional compartida.

## Requerimientos

**1:**  Crear un CRUD de cada una de las tablas
**2:**  Logeo y registro
**3:**  authenticacion con JWT
**4:**  Generacion de archivo sobre clientes con ('documento','nombre completo', 'numero de facturas') y bulk-import d

## Vesiones 


**Backend:** python3.9, django v4.2

**DataBase:** Postgres:14


## Instalaccion

Instalacion manual usar python3.9

Backend 
- Lista de comandos
```bash
  cd api
  python3.9 -m venv venv
  source venv/bin/activate
  pip3 install -r requirements.txt
  python3.9 manager.py migrate
  python3.9 manager.py runserver 0.0.0.0:8000
```

Base de datos
```bash
  docker-compose start postgres
```

Ingresar a http://localhost:8080/docs para ver documentacion de los servicios


## Instalaccion Docker

Inicializacion con dockers en la raiz del proyecto ejecutar

```bash
  docker-compose up -d --build
```

Este comando deberia permitir ya el ingreso a toda la prueba

- Endpoint backend: http://localhost:8000

