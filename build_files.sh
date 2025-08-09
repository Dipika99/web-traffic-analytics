#!/bin/bash

# Build script for Vercel deployment
echo "🚀 Building for Vercel deployment..."

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput --settings=backend.settings_vercel

# Run migrations
python manage.py migrate --settings=backend.settings_vercel

echo "✅ Build completed!"
