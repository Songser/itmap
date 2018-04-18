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
docker-compose exec server flask initdb
```

### IPYTHON

```
docker-compose exec server flask ipython
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
