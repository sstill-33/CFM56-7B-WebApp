# Railway Setup Guide

## Step-by-Step Deployment Instructions

### 1. Deploy from GitHub

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose the repository: `sstill-33/CFM56-7B-WebApp`
5. Railway will automatically:
   - Detect Python
   - Install dependencies from `requirements.txt`
   - Start the app using the `Procfile`

### 2. Upload the Database File

The `pdf_linked_database.json` file (230MB) must be uploaded separately. Here are three methods:

#### Method 1: Railway CLI (Easiest)

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to your project (select your CFM56-7B project)
railway link

# Upload the database file
# Replace /path/to/ with your local path
railway run bash -c "mkdir -p CFM56-7B_WebApp/data && cat > CFM56-7B_WebApp/data/pdf_linked_database.json" < /path/to/pdf_linked_database.json
```

Or use `railway run` to open an interactive shell:

```bash
railway run bash
# Then inside the shell:
mkdir -p CFM56-7B_WebApp/data
# Use a file transfer method to upload
```

#### Method 2: Using Railway's File System Access

1. In Railway dashboard, go to your service
2. Click on **"Settings"** → **"Generate Domain"** (if not already done)
3. Use Railway's terminal or file upload feature
4. Navigate to `CFM56-7B_WebApp/data/` directory
5. Upload `pdf_linked_database.json`

#### Method 3: Using Persistent Volume

1. In Railway dashboard, go to your service
2. Click **"New"** → **"Volume"**
3. Mount the volume to `/app/CFM56-7B_WebApp/data`
4. Upload the database file to the volume using Railway CLI or dashboard

### 3. Verify Deployment

1. Check Railway logs to ensure the app started successfully
2. Visit your Railway-generated domain
3. The search interface should load (may show empty results if database isn't uploaded yet)
4. Once database is uploaded, restart the service:
   - Go to Railway dashboard
   - Click **"Deployments"** → **"Redeploy"**

### 4. Troubleshooting

**App starts but shows no results:**
- Verify `pdf_linked_database.json` is in `CFM56-7B_WebApp/data/`
- Check file permissions (should be readable)
- Check Railway logs for any errors

**App fails to start:**
- Check Railway logs for Python errors
- Verify all dependencies installed correctly
- Ensure `Procfile` is correct

**Database file too large:**
- Railway supports files up to several GB
- If issues persist, consider splitting the database or using external storage (S3, etc.)

### 5. Environment Variables

Optional environment variables you can set in Railway:

- `FLASK_ENV=development` - Enable debug mode (not recommended for production)
- `PORT` - Automatically set by Railway (don't override)

### 6. Custom Domain (Optional)

1. In Railway dashboard, go to your service
2. Click **"Settings"** → **"Generate Domain"** (if not done)
3. Or add a custom domain in **"Settings"** → **"Domains"**

## Quick Reference

- **Repository:** https://github.com/sstill-33/CFM56-7B-WebApp
- **Railway Dashboard:** https://railway.app/dashboard
- **Railway CLI Docs:** https://docs.railway.app/develop/cli

