#!/bin/bash

# Production Deployment Script
echo "🚀 Starting production deployment..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --settings=backend.settings_production

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --settings=backend.settings_production

# Create superuser if needed (uncomment if needed)
# echo "👤 Creating superuser..."
# python manage.py createsuperuser --settings=backend.settings_production

echo "✅ Deployment completed successfully!"
echo "🌐 Your app should now be running on the configured domain." 
