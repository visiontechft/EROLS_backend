"""Resets product prices back to their original import-time values, recovered
from two sources that together account for ~306 of the ~323 live products:

- BY_SLUG: the 70 products from the initial WhatsApp catalog import
  (recovered from the now-deleted import_whatsapp_catalog.py, which embedded
  each product's original price directly in its source).
- BY_NAME: the 236 uniquely-named products from the "batch 2" catalog import
  (recovered from a working export of that import, new_catalog_final.json).
  17 entries with ambiguous duplicate names (e.g. several products all named
  "Trotinette") were deliberately excluded rather than guessed at.

This exists to undo the effects of every bulk price adjustment applied since
import — including the tier1+tier2 double-application bug — by returning to
a known-good baseline. After running this for real, re-apply the confirmed
price tier barème once via the (now-fixed) bulk-price-tiers tool.

Products not covered by either source (added later through the admin tool,
or one of the 17 excluded duplicates) are left untouched and listed at the
end for manual review.
"""
from django.core.management.base import BaseCommand

from apps.products.models import Product

BY_SLUG = {'cuisiniere-a-gaz-oscar-3080b-5-foyers-60x76cm': 135000, 'cuisiniere-a-gaz-oscar-g85ne-luxe-5-foyers-avec-po': 170000, 'cuisiniere-a-gaz-oscar-60b-4-foyers-60x60cm': 105000, 'refrigerateur-vitrine-oscar-v250-170l': 190000, 'refrigerateur-oscar-r165s-138l': 120000, 'refrigerateur-oscar-m280d-227l-distributeur-deau': 165000, 'congelateur-hisense-fc-490-315l': 215000, 'refrigerateur-hisense-rd34-262l-double-porte': 250000, 'refrigerateur-midea-mdrt237-173l-double-porte': 140000, 'four-electrique-oscar-4502-45l-1800w': 55000, 'friteuse-a-air-tobi-tb-978-16l-2400w': 35000, 'friteuse-a-air-tobi-tb-969-15l-double-panier-ecran': 50000, 'machine-a-laver-hisense-twin-tub-135kg': 160000, 'hachoirmixeur-electrique-2-en-1-4l': 19000, 'set-ustensiles-de-cuisine-rose-louches-couteaux-si': 9000, 'machine-a-coudre-handy-stitch-electrique-avec-peda': 5000, 'machine-a-coudre-mini-portable-manuelle-a-piles': 2000, 'enceinte-multimedia-oscar-2028t-home-cinema': 65000, 'barre-de-son-oscar-1515b': 45000, 'barre-de-son-hisense-ax-3100-500w': 85000, 'microphone-sans-fil-universel': 2500, 'microphone-sans-fil-f11-2-3n1': 3500, 'ecouteurs-sans-fil-k54-tws': 2000, 'regulateur-de-tension-fodeg-star-dvr-1000va-1000w': 14000, 'compresseur-dair-booster-de-voiture-4-en-1-recharg': 20000, 'kit-eclairage-led-photovideo-pro-led-600-sur-trepi': 15000, 'kit-eclairage-led-giftmax-u800-rgb': 20000, 'lampe-led-photo-rmg-pl-48': 12000, 'combo-montre-connectee-casque-ecouteurs-okpu-rock': 6500, 'telecommande-tv-lg-plasmasmart': 500, 'telecommande-tv-star-x-ecran-plasma': 1000, 'telecommande-decodeur-star-track-universel-mpg4': 500, 'telecommande-decodeur-starx-hd10': 500, 'telecommande-tv-philips-rc7940': 500, 'telecommande-decodeur-universel-supermax-9200-smar': 500, 'telecommande-decodeur-digisat': 500, 'telecommande-decodeur-samtel-universel-mpg4': 500, 'telecommande-decodeur-powerpass-pp-4020-hd': 500, 'telecommande-light-wave-ecran-plasma': 1000, 'telecommande-vestel-2440-tvplasma-universel': 500, 'bouteille-thermos-inox-500ml-ecran-de-temperature': 1500, 'pistolet-de-massage-j1': 3500, 'pistolet-de-massage-rf-723x': 3500, 'pistolet-de-massage-fascial-gun-rf-321': 5000, 'appareil-de-massage-multi-zones-dos-cou-bras-cuiss': 12000, 'tondeuse-cheveux-sans-fil-rechargeable': 4000, 'lampe-uv-sechage-ongles-sun-wy-06': 5000, 'lampe-uv-sechage-ongles-sun-s10-professional': 10000, 'lampe-uv-sechage-ongles-doragym-cordless-rechargea': 10000, 'coffret-huiles-essentielles-fragrant-garden-6x10ml': 1800, 'dalle-pvc-autocollante-sol-marbre-noir-60x60cm': 1300, 'dalle-pvc-autocollante-spc88032-marbre-blancor-60x': 1300, 'dalle-pvc-autocollante-lvt88010-marbre-blanc-60x60': 1300, 'tapis-chaine-doree-fond-marron': 13000, 'tapis-versace-medaillon-noiror': 13000, 'tapis-louis-vuitton-bleubulles': 13000, 'tapis-louis-vuitton-monogramme': 13000, 'tapis-roses-dorees-fond-noir': 13000, 'tapis-poissons-koi-dores': 13000, 'tapis-rougeblancor-motif-cercles': 13000, 'tapis-noirgrisjaune-tourbillon': 13000, 'tapis-versace-damier-ornoir': 13000, 'tapis-plume-doreenoire-abstrait': 13000, 'tapis-tourbillon-bleurougeblanc': 13000, 'tapis-versace-zebre-noirblanc': 13000, 'matelas-gonflable-deux-places': 12000, 'fauteuil-gonflable-pouf-assorti': 8500, 'diffuseur-darome-a-flamme-aroma': 5000, 'diffuseurhumidificateur-sportiness-a-6-pompes': 5000, 'eplucheur-rechargeable-pour-fruits-et-legumes': 5000}

