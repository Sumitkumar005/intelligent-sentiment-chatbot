# 🚀 Deployment Guide

## Current Deployment

**Live URL:** [sumitsaini.com](https://sumitsaini.com)  
**Platform:** Render (Free Tier)  
**Status:** ✅ Operational

### ⚠️ Important Notes

1. **Cold Start Time**: 15-20 seconds on first visit (Render free tier spins down after inactivity)
2. **Database**: SQLite (file-based, resets on redeploy)
3. **Conversation History**: Not persistent across deployments on current setup

---

## Deploying to Render

### Backend Deployment

1. **Create Web Service**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select branch: `main`

2. **Configure Service**
   ```
   Name: sentiment-chatbot-backend
   Region: Choose closest to your users
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```

3. **Environment Variables**
   ```
   GROQ_API_KEY=gsk_your_groq_api_key
   GMAIL_TOKEN={"token":"ya29...","refresh_token":"1//...","token_uri":"..."}
   EMAIL_SENDER=your-email@gmail.com
   JWT_SECRET=your-super-secret-key-change-this
   FLASK_ENV=production
   DATABASE_PATH=/opt/render/project/src/chatbot.db
   FRONTEND_URL=https://your-frontend-url.com
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete (~3-5 minutes)
   - Note the backend URL (e.g., `https://sentiment-chatbot-backend.onrender.com`)

### Frontend Deployment

1. **Update API URL**
   - Edit `frontend/src/services/api.js`
   - Change `BASE_URL` to your backend URL:
   ```javascript
   const BASE_URL = 'https://sentiment-chatbot-backend.onrender.com/api';
   ```

2. **Build Frontend**
   ```bash
   cd frontend
   npm run build
   ```

3. **Deploy to Render Static Site**
   - Go to Render Dashboard
   - Click "New +" → "Static Site"
   - Connect repository
   - Configure:
     ```
     Name: sentiment-chatbot-frontend
     Branch: main
     Root Directory: frontend
     Build Command: npm install && npm run build
     Publish Directory: dist
     ```

4. **Custom Domain (Optional)**
   - Go to Settings → Custom Domains
   - Add your domain (e.g., sumitsaini.com)
   - Update DNS records as instructed

---

## Alternative Deployment Options

### Option 1: Vercel (Frontend) + Render (Backend)

**Frontend on Vercel:**
```bash
cd frontend
npm install -g vercel
vercel --prod
```

**Backend on Render:** (Same as above)

### Option 2: Railway

**Full Stack on Railway:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy backend
cd backend
railway up

# Deploy frontend
cd ../frontend
railway up
```

### Option 3: Heroku

**Backend:**
```bash
cd backend
heroku create sentiment-chatbot-backend
git push heroku main
heroku config:set GROQ_API_KEY=your_key
heroku config:set GMAIL_TOKEN='{"token":"..."}'
```

**Frontend:**
```bash
cd frontend
heroku create sentiment-chatbot-frontend
heroku buildpacks:set heroku/nodejs
git push heroku main
```

---

## Production Recommendations

### For Production Use (Beyond Assignment)

1. **Database Migration**
   - Migrate from SQLite to PostgreSQL
   - Use Render's PostgreSQL add-on or external service
   - Update `database.py` to use SQLAlchemy with PostgreSQL

2. **File Storage**
   - Use cloud storage (AWS S3, Cloudinary) for persistent data
   - Store conversation history in cloud database

3. **Upgrade Hosting**
   - Move to paid tier for:
     - No cold starts
     - Better performance
     - More resources
     - Custom domains

4. **Add Monitoring**
   - Sentry for error tracking
   - LogRocket for session replay
   - Google Analytics for usage metrics

5. **Security Enhancements**
   - Add rate limiting (Flask-Limiter)
   - Implement CORS properly
   - Use environment-specific configs
   - Add API key rotation

6. **Performance Optimization**
   - Add Redis for caching
   - Implement CDN for static assets
   - Use connection pooling
   - Add load balancing

---

## Environment-Specific Configuration

### Development
```env
FLASK_ENV=development
FLASK_DEBUG=True
FRONTEND_URL=http://localhost:5173
DATABASE_PATH=./chatbot.db
```

### Production
```env
FLASK_ENV=production
FLASK_DEBUG=False
FRONTEND_URL=https://your-domain.com
DATABASE_PATH=/opt/render/project/src/chatbot.db
```

---

## Troubleshooting Deployment

### Backend Issues

**Problem:** "Application failed to start"
- Check logs: `render logs`
- Verify all environment variables are set
- Ensure `requirements.txt` is complete
- Check Python version compatibility

**Problem:** "Database not found"
- Verify `DATABASE_PATH` is correct
- Ensure write permissions
- Run migrations after deployment

**Problem:** "Gmail API authentication failed"
- Verify `GMAIL_TOKEN` is valid JSON
- Check token hasn't expired
- Regenerate token if needed

### Frontend Issues

**Problem:** "API calls failing"
- Check `BASE_URL` in `api.js`
- Verify CORS settings on backend
- Check network tab for errors

**Problem:** "Build fails"
- Clear `node_modules` and reinstall
- Check Node.js version (16+)
- Verify all dependencies in `package.json`

---

## Monitoring Deployment

### Check Backend Health
```bash
curl https://your-backend-url.com/api/health
```

### Check Frontend
```bash
curl https://your-frontend-url.com
```

### View Logs
```bash
# Render Dashboard → Your Service → Logs
# Or use Render CLI:
render logs -s your-service-name
```

---

## Rollback Strategy

### If Deployment Fails

1. **Render Dashboard:**
   - Go to Deploys tab
   - Click "Rollback" on previous successful deploy

2. **Git Revert:**
   ```bash
   git revert HEAD
   git push origin main
   ```

3. **Manual Fix:**
   - Fix the issue locally
   - Test thoroughly
   - Commit and push
   - Redeploy

---

## Cost Estimation

### Current Setup (Free Tier)
- **Render Free:** $0/month
- **Groq API:** $0/month (free tier)
- **Gmail API:** $0/month (free)
- **Total:** $0/month

### Recommended Production Setup
- **Render Starter:** $7/month (backend)
- **Render Static:** $0/month (frontend)
- **PostgreSQL:** $7/month (database)
- **Groq API:** ~$10/month (estimated usage)
- **Total:** ~$24/month

---

## Post-Deployment Checklist

- [ ] Backend URL accessible
- [ ] Frontend URL accessible
- [ ] Login flow works (OTP emails sent)
- [ ] Chat functionality works
- [ ] Sentiment analysis displays correctly
- [ ] Conversation summary works
- [ ] Voice features work (if HTTPS)
- [ ] Mobile responsive
- [ ] No console errors
- [ ] All environment variables set
- [ ] Custom domain configured (if applicable)

---

**Deployment Status:** ✅ Live at [sumitsaini.com](https://sumitsaini.com)

**Last Updated:** [Current Date]
