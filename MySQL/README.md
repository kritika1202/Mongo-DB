# MySQL Terminal Lab

Practice each SQL statement directly in the MySQL command-line client. This lab creates the `EmployeeDB` database and an `employee` table, then inserts, searches, deletes, and updates employee records.

## Open the MySQL terminal

Start the MySQL Server first. Open a terminal and connect with a MySQL account that can create databases. For example:

```sh
mysql -u root -p
```

Enter the MySQL password when prompted (the password will not appear as you type). You should then see a `mysql>` prompt. Type each SQL statement below at that prompt. On Windows, you can also open the **MySQL Command Line Client** installed with MySQL Server. If `mysql` is not recognized, add the MySQL `bin` directory to `PATH` or use that client shortcut.

## Exercise

### 1. List databases

```sql
SHOW DATABASES;
```

**What it does:** Lists databases on the MySQL server.

**Expected result:** A table of existing databases. `EmployeeDB` is added in the next step.

### 2. Create the practice database

```sql
CREATE DATABASE EmployeeDB;
```

**What it does:** Creates a database named `EmployeeDB`.

**Expected result:** `Query OK`.

### 3. Select the database

```sql
USE EmployeeDB;
```

**What it does:** Makes `EmployeeDB` the active database for the following commands.

**Expected result:** `Database changed`.

### 4. Create the employee table

```sql
CREATE TABLE employee (
  id INT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  age INT NOT NULL,
  design VARCHAR(100) NOT NULL,
  salary DECIMAL(10, 2) NOT NULL
);
```

**What it does:** Creates an `employee` table. `id` is the primary key, so each employee must have a unique id.

**Expected result:** `Query OK`.

### 5. Show tables

```sql
SHOW TABLES;
```

**What it does:** Lists tables in the selected database.

**Expected result:** A table containing `employee`.

### 6. Insert one employee

```sql
INSERT INTO employee (id, name, age, design, salary)
VALUES (100, 'Alex', 60, 'Manager', 90000.00);
```

**What it does:** Inserts the first employee. This record is used in the age-over-50 Manager search.

**Expected result:** `Query OK, 1 row affected`.

### 7. Insert several employees

```sql
INSERT INTO employee (id, name, age, design, salary) VALUES
  (101, 'Rahul', 25, 'Developer', 50000.00),
  (102, 'Priya', 28, 'Tester', 65000.00),
  (103, 'Kiran', 45, 'Manager', 80000.00),
  (104, 'Meera', 35, 'Developer', 72000.00),
  (105, 'Omar', 18, 'Intern', 30000.00);
```

**What it does:** Inserts five more employees in one statement.

**Expected result:** `Query OK, 5 rows affected`.

### 8. Select all employees

```sql
SELECT * FROM employee;
```

**What it does:** Returns every row in the table.

**Expected result:** Six employees, with ids `100` through `105`.

### 9. Select one employee by id

```sql
SELECT * FROM employee WHERE id = 100;
```

**What it does:** Finds the employee whose id is `100`.

**Expected result:** Alex's row, including age `60` and design `Manager`.

### 10. Select employees by design

```sql
SELECT * FROM employee WHERE design = 'Manager';
```

**What it does:** Finds employees whose design is `Manager`.

**Expected result:** Alex (id `100`) and Kiran (id `103`).

### 11. Select employees by age comparisons

Age greater than 30:

```sql
SELECT * FROM employee WHERE age > 30;
```

**Expected result:** Employees aged 35, 45, and 60.

Age less than 30:

```sql
SELECT * FROM employee WHERE age < 30;
```

**Expected result:** Employees aged 18, 25, and 28.

Age greater than or equal to 45:

```sql
SELECT * FROM employee WHERE age >= 45;
```

**Expected result:** Employees aged 45 and 60.

Age less than or equal to 25:

```sql
SELECT * FROM employee WHERE age <= 25;
```

**Expected result:** Employees aged 18 and 25.

### 12. Select employees by age and design together

```sql
SELECT * FROM employee
WHERE age > 50 AND design = 'Manager';
```

**What it does:** Returns rows matching both conditions.

**Expected result:** Alex (id `100`).

### 13. Delete one employee by id

```sql
DELETE FROM employee WHERE id = 105;
```

**What it does:** Deletes the employee with id `105`.

**Expected result:** `Query OK, 1 row affected`.

### 14. Delete multiple employees by age

```sql
DELETE FROM employee WHERE age < 30;
```

**What it does:** Deletes all remaining employees younger than 30.

**Expected result:** `Query OK, 2 rows affected` (ids `101` and `102`; id `105` was deleted in the previous step).

### 15. Update an employee's salary by id

```sql
UPDATE employee
SET salary = 95000.00
WHERE id = 100;
```

**What it does:** Sets Alex's salary to `95000.00` and leaves the other fields unchanged.

**Expected result:** `Query OK, 1 row affected`.

Verify the update:

```sql
SELECT * FROM employee WHERE id = 100;
```

**Expected result:** Alex's row now has salary `95000.00`.

> Run the create and insert steps once in a fresh practice database. If you rerun them, MySQL reports an error because the database, table, and primary-key ids already exist.
