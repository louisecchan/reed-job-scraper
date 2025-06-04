# 🧑‍💻 Web Developer Job Finder (Using Reed.co.uk API)

This simple Python script helps you find **jobs in London** using the [Reed.co.uk](https://www.reed.co.uk/) job search API. It fetches job listings and shows details like the title, company, location, salary, and job type. You can even open job applications directly in your browser.

---

## 🧰 What You Need

1. **Python Installed**
   You need Python 3 installed on your computer.
   📥 Download here: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. **A Reed.co.uk API Key**

   * Go to [Reed.co.uk API Registration](https://www.reed.co.uk/developers)
   * Sign up and request an API key (it’s free)
   * Copy the API key — you'll need to paste it into the script.

---

## 📝 How to Set It Up

1. **Download the Script**

   * Save the Python code into a file named `job_finder.py`.

2. **Insert Your API Key**

   * Open the file in any text editor (Notepad, VS Code, etc.)
   * Find this line:

     ```python
     API_KEY = "YOUR API KEY - REGISTER ON REED TO GET ONE"
     ```
   * Replace it with your actual API key:

     ```python
     API_KEY = "your_api_key_here"
     ```

3. **Install Required Libraries**
   Open your terminal (Command Prompt on Windows or Terminal on Mac) and run:

   ```bash
   pip install requests
   ```

---

## ▶️ How to Run the Script

Once set up, you can run the script using this command in your terminal:

```bash
python job_finder.py
```

It will:

* Fetch web developer jobs in London
* Display job details like salary and location
* Ask if you want to apply
* Open the application page in your browser if you say **yes**

---

## 💡 Example Output

```
Fetching web developer jobs from Reed.co.uk...

Found 2 web developer jobs in London (within 10 miles) with minimum salary £32,000:

Title: Frontend Web Developer
Company: ABC Tech
Location: Camden, Greater London (NW1)
Salary: £32,000 - £45,000
Job Type: Permanent
Posted by: Agency
Job URL: https://www.reed.co.uk/jobs/frontend-web-developer/12345678

Would you like to apply for this job? (yes/no):
```

---

## ❓ FAQs

**Q: Will this work outside the UK?**
A: The job search is limited to the UK, and currently set to search London-based jobs.

**Q: Can I change the job type or location?**
A: Yes! Open the file and scroll to the `params` section. You can change keywords and location easily.

---

## 🔐 Important

* Never share your API key publicly.
* This script is for personal use and learning.

---

## ❤️ Credits

Made with Python, using:

* [Reed.co.uk API](https://www.reed.co.uk/developers)
* [Postcodes.io API](https://postcodes.io/) for postcode lookup

---

Would you like me to package this with a `.bat` or `.sh` file so non-coders can double-click to run it?
