# 🏠 Projet Big Data — Analyse du Marché Immobilier Français

> Projet M2 TIDE — Big Data Analytics  
> Alexis Johnson · Saikou BAH — 2026

Pipeline complet de collecte, traitement, analyse NLP et modélisation ML sur des annonces immobilières françaises scrappées depuis **LeBonCoin** et **BienIci**, couvrant 5 villes : Paris, Lyon, Marseille, Bordeaux, Nantes.

---

## 📁 Structure du repo

```
bigdata-immobilier/
├── 01_scraping.ipynb          # Scraping via Firecrawl API (LeBonCoin + BienIci)
├── 02_spark_nettoyage.ipynb   # Nettoyage et standardisation PySpark
├── 03_spark_nlp.ipynb         # Analyse NLP MapReduce — Top 50 mots
├── 04_modelisation.ipynb      # EDA + Régression + Classification PySpark ML
├── app.py                     # Application Streamlit — estimation de prix
├── data/
│   ├── raw/                   # CSVs bruts scrappés
│   └── clean/                 # Parquet nettoyé (partitionné par ville)
├── models/
│   └── gbt_regression/        # Modèle GBT sauvegardé (PipelineModel)
└── .devcontainer/             # Config GitHub Codespaces (Docker + Java + PySpark)
```

---

## ⚙️ Pipeline

### 01 — Scraping
- Source : LeBonCoin + BienIci via API Firecrawl
- 5 778 annonces collectées sur 5 villes
- Sortie : CSV bruts dans `data/raw/`

### 02 — Nettoyage PySpark
- Standardisation des types (`surface`, `prix`, `nb_pieces`, `nb_chambres`, `code_postal`)
- Suppression des doublons et valeurs aberrantes
- Parsing CSV multiLine (descriptions avec sauts de ligne)
- Sortie : Parquet partitionné par ville dans `data/clean/`

### 03 — NLP MapReduce
- Tokenisation des descriptions avec regex préservant les accents français
- Suppression des stopwords (grammaticaux, commerciaux, noms de villes, mentions légales)
- Comptage MapReduce PySpark → extraction du **Top 50 mots**
- Ces mots deviennent des **features binaires** (présence/absence) pour le ML

### 04 — Modélisation
**Régression — prédiction du prix :**
| Modèle | RMSE (€) | MAE (€) | R² |
|--------|----------|---------|-----|
| Régression Linéaire | 268 157 | 183 383 | 0.5325 |
| Random Forest | 210 753 | 105 965 | 0.7112 |
| **GBT Regressor** ✅ | **188 416** | **103 369** | **0.7692** |

**Classification — bien cher ou non (vs médiane ville ±10%) :**
| Modèle | AUC | Accuracy | F1 |
|--------|-----|----------|----|
| Régression Logistique | 0.684 | 0.625 | 0.625 |
| Random Forest | 0.708 | 0.649 | 0.649 |
| **GBT Classifier** ✅ | **0.7121** | **0.6336** | **0.6336** |

Features : surface, nb_pièces, nb_chambres, ville (OHE), type_bien (OHE) + 50 features NLP binaires.

---

## 🚀 Lancer l'application Streamlit

### Prérequis
Avoir exécuté le notebook `04_modelisation.ipynb` en entier pour générer le modèle dans `models/gbt_regression/`.

### Démarrage

```bash
# Dans le Codespace ou en local
streamlit run app.py
```

L'app permet d'estimer le prix d'un bien en renseignant ville, type, surface, pièces, chambres et une description optionnelle. Elle utilise le modèle GBT Regressor chargé via PySpark ML.

---

## 🛠️ Environnement

- **Python** 3.10
- **PySpark** 4.1.1 (MLlib, SQL, MapReduce)
- **Streamlit** — interface de démo
- **GitHub Codespaces** — `.devcontainer` fourni (Docker + Java + PySpark)

### Installation manuelle (hors Codespace)

```bash
pip install pyspark streamlit pandas numpy matplotlib seaborn scipy
```

> Java 11+ requis pour PySpark.

---

## 👥 Auteurs

| Membre | GitHub | Périmètre |
|--------|--------|-----------|
| Alexis Johnson | [@AlexisJohnson-data](https://github.com/AlexisJohnson-data) | Scraping · NLP · données CSV |
| Saikou BAH | [@Saikou-BAH](https://github.com/Saikou-BAH) | Nettoyage PySpark · Modélisation · Rapport |
