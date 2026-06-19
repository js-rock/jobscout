import streamlit as st
import pandas as pd
import time
from jobspy import scrape_jobs
from src.sanitizer import InputSanitizer 
from src.utils import normalize_location_for_scraper


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
    #return "australia" # Default

# Helper Function: Core Logic (From main.py)
def run_job_search(search_term, location):
    with st.spinner('Scraping LinkedIn and Indeed...'):
        try:
            jobs = scrape_jobs(
                site_name=['LinkedIn', 'Indeed'],
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

# Helper Function: Generate HTML Report (From main.py)
def generate_html_report(df):
    # 1. Define the desired display order using the ACTUAL column names from jobspy
    # (jobspy usually returns lowercase keys)
    target_order = ['title', 'company', 'location', 'job_url']
    
    # 2. Filter to only columns that actually exist in the DataFrame
    available_columns = [col for col in target_order if col in df.columns]
    
    if not available_columns:
        return None
        
    # 3. Reindex to get the correct order
    output_data = df[available_columns].copy() # Use [] instead of reindex to avoid NaN columns
    
    # 4. Create a mapping for nice headers (Sentence Case)
    # This maps 'title' -> 'Title', 'job_url' -> 'Job URL', etc.
    headers = {
        'title': 'Title',
        'company': 'Company',
        'location': 'Location',
        'job_url': 'Job Link' # or 'URL'
    }
    
    # 5. Apply the new headers using the mapping defined above
    # We only rename the columns that exist in available_columns
    output_data.columns = [headers.get(col, col.title()) for col in output_data.columns]
    
    # 6. Generate HTML
    # note: render_links=True is crucial for job_url to be clickable in the HTML file
    html_content = output_data.to_html(index=False, render_links=True, justify='center')
    return html_content

# --- Main Execution ---

if search_btn:
    # 1. Sanitize Inputs (Reusing existing sanitizer)
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
            # Use the new utility function to get a robust location string
            final_location = normalize_location_for_scraper(loc)
            
            # Optional: Show the user what we normalized it to, so they know what was searched
            st.info(f"📍 Searching for: **{final_location}**")
            
            results = run_job_search(keywords, final_location)

            if results is not None and not results.empty:
                st.success(f"✅ Found {len(results)} jobs!")
                
                # Make df table job_url clickable           
                # Display Data as a DataFrame (Better than table for Streamlit)
                st.subheader("Results")
                
                # Only show columns that exist
                cols_to_show = ['title', 'company', 'location', 'job_url']
                available_cols = [c for c in cols_to_show if c in results.columns]
                    
    
                if 'job_url' in results.columns:
                    # 1. Define the desired display names (Sentence Case)
                    display_columns_map = {
                        'title': 'Title',
                        'company': 'Company',
                        'location': 'Location',
                        'job_url': 'Job Link'
                    }
                    
                    # 2. Determine which columns exist
                    cols_to_show = [c for c in ['title', 'company', 'location', 'job_url'] if c in results.columns]
                    
                    # 3. Create a temporary DataFrame with renamed columns for display
                    display_df = results[cols_to_show].copy()
                    display_df.columns = [display_columns_map.get(col, col.title()) for col in display_df.columns]
                    
                    # 4. Move 'Job Link' to the end for better UX
                    if 'job_url' in cols_to_show:
                        cols_order = [c for c in display_df.columns if c != 'Job Link'] + ['Job Link']
                        display_df = display_df[cols_order]

                    # 5. Highlight numeric columns (if any)
                    numeric_cols = display_df.select_dtypes(include='number').columns
                    if len(numeric_cols) > 0:
                        styled_df = display_df.style.highlight_max(subset=numeric_cols)
                    else:
                        styled_df = display_df

                    # 6. Display with LinkColumn
                    # Note: The column name here MUST match the NEW header 'Job Link'
                    st.dataframe(
                        styled_df,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Job Link": st.column_config.LinkColumn(
                                "Job Link",
                                help="Click to view the job",
                                display_text="View Job"
                            )
                        }
                    )
                else:
                    # Fallback if no job_url column exists
                    numeric_cols = results[cols_to_show].select_dtypes(include='number').columns
                    if len(numeric_cols) > 0:
                        st.dataframe(
                            results[cols_to_show].style.highlight_max(subset=numeric_cols),
                            use_container_width=True,
                            hide_index=True
                        )
                    else:
                        st.dataframe(
                            results[cols_to_show],
                            use_container_width=True,
                            hide_index=True
                        )
                
                # 3. Site Metrics
                st.subheader("📊 Site Breakdown")
                
                # Get counts and convert to a DataFrame
                site_counts = results['site'].value_counts().to_frame()
                site_counts.index.name = 'site'
                
                # Configure the chart to ensure labels are horizontal
                # orientation='h' forces the x-axis to be the index (labels) and y-axis to be the values
                st.bar_chart(
                    site_counts, 
                    height=300,
                    horizontal=True  # This ensures vertical bars with horizontal labels
                )

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