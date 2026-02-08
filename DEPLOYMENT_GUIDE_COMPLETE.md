# DocuBrain - Complete Deployment Guide

This guide covers deploying the DocuBrain application to production with:
- **Frontend**: Vercel
- **Backend**: Render.com
- **Database**: MongoDB Atlas

## Prerequisites Checklist

- [ ] GitHub account
- [ ] Vercel account (free tier)
- [ ] Render.com account (free tier)
- [ ] MongoDB Atlas account (already configured)
- [ ] Git installed locally

## Part 1: Push Code to GitHub

### Step 1: Create a New GitHub Repository

1. Go to https://github.com/new
2. Repository name: `docubrain-app` (or any name you prefer)
3. Make it **Public** or **Private** (your choice)
4. **DO NOT** initialize with README, .gitignore, or license
5. Click "Create repository"

### Step 2: Push Your Code

Open terminal in your project root and run:

```bash
# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/docubrain-app.git

# Push the feature branch
git push -u origin feature/gemini-embeddings-crud-enhancements

# Also push main branch (if you want to merge first)
git checkout main
git merge feature/gemini-embeddings-crud-enhancements
git push -u origin main
```

Your code is now on GitHub! 🎉

## Part 2: Deploy Backend to Render.com

### Step 1: Sign Up / Login to Render.com

1. Go to https://render.com
2. Sign up or login (use GitHub account for easy integration)

### Step 2: Create New Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub account if not already connected
3. Select your `docubrain-app` repository
4. Click **"Connect"**

### Step 3: Configure the Web Service

**Basic Settings:**
- **Name**: `docubrain-backend` (or any unique name)
- **Region**: Choose closest to your users (e.g., Oregon USA)
- **Branch**: `main` (or your feature branch)
- **Root Directory**: `backend`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`

**Instance Type:**
- Select **"Free"** (for testing)
- You can upgrade later if needed

### Step 4: Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add these variables:

| Key | Value |
|-----|-------|
| `MONGO_URL` | `mongodb+srv://prasannagoudasp12_db_user:pTp3DGKPI5yAR96G@cluster0.lzkj7l1.mongodb.net/?appName=Cluster0` |
| `DATABASE_NAME` | `docu` |
| `GEMINI_API_KEY` | `AIzaSyDpsXHjyqHYMWWRu9yCPGCdEm7EBTjuTwA` |
| `CORS_ORIGINS` | `*` |
| `PORT` | `8001` |

### Step 5: Deploy

1. Click **"Create Web Service"**
2. Render will start building and deploying your backend
3. Wait 5-10 minutes for the deployment to complete
4. You'll get a URL like: `https://docubrain-backend.onrender.com`

### Step 6: Test Backend Deployment

Open your backend URL in a browser:
```
https://docubrain-backend.onrender.com
```

You should see:
```json
{
  "message": "DocuBrain API is running! [BRAIN]",
  "version": "1.0.0",
  "endpoints": {
    "register": "POST /api/auth/register",
    "login": "POST /api/auth/login",
    "upload": "POST /api/documents/upload",
    "query": "POST /api/query",
    "docs": "/docs"
  }
}
```

**Important:** Copy this URL! You'll need it for frontend deployment.

## Part 3: Deploy Frontend to Vercel

### Step 1: Sign Up / Login to Vercel

1. Go to https://vercel.com
2. Sign up or login (use GitHub account)

### Step 2: Import Project

1. Click **"Add New..."** → **"Project"**
2. Select your GitHub repository: `docubrain-app`
3. Click **"Import"**

### Step 3: Configure Project

**Framework Preset:**
- Vercel should auto-detect **"Create React App"**

**Root Directory:**
- Click **"Edit"**
- Set to: `frontend`

**Build and Output Settings:**
- Build Command: `npm run build` (default)
- Output Directory: `build` (default)
- Install Command: `npm install` (default)

### Step 4: Add Environment Variables

Click **"Environment Variables"**

Add this variable:

| Key | Value |
|-----|-------|
| `REACT_APP_BACKEND_URL` | `https://docubrain-backend.onrender.com` |

**Replace** `docubrain-backend.onrender.com` with YOUR actual Render backend URL!

### Step 5: Deploy

1. Click **"Deploy"**
2. Vercel will build and deploy your frontend
3. Wait 2-5 minutes
4. You'll get a URL like: `https://docubrain-app.vercel.app`

### Step 6: Test Frontend Deployment

1. Open your Vercel URL: `https://docubrain-app.vercel.app`
2. You should see the DocuBrain login page
3. Try registering a new user
4. Upload a document
5. Ask a question

## Part 4: Configure MongoDB Atlas

Your MongoDB is already set up, but let's verify the configuration:

### Step 1: Login to MongoDB Atlas

1. Go to https://cloud.mongodb.com
2. Login with your credentials

### Step 2: Check Network Access

1. Click **"Network Access"** in the left sidebar
2. Ensure you have one of these:
   - **0.0.0.0/0** (Allow access from anywhere) - Easiest for deployment
   - Or add specific IPs for Render.com

### Step 3: Verify Database

1. Click **"Database"** in the left sidebar
2. Click **"Browse Collections"**
3. You should see the `docu` database
4. Collections will be created automatically when you use the app

