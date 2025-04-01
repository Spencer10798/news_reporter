# Setup and Usage Guide

## 1. Prerequisites

* Python 3.11 or higher installed.
* Access to a terminal or command prompt.
* Git (optional, for version control).
* API keys for Tavily and OpenAI.
* A configured default printer accessible by the operating system (if using the print feature).

## 2.  **Activate Virtual Environment:**
    * **Windows (Command Prompt/PowerShell):**
        ```bash
        .\news_reporter_env\Scripts\activate
        ```
    * **macOS/Linux (Bash/Zsh):**
        ```bash
        source news_reporter_env/bin/activate
        ```
    Your terminal prompt should now indicate the active environment (e.g., `(news_reporter_env)`).

## 3. Running the Script

1.  **Ensure Environment is Active:** Make sure your virtual environment (`news_reporter_env`) is activated (see Step 3).
2.  **Execute the Script:** Run the main Python script from the project root directory:
    ```bash
    python main.py
    ```
3.  **Output:**
    * The script will print status messages to the console indicating the search, generation, and printing steps.
    * `.docx` files (e.g., `local_news.docx`, `regional_news.docx`, etc.) will be generated in the project root directory.
    * The script will attempt to send these `.docx` files to your system's default printer. Success depends on OS configuration and printer setup. Error messages will be printed if printing fails.

## 4. Deactivating the Environment

When you are finished working on the project, you can deactivate the virtual environment:
```bash
deactivate
