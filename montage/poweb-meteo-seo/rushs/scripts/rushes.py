"""Extraits retenus du webinaire « La météo du SEO » (mars 2025, Camille Dufossez et Delphine).
Temps en secondes, relatifs au début de la plage caméras (seg A ou B) ; SEG_OFFSET donne le début dans la vidéo source."""

SEG_OFFSET = {"A": 1318.0, "B": 2862.0}

RUSHES = {
    "01-intention": {
        "seg": "A", "ranges": [(63.9, 116.0)], "first": "camille",
        "titre": "Page de vente ou article de blog",
        "question": ["Page de vente", "ou article de blog ?"],
        "fix": {"blocs": "blog", "rangent": "rankent", "mots-clé": "mot-clé", "lesquelles": "lesquels"},
    },
    "02-magasin": {
        "seg": "A", "ranges": [(121.7, 167.9)], "first": "camille",
        "titre": "Le vendeur qui vous saute dessus",
        "question": ["Pourquoi vos visiteurs", "repartent aussitôt ?"],
        "fix": {"je n'ai pas de": "de", "proposition.": "position.", "l'arborécence": "l'arborescence"},
    },
    "03-faq": {
        "seg": "A", "ranges": [(209.9, 227.3), (232.95, 250.0)], "first": "delphine",
        "titre": "À quoi sert une FAQ",
        "question": ["À quoi sert une FAQ", "en SEO ?"],
        "fix": {"une donnée structurée.": "des données structurées.", "un de résultat": "un, deux résultats"},
    },
    "04-hack-top10": {
        "seg": "A", "ranges": [(265.9, 274.0), (291.9, 333.7)], "first": "camille",
        "titre": "Le hack de la FAQ",
        "question": ["Pas dans le top 10 ?", "Il reste une place."],
        "fix": {"C'est-à-dire, sur la FAQ,": "Moi, ce que j'aime bien dire sur la FAQ,", "Je sais que vous": "Vous", "ranquer": "ranker"},
    },
    "05-objections": {
        "seg": "A", "ranges": [(347.9, 354.0), (357.9, 383.7)], "first": "delphine",
        "titre": "Quoi mettre dans votre FAQ",
        "question": ["Quoi mettre", "dans votre FAQ ?"],
        "fix": {"meilleurs": "meilleures", "serre": "sers", "pour avoir l'utilisateur,": "de l'utilisateur,", "pour avoir ton client": "de ton client", "ça ?": "ça."},
    },
    "06-ia-outil": {
        "seg": "B", "ranges": [(57.0, 90.5)], "first": "delphine", "speakers": [(0.0, "delphine")],
        "titre": "L'IA va-t-elle remplacer le SEO",
        "question": ["L'IA va remplacer", "le SEO ?"],
    },
    "07-chatgpt": {
        "seg": "B", "ranges": [(95.7, 122.3)], "first": "delphine", "speakers": [(0.0, "delphine"), (2.2, "camille")],
        "titre": "Apparaître dans ChatGPT",
        "question": ["Comment apparaître", "dans ChatGPT ?"],
        "fix": {"j'ai pété": "ChatGPT", "Chartier PT,": "ChatGPT,", "il y a des moteurs": "IA des moteurs"},
    },
    "08-niche": {
        "seg": "B", "ranges": [(129.9, 173.9)], "first": "camille", "speakers": [(0.0, "camille")],
        "titre": "Pas besoin d'être un gros site",
        "question": ["Petit site cité", "par ChatGPT ?"],
        "fix": {"ranquer": "ranker", "d'un tiers de GPT.": "dans ChatGPT."},
    },
    "09-sea-seo": {
        "seg": "B", "ranges": [(321.3, 371.5)], "first": "camille",
        "titre": "SEA ou SEO",
        "question": ["Payer Google", "ou attendre 6 mois ?"],
        "fix": {"S.I.A.": "SEA.", "ranquer,": "ranker,", "processus sur du long terme. C'est intéressant": "processus. Sur du long terme, c'est intéressant", "d'en cher.": "d'enchères.", "mots-clé": "mot-clé", "ranquer": "ranker", "va faire créer": "il faut créer", "lits": "leads"},
    },
    "10-cpc": {
        "seg": "B", "ranges": [(371.65, 423.4)], "first": "camille",
        "titre": "Le SEO fait baisser vos pubs",
        "question": ["Le SEO fait baisser", "le prix de vos pubs"],
        "fix": {"coups par clics en SEO.": "coûts par clic en SEA.", "au clic en SEO.": "au clic en SEA.", "manquer sur faire des crêpes.": "ranker sur « faire des crêpes ».", "à beaucoup": "a beaucoup"},
    },
    "11-position-zero": {
        "seg": "B", "ranges": [(440.05, 482.5)], "first": "camille",
        "titre": "La position 0",
        "question": ["Passer devant", "les pubs Google ?"],
        "fix": {"passe à passe,": "ça passe"},
    },
    "12-cannibalisation": {
        "seg": "B", "ranges": [(520.0, 522.3), (526.25, 550.3)], "first": "camille", "speakers": [(0.0, "camille")],
        "titre": "La cannibalisation",
        "question": ["Deux pages", "sur le même mot-clé ?"],
        "fix": {"t'autoconcurancer.": "t'autoconcurrencer.", "recherches": "recherche", "ranquer": "ranker", "tout au concurrencez": "t'autoconcurrencer", "t'autoconcurancer": "t'autoconcurrencer"},
    },
    "13-financement": {
        "seg": "B", "ranges": [(641.3, 665.2)], "first": "delphine", "speakers": [(0.0, "delphine")],
        "titre": "Indépendants, vous avez des droits",
        "question": ["Indépendant ?", "Ta formation peut être financée."],
        "fix": {"La petite ligne cotisation": "Je précise que les indépendants y ont droit. La petite ligne cotisation"},
    },
}
for k, v in RUSHES.items():
    v["id"] = k
