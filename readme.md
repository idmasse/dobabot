# Doba Ops Automation Tool

This repository contains an internal automation tool built to streamline and automate operational workflows related to Doba dropshipping order and catalog management.

The script replaces repetitive, manual actions previously performed through web dashboards by programmatically executing them in a safe, repeatable, and auditable way.

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
- Can be scheduled or run on-demand depending on operational needs

A macOS `plist` file is included to support **scheduled execution** via `launchd`.

---

## Project Structure

- **`main.py`**  
  Primary entry point for the automation logic.

- **`com.doba.plist`**  
  macOS LaunchAgent configuration for scheduling automated runs.

- **`requirements.txt`**  
  Python dependencies required to run the script.