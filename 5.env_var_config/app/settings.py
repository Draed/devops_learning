"""
Todo app (fast api) setting module
"""
import os
import sys
import logging
from pathlib import Path
from enum import Enum
from pydantic import Field, validator, ValidationError

from pydantic_settings import BaseSettings

class LogLevel(str, Enum):
    """Class representing log level value using python enum
    """
    CRITICAL = "CRITICAL"
    ERROR    = "ERROR"
    WARNING  = "WARNING"
    INFO     = "INFO"
    DEBUG    = "DEBUG"

class LogOutput(str, Enum):
    """Class representing log output value using python enum
    """
    STDOUT = "STDOUT"   # write to console
    FILE   = "FILE"     # write to a file

class Settings(BaseSettings):
    """Class representing pytdantic configuration for fast api

    Attributes:
        app_name: application name
        host: Host address to bind
            The default value is ``127.0.0.1``.
        port: Port number on which to bind the app (1-65535)
            The default value is ``8000``.
        log_level: Logging level for the app (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            The default value is ``INFO``.
        log_output: Logging output for the app (STDOUT, FILE)
            The default value is ``STDOUT``.
        log_file: Logging file in case using log_output = file
            The default value is ``the application name .log``.
    """
    ## The ellipsis (...) tells pydantic that the field is required; if it cannot be sourced from either the .env file or the OS environment, a ValidationError is raised.
    app_name: str = Field(..., description="application name")
    host: str = Field("127.0.0.1", description="Host address to bind")
    port: int = Field(8000, ge=1, le=65535, description="Port number (1-65535)")

    ## Default log level - falls back to INFO when neither .env nor OS env provides it
    log_level: LogLevel = Field(LogLevel.INFO, description="Logging level for the app (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
    log_output: LogOutput = Field(LogOutput.STDOUT, description="Where to send logs - console or file")
    log_file: str = Field(f"./{app_name}.log", description="Path to log file when log_output=FILE")

    @validator("log_file")
    def file_must_be_writable(cls, v, values):
        ## Only validate when the user asked for file output
        if values.get("log_output") == LogOutput.FILE:
            p = Path(v)
            if p.is_dir():
                raise ValueError("log_file must be a file, not a directory")
            ## Ensure parent directory exists (create if needed)
            p.parent.mkdir(parents=True, exist_ok=True)
        return v

    class Config:
        """Class representing application custom configuration parameters

        Attributes:
            env_file: default env file name to load settings from
                The default value is ``.env``.
            env_file_encoding: enf file format from which to load settings
                The default value is ``utf-8``.
        """
        ## ``env_file`` is optional - pydantic will ignore it if the file is absent
        env_file = ".env"
        env_file_encoding = "utf-8"

def load_settings() -> Settings:
    ## Check whether a .env file exists
    env_path = Path(".env")
    if env_path.is_file():
        logging.info("Loading configuration from .env file")
    else:
        logging.info(".env file not found - using only OS environment variables")

    ## Attempt to create the Settings instance
    try:
        ## pydantic reads .env (if present) + os.environ
        return Settings()
    except ValidationError as exc:
        ## If required variables missing then show a clear message and exit
        missing = "\n".join(
            f"  • {err['loc'][0]}: {err['msg']}"
            for err in exc.errors()
        )
        logging.error("Configuration error - required variables are missing:\n%s", missing)
        sys.exit(1)

settings = load_settings()

