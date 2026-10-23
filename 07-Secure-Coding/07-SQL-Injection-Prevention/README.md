# SQL Injection Prevention

This module teaches practical techniques for preventing SQL injection in web applications, APIs, and database-backed services. The emphasis is on secure implementation, code review, and authorized testing in local labs.

## Learning objectives

By the end of this module, you should be able to:

- Explain how SQL injection occurs when untrusted input changes query structure.
- Replace string-concatenated SQL with parameterized queries.
- Use ORM query APIs safely and recognize unsafe raw-query patterns.
- Safely handle dynamic identifiers such as column names and sort directions.
- Apply least privilege, safe error handling, and secure database configuration.
- Test positive and negative cases and identify likely injection sinks during code review.

## What is SQL injection?

SQL injection occurs when an application builds a SQL statement by combining SQL syntax with untrusted input, allowing input to change the meaning of the query. Depending on the query and database privileges, impact may include unauthorized data access, data modification, or deletion.

**Core rule:** keep SQL code separate from data. Use prepared statements / parameterized queries instead of concatenating user input into SQL.

## Unsafe vs. safe query construction

Unsafe pattern:

```python
# UNSAFE: user input becomes part of the SQL syntax.
sql = "SELECT id, email FROM users WHERE email = '" + email + "'"
cursor.execute(sql)
```

Safe pattern:

```python
# SAFE: SQL structure is fixed; email is passed separately as data.
cursor.execute(
    "SELECT id, email FROM users WHERE email = %s",
    (email,),
)
```

The placeholder syntax varies by database driver. Use the parameter style documented by your driver; do not copy `%s`, `?`, or `:name` blindly across libraries.

## Primary prevention techniques

1. **Parameterized queries:** preferred for values in `WHERE`, `INSERT`, `UPDATE`, and `DELETE` clauses.
2. **Safe ORM APIs:** use query builders and ORM filters as designed; avoid concatenating untrusted values into raw SQL fragments.
3. **Allow-list dynamic identifiers:** parameters usually cannot stand for table names, column names, or `ASC`/`DESC`. Map user choices to a fixed set of code-defined identifiers.
4. **Safely implemented stored procedures:** parameterize values inside the procedure and avoid unsafe dynamic SQL.
5. **Input validation:** validate type, length, format, and business constraints as a secondary control; validation alone does not replace parameterization.
6. **Least privilege:** use separate, minimally privileged database accounts; do not connect as a database administrator.
7. **Safe error handling:** return generic errors to clients while recording useful diagnostic details in restricted logs.

OWASP identifies parameterized queries as a primary defense, recommends allow-listing dynamic identifiers, and discourages relying on escaping all input as the main defense. See the references below.

## Dynamic sorting: allow-list the identifier

Bind variables protect values, not arbitrary SQL syntax. Do not insert a user-provided column name directly into a query.

```python
SORT_COLUMNS = {
    "name": "display_name",
    "created": "created_at",
}
SORT_DIRECTIONS = {
    "ascending": "ASC",
    "descending": "DESC",
}

def build_order_clause(sort_key, direction):
    column = SORT_COLUMNS.get(sort_key)
    order = SORT_DIRECTIONS.get(direction)

    if column is None or order is None:
        raise ValueError("Unsupported sort option")

    return f"ORDER BY {column} {order}"
```

Only fixed, code-defined strings are interpolated. All actual data values in the query should still be passed as parameters.

## Defense-in-depth checklist

- [ ] Parameterize all untrusted values in SQL queries.
- [ ] Review raw SQL, query builders, stored procedures, and report/export queries.
- [ ] Allow-list any dynamic identifier or SQL fragment.
- [ ] Validate inputs for expected type, length, and business meaning.
- [ ] Use a least-privileged database identity.
- [ ] Keep credentials outside source code and repository history.
- [ ] Do not expose SQL statements, stack traces, or database errors to clients.
- [ ] Log errors safely; do not log passwords, access tokens, or sensitive records.
- [ ] Test special-character inputs as ordinary data, without allowing query structure to change.
- [ ] Include regression tests for every fixed vulnerability.
- [ ] Run static analysis and review database access code during code review.

## Code-review red flags

- SQL created with `+`, f-strings, string interpolation, or template substitution using request data.
- Dynamic `ORDER BY`, table, schema, or column names sourced directly from the client.
- ORM methods that execute raw SQL built from untrusted strings.
- Stored procedures that concatenate values into dynamic SQL.
- Database credentials with unnecessary `CREATE`, `DROP`, administrative, or broad write privileges.
- Detailed database exceptions returned directly to users.

## Safe practice boundaries

Use a local demo database, intentionally vulnerable training application, or a system for which you have explicit authorization. Do not probe third-party or production systems without permission.

## Further reading

- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [OWASP Query Parameterization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet.html)
- [OWASP Secure Database Access](https://devguide.owasp.org/en/04-design/02-web-app-checklist/03-secure-database-access/)
- [OWASP Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html)
