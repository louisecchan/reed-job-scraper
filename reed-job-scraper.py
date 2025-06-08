import requests
import json
from datetime import datetime
import base64
import re
import webbrowser
import time

# API Configuration
API_KEY = "YOUR API KEY - REGISTER ON REED TO GET ONE"
BASE_URL = "https://www.reed.co.uk/api/1.0/search"
POSTCODE_API_URL = "https://api.postcodes.io/postcodes/"

def get_location_from_postcode(postcode):
    """Convert postcode to readable location using postcodes.io API"""
    try:
        # Clean the postcode
        postcode = postcode.strip().upper()
        # Remove any spaces
        postcode = re.sub(r'\s+', '', postcode)
        
        response = requests.get(f"{POSTCODE_API_URL}{postcode}")
        if response.status_code == 200:
            data = response.json()
            if data.get('result'):
                result = data['result']
                location_parts = []
                
                # Add district if available
                if result.get('admin_district'):
                    location_parts.append(result['admin_district'])
                
                # Add county if available
                if result.get('admin_county'):
                    location_parts.append(result['admin_county'])
                
                # Add region if available
                if result.get('region'):
                    location_parts.append(result['region'])
                
                return f"{', '.join(location_parts)} ({postcode})"
    except Exception as e:
        print(f"Error converting postcode: {e}")
    
    return postcode  # Return original postcode if conversion fails

def apply_to_job(job_url):
    """Open the job application page in the default web browser"""
    try:
        print(f"\nOpening application page: {job_url}")
        webbrowser.open(job_url)
        return True
    except Exception as e:
        print(f"Error opening application page: {e}")
        return False

def fetch_web_developer_jobs():
    # API parameters
    params = {
        "keywords": '"web developer" -trainee',  # Exact phrase search, excluding trainee positions
        "locationName": "London",  # Limit to London jobs
        "distanceFromLocation": 10,  # Search radius in miles
        "resultsToTake": 10,     # Maximum results per request
        "minimumSalary": 32000,  # Minimum salary of £32,000
        "permanent": "true",    # Include permanent jobs
        "contract": "true",     # Include contract jobs
        "temp": "true",         # Include temporary jobs
        "fullTime": "true",     # Include full-time jobs
        "partTime": "true",     # Include part-time jobs
        "postedByRecruitmentAgency": "true",  # Include agency jobs
        "postedByDirectEmployer": "true",     # Include direct employer jobs
    }
    
    # Headers with API key - using Basic Auth with empty password
    auth_string = f"{API_KEY}:"
    auth_bytes = auth_string.encode('ascii')
    base64_auth = base64.b64encode(auth_bytes).decode('ascii')
    
    headers = {
        "Authorization": f"Basic {base64_auth}",
        "Content-Type": "application/json"
    }
    
    try:
        # Make the API request
        response = requests.get(BASE_URL, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the response
        jobs = response.json().get('results', [])
        
        # Print job information
        print(f"\nFound {len(jobs)} web developer jobs in London (within 10 miles) with minimum salary £32,000:\n")
        
        for job in jobs:
            print(f"Title: {job.get('jobTitle', 'N/A')}")
            print(f"Company: {job.get('employerName', 'N/A')}")
            
            # Get and convert location
            location = job.get('locationName', 'N/A')
            if location != 'N/A':
                # Try to extract postcode if present
                postcode_match = re.search(r'[A-Z]{1,2}[0-9][A-Z0-9]? ?[0-9][A-Z]{2}', location.upper())
                if postcode_match:
                    postcode = postcode_match.group(0)
                    readable_location = get_location_from_postcode(postcode)
                    print(f"Location: {readable_location}")
                else:
                    print(f"Location: {location}")
            else:
                print(f"Location: {location}")
            
            # Format salary information
            min_salary = job.get('minimumSalary')
            max_salary = job.get('maximumSalary')
            if min_salary or max_salary:
                salary_range = f"£{min_salary:,}" if min_salary else "N/A"
                if max_salary:
                    salary_range += f" - £{max_salary:,}"
                print(f"Salary: {salary_range}")
            
            # Add job type information
            job_type = []
            if job.get('permanent'):
                job_type.append("Permanent")
            if job.get('contract'):
                job_type.append("Contract")
            if job.get('temp'):
                job_type.append("Temporary")
            if job_type:
                print(f"Job Type: {', '.join(job_type)}")
            
            # Add posting type information
            posting_type = []
            if job.get('postedByRecruitmentAgency'):
                posting_type.append("Agency")
            if job.get('postedByDirectEmployer'):
                posting_type.append("Direct Employer")
            if posting_type:
                print(f"Posted by: {', '.join(posting_type)}")
            
            job_url = job.get('jobUrl', 'N/A')
            print(f"Job URL: {job_url}")
            
            # Ask user if they want to apply
            if job_url != 'N/A':
                apply = input("\nWould you like to apply for this job? (yes/no): ").lower()
                if apply in ['yes', 'y']:
                    if apply_to_job(job_url):
                        print("Application page opened in your browser.")
                        # Wait a bit before showing the next job
                        time.sleep(2)
            
            print("-" * 80 + "\n")
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching jobs: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response content: {e.response.text}")
    except json.JSONDecodeError as e:
        print(f"Error parsing response: {e}")
        print(f"Raw response: {response.text}")

if __name__ == "__main__":
    print("Fetching web developer jobs from Reed.co.uk...")
    fetch_web_developer_jobs()
