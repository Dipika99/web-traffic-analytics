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
                    sample_website = Website.objects.create(
                        name='Sample Website',
                        domain='https://example.com'
                    )
                    
                    # Create some sample traffic logs
                    TrafficLog.objects.create(
                        website=sample_website,
                        path='/',
                        method='GET',
                        ip_address='192.168.1.1',
                        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        referrer='https://google.com',
                        timestamp=timezone.now()
                    )
                    
                    TrafficLog.objects.create(
                        website=sample_website,
                        path='/about',
                        method='GET',
                        ip_address='192.168.1.2',
                        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                        referrer='https://example.com',
                        timestamp=timezone.now()
                    )
                    
                    self.stdout.write(
                        self.style.SUCCESS('✅ Sample website and traffic data created!')
                    )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating default data: {e}')
            )
