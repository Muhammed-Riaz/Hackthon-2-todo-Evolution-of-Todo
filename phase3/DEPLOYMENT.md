# Deployment Guide: Frontend to Vercel

## Prerequisites
- Vercel account (sign up at https://vercel.com)
- Git repository pushed to GitHub/GitLab/Bitbucket
- Backend deployed and running on Hugging Face

## Step 1: Fix Hugging Face Backend (IMPORTANT!)

Before deploying frontend, ensure your backend is working:

### 1.1 Check Backend Status
Visit: https://huggingface.co/spaces/riaz110/phase3

### 1.2 Required Environment Variables on Hugging Face
Make sure these are set in your Space settings:

```
DATABASE_URL=postgresql+asyncpg://neondb_owner:npg_KzNuXVCp2RB5@ep-dark-union-ahj01ro8-pooler.c-3.us-east-1.aws.neon.tech/neondb
SECRET_KEY=n34_axppdz3mO2qxH5jUdwXj0JFzj09logjcHZfzfLs
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
ENVIRONMENT=production
```

### 1.3 Update Backend CORS for Vercel
After you deploy to Vercel, you'll get a URL like: `https://your-app.vercel.app`

Update your backend's `main.py` CORS configuration to include your Vercel domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://your-app.vercel.app",  # Add your Vercel URL here
        "https://*.vercel.app"  # Allow all Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Step 2: Deploy to Vercel

### Option A: Deploy via Vercel Dashboard (Easiest)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

2. **Go to Vercel Dashboard**
   - Visit https://vercel.com/new
   - Click "Import Project"
   - Select your GitHub repository

3. **Configure Project**
   - Framework Preset: **Next.js**
   - Root Directory: **frontend**
   - Build Command: `npm run build` (default)
   - Output Directory: `.next` (default)

4. **Add Environment Variables**
   Click "Environment Variables" and add:
   ```
   NEXT_PUBLIC_API_URL=https://riaz110-phase3.hf.space
   NEXT_PUBLIC_BETTER_AUTH_URL=https://riaz110-phase3.hf.space
   ```

5. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete (2-3 minutes)
   - Copy your deployment URL

### Option B: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy from frontend directory**
   ```bash
   cd frontend
   vercel --prod
   ```

4. **Follow the prompts**
   - Set up and deploy? **Y**
   - Which scope? Select your account
   - Link to existing project? **N**
   - What's your project's name? **phase3-todo** (or your choice)
   - In which directory is your code located? **./frontend**
   - Want to override settings? **N**

## Step 3: Post-Deployment Configuration

### 3.1 Update Backend CORS
Once you have your Vercel URL (e.g., `https://phase3-todo.vercel.app`):

1. Go to your Hugging Face Space
2. Update `main.py` CORS to include your Vercel URL
3. Restart the Space

### 3.2 Test Your Deployment

1. Visit your Vercel URL
2. Register a new account
3. Go to `/chat` and create a task
4. Check `/dashboard` to see if the task appears
5. Verify in Neon database

## Step 4: Custom Domain (Optional)

If you have a custom domain:

1. Go to Vercel Dashboard → Your Project → Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed
4. Update backend CORS to include your custom domain

## Troubleshooting

### Issue: CORS Errors
**Solution**: Make sure your Vercel URL is added to backend CORS configuration

### Issue: 404 on API Calls
**Solution**: Verify `NEXT_PUBLIC_API_URL` environment variable is set correctly

### Issue: Authentication Not Working
**Solution**: Check that `NEXT_PUBLIC_BETTER_AUTH_URL` matches your backend URL

### Issue: Backend Not Responding
**Solution**:
- Check Hugging Face Space status
- Verify environment variables are set
- Check Space logs for errors

## Verification Checklist

- [ ] Backend is running on Hugging Face (check /health endpoint)
- [ ] Environment variables set on Vercel
- [ ] CORS configured on backend to allow Vercel domain
- [ ] Frontend deployed successfully
- [ ] Can register/login
- [ ] Can create tasks via chat
- [ ] Tasks appear on dashboard
- [ ] Tasks saved to Neon database

## Useful Commands

```bash
# Check deployment status
vercel ls

# View deployment logs
vercel logs

# Redeploy
vercel --prod

# Remove deployment
vercel remove [deployment-url]
```

## Support

If you encounter issues:
1. Check Vercel deployment logs
2. Check Hugging Face Space logs
3. Check browser console for errors
4. Verify all environment variables are set correctly
