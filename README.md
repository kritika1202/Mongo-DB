# Mongo-DB

Employee Management API built with FastAPI and MongoDB. It includes the tutorial
endpoints `POST /add` and `GET /getAll`, plus the original full CRUD API under
`/employees`.

## Requirements

- Python 3.10+
- Docker with the Compose plugin, or a separately running MongoDB server
- MongoDB Compass (optional, for browsing documents)

## 1. Start MongoDB

The simplest option is Docker Compose, which works on Windows, macOS, and Linux.
From this directory, run:

```bash
docker compose up -d
```

Check that the `mongo` container is running with `docker compose ps`. The
MongoDB connection URI is `mongodb://127.0.0.1:27017`.

If MongoDB Community Server is already installed as a Windows service, open
Command Prompt as Administrator and run:

```bat
net start MongoDB
```

To check whether the port is listening on Windows:

```bat
netstat -ano | findstr :27017
```

## 2. Install and start the API

From this directory, create and activate a virtual environment, then install
dependencies. On Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

On Windows PowerShell, use `py -m venv .venv`, then
`.\.venv\Scripts\Activate.ps1`, and `Copy-Item .env.example .env`.

Start the API:

```bash
uvicorn main:app --reload --env-file .env
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) to try the API.

## 3. Verify the MongoDB connection

In a second terminal with the virtual environment active, run:

```bash
python test_connection.py
```

Expected output: `MongoDB connected successfully`. If the connection is refused,
make sure MongoDB is running and that `MONGO_URI` in `.env` points to the right
server. Compass is only a database GUI; it does not start MongoDB Server.

## 4. Insert an employee record

In Swagger UI at [http://localhost:8000/docs](http://localhost:8000/docs), choose
`POST /add`, click **Try it out**, enter this request body, and click **Execute**:

```json
{
  "id": 101,
  "name": "Rahul",
  "age": 25,
  "salary": 50000,
  "desig": "Developer"
}
```

The API responds with HTTP `201` and `{"message":"Employee added successfully"}`.
MongoDB creates the database and collection automatically on the first insert.
This endpoint stores the record in `employee_db.employee`.

## 5. Verify the record

In MongoDB Compass, connect using `mongodb://127.0.0.1:27017`, then open
`employee_db` > `employee` > **Documents**. Or call `GET /getAll` in Swagger UI;
the response contains the inserted employee.

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/add` | Insert a tutorial-format employee (`id`, `name`, `age`, `salary`, `desig`) |
| `GET` | `/getAll` | List tutorial-format employee records |
| `POST` | `/employees` | Create an employee |
| `GET` | `/employees` | List employees |
| `GET` | `/employees/{employee_id}` | Get one employee |
| `PUT` | `/employees/{employee_id}` | Replace an employee |
| `DELETE` | `/employees/{employee_id}` | Delete an employee |

The tutorial endpoints use the `employee_db.employee` collection. The original
CRUD endpoints use `employee_db.employees` and a different employee schema
(`name`, `email`, `department`, `position`, `salary`, and optional
`date_joined`). For the original CRUD API, create an employee first and use its
returned MongoDB `id` for get, update, and delete. `PUT` replaces all fields.

To use a different MongoDB connection, update `MONGO_URI` in `.env`. Stop the
local MongoDB container with `docker compose down`; add `-v` only if you intend
to delete its persisted data.
