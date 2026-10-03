import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "3306"))
    db_user: str = os.getenv("DB_USER", "root")
    db_password: str = os.getenv("DB_PASSWORD", "")
    db_name: str = os.getenv("DB_NAME", "employee_analytics")
    app_name: str = "Employee Analytics Warehouse"


settings = AppConfig()
