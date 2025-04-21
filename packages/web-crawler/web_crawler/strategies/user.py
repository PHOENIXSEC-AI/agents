"""User-facing web crawling strategies.

This module provides high-level crawling strategies that can be used
directly by WebCrawler to perform common web crawling tasks.
"""
from typing import List

from crawl4ai import CrawlerRunConfig

from web_crawler.strategies.crawl4ai import (
    create_bfcs_strategy,
    create_bfs_strategy,  # Changed from BFS to bfs for consistency
    get_filter,
    get_relevance_filter,
)
from web_crawler.proxies import configure_proxies


def smart_crawl(domain: str) -> CrawlerRunConfig:
    """Create a smart crawling strategy focused on relevance scoring.
    
    This strategy uses breadth-first content-scored (BFCS) approach to
    prioritize pages that are more relevant based on keywords.
    
    Args:
        domain: The domain to crawl (e.g., "example.com")
        
    Returns:
        A configured crawler strategy
    """
    filter = get_filter(
        allowed_domains=[domain],
        allowed_content_types=["text/html"],
        url_patterns=["*news/daily*"]
    )
    
    relevant_keywords = get_relevance_filter(
        keywords=["news", "daily"],
        weight=0.7
    )
    
    _, proxy_strategy = configure_proxies()
    
    crawl_strategy = create_bfcs_strategy(
        scorer=relevant_keywords,
        filter_chain=filter,
        proxy_strategy=proxy_strategy,
        max_pages=10
    )
    
    return crawl_strategy


def web_content_discovery(domain: str, url_patterns: List[str], max_pages:int=25) -> CrawlerRunConfig:
    """Create a web content discovery crawling strategy.
    
    This strategy uses a simple breadth-first search (BFS) approach to
    discover content matching specified URL patterns.
    
    Args:
        domain: The domain to crawl (e.g., "example.com")
        url_patterns: List of URL patterns to match (e.g., ["*/blog/*", "*/news/*"])
        max_pages: Number of pages to crawl
    Returns:
        A configured crawler strategy
    """
    filter = get_filter(
        allowed_domains=[domain],
        allowed_content_types=["text/html"],
        url_patterns=url_patterns
    )
    
    _, proxy_strategy = configure_proxies()

    crawl_strategy = create_bfs_strategy(
        filter_chain=filter,
        proxy_strategy=proxy_strategy,
        max_pages=max_pages
    )
    
    return crawl_strategy
