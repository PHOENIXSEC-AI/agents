# Agents Monorepo

![Status: Active](https://img.shields.io/badge/Status-Active-green)
![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A modern monorepo for building, deploying, and managing AI agents.

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Development](#-development)
- [Packages](#-packages)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

## 📚 Overview

This monorepo contains a collection of Python packages for AI agents. It provides a unified development experience while maintaining the modularity of separate components.

## 🏛️ Architecture

The Agents Monorepo follows a modular architecture with these key principles:

- **Shared Core:** Common utilities and interfaces in the `shared/` directory
- **Specialized Agents:** Individual agent implementations in the `packages/` directory
- **Dependency Isolation:** Each package manages its dependencies while leveraging shared components
- **Consistent Tooling:** Unified development tools and workflows across all packages

## 🏗️ Project Structure

```
agents/
├── packages/           # Individual agent packages
│   ├── web-crawler/    # Web crawling agent
│   └── ...             # Other agent packages
├── shared/             # Shared libraries and utilities
│   └── core/           # Core shared functionality
├── scripts/            # Build and utility scripts
└── .devcontainer/      # Development container configuration
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/) (for dependency management)
- Make (optional, for build scripts)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd agents
   ```

2. Copy the environment variable template:
   ```bash
   cp .env.sample .env
   ```

3. Install all dependencies:
   ```bash
   make install-full
   ```

## 🛠️ Development

### Common Tasks

```bash
# Install all dependencies
make install-full

# Update poetry.lock files without changing versions
make update-lock

# Update all dependencies to their latest versions
make update

# Clean up Python cache files
make clean-pyc

# Clean up test artifacts
make clean-test

# Clean everything
make clean-all
```

### Development Workflow

1. Work on a specific package within the `packages/` directory
2. Use shared code from the `shared/` directory for common functionality
3. Run tests for your specific package

## 📦 Packages

### Web Crawler

A powerful agent for crawling and extracting data from web sources. The web crawler supports parallel processing, custom extraction rules, and various output formats.

```bash
# Navigate to package directory
cd packages/web-crawler

# Assuming make install-full was run from the root
source .venv/bin/activate

# Run the initial setup
crawl4ai-setup

# Run the crawler for demo
python web_crawler/crawler.py https://news.ycombinator.com/ --config sample_crawler_config.json
```

### Shared Core

Core libraries and utilities shared across packages, including:

- Networking utilities
- Data processing helpers
- Common interfaces for agent development
- Configuration management

```python
from core.env import Environment, EnvManager
from core.logger import configure_logger, Logger

# And much more..
```

## 🧪 Testing


```bash

```

## 🔧 Troubleshooting

### Common Issues

**Poetry Installation Problems**

```bash
# If you encounter issues with Poetry, try:
curl -sSL https://install.python-poetry.org | python3 -
```

**Virtual Environment Issues**

```bash
# Remove and recreate virtual environments
make clean-all
make install-full
```

**Package Dependency Conflicts**

```bash
# Update all dependencies to compatible versions
make update
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