BY_NAME = {'Carreaux mosaique en metal et verre 3D autocolant 30cm×30cm': 1000, 'Ruban adhesif 200M': 1500, 'Fiche adaptateur multiple': 250, 'Pile rechargeable long 18650 / 3.7V / 6800mah': 500, 'Batterie solaire 12V/7AH': 4000, 'Batterie 4V/4AH': 1500, 'Detecteur de faux billet TK- 2028': 4000, "Ampoule rechargeable 150w d'origine": 3000, "Ampoule rechargeable d'origine 150W": 3000, 'Speakon': 300, 'Fiche adaptateur marken': 250, 'Projecteur solaire exterieur led 200W fonctionement automatique et avec telecommande': 8000, 'Telecommande universele pour ecran plasma': 1000, 'Telecommande universel Led TV': 500, 'Telecommande canal+ HD': 500, 'Cordon AV 3/3': 200, 'Rallonge 016': 600, 'Rallonge 017': 700, 'Rallonge 018': 800, "Rallonge 990 d'origine avec controleur de tension et coupe circuit": 4000, 'Prise multiple parasurtenseur Power Source Protector, modele 990': 4000, 'Micro balladeur rechargeable VM150PRO': 25000, 'Micro balladeur JBL CMC11': 35000, 'Ponceuse Kemei a 3 lames': 4500, 'Papier peint autocolant pour mur et plafond 3M×1.20M': 7500, 'Manette USB UCOM': 2000, "Chargeur SAMSUNG d'origine 45W": 1000, 'Jeux de lumiere bande led Neon 5m RGB': 3500, 'Frondre 200g': 9000, 'Frondre 100g': 4500, 'Microphone de bureau sans fil avec streaming en direct / enregistrement et jeux': 12000, "Lampadaire d'angle multicolore avec telecommande": 4000, 'Projecteur pour photo et video PL48': 13000, 'Projecteur pour photo et video avec deux batteries , telecommande et tripier': 15000, 'Ring light 18" complet': 15000, 'Ventillateur solaire rechargeable avec deux ampoules , plaque solaire et power bank GD8014': 23000, 'Telecommande universel ecran plasma 10pcs': 1000, 'Ventillateur rechargeable solaire avec deux ampoules et plaque solaire': 28000, 'Power bank 50000mah': 10000, 'Ventilateur de cou portable': 2500, 'Jeux de lumiere astronaute bluetooth avec telecommande': 6000, 'Jeux cuilleres/fourchettes et couteaux en or inoxidable 24en1': 9000, 'Range cuierres et louches': 3500, 'Bosse de douche en silicone': 700, 'Hachoir manuel multifonction': 3500, 'Kit de 3 moules à gâteaux en acier inoxydable': 6500, 'Miroir flexible HA-39': 5000, 'Miroir flexible autocollant HA-39': 5000, 'Jeux de 5 plateaux en acier inoxydable': 5000, 'Jeux de lumière de scène 54 Led RGB': 8500, 'Jeux de lumière de scène 36 Led avec télécommande': 5000, 'Projecteur veilleuse rotatif lumière étoile': 3000, "Barbilice professionnel d'origine double lames": 4000, 'Liseur professionnel électrique à vapeur': 15000, "Brosse et lisseur professionnel d'origine électrique": 3500, 'Brosse chauffante et lissante rechargeable': 4000, 'Liseur professionnel SONAR avec affichage numérique': 8000, 'Étagères de douche GM': 9000, 'Étagères pour douche et machine à lavé': 7500, 'Moustiquaire royale 3places': 10000, "Bafle d'origine d'ordinateur": 2500, 'Support téléphone auto rotatif': 2000, 'Horloge murale numérique électrique avec télécommande': 10000, 'Mini compresseur portatif gonfleur pour roue de voiture matelas gonflable moto rechargeable': 8500, 'Trousse de maquillage de voyage avec un miroir Led intelligent': 9000, 'Étagères à œufs pliable pour réfrigérateur': 3500, 'Mélangeur de tasses automatique rechargeable': 3500, 'Étagères de douche 5en1': 6000, 'Matelas gonflable 2 places 300KG': 13000, 'Matelas gonflable 1place 150kg': 8500, 'Fontaine 3 niveaux avec cercle lumineux': 15000, 'Projecteur LED multicolore portable pour photo et video avec telecommande': 11000, 'Range plat': 23000, 'Kit de décoration 110pcs pour gâteau': 8500, 'Miroir flexible autocollant HA-06': 3000, 'Defroisseur RAF R-1313 /800W': 5000, 'Miroir flexible HA27': 5000, 'Hachoir manuel': 3000, 'Porte-couteaux et accroche louche murale': 2500, 'Fontaine 3 niveaux L006': 5000, 'Support murale GM': 4000, 'Trotinette avec melodie': 17000, "Home cinema avec deux enceinte colonne et une caison bass d'origine INNOVA": 55000, 'Machine à crêpes électrique': 7500, 'Gamelle termos électrique': 5000, 'Stimulateur musculaire abdominale EMS': 4500, 'Machine à café 1.8L/1500W': 40000, 'Lime ongles électrique': 5000, "Lime ongles rechargeable d'origine GM": 18500, 'Aerographe portable pour ongles rechargeable numérique sans fil avec compresseur': 12000, 'Mèche de vernis à ongles': 500, 'Jeux de goude 3en1': 3000, 'Caisse pour range meckup': 6000, "Distributeur d'eau de refroidissement par compresseur chaud et froid debout libre": 30000, 'Basin à pédicure pliable': 13000, 'Extracteur de jus rechargeable': 3000, 'Press jus électrique': 10000, 'Poêle à gâteaux 7 trous': 6000, 'Ouvre vin à pompe': 1500, 'Diffuseur de parfum astronaute': 4000, 'Diffuseur de parfum à brume froide': 3500, "Diffuseur de parfum d'ambiance avec des bâtonnets en rotin et des fleures décoratives": 700, 'Diffuseur de parfum avec des bâtonnets en rotin et des fleures décoratives': 900, 'Diffuseur de parfum avec des bâtonnets en rotin et des fleures décoratives New look': 1300, 'Diffuseur de parfum avec des bâtonnets en rotin naturel': 1300, 'Diffuseur de parfum vaisseau spatial': 2000, 'Bafle rechargeable avec micro a fil': 6000, 'Ventillateur portable rechargeable avec veilleuse': 15000, 'Ventillateur plafonier electrique': 12500, 'Ventillateur electrique 16"': 8500, 'Tablette ronde': 10000, 'Gueridon': 6000, 'Classeur rond': 20000, 'Claseur LQ2': 20000, 'Classeur 1#': 13000, 'Tablette carre': 10000, 'Chemine electrique PM': 13000, 'Chemine electrique GM': 40000, 'Classeur A118': 13000, 'Table 2en1 PM': 23000, 'Tablette ronde B5': 10000, 'Congelateur INNOVA IN159 100L': 95000, 'Refrigerateur congelateur MIDEA MDRT 237 / 173L': 140000, 'Refrigerateur congelateur INNOVA IN-241 / 168L': 150000, 'Ecran plasma 43" Led TV': 75000, 'Ecran plasma 32" Led TV': 43000, 'Ecran plasma starX 30"': 35000, 'Congelateur vertical INNOVA IN155 / 100Litres 3 tiroirs': 110000, 'Refrigerateur INNOVA IN-120 / 90L': 80000, 'Ecran plasma Light Wave LW-S6500-T2S2 65 pouces 4K Smart TV': 280000, 'Ecran plasma light wave 43" numerique et smart': 120000, 'Ecran plasma 43" Hisense A4 Smart': 135000, 'Ecran plasma 28" slim LG/SAMSUNG': 34000, 'Ecran plasma 22" slim LG/SAMSUNG': 28000, 'Ecran led STAR X 18"': 22000, 'Ecran plasma HISENSE SMART 55" 55A6Q': 220000, 'Ecran plasma HISENSE SMART 50" 50A4Q': 160000, 'Friteuse electrique sylver crest 12L': 35000, 'Friteuse electrique sylver crest 6L': 25000, 'Bouloire marado 2.5 L': 6000, 'Plaque a gaz star sat vitre automatique deux foyers': 11000, 'Moustiquaire 2m×1.8m': 6000, 'Moustiquaire royale': 10000, 'Home cinema JACK DMX': 19000, 'Plaque a gaz VISION INOX automatique deux foyers': 8500, 'Plaque a gaz VISION VITRE automatique deux foyers': 10000, 'Machine a lave HISENSE 6KG': 155000, 'Machine a lave HISENSE 7 KG': 180000, 'Machine a lave HISENSE semi - automatique 11KG': 140000, 'Machine a lave HISENSE semi - automatique 13.5 KG': 160000, "Bafle rechargeable d'origine": 90000, "Bafle rechargeable d'origine portatif avec deux micro balladeur": 70000, "Bafle bluetooth rechargeable d'origine avec deux micro balladeur": 50000, 'Machine electrique pour gateaux': 10000, 'Table tournante electrique 20cm×3.8cm': 3500, 'Classeur 3 niveaux NEW': 16000, 'Distributeur de pâtes dentifrice automatique avec stérilisateur et range brosse à dents': 2500, 'Table vitre': 25000, 'Bouloire thermos MARADO WDF - 3302 /2L': 6000, 'Table basse effet marbre (modele 418, blanc ou noir)': 45000, "Classeur d'oeufs pliable": 3000, "Distributeur d'eau chaude et froide": 30000, 'Lime ongle rechargeable numerique': 10000, 'Aerographe portable rechargeable avec compresseur (kit complet)': 10000, 'Lime ongle rechargeable GM': 15000, 'Air fryer sylver crest 12L': 35000, 'Machine a gaufre': 8500, 'Brosse de douche en silicone': 500, 'Short avec effet fesse rebondit': 1500, 'Robe gainante avec bretelles': 2000, 'Robe gainante bandeau, sans bretelles': 2000, 'Table rotative pour gâteau': 4000, 'Caisse pour range bijoux et meckup': 5000, 'Jeux de termos 3en1': 13000, 'Jeux de 4 plateaux en acier inoxydable': 6000, 'Fontaine 3 niveaux L011': 5000, "Caisse d'epagne pm": 500, 'Meule rechargeable avec deux batteries': 8000, 'Machine à café et à épices': 3000, 'Congelateur INNOVA IN499 / 350L': 200000, 'Congelateur HISENSE FC-270 / 200L': 140000, 'Refrigerateur avec congelateur INNOVA IN-175 / 175L': 115000, 'Vibro masseur rechargeable numérique 4 tête': 10000, 'Air fresher AB 1001': 1000, 'Detendeur a gaz cartonne': 1000, 'Batterie solaire avec plaque solaire et 3 ampoules GD- 12230': 20000, 'Parfum spray franck': 1000, "Lampe rechargeable electrique d'origine GD - 8010S": 4000, 'Mixeur des fruits rechargeable numerique': 3500, 'Corbeille a fruits et fleures pliable en metal': 1500, 'Perle parfume pour vetements': 1000, 'Air fresher F-800': 1000, 'Fiche adaptateur multiple 882': 500, 'Peinture spray': 1500, 'Detendeur a gaz avec tuyaux': 1500, 'Rallonge 10M M03 USB': 2800, 'Ring light 14" complet': 7000, 'Matelas gonflable 3 places': 15000, 'Lecteur auto MP3': 6000, 'Trotinette 606 avec melodie': 15000, 'Matelas gonflable deux places': 13000, 'Matelas gonflable 1 place': 8500, 'Vello sport': 55000, 'Penderie 610 / 48KG': 14000, 'Viseuse avec deux batteries rechargeable': 14000, 'Lecteur auto 521': 6000, 'Lecteur auto DVD': 17000, 'Decodeur startrack 1 telecommande MPG4': 6000, 'Decodeur digit sat 2telecommandes': 8000, 'Tete KU TOKYOSAT 2001': 1000, 'Penderie 88130': 9000, 'Peigne chauffante': 3000, 'Machine seche verni gel rechargeable S10': 10000, 'Ballance numerique SF-400': 2000, 'Pistolet vibro masseur RF - 321': 5000, 'Accoudoir de voiture multifontionel': 5000, 'Colonne de douche': 5000, 'Range epices rotatif': 7000, 'Lisseur Grious GR -520': 3000, 'Seau avec serpierre pm': 6000, 'Pistolet vibro masseur RF-723X': 3500, 'Seau avec serpierre gm': 7000, 'Pendule murale auto colant': 2500, 'Ampoule LED rechargeable deux batteries a bayonette': 1500, "Rallonge d'origine 15M": 10000, 'Rallonge 360USB /2M': 1500, 'Ampoule LEIZHE LED 12W': 500, 'Ampoule LED LEIZHE 9W': 400, 'Ampoule LED LEIZHE 7W': 300, "Fer a repassé d'origine RAF R - 1234 a eau et a vapeur 2200W": 7000, 'Plaque a gaz FODEG Star inox deux foyers automatique': 8000, 'Ecran plasma 35" smart android SAMSUNG ou LG': 52000, 'Machine a epice et a cafe Hoffmans HM-9081/150g': 15000, 'Comode 6 compartiments': 18000, 'Comode 8 compartiments': 20000, 'Barbilice Grious GR-2607': 3000}


