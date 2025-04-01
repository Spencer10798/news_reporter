import os
import sys
import requests
import subprocess
from docx import Document
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from tavily import TavilyClient

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai_client = OpenAI()
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

def search_news(query):
    try:
        response = tavily_client.search(query=query, search_depth="basic", include_answer=False)
        results = response.get("results", [])
        return results
    except Exception as e:
        print(f"Error during Tavily search for query '{query}': {e}")
        return []

def format_news_with_openai(results, level):
    news_text = ""
    for r in results:
        title = r.get("title", "No Title")
        snippet = r.get("snippet", r.get("content", ""))
        news_text += f"Title: {title}\nSnippet: {snippet}\n\n"

    prompt = (f"Act as a professional news reporter. Based on the following search results, "
              f"create a well-organized and concise news report for {level} news. The report "
              f"should include clear headlines and summary paragraphs. The report should be "
              f"properly formatted for a .docx docuiment.\n\n{news_text}")

    try:
        completion = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "developer", "content": "You are a professional news reporter."},
                {"role": "user", "content": prompt}
            ]
        )
        report = completion.choices[0].message.content
        return report
    except Exception as e:
        print(f"Error generating report with OpenAI: {e}")
        return "Report generation failed."

def generate_docx(report, filename):
    doc = Document()
    doc.add_heading(f"{filename.split('.')[0].replace('_', ' ')} News Report", 0)
    doc.add_paragraph(report)
    try:
        doc.save(filename)
        print(f"Saved report to {filename}")
    except Exception as e:
        print(f"Error saving file {filename}: {e}")

def print_docx(filename):
    if not os.path.exists(filename):
        print(f"File '{filename}' does not exist.")

    if sys.platform.startswith('win'):
        try:
            print(f"Sending '{filename}' to the printer on Windows...")
            os.startfile(filename, "print")
        except Exception as e:
            print(f"Error printing '{filename}' on Windows: {e}")
    elif sys.platform.startswith('darwin') or sys.platform.startswith('linux'):
        try:
            print(f"Sending '{filename}' to the printer on Unix-like system...")
            subprocess.run(["lp", filename], check=True)
        except Exception as e:
            print(f"Error printing '{filename}' on this system: {e}")
    else:
        print("Unsupported operating system for printing.")

def main():
    queries = {
        "local": "Reston, Virginia news",
        "regional": "Northern Virginia news",
        "national": "United States news",
        "global": "Latest global news"
    }

    print("Starting news report generation...")
    generated_files = [] # Keep track of generated files for printing

    for level, query in queries.items():
        print(f"Searching for {level} news with query: '{query}'")
        results = search_news(query)
        if not results:
            print(f"No news articles found for {level} news.") # Provide feedback
            # Decide if you want a docx saying no results or just skip
            # report = f"No news articles found for {level} news."
            continue # Skip this level if no results
        else:
            report = format_news_with_openai(results, level)
            if "Report generation failed." in report:
                 print(f"Skipping document generation for {level} due to report failure.")
                 continue # Skip if report generation failed

        filename = f"{level}_news.docx"
        generate_docx(report, filename)
        if os.path.exists(filename): # Check if doc was actually created
            generated_files.append(filename)
        else:
            print(f"Warning: Failed to create {filename}")


    print("News report generation completed.\nNow printing the reports...")
    if not generated_files:
        print("No reports were successfully generated to print.")
    else:
        for filename in generated_files:
            if os.path.exists(filename):
                print_docx(filename)
            # else: # Already handled in print_docx
            #     print(f"File '{filename}' does not exist.")

if __name__ == "__main__":
    main()
