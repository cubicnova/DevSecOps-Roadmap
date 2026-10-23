# SQL Injection Prevention — Examples

The examples use illustrative database schemas. Placeholder syntax and API details differ by driver; consult the documentation for your selected library.

## 1. Python DB-API: parameterized lookup

```python
def find_user_by_email(cursor, email):
    cursor.execute(
        "SELECT id, email FROM users WHERE email = %s",
        (email,),
    )
    return cursor.fetchone()
```

The SQL string contains the query structure. The driver sends the email as a value, not as SQL syntax. Some drivers use `?` or named placeholders instead of `%s`.

## 2. Python SQLite: use `?` placeholders

```python
import sqlite3

def find_product(connection, product_id):
    connection.row_factory = sqlite3.Row
    return connection.execute(
        "SELECT id, name, price FROM products WHERE id = ?",
        (product_id,),
    ).fetchone()
```

Do not use an f-string to place `product_id` directly into the query.

## 3. Python ORM: Django QuerySet

```python
# Safe ORM filter: the value is handled as query data.
def get_orders_for_customer(customer_id):
    return Order.objects.filter(customer_id=customer_id)
```

Be careful with raw SQL, `extra()`-style legacy patterns, and dynamically assembled expressions. ORM usage is not automatically safe if untrusted strings are inserted into raw SQL.

## 4. Java JDBC: PreparedStatement

```java
String sql = "SELECT id, email FROM users WHERE email = ?";
try (PreparedStatement statement = connection.prepareStatement(sql)) {
    statement.setString(1, email);
    try (ResultSet results = statement.executeQuery()) {
        while (results.next()) {
            System.out.println(results.getLong("id"));
        }
    }
}
```

Do not build the query by concatenating `email` into the SQL string.

## 5. Node.js with a parameterized PostgreSQL query

```javascript
const result = await pool.query(
  "SELECT id, email FROM users WHERE email = $1",
  [email]
);
```

The `$1` placeholder is PostgreSQL-specific. Other database drivers use different parameter syntax.

## 6. PHP PDO

```php
$stmt = $pdo->prepare(
    "SELECT id, email FROM users WHERE email = :email"
);
$stmt->execute(["email" => $email]);
$user = $stmt->fetch();
```

Configure PDO appropriately for your database and driver. Do not concatenate user-controlled data into the SQL statement.

## 7. Safe dynamic sorting with an allow-list

```python
SORT_COLUMNS = {
    "name": "display_name",
    "created": "created_at",
}
SORT_DIRECTIONS = {
    "asc": "ASC",
    "desc": "DESC",
}

def list_users(cursor, sort_key, direction, limit):
    column = SORT_COLUMNS.get(sort_key)
    order = SORT_DIRECTIONS.get(direction.lower())

    if column is None or order is None:
        raise ValueError("Invalid sort option")

    # column and order can only come from the fixed mappings above.
    sql = f"SELECT id, display_name FROM users ORDER BY {column} {order} LIMIT %s"
    cursor.execute(sql, (limit,))
    return cursor.fetchall()
```

This pattern assumes the selected driver accepts `%s` for the `LIMIT` value. Verify the placeholder style for your driver. The dynamic SQL fragments are restricted to fixed code-defined choices.

## 8. Safer update query

```python
def update_display_name(cursor, user_id, display_name):
    cursor.execute(
        "UPDATE users SET display_name = %s WHERE id = %s",
        (display_name, user_id),
    )
```

Validate business constraints such as length and allowed characters separately. Do not treat validation as a substitute for parameterization.

## 9. Stored procedure caution

Calling a stored procedure with parameters can be safe, but a procedure may reintroduce injection if it builds and executes SQL by concatenating input. Review the procedure's implementation as well as the application call.

## 10. Safe error handling

```python
try:
    cursor.execute(
        "SELECT id FROM products WHERE sku = %s",
        (sku,),
    )
except DatabaseError:
    logger.exception("Database lookup failed; request_id=%s", request_id)
    raise ServiceUnavailableError("Unable to complete the request")
```

The exact exception classes depend on the library. Restrict log access and avoid logging credentials or full sensitive payloads. Do not return raw SQL or stack traces to the client.

## Example regression test idea

Given a user-supplied string containing quotes and SQL-looking characters, a parameterized lookup should treat the entire string as one value and should not broaden the query or alter database state. Assert that unrelated records are not returned and that no unintended writes occur.
