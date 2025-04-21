import os
from enum import Enum
from typing import Optional, Tuple
from dotenv import load_dotenv


class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class EnvManager:
    """
    Static utility class for environment management.
    Handles loading environment variables from .env files
    and provides helper methods for environment checks.
    """
    _initialized = False

    @classmethod
    def initialize(cls, env_file: Optional[str] = None) -> None:
        """
        Initialize the environment by loading variables from .env file.
        
        Args:
            env_file: Optional path to custom .env file
        """
        if not cls._initialized:
            load_dotenv(dotenv_path=env_file)
            cls._initialized = True

    @staticmethod
    def get(key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get an environment variable.
        
        Args:
            key: The environment variable name
            default: Optional default value if variable is not set
            
        Returns:
            The environment variable value or default
        """
        return os.environ.get(key, default)

    @staticmethod
    def set(key: str, value: str) -> None:
        """
        Set an environment variable.
        
        Args:
            key: The environment variable name
            value: The value to set
        """
        os.environ[key] = value

    @classmethod
    def get_current_environment(cls) -> Environment:
        """
        Get the current environment.
        
        Returns:
            The current environment (development, staging, or production)
        """
        env = cls.get("ENVIRONMENT", Environment.DEVELOPMENT).lower()
        
        if env == Environment.DEVELOPMENT:
            return Environment.DEVELOPMENT
        elif env == Environment.STAGING:
            return Environment.STAGING
        elif env == Environment.PRODUCTION:
            return Environment.PRODUCTION
        else:
            return Environment.DEVELOPMENT

    @classmethod
    def is_development(cls) -> bool:
        """Check if current environment is development"""
        return cls.get_current_environment() == Environment.DEVELOPMENT

    @classmethod
    def is_staging(cls) -> bool:
        """Check if current environment is staging"""
        return cls.get_current_environment() == Environment.STAGING

    @classmethod
    def is_production(cls) -> bool:
        """Check if current environment is production"""
        return cls.get_current_environment() == Environment.PRODUCTION

    @staticmethod
    def create_dir(dir_name:str) -> Tuple[bool, str]:
        """
        Safely create a directory if it doesn't exist.
        
        Args:
            dir_name: The path of the directory to create
            
        Returns:
            A tuple containing (success, error_message):
                - success: True if directory exists or was created successfully, False otherwise
                - error_message: Empty string on success, exception message on failure
        """
        try:
            if not os.path.exists(dir_name):
                os.makedirs(dir_name, exist_ok=True)
            return True, ""
        except Exception as ex:
            return False, str(ex)

# Initialize environment variables from .env file by default
EnvManager.initialize()

__all__ = ["Environment", "EnvManager"]
