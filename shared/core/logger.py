import logfire

from typing import Any, Dict, Optional

from core.env import EnvManager

def configure_logger(
    service_name: Optional[str] = None,
    service_version: Optional[str] = None,
    environment: Optional[str] = None,
) -> 'Logger':
    """
    Configure the Logfire logger.
    
    Args:
        service_name: Name of the service being logged
        environment: Environment (dev, staging, prod)
        
    Returns:
        Logger instance for method chaining
    """
    # Determine service, environment, and version for Logfire configuration
    service = service_name or EnvManager.get("SERVICE_NAME", "unnamed-service")
    env = environment or EnvManager.get_current_environment()
    ver = service_version or EnvManager.get("SERVICE_VERSION", "0.1.0")
    
    token = EnvManager.get('LOGFIRE_API_KEY','')
    
    # Configure Logfire with valid keys
    logfire.configure(
        service_name=service,
        service_version=ver,
        environment=env,
        token=token,
        send_to_logfire=bool(token)
    )
    return Logger

def configure_default_logger() -> 'Logger':
    """
    Configure the logger with default settings.
    Uses environment variables SERVICE_NAME and ENVIRONMENT if available.
    
    Returns:
        Logger instance for method chaining
    """
    service_name = EnvManager.get("SERVICE_NAME", "default-service")
    environment = EnvManager.get_current_environment()
    version = EnvManager.get("SERVICE_VERSION", "0.1.0")
    
    return configure_logger(
        service_name=service_name,
        service_version=version,
        environment=environment
    )

class Logger:
    """
    Logger utility class for structured logging with Logfire.
    """
    
    @staticmethod
    def trace(message: str, **kwargs):
        """Log a trace message"""
        logfire.trace(message, **kwargs)

    @staticmethod
    def debug(message: str, **kwargs):
        """Log a debug message"""
        logfire.debug(message, **kwargs)

    @staticmethod
    def info(message: str, **kwargs):
        """Log an info message"""
        logfire.info(message, **kwargs)

    @staticmethod
    def notice(message: str, **kwargs):
        """Log a notice message"""
        logfire.notice(message, **kwargs)

    @staticmethod
    def warn(message: str, **kwargs):
        """Log a warning message"""
        logfire.warn(message, **kwargs)

    @staticmethod
    def error(message: str, **kwargs):
        """Log an error message"""
        logfire.error(message, **kwargs)

    @staticmethod
    def fatal(message: str, **kwargs):
        """Log a fatal message"""
        logfire.fatal(message, **kwargs)

    @staticmethod
    def span(name: str, **kwargs):
        """Create a span context manager"""
        return logfire.span(name, **kwargs)

    @staticmethod
    def traced(func=None, **kwargs):
        """Decorator to trace function execution"""
        return logfire.traced(func, **kwargs)
