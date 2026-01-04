from django.core.management.base import BaseCommand
from apps.orders.models import City


class Command(BaseCommand):
    help = 'Créer les villes avec leurs numéros WhatsApp'

    def handle(self, *args, **options):
        cities_data = [
            {
                'name': 'Bafoussam',
                'whatsapp_number': '237659270205',
                'is_active': True,
                'display_order': 1
            },
            {
                'name': 'Douala',
                'whatsapp_number': '237691563244',
                'is_active': True,
                'display_order': 2
            },
            {
                'name': 'Yaoundé',
                'whatsapp_number': '237698566659',
                'is_active': True,
                'display_order': 3
            },
        ]

        self.stdout.write('🏙️  Création des villes...\n')
        
        for city_data in cities_data:
            city, created = City.objects.update_or_create(
                name=city_data['name'],
                defaults={
                    'whatsapp_number': city_data['whatsapp_number'],
                    'is_active': city_data['is_active'],
                    'display_order': city_data['display_order']
                }
            )
            
            status = '✅ Créée' if created else '🔄 Mise à jour'
            self.stdout.write(
                f"{status} : {self.style.SUCCESS(city.name)} - "
                f"WhatsApp: {city.whatsapp_number}"
            )
        
        self.stdout.write(
            self.style.SUCCESS(f"\n✨ Total : {City.objects.count()} ville(s)")
        )