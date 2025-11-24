# Railway Build Fix Instructions

The Railway build is failing because it's trying to read binary files from the repository that contain invalid UTF-8 encoding.

## Solution: Configure Railway Service Root Directory

Since the problematic files are in git history, you need to configure Railway to only build from the `CFM56-7B_WebApp` directory:

### Steps:

1. **Go to Railway Dashboard**
   - Open your project: https://railway.app/dashboard
   - Click on your service

2. **Set Root Directory**
   - Go to **Settings** tab
   - Find **"Root Directory"** setting
   - Set it to: `CFM56-7B_WebApp`
   - Save changes

3. **Update Build Settings**
   - The `requirements.txt` is already in `CFM56-7B_WebApp/`
   - The `Procfile` is already in `CFM56-7B_WebApp/`
   - Railway will now only scan files in that directory

4. **Redeploy**
   - Railway will automatically trigger a new build
   - Or manually trigger from the Deployments tab

## Alternative: Create Clean Repository

If the above doesn't work, create a new repository with only the web app:

```bash
# Create a new clean repository
mkdir CFM56-7B-WebApp-Clean
cd CFM56-7B-WebApp-Clean
cp -r ../CFM56-7B/CFM56-7B_WebApp/* .
git init
git add .
git commit -m "Initial commit - clean web app only"
git remote add origin <new-repo-url>
git push -u origin main
```

Then connect this clean repository to Railway.

