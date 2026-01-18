# API Examples (curl)

## Health Check
```bash
curl http://<DB_API_PRIVATE_IP>:5000/health
```

## List Notes
```bash
curl http://<DB_API_PRIVATE_IP>:5000/notes
```

## Create Note
```bash
curl -X POST http://<DB_API_PRIVATE_IP>:5000/notes \
  -H "Content-Type: application/json" \
  -d '{"content":"Hello from curl"}'
```

## Get Note by ID
```bash
curl http://<DB_API_PRIVATE_IP>:5000/notes/1
```

## Update Note
```bash
curl -X PUT http://<DB_API_PRIVATE_IP>:5000/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"content":"Updated content"}'
```

## Delete Note
```bash
curl -X DELETE http://<DB_API_PRIVATE_IP>:5000/notes/1
```
