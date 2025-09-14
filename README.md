# Carouselle Maker

## Description
Carouselle Maker est une application qui permet de générer des carrousels pour les réseaux sociaux tels que Instagram et LinkedIn. L'application utilise Streamlit pour fournir une interface utilisateur interactive où les utilisateurs peuvent personnaliser leurs carrousels en choisissant des arrière-plans, en ajoutant du texte et en téléchargeant des logos.

## Structure du projet
Le projet est organisé comme suit :

```
carouselle-maker
├── src
│   ├── app.py                # Point d'entrée de l'application
│   └── components
│       ├── backgrounds.py     # Fonctions pour créer des arrière-plans
│       └── exporters.py       # Fonctions pour exporter les carrousels
├── requirements.txt           # Dépendances nécessaires
└── README.md                  # Documentation du projet
```

## Installation
Pour installer les dépendances nécessaires, exécutez la commande suivante dans votre terminal :

```
pip install -r requirements.txt
```

## Utilisation
Pour exécuter l'application, utilisez la commande suivante :

```
streamlit run src/app.py
```

Une fois l'application lancée, vous pourrez :

1. Choisir le format de carrousel.
2. Sélectionner un style d'arrière-plan.
3. Ajouter du texte pour chaque diapositive.
4. Télécharger votre carrousel au format PNG ou PDF.

## Contribuer
Les contributions sont les bienvenues ! N'hésitez pas à soumettre des demandes de tirage pour des améliorations ou des corrections de bogues.

## License
Ce projet est sous licence MIT. Veuillez consulter le fichier LICENSE pour plus de détails.# iacubateur_carouselle_maker
