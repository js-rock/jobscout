import re
import logging

# ---------------------------------------------------------
# SECURITY: SANITIZE USER INPUT FOR MALICIOUS CODE
# ---------------------------------------------------------

class InputSanitizer:
    @staticmethod
    def sanitize_city_name(city_name):
        """Sanitize city name input"""
        if not city_name or not isinstance(city_name, str):
            return None
            
        # Strip whitespace
        city_name = city_name.strip()
        
        # Check length
        if len(city_name) > 50:
            return None
            
        # Only allow letters, spaces, hyphens, apostrophes, and periods
        if re.match("^[a-zA-Z\s\-'\.]+$", city_name):
            return city_name.title()
        return None
    
    @staticmethod
    def sanitize_text_input(text, max_length=100):
        """Sanitize general text input"""
        if not text or not isinstance(text, str):
            return None
        
        # This regex now allows commas, so we don't need the dangerous_chars loop anymore.
        if not re.match(r"^[a-zA-Z0-9\s\-',\.]+$", text):
            return None
            
        text = text.strip()
        if len(text) > max_length:
            return None
            
        return text.title()
        
    
    @staticmethod
    def validate_day_request(user_text):
        """Validate day request input"""
        if not user_text:
            return None
            
        # Sanitize first
        sanitized = InputSanitizer.sanitize_text_input(user_text, 50)
        if not sanitized:
            return None
            
        # Check for valid day names
        valid_days = ['today', 'tomorrow', 'monday', 'tuesday', 'wednesday', 
                     'thursday', 'friday', 'saturday', 'sunday']
        
        return sanitized.lower() if sanitized.lower() in valid_days else None
    
    @staticmethod
    def validate_location_format(location: str) -> dict:
        """
        Ensures location has a City AND a Country.
        Returns: {'valid': bool, 'error': str or None, 'city': str, 'country': str}
        """
        if not location:
            return {'valid': False, 'error': "Location cannot be empty.", 'city': '', 'country': ''}

        # Split by comma to check structure
        parts = [p.strip() for p in location.split(',')]
        
        # Check if user provided BOTH parts (e.g., "Sydney, Australia")
        if len(parts) < 2:
            return {
                'valid': False, 
                'error': "Location must include City and Country (e.g., 'Sydney, Australia').", 
                'city': '', 
                'country': ''
            }
        
        city = parts[0]
        country = parts[-1] # Take the last part as country

        # Check for Gibberish in City (Must have at least 2 letters)
        if len([c for c in city if c.isalpha()]) < 2:
            return {
                'valid': False, 
                'error': f"City '{city}' looks invalid. Please enter a real city name.", 
                'city': '', 
                'country': ''
            }

        # Check for Gibberish in Country (Must have at least 2 letters)
        if len([c for c in country if c.isalpha()]) < 2:
            return {
                'valid': False, 
                'error': f"Country '{country}' looks invalid. Please enter a real country.", 
                'city': '', 
                'country': ''
            }

        return {
            'valid': True, 
            'error': None, 
            'city': city, 
            'country': country
        }

# Simple functions for easy use
def sanitize_city(city_input):
    return InputSanitizer.sanitize_city_name(city_input)

def validate_text(text_input):
    return InputSanitizer.sanitize_text_input(text_input)

def validate_day(day_input):
    return InputSanitizer.validate_day_request(day_input)

def validate_location_format(location_input):
    return InputSanitizer.validate_location_format(location_input)