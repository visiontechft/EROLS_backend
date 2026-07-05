from django.core.management.base import BaseCommand
from apps.orders.models import City


class Command(BaseCommand):
    help = 'Créer les quartiers de Bafoussam avec leurs numéros WhatsApp'

    def handle(self, *args, **options):
        whatsapp_number = '237659270205'

        quartiers_data = [
            {'name': 'Tamdja', 'display_order': 1},
            {'name': 'Kamkop', 'display_order': 2},
            {'name': 'Marché A', 'display_order': 3},
            {'name': 'Marché B', 'display_order': 4},
            {'name': 'Ndiangdam', 'display_order': 5},
            {'name': 'Tocket', 'display_order': 6},
            {'name': 'Banengo', 'display_order': 7},
            {'name': 'Djeleng', 'display_order': 8},
        ]

        self.stdout.write('🏘️  Création des quartiers de Bafoussam...\n')

        for quartier_data in quartiers_data:
            quartier, created = City.objects.update_or_create(
                name=quartier_data['name'],
                defaults={
                    'whatsapp_number': whatsapp_number,
                    'is_active': True,
                    'display_order': quartier_data['display_order'],
                }
            )

            status = '✅ Créé' if created else '🔄 Mis à jour'
            self.stdout.write(
                f"{status} : {self.style.SUCCESS(quartier.name)} - "
                f"WhatsApp: {quartier.whatsapp_number}"
            )

        # Désactiver les anciennes entrées "villes" qui ne sont plus utilisées
        old_cities = City.objects.filter(name__in=['Douala', 'Yaoundé', 'Bafoussam']).exclude(
            name__in=[q['name'] for q in quartiers_data]
        )
        deactivated = old_cities.update(is_active=False)
        if deactivated:
            self.stdout.write(self.style.WARNING(f"\n🗑️  {deactivated} ancienne(s) ville(s) désactivée(s)"))

        self.stdout.write(
            self.style.SUCCESS(f"\n✨ Total : {City.objects.filter(is_active=True).count()} quartier(s) actif(s)")
        )
