# itmap

## SERVER

### Build

```
docker-compose build server
```

### Run

```
docker-compose up -d
```

### INITIAL DATABASE

```
TEST ENV:
 - docker-compose exec server flask initdb
PRODUCT ENV:
 only the third step is always need.
 - docker-compose exec server flask db init
 - docker-compose exec server flask db migrate
 - docker-compose exec server flask db upgrade

```

### IPYTHON

```
docker-compose exec server flask ipython
```

### APIDOC

```
open http://localhost:5000/apidocs/
```

### ADMIN

```
open http://localhost:5000/admin/
```

## WEB

### Build

```
docker-compose build web
```

### Run

```
docker-compose up -d
```

### Access

```
open http://localhost:8020
```
