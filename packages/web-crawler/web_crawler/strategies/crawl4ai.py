"""Crawl4AI strategy configuration utilities.

This module provides factory functions and utilities for configuring
and customizing crawl4ai-based web crawling strategies.
"""
from typing import List

# Third-party imports
from crawl4ai import CrawlerRunConfig
from crawl4ai.deep_crawling import BestFirstCrawlingStrategy, BFSDeepCrawlStrategy
from crawl4ai.deep_crawling.scorers import KeywordRelevanceScorer
from crawl4ai.deep_crawling.filters import (
    FilterChain, 
    DomainFilter,
    URLPatternFilter, 
    ContentTypeFilter
)
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.proxy_strategy import ProxyRotationStrategy


def create_bfs_strategy(
    filter_chain: FilterChain,
    proxy_strategy: ProxyRotationStrategy,
    max_depth: int = 2,
    max_pages: int = 50
) -> CrawlerRunConfig:
    """Create a breadth-first search crawling strategy.
    
    This strategy explores pages in a breadth-first manner, visiting all pages
    at the current depth before moving to the next depth level.
    
    Args:
        filter_chain: Chain of filters to apply to URLs during crawling
        proxy_strategy: Strategy for rotating proxies
        max_depth: Maximum depth to crawl (default: 2)
        max_pages: Maximum number of pages to crawl (default: 50)
        
    Returns:
        A configured crawler run configuration
    """
    strategy = BFSDeepCrawlStrategy(
        max_depth=max_depth,
        include_external=False,    # Stay within the same domain
        max_pages=max_pages,
        filter_chain=filter_chain
    )
    
    return CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        scraping_strategy=LXMLWebScrapingStrategy(),
        proxy_rotation_strategy=proxy_strategy,
        stream=True,
        verbose=True
    )


def create_bfcs_strategy(
    scorer: KeywordRelevanceScorer, 
    filter_chain: FilterChain,
    proxy_strategy: ProxyRotationStrategy,
    include_external_links: bool = False,
    max_depth: int = 2, 
    max_pages: int = 25
) -> CrawlerRunConfig:
    """Create a best-first content-scored crawling strategy.
    
    This strategy uses a scoring mechanism to prioritize pages that are 
    more likely to contain relevant content.
    
    Args:
        scorer: Scoring mechanism for prioritizing URLs
        filter_chain: Chain of filters to apply to URLs during crawling
        proxy_strategy: Strategy for rotating proxies
        include_external_links: Whether to include links to external domains (default: False)
        max_depth: Maximum depth to crawl (default: 2)
        max_pages: Maximum number of pages to crawl (default: 25)
        
    Returns:
        A configured crawler run configuration
    """
    assert scorer is not None
    
    strategy = BestFirstCrawlingStrategy(
        max_depth=max_depth,
        include_external=include_external_links,
        url_scorer=scorer,
        max_pages=max_pages,  # Maximum number of pages to crawl
        filter_chain=filter_chain
    )
    
    return CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        scraping_strategy=LXMLWebScrapingStrategy(),
        proxy_rotation_strategy=proxy_strategy,
        stream=True,
        verbose=True
    )


def get_filter(
    allowed_domains: List[str],
    url_patterns: List[str],
    allowed_content_types: List[str]
) -> FilterChain:
    """Create a filter chain for URL filtering.
    
    Args:
        allowed_domains: List of domains to allow
        url_patterns: List of URL patterns to match
        allowed_content_types: List of content types to allow
        
    Returns:
        A configured filter chain
    """
    return FilterChain([
        DomainFilter(allowed_domains=allowed_domains),
        URLPatternFilter(patterns=url_patterns),
        ContentTypeFilter(allowed_types=allowed_content_types),
    ])


def get_relevance_filter(
    keywords: List[str],
    weight: float = 0.7
) -> KeywordRelevanceScorer:
    """Create a keyword relevance scorer for content-based URL scoring.
    
    Args:
        keywords: List of keywords to score relevance against
        weight: Weight to apply to the keyword scoring (default: 0.7)
        
    Returns:
        A configured keyword relevance scorer
    """
    return KeywordRelevanceScorer(
        keywords=keywords,
        weight=weight
    )