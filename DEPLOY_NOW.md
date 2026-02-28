# 🚀 DEPLOY TO VERCEL - STEP BY STEP

## ⚠️ Important: Generate Pickle Files First

The Flask app needs pre-trained models. Follow these steps:

---

## STEP 1: Run the Jupyter Notebook (Generates Models)

1. **Open the notebook:**
   ```
   d:\sentiment recommendation\sentiment_recommendation_notebook.ipynb
   ```

2. **Run all cells:**
   - Click "Run All" button in VS Code
   - Wait for completion (~5-10 minutes)
   - This generates:
     - ✅ tfidf_vectorizer.pkl
     - ✅ sentiment_model.pkl
     - ✅ user_based_cf.pkl
     - ✅ master_reviews.pkl

3. **Verify files exist:**
   ```powershell
   ls d:\sentiment\ recommendation\*.pkl
   ```
   You should see 4 .pkl files

---

## STEP 2: Test Locally (Optional but Recommended)

```powershell
cd d:\sentiment recommendation
python app.py
```

Then open http://localhost:5000 in your browser

Test:
- Enter username: "alice"
- Enter review: "This product is amazing!"
- Click "Analyze"
- Should see sentiment + recommendations

---

## STEP 3: Deploy to Vercel (Global)

### 3A: Install Vercel CLI

```powershell
npm install -g vercel
```

### 3B: Push to GitHub

```powershell
cd d:\sentiment recommendation

# Initialize and commit all files
git add .
git commit -m "Complete sentiment recommender - ready to deploy"

# Create new repo at https://github.com/new
# Name it: sentiment-recommender

# Push to GitHub (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/sentiment-recommender
git branch -M main
git push -u origin main
```

### 3C: Deploy to Vercel

```powershell
vercel login
vercel --prod
```

Vercel will:
1. Clone your repo from GitHub
2. Install dependencies
3. Deploy your app globally
4. Give you a live URL

⏳ **Takes 2-3 minutes**

---

## STEP 4: Access Your Live App

After deployment, Vercel shows your URL:
```
✓ Production: https://sentiment-recommender-YOUR_USERNAME.vercel.app
```

Open it in your browser! 🎉

---

## 🧪 Test Your Vercel Deployment

```bash
# Replace with your actual Vercel URL
curl -X POST https://YOUR_APP.vercel.app/api/health

# Should return:
# {"status": "healthy", "message": "...operational", ...}
```

---

## 📋 Summary

| Step | Command | Time | Status |
|------|---------|------|--------|
| 1 | Run notebook | 5-10 min | Generates models |
| 2 | Test locally | 2 min | (Optional) |
| 3A | `npm install -g vercel` | 1 min | Install CLI |
| 3B | `git push` | 2 min | Push to GitHub |
| 3C | `vercel --prod` | 3 min | Deploy to Vercel |
| 4 | Open URL | - | Live! |

**Total: ~15-20 minutes** ⏱️

---

## ❓ Common Issues & Fixes

### Issue: Pickle files missing
```
❌ Failed to initialize system: Missing required pickle files
```
**Fix:** Run the Jupyter notebook end-to-end first

### Issue: Git not initialized
```
❌ fatal: not a git repository
```
**Fix:**
```powershell
cd d:\sentiment recommendation
git init
git add .
git commit -m "Initial commit"
```

### Issue: Vercel CLI not found
```
❌ vercel: The term 'vercel' is not recognized
```
**Fix:**
```powershell
npm install -g vercel
```

### Issue: GitHub repo doesn't exist
```
❌ fatal: repository not found
```
**Fix:** Create new repo at https://github.com/new first, then push

---

## ✅ You're Ready!

1. **Run notebook** → Generates pickle files
2. **Push to GitHub** → Stores your code
3. **Deploy to Vercel** → Live globally in 3 minutes
4. **Share URL** → Show friends/colleagues

Your app will be:
- ✅ Live on the internet (global CDN)
- ✅ Auto-scaling (handles 1000s of users)
- ✅ Free HTTPS (secure)
- ✅ 99.95% uptime SLA

---

## 🚀 Quick Command Summary

```powershell
# 1. Generate models (in Jupyter, run all cells)
# (5-10 minutes, run in VS Code)

# 2. After notebook completes, deploy to Vercel
cd d:\sentiment recommendation
npm install -g vercel
git add .
git commit -m "Deploy to Vercel"
git remote add origin https://github.com/YOUR_USERNAME/sentiment-recommender
git push -u origin main
vercel login
vercel --prod

# 3. Open the URL in browser
# Done! Your app is live ✨
```

---

**Start here:** Run the Jupyter notebook first, then follow the steps above. 🚀
