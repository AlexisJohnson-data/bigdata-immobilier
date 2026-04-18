import streamlit as st
import pandas as pd
import numpy as np

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ImmoPredict — Estimation Prix",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# CSS CUSTOM
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg:        #0a0f1e;
    --bg2:       #111827;
    --bg3:       #1a2235;
    --border:    rgba(255,255,255,0.07);
    --accent:    #4f8ef7;
    --accent2:   #7c5df9;
    --gold:      #f5c842;
    --text:      #e8edf5;
    --muted:     #6b7a99;
    --success:   #34d399;
    --danger:    #f87171;
    --radius:    16px;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text);
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem !important; max-width: 1200px; }

/* ── HERO ── */
.hero {
    background: linear-gradient(135deg, #0d1b3e 0%, #0a0f1e 50%, #1a0a2e 100%);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 3rem 3.5rem;
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(79,142,247,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 30%;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(124,93,249,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-tag {
    display: inline-block;
    background: rgba(79,142,247,0.12);
    border: 1px solid rgba(79,142,247,0.3);
    color: var(--accent);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.3rem 0.9rem;
    border-radius: 100px;
    margin-bottom: 1.2rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    line-height: 1.15;
    margin: 0 0 0.8rem 0;
    background: linear-gradient(135deg, #fff 30%, #4f8ef7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero p {
    color: var(--muted);
    font-size: 1.05rem;
    font-weight: 300;
    max-width: 600px;
    line-height: 1.7;
    margin: 0;
}

/* ── CARDS ── */
.card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.8rem;
    margin-bottom: 1.2rem;
}
.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.card-title span { color: var(--accent); }

/* ── RESULT BOX ── */
.result-box {
    background: linear-gradient(135deg, #0d1b3e, #111827);
    border: 1px solid rgba(79,142,247,0.3);
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.result-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
}
.result-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.5rem;
}
.result-price {
    font-family: 'Syne', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #fff, var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
}
.result-m2 {
    font-size: 1rem;
    color: var(--muted);
    margin-top: 0.4rem;
}
.result-range {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
}
.range-item { text-align: center; }
.range-val {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text);
}
.range-lbl {
    font-size: 0.7rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* ── METRIC CHIPS ── */
.chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    margin-top: 1rem;
}
.chip {
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 100px;
    padding: 0.35rem 0.9rem;
    font-size: 0.8rem;
    color: var(--muted);
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.chip b { color: var(--text); }

/* ── MODEL BADGE ── */
.model-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(52,211,153,0.1);
    border: 1px solid rgba(52,211,153,0.25);
    color: var(--success);
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.3rem 0.8rem;
    border-radius: 100px;
    margin-bottom: 1rem;
}

/* ── INPUTS OVERRIDE ── */
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
}
.stSlider > div { padding: 0 !important; }

/* ── BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2.5rem !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(79,142,247,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(79,142,247,0.45) !important;
}

/* ── SEPARATOR ── */
hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

/* ── LABEL ── */
label, .stSelectbox label, .stNumberInput label, .stSlider label {
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: var(--muted) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.07em !important;
}

/* ── INFO BOX ── */
.info-box {
    background: rgba(79,142,247,0.06);
    border: 1px solid rgba(79,142,247,0.15);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    font-size: 0.85rem;
    color: var(--muted);
    line-height: 1.6;
    margin-top: 1rem;
}
.info-box b { color: var(--accent); }

/* ── COUNTER ANIMATION ── */
@keyframes countUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
.result-price-animated {
    font-family: 'Syne', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #fff, var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
    animation: countUp 0.6s ease forwards;
}

/* ── COMPARATEUR ── */
.comparator {
    margin-top: 1.2rem;
    padding: 1rem 1.2rem;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}
.comparator.above {
    background: rgba(248,113,113,0.08);
    border: 1px solid rgba(248,113,113,0.2);
}
.comparator.below {
    background: rgba(52,211,153,0.08);
    border: 1px solid rgba(52,211,153,0.2);
}
.comparator.neutral {
    background: rgba(107,122,153,0.08);
    border: 1px solid rgba(107,122,153,0.2);
}
.comp-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
}
.comp-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
}
.comp-value.above { color: #f87171; }
.comp-value.below { color: #34d399; }
.comp-value.neutral { color: var(--muted); }
.comp-desc {
    font-size: 0.78rem;
    color: var(--muted);
    margin-top: 0.15rem;
}

/* ── JAUGE R² ── */
.gauge-box {
    margin-top: 1.2rem;
    padding: 1rem 1.2rem;
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 12px;
}
.gauge-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.6rem;
}
.gauge-title {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: var(--muted);
}
.gauge-score {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: var(--accent);
}
.gauge-track {
    height: 6px;
    background: rgba(255,255,255,0.06);
    border-radius: 100px;
    overflow: hidden;
}
.gauge-fill {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
}
.gauge-labels {
    display: flex;
    justify-content: space-between;
    margin-top: 0.4rem;
    font-size: 0.62rem;
    color: var(--muted);
}

/* ── FEATURE TAGS ── */
.feature-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.8rem;
}
.ftag {
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.4rem 0.75rem;
    font-size: 0.78rem;
    color: var(--text);
}
.ftag-active {
    background: rgba(79,142,247,0.12);
    border-color: rgba(79,142,247,0.3);
    color: var(--accent);
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDE TICKERS
# ─────────────────────────────────────────────
st.markdown("""
<style>
.ticker-left, .ticker-right {
    position: fixed;
    top: 0;
    width: 32px;
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow: hidden;
    z-index: 999;
    opacity: 0.18;
}
.ticker-left  { left: 0;  border-right: 1px solid rgba(255,255,255,0.06); }
.ticker-right { right: 0; border-left:  1px solid rgba(255,255,255,0.06); }

.ticker-track {
    display: flex;
    flex-direction: column;
    animation: scrollUp 12s linear infinite;
    gap: 2.5rem;
    padding-top: 2rem;
}
.ticker-right .ticker-track { animation-direction: reverse; }

.ticker-track span {
    font-family: 'Syne', sans-serif;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
    writing-mode: vertical-rl;
    text-orientation: mixed;
}

@keyframes scrollUp {
    0%   { transform: translateY(0); }
    100% { transform: translateY(-50%); }
}
</style>

<div class="ticker-left">
    <div class="ticker-track">
        <span>Paris</span><span>Lyon</span><span>Marseille</span>
        <span>Bordeaux</span><span>Nantes</span>
        <span>Paris</span><span>Lyon</span><span>Marseille</span>
        <span>Bordeaux</span><span>Nantes</span>
    </div>
</div>
<div class="ticker-right">
    <div class="ticker-track">
        <span>Paris</span><span>Lyon</span><span>Marseille</span>
        <span>Bordeaux</span><span>Nantes</span>
        <span>Paris</span><span>Lyon</span><span>Marseille</span>
        <span>Bordeaux</span><span>Nantes</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SPARK + MODEL LOADING
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_spark_and_model():
    from pyspark.sql import SparkSession
    from pyspark.ml import PipelineModel

    spark = SparkSession.builder \
        .appName("ImmoPredict_App") \
        .master("local[2]") \
        .config("spark.ui.enabled", "false") \
        .config("spark.sql.shuffle.partitions", "4") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    model = PipelineModel.load("/workspaces/bigdata-immobilier/projet/models/gbt_regression")
    return spark, model


# ─────────────────────────────────────────────
# TOP 50 MOTS NLP
# ─────────────────────────────────────────────
TOP50_MOTS = [
    'appartement','situ','tage','maison','quartier','rue','immeuble','calme',
    'chambres','terrasse','cuisine','salle','lumineux','ascenseur','balcon',
    'jardin','saint','vie','proximit','jour','place','vue','exclusivit',
    'dernier','parking','vendre','coeur','commerces','garage','proche',
    'duplex','cave','recherch','studio','entr','eau','copropri','offre',
    'rement','immobilier','nov','sejour','espace','beau','entier',
    'sud','expo','risques','geo','calme'
]


def predict_price(spark, model, surface, nb_pieces, nb_chambres, ville, type_bien, description=""):
    from pyspark.sql import functions as F

    data = [{
        "surface":     float(surface),
        "nb_pieces":   int(nb_pieces),
        "nb_chambres": int(nb_chambres),
        "ville":       ville,
        "type_bien":   type_bien,
        "description": description.lower(),
        "prix":        0.0,
        "prix_m2":     0.0,
    }]

    df = spark.createDataFrame(data)

    for mot in TOP50_MOTS:
        df = df.withColumn("nlp_" + mot, F.when(F.col("description").contains(mot), 1.0).otherwise(0.0))

    preds = model.transform(df)
    prix  = preds.select("prediction").collect()[0][0]
    return max(prix, 0)


# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag">🏙️ Marché Immobilier Français</div>
    <h1>Estimation de Prix<br>Immobilier</h1>
    <p>Prédiction intelligente basée sur un modèle Gradient Boosting entraîné sur plus de 4 800 annonces réelles issues de LeBonCoin et BienIci.</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LAYOUT
# ─────────────────────────────────────────────
col_form, col_result = st.columns([1.1, 0.9], gap="large")

# ── FORMULAIRE ──
with col_form:

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span>01</span> Localisation</div>', unsafe_allow_html=True)

    col_v, col_t = st.columns(2)
    with col_v:
        ville = st.selectbox("Ville", ["Paris", "Lyon", "Marseille", "Bordeaux", "Nantes"], index=0)
    with col_t:
        type_bien = st.selectbox("Type de bien", ["appartement", "maison", "studio", "duplex", "loft"], index=0)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span>02</span> Caractéristiques</div>', unsafe_allow_html=True)

    surface = st.slider("Surface (m²)", min_value=10, max_value=400, value=65, step=1)

    col_p, col_c = st.columns(2)
    with col_p:
        nb_pieces = st.number_input("Nombre de pièces", min_value=1, max_value=15, value=3)
    with col_c:
        nb_chambres = st.number_input("Nombre de chambres", min_value=0, max_value=10, value=2)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span>03</span> Description <span style="font-size:0.65rem;color:#6b7a99;text-transform:none;letter-spacing:0">(optionnel — améliore la précision)</span></div>', unsafe_allow_html=True)

    description = st.text_area(
        "Description de l'annonce",
        placeholder="Ex: Bel appartement lumineux avec terrasse, proche commerces et transports, parking inclus...",
        height=100,
        label_visibility="collapsed"
    )

    # Tags NLP détectés
    if description:
        mots_detectes = [m for m in TOP50_MOTS if m in description.lower()]
        if mots_detectes:
            tags_html = '<div class="feature-row">'
            for m in mots_detectes[:12]:
                tags_html += f'<span class="ftag ftag-active">✓ {m}</span>'
            tags_html += '</div>'
            st.markdown(tags_html, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    predict_btn = st.button("✦ Estimer le prix", use_container_width=True)

# ── RÉSULTAT ──
with col_result:

    st.markdown('<div class="model-badge">✦ GBT Regressor — Meilleur modèle</div>', unsafe_allow_html=True)

    if predict_btn:
        with st.spinner("Calcul en cours..."):
            try:
                spark, model = load_spark_and_model()
                prix_predit  = predict_price(spark, model, surface, nb_pieces, nb_chambres, ville, type_bien, description)
                prix_m2      = prix_predit / surface if surface > 0 else 0
                prix_low     = prix_predit * 0.90
                prix_high    = prix_predit * 1.10

                # Comparateur vs médiane ville
                MEDIANES_M2 = {"Paris": 9800, "Lyon": 4200, "Marseille": 3100, "Bordeaux": 4500, "Nantes": 3800}
                mediane_ville_m2 = MEDIANES_M2[ville]
                prix_median_ville = mediane_ville_m2 * surface
                diff_pct = ((prix_predit - prix_median_ville) / prix_median_ville) * 100

                if diff_pct > 5:
                    comp_class = "above"
                    comp_icon  = "↑"
                    comp_txt   = f"Au-dessus du marché {ville}"
                elif diff_pct < -5:
                    comp_class = "below"
                    comp_icon  = "↓"
                    comp_txt   = f"En dessous du marché {ville}"
                else:
                    comp_class = "neutral"
                    comp_icon  = "≈"
                    comp_txt   = f"Dans la moyenne du marché {ville}"

                # Animation JS compteur
                st.markdown(f"""
                <div class="result-box">
                    <div class="result-label">Prix estimé</div>
                    <div class="result-price-animated" id="price-display">{prix_predit:,.0f} €</div>
                    <div class="result-m2">{prix_m2:,.0f} €/m² · {surface} m²</div>
                    <div class="result-range">
                        <div class="range-item">
                            <div class="range-val">{prix_low:,.0f} €</div>
                            <div class="range-lbl">Fourchette basse</div>
                        </div>
                        <div class="range-item">
                            <div class="range-val">{prix_high:,.0f} €</div>
                            <div class="range-lbl">Fourchette haute</div>
                        </div>
                    </div>
                </div>

                <script>
                (function() {{
                    const el = document.getElementById('price-display');
                    if (!el) return;
                    const target = {prix_predit:.0f};
                    const duration = 900;
                    const start = performance.now();
                    function update(now) {{
                        const elapsed = now - start;
                        const progress = Math.min(elapsed / duration, 1);
                        const ease = 1 - Math.pow(1 - progress, 3);
                        const current = Math.round(ease * target);
                        el.textContent = current.toLocaleString('fr-FR') + ' €';
                        if (progress < 1) requestAnimationFrame(update);
                    }}
                    requestAnimationFrame(update);
                }})();
                </script>

                <div class="comparator {comp_class}">
                    <div>
                        <div class="comp-label">vs marché {ville}</div>
                        <div class="comp-desc">{comp_txt}</div>
                    </div>
                    <div class="comp-value {comp_class}">{comp_icon} {abs(diff_pct):.1f}%</div>
                </div>

                <div class="gauge-box">
                    <div class="gauge-header">
                        <div class="gauge-title">Confiance du modèle (R²)</div>
                        <div class="gauge-score">75.5%</div>
                    </div>
                    <div class="gauge-track">
                        <div class="gauge-fill" style="width: 75.5%"></div>
                    </div>
                    <div class="gauge-labels">
                        <span>Faible</span>
                        <span>Modéré</span>
                        <span>Élevé</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="chips">
                    <div class="chip">🏙️ <b>{ville}</b></div>
                    <div class="chip">🏠 <b>{type_bien}</b></div>
                    <div class="chip">📐 <b>{surface} m²</b></div>
                    <div class="chip">🛏 <b>{nb_chambres} ch.</b></div>
                    <div class="chip">🔑 <b>{nb_pieces} pièces</b></div>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Erreur lors de la prédiction : {e}")
                st.info("Assurez-vous que le modèle est sauvegardé dans `../models/gbt_regression`")

    else:
        st.markdown("""
        <div class="result-box" style="opacity:0.5;">
            <div class="result-label">Prix estimé</div>
            <div class="result-price" style="font-size:2rem;color:#6b7a99;">— €</div>
            <div class="result-m2">Renseignez le formulaire et cliquez sur Estimer</div>
        </div>
        """, unsafe_allow_html=True)

    # Info box modèle
    st.markdown("""
    <div class="info-box">
        <b>Modèle</b> : Gradient Boosting Regressor (PySpark ML)<br>
        <b>Features</b> : Surface, pièces, chambres, ville, type + 50 mots NLP<br>
        <b>Données</b> : 4 860 annonces · LeBonCoin & BienIci<br>
        <b>Villes</b> : Paris · Lyon · Marseille · Bordeaux · Nantes
    </div>
    """, unsafe_allow_html=True)

    # Médianes de référence par ville
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="card-title" style="margin-bottom:0.8rem"><span>📊</span> Prix médians de référence</div>', unsafe_allow_html=True)

    medianes = {
        "Paris": 9800, "Lyon": 4200, "Marseille": 3100,
        "Bordeaux": 4500, "Nantes": 3800
    }
    cols_med = st.columns(5)
    for i, (v, m) in enumerate(medianes.items()):
        is_selected = (v == ville)
        bg = "rgba(79,142,247,0.12)" if is_selected else "var(--bg3)"
        border = "rgba(79,142,247,0.3)" if is_selected else "var(--border)"
        color = "#4f8ef7" if is_selected else "#6b7a99"
        cols_med[i].markdown(f"""
        <div style="background:{bg};border:1px solid {border};border-radius:10px;padding:0.7rem;text-align:center;">
            <div style="font-size:0.65rem;color:{color};font-weight:700;text-transform:uppercase;letter-spacing:0.08em">{v}</div>
            <div style="font-family:'Syne',sans-serif;font-size:0.95rem;font-weight:700;color:{'#fff' if is_selected else '#e8edf5'};margin-top:0.2rem">{m:,}€</div>
            <div style="font-size:0.6rem;color:#6b7a99">/m²</div>
        </div>
        """, unsafe_allow_html=True)