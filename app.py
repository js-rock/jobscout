import streamlit as st
import pandas as pd
from jobspy import scrape_jobs
from src.sanitizer import InputSanitizer 
import time

# Page Config
st.set_page_config(page_title="JobScout", page_icon="🕵️‍♂️", layout="wide")

# Title
st.title("🕵️‍♂️ JobScout")
st.markdown("Find jobs from LinkedIn and Indeed instantly.")

# Sidebar for inputs (Cleaner UI)
with st.sidebar:
    st.header("Search Parameters")
    raw_keywords = st.text_input("Job Keywords", value="Web Developer")
    raw_loc = st.text_input("Location", value="Sydney, Australia")

    st.markdown(
        '<h3 style="font-size: 16px; color: #white;">Jobs are capped to 40 max and the past 72 hours</h3>', 
        unsafe_allow_html=True
    )
    
    search_btn = st.button("🔍 Search Jobs", type="primary")

# Helper Function: Get country from location
def get_country_from_location(loc):
    if "," in loc:
        return loc.split(",")[-1].strip().lower()
    return "australia" # Default

# Helper Function: Core Logic (From your main.py)
def run_job_search(search_term, location):
    with st.spinner('Scraping LinkedIn and Indeed...'):
        try:
            jobs = scrape_jobs(
                site_name=['linkedin', 'indeed'],
                search_term=search_term,
                location=location,
                results_wanted=20,
                hours_old=72,
                country_indeed=get_country_from_location(location)
            )
            
            if jobs is None or jobs.empty or 'site' not in jobs.columns:
                return pd.DataFrame()
            
            return jobs
        except Exception as e:
            st.error(f"Scraper Error: {e}")
            return pd.DataFrame()

# Helper Function: Generate HTML Report (From your main.py)
def generate_html_report(df):
    target_order = ['title', 'company', 'location', 'job_url']
    available_columns = [col for col in target_order if col in df.columns]
    output_data = df.reindex(columns=available_columns)
    
    if not available_columns:
        return None
        
    output_data.columns = [col.upper() for col in output_data.columns]
    html_content = output_data.to_html(index=False, render_links=True, justify='center')
    return html_content

# --- Main Execution ---

if search_btn:
    # 1. Sanitize Inputs (Reusing your existing sanitizer)
    keywords = InputSanitizer.sanitize_text_input(raw_keywords, max_length=100)
    loc = InputSanitizer.sanitize_text_input(raw_loc, max_length=100) 

    if not keywords or not loc:
        st.warning("Please enter valid keywords and location.")
    else:
        if len(keywords) < 3:
            st.warning("Keywords must be at least 3 characters.")
        elif len(loc) < 3:
            st.warning("Location must be at least 3 characters.")
        else:
            # *** NEW: Validate Location Format (City, Country) ***
            loc_check = InputSanitizer.validate_location_format(loc)
            
            if not loc_check['valid']:
                st.error(f"❌ Invalid Location: {loc_check['error']}")
            else:
                # ✅ All checks passed. Run the search.
                # We use the validated city/country to ensure correct format for the scraper
                final_location = f"{loc_check['city']}, {loc_check['country']}"
                
                results = run_job_search(keywords, final_location)

                if results is not None and not results.empty:
                    st.success(f"✅ Found {len(results)} jobs!")
                    
                    # 2. Display Data as a DataFrame (Better than table for Streamlit)
                    st.subheader("Results")
                    
                    # Only show columns that exist
                    cols_to_show = ['title', 'company', 'location', 'job_url']
                    available_cols = [c for c in cols_to_show if c in results.columns]
                    
                    # Rename for display if needed, but usually keep original names
                    st.dataframe(results[available_cols].style.highlight_max(axis=0)) # Optional: highlight rows
                  

                    # 3. Site Metrics
                    st.subheader("📊 Site Breakdown")
                    site_counts = results['site'].value_counts()
                    st.bar_chart(site_counts)

                    # 4. Download HTML Report
                    st.subheader("📥 Download Report")
                    html_report = generate_html_report(results)
                    
                    if html_report:
                        st.download_button(
                            label="Download HTML Report",
                            data=html_report.encode("utf-8"),
                            file_name="job_leads.html",
                            mime="text/html"
                        )
                    else:
                        st.info("No HTML report available.")
                        
                else:
                    st.warning("No jobs found. Try adjusting your keywords or location.")

# Footer
st.markdown("---")
st.caption("Powered by JobSpy & Streamlit")