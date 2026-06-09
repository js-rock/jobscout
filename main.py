import pandas as pd
import webbrowser
import os
from jobspy import scrape_jobs
from prettytable import PrettyTable

print("Welcome to JobScout! 🕵️‍♂️")
# ------------------------------------------------------------------------------------------
# User Inputs
# ------------------------------------------------------------------------------------------
keywords = input(f'Enter job keywords etc "python developer": ').lower() or "Junior AI"
loc = input(f'Input city + country i.e. "Sydney, Australia": ').lower() or "Sydney, Australia"

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
            hours_old=168, #72,
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