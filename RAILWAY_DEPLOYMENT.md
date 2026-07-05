# 🚀 HealthGuard AI - Railway.app Deployment Guide

## ✅ Prerequisites
- GitHub account (you have it ✓)
- Railway.app account (free)
- Credit card for billing (optional - first $5 credit free)

---

## 📋 STEP-BY-STEP DEPLOYMENT (15 Minutes)

### STEP 1: Create Railway Account
```
1. Go to https://railway.app
2. Click "Start Free"
3. Click "GitHub" button
4. Authorize Railway to access your GitHub
5. You'll be logged in ✓
```

---

### STEP 2: Create New Project
```
1. In Railway Dashboard, click "New Project" (top right)
2. Select "Deploy from GitHub repo"
3. Search for: "Healthgaurd-AI"
4. Click on your repo: "Phantom-dcode/Healthgaurd-AI"
5. Click "Deploy Now"
```

**Railway will auto-detect:**
- ✅ Backend service (Python/FastAPI)
- ✅ Frontend service (React/Node)
- ✅ Needs: PostgreSQL database

---

### STEP 3: Create PostgreSQL Database
```
1. In Railway Dashboard → Your Project
2. Click "New" (top right) → "Database" → "PostgreSQL"
3. Wait for database to initialize (2-3 minutes)
4. Copy the DATABASE_URL when ready
```

**You'll see:**
```
PGDATABASE=railway
PGHOST=containers-us-west-xyz.railway.app
PGPASSWORD=xxxxxxxxxx
PGPORT=7700
PGUSER=postgres
```

---

### STEP 4: Configure Backend Service

#### 4.1 Set Environment Variables
```
1. Dashboard → Services → "backend" service
2. Click "Variables" tab
3. Add these variables:

DEBUG=False
ENVIRONMENT=production
SECRET_KEY=[GENERATE NEW - see below]
ALLOWED_ORIGINS=https://yourdomain.railway.app,http://localhost:5173
AWS_REGION=us-east-1
LOG_LEVEL=INFO
```

#### 4.2 Generate SECRET_KEY
**On your computer, run:**
```bash
openssl rand -hex 32
```
**Copy the output and paste in Railway SECRET_KEY field**

#### 4.3 Add Database Connection
```
1. Still in Backend Variables tab
2. Click "Raw Editor" (toggle at top)
3. Add: DATABASE_URL from PostgreSQL service above
   (It auto-links if you use ${{ Postgres.DATABASE_URL }})
```

#### 4.4 Configure Start Command
```
1. Backend service → "Settings" tab
2. Scroll down to "Deploy"
3. Start Command:
   gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT

4. Click "Save"
```

---

### STEP 5: Configure Frontend Service

#### 5.1 Set Environment Variables
```
1. Dashboard → Services → "frontend" service
2. Click "Variables" tab
3. Add this variable:

VITE_API_URL=https://[BACKEND_URL]/api/v1
```

**Replace [BACKEND_URL] with your backend Railway URL:**
- Go to Backend service → Copy domain
- Example: `https://healthguard-backend-prod-production.up.railway.app`

#### 5.2 Configure Build & Start
```
1. Frontend service → "Settings" tab
2. Build Command:
   cd frontend && npm run build

3. Start Command:
   cd frontend && npm run preview

4. Publish Directory:
   frontend/dist

5. Click "Save"
```

---

### STEP 6: Deploy Everything

```
1. Backend service → "Deploy" tab
2. Click "Redeploy" button
3. Watch logs - wait for "Build successful ✓"
4. Once backend is live, redeploy frontend

5. Frontend service → "Deploy" tab
6. Click "Redeploy" button
7. Wait for deployment to complete
```

**This takes 3-5 minutes**

---

### STEP 7: Get Your Live URLs

```
After both services are deployed:

1. Backend service → Click "⚙️ Settings"
2. Find "Domains" section
3. Copy your backend URL
   Example: https://healthguard-backend-prod-production.up.railway.app

4. Frontend service → "⚙️ Settings"
5. Find "Domains" section
6. Copy your frontend URL
   Example: https://healthguard-frontend-prod-production.up.railway.app
```

---

### STEP 8: Test Your Deployment ✅

```bash
# Test 1: Backend Health Check
curl https://[YOUR-BACKEND-URL]/api/v1/health

# Test 2: Login API
curl -X POST https://[YOUR-BACKEND-URL]/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@healthguard.ai","password":"Admin@123"}'

# Test 3: View API Docs
Open: https://[YOUR-BACKEND-URL]/docs

# Test 4: Open Frontend
Open: https://[YOUR-FRONTEND-URL] in browser
```

**Expected Results:**
- ✅ Health check returns 200 OK
- ✅ Login returns JWT tokens
- ✅ Swagger API docs load
- ✅ Frontend dashboard loads

---

### STEP 9: Setup Custom Domain (Optional)

```
1. Railway Dashboard → Project Settings
2. Domains → "Add Domain"
3. Enter your domain: yourdomain.com
4. Click "Add"
5. Railway gives you DNS records
6. Go to your domain registrar (GoDaddy, Namecheap, etc.)
7. Add DNS records:
   - Type: CNAME
   - Name: yourdomain.com
   - Value: [Railway DNS target]
8. Wait 24 hours for DNS propagation
```

---

### STEP 10: Setup Environment for Production

