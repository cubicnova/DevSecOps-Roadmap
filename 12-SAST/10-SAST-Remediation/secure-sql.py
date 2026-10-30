"""Safe parameterized SQL example; adapt placeholder syntax to your DB driver."""


def get_user(cursor, email):
    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,),
    )
    return cursor.fetchall()
