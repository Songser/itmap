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

### Access

open http://localhost:5000

### INITIAL DATABASE

```
docker-compose exec server sh
flask initdb
```

### ADMIN

open http://localhost:5000/admin/

### IPYTHON

```
docker-compose exec server sh
flask ipython
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

open http://localhost:8020