```
1. Backend service → Variables
2. Update ALLOWED_ORIGINS:
   ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

3. Frontend service → Variables
4. Update VITE_API_URL:
   VITE_API_URL=https://yourdomain.com/api/v1

5. Redeploy both services
```

---

## 🎯 COMPLETE CHECKLIST

- [ ] Created Railway account
- [ ] Connected GitHub repo
- [ ] Created PostgreSQL database
- [ ] Set backend environment variables (SECRET_KEY, DEBUG, etc.)
- [ ] Set frontend environment variable (VITE_API_URL)
- [ ] Configured backend start command (Gunicorn)
- [ ] Configured frontend build & start
- [ ] Backend deployed successfully
- [ ] Frontend deployed successfully
- [ ] Tested API health endpoint
- [ ] Tested login endpoint
- [ ] Tested frontend loads
- [ ] (Optional) Added custom domain
- [ ] (Optional) Configured production ALLOWED_ORIGINS

---

## 🚀 QUICK REFERENCE - Copy-Paste Ready

### Backend Environment Variables
```
DEBUG=False
ENVIRONMENT=production
SECRET_KEY=GENERATE-WITH-openssl-rand-hex-32
ALLOWED_ORIGINS=https://yourdomain.railway.app
DATABASE_URL=${{ Postgres.DATABASE_URL }}
AWS_REGION=us-east-1
LOG_LEVEL=INFO
```

### Frontend Environment Variable
```
VITE_API_URL=https://[YOUR-BACKEND-RAILWAY-URL]/api/v1
```

### Backend Start Command
```
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

### Frontend Build Command
```
cd frontend && npm run build
```

### Frontend Start Command
```
cd frontend && npm run preview
```

---

## ✅ Success Indicators

After deployment, you should see:

```
✓ Backend service shows "Active" in green
✓ Frontend service shows "Active" in green
✓ PostgreSQL shows "Active" in green
✓ No errors in deployment logs
✓ API responds to /api/v1/health endpoint
✓ Frontend loads at frontend URL
✓ Can login with admin@healthguard.ai / Admin@123
```

---

## 🆘 Troubleshooting

### Problem: "Backend not deploying"
**Solution:**
```
1. Check logs: Backend → "Logs" tab
2. Look for error messages
3. Common issues:
   - Missing SECRET_KEY
   - Invalid DATABASE_URL
   - Wrong start command
```

### Problem: "Frontend showing API error"
**Solution:**
```
1. Check frontend logs: Frontend → "Logs" tab
2. Check VITE_API_URL is correct
3. It should NOT have trailing slash
4. Redeploy frontend after fixing
```

### Problem: "Cannot connect to database"
**Solution:**
```
1. Database → "Logs" tab
2. Check PostgreSQL is running (green status)
3. Verify DATABASE_URL in Backend variables
4. Use: ${{ Postgres.DATABASE_URL }}
5. Restart backend service
```

### Problem: "Getting 502 Bad Gateway"
**Solution:**
```
1. Backend service crashed
2. Check backend logs for errors
3. Common causes:
   - Port binding issue
   - Missing dependencies
   - Database connection failed
4. Click "Redeploy" to try again
```

---

## 📊 Monitoring Your Deployment

```
Railway Dashboard → Your Project:

1. Check Service Status (should all be Green ✓)
2. View Logs (Backend → Logs tab)
3. Monitor Resource Usage (Backend → Metrics tab)
4. Check Database Status (PostgreSQL → Status)
5. View Deployment History (Services → Deployments)
```

---

## 💰 Costs

Railway gives you:
- ✅ $5 free credit per month
- ✅ No upfront payment needed
- ✅ Only pay for what you use

**Estimated costs for HealthGuard AI:**
- Backend (FastAPI): $2-5/month
- Frontend (Node): $1-3/month
- PostgreSQL (1GB): $2-4/month
- **Total: $5-12/month**

Free tier usually covers it! 🎉

---

## 🎉 YOU'RE LIVE!

After completing these steps, your HealthGuard AI will be:

✅ Live on the internet  
✅ Accessible 24/7  
✅ Auto-scaled if traffic increases  
✅ Database backed up daily  
✅ HTTPS/SSL certificate (free)  
✅ Auto-deploys on git push to deployment-ready branch  

---

## 📱 What's Next?

1. **Setup Git Auto-Deploy** (Optional)
   ```bash
   # Every push to deployment-ready branch auto-deploys
   git push origin deployment-ready
   ```

2. **Setup Monitoring** (Optional)
   - Add error tracking: Sentry.io
   - Add uptime monitoring: UptimeRobot

3. **Setup Custom Domain** (Optional)
   - Add your own domain
   - Setup SSL certificate (free via Railway)

4. **Setup Backups** (Optional)
   - Railway auto-backups daily
   - Export backups to S3 if needed

---

## 📞 Need Help?

If you get stuck:
1. Check Railway docs: https://docs.railway.app
2. Check your service logs first
3. Common solution: Redeploy the service
4. If still stuck: Share the error logs and I'll help!

---

## 🏁 FINAL STEPS SUMMARY

```
1. Go to railway.app → Sign up with GitHub
2. Create new project from your GitHub repo
3. Add PostgreSQL database
4. Configure Backend variables & start command
5. Configure Frontend variables & build command
6. Deploy both services
7. Test endpoints
8. ✅ DONE! Your app is LIVE!
```

**Time to deployment: 15-20 minutes**

Good luck! 🚀
