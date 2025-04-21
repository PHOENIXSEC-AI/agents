from dataclasses import dataclass

from pydantic import BaseModel, Field, ConfigDict

from httpx import Timeout, Limits, AsyncHTTPTransport, AsyncBaseTransport, AsyncClient

class NetworkConfigBase(BaseModel):
    """
    Base configuration model for HTTP network settings.
    
    Defines the basic configuration needed for HTTPX clients including
    timeout settings and transport configurations.
    """
    timeout: Timeout = Field(..., description="Timeout configuration for HTTP requests")
    transport: AsyncBaseTransport = Field(..., description="Transport mechanism for HTTP requests")
    
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True) 

@dataclass
class HTTPClientBuilder:
    """
    Factory class for creating and configuring HTTPX client instances.
    
    Provides utilities to generate default configurations and create
    pre-configured AsyncClient instances.
    """
    
    @staticmethod
    def get_default_config() -> NetworkConfigBase:
        """
        Creates a default network configuration with sensible timeout and connection settings.
        
        Returns:
            NetworkConfigBase: A validated configuration object with default settings
        """
        _httpx_timeout = 30
        _httpx_max_connections = 10
        
        _httpx_limits = Limits(max_connections=_httpx_max_connections)
        
        build_kwargs = {
            "timeout": Timeout(timeout=_httpx_timeout, connect=5),
            "transport": AsyncHTTPTransport(limits=_httpx_limits),
        }
        
        return NetworkConfigBase.validate_model(**build_kwargs)
    
    @staticmethod
    def get_httpx_client() -> AsyncClient:
        """
        Creates an AsyncClient instance with default configuration settings.
        
        Returns:
            AsyncClient: A configured HTTPX async client ready for use
        """
        default_config = HTTPClientBuilder.get_default_config()
        return AsyncClient(**default_config)

__all__ = ["HTTPClientBuilder", "NetworkConfigBase"]