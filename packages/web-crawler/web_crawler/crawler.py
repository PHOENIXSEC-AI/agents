"""WebCrawler implementation for asynchronous web crawling.

This module provides a WebCrawler class that wraps the AsyncWebCrawler
from crawl4ai and adds functionality for saving results and logging.
"""
import os
import time
import asyncio
from typing import List, Optional

from core.logger import configure_logger, Logger
from core.env import Environment, EnvManager

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

VERSION = "0.1.0"
SERVICE_NAME = 'social-crawler'
C_ENV = Environment.DEVELOPMENT


def save_result(path: str, content: str) -> None:
    """Save crawled content to a file.
    
    Args:
        path: The file path to save the content to
        content: The content to save
    """
    with open(path, 'w') as out_file:
        out_file.write(content)


class WebCrawler:
    """Main web crawler implementation.
    
    This class provides a high-level interface for web crawling, with support
    for different crawling strategies, logging, and result saving.
    """
    
    def __init__(self, result_dir: str = ".tmp_data/"):
        """Initialize the web crawler.
        
        Args:
            result_dir: Directory where crawled results will be saved (default: ".tmp_data/")
        """
        self.logger = self._configure_logger()
        self.crawler = self._configure_crawler()
        
        self.result_dir = result_dir
        is_success, err = EnvManager.create_dir(result_dir)
        if not is_success:
            self.logger.error(err)
            exit()
        
        self.crawler_strategy = None
        
    def _configure_logger(self) -> Logger:
        """Configure and return a logger instance.
        
        Returns:
            Configured logger instance
        """
        return configure_logger(
            service_name=SERVICE_NAME,
            environment=C_ENV,
            service_version=VERSION
        )
    
    def _configure_crawler(self, headless: Optional[bool] = True) -> AsyncWebCrawler:
        """Configure and return an AsyncWebCrawler instance.
        
        Args:
            headless: Whether to run the browser in headless mode (default: True)
            
        Returns:
            Configured AsyncWebCrawler instance
        """
        browser_cfg = BrowserConfig(headless=headless)
        
        # TODO: Pass our logger
        return AsyncWebCrawler(config=browser_cfg)
        
    def set_crawl_strategy(self, strategy_to_use: CrawlerRunConfig) -> None:
        """Set the crawling strategy to use.
        
        Args:
            strategy_to_use: The crawling strategy configuration to use
            
        Raises:
            Exception: If there's an error setting the strategy
        """
        try:
            self.crawler_strategy = strategy_to_use
        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            raise e
    
    async def run(self, url: str) -> None:
        """Run the crawler on the specified URL.
        
        Args:
            url: The starting URL to crawl
            
        Raises:
            AssertionError: If no crawler strategy has been set
        """
        assert self.crawler_strategy is not None, 'Crawler strategy not found. Try running `set_crawl_strategy` first'
        
        async with self.crawler as crawler:
            self.logger.info(f"Running Social Crawler")
            results = []
            
            async for result in await crawler.arun(url=url, config=self.crawler_strategy):
                self.logger.info(f"Crawled: {result.url} (Depth: {result.metadata.get('depth')})")
                
                results.append(result)
                
                result_filename = os.path.join(
                    self.result_dir,
                    result.url.split('/')[-1] + ".md"
                )
                
                save_result(result_filename, result.markdown)
                
                self.logger.info(f"\n✅ Total Crawled {len(results)}")


async def demo() -> None:
    """Run a demonstration of the WebCrawler.
    
    This function demonstrates how to use the WebCrawler with a specific
    crawling strategy.
    """
    from web_crawler.strategies.user import web_content_discovery
    
    url = "https://www.delfi.lt/news/daily/lithuania"
    
    crawl_strategy = web_content_discovery(
        "delfi.lt", 
        url_patterns=["*news/daily/lithuania*"],
        max_pages=10
    )
    
    sc = WebCrawler()
    sc.set_crawl_strategy(strategy_to_use=crawl_strategy)
    
    await sc.run(url)


if __name__ == "__main__":
    asyncio.run(demo())