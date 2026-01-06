from jobspy import scrape_jobs

def get_jobs(location, keywords):
    """
    Fetch job listings based on location and keywords.
    
    :param location: location string
    :param keywords: keywords list string
    """
    jobs = scrape_jobs(
        site_name=["indeed", "linkedin", "google"], # ziprecruited is geo restricted for EU region
        search_term=keywords,
        google_search_term=f"{keywords} jobs near {location} since yesterday",
        location=location,
        results_wanted=20,
        hours_old=72,
        country_indeed='USA',
        
    )
    
    df = jobs[['id', 'site', 'job_url', 'job_url_direct', 'title', 'company','location', 'date_posted', 'job_type', 'description']].head()
    return df