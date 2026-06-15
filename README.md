# 🕵️ Job Scout

A local, private lightweight command-line tool for scanning job listings across **LinkedIn** and **Indeed**. It fetches recent job postings, filters them by location and keywords, and displays them in a clean, readable table format directly in your terminal. 



https://github.com/user-attachments/assets/06e32817-8b4f-4d16-8d53-4d664359adb5



🛠️ Why this matters: Built to automate and streamline my own daily job search pipeline. Constructed with Python to demonstrate robust web scraping, error handling, and data structuring—the foundational steps for any future AI-driven data pipeline.

**PLEASE NOTE:** JobScout is capped to 3 days / 72 hours to keep listings fresh.

## 🚀 Features

- **Multi-Source Scraping**: Simultaneously searches LinkedIn and Indeed.
- **Clean Output**: Displays results in a formatted table using `prettytable`.
- **Smart Location Handling**: Automatically detects country for Indeed's API requirements.
- **Error Resilient**: Gracefully handles scraping failures without crashing.
- **Local & Private**: Processes all data locally on your machine with zero external data logging.
## 🛠️ Prerequisites

- Python 3.8+
- `pip`

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/js-rock/jobscout.git
   cd jobscout
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

### Option 2: Use the Standalone Executable (Windows/macOS - coming soon)
A pre-compiled binary created using **PyInstaller** is currently being prepared for distribution. This will allow users to run the tool without installing Python or dependencies. 
> *Updates will be posted in the [Releases](https://github.com/js-rock/jobscout/releases) section.*
```
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

### 📊 Dashboard Generation
Upon completion, the tool automatically generates a file named `australian_job_leads.html` in your root directory. This provides a persistent, searchable, and click-ready HTML dashboard of your local search results.

## ⚠️ Platform Compatibility & Limitations 

This project aggregates data from LinkedIn and Indeed. Integrations for local Australian platforms (like SEEK/Jora) or Google Jobs were evaluated; however, these platforms enforce strict bot-protection and anti-scraping policies to protect their proprietary data. This project prioritizes stability and compliance by focusing on platforms that support ethical, open-source data aggregation.

## 🔮 Future Roadmap 
- Automated Email Alerts: Integrating smtplib to email the HTML report automatically once a scan finishes.

- Proxy Rotation: Implementing rotating residential proxies to improve success rates on high-security job boards.

- AI Filtering: Using a small LLM (like Ollama or GPT-4o-mini) to "score" job descriptions against the user's CV to calculate a "match percentage."

## 🐛 Troubleshooting

- **"Scraper error:** Invalid location": The tool is currently optimized for the Australian job market. Please ensure you are entering valid Australian location strings (e.g., "Sydney", "Melbourne"). The application handles the country-specific API formatting automatically.
- **No Results**: Some job sites block automated requests. If you receive no data, wait a few minutes and try again.

## 🙏 Acknowledgements

This project is inspired by JobSpy. Many thanks to the contributors for their excellent work on the core scraping logic.

## 📬 Support

For issues or feature requests, please open an issue on GitHub.

## 📜 License

This project is for educational and personal use only. By using this tool, you agree to comply with the Terms of Service of LinkedIn, Indeed, and other third-party sites.