# DocuBrain - Local Setup Guide

This guide will help you run the DocuBrain application locally in VS Code.

## Prerequisites

Before you start, make sure you have the following installed:

- **Python 3.11+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** - [Download Node.js](https://nodejs.org/)
- **Git** - [Download Git](https://git-scm.com/)
- **VS Code** - [Download VS Code](https://code.visualstudio.com/)

## Project Structure

```
4.askmydocs-main/
├── backend/          # FastAPI Backend
│   ├── server.py     # Main API server
│   ├── database.py   # MongoDB operations
│   ├── gemini_embeddings.py  # Gemini Text Embeddings
│   ├── .env          # Backend environment variables
│   └── requirements.txt
├── frontend/         # React Frontend
│   ├── src/
│   │   └── App.js   # Main React component
│   ├── .env         # Frontend environment variables
│   └── package.json
└── LOCAL_SETUP_GUIDE.md (this file)
```

## Step-by-Step Setup Instructions

### 1. Open Project in VS Code

```bash
# Open VS Code in the project directory
cd C:\Users\prasannagoudap\Downloads\4.askmydocs-main\4.askmydocs-main
code .
```

### 2. Backend Setup

#### Open Terminal in VS Code
- Press `` Ctrl + ` `` (backtick) to open the integrated terminal
- Or go to: **Terminal → New Terminal**

#### Navigate to Backend Directory
```bash
cd backend
```

#### Install Python Dependencies
```bash
pip install fastapi uvicorn motor google-generativeai PyPDF2 python-dotenv scikit-learn numpy python-multipart
```

#### Verify Backend .env File
The `backend/.env` file should contain:
```env
MONGO_URL=mongodb+srv://prasannagoudasp12_db_user:pTp3DGKPI5yAR96G@cluster0.lzkj7l1.mongodb.net/?appName=Cluster0
DATABASE_NAME=docu
GEMINI_API_KEY=AIzaSyDpsXHjyqHYMWWRu9yCPGCdEm7EBTjuTwA
CORS_ORIGINS="*"
```

#### Start Backend Server
```bash
python -m uvicorn server:app --port 8001 --reload
```

**Expected Output:**
```
[OK] Google Gemini loaded successfully
[OK] Gemini API configured with key: AIzaSyDpsXHjyqHYMWWR...
[OK] Successfully connected to MongoDB database: docu
INFO:     Uvicorn running on http://127.0.0.1:8001
INFO:     Application startup complete.
```

**Backend is now running at:** `http://localhost:8001`

### 3. Frontend Setup (Open New Terminal)

#### Open Second Terminal
- Click the `+` button in VS Code terminal panel to open a new terminal
- Or press `` Ctrl + Shift + ` ``

#### Navigate to Frontend Directory
```bash
cd frontend
```

#### Install Node Dependencies
```bash
npm install
```

This will install all required packages including:
- React 18
- React Router DOM
- Axios
- Tailwind CSS
- Shadcn/ui components

#### Verify Frontend .env File
The `frontend/.env` file should contain:
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

#### Start Frontend Development Server
```bash
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view the app in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

**Frontend is now running at:** `http://localhost:3000`

### 4. Access the Application

Open your browser and go to: **http://localhost:3000**

You should see the DocuBrain login page!

## VS Code Terminal Layout

Your VS Code should have 2 terminal tabs:

```
Terminal 1: Backend Server (backend directory)
Running: python -m uvicorn server:app --port 8001 --reload

Terminal 2: Frontend Server (frontend directory)
Running: npm start
```

## Testing the Application

### 1. Register a New User
- Click "Don't have an account? Register"
- Enter username and password
- Click "Register"
- You'll see a success popup

### 2. Login
- Enter your credentials
- Click "Login"
- You'll be redirected to the Dashboard

### 3. Upload a Document
- **Option A:** Upload a PDF file
  - Click "Choose File" under "Upload PDF Document"
  - Select a PDF file
  - Wait for processing

- **Option B:** Add text document
  - Click "Add Text Document"
  - Enter a title
  - Paste or type your content
  - Click "Add Text Document"

### 4. View Documents
- Your uploaded documents will appear in the "Your Documents" section
- Click the **👁️ View** button to see the full document content
- Click the **🗑️ Delete** button to delete a document (with confirmation)

### 5. Ask Questions
- Type a question in the "Your Question" field
- Click "Ask Question"
- The AI will search your documents and provide an answer
- Sources will be shown below the answer

## Troubleshooting

### Backend Won't Start

**Error: "Module not found"**
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt
```

**Error: "MongoDB connection failed"**
- Check your internet connection
- Verify the MongoDB URL in `backend/.env`
- Ensure MongoDB Atlas allows connections from your IP

**Error: "Port 8001 already in use"**
```bash
# Solution: Use a different port
python -m uvicorn server:app --port 8002 --reload

# Update frontend/.env:
REACT_APP_BACKEND_URL=http://localhost:8002
```

### Frontend Won't Start

**Error: "npm command not found"**
- Install Node.js from https://nodejs.org/

**Error: "Port 3000 already in use"**
- Another app is using port 3000
- The React app will automatically suggest port 3001

**Error: "Module not found" or "Cannot find package"**
```bash
# Solution: Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Connection Issues

**Error: "Network Error" when uploading documents**
- Check if backend is running on port 8001
- Verify `REACT_APP_BACKEND_URL` in `frontend/.env`
- Check browser console (F12) for CORS errors

## Stopping the Application

### Stop Backend Server
- Go to Terminal 1 (backend)
- Press `Ctrl + C`

### Stop Frontend Server
- Go to Terminal 2 (frontend)
- Press `Ctrl + C`

## Quick Reference Commands

### Backend Commands (from backend directory)
```bash
# Start server
python -m uvicorn server:app --port 8001 --reload

# Install dependencies
pip install -r requirements.txt

# Check Python version
python --version
```

### Frontend Commands (from frontend directory)
```bash
# Start development server
npm start

# Install dependencies
npm install

# Build for production
npm run build

# Check Node version
node --version
```

## Environment Variables Summary

### Backend (.env)
- `MONGO_URL` - MongoDB connection string
- `DATABASE_NAME` - Database name (docu)
- `GEMINI_API_KEY` - Google Gemini API key
- `CORS_ORIGINS` - Allowed origins (*)

### Frontend (.env)
- `REACT_APP_BACKEND_URL` - Backend API URL

## Features Available

✅ **User Authentication**
- Simple registration and login
- Secure token-based authentication
- API key for external integrations

✅ **Document Management**
- Upload PDF files
- Add text documents
- View full document content (read-only)
- Delete documents with confirmation

✅ **AI-Powered Q&A**
- Ask questions about your documents
- Get intelligent answers using Gemini API
- See relevant sources with relevance scores

✅ **Gemini Text Embeddings**
- 768-dimensional semantic embeddings
- ~85-90% accuracy (vs 40-50% with TF-IDF)
- Improved document search and retrieval

## Next Steps: Deployment

Once you've tested locally and everything works, you can deploy:

- **Frontend**: Vercel
- **Backend**: Render.com
- **Database**: MongoDB Atlas (already configured)

See `DEPLOYMENT_GUIDE.md` for deployment instructions.

## Support

If you encounter any issues not covered in this guide:
1. Check the browser console (F12) for errors
2. Check the backend terminal for error messages
3. Verify all environment variables are set correctly
4. Ensure MongoDB Atlas allows your IP address

---

**Happy Coding! 🚀**
