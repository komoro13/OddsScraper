# Betting Odds Scraper with Telegram Alerts

This Python project scrapes live betting odds from a betting website for soccer matches scheduled within the next three hours. If the odds change by a specified threshold, it sends an alert message to a Telegram channel using a bot.

## Features
Web Scraping: Utilizes undetected_chromedriver and selenium to gather soccer match odds from the Stoiximan website.
Odds Monitoring: Continuously monitors odds and detects changes greater than a defined threshold.
Telegram Integration: Sends alerts to a specified Telegram channel using a bot when significant changes in odds occur.
Dynamic Odds Threshold: Configurable threshold to detect odds percentage changes for Over/Under, 1X2 results, and goal lines.

## Prerequisites

**Python 3.8+**
**Selenium:** pip install selenium
**Undetected ChromeDriver:** pip install undetected-chromedriver
**Requests:** pip install requests
**Telegram Bot:** You need to set up a Telegram bot using BotFather and get your API token and chat ID.
**Google Chrome:** Make sure you have Google Chrome installed.

## Installation

### Clone the repository:

git clone <repository-url>
cd <project-directory>

### Install dependencies:

pip install -r requirements.txt
Setup Telegram Bot:

### Create credentials file

Create a creds.txt file in the root directory containing the CHAT_ID on the first line and the BOT_TOKEN on the second line.
Configure Constants:

### Run the Script:

python odds_scraper.py

## How It Works

**Scraping Odds:** The script scrapes soccer match odds from the Stoiximan website using the undetected_chromedriver to avoid detection by the site.

**Odds Monitoring:** The script continuously checks for changes in odds. It monitors for Over, Under, 1X2 results, and the goals market (e.g., Over/Under 2.5 goals).

**Sending Alerts:** If the percentage change of any odd exceeds the defined threshold (default 10%), a message is generated and sent to a Telegram channel.

**Dynamic Updates:** The script runs in an infinite loop and updates odds every few seconds, ensuring that you get timely alerts on changes in betting odds.

## Configuration
Thresholds: Change the threshold for alerting odds change in the Match_DAT class:

python
THRESHOLD = 10  # percentage of change that triggers an alert

### Time Intervals:

WRITE_TIME: Time window for sending an alert before a match starts.
CHECK_TIME: How frequently the script checks for changes in odds.

## Example Telegram Message

Match: Team A - Team B
Change in Over line
Previous over line: 2.5, Current over line: 2.5
Current odds: 1.85, Previous odds: 1.90
Percentage of change: 2.63%

## Error Handling

The script is designed to continue running even if an exception occurs. If an error is encountered, a debug message is sent to the Telegram channel.

## Troubleshooting

**-Bot not sending messages:** Ensure the bot has permission to send messages to the specified channel. You may need to add the bot to the channel and grant appropriate permissions.

**-No matches being scraped:** Ensure that the website's structure has not changed. If changes occur, the XPATH or class selectors for scraping may need to be updated.

**-Page opening and closing instantly:** Try updating google Chrome or make sure creds.txt is on the same folder and contains the right credentials
