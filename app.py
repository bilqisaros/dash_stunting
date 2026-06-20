import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from data_utils import (
    load_data, get_province_summary, get_faktor_summary,
    VAR_LABELS, VAR_UNITS, FAKTOR_COLORS, KATEGORI_COLORS, KATEGORI_ORDER,
)

# PAGE CONFIG
st.set_page_config(
    page_title="Precision Stunting Policy | Dashboard GWRF Indonesia",
    page_icon="\U0001F4CA",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700;9..144,900&family=Inter:wght@400;500;600;700;800&display=swap');

:root {
  --cream: #FAF6EF;
  --cream-deep: #F2EBDD;
  --card: #FFFFFF;
  --ink: #2B2620;
  --ink-soft: #6B6256;
  --forest: #1B4332;
  --teal: #2D8B72;
  --teal-soft: #E3F1EC;
  --terracotta: #C9683B;
  --terracotta-soft: #FBEAE0;
  --gold: #C99A2E;
  --gold-soft: #FAF1DC;
  --line: #E7DFD0;
  --line-soft: #F0EAE0;
}

html, body, [data-testid="stAppViewContainer"] {
  background-color: var(--cream);
  color: var(--ink);
  font-family: 'Inter', sans-serif;
}
[data-testid="stSidebar"] {
  background: var(--cream-deep);
  border-right: 1px solid var(--line);
}
[data-testid="stHeader"] { background: rgba(250,246,239,0); }
.block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1300px; }

h1, h2, h3 { font-family: 'Fraunces', serif; color: var(--forest); }

.topbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 6px 0 18px;
  border-bottom: 1px solid var(--line);
  margin-bottom: 28px;
}
.topbar-brand { display: flex; align-items: center; gap: 10px; }
.topbar-mark {
  width: 34px; height: 34px; border-radius: 9px;
  background: linear-gradient(135deg, var(--teal) 0%, var(--forest) 100%);
  display: flex; align-items: center; justify-content: center;
  color: white; font-family: 'Fraunces', serif; font-weight: 700; font-size: 16px;
}
.topbar-name { font-family: 'Fraunces', serif; font-weight: 600; font-size: 17px; color: var(--forest); }
.topbar-tag { font-size: 11px; color: var(--ink-soft); letter-spacing: .4px; }
.topbar-pill {
  background: var(--teal-soft); color: var(--forest);
  border: 1px solid rgba(45,139,114,.25);
  padding: 5px 14px; border-radius: 20px;
  font-size: 12px; font-weight: 600;
}

