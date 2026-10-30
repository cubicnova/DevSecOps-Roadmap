# SQL Injection Prevention — Exercises

Complete these exercises in a local project or a code review of software you own or are authorized to assess.

## Exercise 1: Identify the unsafe query

```python
def search_products(cursor, term):
    sql = f"SELECT id, name FROM products WHERE name LIKE '%{term}%'"
    cursor.execute(sql)
    return cursor.fetchall()
```

1. Explain why the query is unsafe.
2. Rewrite it using the parameter style of your chosen database driver.
3. Describe a regression test that verifies the input is treated as data.

## Exercise 2: Choose a defense

For each situation, choose an appropriate control:

- A user searches for an account by email.
- A user selects a sort column.
- A report filters records by date.
- An application calls a stored procedure.
- A legacy module uses raw dynamic SQL.

Explain where parameterization applies and where an allow-list is required.

## Exercise 3: Audit a login query

Review this pseudocode:

```python
sql = (
    "SELECT id FROM users WHERE username = '"
    + username
    + "' AND password_hash = '"
    + password_hash
    + "'"
)
cursor.execute(sql)
```

Identify the risks and propose a safer authentication data-access design. Include password-hash verification outside the SQL comparison where appropriate.

## Exercise 4: Dynamic sorting

An endpoint accepts `sort` and `direction` parameters. Design an allow-list mapping for `name`, `created_at`, and `price`, and for ascending/descending order. Reject all unsupported values. Keep filter values parameterized.

## Exercise 5: ORM review

A developer says, “We use an ORM, so SQL injection is impossible.”

Explain why this statement is too broad. Identify safe ORM filters and risky raw-query patterns, and outline a code-review checklist.

## Exercise 6: Stored procedure review

A stored procedure accepts a search term and concatenates it into a dynamic SQL statement before execution.

1. Why does putting the logic in a stored procedure not automatically make it safe?
2. Suggest a parameterized implementation approach.
3. List the privileges the application database identity should and should not have.

## Exercise 7: Least privilege

A web application connects to its database as an account with full administrative rights. Recommend a safer privilege design for a read-only catalog endpoint and a separate account-registration endpoint.

## Exercise 8: Error handling

An API returns database exception messages directly to users.

Explain what information may leak and propose a client response, logging approach, and monitoring signal.

## Exercise 9: Write regression tests

Create tests for a parameterized product search and update function. Include:
- Normal input.
- Empty input.
- Quotes and special characters.
- Very long input.
- A value that resembles SQL syntax.
- Invalid data type or failed validation.

Describe the expected outcome for each case.

## Exercise 10: Code-review checklist

Review a fictional application with queries in controllers, repositories, scheduled jobs, CSV exports, and admin reports. Write a checklist to ensure all database access paths are covered.

## Exercise 11: Safe lab investigation

In an intentionally vulnerable local app, compare an unsafe concatenated query with a parameterized version using harmless test records. Record:
- The vulnerable source line.
- The data flow from input to query.
- The corrected code.
- A regression test.
- A least-privilege improvement.

Do not run tests against systems without explicit authorization.

## Exercise 12: Mini-project

Build a small CRUD API backed by SQLite or PostgreSQL. Include:

- Parameterized create, read, update, and delete queries.
- An ORM filter or repository abstraction.
- Allow-listed sorting.
- Input type and length validation.
- A least-privileged database account for the deployed environment.
- Safe error handling and audit logging.
- Unit tests and integration tests for normal and SQL-looking inputs.

**Acceptance criteria:** user input cannot change query structure; unsupported dynamic identifiers are rejected; tests confirm no unintended records are exposed or modified.
