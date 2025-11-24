# Upload Database File to Railway

## Quick Upload Instructions

The database file `pdf_linked_database.json` (230MB) must be uploaded to Railway for the application to work.

### Method 1: Railway CLI (Recommended)

```bash
# 1. Install Railway CLI
npm i -g @railway/cli

# 2. Login to Railway
railway login

# 3. Link to your project
railway link

# 4. Upload the database file
# Replace /path/to/ with the actual path to your pdf_linked_database.json file
railway run bash -c "mkdir -p data && cat > data/pdf_linked_database.json" < /path/to/pdf_linked_database.json

# Example if file is in current directory:
railway run bash -c "mkdir -p data && cat > data/pdf_linked_database.json" < pdf_linked_database.json
```

### Method 2: Using Railway Dashboard Terminal

1. Go to your Railway project dashboard
2. Click on your service
3. Go to the **"Deployments"** tab
4. Click on the latest deployment
5. Click **"View Logs"** or open the terminal
6. Run:
   ```bash
   mkdir -p data
   ```
7. Use Railway's file upload feature or SCP to upload the file to the `data/` directory

### Method 3: Using Railway Volume

1. In Railway dashboard, go to your service
2. Click **"New"** → **"Volume"**
3. Mount the volume to `/app/data` (or `/app/CFM56-7B_WebApp/data` depending on your root directory setting)
4. Upload the database file using Railway CLI or dashboard

## Verify Upload

After uploading, check if the database is loaded:

1. Visit: `https://your-railway-app.railway.app/api/debug`
2. This will show you:
   - Which paths were checked
   - Whether the database file exists
   - How many parts/documents were loaded

## Restart Service

After uploading the database file:

1. Go to Railway dashboard
2. Click on your service
3. Go to **"Deployments"** tab
4. Click **"Redeploy"** to restart the service

## Troubleshooting

**If database still shows 0 documents:**
- Check the debug endpoint: `/api/debug`
- Verify the file is in the correct location
- Check Railway logs for any errors
- Ensure the file is named exactly: `pdf_linked_database.json`
- Make sure the file is in the `data/` directory relative to where the app runs

