# SMART DATA COLLECTION TOOL
### One-stop platform for automated news scraping, image dataset generation, and AI-driven blog synthesis.

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

## 🚀 Overview
The **Smart Data Collection Tool** is a production-ready application designed to streamline the process of gathering and synthesizing multi-modal data. Whether you need structured news datasets for financial analysis, image collections for computer vision training, or long-form blog reports for content marketing, this tool provides a unified, highly intuitive interface to get it done in seconds.

## ✨ Core Features
- 📰 **Automated News Scraping:** High-speed extraction of articles from Google RSS based on dynamic keywords and date ranges.
- 🖼️ **Image Dataset Generation:** Automated scraping of high-quality images via DuckDuckGo, packaged into portable ZIP archives.
- 📝 **AI-Synthesized Blogs:** Algorithmic generation of unique, plagiarism-free blog reports exported as professional PDFs.
- 🛠️ **Configurable Keyword Engine:** Intelligent tag-based keyword expansion to ensure high-relevance data collection.
- 📂 **Flexible Data Export:** Support for CSV and Excel formats for tabular data.
- ⚡ **Asynchronous Processing:** Optimized to prevent timeouts and ensure smooth user experience through progress monitoring.

## 🛠️ Tech Stack
- **Frontend:** Streamlit (UI/UX)
- **Backend:** Python (Modular Architecture)
- **Data Handling:** Pandas, NumPy
- **Scraping & APIs:** BeautifulSoup4, Feedparser, DuckDuckGo Search, HuggingFace Inference API
- **Document Rendering:** ReportLab (PDF Synthesis)
- **Environment Management:** Python-Dotenv

## 📂 Project Architecture
```text
Smart-Data-Collection-Tool/
├── frontend/
│   └── app.py              # Main Entry Point (Streamlit UI)
├── backend/
│   ├── news_module.py      # RSS Feed Scraping Logic
│   ├── image_module.py     # Image Scraping & ZIP Packing
│   ├── blog_module.py      # PDF Report Synthesis
│   ├── keyword_module.py   # AI Keyword Expansion Engine
│   └── utils.py            # Shared Helper Functions
├── config/
│   └── config.py           # Application Constants & Mappings
├── data/                   # Output storage (Local Cache)
│   ├── raw/
│   └── processed/
├── requirements.txt        # Dependency Manifest
├── .gitignore              # Git Exclusion Rules
└── README.md               # Project Documentation
```

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Dhruva912005/Smart-Data-Collection-Tool.git
cd Smart-Data-Collection-Tool
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration
Create a `.env` file in the root directory:
```env
HF_API_KEY=your_huggingface_key_here
```

## 🚦 How to Run
Launch the application from the project root:
```bash
streamlit run frontend/app.py
```

## 📸 Screenshots
*(Add high-quality screenshots here to showcase the UI)*

| Feature Selection | Results Preview |
| :---: | :---: |
| ![Selection Placeholder](https://via.placeholder.com/400x250?text=Feature+Selection) | ![Results Placeholder](https://via.placeholder.com/400x250?text=Data+Preview) |

## 🌟 Why This Project? (Recruiter Focus)
This project demonstrates expertise in:
1. **Modular System Design:** Separation of concerns between UI, Business Logic, and Configuration.
2. **Data Engineering:** Handling real-time streams (RSS) and multi-modal data (Images, Text).
3. **API Integration:** Leveraging external LLMs (HuggingFace) for intelligent utility.
4. **Performance Optimization:** Handling concurrency, timeouts, and large file IO.

## 📈 Future Roadmap
- [ ] Integration with GPT-4 for more advanced blog synthesis.
- [ ] Dynamic Data Visualization (Charts/Graphs) for scraped news trends.
- [ ] Support for social media scraping (Twitter/X, LinkedIn).
- [ ] Cloud deployment (Streamlit Community Cloud or AWS).

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

---
**Developed with ❤️ by [Dhruva](https://github.com/Dhruva912005)**
