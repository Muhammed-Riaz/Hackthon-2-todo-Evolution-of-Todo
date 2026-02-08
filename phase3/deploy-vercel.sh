#!/bin/bash
# Vercel Deployment Script

echo "=========================================="
echo "Deploying Frontend to Vercel"
echo "=========================================="

# Navigate to frontend directory
cd frontend

# Install Vercel CLI if not already installed
echo "Checking Vercel CLI..."
if ! command -v vercel &> /dev/null; then
    echo "Installing Vercel CLI..."
    npm install -g vercel
fi

# Login to Vercel (if not already logged in)
echo "Logging in to Vercel..."
vercel login

# Deploy to production
echo "Deploying to production..."
vercel --prod

echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Copy your Vercel deployment URL"
echo "2. Update CORS in your Hugging Face backend to allow your Vercel domain"
echo "3. Test the application"
