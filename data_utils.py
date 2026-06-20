"""
Modul pemuatan dan persiapan data untuk Dashboard Precision Stunting Policy.
Data bersumber dari hasil analisis Geographically Weighted Random Forest (GWRF)
pada 404 kabupaten/kota di Indonesia.
"""

import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "df_final.csv"


VAR_LABELS = {
    "kemiskinan": "Persentase Penduduk Miskin",
    "rls": "Rata-rata Lama Sekolah (RLS)",
    "pangan_hewani": "Konsumsi Pangan Hewani",
    "konsumsi_protein_per_kapita": "Konsumsi Protein per Kapita",
    "melahirkan_tidak_difaskes": "Persalinan Tidak di Faskes",
}

VAR_UNITS = {
    "kemiskinan": "%",
    "rls": "tahun",
    "pangan_hewani": "skor",
    "konsumsi_protein_per_kapita": "gram/hari",
    "melahirkan_tidak_difaskes": "%",
}

FAKTOR_COLORS = {
    "RLS": "#2D8B72",
    "Kemiskinan": "#C9683B",
    "Pangan Hewani": "#E8B341",
    "Konsumsi Protein": "#5B7DB1",
    "Melahirkan Tidak di Faskes": "#9C5B8C",
}

KATEGORI_COLORS = {
    "Rendah": "#7FB69E",
    "Sedang": "#E8B341",
    "Tinggi": "#D97B47",
    "Sangat Tinggi": "#B8443A",
    "Data Tidak Tersedia": "#C9C2B5",
}

KATEGORI_ORDER = ["Rendah", "Sedang", "Tinggi", "Sangat Tinggi"]


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_DIR / "df_final.csv")
    missing = pd.read_csv(DATA_DIR / "missing_regencies.csv")
    return df, missing


@st.cache_data
def get_province_summary(df: pd.DataFrame) -> pd.DataFrame:
    agg = (
        df.groupby("provinsi")
        .agg(
            stunting_mean=("stunting", "mean"),
            n_kab=("kab_kota", "count"),
            skor_prioritas_mean=("skor_prioritas_100", "mean"),
            kemiskinan_mean=("kemiskinan", "mean"),
            rls_mean=("rls", "mean"),
        )
        .reset_index()
        .sort_values("stunting_mean", ascending=False)
    )
    return agg


@st.cache_data
def get_faktor_summary(df: pd.DataFrame) -> pd.DataFrame:
    counts = df["faktor_dominan"].value_counts().reset_index()
    counts.columns = ["faktor", "jumlah"]
    counts["persen"] = (counts["jumlah"] / counts["jumlah"].sum() * 100).round(1)
    order = ["RLS", "Kemiskinan", "Pangan Hewani", "Konsumsi Protein", "Melahirkan Tidak di Faskes"]
    counts["faktor"] = pd.Categorical(counts["faktor"], categories=order, ordered=True)
    counts = counts.sort_values("faktor")
    return counts


def format_number(x, decimals=1):
    return f"{x:,.{decimals}f}".replace(",", "#").replace(".", ",").replace("#", ".")