## Part 5: Update Backend CORS (If Needed)

If you encounter CORS issues, update the backend environment variable:

### On Render.com:

1. Go to your backend service
2. Click **"Environment"** tab
3. Update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=https://docubrain-app.vercel.app
   ```
4. Click **"Save Changes"**
5. Service will automatically redeploy

## Part 6: Custom Domain (Optional)

### For Vercel (Frontend):

1. Go to your Vercel project
2. Click **"Settings"** → **"Domains"**
3. Add your custom domain (e.g., `docubrain.com`)
4. Follow Vercel's instructions to update DNS

### For Render (Backend):

1. Go to your Render service
2. Click **"Settings"** → **"Custom Domain"**
3. Add your API domain (e.g., `api.docubrain.com`)
4. Update DNS records as instructed

**Don't forget:** Update `REACT_APP_BACKEND_URL` in Vercel if you add a custom backend domain!

## Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Backend deployed on Render.com
- [ ] Backend URL tested and working
- [ ] Frontend deployed on Vercel
- [ ] Frontend URL tested and working
- [ ] Environment variables set correctly
- [ ] MongoDB Atlas network access configured
- [ ] Test user registration
- [ ] Test document upload
- [ ] Test document viewing
- [ ] Test document deletion
- [ ] Test AI question answering

## Troubleshooting

### Backend Issues

**Error: "Application failed to respond"**
- Check Render logs: Dashboard → Logs
- Verify environment variables are set
- Check MongoDB connection string
- Ensure PORT is set to 8001

**Error: "502 Bad Gateway"**
- Service might be starting (wait 2-3 minutes)
- Check if build command succeeded
- Verify Python dependencies installed

### Frontend Issues

**Error: "CORS policy blocking"**
- Update `CORS_ORIGINS` in backend environment variables
- Make sure it matches your Vercel domain exactly

**Error: "Network Error" when calling API**
- Verify `REACT_APP_BACKEND_URL` is set correctly
- Check if backend is running on Render
- Test backend URL directly in browser

**Error: "Failed to load page"**
- Check Vercel build logs
- Verify `frontend/.env` has correct backend URL
- Try redeploying

### MongoDB Issues

**Error: "MongoNetworkError"**
- Add `0.0.0.0/0` to Network Access in MongoDB Atlas
- Or add Render's IP addresses

**Error: "Authentication failed"**
- Verify MongoDB credentials in environment variables
- Check if username/password has special characters (URL encode if needed)

## Continuous Deployment

Both Vercel and Render support automatic deployments:

### How It Works:
1. You push code to GitHub
2. Vercel automatically rebuilds frontend
3. Render automatically rebuilds backend
4. Changes go live within minutes

### To Trigger Deployment:
```bash
# Make changes to your code
git add .
git commit -m "Your commit message"
git push origin main
```

## Monitoring & Logs

### Render Logs:
- Go to your service dashboard
- Click **"Logs"** tab
- See real-time server logs

### Vercel Logs:
- Go to your project
- Click **"Deployments"** tab
- Click any deployment → View logs

### MongoDB Monitoring:
- MongoDB Atlas dashboard shows:
  - Connection statistics
  - Query performance
  - Database size

## Free Tier Limitations

### Render.com Free Tier:
- ✅ 750 hours/month (enough for 1 service)
- ⚠️ Spins down after 15 minutes of inactivity
- ⚠️ Cold start time: ~30 seconds
- ✅ Auto SSL certificate

### Vercel Free Tier:
- ✅ Unlimited projects
- ✅ 100GB bandwidth/month
- ✅ Auto SSL certificate
- ✅ Edge network (fast worldwide)

### MongoDB Atlas Free Tier:
- ✅ 512MB storage
- ✅ Shared cluster
- ✅ Good for development/small projects

## Upgrade Path

When you need more performance:

1. **Render**: Upgrade to $7/month for always-on service
2. **Vercel**: Pro plan at $20/month for team features
3. **MongoDB**: Upgrade to dedicated cluster for better performance

## Production Best Practices

### Security:
- [ ] Use strong MongoDB password
- [ ] Restrict CORS origins to your domain only
- [ ] Enable rate limiting (add later)
- [ ] Use HTTPS only (both platforms provide this)

### Performance:
- [ ] Enable caching for embeddings (future enhancement)
- [ ] Optimize MongoDB indexes
- [ ] Monitor API response times

### Monitoring:
- [ ] Set up uptime monitoring (UptimeRobot, Pingdom)
- [ ] Monitor error rates
- [ ] Track API usage

## Support & Resources

### Render.com:
- Docs: https://render.com/docs
- Support: https://render.com/support

### Vercel:
- Docs: https://vercel.com/docs
- Support: https://vercel.com/support

### MongoDB Atlas:
- Docs: https://docs.mongodb.com/
- Support: https://support.mongodb.com/

---

## 🎉 Congratulations!

Your DocuBrain application is now live and accessible from anywhere in the world!

**Share your app:**
- Frontend URL: `https://your-app.vercel.app`
- API Documentation: `https://your-backend.onrender.com/docs`

---

**Need help?** Check the logs, review the troubleshooting section, or contact support for the respective platforms.
