import pandas as pd
import webbrowser
import os
import sys
from jobspy import scrape_jobs
from prettytable import PrettyTable
from src.sanitizer import InputSanitizer 

# ------------------------------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------------------------------
def run_job_search(search_term, city, country):
    """
    Runs the job search using validated city and country components.
    """
    print(f"Searching for '{search_term}' in {city}, {country}...")

    # Build location string for JobSpy (usually accepts 'City, Country')
    location_str = f"{city}, {country}"

    try:
        jobs = scrape_jobs(
            site_name=['linkedin', 'indeed'],
            search_term=search_term,
            location=location_str,
            results_wanted=20,
            hours_old=72,
            country_indeed=country.lower() # Indeed often needs lowercase country code
        )
        
        if jobs is None or jobs.empty or 'site' not in jobs.columns:
            print("❌ Indeed/LinkedIn returned no valid data.")
            return pd.DataFrame()
            
        return jobs
    except Exception as e:
        print(f"❌ Scraper error: {e}")
        return pd.DataFrame()

def print_dashboard(df):
    """
    Presents the clean, centered PrettyTable terminal display
    """
    if df is not None and not df.empty:
        table = PrettyTable()
        table.field_names = ["Title", "Company", "Location"]
        
        for _, row in df.iterrows():
            table.add_row([row['title'], row['company'], row['location']])
            
        table.align = "c" 
        print("\n" + str(table) + "\n")
    else:
        print("Dashboard empty: No data to display.")

def generate_html_report(df):
    """
    Silently saves the raw data in the background
    """
    if not df.empty:
        try:
            target_order = ['title', 'company', 'location', 'job_url']
            available_columns = [col for col in target_order if col in df.columns]
            output_data = df.reindex(columns=available_columns)
            output_data.columns = [col.upper() for col in output_data.columns]
            
            output_data.to_html("australian_job_leads.html", 
                                index=False, 
                                render_links=True, 
                                justify='center')
            print("[SUCCESS] Clean HTML report generated.")
            
            # Optional: Open the file automatically
            # webbrowser.open_new_tab(os.path.abspath("australian_job_leads.html"))
            
        except Exception as e:
            print(f"[WARNING] HTML generation failed: {e}")

if __name__ == "__main__":
    # Set console title for Windows
    if os.name == 'nt':
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleTitleW("JobScout")
        except:
            pass

    print("Welcome to JobScout! 🕵️‍♂️")
    
    # Loop until we have valid input
    while True:
        print("-" * 40)
        raw_keywords = input('Enter job keywords (e.g., "Python Developer"): ').strip() or "Junior AI Engineer"
        raw_loc = input('Input city + country (e.g., "Sydney, Australia" or type quit to exit): ').strip()  or "Sydney, Australia" 
        
        # Check for exit command
        if raw_keywords.strip().lower() == 'quit' or raw_loc.strip().lower() == 'quit':
            print("\nExiting JobScout. Goodbye!")
            sys.exit() # Or just 'break' if you want to fall through to the end

        # 1. Sanitize Keywords
        keywords = InputSanitizer.sanitize_text_input(raw_keywords, max_length=100)
        
        # 2. Validate Location Format
        location_validation = InputSanitizer.validate_location_format(raw_loc)

        # --- Validation Checks ---
        is_valid = True
        error_message = ""

        if len(keywords) < 3:
            is_valid = False
            error_message = "Keywords are too short. Please enter at least 3 characters."
        
        elif not location_validation['valid']:
            is_valid = False
            error_message = f"Invalid Location: {location_validation['error']}"

        if is_valid:
            # If valid, break the loop and proceed
            city = location_validation['city']
            country = location_validation['country']
            break
        else:
            # If invalid, print error and loop back to the top
            print(f"\n❌ Input Error: {error_message}\n")
            print("Please try again...")
    

    # --- Execution (Only reached if inputs are valid) ---
    print(f"\n✅ Searching for '{keywords}' in {city}, {country}...")
    
    results = run_job_search(keywords, city, country)

    # --- Output ---
    if not results.empty:
        print_dashboard(results)
        
        # Metric Summary
        if 'site' in results.columns:
            print("\nSource Metrics:")
            print(results['site'].value_counts())
            
        # Generate HTML Report
        generate_html_report(results)
    else:
        print("\n❌ No jobs found. Please try different keywords or location.")

    print("\nScan complete. Press Enter to close this window...")
    input()