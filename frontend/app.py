import streamlit as st
import time
import sys
import os

# Add root project folder to sys path for access to backend and config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.news_module import generate_news_dataset
from backend.image_module import generate_image_dataset
from backend.blog_module import generate_blog_pdf
from config.config import CATEGORIES

st.set_page_config(page_title="Smart Data Tool", page_icon="📊", layout="wide")

# 🔹 2. Centered Heading (Pro Look)
st.markdown("<h1 style='text-align: center; color: #FFFFFF;'>📊 Smart Data Collection Tool</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #A0AEC0; margin-bottom: 40px;'>Easily collect datasets, images, and blogs</h4>", unsafe_allow_html=True)

# 🔹 1. Sidebar Navigation
with st.sidebar:
    st.markdown("### 🛠️ Navigation Menu")
    option = st.selectbox(
        "Choose Feature",
        ["News Dataset", "Image Dataset", "Blog Generator"]
    )
    st.markdown("<hr>", unsafe_allow_html=True)
    st.info("System optimized for dark theme.")
    
    with st.expander("📂 Explore Categories"):
        cat_search = st.selectbox("View Tags for:", list(CATEGORIES.keys()))
        st.write(", ".join(CATEGORIES[cat_search]))

# 🔹 4 & 6. Clean Input Layout & Spacing

def get_keywords_from_categories(selected_categories, core_topic):
    all_keywords = []
    for cat in selected_categories:
        all_keywords.extend(CATEGORIES.get(cat, []))
    
    # Add core topic variations if topic provided
    if core_topic:
        base = core_topic.lower()
        all_keywords.extend([base, f"{base} news", f"{base} market", f"{base} trends", f"{base} forecast"])
        
    # Deduplicate while preserving order
    unique_keywords = []
    seen = set()
    for kw in all_keywords:
        kw_lower = kw.lower().strip()
        if kw_lower and kw_lower not in seen:
            unique_keywords.append(kw_lower)
            seen.add(kw_lower)
    return unique_keywords

st.markdown("<br>", unsafe_allow_html=True)

# Center inputs slightly dynamically
_, center_col, _ = st.columns([1, 10, 1])

with center_col:
    with st.container():
        st.markdown("### 🔎 Query Configuration")
        col1, col2 = st.columns([1, 2])
        with col1:
            topic = st.text_input("Core Topic (Optional Context):", placeholder="e.g., Gold, AI...")
        with col2:
            selected_cats = st.multiselect(
                "Select Keyword Categories:",
                options=list(CATEGORIES.keys()),
                help="Choose one or more categories to auto-load associated keywords."
            )
            
    if selected_cats or topic:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 🔹 5. Keywords Display (UI Upgrade)
        keywords = get_keywords_from_categories(selected_cats, topic)
        st.session_state['active_keywords'] = keywords
        
        with st.container():
            st.markdown("#### 🤖 Active Keywords (Auto from Categories)")
            if keywords:
                # Beautiful dark-themed pill badges
                keywords_html = " ".join([f"<span style='background-color: #2D3748; border: 1px solid #4A5568; color: #E2E8F0; padding: 6px 14px; border-radius: 16px; margin: 4px; display: inline-block; font-weight: 500; font-size: 14px; box-shadow: 0px 2px 4px rgba(0,0,0,0.2);'>{kw}</span>" for kw in keywords])
                st.markdown(f"<div style='padding: 10px 0; max-height: 300px; overflow-y: auto;'>{keywords_html}</div>", unsafe_allow_html=True)
            else:
                st.warning("⚠️ Please select at least one category to populate keywords.")
                
        st.markdown("<hr style='border-top: 1px solid #4A5568; margin: 30px 0;'>", unsafe_allow_html=True)

        # 🔹 Feature Sections
        if option == "News Dataset":
            st.markdown("### 📰 Generate News Dataset")
            with st.container():
                col_d1, col_d2, col_d3 = st.columns(3)
                with col_d1:
                    start_date = st.date_input("📅 Start Date")
                with col_d2:
                    end_date = st.date_input("📅 End Date")
                with col_d3:
                    file_format = st.selectbox("📂 File Format", ["csv", "excel"])
                    
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 🔹 7. Button Styles
            if st.button("🚀 Generate News Dataset", type="primary", use_container_width=True):
                # 🔹 3. Progress Bar
                loading_bar = st.progress(0, text="Initializing connections...")
                for percent in range(1, 75):
                    time.sleep(0.01)
                    loading_bar.progress(percent, text=f"Generating... {percent}% complete")
                
                with st.spinner("Fetching News from Google RSS (Extracting articles)..."):
                    df, file_path = generate_news_dataset(keywords, start_date, end_date, file_format)
                
                loading_bar.progress(100, text="Generating... 100% complete")
                
                # 🔹 9. Error & Success UI
                st.success("🎉 Dataset Ready Successfully!")
                st.dataframe(df, use_container_width=True)

                with open(file_path, "rb") as f:
                    st.download_button("📥 Download Dataset", f, file_name=file_path.split("/")[-1], use_container_width=True)

        elif option == "Image Dataset":
            st.markdown("### 🖼️ Download Image Dataset")
            
            with st.container():
                image_count = st.number_input("🔢 Number of Images", min_value=1, max_value=100, value=10, step=1)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🚀 Generate Images", type="primary", use_container_width=True):
                loading_bar = st.progress(0, text="Allocating bandwidth...")
                for percent in range(1, 60):
                    time.sleep(0.01)
                    loading_bar.progress(percent, text=f"Generating... {percent}% complete")
                    
                with st.spinner(f"Scraping {image_count} Unique Images..."):
                    zip_path, timeout_occurred = generate_image_dataset(topic, n=image_count, timeout_limit=180)
                
                loading_bar.progress(100, text="Generating... 100% complete")
                
                if timeout_occurred:
                    st.warning("⚠️ Stopped early to prevent timeout limitations!")

                if zip_path is None:
                    st.error("❌ Failed to download images. Please try a different topic.")
                else:
                    st.success("🎉 Image Archive Prepared Successfully!")
                    with open(zip_path, "rb") as f:
                        st.download_button("📥 Download ZIP Archive", f, file_name=zip_path.split("/")[-1], use_container_width=True)

        elif option == "Blog Generator":
            st.markdown("### 📝 Generate Blog PDF")
            
            blog_pages = st.number_input("📄 Target Number of Pages (1-20)", min_value=1, max_value=20, value=2, step=1)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🚀 Generate Blog Report", type="primary", use_container_width=True):
                loading_bar = st.progress(0, text="Loading textual parameters...")
                for percent in range(1, 85):
                    time.sleep(0.01)
                    loading_bar.progress(percent, text=f"Generating... {percent}% complete")
                    
                with st.spinner(f"Rendering up to {blog_pages} Unique Pages via ReportLab..."):
                    try:
                        pdf_path, stopped_early = generate_blog_pdf(topic, num_pages=blog_pages)
                        
                        loading_bar.progress(100, text="Generating... 100% complete")
                        
                        if stopped_early:
                            st.warning("⚠️ Partial content generated gracefully due to limited unique data preventing duplicate phrasing!")
                        else:
                            st.success("🎉 PDF Document Synthesized Successfully!")
                            
                        with open(pdf_path, "rb") as f:
                            st.download_button("📥 Download PDF Report", f, file_name=pdf_path.split("/")[-1], use_container_width=True)
                    except Exception as e:
                        loading_bar.empty()
                        st.error(f"❌ Blog generation unexpectedly failed: {e}")
    else:
        st.info("👈 Please define a Core Topic above to begin generating context-rich datasets!")