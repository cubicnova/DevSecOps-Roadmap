# SQL Injection Prevention — Suggested Solutions

These are reference solutions. Adjust placeholder syntax, exception classes, transaction handling, and connection management for the database driver and framework you use.

## Solution 1: Parameterized search

The f-string inserts `term` into the SQL text, allowing the input to affect query structure.

For a driver that uses `%s` placeholders:

```python
def search_products(cursor, term):
    pattern = f"%{term}%"
    cursor.execute(
        "SELECT id, name FROM products WHERE name LIKE %s",
        (pattern,),
    )
    return cursor.fetchall()
```

For SQLite, use `?` instead of `%s`. A regression test should confirm a quote-containing or SQL-looking string is handled as a literal search value and does not return unrelated rows or modify data.

## Solution 2: Select defenses

- Email lookup: parameterized value.
- Sort column: fixed allow-list mapping because a bind parameter generally cannot represent an identifier.
- Date filter: parameterized values, with date parsing and range validation.
- Stored procedure: parameterize its arguments and review the procedure for unsafe dynamic SQL.
- Legacy raw SQL: replace concatenation with parameterization; use a narrowly defined allow-list for unavoidable dynamic identifiers. Do not rely on blanket escaping.

## Solution 3: Login query

Do not concatenate either username or password-derived data into SQL. Query the user by username with a parameterized statement, retrieve the stored password hash, and verify the submitted password using the password-hashing library appropriate to the system. Use generic authentication failures so the response does not reveal whether a username exists.

```python
cursor.execute(
    "SELECT id, password_hash, is_active FROM users WHERE username = %s",
    (username,),
)
record = cursor.fetchone()

if not record or not record.is_active:
    return authentication_failed()

if not password_hasher.verify(submitted_password, record.password_hash):
    return authentication_failed()

return create_authenticated_session(record.id)
```

The placeholder and record access syntax depend on the driver. Apply rate limiting and secure session handling as separate controls.

## Solution 4: Dynamic sorting

```python
SORT_COLUMNS = {
    "name": "name",
    "created_at": "created_at",
    "price": "price",
}
SORT_DIRECTIONS = {
    "ascending": "ASC",
    "descending": "DESC",
}

def make_sort_clause(sort_key, direction):
    column = SORT_COLUMNS.get(sort_key)
    order = SORT_DIRECTIONS.get(direction)

    if column is None or order is None:
        raise ValueError("Unsupported sort option")

    return f"ORDER BY {column} {order}"
```

Only the mapped strings are interpolated. All filter values should still use bind parameters. Use the driver's parameter style for limit/offset values and verify its support.

## Solution 5: ORM review

ORM filters usually parameterize values, but unsafe raw SQL, dynamically assembled fragments, and some expression APIs can still introduce injection. Review all raw query calls and ensure the ORM's documented parameter-binding API is used. Dynamic table or column names should come from code-defined allow-lists.

## Solution 6: Stored procedure review

A stored procedure can still be vulnerable if it concatenates input into dynamic SQL. Prefer static SQL within the procedure or the database's supported parameterized dynamic-SQL mechanism. Grant the application only the execute or table privileges needed for its operations; do not grant administrative, schema-altering, or broad database-owner privileges without a documented requirement.

## Solution 7: Least privilege

For a catalog endpoint, use a database identity with read-only access to the required tables or a limited view. For account registration, use an identity with only the required insert privileges and any narrowly required reads. Keep credentials separate, rotate them appropriately, and do not reuse a DBA account for the application.

## Solution 8: Error handling

Raw database errors can expose schema names, SQL statements, database versions, table/column names, and implementation details. Return a generic controlled error and correlation ID. Log diagnostic details in a restricted logging system, redact secrets, and monitor repeated query failures or unusual error patterns.

## Solution 9: Regression tests

- Normal input: returns expected matching rows.
- Empty input: follows the documented search behavior.
- Quotes/special characters: treated as literal data; no query structure changes.
- Very long input: rejected or handled according to a documented length limit.
- SQL-looking string: does not broaden results or cause writes.
- Invalid type: rejected before query execution or safely converted using a defined schema.

Test database state before and after suspicious-looking values to confirm there are no unintended writes.

## Solution 10: Code-review checklist

Search all controllers, repositories, background jobs, exports, reporting code, stored procedures, and admin endpoints for raw SQL and dynamic query construction. Verify parameterization, allow-listed identifiers, least privilege, safe errors, and tests. Review data flow from request, message, file, or job input to the database execution call.

## Solution 11: Safe lab investigation

Document the unsafe concatenation and the exact source of the input. Replace it with a prepared statement, add a regression test that demonstrates the input is treated as data, and reduce database permissions so the application identity can perform only required operations. Keep the test in a local authorized environment.

## Solution 12: Mini-project checklist

A complete solution should have:
- Parameterized values in all CRUD operations.
- Allow-listed sort keys and sort direction.
- Validation of type, length, and business constraints.
- No credentials committed to source control.
- Least-privileged deployment credentials.
- Generic client errors and protected diagnostic logs.
- Tests for normal and SQL-looking inputs.
- Review of ORM raw-query APIs and stored procedures.

## Further reading

- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [OWASP Query Parameterization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet.html)
- [OWASP Secure Database Access](https://devguide.owasp.org/en/04-design/02-web-app-checklist/03-secure-database-access/)