class Command(BaseCommand):
    help = "Remet les prix des produits a leur valeur d'origine (avant tout ajustement en masse)."

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help="N'affiche que ce qui serait change, sans rien ecrire en base.",
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        updated = 0
        unchanged = 0
        matched_slugs = set()
        matched_names = set()

        for slug, price in BY_SLUG.items():
            try:
                product = Product.objects.get(slug=slug)
            except Product.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"[slug introuvable] {slug}"))
                continue
            matched_slugs.add(slug)
            if product.price == price:
                unchanged += 1
                continue
            self.stdout.write(f"{product.name!r}: {product.price} -> {price}")
            if not dry_run:
                product.price = price
                product.save(update_fields=['price'])
            updated += 1

        for name, price in BY_NAME.items():
            try:
                product = Product.objects.get(name=name)
            except Product.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"[nom introuvable] {name}"))
                continue
            except Product.MultipleObjectsReturned:
                self.stdout.write(self.style.ERROR(f"[nom en double, ignore] {name}"))
                continue
            matched_names.add(name)
            if product.price == price:
                unchanged += 1
                continue
            self.stdout.write(f"{product.name!r}: {product.price} -> {price}")
            if not dry_run:
                product.price = price
                product.save(update_fields=['price'])
            updated += 1

        all_products = Product.objects.all()
        untouched = [
            p for p in all_products
            if p.slug not in matched_slugs and p.name not in matched_names
        ]

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f"{'[DRY RUN] ' if dry_run else ''}"
            f"{updated} produit(s) {'a modifier' if dry_run else 'modifie(s)'}, "
            f"{unchanged} deja corrects."
        ))
        if untouched:
            self.stdout.write(self.style.WARNING(
                f"\n{len(untouched)} produit(s) NON couverts par cette reinitialisation "
                f"(nom en double dans la source, ou ajoutes apres les imports) :"
            ))
            for p in untouched:
                self.stdout.write(f"  - {p.name!r} (prix actuel : {p.price})")
