import pandas as pd
import webbrowser
import os
from jobspy import scrape_jobs
from prettytable import PrettyTable

# ------------------------------------------------------------------------------------------
# User Inputs
# ------------------------------------------------------------------------------------------
keywords = input(f'Enter job keywords etc "senior dev": ').lower() or "Junior AI"
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
            site_name=["linkedin", "indeed"], #"seek", "jora",
            search_term=search_term,
            location=location,
            results_wanted=20,
            hours_old=72,
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

    # Run the search
    results = run_job_search(keywords, loc)

    # Call the dashboard
    print_dashboard(results)

    # This will show you exactly which site provided which job
    if not results.empty and 'site' in results.columns:
        print(results['site'].value_counts())
    else:
        print("\nNo site data available.")

    print("\nScan complete. Press Enter to close this window. .")
    input()