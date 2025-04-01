# Project Plan: Automated News Reporter

## 1. Goals

* Automate the process of gathering news based on predefined geographical scopes (local, regional, national, global).
* Utilize AI (OpenAI GPT-4o) via the Tavily Search API to summarize and format the gathered news into concise reports.
* Generate `.docx` document files for each report.
* Automatically send the generated `.docx` files to the default system printer.
* Ensure API keys are handled securely using environment variables and a `.env` file.

## 2. Core Features (Current)

* **News Search:** Queries the Tavily API for news based on hardcoded locations/scopes.
* **AI Summarization:** Sends search results to OpenAI API (GPT-4o) for summarization and formatting into a news report structure.
* **DOCX Generation:** Creates a `.docx` file for each generated report using `python-docx`.
* **Automated Printing:** Attempts to print generated `.docx` files using OS-specific commands (`os.startfile` for Windows, `lp` for macOS/Linux).
* **Secure API Key Handling:** Loads API keys from a `.env` file.
* **Basic Error Handling:** Includes `try...except` blocks for API calls, file saving, and printing.

## 3. Potential Future Features / Milestones

* **Configuration File:** Move queries and potentially API model choices into a configuration file (e.g., `config.yaml`, `config.json`) instead of hardcoding them in `main.py`.
* **Improved DOCX Formatting:** Leverage more `python-docx` features to apply styles (headings, paragraphs, bolding) based on the AI's output structure, rather than just adding one large text block.
* **Enhanced Error Handling:** Implement more specific exception catching and provide more informative error messages. Add retries for transient network errors.
* **Logging:** Implement proper logging (using Python's `logging` module) instead of just `print` statements.
* **User Interface:** Develop a simple GUI (e.g., using Tkinter, PyQt) or Web UI (e.g., using Flask, Streamlit) to trigger the process and view status/results.
* **More Robust Printing:** Investigate platform-specific libraries or methods for more reliable printing, potentially including printer selection.
* **Customizable Prompts:** Allow users to customize the OpenAI prompt via the configuration file.
* **Report Archiving:** Add functionality to archive generated reports in a structured directory (e.g., by date).
* **Parameterization:** Allow passing queries or configuration file paths via command-line arguments.
