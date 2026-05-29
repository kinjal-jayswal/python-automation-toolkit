"""
Python Automation Toolkit — JK Data Lab
Web scraping, file automation, data pipeline, email automation demos
Author: Kinjal Jayswal | JK Data Lab
Website: https://www.jkdatalab.com
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import time
import random
import re
from datetime import datetime, timedelta
from pathlib import Path

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Python Automation Toolkit | JK Data Lab",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #0A2A2A; color: #ffffff; }
    h1, h2, h3 { color: #00FFD4; }
    .tool-card {
        background: linear-gradient(135deg, #0d3333, #1a4a4a);
        border: 1px solid #00FFD4;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    .stButton>button {
        background-color: #00FFD4;
        color: #0A2A2A;
        font-weight: bold;
        border-radius: 8px;
    }
    .stTabs [data-baseweb="tab"] { color: #00FFD4; }
    .stTabs [data-baseweb="tab-highlight"] { background-color: #00FFD4; }
    code { background-color: #0d2020; color: #00FFD4; }
    .stTextInput input, .stTextArea textarea { background-color: #0d2020; color: white; }
    .log-box {
        background-color: #050f0f;
        border: 1px solid #00FFD4;
        border-radius: 8px;
        padding: 15px;
        font-family: monospace;
        font-size: 0.85rem;
        color: #00FFD4;
    }
</style>
""", unsafe_allow_html=True)

# ─── Header ─────────────────────────────────────────────────────────────────
st.title("⚙️ Python Automation Toolkit")
st.markdown("**Web Scraping · Data Pipeline · File Automation · Report Generation**")
st.markdown("---")

# ─── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🛠️ Automation Tools")
    st.markdown("""
    - 🌐 Web Scraper
    - 🔄 ETL Pipeline
    - 📁 File Organizer
    - 📊 Report Generator
    - 📧 Email Automation
    - 🔍 Data Validator
    """)
    st.markdown("---")
    st.markdown("**🌐 [JK Data Lab](https://www.jkdatalab.com)**")
    st.markdown("*kinjal@jkdatalab.com*")

# ─── Tabs ───────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌐 Web Scraper",
    "🔄 ETL Pipeline",
    "📁 File Organizer",
    "📊 Report Generator",
    "📧 Email Automation"
])

