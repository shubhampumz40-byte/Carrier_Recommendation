#!/usr/bin/env python3
"""
Career Compass - Permanent URL Deployment
This script helps you get ONE permanent public URL that never changes
"""

import os
import json
import subprocess
from datetime import datetime

def create_permanent_url_guide():
    """Create a guide for getting one permanent URL"""
    
    guide = """
# 🌐 ONE PERMANENT URL FOR CAREER COMPASS

## 🎯 THE PROBLEM:
- Cloudflare tunnels create NEW URLs every time they restart
- URLs like "understanding-heath-cos-rip.trycloudflare.com" keep changing
- You want ONE permanent URL that NEVER changes

## ✅ THE SOLUTION: Railway Deployment

### 🚀 Railway gives you ONE permanent URL:
**Example: https://career-compass-production.up.railway.app**
- ✅ NEVER changes
- ✅ Always online (24/7)
- ✅ Professional looking
- ✅ Works even when your computer is off

## 📋 SIMPLE 5-MINUTE SETUP:

### Step 1: Create GitHub Account (if you don't have one)
1. Go to: https://github.com/join
2. Sign up with your email

### Step 2: Create Repository
1. Go to: https://github.com/new
2. Repository name: `career-compass`
3. Make it Public
4. Click "Create repository"

### Step 3: Upload Your Code
1. Click "uploading an existing file"
2. Drag and drop ALL files from your project folder
3. Write commit message: "Initial Career Compass upload"
4. Click "Commit changes"

### Step 4: Deploy to Railway
1. Go to: https://railway.app
2. Click "Login" → "Login with GitHub"
3. Click "New Project"
4. Click "Deploy from GitHub repo"
5. Select "career-compass"
6. Wait 2-3 minutes for deployment

### Step 5: Get Your PERMANENT URL
Railway will give you a URL like:
**https://career-compass-production.up.railway.app**

This URL will NEVER change and work 24/7!

## 🎉 BENEFITS:
- ✅ ONE permanent URL (never changes)
- ✅ Always online (24/7)
- ✅ Professional domain
- ✅ Free hosting
- ✅ Auto-updates when you change code
- ✅ Works worldwide
- ✅ No computer needed

## 📱 SHARE YOUR PERMANENT LINK:
```
🧭 Career Compass - AI Career Recommender
https://career-compass-production.up.railway.app

✨ Permanent Link - Never Changes!
• Personalized AI recommendations
• 36 inspiring role models
• Trending careers 2025-2035
• Interactive career simulations

Perfect for students! 🚀
```

## 🔗 QUICK LINKS:
- GitHub: https://github.com/new
- Railway: https://railway.app
- Your future permanent URL: https://career-compass-production.up.railway.app

## ⚡ ALTERNATIVE QUICK OPTIONS:

### Option 2: Render (Also gives permanent URL)
1. GitHub: https://github.com/new (upload code)
2. Render: https://render.com (connect GitHub)
3. Your URL: https://career-compass.onrender.com

### Option 3: Vercel (For static sites)
1. GitHub: https://github.com/new
2. Vercel: https://vercel.com
3. Your URL: https://career-compass.vercel.app

## 🎯 RECOMMENDATION:
Use Railway - it's the easiest and gives you the most professional permanent URL.

Once deployed, you'll have ONE URL that:
- Never changes
- Always works
- Looks professional
- Works 24/7 without your computer

No more changing URLs! 🌟
"""
    
    with open('PERMANENT_URL_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print("✅ Created PERMANENT_URL_GUIDE.md")
    print("\n🎯 TO GET ONE PERMANENT URL:")
    print("1. Read PERMANENT_URL_GUIDE.md")
    print("2. Follow the 5-minute Railway setup")
    print("3. Get your permanent URL that NEVER changes!")

def show_current_issue():
    """Show the current URL changing issue"""
    print("🚨 CURRENT ISSUE:")
    print("- Cloudflare tunnels create NEW URLs every restart")
    print("- Your URLs keep changing:")
    print("  ❌ https://animated-variations-xbox-knitting.trycloudflare.com")
    print("  ❌ https://calculators-crucial-rear-qualification.trycloudflare.com") 
    print("  ❌ https://stickers-ringtone-fleet-sun.trycloudflare.com")
    print("  ❌ https://understanding-heath-cos-rip.trycloudflare.com")
    print("\n✅ SOLUTION: Deploy to Railway for ONE permanent URL")
    print("  ✅ https://career-compass-production.up.railway.app (NEVER changes)")

def main():
    print("🧭 Career Compass - ONE Permanent URL Solution")
    print("=" * 60)
    
    show_current_issue()
    print("\n" + "=" * 60)
    create_permanent_url_guide()
    
    print("\n🌟 NEXT STEPS:")
    print("1. Open PERMANENT_URL_GUIDE.md")
    print("2. Follow the Railway deployment steps")
    print("3. Get your ONE permanent URL!")
    print("\n🔗 Start here: https://railway.app")

if __name__ == "__main__":
    main()