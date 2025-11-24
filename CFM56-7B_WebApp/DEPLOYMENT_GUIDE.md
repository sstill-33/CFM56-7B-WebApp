# CFM56-7B Web Application Deployment Guide

## PythonAnywhere Deployment Instructions

### 1. Upload Files
1. Go to PythonAnywhere.com and create an account
2. Upload all files from this directory to your PythonAnywhere account
3. Place files in your home directory or a subdirectory

### 2. Set Up Virtual Environment
```bash
# In PythonAnywhere console
mkvirtualenv --python=python3.10 cfm56-webapp
pip install -r requirements.txt
```

### 3. Configure Web App
1. Go to the "Web" tab in PythonAnywhere dashboard
2. Click "Add a new web app"
3. Choose "Flask" and Python 3.10
4. Set the source code directory to your uploaded folder
5. Set the WSGI file to: `/home/yourusername/CFM56-7B_WebApp/app.py`

### 4. Update WSGI Configuration
Replace the WSGI file content with:
```python
import sys
path = '/home/yourusername/CFM56-7B_WebApp'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

### 5. Upload Data Files
1. Upload the `data/` folder with your database
2. Upload PDF files to a `static/` folder if needed
3. Update file paths in `app.py` if necessary

### 6. Reload Web App
1. Go to the "Web" tab
2. Click "Reload" to restart your web app
3. Visit your PythonAnywhere URL

## File Structure
```
CFM56-7B_WebApp/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── search.html       # Main search interface
├── static/               # Static files (CSS, JS, images)
└── data/
    └── pdf_linked_database.json  # Search database
```

## Features
- Search across all CFM56-7B document categories
- Direct PDF document access
- Image viewing capabilities
- Category filtering
- Responsive design
- API endpoints for search functionality

## Troubleshooting
- Check PythonAnywhere error logs if the app doesn't load
- Ensure all file paths are correct
- Verify database file is uploaded and accessible
- Check that all dependencies are installed