# ════════════════════════════════════════════════════════
# TAB 1 — WEB SCRAPER DEMO
# ════════════════════════════════════════════════════════
with tab1:
    st.subheader("🌐 Web Scraper Demo")
    st.markdown("Simulate scraping product data, news, or job listings from websites.")

    col1, col2 = st.columns([2, 1])
    with col1:
        url = st.text_input("Target URL", value="https://example-ecommerce.com/products")
        scrape_type = st.selectbox("Scrape Type", ["Product Listings", "News Articles", "Job Postings", "Company Data"])
        max_pages = st.slider("Max Pages", 1, 10, 3)

    with col2:
        st.markdown("**Scraper Config:**")
        delay = st.slider("Delay (seconds)", 0.5, 3.0, 1.0, 0.5)
        headers = st.checkbox("Use Custom Headers", value=True)
        proxy = st.checkbox("Use Proxy Rotation", value=False)

    if st.button("🚀 Start Scraping", type="primary"):
        progress = st.progress(0)
        log_placeholder = st.empty()
        logs = []

        for page in range(1, max_pages + 1):
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] 📡 Fetching page {page}/{max_pages}...")
            log_placeholder.markdown(
                '<div class="log-box">' + "<br>".join(logs[-5:]) + "</div>",
                unsafe_allow_html=True
            )
            progress.progress(page / max_pages)
            time.sleep(0.3)

        logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Scraping complete!")
        log_placeholder.markdown(
            '<div class="log-box">' + "<br>".join(logs) + "</div>",
            unsafe_allow_html=True
        )

        # Generate demo scraped data
        n = max_pages * 10
        if scrape_type == "Product Listings":
            data = {
                "Product": [f"Product {i}" for i in range(1, n+1)],
                "Price": [round(random.uniform(10, 500), 2) for _ in range(n)],
                "Rating": [round(random.uniform(3.0, 5.0), 1) for _ in range(n)],
                "Reviews": [random.randint(10, 1000) for _ in range(n)],
                "In Stock": [random.choice(["Yes", "Yes", "Yes", "No"]) for _ in range(n)],
                "URL": [f"{url}/product-{i}" for i in range(1, n+1)]
            }
        elif scrape_type == "Job Postings":
            data = {
                "Title": [f"Data {random.choice(['Scientist','Analyst','Engineer'])} {i}" for i in range(1, n+1)],
                "Company": [f"Company {random.choice(['A','B','C','D','E'])}" for _ in range(n)],
                "Location": [random.choice(["Remote", "New York", "London", "Bangalore"]) for _ in range(n)],
                "Salary": [f"${random.randint(50,150)}k" for _ in range(n)],
                "Posted": [f"{random.randint(1,30)} days ago" for _ in range(n)],
            }
        else:
            data = {
                "Title": [f"Article {i}: {random.choice(['AI', 'ML', 'Data', 'Python'])} News" for i in range(1, n+1)],
                "Source": [random.choice(["TechCrunch", "Medium", "ArXiv", "Reuters"]) for _ in range(n)],
                "Date": [(datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d") for _ in range(n)],
                "Sentiment": [random.choice(["Positive", "Neutral", "Negative"]) for _ in range(n)],
            }

        df = pd.DataFrame(data)
        st.success(f"✅ Scraped {len(df)} records from {max_pages} pages!")
        st.dataframe(df, use_container_width=True, height=250)

        col1, col2 = st.columns(2)
        with col1:
            csv = df.to_csv(index=False)
            st.download_button("📥 Download CSV", csv, "scraped_data.csv", "text/csv")
        with col2:
            st.json({"records": len(df), "pages": max_pages, "source": url})

# ════════════════════════════════════════════════════════
# TAB 2 — ETL PIPELINE
# ════════════════════════════════════════════════════════
with tab2:
    st.subheader("🔄 ETL Pipeline Demo")
    st.markdown("Extract → Transform → Load data pipeline with validation and logging.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**📥 Extract**")
        source = st.selectbox("Data Source", ["CSV File", "Excel File", "Database", "API", "JSON"])
        st.text_input("Connection String", value="postgresql://localhost:5432/mydb", disabled=True)

    with col2:
        st.markdown("**🔧 Transform**")
        transforms = st.multiselect("Transformations", [
            "Remove Duplicates", "Fill Missing Values", "Normalize Columns",
            "Date Formatting", "Currency Conversion", "Text Cleaning",
            "Outlier Removal", "Feature Engineering"
        ], default=["Remove Duplicates", "Fill Missing Values", "Date Formatting"])

    with col3:
        st.markdown("**📤 Load**")
        destination = st.selectbox("Destination", ["PostgreSQL", "MySQL", "BigQuery", "S3 Bucket", "CSV Export"])
        batch_size = st.number_input("Batch Size", 100, 10000, 1000, 100)

    if st.button("▶️ Run ETL Pipeline", type="primary"):
        steps = [
            ("🔗 Connecting to source...", 0.2),
            ("📥 Extracting data...", 0.3),
            ("🔍 Validating schema...", 0.2),
            ("🧹 Removing duplicates...", 0.3),
            ("🔧 Applying transformations...", 0.4),
            ("✅ Validating output...", 0.2),
            ("📤 Loading to destination...", 0.4),
            ("🎉 Pipeline complete!", 0.1),
        ]

        progress = st.progress(0)
        status = st.empty()
        for i, (step, delay) in enumerate(steps):
            status.markdown(f"**{step}**")
            progress.progress((i + 1) / len(steps))
            time.sleep(delay)

        # Show results
        st.success("✅ ETL Pipeline completed successfully!")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Records Extracted", "45,231")
        col2.metric("After Dedup", "43,890")
        col3.metric("Transformed", "43,890")
        col4.metric("Loaded", "43,890")

        # Pipeline visualization
        fig = go.Figure(go.Sankey(
            node=dict(
                pad=15, thickness=20,
                label=["Raw Data", "Extracted", "Validated", "Transformed", "Loaded"],
                color=["#00FFD4", "#00cc99", "#009966", "#006644", "#003322"]
            ),
            link=dict(
                source=[0, 1, 2, 3],
                target=[1, 2, 3, 4],
                value=[45231, 43890, 43890, 43890],
                color=["rgba(0,255,212,0.3)"] * 4
            )
        ))
        fig.update_layout(
            paper_bgcolor="#0A2A2A", font=dict(color="white"),
            height=250, margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

# ════════════════════════════════════════════════════════
# TAB 3 — FILE ORGANIZER
# ════════════════════════════════════════════════════════
with tab3:
    st.subheader("📁 File Organizer Demo")
    st.markdown("Automatically organize files by type, date, or custom rules.")

    folder_path = st.text_input("Source Folder", value="C:/Downloads")
    col1, col2 = st.columns(2)
    with col1:
        org_by = st.radio("Organize By", ["File Type", "Date", "Size", "Custom Rules"])
    with col2:
        action = st.radio("Action", ["Move Files", "Copy Files", "Dry Run (Preview)"])

    if st.button("🗂️ Organize Files", type="primary"):
        # Simulate file organization
        file_types = {
            "📄 Documents": ["report.pdf", "proposal.docx", "notes.txt", "contract.pdf"],
            "🖼️ Images": ["photo.jpg", "logo.png", "banner.gif", "screenshot.png"],
            "📊 Spreadsheets": ["data.xlsx", "budget.csv", "sales.xlsx"],
            "🐍 Python Files": ["script.py", "analysis.py", "model.py"],
            "📦 Archives": ["backup.zip", "project.tar.gz"],
            "🎵 Media": ["presentation.mp4", "recording.mp3"],
        }

        st.success(f"✅ Scan complete! Found {sum(len(v) for v in file_types.values())} files")

        for folder, files in file_types.items():
            with st.expander(f"{folder} ({len(files)} files)"):
                for f in files:
                    size = round(random.uniform(0.1, 50), 1)
                    st.markdown(f"📄 `{f}` — {size} MB → `{folder_path}/{folder.split()[1]}/`")

        counts = {k.split()[1]: len(v) for k, v in file_types.items()}
        fig = px.pie(
            values=list(counts.values()),
            names=list(counts.keys()),
            color_discrete_sequence=px.colors.sequential.Teal
        )
        fig.update_layout(paper_bgcolor="#0A2A2A", font=dict(color="white"), height=300)
        st.plotly_chart(fig, use_container_width=True)

# ════════════════════════════════════════════════════════
# TAB 4 — REPORT GENERATOR
# ════════════════════════════════════════════════════════
with tab4:
    st.subheader("📊 Automated Report Generator")
    st.markdown("Generate professional reports automatically from your data.")

    col1, col2 = st.columns(2)
    with col1:
        report_type = st.selectbox("Report Type", [
            "Weekly Sales Summary", "Monthly Analytics", "Data Quality Report",
            "Performance Dashboard", "Executive Summary"
        ])
        report_format = st.multiselect("Output Format", ["PDF", "Excel", "HTML", "PowerPoint"], default=["PDF", "Excel"])

    with col2:
        include_charts = st.checkbox("Include Charts", value=True)
        include_summary = st.checkbox("Include AI Summary", value=True)
        schedule = st.selectbox("Schedule", ["Once", "Daily", "Weekly", "Monthly"])

    if st.button("📊 Generate Report", type="primary"):
        with st.spinner("Generating report..."):
            time.sleep(1.5)

        st.success("✅ Report generated successfully!")

        # Preview
        st.markdown("### 📋 Report Preview")
        st.markdown(f"""
        **{report_type}**
        Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}

        **Executive Summary:**
        This automated report covers key performance metrics for the selected period.
        Total revenue increased by 12.3% compared to last period. Customer satisfaction
        score improved to 4.6/5.0. Three key areas identified for improvement.

        **Key Metrics:**
        - 📈 Revenue: $125,430 (+12.3%)
        - 🛒 Orders: 1,245 (+8.7%)
        - 😊 Satisfaction: 4.6/5.0 (+0.2)
        - ⚡ Processing Time: 2.3s avg (-15%)
        """)

        for fmt in report_format:
            st.download_button(
                f"📥 Download {fmt}",
                data=f"Sample {fmt} report content",
                file_name=f"report_{datetime.now().strftime('%Y%m%d')}.{fmt.lower()}",
                mime="text/plain"
            )

# ════════════════════════════════════════════════════════
# TAB 5 — EMAIL AUTOMATION
# ════════════════════════════════════════════════════════
with tab5:
    st.subheader("📧 Email Automation Demo")
    st.markdown("Automate bulk emails, follow-ups, and notifications.")

    col1, col2 = st.columns(2)
    with col1:
        email_type = st.selectbox("Email Type", [
            "Client Report Email", "Follow-up Sequence",
            "Invoice Notification", "Weekly Newsletter", "Alert Email"
        ])
        recipients_text = st.text_area("Recipients (one per line)", value="client1@company.com\nclient2@company.com\nclient3@company.com", height=100)

    with col2:
        subject = st.text_input("Subject", value="Your Weekly Analytics Report — JK Data Lab")
        schedule_time = st.time_input("Schedule Time", value=datetime.now().time())
        personalize = st.checkbox("Personalize with Name", value=True)
        attach_report = st.checkbox("Attach Auto-Generated Report", value=True)

    template = st.text_area("Email Template", value="""Dear {name},

Please find attached your weekly analytics report for {date}.

Key highlights this week:
• Revenue: ${revenue} (+{growth}% vs last week)
• New clients: {new_clients}
• Tasks completed: {tasks}

Best regards,
JK Data Lab Team
kinjal@jkdatalab.com""", height=180)

    if st.button("📤 Send Emails", type="primary"):
        recipients = [r.strip() for r in recipients_text.split("\n") if r.strip()]
        progress = st.progress(0)

        for i, email in enumerate(recipients):
            time.sleep(0.3)
            progress.progress((i + 1) / len(recipients))

        st.success(f"✅ {len(recipients)} emails sent successfully!")
        st.dataframe(pd.DataFrame({
            "Recipient": recipients,
            "Status": ["✅ Sent"] * len(recipients),
            "Time": [datetime.now().strftime("%H:%M:%S")] * len(recipients),
            "Opens": [random.randint(0, 1) for _ in recipients]
        }), use_container_width=True)

# ─── Footer ─────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "Built with ❤️ by **[JK Data Lab](https://www.jkdatalab.com)** | "
    "kinjal@jkdatalab.com | Ahmedabad, India"
)
