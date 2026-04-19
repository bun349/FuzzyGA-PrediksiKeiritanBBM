import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time

st.set_page_config(
    page_title="FuzzyGA — Prediksi Keiritan BBM",
    page_icon="⛽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.main { background: #0d0f14; }
[data-testid="stAppViewContainer"] { background: #0d0f14; }
[data-testid="stSidebar"] { background: #111420 !important; border-right: 1px solid #1e2235; }
[data-testid="stSidebar"] > div { background: #111420; }

h1,h2,h3 { font-family: 'Space Mono', monospace !important; color: #e8eaf0 !important; }

.hero-banner {
    background: linear-gradient(135deg, #0d1b3e 0%, #0a2744 40%, #0d1f3a 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(56,139,253,0.12) 0%, transparent 70%);
}
.hero-title { font-family: 'Space Mono', monospace; font-size: 1.7rem; font-weight: 700; color: #58a6ff; margin: 0 0 0.3rem; }
.hero-sub { color: #8b9bb4; font-size: 0.92rem; margin: 0; }

.metric-card {
    background: #151922;
    border: 1px solid #1e2a3a;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    text-align: center;
}
.metric-card .val { font-family: 'Space Mono', monospace; font-size: 1.8rem; font-weight: 700; color: #58a6ff; }
.metric-card .lbl { font-size: 0.78rem; color: #6e7f96; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 4px; }

.result-hero {
    background: linear-gradient(135deg, #0d2818 0%, #0a2012 100%);
    border: 1px solid #1a4a2e;
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin: 1rem 0;
}
.result-hero .mpg-val { font-family: 'Space Mono', monospace; font-size: 3.5rem; font-weight: 700; color: #3fb950; line-height: 1; }
.result-hero .mpg-unit { font-size: 1.1rem; color: #56d364; margin-top: 0.3rem; }
.result-hero .category { font-size: 0.85rem; color: #8b9bb4; margin-top: 0.5rem; }

.category-badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.04em;
}
.cat-sangat-irit { background: #0d2818; color: #3fb950; border: 1px solid #1a4a2e; }
.cat-irit        { background: #0d2818; color: #56d364; border: 1px solid #1a4a2e; }
.cat-cukup-irit  { background: #1c2a0d; color: #a8cc5c; border: 1px solid #2d4a10; }
.cat-sedang      { background: #2a1f00; color: #d29922; border: 1px solid #4a3500; }
.cat-boros       { background: #2a0f00; color: #f0883e; border: 1px solid #4a1f00; }
.cat-sangat-boros{ background: #2a0808; color: #ff7b72; border: 1px solid #4a1010; }

.rule-row { background: #151922; border: 1px solid #1e2a3a; border-radius: 8px; padding: 0.6rem 1rem; margin-bottom: 0.4rem; display: flex; align-items: center; justify-content: space-between; }
.rule-row.active { border-color: #388bfd44; background: #0d1b3e; }
.rule-label { font-size: 0.82rem; color: #8b9bb4; }
.rule-val { font-family: 'Space Mono', monospace; font-size: 0.82rem; color: #58a6ff; }
.fire-bar-bg { background: #1e2a3a; border-radius: 4px; height: 6px; width: 80px; margin-left: 12px; }
.fire-bar-fill { background: #58a6ff; border-radius: 4px; height: 6px; }

.section-header {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: #58a6ff;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 1.5rem 0 0.8rem;
    padding-bottom: 6px;
    border-bottom: 1px solid #1e2a3a;
}

.stButton>button {
    background: #1a3a5c !important;
    border: 1px solid #388bfd44 !important;
    color: #58a6ff !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.82rem !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.4rem !important;
    transition: all 0.2s !important;
}
.stButton>button:hover { background: #1e4a7a !important; border-color: #58a6ff !important; }
.stButton>button:active { transform: scale(0.97) !important; }

.stSlider > div > div > div { color: #58a6ff !important; }
[data-testid="stNumberInput"] input { background: #151922 !important; border: 1px solid #1e2a3a !important; color: #e8eaf0 !important; border-radius: 8px !important; }
[data-testid="stSelectbox"] > div { background: #151922 !important; border: 1px solid #1e2a3a !important; border-radius: 8px !important; }

.stProgress > div > div { background: #58a6ff !important; }
[data-testid="stProgressBar"] > div { background: #58a6ff !important; }

.info-box {
    background: #0d1b2e;
    border: 1px solid #1e3a5f;
    border-left: 3px solid #58a6ff;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    font-size: 0.83rem;
    color: #8b9bb4;
    margin: 0.5rem 0;
}
.warn-box {
    background: #1c1500;
    border: 1px solid #3a2e00;
    border-left: 3px solid #d29922;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    font-size: 0.83rem;
    color: #a89060;
    margin: 0.5rem 0;
}

label, .stSlider label { color: #8b9bb4 !important; font-size: 0.85rem !important; }
p { color: #c8d0dc !important; }
</style>
""", unsafe_allow_html=True)


# ─── FUZZY FUNCTIONS ───────────────────────────────────────────────────────────
def trap_left(x, a, b, c, d):
    if x <= a: return 1.0
    if x >= d: return 0.0
    if x <= b: return 1.0
    if x <= c: return (c - x) / (c - b)
    return 0.0

def trap_right(x, a, b, c, d):
    if x <= a: return 0.0
    if x >= d: return 1.0
    if x <= b: return (x - a) / (b - a)
    return 1.0

def triangle(x, a, b, c):
    if x <= a or x >= c: return 0.0
    if x <= b: return (x - a) / (b - a)
    return (c - x) / (c - b)


def calculate_fis(weight_arr, hp_arr, params):
    Z = params[0:9]
    W = np.sort(params[9:13])
    H = np.sort(params[13:17])
    predictions = np.zeros(len(weight_arr))

    for i, (w, h) in enumerate(zip(weight_arr, hp_arr)):
        mu_w_ringan = trap_left(w, W[0], W[0], W[1], W[1])
        mu_w_sedang = triangle(w, W[0], (W[0]+W[3])/2, W[3])
        mu_w_berat  = trap_right(w, W[2], W[3], W[3], W[3])

        mu_h_kecil    = trap_left(h, H[0], H[0], H[1], H[1])
        mu_h_menengah = triangle(h, H[0], (H[0]+H[3])/2, H[3])
        mu_h_besar    = trap_right(h, H[2], H[3], H[3], H[3])

        alpha = [
            min(mu_w_ringan, mu_h_kecil),
            min(mu_w_ringan, mu_h_menengah),
            min(mu_w_ringan, mu_h_besar),
            min(mu_w_sedang, mu_h_kecil),
            min(mu_w_sedang, mu_h_menengah),
            min(mu_w_sedang, mu_h_besar),
            min(mu_w_berat,  mu_h_kecil),
            min(mu_w_berat,  mu_h_menengah),
            min(mu_w_berat,  mu_h_besar),
        ]

        s = sum(alpha)
        predictions[i] = (sum(a * z for a, z in zip(alpha, Z)) / s) if s > 1e-9 else 0.0

    return predictions


def fis_single_with_alpha(weight, hp, params):
    Z = params[0:9]
    W = np.sort(params[9:13])
    H = np.sort(params[13:17])

    mu_w_ringan = trap_left(weight, W[0], W[0], W[1], W[1])
    mu_w_sedang = triangle(weight, W[0], (W[0]+W[3])/2, W[3])
    mu_w_berat  = trap_right(weight, W[2], W[3], W[3], W[3])

    mu_h_kecil    = trap_left(hp, H[0], H[0], H[1], H[1])
    mu_h_menengah = triangle(hp, H[0], (H[0]+H[3])/2, H[3])
    mu_h_besar    = trap_right(hp, H[2], H[3], H[3], H[3])

    alpha = [
        min(mu_w_ringan, mu_h_kecil),
        min(mu_w_ringan, mu_h_menengah),
        min(mu_w_ringan, mu_h_besar),
        min(mu_w_sedang, mu_h_kecil),
        min(mu_w_sedang, mu_h_menengah),
        min(mu_w_sedang, mu_h_besar),
        min(mu_w_berat,  mu_h_kecil),
        min(mu_w_berat,  mu_h_menengah),
        min(mu_w_berat,  mu_h_besar),
    ]

    s = sum(alpha)
    mpg = (sum(a * z for a, z in zip(alpha, Z)) / s) if s > 1e-9 else 0.0

    mf_berat = {'Ringan': mu_w_ringan, 'Sedang': mu_w_sedang, 'Berat': mu_w_berat}
    mf_hp    = {'Kecil': mu_h_kecil, 'Menengah': mu_h_menengah, 'Besar': mu_h_besar}

    return mpg, alpha, mf_berat, mf_hp


# ─── GENETIC ALGORITHM ─────────────────────────────────────────────────────────
def fitness_function(params, weight_arr, hp_arr, mpg_arr):
    preds = calculate_fis(weight_arr, hp_arr, params)
    mae = np.mean(np.abs(mpg_arr - preds))
    return 1.0 / (mae + 1e-6), mae


class FuzzyGA:
    def __init__(self, pop_size=50, generations=100, mutation_rate=0.1):
        self.pop_size = pop_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.base_chromosome = np.array([
            45, 38, 30, 32, 26, 20, 22, 16, 11,
            1500, 2240, 2980, 3720,
            40,  88,  136, 184
        ], dtype=np.float64)

    def create_population(self):
        pop = []
        for _ in range(self.pop_size):
            ind = np.copy(self.base_chromosome)
            ind[0:9]   += np.random.uniform(-5, 5, 9)
            ind[9:13]  += np.random.uniform(-200, 200, 4)
            ind[13:17] += np.random.uniform(-15, 15, 4)
            pop.append(ind)
        return pop

    def crossover(self, p1, p2):
        child = np.copy(p1)
        mask = np.random.rand(len(child)) > 0.5
        child[mask] = p2[mask]
        return child

    def mutate(self, child):
        for i in range(len(child)):
            if np.random.rand() < self.mutation_rate:
                if i < 9:    child[i] += np.random.uniform(-3, 3)
                elif i < 13: child[i] += np.random.uniform(-100, 100)
                else:        child[i] += np.random.uniform(-10, 10)
        return child

    def run(self, weight_arr, hp_arr, mpg_arr, progress_cb=None):
        population = self.create_population()
        best_params = None
        best_fitness = -np.inf
        history = []

        for gen in range(self.generations):
            scored = []
            for ind in population:
                fit, mae = fitness_function(ind, weight_arr, hp_arr, mpg_arr)
                scored.append((fit, mae, ind))
            scored.sort(key=lambda x: -x[0])

            if scored[0][0] > best_fitness:
                best_fitness = scored[0][0]
                best_params  = np.copy(scored[0][2])
                best_mae     = scored[0][1]

            history.append({'gen': gen+1, 'best_mae': scored[0][1], 'avg_mae': np.mean([s[1] for s in scored])})

            if progress_cb:
                progress_cb(gen+1, self.generations, scored[0][1])

            elite = [s[2] for s in scored[:5]]
            new_pop = list(elite)
            while len(new_pop) < self.pop_size:
                parents = [scored[i][2] for i in np.random.choice(20, 2, replace=False)]
                child = self.crossover(parents[0], parents[1])
                child = self.mutate(child)
                new_pop.append(child)
            population = new_pop

        return best_params, best_mae, pd.DataFrame(history)


# ─── HELPERS ───────────────────────────────────────────────────────────────────
def get_category(mpg):
    if mpg >= 40:   return "Sangat Irit",   "cat-sangat-irit"
    if mpg >= 32:   return "Irit",           "cat-irit"
    if mpg >= 26:   return "Cukup Irit",     "cat-cukup-irit"
    if mpg >= 20:   return "Sedang",         "cat-sedang"
    if mpg >= 14:   return "Boros",          "cat-boros"
    return "Sangat Boros", "cat-sangat-boros"


def build_sample_dataset():
    np.random.seed(42)
    n = 200
    weight = np.random.uniform(1500, 5200, n)
    hp     = np.random.uniform(40, 280, n)
    base_params = np.array([45,38,30,32,26,20,22,16,11, 1500,2240,2980,3720, 40,88,136,184], dtype=np.float64)
    mpg = calculate_fis(weight, hp, base_params)
    mpg += np.random.normal(0, 1.5, n)
    mpg = np.clip(mpg, 9, 47)
    return pd.DataFrame({'weight': weight, 'horsepower': hp, 'mpg': mpg})


RULE_LABELS = [
    ("R1","Ringan","Kecil"),("R2","Ringan","Menengah"),("R3","Ringan","Besar"),
    ("R4","Sedang","Kecil"),("R5","Sedang","Menengah"),("R6","Sedang","Besar"),
    ("R7","Berat", "Kecil"),("R8","Berat", "Menengah"),("R9","Berat", "Besar"),
]


# ─── PLOTTING ──────────────────────────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(13,15,20,0.8)',
    font=dict(family='DM Sans', color='#8b9bb4'),
    margin=dict(t=40,b=40,l=50,r=20),
)


def plot_mf_berat(params, current_weight=None):
    W = np.sort(params[9:13])
    x = np.linspace(1500, 5200, 400)
    ringan = [trap_left(v, W[0],W[0],W[1],W[1]) for v in x]
    sedang = [triangle(v, W[0],(W[0]+W[3])/2,W[3]) for v in x]
    berat  = [trap_right(v, W[2],W[3],W[3],W[3]) for v in x]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=ringan, name='Ringan', line=dict(color='#58a6ff',width=2)))
    fig.add_trace(go.Scatter(x=x, y=sedang, name='Sedang', line=dict(color='#3fb950',width=2)))
    fig.add_trace(go.Scatter(x=x, y=berat,  name='Berat',  line=dict(color='#f0883e',width=2)))
    if current_weight:
        fig.add_vline(x=current_weight, line=dict(color='#ff7b72',width=1.5,dash='dash'))
    fig.update_layout(**PLOT_LAYOUT, title=dict(text='MF Berat Kendaraan (kg)',font=dict(color='#e8eaf0',size=13)),
        xaxis=dict(title='kg', gridcolor='#1e2a3a', showline=True, linecolor='#1e2a3a'),
        yaxis=dict(title='μ', range=[-0.05,1.15], gridcolor='#1e2a3a'),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#8b9bb4')), height=220)
    return fig


def plot_mf_hp(params, current_hp=None):
    H = np.sort(params[13:17])
    x = np.linspace(40, 280, 400)
    kecil    = [trap_left(v, H[0],H[0],H[1],H[1]) for v in x]
    menengah = [triangle(v, H[0],(H[0]+H[3])/2,H[3]) for v in x]
    besar    = [trap_right(v, H[2],H[3],H[3],H[3]) for v in x]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=kecil,    name='Kecil',    line=dict(color='#58a6ff',width=2)))
    fig.add_trace(go.Scatter(x=x, y=menengah, name='Menengah', line=dict(color='#3fb950',width=2)))
    fig.add_trace(go.Scatter(x=x, y=besar,    name='Besar',    line=dict(color='#f0883e',width=2)))
    if current_hp:
        fig.add_vline(x=current_hp, line=dict(color='#ff7b72',width=1.5,dash='dash'))
    fig.update_layout(**PLOT_LAYOUT, title=dict(text='MF Tenaga Mesin (hp)',font=dict(color='#e8eaf0',size=13)),
        xaxis=dict(title='hp', gridcolor='#1e2a3a', showline=True, linecolor='#1e2a3a'),
        yaxis=dict(title='μ', range=[-0.05,1.15], gridcolor='#1e2a3a'),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#8b9bb4')), height=220)
    return fig


def plot_convergence(history_df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=history_df['gen'], y=history_df['best_mae'],
        name='Best MAE', line=dict(color='#58a6ff',width=2)))
    fig.add_trace(go.Scatter(x=history_df['gen'], y=history_df['avg_mae'],
        name='Avg MAE', line=dict(color='#3fb950',width=1.5,dash='dot')))
    fig.update_layout(**PLOT_LAYOUT, title=dict(text='Konvergensi Algoritma Genetika',font=dict(color='#e8eaf0',size=13)),
        xaxis=dict(title='Generasi', gridcolor='#1e2a3a'),
        yaxis=dict(title='MAE', gridcolor='#1e2a3a'),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#8b9bb4')), height=280)
    return fig


def plot_prediction_scatter(df, params):
    preds = calculate_fis(df['weight'].values, df['horsepower'].values, params)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['mpg'], y=preds, mode='markers',
        marker=dict(color='#58a6ff', size=5, opacity=0.6),
        name='Prediksi vs Aktual'))
    mn = min(df['mpg'].min(), preds.min()) - 1
    mx = max(df['mpg'].max(), preds.max()) + 1
    fig.add_trace(go.Scatter(x=[mn,mx], y=[mn,mx], mode='lines',
        line=dict(color='#f0883e',width=1.5,dash='dash'), name='Ideal'))
    fig.update_layout(**PLOT_LAYOUT, title=dict(text='Prediksi vs Aktual MPG',font=dict(color='#e8eaf0',size=13)),
        xaxis=dict(title='Aktual MPG', gridcolor='#1e2a3a'),
        yaxis=dict(title='Prediksi MPG', gridcolor='#1e2a3a'),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#8b9bb4')), height=280)
    return fig


def plot_heatmap(params):
    weights = np.linspace(1500, 5200, 40)
    hps     = np.linspace(40, 280, 40)
    Z = np.zeros((40, 40))
    for i, hp in enumerate(hps):
        Z[i] = calculate_fis(weights, np.full(40, hp), params)

    fig = go.Figure(go.Heatmap(
        x=weights, y=hps, z=Z,
        colorscale=[[0,'#2a0808'],[0.3,'#4a3500'],[0.6,'#1c2a0d'],[1,'#0d2818']],
        # Updated colorbar syntax here:
        colorbar=dict(
            title=dict(text='MPG', font=dict(color='#8b9bb4')), 
            tickfont=dict(color='#8b9bb4')
        ),
        hovertemplate='Berat: %{x:.0f} kg<br>HP: %{y:.0f}<br>MPG: %{z:.1f}<extra></extra>'
    ))
    fig.update_layout(**PLOT_LAYOUT, title=dict(text='Peta MPG (Berat × Tenaga Mesin)',font=dict(color='#e8eaf0',size=13)),
        xaxis=dict(title='Berat (kg)', gridcolor='#1e2a3a'),
        yaxis=dict(title='Tenaga Mesin (hp)', gridcolor='#1e2a3a'), height=320)
    return fig

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
if 'trained_params' not in st.session_state:
    st.session_state.trained_params = None
if 'history_df' not in st.session_state:
    st.session_state.history_df = None
if 'best_mae' not in st.session_state:
    st.session_state.best_mae = None
if 'dataset' not in st.session_state:
    st.session_state.dataset = build_sample_dataset()


# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="section-header">⚙ Parameter Algoritma Genetika</div>', unsafe_allow_html=True)
    pop_size    = st.slider("Ukuran Populasi",   20, 200, 50, 10)
    generations = st.slider("Jumlah Generasi",   20, 300, 100, 10)
    mut_rate    = st.slider("Mutation Rate",     0.01, 0.5, 0.1, 0.01, format="%.2f")

    st.markdown('<div class="section-header">📊 Dataset</div>', unsafe_allow_html=True)
    use_custom = st.checkbox("Upload dataset sendiri", False)

    if use_custom:
        uploaded = st.file_uploader("Upload CSV (weight, horsepower, mpg)", type=['csv'])
        if uploaded:
            try:
                df_up = pd.read_csv(uploaded)
                if all(c in df_up.columns for c in ['weight','horsepower','mpg']):
                    st.session_state.dataset = df_up
                    st.success(f"✓ {len(df_up)} baris dimuat")
                else:
                    st.error("Kolom harus: weight, horsepower, mpg")
            except Exception as e:
                st.error(str(e))

    df = st.session_state.dataset
    st.markdown(f'<div class="info-box">Dataset aktif: <strong style="color:#58a6ff">{len(df)} sampel</strong> | Range berat: {df["weight"].min():.0f}–{df["weight"].max():.0f} kg</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">🔧 Parameter Awal (chromosome)</div>', unsafe_allow_html=True)
    with st.expander("Lihat / ubah parameter awal"):
        st.caption("Output rules (Z1–Z9)")
        z_vals = [st.number_input(f"Z{i+1} ({RULE_LABELS[i][1]}/{RULE_LABELS[i][2]})", value=float([45,38,30,32,26,20,22,16,11][i]), step=1.0, key=f'z{i}') for i in range(9)]
        st.caption("Batas berat kendaraan (kg)")
        w1 = st.number_input("W1", value=1500.0, step=100.0)
        w2 = st.number_input("W2", value=2240.0, step=100.0)
        w3 = st.number_input("W3", value=2980.0, step=100.0)
        w4 = st.number_input("W4", value=3720.0, step=100.0)
        st.caption("Batas tenaga mesin (hp)")
        h1 = st.number_input("H1", value=40.0, step=5.0)
        h2 = st.number_input("H2", value=88.0, step=5.0)
        h3 = st.number_input("H3", value=136.0, step=5.0)
        h4 = st.number_input("H4", value=184.0, step=5.0)
        custom_base = np.array(z_vals + [w1,w2,w3,w4,h1,h2,h3,h4], dtype=np.float64)

    # BAGIAN 'else' DIHAPUS KARENA MENYEBABKAN SYNTAX ERROR

    if st.button("🧬 Jalankan Training GA", use_container_width=True):
        ga = FuzzyGA(pop_size=pop_size, generations=generations, mutation_rate=mut_rate)
        if custom_base is not None:
            ga.base_chromosome = custom_base

        prog_bar = st.progress(0)
        prog_text = st.empty()

        def progress_cb(gen, total, mae):
            pct = gen / total
            prog_bar.progress(pct)
            prog_text.markdown(f'<small style="color:#8b9bb4">Gen {gen}/{total} — MAE: {mae:.4f}</small>', unsafe_allow_html=True)

        with st.spinner(""):
            best_p, best_mae, hist = ga.run(
                df['weight'].values, df['horsepower'].values, df['mpg'].values,
                progress_cb=progress_cb
            )

        st.session_state.trained_params = best_p
        st.session_state.history_df     = hist
        st.session_state.best_mae       = best_mae
        prog_bar.empty(); prog_text.empty()
        st.success(f"✓ Selesai! MAE akhir: {best_mae:.4f}")


# ─── MAIN ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <div class="hero-title">⛽ FuzzyGA — Prediksi Keiritan BBM</div>
  <div class="hero-sub">Sistem Inferensi Fuzzy Sugeno yang dioptimasi dengan Algoritma Genetika</div>
</div>
""", unsafe_allow_html=True)

params = st.session_state.trained_params if st.session_state.trained_params is not None else \
         np.array([45,38,30,32,26,20,22,16,11, 1500,2240,2980,3720, 40,88,136,184], dtype=np.float64)

tab1, tab2, tab3 = st.tabs(["🔮 Prediksi", "📈 Visualisasi", "🧬 Hasil Training"])

# ──────── TAB 1: PREDIKSI ───────────────────────────────────────────────────
with tab1:
    if st.session_state.trained_params is None:
        st.markdown('<div class="warn-box">⚠ Model belum dilatih. Menggunakan parameter default. Jalankan Training GA di sidebar untuk hasil optimal.</div>', unsafe_allow_html=True)

    col_inp, col_res = st.columns([1, 1], gap="large")

    with col_inp:
        st.markdown('<div class="section-header">🚗 Data Kendaraan</div>', unsafe_allow_html=True)
        weight_in = st.slider("Berat Kendaraan (kg)", 1500, 5200, 2500, 50)
        hp_in     = st.slider("Tenaga Mesin (hp)",    40,   280,  130,  5)

        mpg_pred, alpha, mf_b, mf_h = fis_single_with_alpha(weight_in, hp_in, params)
        cat_label, cat_cls = get_category(mpg_pred)

        st.markdown(f"""
        <div class="result-hero">
          <div class="mpg-val">{mpg_pred:.2f}</div>
          <div class="mpg-unit">Miles Per Gallon</div>
          <div class="category" style="margin-top:0.8rem">
            <span class="category-badge {cat_cls}">{cat_label}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        lpm = 235.214 / mpg_pred if mpg_pred > 0 else 0
        km_liter = mpg_pred * 0.4251
        co2 = 2392 / mpg_pred if mpg_pred > 0 else 0
        c1.markdown(f'<div class="metric-card"><div class="val">{lpm:.1f}</div><div class="lbl">L/100 km</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="metric-card"><div class="val">{km_liter:.1f}</div><div class="lbl">km/liter</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="metric-card"><div class="val">{co2:.0f}</div><div class="lbl">g CO₂/km</div></div>', unsafe_allow_html=True)

    with col_res:
        st.markdown('<div class="section-header">🔥 Aktivasi Rule Base</div>', unsafe_allow_html=True)
        for idx, (r, b, h) in enumerate(RULE_LABELS):
            w = alpha[idx]
            z = params[idx]
            active = w > 0.01
            bar_w = int(w * 80)
            st.markdown(f"""
            <div class="rule-row {'active' if active else ''}">
              <span class="rule-label">{r}: {b} + {h}</span>
              <span style="display:flex;align-items:center;gap:8px">
                <span class="rule-val">{z:.1f} MPG</span>
                <div class="fire-bar-bg"><div class="fire-bar-fill" style="width:{bar_w}px"></div></div>
                <span style="font-family:Space Mono,monospace;font-size:0.75rem;color:{'#58a6ff' if active else '#3a4a5a'};min-width:36px;text-align:right">{w:.3f}</span>
              </span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">📐 Derajat Keanggotaan</div>', unsafe_allow_html=True)
        cols = st.columns(2)
        with cols[0]:
            st.caption("Berat Kendaraan")
            for k, v in mf_b.items():
                st.markdown(f'<div style="display:flex;justify-content:space-between;font-size:0.82rem;padding:3px 0"><span style="color:#8b9bb4">{k}</span><span style="font-family:Space Mono,monospace;color:#58a6ff">{v:.4f}</span></div>', unsafe_allow_html=True)
        with cols[1]:
            st.caption("Tenaga Mesin")
            for k, v in mf_h.items():
                st.markdown(f'<div style="display:flex;justify-content:space-between;font-size:0.82rem;padding:3px 0"><span style="color:#8b9bb4">{k}</span><span style="font-family:Space Mono,monospace;color:#58a6ff">{v:.4f}</span></div>', unsafe_allow_html=True)


# ──────── TAB 2: VISUALISASI ────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-header">📐 Fungsi Keanggotaan</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(plot_mf_berat(params, weight_in), use_container_width=True)
    with c2:
        st.plotly_chart(plot_mf_hp(params, hp_in), use_container_width=True)

    st.plotly_chart(plot_heatmap(params), use_container_width=True)

if st.session_state.trained_params is not None:
    st.plotly_chart(plot_prediction_scatter(df, params), use_container_width=True, key="scatter_tab2")

    st.markdown('<div class="section-header">📋 Rule Base (Parameter Aktif)</div>', unsafe_allow_html=True)
    W = np.sort(params[9:13])
    H = np.sort(params[13:17])
    Z = params[0:9]
    rule_df = pd.DataFrame([
        {"Rule": RULE_LABELS[i][0], "Berat": RULE_LABELS[i][1], "HP": RULE_LABELS[i][2],
         "Output MPG": f"{Z[i]:.2f}", "Firing": f"{alpha[i]:.4f}"}
        for i in range(9)
    ])
    st.dataframe(rule_df, use_container_width=True, hide_index=True)

    with st.expander("Parameter fungsi keanggotaan aktif"):
        p_df = pd.DataFrame({
            "Parameter": ["W1","W2","W3","W4","H1","H2","H3","H4"],
            "Nilai": [f"{v:.2f}" for v in list(W)+list(H)],
            "Keterangan": [
                "Batas bawah Ringan","Batas atas Ringan / Sedang awal",
                "Puncak Sedang / Berat awal","Batas atas Berat",
                "Batas bawah Kecil","Batas atas Kecil / Menengah awal",
                "Puncak Menengah / Besar awal","Batas atas Besar"
            ]
        })
        st.dataframe(p_df, use_container_width=True, hide_index=True)


# ──────── TAB 3: HASIL TRAINING ─────────────────────────────────────────────
with tab3:
    if st.session_state.history_df is None:
        st.markdown('<div class="info-box">Belum ada data training. Jalankan Training GA di sidebar terlebih dahulu.</div>', unsafe_allow_html=True)
    else:
        hist = st.session_state.history_df
        mae  = st.session_state.best_mae
        preds_all = calculate_fis(df['weight'].values, df['horsepower'].values, params)
        rmse = np.sqrt(np.mean((df['mpg'].values - preds_all)**2))
        r2   = 1 - np.sum((df['mpg'].values - preds_all)**2) / np.sum((df['mpg'].values - df['mpg'].mean())**2)

        c1,c2,c3,c4 = st.columns(4)
        c1.markdown(f'<div class="metric-card"><div class="val">{mae:.4f}</div><div class="lbl">Best MAE</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="metric-card"><div class="val">{rmse:.4f}</div><div class="lbl">RMSE</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="metric-card"><div class="val">{r2:.4f}</div><div class="lbl">R²</div></div>', unsafe_allow_html=True)
        c4.markdown(f'<div class="metric-card"><div class="val">{len(hist)}</div><div class="lbl">Generasi</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.plotly_chart(plot_convergence(hist), use_container_width=True)
        st.plotly_chart(plot_prediction_scatter(df, params), use_container_width=True, key="scatter_tab3")

        st.markdown('<div class="section-header">📥 Export Parameter Terbaik</div>', unsafe_allow_html=True)
        param_export = pd.DataFrame({
            "Nama": [f"Z{i+1}" for i in range(9)] + ["W1","W2","W3","W4","H1","H2","H3","H4"],
            "Nilai": params.tolist()
        })
        csv_str = param_export.to_csv(index=False)
        st.download_button("⬇ Download Parameter (CSV)", csv_str, "best_params_ga.csv", "text/csv", use_container_width=True)

        st.markdown('<div class="section-header">📋 Riwayat Konvergensi</div>', unsafe_allow_html=True)
        st.dataframe(hist.rename(columns={'gen':'Generasi','best_mae':'Best MAE','avg_mae':'Avg MAE'}).tail(20),
                     use_container_width=True, hide_index=True)