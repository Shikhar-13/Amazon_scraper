# Amazon Scraper Tool

## Overview

The Amazon Scraper is a Python-based tool that automates the process of logging into Amazon, navigating the site, and extracting product information from the Best Sellers page. It uses Selenium for web interaction and supports headless operation.

---

## Features

- **Automated Login**: Logs into Amazon using user-provided credentials.
- **Product Link Extraction**: Collects product links from Amazon Best Sellers categories.
- **Data Collection**: Scrapes key details such as product name, price, discount, ratings, shipping details, and description.
- **CSV Export**: Saves the scraped data into a CSV file for easy access and analysis.
- **Error Handling**: Includes mechanisms to handle timeouts and missing elements.

---

## Prerequisites

- Python 3.7+
- Google Chrome browser
- ChromeDriver (installed automatically via `webdriver-manager`)
- Required Python packages:
  - `selenium`
  - `webdriver-manager`

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/amazon-scraper.git
   cd amazon-scraper
   ```
2. Install the dependencies using pip:
   ```bash
   pip install selenium webdriver-manager
   ```
3. Ensure Google Chrome is installed on your machine.

---

## Usage

1. Run the script:
   ```bash
   python scraper.py
   ```
2. Enter your Amazon email and password when prompted.
3. The script will:
   - Log in to Amazon.
   - Navigate to the Best Sellers page.
   - Scrape product data.
   - Save the data to `output.csv`.

---

## File Structure

```
.
├── scraper.py          # Main script file containing the scraper class and functionality
├── output.csv          # Output file containing the scraped data
├── amazon_scraper.log  # Log file recording the script’s activities and errors
```

---