.hero {
  background: linear-gradient(135deg, #1B4332 0%, #245C45 55%, #2D8B72 100%);
  border-radius: 22px;
  padding: 46px 44px 40px;
  margin-bottom: 30px;
  position: relative;
  overflow: hidden;
  color: #F4F1E8;
}
.hero::before {
  content: '';
  position: absolute; top: -80px; right: -80px;
  width: 360px; height: 360px; border-radius: 50%;
  background: radial-gradient(circle, rgba(232,179,65,.18) 0%, transparent 70%);
}
.hero::after {
  content: '';
  position: absolute; bottom: -100px; left: 10%;
  width: 320px; height: 320px; border-radius: 50%;
  background: radial-gradient(circle, rgba(255,255,255,.07) 0%, transparent 70%);
}
.hero-eyebrow {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(255,255,255,.12);
  border: 1px solid rgba(255,255,255,.22);
  padding: 5px 14px; border-radius: 20px;
  font-size: 11px; font-weight: 700; letter-spacing: 1.1px; text-transform: uppercase;
  margin-bottom: 18px; color: #EAF5EF;
}
.hero-title {
  font-family: 'Fraunces', serif;
  font-size: clamp(28px, 3.4vw, 42px);
  font-weight: 700; line-height: 1.22;
  color: #FFFFFF; margin-bottom: 14px; max-width: 760px;
}
.hero-title em { font-style: italic; color: #E8B341; }
.hero-sub {
  font-size: 15px; line-height: 1.75; color: #DCEAE2;
  max-width: 640px; margin-bottom: 22px;
}
.hero-stats { display: flex; gap: 34px; flex-wrap: wrap; margin-top: 10px; }
.hero-stat-val { font-family: 'Fraunces', serif; font-size: 30px; font-weight: 700; color: #FFFFFF; line-height: 1; }
.hero-stat-lbl { font-size: 11.5px; color: #BFE0CF; margin-top: 5px; letter-spacing: .3px; }

.sec-eyebrow {
  font-size: 11px; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase;
  color: var(--teal); margin-bottom: 6px;
}
.sec-title { font-family: 'Fraunces', serif; font-size: 24px; font-weight: 600; color: var(--forest); margin-bottom: 6px; }
.sec-desc { font-size: 13.5px; color: var(--ink-soft); line-height: 1.7; margin-bottom: 22px; max-width: 760px; }

.card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 22px 22px;
  height: 100%;
}
.metric-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 20px 20px;
  text-align: left;
  height: 100%;
  position: relative;
  overflow: hidden;
}
.metric-card::before {
  content: '';
  position: absolute; top: 0; left: 0; width: 4px; height: 100%;
  background: var(--accent, var(--teal));
}
.metric-eyebrow {
  font-size: 11px; font-weight: 700; color: var(--ink-soft);
  letter-spacing: .6px; text-transform: uppercase; margin-bottom: 10px;
}
.metric-val { font-family: 'Fraunces', serif; font-size: 32px; font-weight: 700; color: var(--forest); line-height: 1; }
.metric-sub { font-size: 12px; color: var(--ink-soft); margin-top: 8px; line-height: 1.5; }
.metric-delta {
  display: inline-block; margin-top: 8px;
  font-size: 11.5px; font-weight: 600; padding: 2px 9px; border-radius: 10px;
}

.box {
  border-radius: 13px; padding: 16px 20px; margin: 10px 0;
  font-size: 13.5px; line-height: 1.7; border: 1px solid;
}
.box-teal { background: var(--teal-soft); border-color: rgba(45,139,114,.22); color: #143228; }
.box-terracotta { background: var(--terracotta-soft); border-color: rgba(201,104,59,.25); color: #5C2C14; }
.box-gold { background: var(--gold-soft); border-color: rgba(201,154,46,.28); color: #5A4310; }
.box b { color: inherit; }

.faktor-chip {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 4px 12px; border-radius: 20px;
  font-size: 11.5px; font-weight: 600;
  border: 1px solid;
}
.faktor-dot { width: 7px; height: 7px; border-radius: 50%; }

.kab-card {
  background: var(--card); border: 1px solid var(--line);
  border-radius: 13px; padding: 16px 18px; margin-bottom: 10px;
  transition: border-color .15s;
}
.kab-card:hover { border-color: var(--teal); }
.kab-rank {
  font-family: 'Fraunces', serif; font-size: 13px; font-weight: 700;
  color: var(--ink-soft); min-width: 28px;
}
.kab-name { font-weight: 700; font-size: 14.5px; color: var(--forest); }
.kab-prov { font-size: 11.5px; color: var(--ink-soft); }

.sb-eyebrow {
  font-size: 10.5px; font-weight: 700; color: #8B8270;
  letter-spacing: 1px; text-transform: uppercase; margin: 4px 0 8px;
}
.sb-card {
  background: var(--card); border: 1px solid var(--line);
  border-radius: 11px; padding: 13px 14px; font-size: 12px; color: var(--ink-soft);
  line-height: 1.7; margin-bottom: 4px;
}

.legend-row { display: flex; align-items: center; gap: 8px; font-size: 12px; color: var(--ink-soft); margin-bottom: 6px; }
.legend-dot { width: 11px; height: 11px; border-radius: 50%; flex-shrink: 0; }

hr.divider { border: none; border-top: 1px solid var(--line); margin: 36px 0 26px; }
[data-testid="stDataFrame"] { background: transparent !important; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--cream); }
::-webkit-scrollbar-thumb { background: #D6CBB5; border-radius: 3px; }

div[data-baseweb="tab-list"] { gap: 4px; }
button[data-baseweb="tab"] {
  font-family: 'Inter', sans-serif; font-weight: 600; font-size: 13.5px;
  color: var(--ink-soft);
}
button[data-baseweb="tab"][aria-selected="true"] { color: var(--forest); }
</style>
""", unsafe_allow_html=True)


# LOAD DATA
df, missing_df = load_data()
prov_summary = get_province_summary(df)
faktor_summary = get_faktor_summary(df)

BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        family="Inter",
        color="#6B6256",
        size=12
    )
)


# TOP BAR
st.markdown("""
<div class="topbar">
  <div class="topbar-brand">
    <div class="topbar-mark">PS</div>
    <div>
      <div class="topbar-name">Precision Stunting Policy</div>
      <div class="topbar-tag">Dashboard Riset Berbasis GWRF</div>
    </div>
  </div>
  <div class="topbar-pill">404 Kabupaten / Kota Dianalisis</div>
</div>
""", unsafe_allow_html=True)


# SIDEBAR
with st.sidebar:
    st.markdown("<div class='sb-eyebrow'>Navigasi</div>", unsafe_allow_html=True)
    page = st.radio(
        label="nav",
        options=[
            "Ringkasan",
            "Peta Sebaran Stunting",
            "Faktor Dominan",
            "Prioritas Intervensi",
            "Perbandingan Model",
            "Tentang Metodologi",
        ],
        label_visibility="collapsed",
    )

    st.markdown("<hr style='border-color:#E7DFD0;margin:18px 0;'>", unsafe_allow_html=True)
    st.markdown("<div class='sb-eyebrow'>Tentang Riset</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='sb-card'>
      <b style='color:#1B4332;'>Precision Stunting Policy</b><br>
      Prioritas intervensi penurunan stunting berbasis Geographically Weighted
      Random Forest (GWRF) pada tingkat kabupaten/kota di Indonesia.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sb-eyebrow' style='margin-top:14px;'>Cakupan Data</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='sb-card'>
      404 dari 514 kabupaten/kota (78,6%) memiliki data lengkap dan dianalisis.
      Sisanya ditandai sebagai data tidak tersedia pada peta.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sb-eyebrow' style='margin-top:14px;'>Variabel Penelitian</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='sb-card'>
      <b>Y</b> - Persentase stunting<br>
      <b>X1</b> - Persalinan tidak di faskes<br>
      <b>X2</b> - Persentase penduduk miskin<br>
      <b>X3</b> - Konsumsi protein per kapita<br>
      <b>X4</b> - Konsumsi pangan hewani<br>
      <b>X5</b> - Rata-rata lama sekolah
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='margin-top:16px;padding:11px 13px;background:#E3F1EC;
                border:1px solid rgba(45,139,114,.2);border-radius:10px;
                font-size:11px;color:#1B4332;line-height:1.6;'>
      Dashboard ini disusun sebagai media visualisasi hasil penelitian akademik
      untuk mendukung penyusunan kebijakan penurunan stunting yang lebih tepat sasaran.
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# PAGE 1 - RINGKASAN
# ============================================================================
if page == "Ringkasan":
    st.markdown("""
    <div class="hero">
      <div class="hero-eyebrow">Riset Kebijakan Kesehatan Spasial</div>
      <div class="hero-title">
        Precision Stunting Policy:<br>
        Prioritas Intervensi Berbasis <em>Geographically Weighted Random Forest</em>
      </div>
      <div class="hero-sub">
        Setiap wilayah punya akar masalah berbeda. Dashboard ini memetakan sebaran
        stunting di 404 kabupaten/kota Indonesia dan mengidentifikasi faktor dominan
        yang spesifik untuk masing-masing wilayah, sebagai dasar perumusan kebijakan
        yang lebih tepat sasaran.
      </div>
      <div class="hero-stats">
        <div>
          <div class="hero-stat-val">404</div>
          <div class="hero-stat-lbl">Kabupaten/Kota Dianalisis</div>
        </div>
        <div>
          <div class="hero-stat-val">34</div>
          <div class="hero-stat-lbl">Provinsi Tercakup</div>
        </div>
        <div>
          <div class="hero-stat-val">5</div>
          <div class="hero-stat-lbl">Variabel Prediktor</div>
        </div>
        <div>
          <div class="hero-stat-val">0,203</div>
          <div class="hero-stat-lbl">R&sup2; Model GWRF</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sec-eyebrow'>Gambaran Umum</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-title'>Statistik Kunci Stunting Nasional</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-desc'>Ringkasan kondisi stunting dari 404 kabupaten/kota yang berhasil dianalisis dalam penelitian ini.</div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        (c1, "teal", "Rata-rata Stunting", f"{df['stunting'].mean():.1f}%",
         f"Median {df['stunting'].median():.1f}% &middot; rentang {df['stunting'].min():.1f}-{df['stunting'].max():.1f}%"),
        (c2, "terracotta", "Wilayah Prioritas Tinggi", f"{(df['kategori_stunting'].isin(['Tinggi','Sangat Tinggi'])).sum()}",
         f"{(df['kategori_stunting'].isin(['Tinggi','Sangat Tinggi'])).sum()/len(df)*100:.0f}% dari total kabupaten/kota dianalisis"),
        (c3, "gold", "Faktor Dominan Teratas", "RLS",
         f"{(df['faktor_dominan']=='RLS').sum()} kabupaten/kota ({(df['faktor_dominan']=='RLS').sum()/len(df)*100:.0f}%)"),
        (c4, "forest", "Performa Model Terbaik", "GWRF",
         "R&sup2; 0,203 &middot; mengungguli OLS dan Random Forest global"),
    ]
    accent_map = {"teal": "#2D8B72", "terracotta": "#C9683B", "gold": "#C99A2E", "forest": "#1B4332"}
    for col, accent, lbl, val, sub in metrics:
        with col:
            st.markdown(f"""
            <div class='metric-card' style='--accent:{accent_map[accent]};'>
              <div class='metric-eyebrow'>{lbl}</div>
              <div class='metric-val'>{val}</div>
              <div class='metric-sub'>{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns([1.3, 1], gap="large")

    with col_a:
        st.markdown("<div class='sec-title' style='font-size:18px;'>Distribusi Kategori Tingkat Stunting</div>", unsafe_allow_html=True)
        cat_counts = df['kategori_stunting'].value_counts().reindex(KATEGORI_ORDER).fillna(0)
        fig = go.Figure(go.Bar(
            x=cat_counts.values, y=cat_counts.index, orientation="h",
            marker=dict(color=[KATEGORI_COLORS[k] for k in cat_counts.index]),
            text=[f"  {int(v)} kab/kota" for v in cat_counts.values],
            textposition="outside",
            textfont=dict(size=12, color="#6B6256"),
            hovertemplate="<b>%{y}</b><br>%{x} kabupaten/kota<extra></extra>",
        ))
        fig.update_layout(
            **BASE_LAYOUT, height=260,
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, tickfont=dict(size=12.5, color="#2B2620")),
            bargap=0.35,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("""
        <div class="legend-row" style="margin-top:6px;">
          <span style="font-size:11.5px;">Kategori mengikuti ambang prevalensi Kemenkes: Rendah &lt;10%, Sedang 10-19,9%, Tinggi 20-29,9%, Sangat Tinggi &ge;30%</span>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("<div class='sec-title' style='font-size:18px;'>Sebaran Faktor Dominan</div>", unsafe_allow_html=True)
        fig2 = go.Figure(go.Pie(
            labels=faktor_summary['faktor'], values=faktor_summary['jumlah'],
            hole=0.58,
            marker=dict(colors=[FAKTOR_COLORS[f] for f in faktor_summary['faktor']],
                       line=dict(color="#FAF6EF", width=3)),
            textinfo="percent",
            textfont=dict(size=11, color="white"),
            hovertemplate="<b>%{label}</b><br>%{value} kab/kota (%{percent})<extra></extra>",
        ))
        fig2.add_annotation(text="<b>404</b><br>kab/kota", x=0.5, y=0.5, showarrow=False,
                            font=dict(size=15, color="#1B4332", family="Fraunces"))
        fig2.update_layout(**BASE_LAYOUT, height=260, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    st.markdown(f"""
    <div class='box box-teal'>
      <b>Temuan Utama:</b> Faktor dominan penyebab stunting berbeda-beda antarwilayah.
      <b>Rata-rata Lama Sekolah (RLS)</b> menjadi faktor paling dominan di
      {(df['faktor_dominan']=='RLS').sum()} kabupaten/kota (48,3%), diikuti
      <b>Kemiskinan</b> di {(df['faktor_dominan']=='Kemiskinan').sum()} wilayah (29,7%).
      Temuan ini menegaskan pentingnya pendekatan kebijakan yang disesuaikan dengan
      konteks lokal, bukan kebijakan satu ukuran untuk semua wilayah.
    </div>
    <div class='box box-gold'>
      <b>Mengapa GWRF?</b> Stunting memiliki karakteristik spasial - wilayah yang
      berdekatan cenderung memiliki pola serupa, namun faktor penyebab dominannya
      bisa sangat berbeda antarwilayah. Geographically Weighted Random Forest (GWRF)
      menangkap heterogenitas spasial ini, sesuatu yang tidak dapat dilakukan oleh
      model global seperti OLS atau Random Forest konvensional.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='sec-eyebrow'>Konteks Wilayah</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-title'>10 Provinsi dengan Rata-rata Stunting Tertinggi</div>", unsafe_allow_html=True)

    top10_prov = prov_summary.head(10).sort_values('stunting_mean')
    fig3 = go.Figure(go.Bar(
        x=top10_prov['stunting_mean'], y=top10_prov['provinsi'], orientation="h",
        marker=dict(
            color=top10_prov['stunting_mean'],
            colorscale=[[0, "#E8B341"], [0.5, "#D97B47"], [1, "#B8443A"]],
            line=dict(width=0),
        ),
        text=[f"  {v:.1f}%" for v in top10_prov['stunting_mean']],
        textposition="outside",
        textfont=dict(size=12, color="#2B2620"),
        hovertemplate="<b>%{y}</b><br>Rata-rata stunting: %{x:.1f}%<extra></extra>",
    ))
    fig3.update_layout(
        **BASE_LAYOUT, height=380,
        xaxis=dict(showgrid=True, gridcolor="#F0EAE0", zeroline=False, title="Rata-rata Persentase Stunting"),
        yaxis=dict(showgrid=False, tickfont=dict(size=12, color="#2B2620")),
        bargap=0.3,
    )
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})


# ============================================================================
# PAGE 2 - PETA SEBARAN STUNTING
# ============================================================================
elif page == "Peta Sebaran Stunting":
    st.markdown("<div class='sec-eyebrow'>Visualisasi Spasial</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-title'>Peta Sebaran Stunting Seluruh Indonesia</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='sec-desc'>
      Peta menampilkan seluruh 514 kabupaten/kota di Indonesia. Wilayah berwarna menunjukkan
      kabupaten/kota dengan data lengkap yang dianalisis (404 wilayah), sementara wilayah
      abu-abu menandai kabupaten/kota dengan data tidak tersedia (110 wilayah) akibat
      keterbatasan data pada tahap pengumpulan.
    </div>
    """, unsafe_allow_html=True)

    map_col, control_col = st.columns([3, 1], gap="large")

    with control_col:
        st.markdown("<div style='font-size:12.5px;font-weight:700;color:#1B4332;margin-bottom:10px;'>FILTER PETA</div>", unsafe_allow_html=True)
        kategori_filter = st.multiselect(
            "Kategori tingkat stunting",
            options=KATEGORI_ORDER,
            default=KATEGORI_ORDER,
        )
        show_missing = st.checkbox("Tampilkan wilayah data tidak tersedia", value=True)
        prov_options = ["Semua Provinsi"] + sorted(df['provinsi'].unique().tolist())
        prov_filter = st.selectbox("Provinsi", options=prov_options)

        st.markdown("<div style='font-size:12.5px;font-weight:700;color:#1B4332;margin:18px 0 10px;'>LEGENDA</div>", unsafe_allow_html=True)
        for kat in KATEGORI_ORDER:
            st.markdown(f"""
            <div class="legend-row">
              <div class="legend-dot" style="background:{KATEGORI_COLORS[kat]};"></div>
              <span>{kat}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="legend-row">
          <div class="legend-dot" style="background:{KATEGORI_COLORS['Data Tidak Tersedia']};"></div>
          <span>Data Tidak Tersedia</span>
        </div>
        """, unsafe_allow_html=True)

    with map_col:
        plot_df = df[df['kategori_stunting'].isin(kategori_filter)].copy()
        if prov_filter != "Semua Provinsi":
            plot_df = plot_df[plot_df['provinsi'] == prov_filter]
            missing_plot = missing_df[missing_df['province_name'] == prov_filter]
        else:
            missing_plot = missing_df

        fig = go.Figure()

        if show_missing and len(missing_plot) > 0:
            fig.add_trace(go.Scattergeo(
                lon=missing_plot['longitude'], lat=missing_plot['latitude'],
                mode="markers",
                marker=dict(size=6, color=KATEGORI_COLORS['Data Tidak Tersedia'],
                           opacity=0.55, line=dict(width=0)),
                name="Data Tidak Tersedia",
                text=missing_plot['display_name'] + " - Data tidak tersedia",
                hovertemplate="<b>%{text}</b><extra></extra>",
            ))

        for kat in KATEGORI_ORDER:
            sub = plot_df[plot_df['kategori_stunting'] == kat]
            if len(sub) == 0:
                continue
            fig.add_trace(go.Scattergeo(
                lon=sub['lon'], lat=sub['lat'],
                mode="markers",
                marker=dict(
                    size=np.clip(sub['stunting'] * 0.9, 6, 26),
                    color=KATEGORI_COLORS[kat],
                    opacity=0.85,
                    line=dict(width=0.8, color="white"),
                ),
                name=kat,
                text=sub['kab_kota'] + ", " + sub['provinsi'] + "<br>Stunting: " + sub['stunting'].astype(str) + "%" +
                     "<br>Faktor dominan: " + sub['faktor_dominan'],
                hovertemplate="<b>%{text}</b><extra></extra>",
            ))

        fig.update_geos(
            scope="asia",
            center=dict(lon=118, lat=-2.5),
            projection_scale=4.6,
            showland=True, landcolor="#F2EBDD",
            showocean=True, oceancolor="#E8F0EC",
            showcountries=True, countrycolor="#D6CBB5",
            showcoastlines=True, coastlinecolor="#C9C2B5",
            showframe=False,
            bgcolor="rgba(0,0,0,0)",
        )
        fig.update_layout(
        **BASE_LAYOUT,
        height=560,
        legend=...,
        margin=dict(t=10, b=10, l=0, r=0),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("""
        <div style='font-size:11.5px;color:#8B8270;margin-top:-6px;'>
          Ukuran titik merepresentasikan besarnya persentase stunting. Arahkan kursor ke
          titik untuk melihat detail kabupaten/kota.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='sec-title' style='font-size:18px;'>Rata-rata Stunting per Provinsi</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-desc'>Perbandingan menyeluruh tingkat stunting rata-rata di seluruh provinsi yang tercakup dalam data penelitian.</div>", unsafe_allow_html=True)

    prov_sorted = prov_summary.sort_values('stunting_mean')
    fig4 = go.Figure(go.Bar(
        x=prov_sorted['stunting_mean'], y=prov_sorted['provinsi'], orientation="h",
        marker=dict(
            color=prov_sorted['stunting_mean'],
            colorscale=[[0, "#7FB69E"], [0.4, "#E8B341"], [0.7, "#D97B47"], [1, "#B8443A"]],
        ),
        text=[f" {v:.1f}%" for v in prov_sorted['stunting_mean']],
        textposition="outside",
        textfont=dict(size=10.5, color="#2B2620"),
        hovertemplate="<b>%{y}</b><br>Rata-rata: %{x:.1f}%<extra></extra>",
    ))
    fig4.update_layout(
        **BASE_LAYOUT, height=760,
        xaxis=dict(showgrid=True, gridcolor="#F0EAE0", zeroline=False, title="Rata-rata Persentase Stunting"),
        yaxis=dict(showgrid=False, tickfont=dict(size=10.5, color="#2B2620")),
        bargap=0.25,
    )
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})


# ============================================================================
# PAGE 3 - FAKTOR DOMINAN
# ============================================================================
elif page == "Faktor Dominan":
    st.markdown("<div class='sec-eyebrow'>Local Feature Importance</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-title'>Faktor Dominan Penyebab Stunting per Wilayah</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='sec-desc'>
      GWRF menghasilkan estimasi pentingnya variabel (feature importance) secara lokal untuk
      setiap kabupaten/kota. Artinya, faktor yang paling berpengaruh terhadap stunting dapat
      berbeda dari satu wilayah ke wilayah lain - inilah inti dari pendekatan "precision policy".
    </div>
    """, unsafe_allow_html=True)

    fc1, fc2, fc3, fc4, fc5 = st.columns(5)
    faktor_icons_col = [fc1, fc2, fc3, fc4, fc5]
    for col, (_, row) in zip(faktor_icons_col, faktor_summary.iterrows()):
        color = FAKTOR_COLORS[row['faktor']]
        with col:
            st.markdown(f"""
            <div class='metric-card' style='--accent:{color};'>
              <div class='metric-eyebrow'>{row['faktor']}</div>
              <div class='metric-val' style='font-size:26px;'>{int(row['jumlah'])}</div>
              <div class='metric-sub'>{row['persen']}% dari total wilayah</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Eksplorasi per Wilayah", "Sebaran Faktor per Provinsi", "Pentingnya Variabel Global"])

    with tab1:
        st.markdown("<div style='font-size:13px;color:#6B6256;margin-bottom:14px;'>Pilih kabupaten/kota untuk melihat rincian local feature importance hasil model GWRF.</div>", unsafe_allow_html=True)
        kab_list = sorted(df['kab_kota'] + " - " + df['provinsi'])
        selected = st.selectbox("Cari kabupaten/kota", options=kab_list, index=0, label_visibility="collapsed")
        kab_name = selected.split(" - ")[0]
        row = df[df['kab_kota'] == kab_name].iloc[0]

        detail_col, chart_col = st.columns([1, 1.3], gap="large")
        with detail_col:
            dom_color = FAKTOR_COLORS[row['faktor_dominan']]
            st.markdown(f"""
            <div class='card'>
              <div style='font-family:Fraunces,serif;font-size:21px;font-weight:700;color:#1B4332;'>{row['kab_kota']}</div>
              <div style='font-size:12.5px;color:#6B6256;margin-bottom:16px;'>{row['provinsi']}</div>
              <div style='display:flex;gap:10px;margin-bottom:18px;flex-wrap:wrap;'>
                <span class='faktor-chip' style='border-color:{KATEGORI_COLORS[row["kategori_stunting"]]};color:{KATEGORI_COLORS[row["kategori_stunting"]]};'>
                  <span class='faktor-dot' style='background:{KATEGORI_COLORS[row["kategori_stunting"]]};'></span>
                  Stunting {row['kategori_stunting']}
                </span>
              </div>
              <div style='font-size:30px;font-family:Fraunces,serif;font-weight:700;color:#1B4332;'>{row['stunting']:.1f}%</div>
              <div style='font-size:12px;color:#6B6256;margin-bottom:18px;'>Persentase stunting wilayah ini</div>
              <hr style='border-color:#E7DFD0;margin:14px 0;'>
              <div style='font-size:12px;font-weight:700;color:#8B8270;letter-spacing:.5px;text-transform:uppercase;margin-bottom:8px;'>Faktor Dominan</div>
              <div style='display:flex;align-items:center;gap:8px;'>
                <div style='width:10px;height:10px;border-radius:50%;background:{dom_color};'></div>
                <span style='font-weight:700;font-size:15px;color:#2B2620;'>{row['faktor_dominan']}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

        with chart_col:
            fi_cols = ['fi_RLS', 'fi_Kemiskinan', 'fi_Pangan Hewani', 'fi_Konsumsi Protein', 'fi_Melahirkan Tidak di Faskes']
            fi_labels = ['RLS', 'Kemiskinan', 'Pangan Hewani', 'Konsumsi Protein', 'Melahirkan Tidak di Faskes']
            fi_vals = [row[c] * 100 for c in fi_cols]
            sorted_pairs = sorted(zip(fi_labels, fi_vals), key=lambda x: x[1])
            labels_sorted = [p[0] for p in sorted_pairs]
            vals_sorted = [p[1] for p in sorted_pairs]
            colors_sorted = [FAKTOR_COLORS[l] for l in labels_sorted]

            fig5 = go.Figure(go.Bar(
                x=vals_sorted, y=labels_sorted, orientation="h",
                marker=dict(color=colors_sorted),
                text=[f" {v:.1f}%" for v in vals_sorted],
                textposition="outside",
                textfont=dict(size=12, color="#2B2620"),
                hovertemplate="<b>%{y}</b><br>Kontribusi: %{x:.1f}%<extra></extra>",
            ))
            fig5.update_layout(
                **BASE_LAYOUT, height=300,
                title=dict(text="Local Feature Importance", font=dict(size=13.5, color="#1B4332", family="Fraunces")),
                xaxis=dict(showgrid=True, gridcolor="#F0EAE0", zeroline=False, title="Kontribusi (%)"),
                yaxis=dict(showgrid=False, tickfont=dict(size=12, color="#2B2620")),
                bargap=0.35,
            )
            st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})

            st.markdown(f"""
            <div class='box box-teal' style='margin-top:0;'>
              Di <b>{row['kab_kota']}</b>, faktor <b>{row['faktor_dominan']}</b> memberikan kontribusi
              paling besar terhadap tingkat stunting lokal. Ini mengindikasikan intervensi yang
              menyasar faktor tersebut berpotensi memberikan dampak penurunan stunting paling signifikan
              di wilayah ini, dibandingkan pendekatan yang seragam secara nasional.
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown("<div style='font-size:13px;color:#6B6256;margin-bottom:14px;'>Komposisi faktor dominan pada setiap provinsi, diurutkan berdasarkan jumlah kabupaten/kota.</div>", unsafe_allow_html=True)

        cross = pd.crosstab(df['provinsi'], df['faktor_dominan'])
        order_cols = ['RLS', 'Kemiskinan', 'Pangan Hewani', 'Konsumsi Protein', 'Melahirkan Tidak di Faskes']
        cross = cross.reindex(columns=[c for c in order_cols if c in cross.columns], fill_value=0)
        cross['total'] = cross.sum(axis=1)
        cross = cross.sort_values('total', ascending=True)

        fig6 = go.Figure()
        for faktor in order_cols:
            if faktor not in cross.columns:
                continue
            fig6.add_trace(go.Bar(
                y=cross.index, x=cross[faktor], orientation="h",
                name=faktor, marker=dict(color=FAKTOR_COLORS[faktor]),
                hovertemplate=f"<b>%{{y}}</b><br>{faktor}: %{{x}}<extra></extra>",
            ))
        fig6.update_layout(
            **BASE_LAYOUT, height=820, barmode="stack",
            xaxis=dict(showgrid=True, gridcolor="#F0EAE0", zeroline=False, title="Jumlah Kabupaten/Kota"),
            yaxis=dict(showgrid=False, tickfont=dict(size=10.5, color="#2B2620")),
            legend=dict(orientation="h", yanchor="bottom", y=1.01, font=dict(size=11.5)),
            bargap=0.25,
        )
        st.plotly_chart(fig6, use_container_width=True, config={"displayModeBar": False})

    with tab3:
        st.markdown("""
        <div class='sec-desc' style='margin-bottom:18px;'>
          Selain local feature importance, model Random Forest global memberikan gambaran
          pentingnya variabel secara umum di seluruh Indonesia (tanpa mempertimbangkan
          variasi spasial). Perbandingan ini membantu memahami perbedaan antara pendekatan
          global dan lokal.
        </div>
        """, unsafe_allow_html=True)

        global_fi = pd.DataFrame({
            "variabel": ["Kemiskinan (%)", "RLS", "Pangan Hewani", "Konsumsi Protein", "Melahirkan Tidak di Faskes"],
            "importance": [0.284, 0.253, 0.220, 0.135, 0.108],
        }).sort_values("importance")

        color_lookup = {
            "Kemiskinan (%)": FAKTOR_COLORS["Kemiskinan"],
            "RLS": FAKTOR_COLORS["RLS"],
            "Pangan Hewani": FAKTOR_COLORS["Pangan Hewani"],
            "Konsumsi Protein": FAKTOR_COLORS["Konsumsi Protein"],
            "Melahirkan Tidak di Faskes": FAKTOR_COLORS["Melahirkan Tidak di Faskes"],
        }

        fig7 = go.Figure(go.Bar(
            x=global_fi['importance'], y=global_fi['variabel'], orientation="h",
            marker=dict(color=[color_lookup[v] for v in global_fi['variabel']]),
            text=[f" {v:.1%}" for v in global_fi['importance']],
            textposition="outside",
            textfont=dict(size=12, color="#2B2620"),
            hovertemplate="<b>%{y}</b><br>Importance: %{x:.1%}<extra></extra>",
        ))
        fig7.update_layout(
            **BASE_LAYOUT, height=340,
            xaxis=dict(showgrid=True, gridcolor="#F0EAE0", zeroline=False, title="Feature Importance (Random Forest Global)"),
            yaxis=dict(showgrid=False, tickfont=dict(size=12.5, color="#2B2620")),
            bargap=0.35,
        )
        st.plotly_chart(fig7, use_container_width=True, config={"displayModeBar": False})

        st.markdown("""
        <div class='box box-gold'>
          <b>Catatan Penting:</b> Pada model Random Forest global, <b>Kemiskinan</b> dan
          <b>RLS</b> menjadi dua variabel paling penting secara nasional. Namun, hasil GWRF
          menunjukkan bahwa secara lokal, RLS justru menjadi faktor dominan di hampir separuh
          wilayah (48,3%) - menggarisbawahi bahwa pentingnya variabel secara global tidak selalu
          mencerminkan kondisi spesifik tiap wilayah.
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# PAGE 4 - PRIORITAS INTERVENSI
# ============================================================================
elif page == "Prioritas Intervensi":
    st.markdown("<div class='sec-eyebrow'>Rekomendasi Kebijakan</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-title'>Peringkat Prioritas Intervensi Penurunan Stunting</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='sec-desc'>
      Skor prioritas dihitung dari kombinasi tertimbang lima indikator: persentase stunting (40%),
      tingkat kemiskinan (20%), rata-rata lama sekolah (15%), konsumsi pangan hewani (15%), dan
      persalinan tidak di fasilitas kesehatan (10%). Semakin tinggi skor, semakin mendesak
      kebutuhan intervensi di wilayah tersebut.
    </div>
    """, unsafe_allow_html=True)

    f1, f2 = st.columns([1, 1])
    with f1:
        prov_filter2 = st.selectbox(
            "Filter berdasarkan provinsi",
            options=["Semua Provinsi"] + sorted(df['provinsi'].unique().tolist()),
            key="prov_filter_priority",
        )
    with f2:
        faktor_filter = st.selectbox(
            "Filter berdasarkan faktor dominan",
            options=["Semua Faktor"] + sorted(df['faktor_dominan'].unique().tolist()),
            key="faktor_filter_priority",
        )

    filtered = df.copy()
    if prov_filter2 != "Semua Provinsi":
        filtered = filtered[filtered['provinsi'] == prov_filter2]
    if faktor_filter != "Semua Faktor":
        filtered = filtered[filtered['faktor_dominan'] == faktor_filter]

    top20 = filtered.sort_values('skor_prioritas_100', ascending=False).head(20)

    st.markdown(f"<div style='font-size:12.5px;color:#8B8270;margin:18px 0 14px;'>Menampilkan {len(top20)} dari {len(filtered)} kabupaten/kota dengan skor prioritas tertinggi</div>", unsafe_allow_html=True)

    for _, row in top20.iterrows():
        dom_color = FAKTOR_COLORS[row['faktor_dominan']]
        kat_color = KATEGORI_COLORS[row['kategori_stunting']]
        st.markdown(f"""
        <div class='kab-card'>
          <div style='display:flex;align-items:center;gap:16px;'>
            <div class='kab-rank'>#{int(row['rank_prioritas'])}</div>
            <div style='flex:1;'>
              <div class='kab-name'>{row['kab_kota']}</div>
              <div class='kab-prov'>{row['provinsi']}</div>
            </div>
            <div style='text-align:center;min-width:90px;'>
              <div style='font-family:Fraunces,serif;font-size:18px;font-weight:700;color:{kat_color};'>{row['stunting']:.1f}%</div>
              <div style='font-size:10.5px;color:#8B8270;'>Stunting</div>
            </div>
            <div style='min-width:150px;'>
              <span class='faktor-chip' style='border-color:{dom_color};color:{dom_color};'>
                <span class='faktor-dot' style='background:{dom_color};'></span>
                {row['faktor_dominan']}
              </span>
            </div>
            <div style='min-width:130px;'>
              <div style='background:#F0EAE0;border-radius:100px;height:7px;width:100%;'>
                <div style='background:linear-gradient(90deg,#E8B341,#C9683B);width:{row['skor_prioritas_100']:.0f}%;height:7px;border-radius:100px;'></div>
              </div>
              <div style='font-size:10.5px;color:#8B8270;margin-top:3px;'>Skor prioritas {row['skor_prioritas_100']:.0f}/100</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1.2, 1], gap="large")
    with col_left:
        st.markdown("<div class='sec-title' style='font-size:18px;'>Skor Prioritas vs Tingkat Stunting</div>", unsafe_allow_html=True)
        st.markdown("<div class='sec-desc' style='font-size:12.5px;'>Setiap titik mewakili satu kabupaten/kota. Warna menunjukkan faktor dominan penyebab stunting di wilayah tersebut.</div>", unsafe_allow_html=True)

        fig8 = go.Figure()
        for faktor in df['faktor_dominan'].unique():
            sub = df[df['faktor_dominan'] == faktor]
            fig8.add_trace(go.Scatter(
                x=sub['stunting'], y=sub['skor_prioritas_100'],
                mode="markers", name=faktor,
                marker=dict(color=FAKTOR_COLORS[faktor], size=8, opacity=0.7,
                           line=dict(width=0.5, color="white")),
                text=sub['kab_kota'] + ", " + sub['provinsi'],
                hovertemplate="<b>%{text}</b><br>Stunting: %{x:.1f}%<br>Skor prioritas: %{y:.0f}<extra></extra>",
            ))
        fig8.update_layout(
            **BASE_LAYOUT, height=400,
            xaxis=dict(title="Persentase Stunting (%)", showgrid=True, gridcolor="#F0EAE0", zeroline=False),
            yaxis=dict(title="Skor Prioritas (0-100)", showgrid=True, gridcolor="#F0EAE0", zeroline=False),
            legend=dict(font=dict(size=10.5), orientation="h", yanchor="bottom", y=1.01),
        )
        st.plotly_chart(fig8, use_container_width=True, config={"displayModeBar": False})

    with col_right:
        st.markdown("<div class='sec-title' style='font-size:18px;'>Provinsi dengan Skor Prioritas Tertinggi</div>", unsafe_allow_html=True)
        prov_priority = prov_summary.sort_values('skor_prioritas_mean', ascending=False).head(8).sort_values('skor_prioritas_mean')
        fig9 = go.Figure(go.Bar(
            x=prov_priority['skor_prioritas_mean'], y=prov_priority['provinsi'], orientation="h",
            marker=dict(color="#C9683B", opacity=0.85),
            text=[f" {v:.0f}" for v in prov_priority['skor_prioritas_mean']],
            textposition="outside",
            textfont=dict(size=11.5, color="#2B2620"),
            hovertemplate="<b>%{y}</b><br>Skor rata-rata: %{x:.0f}<extra></extra>",
        ))
        fig9.update_layout(
            **BASE_LAYOUT, height=400,
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, tickfont=dict(size=11, color="#2B2620")),
            bargap=0.35,
        )
        st.plotly_chart(fig9, use_container_width=True, config={"displayModeBar": False})

    st.markdown("""
    <div class='box box-terracotta'>
      <b>Rekomendasi Penggunaan:</b> Skor prioritas ini dirancang sebagai alat bantu awal
      bagi pengambil kebijakan untuk mengidentifikasi wilayah yang memerlukan perhatian segera.
      Kombinasikan dengan analisis faktor dominan pada tab "Faktor Dominan" untuk merancang
      intervensi yang sesuai dengan akar masalah di tiap wilayah - bukan pendekatan generik
      yang sama untuk semua kabupaten/kota.
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# PAGE 5 - PERBANDINGAN MODEL
# ============================================================================
elif page == "Perbandingan Model":
    st.markdown("<div class='sec-eyebrow'>Evaluasi Model</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-title'>Perbandingan Performa: OLS vs Random Forest vs GWRF</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='sec-desc'>
      Tiga model dibandingkan untuk memprediksi persentase stunting: regresi linear klasik
      (OLS), Random Forest global, dan Geographically Weighted Random Forest (GWRF) yang
      mempertimbangkan heterogenitas spasial. Evaluasi dilakukan menggunakan koefisien
      determinasi (R&sup2;) dan Root Mean Squared Error (RMSE).
    </div>
    """, unsafe_allow_html=True)

    model_data = pd.DataFrame({
        "model": ["OLS (Regresi Linear)", "Random Forest Global", "GWRF (Geographically Weighted RF)"],
        "r2": [0.146, 0.182, 0.203],
        "rmse": [5.474, 5.255, 5.036],
        "color": ["#9C8B6F", "#5B7DB1", "#2D8B72"],
    })

    mc1, mc2, mc3 = st.columns(3)
    for col, (_, row) in zip([mc1, mc2, mc3], model_data.iterrows()):
        is_best = row['model'].startswith("GWRF")
        badge = "<span style='background:#E3F1EC;color:#1B4332;font-size:10.5px;font-weight:700;padding:2px 9px;border-radius:9px;margin-left:8px;'>TERBAIK</span>" if is_best else ""
        with col:
            st.markdown(f"""
            <div class='metric-card' style='--accent:{row["color"]};'>
              <div class='metric-eyebrow'>{row['model']}{badge}</div>
              <div style='display:flex;gap:24px;margin-top:10px;'>
                <div>
                  <div class='metric-val' style='font-size:26px;'>{row['r2']:.3f}</div>
                  <div class='metric-sub'>R&sup2;</div>
                </div>
                <div>
                  <div class='metric-val' style='font-size:26px;'>{row['rmse']:.2f}</div>
                  <div class='metric-sub'>RMSE</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns(2, gap="large")
    with chart_col1:
        st.markdown("<div class='sec-title' style='font-size:17px;'>Perbandingan R&sup2;</div>", unsafe_allow_html=True)
        fig10 = go.Figure(go.Bar(
            x=model_data['model'], y=model_data['r2'],
            marker=dict(color=model_data['color']),
            text=[f"{v:.3f}" for v in model_data['r2']],
            textposition="outside",
            textfont=dict(size=13, color="#2B2620"),
            hovertemplate="<b>%{x}</b><br>R&sup2;: %{y:.3f}<extra></extra>",
        ))
        fig10.update_layout(
            **BASE_LAYOUT, height=340,
            xaxis=dict(showgrid=False, tickfont=dict(size=10.5, color="#2B2620")),
            yaxis=dict(showgrid=True, gridcolor="#F0EAE0", zeroline=False, range=[0, 0.26]),
            bargap=0.45,
        )
        st.plotly_chart(fig10, use_container_width=True, config={"displayModeBar": False})

    with chart_col2:
        st.markdown("<div class='sec-title' style='font-size:17px;'>Perbandingan RMSE</div>", unsafe_allow_html=True)
        fig11 = go.Figure(go.Bar(
            x=model_data['model'], y=model_data['rmse'],
            marker=dict(color=model_data['color']),
            text=[f"{v:.2f}" for v in model_data['rmse']],
            textposition="outside",
            textfont=dict(size=13, color="#2B2620"),
            hovertemplate="<b>%{x}</b><br>RMSE: %{y:.2f}<extra></extra>",
        ))
        fig11.update_layout(
            **BASE_LAYOUT, height=340,
            xaxis=dict(showgrid=False, tickfont=dict(size=10.5, color="#2B2620")),
            yaxis=dict(showgrid=True, gridcolor="#F0EAE0", zeroline=False, range=[4.8, 5.6]),
            bargap=0.45,
        )
        st.plotly_chart(fig11, use_container_width=True, config={"displayModeBar": False})

    st.markdown("""
    <div class='box box-teal'>
      <b>Interpretasi:</b> GWRF konsisten unggul pada kedua metrik - R&sup2; tertinggi (0,203)
      dan RMSE terendah (5,036). Peningkatan performa dari OLS ke GWRF (R&sup2; naik dari 0,146
      menjadi 0,203, atau peningkatan sekitar 39%) menunjukkan bahwa mempertimbangkan
      heterogenitas spasial dan hubungan non-linear antarvariabel memberikan kemampuan prediksi
      yang lebih baik dibandingkan model klasik.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='sec-title' style='font-size:18px;'>Hasil Uji Asumsi Model OLS</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-desc'>Sebelum membandingkan dengan model machine learning, model OLS diuji asumsi klasiknya untuk memastikan validitas interpretasi.</div>", unsafe_allow_html=True)

    asumsi_data = pd.DataFrame({
        "Uji Asumsi": ["Normalitas Residual (Jarque-Bera)", "Multikolinearitas (VIF)", "Heteroskedastisitas (Breusch-Pagan)", "Autokorelasi Spasial (Moran's I)"],
        "Hasil": ["Residual tidak berdistribusi normal", "Tidak ada multikolinearitas serius (VIF < 10)", "Terindikasi heteroskedastisitas", "Terdapat autokorelasi spasial signifikan"],
        "Implikasi": [
            "Mendukung penggunaan model non-parametrik seperti Random Forest",
            "Variabel prediktor relatif independen satu sama lain",
            "Varians error tidak konstan, memperkuat alasan penggunaan model robust",
            "Mengonfirmasi relevansi pendekatan spasial seperti GWRF",
        ],
    })
    st.dataframe(
        asumsi_data, use_container_width=True, hide_index=True,
        column_config={
            "Uji Asumsi": st.column_config.TextColumn("Uji Asumsi", width="medium"),
            "Hasil": st.column_config.TextColumn("Hasil", width="medium"),
            "Implikasi": st.column_config.TextColumn("Implikasi", width="large"),
        },
    )

    st.markdown("""
    <div class='box box-gold'>
      <b>Mengapa Hasil Uji Asumsi Penting:</b> Pelanggaran asumsi normalitas, heteroskedastisitas,
      dan terutama autokorelasi spasial pada model OLS menjadi justifikasi kuat untuk beralih ke
      pendekatan yang lebih fleksibel dan mempertimbangkan struktur spasial data, yaitu GWRF.
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# PAGE 6 - TENTANG METODOLOGI
# ============================================================================
elif page == "Tentang Metodologi":
    st.markdown("<div class='sec-eyebrow'>Dokumentasi Riset</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-title'>Metodologi Penelitian</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='sec-desc'>
      Precision Stunting Policy menggunakan pendekatan spasial untuk mengidentifikasi
      faktor-faktor yang memengaruhi stunting pada tingkat kabupaten/kota di Indonesia,
      serta menentukan faktor dominan yang spesifik untuk masing-masing wilayah.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sec-title' style='font-size:18px;'>Tujuan Penelitian</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='box box-teal'>
      Mengidentifikasi faktor-faktor yang memengaruhi stunting pada tingkat kabupaten/kota
      di Indonesia, serta menentukan faktor dominan pada masing-masing wilayah sehingga dapat
      digunakan sebagai dasar penyusunan kebijakan penurunan stunting yang lebih tepat sasaran.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='sec-title' style='font-size:18px;'>Alur Penelitian</div>", unsafe_allow_html=True)

    steps = [
        ("1", "Pengumpulan Data", "Data dikumpulkan pada tingkat kabupaten/kota: persentase stunting, persalinan tidak di faskes, kemiskinan, konsumsi protein, pangan hewani, dan rata-rata lama sekolah."),
        ("2", "Pembersihan Data", "Wilayah dengan data tidak lengkap dikeluarkan dari analisis, menghasilkan 404 dari 579 kabupaten/kota dengan data bersih dan siap dianalisis."),
        ("3", "Uji Asumsi OLS", "Model regresi linear klasik diuji asumsinya (normalitas, multikolinearitas, heteroskedastisitas, autokorelasi spasial) sebagai baseline pembanding."),
        ("4", "Pemodelan Random Forest", "Random Forest global diterapkan untuk menangkap hubungan non-linear antarvariabel tanpa mempertimbangkan struktur spasial."),
        ("5", "Pemodelan GWRF", "Geographically Weighted Random Forest diterapkan dengan pembobotan spasial, menghasilkan model lokal untuk setiap kabupaten/kota."),
        ("6", "Local Feature Importance", "Untuk setiap wilayah, dihitung kontribusi relatif masing-masing variabel prediktor guna mengidentifikasi faktor dominan."),
        ("7", "Penyusunan Skor Prioritas", "Hasil model dikombinasikan menjadi skor prioritas intervensi yang mempertimbangkan tingkat keparahan dan faktor risiko di tiap wilayah."),
        ("8", "Visualisasi Dashboard", "Seluruh hasil dirangkum dalam dashboard interaktif untuk mendukung pengambilan keputusan berbasis data oleh pemangku kebijakan."),
    ]
    cols_per_row = 4
    for i in range(0, len(steps), cols_per_row):
        row_cols = st.columns(cols_per_row)
        for col, (num, title, desc) in zip(row_cols, steps[i:i+cols_per_row]):
            with col:
                st.markdown(f"""
                <div class='card' style='margin-bottom:14px;'>
                  <div style='width:30px;height:30px;border-radius:50%;background:#E3F1EC;
                              border:1.5px solid #2D8B72;color:#1B4332;display:flex;
                              align-items:center;justify-content:center;font-family:Fraunces,serif;
                              font-weight:700;font-size:13px;margin-bottom:10px;'>{num}</div>
                  <div style='font-weight:700;font-size:13.5px;color:#1B4332;margin-bottom:6px;'>{title}</div>
                  <div style='font-size:11.5px;color:#6B6256;line-height:1.55;'>{desc}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        st.markdown("<div class='sec-title' style='font-size:18px;'>Variabel Penelitian</div>", unsafe_allow_html=True)
        var_table = pd.DataFrame({
            "Kode": ["Y", "X1", "X2", "X3", "X4", "X5"],
            "Variabel": [
                "Persentase Stunting",
                "Persalinan Tidak di Fasilitas Kesehatan",
                "Persentase Penduduk Miskin",
                "Konsumsi Protein per Kapita",
                "Konsumsi Pangan Hewani",
                "Rata-rata Lama Sekolah (RLS)",
            ],
            "Peran": ["Variabel Target", "Prediktor", "Prediktor", "Prediktor", "Prediktor", "Prediktor"],
        })
        st.dataframe(var_table, use_container_width=True, hide_index=True)

    with col_b:
        st.markdown("<div class='sec-title' style='font-size:18px;'>Cakupan dan Keterbatasan Data</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='box box-gold'>
          <b>Cakupan:</b> 404 dari 514 kabupaten/kota di Indonesia (78,6%) memiliki data
          lengkap pada keenam variabel dan digunakan dalam pemodelan.<br><br>
          <b>Keterbatasan:</b> 110 kabupaten/kota (21,4%) dikeluarkan dari analisis karena
          ketidaklengkapan data pada satu atau lebih variabel, terutama untuk wilayah pemekaran
          baru dan beberapa kabupaten di Papua. Wilayah ini ditandai sebagai "Data Tidak
          Tersedia" pada peta sebaran.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='sec-title' style='font-size:18px;'>Mengapa Geographically Weighted Random Forest?</div>", unsafe_allow_html=True)

    gcol1, gcol2, gcol3 = st.columns(3)
    with gcol1:
        st.markdown("""
        <div class='card'>
          <div style='font-weight:700;color:#1B4332;font-size:14.5px;margin-bottom:8px;'>Heterogenitas Spasial</div>
          <div style='font-size:12.5px;color:#6B6256;line-height:1.65;'>
            Stunting tidak disebabkan oleh faktor yang sama di setiap wilayah. GWRF
            memungkinkan koefisien model bervariasi secara spasial, menangkap perbedaan
            ini secara eksplisit.
          </div>
        </div>
        """, unsafe_allow_html=True)
    with gcol2:
        st.markdown("""
        <div class='card'>
          <div style='font-weight:700;color:#1B4332;font-size:14.5px;margin-bottom:8px;'>Hubungan Non-linear</div>
          <div style='font-size:12.5px;color:#6B6256;line-height:1.65;'>
            Berbeda dari regresi linear, Random Forest dapat menangkap pola hubungan
            kompleks dan interaksi antarvariabel yang sering terjadi dalam fenomena
            sosial-kesehatan seperti stunting.
          </div>
        </div>
        """, unsafe_allow_html=True)
    with gcol3:
        st.markdown("""
        <div class='card'>
          <div style='font-weight:700;color:#1B4332;font-size:14.5px;margin-bottom:8px;'>Kebijakan Tepat Sasaran</div>
          <div style='font-size:12.5px;color:#6B6256;line-height:1.65;'>
            Dengan mengetahui faktor dominan di tiap wilayah, pemangku kebijakan dapat
            merancang program intervensi yang lebih relevan dan efisien dibandingkan
            kebijakan seragam nasional.
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center;padding:24px 0;'>
      <div style='font-family:Fraunces,serif;font-size:16px;font-weight:700;color:#1B4332;margin-bottom:6px;'>
        Precision Stunting Policy
      </div>
      <div style='font-size:12px;color:#8B8270;line-height:1.7;max-width:560px;margin:0 auto;'>
        Prioritas Intervensi Penurunan Stunting Berbasis Geographically Weighted Random Forest
        pada Tingkat Kabupaten/Kota di Indonesia.<br>
        Dashboard dikembangkan menggunakan Streamlit dan Plotly.
      </div>
    </div>
    """, unsafe_allow_html=True)
