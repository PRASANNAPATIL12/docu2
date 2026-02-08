# Quick Render.com Deployment Fix

## 🔧 The Issue
Your deployment failed because Render was trying to use a build script with incorrect permissions.

## ✅ The Solution
I've added a `render.yaml` configuration file that simplifies deployment.

---

## 📦 Option 1: Redeploy Current Service (Recommended)

### Step 1: Update Your Service Settings
1. Go to your Render dashboard: https://dashboard.render.com
2. Click on your `docubrain-backend` service
3. Click **"Settings"** in the left sidebar

### Step 2: Update Build & Start Commands
Scroll to **"Build & Deploy"** section:

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
uvicorn server:app --host 0.0.0.0 --port $PORT
```

### Step 3: Verify Environment Variables
Click **"Environment"** tab and ensure these are set:

| Key | Value |
|-----|-------|
| `MONGO_URL` | `mongodb+srv://prasannagoudasp12_db_user:pTp3DGKPI5yAR96G@cluster0.lzkj7l1.mongodb.net/?appName=Cluster0` |
| `DATABASE_NAME` | `docu` |
| `GEMINI_API_KEY` | `AIzaSyDpsXHjyqHYMWWRu9yCPGCdEm7EBTjuTwA` |
| `CORS_ORIGINS` | `*` |

### Step 4: Manual Deploy
1. Go to **"Manual Deploy"** section
2. Click **"Clear build cache & deploy"**
3. Wait 5-10 minutes for deployment

---

## 🆕 Option 2: Create New Service from Scratch

### Step 1: Delete Old Service (Optional)
1. Go to your service dashboard
2. Click **"Settings"** → Scroll to bottom
3. Click **"Delete Web Service"**

### Step 2: Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Select your GitHub repository: `docu2`
3. Click **"Connect"**

### Step 3: Configure Service

**Name:** `docubrain-backend`

**Region:** Oregon (or closest to you)

**Branch:** `main`

**Root Directory:** `backend`

**Runtime:** Python 3

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
uvicorn server:app --host 0.0.0.0 --port $PORT
```

### Step 4: Add Environment Variables
Click **"Advanced"** and add:

```
MONGO_URL=mongodb+srv://prasannagoudasp12_db_user:pTp3DGKPI5yAR96G@cluster0.lzkj7l1.mongodb.net/?appName=Cluster0
DATABASE_NAME=docu
GEMINI_API_KEY=AIzaSyDpsXHjyqHYMWWRu9yCPGCdEm7EBTjuTwA
CORS_ORIGINS=*
```

### Step 5: Create Service
1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)

---

## 🎯 Option 3: Use render.yaml (Easiest)

The code now includes a `render.yaml` file at the root of your repository.

### Step 1: Use Blueprint
1. Go to Render Dashboard
2. Click **"New +"** → **"Blueprint"**
3. Select your `docu2` repository
4. Render will auto-detect the `render.yaml` file
5. Click **"Apply"**

This will automatically:
- ✅ Set the correct build command
- ✅ Set the correct start command
- ✅ Configure all environment variables
- ✅ Set the root directory to `backend`

---

## 🧪 Testing Your Deployment

### After Deployment Succeeds:

1. **Get Your Backend URL:**
   - Look for: `https://docubrain-backend-XXXXX.onrender.com`

2. **Test the API:**
   - Open: `https://your-backend-url.onrender.com`
   - You should see:
   ```json
   {
     "message": "DocuBrain API is running! [BRAIN]",
     "version": "1.0.0",
     "endpoints": {...}
   }
   ```

3. **Check Logs:**
   - Go to **"Logs"** tab
   - Look for:
   ```
   [OK] Successfully connected to MongoDB database: docu
   INFO: Application startup complete
   ```

---

## 🐛 Troubleshooting

### Issue: "Build failed" with Python errors
**Solution:**
- Check if Python version is set correctly
- Render should use Python 3.11+ automatically

### Issue: "Application startup failed"
**Solution:**
- Check environment variables are set correctly
- Verify MongoDB connection string
- Check logs for specific errors

### Issue: "502 Bad Gateway"
**Solution:**
- Wait 2-3 minutes (service might be starting)
- Check if `$PORT` variable is used in start command
- Verify uvicorn is in requirements.txt

### Issue: MongoDB connection error
**Solution:**
1. Go to MongoDB Atlas
2. Click **"Network Access"**
3. Add IP: `0.0.0.0/0` (Allow from anywhere)

---

## 📝 Next Steps After Backend is Live

### Update Frontend for Production:

1. **Get your Render backend URL** (e.g., `https://docubrain-backend-XXXXX.onrender.com`)

2. **Deploy Frontend on Vercel:**
   - Go to: https://vercel.com
   - Click **"Add New..."** → **"Project"**
   - Select your `docu2` repository
   - **Root Directory:** `frontend`
   - **Environment Variable:**
     ```
     REACT_APP_BACKEND_URL=https://your-render-backend-url.onrender.com
     ```
   - Click **"Deploy"**

3. **Test Complete Application:**
   - Open your Vercel URL
   - Register a user
   - Upload a document
   - Ask a question
   - Test View and Delete buttons

---

## 🎉 Success Checklist

- [ ] Backend deployed successfully on Render
- [ ] Backend URL accessible in browser
- [ ] MongoDB connection working (check logs)
- [ ] Frontend deployed on Vercel
- [ ] Frontend connects to backend
- [ ] User registration works
- [ ] Document upload works
- [ ] View document works
- [ ] Delete document works
- [ ] AI queries return answers

---

## 📞 Need More Help?

**Render Issues:**
- Docs: https://render.com/docs/troubleshooting-deploys
- Support: https://render.com/support

**Vercel Issues:**
- Docs: https://vercel.com/docs
- Support: https://vercel.com/support

**Check Your Logs:**
- Render: Dashboard → Your Service → Logs
- Vercel: Dashboard → Your Project → Deployments → Click deployment → Function Logs

---

## 🚀 Quick Deploy Commands (For Reference)

**If you need to update and redeploy:**
```bash
# Make changes to your code
git add -A
git commit -m "Your changes"
git push origin main
```

Render and Vercel will automatically detect changes and redeploy!

---

**Good luck with your deployment! 🎉**
