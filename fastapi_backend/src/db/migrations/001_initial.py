def migrate(migrator, database, fake=False, **kwargs):
    queries = [
        """CREATE TABLE IF NOT EXISTS user (
            id          INTEGER         PRIMARY KEY AUTOINCREMENT,
            username    VARCHAR(255)    UNIQUE,
            email       VARCHAR(255)    UNIQUE,
            password    VARCHAR(255)
        )""",

        """CREATE TABLE IF NOT EXISTS post (
            id              INTEGER         PRIMARY KEY AUTOINCREMENT,
            image_url       VARCHAR,
            image_url_type  VARCHAR(255),
            caption         VARCHAR(255),
            timestamp       DATETIME        DEFAULT     CURRENT_TIMESTAMP,
            user_id         INTEGER                     REFERENCES user(id)     ON DELETE SET NULL   
        )""",

        """CREATE TABLE IF NOT EXISTS comment (
            id              INTEGER         PRIMARY KEY AUTOINCREMENT,
            post_id         INTEGER         NOT NULL    REFERENCES post(id)     ON DELETE CASCADE,
            user_id         INTEGER                     REFERENCES user(id)     ON DELETE SET NULL,
            text            TEXT,
            timestamp       DATETIME        DEFAULT     CURRENT_TIMESTAMP
        )""",
    ]
    for q in queries:
        migrator.sql(q)


def rollback(migrator, database, fake=False, **kwargs):
    queries = [
        """DROP TABLE IF EXISTS user""",
        """DROP TABLE IF EXISTS post""",
        """DROP TABLE IF EXISTS comment""",
    ]
    for q in queries:
        migrator.sql(q)
