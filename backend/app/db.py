import os

from dotenv import load_dotenv

load_dotenv()

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
                "port": int(os.getenv("MYSQL_PORT", "3306")),
                "user": os.getenv("MYSQL_USER", "book_admin"),
                "password": os.getenv("MYSQL_PASSWORD", "change-me"),
                "database": os.getenv("MYSQL_DATABASE", "book_manager"),
                "charset": "utf8mb4",
            },
        }
    },
    "apps": {
        "models": {
            "models": ["app.models.book"],
            "default_connection": "default",
        }
    },
    "use_tz": True,
    "timezone": "Asia/Shanghai",
}
