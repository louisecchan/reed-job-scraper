import requests
import json
from datetime import datetime
import base64
import re
import webbrowser
import time
from bs4 import BeautifulSoup

# API Configuration
API_KEY = "YOUR API KEY - REGISTER ON REED TO GET ONE"
BASE_URL = "https://www.reed.co.uk/api/1.0/search"
POSTCODE_API_URL = "https://api.postcodes.io/postcodes/"
LOGIN_URL = "https://www.reed.co.uk/account/signin"
APPLICATION_URL = "https://www.reed.co.uk/jobs/apply/"

# User credentials (would normally be input or from secure storage)
USER_EMAIL = "louise.cch@gmail.com"
USER_PASSWORD = "H5$e4Aq%55=S3Z,"

# Session for maintaining cookies
session = requests.Session()

def login_to_reed():
    """Log in to Reed.co.uk to maintain session for applications"""
    try:
        # First get the login page to obtain CSRF token
        login_page = session.get(LOGIN_URL)
        soup = BeautifulSoup(login_page.text, 'html.parser')
        csrf_token = soup.find('input', {'name': '__RequestVerificationToken'})['value']
        
        # Prepare login data
        login_data = {
            '__RequestVerificationToken': csrf_token,
            'Credentials.Email': USER_EMAIL,
            'Credentials.Password': USER_PASSWORD,
            'RememberMe': 'false'
        }
        
        # Post login data
        response = session.post(LOGIN_URL, data=login_data)
        
        if "Sign out" in response.text:
            print("Successfully logged in to Reed.co.uk")
            return True
        else:
            print("Login failed")
            return False
    except Exception as e:
        print(f"Login error: {e}")
        return False

def get_cv_id():
    """Get the CV ID from Reed.co.uk after logging in"""
    try:
        # First ensure we're logged in
        if not login_to_reed():
            print("Failed to login. Cannot get CV ID.")
            return None
            
        # Get the CV page
        cv_page = session.get("https://www.reed.co.uk/account/cv")
        soup = BeautifulSoup(cv_page.text, 'html.parser')
        
        # Look for CV ID in the page
        # The CV ID is typically in a data attribute or in the URL of the CV view/edit link
        cv_link = soup.find('a', {'href': re.compile(r'/account/cv/\d+')})
        if cv_link:
            cv_id = re.search(r'/account/cv/(\d+)', cv_link['href']).group(1)
            print(f"Found CV ID: {cv_id}")
            return cv_id
        else:
            print("Could not find CV ID on the page")
            return None
            
    except Exception as e:
        print(f"Error getting CV ID: {e}")
        return None

def apply_to_job_automated(job_id):
    """Attempt to automatically apply to a job using the Reed API"""
    try:
        # Get CV ID first
        cv_id = get_cv_id()
        if not cv_id:
            print("Could not get CV ID. Please upload a CV to your Reed account first.")
            return False
            
        # API endpoint for applying
        apply_url = f"https://www.reed.co.uk/api/1.0/jobs/{job_id}/application"
        
        # Prepare application data with the actual CV ID
        application_data = {
            "cvId": cv_id,
            "coverLetter": "Dear Hiring Manager,\n\nI'm excited to apply for this position...",
            "additionalQuestions": {}  # Would need to handle job-specific questions
        }
        
        # Headers with API key - using Basic Auth with empty password
        auth_string = f"{API_KEY}:"
        auth_bytes = auth_string.encode('ascii')
        base64_auth = base64.b64encode(auth_bytes).decode('ascii')
        
        headers = {
            "Authorization": f"Basic {base64_auth}",
            "Content-Type": "application/json"
        }
        
        response = session.post(apply_url, json=application_data, headers=headers)
        
        if response.status_code == 200:
            print("Application submitted successfully!")
            return True
        else:
            print(f"Application failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error in automated application: {e}")
        return False

def apply_to_job(job_url, job_id=None):
    """Handle job application with fallback options"""
    # First try automated application if job_id is available
    if job_id and login_to_reed():
        if apply_to_job_automated(job_id):
            return True
    
    # Fall back to opening browser if automated fails
    try:
        print(f"\nOpening application page: {job_url}")
        webbrowser.open(job_url)
        return True
    except Exception as e:
        print(f"Error opening application page: {e}")
        return False

def get_location_from_postcode(postcode):
    """Get human-readable location from postcode using postcodes.io API"""
    try:
        response = requests.get(f"{POSTCODE_API_URL}{postcode}")
        if response.status_code == 200:
            data = response.json()
            if data.get('result'):
                # Return a formatted location string
                result = data['result']
                return f"{result.get('admin_ward', '')}, {result.get('admin_district', '')}, {result.get('region', '')}"
        return postcode  # Return original postcode if lookup fails
    except Exception as e:
        print(f"Error looking up postcode: {e}")
        return postcode  # Return original postcode if lookup fails

def fetch_web_developer_jobs():
    # API parameters
    params = {
        "keywords": '"web developer"',  # Exact phrase search
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
            job_id = job.get('jobId')
            print(f"Job URL: {job_url}")
            
            # Auto-apply to jobs that support one-click application
            if job.get('applicationAction') == "applynow" and job_id:
                print("\nThis job supports quick apply - attempting automatic application...")
                if apply_to_job(job_url, job_id):
                    print("Application attempt completed.")
                else:
                    print("Could not complete automatic application.")
            else:
                print("\nThis job requires manual application.")
                if input("Would you like to open the application page? (yes/no): ").lower() in ['yes', 'y']:
                    apply_to_job(job_url)
            
            print("-" * 80 + "\n")
            time.sleep(2)  # Be polite with rate limiting
            
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