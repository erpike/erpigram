def migrate(migrator, database, fake=False, **kwargs):
    queries = [
        """CREATE TABLE IF NOT EXISTS user (
            id          INTEGER PRIMARY KEY,
            username    VARCHAR(255),
            email       VARCHAR(255),
            password    VARCHAR(255)
        )""",
    ]
    for q in queries:
        migrator.sql(q)


def rollback(migrator, database, fake=False, **kwargs):
    queries = [
        """DROP TABLE IF EXISTS user""",
    ]
    for q in queries:
        migrator.sql(q)
