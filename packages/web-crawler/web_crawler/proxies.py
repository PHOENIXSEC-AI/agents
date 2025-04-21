"""Proxy configuration utilities for web crawling.

This module provides functions for loading and configuring proxies
to be used with the web crawler.
"""
import os
from typing import List, Optional, Tuple

from core.env import EnvManager
from crawl4ai.proxy_strategy import ProxyConfig, RoundRobinProxyStrategy, ProxyRotationStrategy


def load_proxies_from_file(proxies_file_path: Optional[str] = None) -> List[str]:
    """Load proxies from a colon-separated(CSV) file and set environment variables.
    
    Expected file format:
    ip:port:username:password
    (one proxy per line)
    
    Side effects:
    - Sets PROXIES env var: Comma-separated list of all proxies
    - Sets PROXY_COUNT env var: Total number of proxies available
    
    Args:
        proxies_file_path: Path to the proxy configuration file
        
    Returns:
        List[str]: List of proxy strings in format "ip:port:username:password"
        
    Raises:
        FileNotFoundError: If the proxy file doesn't exist
        ValueError: If any proxy line is improperly formatted or if proxy file path is missing
    """
    proxies = []
    
    if not proxies_file_path:
        proxies_file_path = EnvManager.get('PROXIES_FILE', None)
        if not proxies_file_path:
            raise ValueError(
                "Proxy file is missing. Either provide `proxies_file_path` when calling "
                "`load_proxies_from_file` or set `PROXIES_FILE` env variable"
            )
    
    if not os.path.exists(proxies_file_path):
        raise FileNotFoundError(f"Proxy file not found: {proxies_file_path}")
    
    with open(proxies_file_path, 'r') as f:
        lines = f.readlines()
        
        if not lines:
            raise ValueError("Proxy file is empty")
            
        for idx, line in enumerate(lines):
            line = line.strip()
            if not line:  # Skip empty lines
                continue
                
            parts = line.split(':')
            if len(parts) == 4:
                ip, port, user, passwd = parts
                # Basic validation could be added here
                proxies.append(f"{ip}:{port}:{user}:{passwd}")
            else:
                raise ValueError(
                    f"Invalid proxy at line {idx+1}: Expected format "
                    f"'ip:port:username:password', got '{line}'"
                )
    
    EnvManager.set('PROXIES', ','.join(proxies))
    EnvManager.set('PROXY_COUNT', str(len(proxies)))  # Ensure it's a string
    
    return proxies


def configure_proxies() -> Tuple[List[ProxyConfig], ProxyRotationStrategy]:
    """Configure proxies for use with the web crawler.
    
    This function loads proxies from a file (specified in environment variables)
    and configures them for use with the crawler.
    
    Returns:
        Tuple containing:
            - List of proxy configurations
            - Proxy rotation strategy instance
    """
    proxy_configs: List[ProxyConfig] = []
        
    proxies = load_proxies_from_file()  # Using file path specified in .env
    
    # Parse raw str proxies into required format
    for proxy in proxies:
        proxy_cfg = ProxyConfig.from_string(proxy)
        proxy_configs.append(proxy_cfg)
    
    proxy_strategy = RoundRobinProxyStrategy(proxy_configs)
    
    return (proxy_configs, proxy_strategy)