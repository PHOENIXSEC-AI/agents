"""Configuration handling for the web crawler.

This module provides a Pydantic model for managing web crawler configurations,
including loading from JSON files and validating the configuration structure.
"""
import json

from typing import Self, List

from pydantic import BaseModel, Field


class WebCrawlerConfig(BaseModel):
    """Configuration model for the web crawler.
    
    This class defines the structure of crawler configurations, with 
    validation through Pydantic. It includes settings for crawl scope,
    domain limitations, and crawl depth controls.
    
    Attributes:
        site_domain: The target website domain to limit crawling scope
        url_patterns: List of glob patterns to match URLs for crawling
        max_pages: Maximum number of pages to crawl before stopping
    """
    site_domain: str = Field(description="Domain to limit crawling scope (e.g., 'example.com')")
    url_patterns: List[str] = Field(description="Glob patterns to match URLs for crawling (e.g., ['*example.com/news*'])")
    max_pages: int = Field(description="Maximum number of pages to crawl")
    
    @classmethod
    def from_config_file(cls, config_path: str) -> Self:
        """Load and validate a configuration from a JSON file.
        
        Args:
            config_path: Path to the JSON configuration file
            
        Returns:
            A validated WebCrawlerConfig instance
            
        Raises:
            FileNotFoundError: If the config file doesn't exist
            JSONDecodeError: If the config file contains invalid JSON
            ValidationError: If the config data doesn't match the expected schema
        """
        with open(config_path, 'r') as cfg_file:
            config = json.load(cfg_file)
        
        return cls.model_validate(config)