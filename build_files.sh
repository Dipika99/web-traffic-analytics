#!/bin/bash

# Build script for Vercel deployment
echo "🚀 Building for Vercel deployment..."

# Install dependencies
pip3 install -r requirements.txt

# Create staticfiles directory
mkdir -p staticfiles

# Collect static files
python3 manage.py collectstatic --noinput --settings=backend.settings_vercel

# Skip database operations for dummy database
echo "⏭️  Skipping database operations (using dummy database)"

echo "✅ Build completed!"
echo "📁 Contents of staticfiles directory:"
ls -la staticfiles/
