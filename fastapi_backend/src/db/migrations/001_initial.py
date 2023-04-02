def migrate(migrator, database, fake=False, **kwargs):
    queries = [
        """CREATE TABLE IF NOT EXISTS user (
            id          INTEGER PRIMARY KEY,
            username    VARCHAR(255) UNIQUE,
            email       VARCHAR(255) UNIQUE,
            password    VARCHAR(255)
        )""",

        """CREATE TABLE IF NOT EXISTS post (
            id              INTEGER PRIMARY KEY,
            image_url       VARCHAR,
            image_url_type  VARCHAR(255),
            caption         VARCHAR(255),
            timestamp       DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_id         INTEGER NOT NULL REFERENCES user(id)    
        )""",
    ]
    for q in queries:
        migrator.sql(q)


def rollback(migrator, database, fake=False, **kwargs):
    queries = [
        """DROP TABLE IF EXISTS user""",
        """DROP TABLE IF EXISTS post""",
    ]
    for q in queries:
        migrator.sql(q)
