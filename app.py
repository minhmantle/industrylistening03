import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Mantle Social Listening", layout="wide")
st.title("🚀 Mantle Squad - Weekly Social Listening Dashboard")
st.caption(f"Week: {st.text_input('Tuần', '2026-W24')} | Updated: {datetime.now().strftime('%d/%m/%Y')}")

tab_upload, tab_ai, tab_rwa, tab_top5, tab_metrics = st.tabs([
    "📥 Upload Data", "📊 AI Agents", "🏦 RWA/Institutional", "🔥 Top 5", "📈 Metrics"
])

with tab_upload:
    st.header("Upload CSV từ Twitter Web Exporter")
    uploaded = st.file_uploader("Upload CSV", type=["csv"])
    
    if uploaded:
        df = pd.read_csv(uploaded)
        st.success(f"✅ Load {len(df)} tweets")
        st.session_state.df = df
        st.dataframe(df.head(10), use_container_width=True)

# Tự động xử lý nếu có data
if "df" in st.session_state:
    df = st.session_state.df
    text_col = next((col for col in ['text', 'tweetText', 'full_text', 'content'] if col in df.columns), None)
    
    with tab_ai:
        st.header("📊 AI Agents & Hot Narratives")
        if text_col:
            text = " ".join(df[text_col].dropna().astype(str))
            words = pd.Series(text.lower().split()).value_counts().head(20)
            st.plotly_chart(px.bar(words, title="Top Keywords"), use_container_width=True)
        
        st.text_area("Key Narratives (chỉnh lại nếu cần)", height=200, 
                     value="• AI Agents + x402\n• RWA + Institutional\n• ...")

    with tab_top5:
        st.header("🔥 Top 5 Impactful (Auto sort by engagement)")
        if 'favorite_count' in df.columns:
            top = df.nlargest(5, 'favorite_count')[['text', 'user_name', 'favorite_count', 'retweet_count']]
            st.dataframe(top, use_container_width=True)

    with tab_metrics:
        st.metric("Total Tweets", len(df))
        if 'favorite_count' in df.columns:
            st.metric("Total Likes", df['favorite_count'].sum())
            st.metric("Total Retweets", df['retweet_count'].sum())

st.caption("Mantle Squad • Cộng Đồng Là Sức Mạnh Thật Sự")
