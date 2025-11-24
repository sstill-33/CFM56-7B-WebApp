# CFM56-7B Aviation Maintenance Search System

A Flask web application for searching CFM56-7B aviation maintenance documentation with direct PDF access.

## Features

- 🔍 Search across all CFM56-7B document categories
- 📄 Direct PDF document access
- 🖼️ Image viewing capabilities
- 🏷️ Category filtering (EIPC, ESM, SB, CMM, CPM, ITEM, NDTM, LLP, SOLUTIONS, SPM, TSP)
- 📱 Responsive design
- 🔌 RESTful API endpoints

## Railway Deployment

This application is configured to run on [Railway](https://railway.app).

### Quick Deploy

1. **Connect to Railway:**
   - Go to [Railway](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose this repository

2. **Automatic Setup:**
   - Railway will automatically detect the Python application
   - It will install dependencies from `requirements.txt`
   - The app will start using the `Procfile`

3. **Environment Variables (Optional):**
   - `FLASK_ENV`: Set to `development` for debug mode (default: production)
   - `PORT`: Automatically set by Railway (no need to configure)

### Manual Deployment

If deploying manually:

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python run_local.py

# Or with gunicorn (production)
gunicorn app:app --bind 0.0.0.0:5000
```

## Project Structure

```
CFM56-7B_WebApp/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Procfile              # Railway deployment configuration
├── railway.json          # Railway-specific settings
├── run_local.py          # Local development server
├── templates/
│   └── search.html       # Main search interface
├── static/               # Static files (CSS, JS, images)
└── data/
    └── pdf_linked_database.json  # Search database
```

## API Endpoints

- `GET /` - Main search page
- `GET /api/search?q=<query>&category=<category>` - Search endpoint
- `GET /api/file?path=<file_path>` - Serve files (PDFs, images, etc.)
- `GET /api/stats` - Get database statistics

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the development server:
   ```bash
   python run_local.py
   ```

3. Open your browser to `http://localhost:5001` (or the port shown)

## Requirements

- Python 3.8+
- Flask 2.3.3
- Gunicorn (for production)

## License

This application is for CFM56-7B aviation maintenance documentation search.

