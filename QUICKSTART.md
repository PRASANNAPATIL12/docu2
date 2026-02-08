# DocuBrain - Quick Start Guide

The fastest way to get DocuBrain running on your local machine.

## 🚀 30-Second Setup

### Prerequisites
- Python 3.11+
- Node.js 18+

### Commands

**Terminal 1 - Backend:**
```bash
cd backend
pip install fastapi uvicorn motor google-generativeai PyPDF2 python-dotenv scikit-learn numpy python-multipart
python -m uvicorn server:app --port 8001 --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm start
```

**Open Browser:**
```
http://localhost:3000
```

That's it! 🎉

---

## 📁 VS Code Setup

1. **Open Project:**
   ```bash
   cd C:\Users\prasannagoudap\Downloads\4.askmydocs-main\4.askmydocs-main
   code .
   ```

2. **Open 2 Terminals in VS Code:**
   - Press `` Ctrl + ` `` for Terminal 1
   - Click `+` for Terminal 2

3. **Terminal 1 (Backend):**
   ```bash
   cd backend
   python -m uvicorn server:app --port 8001 --reload
   ```

4. **Terminal 2 (Frontend):**
   ```bash
   cd frontend
   npm start
   ```

---

## ✅ Environment Variables Already Configured

Both `.env` files are already set up with correct values:

**Backend (.env):**
- MongoDB URL ✓
- Database name: `docu` ✓
- Gemini API Key ✓

**Frontend (.env):**
- Backend URL: `http://localhost:8001` ✓

No configuration needed! Just run the commands above.

---

## 🧪 Test the Application

1. **Register:** Create a new account
2. **Login:** Sign in with your credentials
3. **Upload:** Add a PDF or text document
4. **Query:** Ask questions about your documents
5. **View:** Click 👁️ to view full document
6. **Delete:** Click 🗑️ to delete (with confirmation)

---

## 🆘 Quick Troubleshooting

**Backend won't start?**
```bash
pip install -r requirements.txt
```

**Frontend won't start?**
```bash
npm install
```

**Port already in use?**
- Backend: Change port to 8002 in command + update frontend/.env
- Frontend: React will suggest port 3001 automatically

---

## 📚 Need More Help?

- **Local Setup:** See `LOCAL_SETUP_GUIDE.md`
- **Deployment:** See `DEPLOYMENT_GUIDE_COMPLETE.md`
- **Features:** See `PROJECT_DOCUMENTATION.md`

---

**Happy Coding! 🚀**
