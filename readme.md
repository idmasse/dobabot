# Doba Ops Automation Tool

This repository contains an internal automation tool built to streamline and automate operational workflows related to Doba dropshipping order and catalog management.

The script replaces repetitive, manual actions previously performed through web dashboards by programmatically executing them in a **safe, repeatable, and auditable** way.

---

## Purpose

As order volume and operational complexity increased, certain Doba-related workflows became:

- Time-consuming to perform manually
- Prone to human error
- Difficult to scale consistently

This tool was created to:
- Automate routine operational tasks
- Reduce manual intervention and turnaround time
- Enforce consistency across actions
- Allow Ops to focus on exception handling rather than repetitive work

---

## How It Works

- Uses **Python + Selenium** to automate browser-based workflows that are not exposed via public APIs
- Reads configuration and credentials from environment variables
- Executes deterministic, step-by-step actions against the Doba platform
- Can be run manually or scheduled for hands-off execution

A macOS `plist` file is included to support **scheduled execution** via `launchd`.

---

## What the Automation Does

When executed, the script performs the following actions:

1. **Initialize**
   - Loads required environment variables (URLs, credentials, payment passcode)
   - Initializes a Selenium WebDriver
   - Configures short and long explicit waits for UI stability

2. **Authenticate**
   - Navigates to the Doba login page
   - Enters credentials and signs in
   - Exits safely if login fails

3. **Locate Unpaid Orders**
   - Navigates to the purchase orders page
   - Scans the page for orders marked as *awaiting payment*
   - Exits if no unpaid orders are found

4. **Select Orders and Calculate Totals**
   - Selects all unpaid orders on the page
   - Scrapes:
     - Number of selected orders
     - Grand total payment amount
   - Logs both values for traceability

5. **Proceed to Checkout**
   - Initiates the checkout flow
   - Selects **Doba Credit** as the payment method

6. **Balance Monitoring**
   - Scrapes the remaining Doba credit balance
   - If the balance falls below a predefined threshold ($500), sends an automated email alert prompting a top-up

7. **Submit Payment**
   - Inputs the payment passcode
   - Submits the payment
   - Waits for a success confirmation

8. **Notifications**
   - Sends a summary email on success with:
     - Number of orders paid
     - Total dollar amount processed
   - Sends a failure notification email if any error occurs during execution

9. **Cleanup**
   - Ensures the browser session is closed cleanly in all cases

---

## Project Structure

- **`main.py`**  
  Primary entry point containing the automation logic and overall workflow orchestration.

- **`utils/`**  
  Shared utilities used across the automation workflow.
  - **`selenium_setup.py`** – WebDriver initialization and browser configuration.
  - **`email_utils.py`** – Helper functions for sending success, failure, and alert notifications.

- **`com.doba.plist`**  
  macOS LaunchAgent configuration used to schedule automated runs via `launchd`.

- **`requirements.txt`**  
  Python dependencies required to run the script.

---

## Setup

### Prerequisites
- Python 3.9+
- Google Chrome (or compatible browser)
- Matching ChromeDriver
- macOS (for scheduled execution via `launchd`)

---

### Install Dependencies

```bash
pip install -r requirements.txt