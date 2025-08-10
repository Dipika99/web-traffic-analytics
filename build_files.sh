#!/bin/bash

# Build script for Vercel deployment
echo "🚀 Building for Vercel deployment..."

# Install dependencies
pip3 install -r requirements.txt

# Create staticfiles directory
mkdir -p staticfiles

# Collect static files
python3 manage.py collectstatic --noinput --settings=backend.settings_vercel

# Database operations for PostgreSQL
echo "🗄️  Setting up PostgreSQL database..."
python3 manage.py migrate --settings=backend.settings_vercel
python3 manage.py create_default_superuser --settings=backend.settings_vercel

echo "✅ Build completed!"
echo "📁 Contents of staticfiles directory:"
ls -la staticfiles/
