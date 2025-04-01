import os
import sys
import requests
import subprocess
from docx import Document
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


client = OpenAI()

def search_news(query):
    """
    Uses Tavily's Search API to search for news articles based on the query.
    Returns a list of result dictionaries.
    """
    url = "https://api.tavily.com/search"
    headers = {
        "Authorization": f"Bearer {TAVILY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"query": query}
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        return results
    except Exception as e:
        print(f"Error during search for query '{query}': {e}")
        return []

def format_news_with_openai(results, level):
    """
    Formats a list of news results into a printed report using the OpenAI API.
    It builds a prompt from the news titles and snippets then asks GPT to
    generate a concise report.
    
    Note: This function now imports ChatCompletion directly, which is the 
    new recommended approach in openai>=1.0.0.
    """
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
        completion = client.chat.completions.create(
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
    """
    Generates a .docx file with the given report text.
    """
    doc = Document()
    doc.add_heading(f"{filename.split('.')[0].replace('_', '')} News Report", 0)
    doc.add_paragraph(report)
    try:
        doc.save(filename)
        print(f"Saved report to {filename}")
    except Exception as e:
        print(f"Error saving file {filename}: {e}")


def print_docx(filename):
    if sys.platform.startswith('win'):
        # Windows: use os.startfile with the "print" action
        try:
            print(f"Sending '{filename}' to the printer on Windows...")
            os.startfile(filename, "print")
        except Exception as e:
            print(f"Error printing '{filename}' on Windows: {e}")
    elif sys.platform.startswith('darwin') or sys.platform.startswith('linux'):
        # macOS/Linux: use the lp command
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
    for level, query in queries.items():
        print(f"Searching for {level} news with query: '{query}'")
        results = search_news(query)
        if not results:
            report = f"No news articles found for {level} news."
        else:
            report = format_news_with_openai(results, level)
        filename = f"{level}_news.docx"
        generate_docx(report, filename)

    print("News report generation completed.\nNow printing the reports...")
    filenames = ["local_news.docx", "regional_news.docx", "national_news.docx", "global_news.docx"]
    for filename in filenames:
        if os.path.exists(filename):
            print_docx(filename)
        else:
            print(f"File '{filename}' does not exist.")
            
if __name__ == "__main__":
    main()
