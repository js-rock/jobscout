# 🕵️ Job Scout

A local, private lightweight command-line tool for scanning job listings across **LinkedIn** and **Indeed**. It fetches recent job postings, filters them by location and keywords, and displays them in a clean, readable table format directly in your terminal. 

🛠️ Why this matters: Built with Python to demonstrate robust web scraping, error handling, and data structuring—the foundational steps for any **future** AI-driven data pipeline.

## 🚀 Features

- **Multi-Source Scraping**: Simultaneously searches LinkedIn and Indeed.
- **Clean Output**: Displays results in a formatted table using `prettytable`.
- **Smart Location Handling**: Automatically detects country for Indeed's API requirements.
- **Error Resilient**: Gracefully handles scraping failures without crashing.
- **Zero Dependencies for Data**: Runs entirely on standard Python libraries and `jobspy`.

## 🛠️ Prerequisites

- Python 3.8+
- `pip`

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/jobs-ai-agent.git
   cd jobs-ai-agent
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   > **Note:** If `requirements.txt` is missing, install these packages:
   > ```bash
   > pip install jobspy prettytable pandas
   > ```

## 🏃 Usage

Run the script:

```bash
python main.py
```

1. **Enter Keywords**: Input job titles or skills separated by commas (e.g., `Junior AI, Python Developer`).
2. **Enter Location**: Input city and country (e.g., `Sydney, Australia`).
3. **View Results**: The tool will scrape the web and display a table of the most recent jobs.

### Example Output

```
+-----------------------+------------------+------------------+
|       Title           |      Company      |     Location      |
+-----------------------+------------------+------------------+
| AI Engineer Intern    | TechCorp         | Sydney, Australia|
| Junior Data Scientist | InnovateLtd      | Melbourne, Aus   |
+-----------------------+------------------+------------------+

Scan complete. Press Enter to close this window.
```

## 🐛 Troubleshooting

- **"Scraper error: Invalid country string"**: Ensure you enter the country in English (e.g., "Australia", "United States"). The tool automatically formats this for the API.
- **No Results**: Some job sites block automated requests. If you receive no data, wait a few minutes and try again.

## 📜 License

This project is for educational and personal use only. By using this tool, you agree to comply with the Terms of Service of LinkedIn, Indeed, and other third-party sites.

## 📬 Support

For issues or feature requests, please open an issue on GitHub.