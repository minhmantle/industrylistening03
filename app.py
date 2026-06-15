import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json

st.set_page_config(page_title="Mantle Social Listening Dashboard", layout="wide")
st.title("🚀 Mantle Squad - Weekly Social Listening Dashboard")
st.caption(f"Week: {st.text_input('Tuần hiện tại', '2026-W24')} | Cập nhật: {datetime.now().strftime('%d/%m/%Y')}")

# Tabs
tab_upload, tab_ai, tab_rwa, tab_top5, tab_metrics = st.tabs([
    "📥 Upload Data (CSV)", 
    "📊 AI Agents Weekly", 
    "🏦 RWA / Institutional", 
    "🔥 Top 5 Impactful", 
    "📈 Metrics & Alpha"
])

with tab_upload:
    st.header("📥 Upload CSV từ Twitter Web Exporter")
    st.info("Hướng dẫn: Dùng Twitter Web Exporter export search results → Upload file CSV ở đây.")
    
    uploaded_file = st.file_uploader("Chọn file CSV hoặc JSON", type=["csv", "json"])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_json(uploaded_file)
            
            st.success(f"✅ Đã load **{len(df)}** tweets!")
            st.dataframe(df.head(20), use_container_width=True)
            st.session_state["df"] = df
        except Exception as e:
            st.error(f"Lỗi đọc file: {e}")

with tab_ai:
    st.header("📊 AI Agents - Key Narratives & Alpha Signals")
    if "df" in st.session_state:
        df = st.session_state["df"]
        st.subheader("Thống kê nhanh từ data")
        st.metric("Số lượng tweet", len(df))
        
        # Simple keyword analysis (nếu có cột text)
        if "text" in df.columns or "tweetText" in df.columns or "full_text" in df.columns:
            text_col = "text" if "text" in df.columns else ("tweetText" if "tweetText" in df.columns else "full_text")
            text = " ".join(df[text_col].dropna().astype(str).str.lower())
            words = pd.Series(text.split()).value_counts().head(15)
            fig = px.bar(words, title="Top từ khóa phổ biến")
            st.plotly_chart(fig, use_container_width=True)
    
    st.text_area("Key Narratives (cập nhật thủ công)", height=180, 
                 value="• AI Agents chuyển sang Autonomous Economic Entities\n• x402 Payment Standard + ERC-8004\n• Agentic Finance & M2M Economy\n• Privacy Compute là bottleneck")

with tab_rwa:
    st.header("🏦 RWA / Institutional & Competitors")
    st.text_area("Significant Reports / Articles / Podcasts", height=200, 
                 value="Dán link report + tóm tắt ở đây (ví dụ: CoinGecko RWA Report, Binance Research...)")

with tab_top5:
    st.header("🔥 5 Top Impactful News / Partnerships / Narratives")
    for i in range(1, 6):
        with st.expander(f"#{i}"):
            st.text_input(f"Tiêu đề {i}", key=f"title{i}")
            st.text_area(f"Mô tả + Mantle angle {i}", height=100, key=f"desc{i}")

with tab_metrics:
    st.header("📈 Metrics & Actionable Alpha")
    if "df" in st.session_state:
        df = st.session_state["df"]
        st.metric("Tổng impressions ước tính", f"{len(df) * 1200:,}")
    
    st.text_area("Actionable cho Mantle Squad", height=150, 
                 value="- Push nội dung AI Agents + xStocksFi\n- Ý tưởng bounty: ...\n- Nội dung cần làm tuần sau: ...")

st.caption("Built for Mantle Squad • Cộng Đồng Là Sức Mạnh Thật Sự 🚀")
