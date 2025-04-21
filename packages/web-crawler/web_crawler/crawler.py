"""WebCrawler implementation for asynchronous web crawling.

This module provides a WebCrawler class that wraps the AsyncWebCrawler
from crawl4ai and adds functionality for saving results and logging.
It also includes a command-line interface using Click for easy configuration
and execution of crawling tasks.
"""
import os
import asyncio
import click

from typing import List, Optional

from core.logger import configure_logger
from core.env import Environment, EnvManager

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

VERSION = "0.1.0"
SERVICE_NAME = 'social-crawler'
C_ENV = Environment.DEVELOPMENT


logger = configure_logger(
            service_name=SERVICE_NAME,
            environment=C_ENV,
            service_version=VERSION
        )

def save_result(path: str, content: str) -> None:
    """Save crawled content to a file.
    
    Args:
        path: The file path to save the content to
        content: The content to save
    """
    if content:
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
        self.crawler = self._configure_crawler()
        
        self.result_dir = result_dir
        is_success, err = EnvManager.create_dir(result_dir)
        if not is_success:
            logger.error(err)
            exit()
        
        self.crawler_strategy = None
        
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
            logger.error(f"Error: {str(e)}")
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
            logger.info(f"Running Social Crawler")
            result_counter = 0
            async for result in await crawler.arun(url=url, config=self.crawler_strategy):
                logger.info(f"Crawled: {result.url} (Depth: {result.metadata.get('depth')})")
                
                result_filename = os.path.join(
                    self.result_dir,
                    result.url.split('/')[-1] + ".md"
                )
                
                save_result(result_filename, result.markdown)
                
                result_counter+=1
                logger.info(f"\n✅ Total Crawled {result_counter}")


async def run_with_config(config_path: str, url: str) -> None:
    """Run the WebCrawler with a configuration from a file.
    
    This function loads a configuration from the specified file path,
    creates a crawler strategy based on that configuration, and executes
    the crawler on the specified URL.
    
    Args:
        config_path: Path to a JSON configuration file that follows the WebCrawlerConfig schema
        url: The starting URL to crawl
        
    Raises:
        AssertionError: If config_path is None or the file doesn't exist
        Exception: If there's an error loading the configuration file
    """
    from web_crawler.strategies.user import web_content_discovery
    from web_crawler.config import WebCrawlerConfig
    
    assert config_path is not None
    assert os.path.exists(config_path)
    
    # Load configuration from file if provided
    try:
        config = WebCrawlerConfig.from_config_file(config_path)
    except Exception as e:
        logger.error(f"Error loading config file: {e}")
        return
    
    crawl_strategy = web_content_discovery(
        domain=getattr(config, 'site_domain'), 
        url_patterns=getattr(config, 'url_patterns'),
        max_pages=getattr(config, 'max_pages')
    )
    
    sc = WebCrawler()
    sc.set_crawl_strategy(strategy_to_use=crawl_strategy)
    
    await sc.run(url)


@click.command()
@click.argument('url')
@click.option('--config', '-c', required=True, help='Path to configuration JSON file')
def main(url: str, config: str) -> None:
    """Command-line interface for the web crawler.
    
    This function provides a command-line interface for running the web crawler
    on a specified URL with a configuration file.
    
    Args:
        url: The starting URL to crawl
        config: Path to a JSON configuration file
    """
    asyncio.run(run_with_config(config, url))


if __name__ == "__main__":
    main()