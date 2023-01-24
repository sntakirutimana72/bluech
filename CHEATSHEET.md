```shell
  docker build -t bluech .

  docker run bluech
  
  docker ps

  docker exec -it 240709f0217a /bin/bash

  service postgresql start
  
  su postgres
  
  psql
  
  \password postgres;
  
  service postgresql reload

  python3.9

  from app.utils.db_connect import db_connector
  from app.models import *
```