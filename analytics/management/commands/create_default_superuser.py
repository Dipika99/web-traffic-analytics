from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from analytics.models import Website, TrafficLog
from django.utils import timezone


class Command(BaseCommand):
    help = 'Create a default superuser and sample data for the application'

    def handle(self, *args, **options):
        default_username = 'admin'
        default_email = 'admin@example.com'
        default_password = 'admin123'

        try:
            with transaction.atomic():
                # Check if the default admin user already exists
                if not User.objects.filter(username=default_username).exists():
                    User.objects.create_superuser(
                        username=default_username,
                        email=default_email,
                        password=default_password
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✅ Default superuser created successfully!\n'
                            f'Username: {default_username}\n'
                            f'Password: {default_password}\n'
                            f'Email: {default_email}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'⚠️  Default superuser "{default_username}" already exists'
                        )
                    )

                # Create sample website and traffic data
                if not Website.objects.exists():
                    # Create multiple sample websites
                    websites_data = [
                        {'name': 'Example Corp', 'domain': 'https://example.com'},
                        {'name': 'Demo Store', 'domain': 'https://demo-store.com'},
                        {'name': 'Test Blog', 'domain': 'https://testblog.net'},
                        {'name': 'Portfolio Site', 'domain': 'https://myportfolio.dev'},
                        {'name': 'News Portal', 'domain': 'https://dailynews.org'},
                    ]
                    
                    for site_data in websites_data:
                        website = Website.objects.create(
                            name=site_data['name'],
                            domain=site_data['domain']
                        )
                        
                        # Create diverse traffic logs for each website
                        traffic_data = [
                            {
                                'path': '/',
                                'method': 'GET',
                                'ip': '192.168.1.1',
                                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                                'referrer': 'https://google.com'
                            },
                            {
                                'path': '/about',
                                'method': 'GET', 
                                'ip': '192.168.1.2',
                                'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                                'referrer': site_data['domain']
                            },
                            {
                                'path': '/contact',
                                'method': 'POST',
                                'ip': '10.0.0.1',
                                'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15',
                                'referrer': f"{site_data['domain']}/about"
                            },
                            {
                                'path': '/products',
                                'method': 'GET',
                                'ip': '172.16.0.1',
                                'user_agent': 'Mozilla/5.0 (Android 11; Mobile; rv:91.0) Gecko/91.0 Firefox/91.0',
                                'referrer': 'https://facebook.com'
                            }
                        ]
                        
                        for traffic in traffic_data:
                            TrafficLog.objects.create(
                                website=website,
                                path=traffic['path'],
                                method=traffic['method'],
                                ip_address=traffic['ip'],
                                user_agent=traffic['user_agent'],
                                referrer=traffic['referrer'],
                                timestamp=timezone.now()
                            )
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Created {len(websites_data)} sample websites with traffic data!')
                    )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating default data: {e}')
            )
