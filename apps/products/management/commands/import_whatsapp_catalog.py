import os

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from apps.products.models import Category, Product, ProductImage

IMAGE_DIR = os.path.join(settings.BASE_DIR, 'import_data', 'whatsapp_catalog')

DEFAULT_STOCK = 20

CATEGORIES = {'electromenager': 'Électroménager',
 'electronique': 'Électronique',
 'beaute-bien-etre': 'Beauté & Bien-être',
 'materiaux-revetements': 'Matériaux & Revêtements',
 'maison-decoration': 'Maison & Décoration'}

PRODUCTS = [{'name': 'Cuisinière à gaz OSCAR 3080B, 5 foyers, 60x76cm',
  'slug': 'cuisiniere-a-gaz-oscar-3080b-5-foyers-60x76cm',
  'category': 'electromenager',
  'description': 'Cuisinière à gaz OSCAR modèle 3080B, 5 foyers, dimensions 60x76cm.',
  'price': 135000,
  'images': ['cuisiniere-a-gaz-oscar-3080b-5-foyers-60x76cm-1.jpeg']},
 {'name': 'Cuisinière à gaz OSCAR G85NE Luxe, 5 foyers avec porte gaz, 60x76cm',
  'slug': 'cuisiniere-a-gaz-oscar-g85ne-luxe-5-foyers-avec-po',
  'category': 'electromenager',
  'description': 'Cuisinière à gaz OSCAR modèle G85NE, 5 foyers, avec porte du four vitrée, '
                 'dimensions 60x76cm.',
  'price': 170000,
  'images': ['cuisiniere-a-gaz-oscar-g85ne-luxe-5-foyers-avec-porte-gaz-60x76cm-1.jpeg']},
 {'name': 'Cuisinière à gaz OSCAR 60B, 4 foyers, 60x60cm',
  'slug': 'cuisiniere-a-gaz-oscar-60b-4-foyers-60x60cm',
  'category': 'electromenager',
  'description': 'Cuisinière à gaz OSCAR modèle 60B, 4 foyers, dimensions 60x60cm.',
  'price': 105000,
  'images': ['cuisiniere-a-gaz-oscar-60b-4-foyers-60x60cm-1.jpeg']},
 {'name': 'Réfrigérateur vitrine OSCAR V250, 170L',
  'slug': 'refrigerateur-vitrine-oscar-v250-170l',
  'category': 'electromenager',
  'description': 'Réfrigérateur vitrine OSCAR modèle OSC-V250, capacité 170 litres.',
  'price': 190000,
  'images': ['refrigerateur-vitrine-oscar-v250-170l-1.jpeg']},
 {'name': 'Réfrigérateur OSCAR R165S, 138L',
  'slug': 'refrigerateur-oscar-r165s-138l',
  'category': 'electromenager',
  'description': 'Réfrigérateur avec compartiment congélateur OSCAR modèle OSC-R165S, capacité 138 '
                 'litres.',
  'price': 120000,
  'images': ['refrigerateur-oscar-r165s-138l-1.jpeg']},
 {'name': "Réfrigérateur OSCAR M280D, 227L, distributeur d'eau",
  'slug': 'refrigerateur-oscar-m280d-227l-distributeur-deau',
  'category': 'electromenager',
  'description': 'Réfrigérateur OSCAR modèle OSC-M280D, capacité 227 litres, avec distributeur '
                 "d'eau intégré.",
  'price': 165000,
  'images': ['refrigerateur-oscar-m280d-227l-distributeur-d-eau-1.jpeg']},
 {'name': 'Congélateur HISENSE FC-490, 315L',
  'slug': 'congelateur-hisense-fc-490-315l',
  'category': 'electromenager',
  'description': 'Congélateur coffre HISENSE modèle FC-490, capacité 315 litres.',
  'price': 215000,
  'images': ['congelateur-hisense-fc-490-315l-1.jpeg']},
 {'name': 'Réfrigérateur HISENSE RD34, 262L double porte',
  'slug': 'refrigerateur-hisense-rd34-262l-double-porte',
  'category': 'electromenager',
  'description': 'Réfrigérateur double porte HISENSE modèle RD34, capacité 262 litres.',
  'price': 250000,
  'images': ['refrigerateur-hisense-rd34-262l-double-porte-1.jpeg']},
 {'name': 'Réfrigérateur MIDEA MDRT237, 173L double porte',
  'slug': 'refrigerateur-midea-mdrt237-173l-double-porte',
  'category': 'electromenager',
  'description': 'Réfrigérateur double porte MIDEA modèle MDRT237, capacité 173 litres.',
  'price': 140000,
  'images': ['refrigerateur-midea-mdrt237-173l-double-porte-1.jpeg']},
 {'name': 'Four électrique OSCAR 4502, 45L, 1800W',
  'slug': 'four-electrique-oscar-4502-45l-1800w',
  'category': 'electromenager',
  'description': 'Four électrique OSCAR modèle OSC-4502, capacité 45 litres, 1800W.',
  'price': 55000,
  'images': ['four-electrique-oscar-4502-45l-1800w-1.jpeg']},
 {'name': 'Friteuse à air TOBI TB-978, 16L, 2400W',
  'slug': 'friteuse-a-air-tobi-tb-978-16l-2400w',
  'category': 'electromenager',
  'description': 'Friteuse à air chaud sans huile TOBI modèle TB-978, capacité 16 litres, 2400W.',
  'price': 35000,
  'images': ['friteuse-a-air-tobi-tb-978-16l-2400w-1.jpeg',
             'friteuse-a-air-tobi-tb-978-16l-2400w-2.jpeg',
             'friteuse-a-air-tobi-tb-978-16l-2400w-3.jpeg']},
 {'name': 'Friteuse à air TOBI TB-969, 15L, double panier, écran tactile',
  'slug': 'friteuse-a-air-tobi-tb-969-15l-double-panier-ecran',
  'category': 'electromenager',
  'description': 'Friteuse à air chaud sans huile TOBI modèle TB-969, double panier (2 tiroirs), '
                 'écran tactile couleur numérique, capacité 15 litres.',
  'price': 50000,
  'images': ['friteuse-a-air-tobi-tb-969-15l-double-panier-ecran-tactile-1.jpeg',
             'friteuse-a-air-tobi-tb-969-15l-double-panier-ecran-tactile-2.jpeg',
             'friteuse-a-air-tobi-tb-969-15l-double-panier-ecran-tactile-3.jpeg']},
 {'name': 'Machine à laver HISENSE Twin Tub, 13,5kg',
  'slug': 'machine-a-laver-hisense-twin-tub-135kg',
  'category': 'electromenager',
  'description': 'Machine à laver semi-automatique HISENSE, double cuve (Twin Tub), capacité '
                 '13,5kg.',
  'price': 160000,
  'images': ['machine-a-laver-hisense-twin-tub-13-5kg-1.jpeg']},
 {'name': 'Hachoir/mixeur électrique 2-en-1, 4L',
  'slug': 'hachoirmixeur-electrique-2-en-1-4l',
  'category': 'electromenager',
  'description': 'Hachoir et mixeur électrique 2-en-1, capacité 4L, idéal pour fruits, légumes et '
                 'ail.',
  'price': 19000,
  'images': ['hachoir-mixeur-electrique-2-en-1-4l-1.jpeg',
             'hachoir-mixeur-electrique-2-en-1-4l-2.jpeg']},
 {'name': 'Set ustensiles de cuisine rose (louches + couteaux silicone)',
  'slug': 'set-ustensiles-de-cuisine-rose-louches-couteaux-si',
  'category': 'electromenager',
  'description': 'Ensemble de louches et couteaux de cuisine en silicone, coloris rose.',
  'price': 9000,
  'images': ['set-ustensiles-de-cuisine-rose-louches-couteaux-silicone-1.jpeg',
             'set-ustensiles-de-cuisine-rose-louches-couteaux-silicone-2.jpeg']},
 {'name': 'Machine à coudre Handy Stitch électrique, avec pédale',
  'slug': 'machine-a-coudre-handy-stitch-electrique-avec-peda',
  'category': 'electromenager',
  'description': 'Machine à coudre portable Handy Stitch, fonctionnement électrique et à piles, '
                 'livrée avec pédale et adaptateur secteur.',
  'price': 5000,
  'images': ['machine-a-coudre-handy-stitch-electrique-avec-pedale-1.jpeg']},
 {'name': 'Machine à coudre mini portable, manuelle à piles',
  'slug': 'machine-a-coudre-mini-portable-manuelle-a-piles',
  'category': 'electromenager',
  'description': 'Mini machine à coudre portable, fonctionnement manuel à piles, sans pédale.',
  'price': 2000,
  'images': ['machine-a-coudre-mini-portable-manuelle-a-piles-1.jpeg',
             'machine-a-coudre-mini-portable-manuelle-a-piles-2.jpeg']},
 {'name': 'Enceinte multimédia OSCAR 2028T (home cinéma)',
  'slug': 'enceinte-multimedia-oscar-2028t-home-cinema',
  'category': 'electronique',
  'description': 'Système home cinéma / enceinte multimédia OSCAR modèle OSC-2028T.',
  'price': 65000,
  'images': ['enceinte-multimedia-oscar-2028t-home-cinema-1.jpeg']},
 {'name': 'Barre de son OSCAR 1515B',
  'slug': 'barre-de-son-oscar-1515b',
  'category': 'electronique',
  'description': 'Barre de son / enceinte tower OSCAR modèle OSC-1515B.',
  'price': 45000,
  'images': ['barre-de-son-oscar-1515b-1.jpeg']},
 {'name': 'Barre de son HISENSE AX-3100, 500W',
  'slug': 'barre-de-son-hisense-ax-3100-500w',
  'category': 'electronique',
  'description': 'Barre de son HISENSE modèle AX-3100, puissance 500W.',
  'price': 85000,
  'images': ['barre-de-son-hisense-ax-3100-500w-1.jpeg',
             'barre-de-son-hisense-ax-3100-500w-2.jpeg']},
 {'name': 'Microphone sans fil universel',
  'slug': 'microphone-sans-fil-universel',
  'category': 'electronique',
  'description': 'Microphone sans fil universel, clip pour smartphone/appareil photo.',
  'price': 2500,
  'images': ['microphone-sans-fil-universel-1.jpeg']},
 {'name': 'Microphone sans fil F11-2-3N1',
  'slug': 'microphone-sans-fil-f11-2-3n1',
  'category': 'electronique',
  'description': 'Microphone sans fil modèle F11-2-3N1.',
  'price': 3500,
  'images': ['microphone-sans-fil-f11-2-3n1-1.jpeg']},
 {'name': 'Écouteurs sans fil K54 TWS',
  'slug': 'ecouteurs-sans-fil-k54-tws',
  'category': 'electronique',
  'description': 'Écouteurs sans fil Bluetooth TWS modèle K54.',
  'price': 2000,
  'images': ['ecouteurs-sans-fil-k54-tws-1.jpeg']},
 {'name': 'Régulateur de tension FODEG Star DVR-1000VA, 1000W',
  'slug': 'regulateur-de-tension-fodeg-star-dvr-1000va-1000w',
  'category': 'electronique',
  'description': 'Régulateur/stabilisateur de tension FODEG Star modèle DVR-1000VA, 1000W.',
  'price': 14000,
  'images': ['regulateur-de-tension-fodeg-star-dvr-1000va-1000w-1.jpeg']},
 {'name': "Compresseur d'air / booster de voiture 4-en-1 rechargeable",
  'slug': 'compresseur-dair-booster-de-voiture-4-en-1-recharg',
  'category': 'electronique',
  'description': "Compresseur d'air portable multifonctionnel rechargeable : démarreur de voiture, "
                 'gonfleur, powerbank et lampe, 4-en-1.',
  'price': 20000,
  'images': ['compresseur-d-air-booster-de-voiture-4-en-1-rechargeable-1.jpeg',
             'compresseur-d-air-booster-de-voiture-4-en-1-rechargeable-2.jpeg',
             'compresseur-d-air-booster-de-voiture-4-en-1-rechargeable-3.jpeg',
             'compresseur-d-air-booster-de-voiture-4-en-1-rechargeable-4.jpeg']},
 {'name': 'Kit éclairage LED photo/vidéo Pro LED-600, sur trépied',
  'slug': 'kit-eclairage-led-photovideo-pro-led-600-sur-trepi',
  'category': 'electronique',
  'description': "Kit d'éclairage LED complet pour photo et vidéo, modèle Pro LED-600, avec "
                 'trépied.',
  'price': 15000,
  'images': ['kit-eclairage-led-photo-video-pro-led-600-sur-trepied-1.jpeg',
             'kit-eclairage-led-photo-video-pro-led-600-sur-trepied-2.jpeg']},
 {'name': 'Kit éclairage LED GIFTMAX U800 RGB',
  'slug': 'kit-eclairage-led-giftmax-u800-rgb',
  'category': 'electronique',
  'description': "Kit d'éclairage LED RGB complet pour photo et vidéo, modèle GIFTMAX U800.",
  'price': 20000,
  'images': ['kit-eclairage-led-giftmax-u800-rgb-1.jpeg',
             'kit-eclairage-led-giftmax-u800-rgb-2.jpeg']},
 {'name': 'Lampe LED photo RMG PL-48',
  'slug': 'lampe-led-photo-rmg-pl-48',
  'category': 'electronique',
  'description': 'Lampe LED photo/vidéo complète RMG modèle PL-48.',
  'price': 12000,
  'images': ['lampe-led-photo-rmg-pl-48-1.jpeg']},
 {'name': 'Combo montre connectée + casque + écouteurs OKPU ROCK-450',
  'slug': 'combo-montre-connectee-casque-ecouteurs-okpu-rock',
  'category': 'electronique',
  'description': 'Ensemble montre connectée, casque sans fil et écouteurs type AirPods, marque '
                 'OKPU modèle ROCK-450.',
  'price': 6500,
  'images': ['combo-montre-connectee-casque-ecouteurs-okpu-rock-450-1.jpeg',
             'combo-montre-connectee-casque-ecouteurs-okpu-rock-450-2.jpeg']},
 {'name': 'Télécommande TV LG plasma/smart',
  'slug': 'telecommande-tv-lg-plasmasmart',
  'category': 'electronique',
  'description': 'Télécommande de remplacement pour téléviseurs LG plasma et smart TV.',
  'price': 500,
  'images': ['telecommande-tv-lg-plasma-smart-1.jpeg']},
 {'name': 'Télécommande TV STAR-X écran plasma',
  'slug': 'telecommande-tv-star-x-ecran-plasma',
  'category': 'electronique',
  'description': 'Télécommande de remplacement pour téléviseurs STAR-X écran plasma.',
  'price': 1000,
  'images': ['telecommande-tv-star-x-ecran-plasma-1.jpeg']},
 {'name': 'Télécommande décodeur STAR TRACK, universel MPG4',
  'slug': 'telecommande-decodeur-star-track-universel-mpg4',
  'category': 'electronique',
  'description': 'Télécommande universelle pour décodeur STAR TRACK, format MPG4.',
  'price': 500,
  'images': ['telecommande-decodeur-star-track-universel-mpg4-1.jpeg']},
 {'name': 'Télécommande décodeur STARX HD10',
  'slug': 'telecommande-decodeur-starx-hd10',
  'category': 'electronique',
  'description': 'Télécommande pour décodeur STARX modèle HD10.',
  'price': 500,
  'images': ['telecommande-decodeur-starx-hd10-1.jpeg']},
 {'name': 'Télécommande TV Philips RC7940',
  'slug': 'telecommande-tv-philips-rc7940',
  'category': 'electronique',
  'description': 'Télécommande de remplacement pour téléviseurs Philips et Plasma, modèle RC7940.',
  'price': 500,
  'images': ['telecommande-tv-philips-rc7940-1.jpeg']},
 {'name': 'Télécommande décodeur universel SuperMax 9200 Smart',
  'slug': 'telecommande-decodeur-universel-supermax-9200-smar',
  'category': 'electronique',
  'description': 'Télécommande universelle pour décodeur, modèle SuperMax 9200 Smart.',
  'price': 500,
  'images': ['telecommande-decodeur-universel-supermax-9200-smart-1.jpeg']},
 {'name': 'Télécommande décodeur DigiSat',
  'slug': 'telecommande-decodeur-digisat',
  'category': 'electronique',
  'description': 'Télécommande pour décodeur DigiSat.',
  'price': 500,
  'images': ['telecommande-decodeur-digisat-1.jpeg']},
 {'name': 'Télécommande décodeur Samtel, universel MPG4',
  'slug': 'telecommande-decodeur-samtel-universel-mpg4',
  'category': 'electronique',
  'description': 'Télécommande universelle pour décodeur Samtel, format MPG4.',
  'price': 500,
  'images': ['telecommande-decodeur-samtel-universel-mpg4-1.jpeg']},
 {'name': 'Télécommande décodeur Powerpass PP-4020 HD',
  'slug': 'telecommande-decodeur-powerpass-pp-4020-hd',
  'category': 'electronique',
  'description': 'Télécommande pour décodeur Powerpass modèle PP-4020, format MPG4.',
  'price': 500,
  'images': ['telecommande-decodeur-powerpass-pp-4020-hd-1.jpeg']},
 {'name': 'Télécommande Light Wave, écran plasma',
  'slug': 'telecommande-light-wave-ecran-plasma',
  'category': 'electronique',
  'description': 'Télécommande de remplacement pour téléviseurs écran plasma, marque Light Wave.',
  'price': 1000,
  'images': ['telecommande-light-wave-ecran-plasma-1.jpeg']},
 {'name': 'Télécommande Vestel 2440, TV/Plasma universel',
  'slug': 'telecommande-vestel-2440-tvplasma-universel',
  'category': 'electronique',
  'description': 'Télécommande universelle pour téléviseurs Vestel et Plasma, modèle 2440.',
  'price': 500,
  'images': ['telecommande-vestel-2440-tv-plasma-universel-1.jpeg']},
 {'name': 'Bouteille thermos inox 500ml, écran de température',
  'slug': 'bouteille-thermos-inox-500ml-ecran-de-temperature',
  'category': 'electronique',
  'description': 'Bouteille thermos en inox, capacité 500ml, avec écran digital indiquant la '
                 'température.',
  'price': 1500,
  'images': ['bouteille-thermos-inox-500ml-ecran-de-temperature-1.jpeg',
             'bouteille-thermos-inox-500ml-ecran-de-temperature-2.jpeg']},
 {'name': 'Pistolet de massage J1',
  'slug': 'pistolet-de-massage-j1',
  'category': 'beaute-bien-etre',
  'description': 'Pistolet de massage percussion, modèle J1.',
  'price': 3500,
  'images': ['pistolet-de-massage-j1-1.jpeg', 'pistolet-de-massage-j1-2.jpeg']},
 {'name': 'Pistolet de massage RF-723X',
  'slug': 'pistolet-de-massage-rf-723x',
  'category': 'beaute-bien-etre',
  'description': 'Pistolet de massage percussion, modèle RF-723X.',
  'price': 3500,
  'images': ['pistolet-de-massage-rf-723x-1.jpeg', 'pistolet-de-massage-rf-723x-2.jpeg']},
 {'name': 'Pistolet de massage Fascial Gun RF-321',
  'slug': 'pistolet-de-massage-fascial-gun-rf-321',
  'category': 'beaute-bien-etre',
  'description': 'Pistolet de massage percussion Fascial Gun, modèle RF-321.',
  'price': 5000,
  'images': ['pistolet-de-massage-fascial-gun-rf-321-1.jpeg']},
 {'name': 'Appareil de massage multi-zones (dos, cou, bras, cuisses, mollets, pieds)',
  'slug': 'appareil-de-massage-multi-zones-dos-cou-bras-cuiss',
  'category': 'beaute-bien-etre',
  'description': 'Appareil de massage portable avec ventouses vibrantes, pour dos, cou/épaules, '
                 'bras, cuisses, mollets et plante des pieds.',
  'price': 12000,
  'images': ['appareil-de-massage-multi-zones-dos-cou-bras-cuisses-mollets-pieds-1.jpeg']},
 {'name': 'Tondeuse cheveux sans fil rechargeable',
  'slug': 'tondeuse-cheveux-sans-fil-rechargeable',
  'category': 'beaute-bien-etre',
  'description': 'Tondeuse à cheveux sans fil rechargeable, avec écran digital.',
  'price': 4000,
  'images': ['tondeuse-cheveux-sans-fil-rechargeable-1.jpeg',
             'tondeuse-cheveux-sans-fil-rechargeable-2.jpeg']},
 {'name': 'Lampe UV séchage ongles Sun WY-06',
  'slug': 'lampe-uv-sechage-ongles-sun-wy-06',
  'category': 'beaute-bien-etre',
  'description': 'Lampe UV pour séchage de vernis semi-permanent, modèle Sun WY-06.',
  'price': 5000,
  'images': ['lampe-uv-sechage-ongles-sun-wy-06-1.jpeg',
             'lampe-uv-sechage-ongles-sun-wy-06-2.jpeg']},
 {'name': 'Lampe UV séchage ongles Sun S10 Professional',
  'slug': 'lampe-uv-sechage-ongles-sun-s10-professional',
  'category': 'beaute-bien-etre',
  'description': 'Lampe UV professionnelle pour séchage de vernis semi-permanent, modèle Sun S10.',
  'price': 10000,
  'images': ['lampe-uv-sechage-ongles-sun-s10-professional-1.jpeg',
             'lampe-uv-sechage-ongles-sun-s10-professional-2.jpeg']},
 {'name': 'Lampe UV séchage ongles Doragym Cordless (rechargeable)',
  'slug': 'lampe-uv-sechage-ongles-doragym-cordless-rechargea',
  'category': 'beaute-bien-etre',
  'description': 'Lampe UV rechargeable sans fil pour séchage de vernis semi-permanent, modèle '
                 'Doragym Cordless.',
  'price': 10000,
  'images': ['lampe-uv-sechage-ongles-doragym-cordless-rechargeable-1.jpeg',
             'lampe-uv-sechage-ongles-doragym-cordless-rechargeable-2.jpeg',
             'lampe-uv-sechage-ongles-doragym-cordless-rechargeable-3.jpeg']},
 {'name': 'Coffret huiles essentielles Fragrant Garden (6x10ml)',
  'slug': 'coffret-huiles-essentielles-fragrant-garden-6x10ml',
  'category': 'beaute-bien-etre',
  'description': 'Coffret de 6 huiles essentielles parfumées Fragrant Garden, flacons de 10ml.',
  'price': 1800,
  'images': ['coffret-huiles-essentielles-fragrant-garden-6x10ml-1.jpeg']},
 {'name': 'Dalle PVC autocollante sol, marbre noir, 60x60cm',
  'slug': 'dalle-pvc-autocollante-sol-marbre-noir-60x60cm',
  'category': 'materiaux-revetements',
  'description': 'Dalle de sol PVC autocollante effet marbre noir, format 60x60cm.',
  'price': 1300,
  'images': ['dalle-pvc-autocollante-sol-marbre-noir-60x60cm-1.jpeg']},
 {'name': 'Dalle PVC autocollante SPC88032, marbre blanc/or, 60x60cm',
  'slug': 'dalle-pvc-autocollante-spc88032-marbre-blancor-60x',
  'category': 'materiaux-revetements',
  'description': 'Dalle de sol PVC autocollante SPC88032, effet marbre blanc et or, format '
                 '60x60cm.',
  'price': 1300,
  'images': ['dalle-pvc-autocollante-spc88032-marbre-blanc-or-60x60cm-1.jpeg']},
 {'name': 'Dalle PVC autocollante LVT88010, marbre blanc, 60x60cm',
  'slug': 'dalle-pvc-autocollante-lvt88010-marbre-blanc-60x60',
  'category': 'materiaux-revetements',
  'description': 'Dalle de sol PVC autocollante LVT88010, effet marbre blanc, format 60x60cm '
                 '(également disponible en 30x30 / 40x40 / 30x60).',
  'price': 1300,
  'images': ['dalle-pvc-autocollante-lvt88010-marbre-blanc-60x60cm-1.jpeg']},
 {'name': 'Tapis chaîne dorée, fond marron',
  'slug': 'tapis-chaine-doree-fond-marron',
  'category': 'materiaux-revetements',
  'description': 'Tapis motif chaîne dorée sur fond marron, 2.30m x 1.60m.',
  'price': 13000,
  'images': ['tapis-chaine-doree-fond-marron-1.jpeg']},
 {'name': 'Tapis Versace médaillon, noir/or',
  'slug': 'tapis-versace-medaillon-noiror',
  'category': 'materiaux-revetements',
  'description': 'Tapis motif médaillon Versace, noir et or, 2.30m x 1.60m.',
  'price': 13000,
  'images': ['tapis-versace-medaillon-noir-or-1.jpeg']},
 {'name': 'Tapis Louis Vuitton, bleu/bulles',
  'slug': 'tapis-louis-vuitton-bleubulles',
  'category': 'materiaux-revetements',
  'description': 'Tapis motif Louis Vuitton bleu à bulles, 2.30m x 1.60m.',
  'price': 13000,
  'images': ['tapis-louis-vuitton-bleu-bulles-1.jpeg']},
 {'name': 'Tapis Louis Vuitton, monogramme',
  'slug': 'tapis-louis-vuitton-monogramme',
  'category': 'materiaux-revetements',
  'description': 'Tapis motif monogramme Louis Vuitton, 2.30m x 1.60m.',
  'price': 13000,
  'images': ['tapis-louis-vuitton-monogramme-1.jpeg']},
 {'name': 'Tapis roses dorées, fond noir',
  'slug': 'tapis-roses-dorees-fond-noir',
  'category': 'materiaux-revetements',
  'description': 'Tapis motif roses dorées sur fond noir, 2.30m x 1.60m.',
  'price': 13000,
  'images': ['tapis-roses-dorees-fond-noir-1.jpeg']},
 {'name': 'Tapis poissons koï dorés',
  'slug': 'tapis-poissons-koi-dores',
  'category': 'materiaux-revetements',
  'description': 'Tapis motif poissons koï dorés, 2.30m x 1.60m.',
  'price': 13000,
  'images': ['tapis-poissons-ko-dores-1.jpeg']},
 {'name': 'Tapis rouge/blanc/or, motif cercles',
  'slug': 'tapis-rougeblancor-motif-cercles',
  'category': 'materiaux-revetements',
  'description': 'Tapis motif cercles rouge, blanc et or, 2.30m x 1.60m.',
  'price': 13000,
  'images': ['tapis-rouge-blanc-or-motif-cercles-1.jpeg']},
 {'name': 'Tapis noir/gris/jaune, tourbillon',
  'slug': 'tapis-noirgrisjaune-tourbillon',
  'category': 'materiaux-revetements',
  'description': 'Tapis motif tourbillon noir, gris et jaune, 2.30m x 1.60m.',
  'price': 13000,
  'images': ['tapis-noir-gris-jaune-tourbillon-1.jpeg']},
 {'name': 'Tapis Versace damier, or/noir',
  'slug': 'tapis-versace-damier-ornoir',
  'category': 'materiaux-revetements',
  'description': 'Tapis motif damier Versace, or et noir, 2.30m x 1.60m.',
  'price': 13000,
  'images': ['tapis-versace-damier-or-noir-1.jpeg']},
 {'name': 'Tapis plume dorée/noire, abstrait',
  'slug': 'tapis-plume-doreenoire-abstrait',
  'category': 'materiaux-revetements',
  'description': 'Tapis motif plume abstrait doré et noir, 2.30m x 1.60m.',
  'price': 13000,
  'images': ['tapis-plume-doree-noire-abstrait-1.jpeg']},
 {'name': 'Tapis tourbillon bleu/rouge/blanc',
  'slug': 'tapis-tourbillon-bleurougeblanc',
  'category': 'materiaux-revetements',
  'description': 'Tapis motif tourbillon bleu, rouge et blanc, 2.30m x 1.60m.',
  'price': 13000,
  'images': ['tapis-tourbillon-bleu-rouge-blanc-1.jpeg']},
 {'name': 'Tapis Versace zèbre, noir/blanc',
  'slug': 'tapis-versace-zebre-noirblanc',
  'category': 'materiaux-revetements',
  'description': 'Tapis motif zèbre Versace, noir et blanc, 2.30m x 1.60m.',
  'price': 13000,
  'images': ['tapis-versace-zebre-noir-blanc-1.jpeg']},
 {'name': 'Matelas gonflable deux places',
  'slug': 'matelas-gonflable-deux-places',
  'category': 'maison-decoration',
  'description': 'Matelas gonflable deux places, idéal pour invités ou camping.',
  'price': 12000,
  'images': ['matelas-gonflable-deux-places-1.jpeg']},
 {'name': 'Fauteuil gonflable + pouf assorti',
  'slug': 'fauteuil-gonflable-pouf-assorti',
  'category': 'maison-decoration',
  'description': 'Fauteuil gonflable avec repose-pieds/pouf assorti, plusieurs coloris '
                 'disponibles.',
  'price': 8500,
  'images': ['fauteuil-gonflable-pouf-assorti-1.jpeg', 'fauteuil-gonflable-pouf-assorti-2.jpeg']},
 {'name': 'Diffuseur d\'arôme à flamme "Aroma"',
  'slug': 'diffuseur-darome-a-flamme-aroma',
  'category': 'maison-decoration',
  'description': 'Diffuseur de parfum à flamme décorative, modèle Aroma.',
  'price': 5000,
  'images': ['diffuseur-d-arome-a-flamme-aroma-1.jpeg',
             'diffuseur-d-arome-a-flamme-aroma-2.jpeg',
             'diffuseur-d-arome-a-flamme-aroma-3.jpeg']},
 {'name': 'Diffuseur/humidificateur "Sportiness" à 6 pompes',
  'slug': 'diffuseurhumidificateur-sportiness-a-6-pompes',
  'category': 'maison-decoration',
  'description': 'Diffuseur de parfum / humidificateur à 6 pompes, modèle Sportiness, multicolore.',
  'price': 5000,
  'images': ['diffuseur-humidificateur-sportiness-a-6-pompes-1.jpeg']},
 {'name': 'Éplucheur rechargeable pour fruits et légumes',
  'slug': 'eplucheur-rechargeable-pour-fruits-et-legumes',
  'category': 'maison-decoration',
  'description': 'Éplucheur électrique rechargeable pour fruits et légumes.',
  'price': 5000,
  'images': []}]


