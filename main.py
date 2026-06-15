import pandas as pd
import webbrowser
import os
from jobspy import scrape_jobs
from prettytable import PrettyTable
from src.sanitizer import InputSanitizer 

# ------------------------------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------------------------------
def run_job_search(search_term, location):
    print(f"Searching for {search_term} in {location}...")

        # Determine the country for Indeed based on user's location input
    def get_country_from_location(loc):
        if "," in loc:
            country = loc.split(",")[1].strip().lower()
            return country
        return "australia" # default for Indeed scrape

    country = get_country_from_location(location)

    # Try to scrape, but catch the error if it fails
    try:
        jobs = scrape_jobs(
            site_name=['linkedin', 'indeed'], #"seek", "jora",
            search_term=search_term,
            location=location,
            results_wanted=20,
            hours_old=72, #168,
            country_indeed=country
        )
        
        # Check if the result is empty or missing the 'site' column
        if jobs is None or jobs.empty or 'site' not in jobs.columns:
            print("Indeed returned no valid data.")
            return pd.DataFrame() # Return an empty DataFrame
            
        return jobs
    except Exception as e:
        print(f"Scraper error: {e}")
        return pd.DataFrame()

def print_dashboard(df):
    if df is not None and not df.empty:
        table = PrettyTable()
        table.field_names = ["Title", "Company", "Location"]
        
        for _, row in df.iterrows():
            table.add_row([row['title'], row['company'], row['location']])
            
        # This centers the text inside the columns
        table.align = "c" 
        print(table)
    else:
        print("Dashboard empty: No data to display.")

if __name__ == "__main__":
    if os.name == 'nt':
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW("JobScout")

    print("Welcome to JobScout! 🕵️‍♂️")
    # ------------------------------------------------------------------------------------------
    # User Inputs
    # ------------------------------------------------------------------------------------------
    raw_keywords = input(f'Enter job keywords etc "python developer": ').lower() or "Junior AI"
    raw_loc = input(f'Input city + country i.e. "Sydney, Australia" (otherwise default is any, USA): ').lower() or "Sydney, Australia"

    # ------------------------------------------------------------------------------------------
    # Sanitize the user inputs
    # ------------------------------------------------------------------------------------------
    keywords = InputSanitizer.sanitize_text_input(raw_keywords, max_length=100)
    loc = InputSanitizer.sanitize_text_input(raw_loc, max_length=100) 

    if keywords is not None and loc is not None:
        print(f"✅ Inputs sanitized successfully.")
        print(f"   Keywords: {keywords}")
        print(f"   Location: {loc}")
        
        # Check if keywords are too short or meaningless
        if len(keywords.strip()) < 3:
            print("❌ Keywords too short. Please enter at least 3 characters.")
            exit()
        if len(loc.strip()) < 3:
            print("❌ Location too short. Please enter a full city name (e.g., Sydney, Australia).")
            exit()
        # Warn if location looks like random typing
        # Real locations usually have spaces or commas. 
        # Pure random letters are likely typos.
        if ' ' not in loc and ',' not in loc and len(loc) > 5:
            print(f"⚠️  Warning: Your location '{loc}' looks unusual (no spaces or commas).")
            print(f"   JobSpy may default to USA results.")       

        # Proceed with job search
        run_job_search(keywords, loc)
    else:
        print("❌ Invalid input detected. Please check your keywords and location format.")
        print("   Allowed characters: letters, numbers, spaces, hyphens, apostrophes, periods.")
        # Optionally exit or re-prompt here
        exit()

    if not keywords or not loc:
        print("Error: Invalid input. Please try again.")
        # Optionally exit or re-prompt here
        exit()

    # 1. Ingest the raw data matrix from your search query
    results = run_job_search(keywords, loc)

    # 2. PRESENTATION LAYER: Execute your clean, centered PrettyTable terminal display
    print_dashboard(results)

    # 3. METRIC SUMMARY: Output the quick site metrics count below the table
    if not results.empty and 'site' in results.columns:
        print(results['site'].value_counts())
    else:
        print("\nNo source site data telemetry available.")

    # 4. STORAGE LAYER: Silently save the raw data in the background
    if not results.empty:
        try:
            target_order = ['title', 'company', 'location', 'job_url']
            available_columns = [col for col in target_order if col in results.columns]
            output_data = results.reindex(columns=available_columns)
            output_data.columns = [col.upper() for col in output_data.columns]
            
            # The 'justify' parameter is native to Pandas and needs no extra libraries
            output_data.to_html("australian_job_leads.html", 
                                index=False, 
                                render_links=True, 
                                justify='center')
            
            print("\n[SUCCESS] Clean HTML report generated.")
        except Exception as e:
            print(f"\n[WARNING] HTML generation failed: {e}")
            
    print("\nScan complete. Press Enter to close this window. .")
    input()