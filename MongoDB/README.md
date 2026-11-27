# MongoDB Terminal Lab

Practice each command directly in `mongosh`. This lab creates the `EmployeeDB` database and an `employee` collection, then inserts, searches, deletes, and updates employee records.

## Open mongosh

Start MongoDB Server first. Open a terminal (Command Prompt or PowerShell on Windows; Terminal on Linux/macOS) and connect to the local server:

```sh
mongosh "mongodb://127.0.0.1:27017"
```

You should see a `>` prompt. Type the MongoDB commands below at that prompt, one at a time. If `mongosh` is not recognized, install MongoDB Shell (`mongosh`) or add it to your system `PATH`.

## Exercise

### 1. List databases

```javascript
show dbs
```

**What it does:** Lists databases that already contain data. `EmployeeDB` will not appear until you insert a document.

**Expected result:** A list of existing databases, such as `admin`, `config`, and `local`.

### 2. Select the practice database

```javascript
use EmployeeDB
```

**What it does:** Switches the current shell context to `EmployeeDB`.

**Expected result:** `switched to db EmployeeDB`.

### 3. Create the employee collection

```javascript
db.createCollection("employee")
```

**What it does:** Creates a collection named `employee` in the selected database.

**Expected result:** `{ ok: 1 }`.

### 4. List collections

```javascript
show collections
```

**What it does:** Lists collections in the current database.

**Expected result:** `employee`.

### 5. Insert one employee

```javascript
db.employee.insertOne({
  id: 100,
  name: "Alex",
  age: 60,
  design: "Manager",
  salary: 90000
})
```

**What it does:** Inserts the first employee. This record is used in the age-over-50 Manager search.

**Expected result:** An acknowledged insert with an automatically generated `_id`.

### 6. Insert several employees

```javascript
db.employee.insertMany([
  { id: 101, name: "Rahul", age: 25, design: "Developer", salary: 50000 },
  { id: 102, name: "Priya", age: 28, design: "Tester", salary: 65000 },
  { id: 103, name: "Kiran", age: 45, design: "Manager", salary: 80000 },
  { id: 104, name: "Meera", age: 35, design: "Developer", salary: 72000 },
  { id: 105, name: "Omar", age: 18, design: "Intern", salary: 30000 }
])
```

**What it does:** Inserts five more employee documents.

**Expected result:** An acknowledged insert showing five inserted IDs.

### 7. Find all employees

```javascript
db.employee.find()
```

**What it does:** Returns every document in the collection.

**Expected result:** Six employee documents, with ids `100` through `105`.

### 8. Find one employee by id

```javascript
db.employee.findOne({ id: 100 })
```

**What it does:** Finds the first employee whose `id` is `100`.

**Expected result:** Alex's employee document, including age `60` and design `Manager`.

### 9. Find employees by design

```javascript
db.employee.find({ design: "Manager" })
```

**What it does:** Finds employees whose design is `Manager`.

**Expected result:** Alex (id `100`) and Kiran (id `103`).

### 10. Find employees by age comparisons

Age greater than 30:

```javascript
db.employee.find({ age: { $gt: 30 } })
```

**Expected result:** Employees aged 35, 45, and 60.

Age less than 30:

```javascript
db.employee.find({ age: { $lt: 30 } })
```

**Expected result:** Employees aged 18, 25, and 28.

Age greater than or equal to 45:

```javascript
db.employee.find({ age: { $gte: 45 } })
```

**Expected result:** Employees aged 45 and 60.

Age less than or equal to 25:

```javascript
db.employee.find({ age: { $lte: 25 } })
```

**Expected result:** Employees aged 18 and 25.

### 11. Find employees by age and design together

```javascript
db.employee.find({ age: { $gt: 50 }, design: "Manager" })
```

**What it does:** MongoDB combines these filter fields with AND: the age must be over 50 and the design must be `Manager`.

**Expected result:** Alex (id `100`).

### 12. Delete one employee by id

```javascript
db.employee.deleteOne({ id: 105 })
```

**What it does:** Deletes the first matching employee with id `105`.

**Expected result:** `acknowledged: true` and `deletedCount: 1`.

### 13. Delete multiple employees by age

```javascript
db.employee.deleteMany({ age: { $lt: 30 } })
```

**What it does:** Deletes all remaining employees younger than 30.

**Expected result:** `deletedCount: 2` (ids `101` and `102`; id `105` was deleted in the previous step).

### 14. Update an employee's salary by id

```javascript
db.employee.updateOne(
  { id: 100 },
  { $set: { salary: 95000 } }
)
```

**What it does:** Sets Alex's salary to `95000` without replacing the other fields.

**Expected result:** `matchedCount: 1` and `modifiedCount: 1`.

Verify the update:

```javascript
db.employee.findOne({ id: 100 })
```

**Expected result:** Alex's document now has `salary: 95000`.

> Run the insert steps once in a fresh practice database. Re-running them inserts duplicate employee documents because this exercise does not add a unique index on `id`.