class Command(BaseCommand):
    help = (
        "Importe le catalogue reel de produits recu via WhatsApp (TTR BAZAR SARL, "
        "5-6 juillet 2026) : cree les categories, les produits avec prix reels, "
        "et leur galerie de photos depuis import_data/whatsapp_catalog/."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help="Affiche ce qui serait fait sans ecrire en base",
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        categories = {}
        for slug, name in CATEGORIES.items():
            if dry_run:
                self.stdout.write(f"[dry-run] Categorie: {name} ({slug})")
                continue
            category, created = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'is_active': True},
            )
            categories[slug] = category
            tag = 'creee' if created else 'existante'
            self.stdout.write(self.style.SUCCESS(f"Categorie {tag}: {category.name}"))

        created_count = 0
        updated_count = 0
        missing_images = []

        for entry in PRODUCTS:
            slug = entry['slug']

            if dry_run:
                self.stdout.write(
                    f"[dry-run] Produit: {entry['name']} — {entry['price']} FCFA "
                    f"— {len(entry['images'])} image(s)"
                )
                continue

            category = categories[entry['category']]
            product, created = Product.objects.update_or_create(
                slug=slug,
                defaults=dict(
                    name=entry['name'],
                    description=entry['description'],
                    category=category,
                    price=entry['price'],
                    stock=DEFAULT_STOCK,
                    is_available=True,
                ),
            )
            created_count += 1 if created else 0
            updated_count += 0 if created else 1

            # Rebuild the gallery from scratch to keep the command idempotent on re-run.
            product.images.all().delete()

            for order, filename in enumerate(entry['images']):
                image_path = os.path.join(IMAGE_DIR, filename)
                if not os.path.isfile(image_path):
                    missing_images.append((entry['name'], filename))
                    continue

                with open(image_path, 'rb') as fh:
                    django_file = File(fh, name=filename)
                    if order == 0:
                        product.image.save(filename, django_file, save=True)
                        fh.seek(0)
                        ProductImage.objects.create(
                            product=product, image=File(fh, name=filename), order=0,
                        )
                    else:
                        ProductImage.objects.create(
                            product=product, image=django_file, order=order,
                        )

            tag = 'cree' if created else 'mis a jour'
            self.stdout.write(f"Produit {tag}: {product.name} ({entry['price']} FCFA)")

        if dry_run:
            self.stdout.write(self.style.WARNING(
                f"\n[dry-run] {len(PRODUCTS)} produit(s) seraient traites — aucune ecriture en base."
            ))
            return

        self.stdout.write(self.style.SUCCESS(
            f"\nTermine : {created_count} produit(s) cree(s), {updated_count} mis a jour."
        ))
        if missing_images:
            self.stdout.write(self.style.WARNING(
                f"{len(missing_images)} image(s) introuvable(s) (produit cree sans cette photo) :"
            ))
            for name, filename in missing_images:
                self.stdout.write(f"  - {name}: {filename}")
