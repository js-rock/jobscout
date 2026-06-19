def normalize_location_for_scraper(loc: str) -> str:
    """
    Converts any location input into 'City, Country' format.
    Defaults to 'Australia' if no country is specified.
    """
    if not loc:
        return "Sydney, Australia"

    lower_loc = loc.lower()
    
    # 1. Handle "Greater [City] Area" specifically
    if "greater" in lower_loc and "area" in lower_loc:
        city_part = loc.replace("Greater", "").replace(" Area", "").strip()
        if not city_part or len(city_part) < 2:
            city_part = "Sydney"
        return f"{city_part}, Australia"

    # 2. Handle standard inputs
    parts = [p.strip() for p in loc.split(',')]
    city = parts[0]
    
    if not city or len(city) < 2:
        city = "Sydney"
        
    specified_country = None
    
    if len(parts) == 1:
        specified_country = "Australia"
    elif len(parts) > 1:
        last_part = parts[-1].strip().lower()
        known_countries = ['australia', 'usa', 'united states', 'uk', 'united kingdom', 'canada', 'new zealand', 'nz']
        
        if last_part in known_countries:
            specified_country = last_part
        else:
            specified_country = "Australia"

    # Normalize country display names
    country_display = specified_country
    if country_display == "usa":
        country_display = "United States"
    elif country_display == "uk":
        country_display = "United Kingdom"
    elif country_display == "nz":
        country_display = "New Zealand"
    else:
        # Ensure standard countries are Title Cased (e.g., "australia" -> "Australia")
        country_display = country_display.title()
        
    return f"{city}, {country_display}"