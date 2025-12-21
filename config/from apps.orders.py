from apps.orders.models import City

# Douala
City.objects.create(
    name='Douala',
    whatsapp_number='237691563244',  # ⚠️ REMPLACEZ par votre vrai numéro
    display_order=1,
    is_active=True
)

# Yaoundé
City.objects.create(
    name='Yaoundé',
    whatsapp_number='237698566659',  # ⚠️ REMPLACEZ par votre vrai numéro
    display_order=2,
    is_active=True
)

# Bafoussam
City.objects.create(
    name='Bafoussam',
    whatsapp_number='237659270205',  # ⚠️ REMPLACEZ par votre vrai numéro
    display_order=3,
    is_active=True
)

# Vérifier
City.objects.all()

exit()