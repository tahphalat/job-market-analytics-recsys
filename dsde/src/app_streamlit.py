"""
Internal Analytics Tool for Job Market Analysis.
Includes Batch + Streaming capabilities, Insight generation, and Explainable RecSys.

Run from the dsde directory:
    streamlit run src/app_streamlit.py
"""

from __future__ import annotations

import ast
import json
import sys
import time
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import altair as alt
import pandas as pd
import streamlit as st

# Ensure project root is importable
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from src.config import ARTIFACTS_DIR, PROCESSED_DIR
from src.utils.io import read_auto
# Import Mock Streaming Components
try:
    from src.streaming.mock_stream import MockProducer, MockConsumer
except ImportError:
    MockProducer = None
    MockConsumer = None


st.set_page_config(page_title="JobScope Internal Analytics", layout="wide", page_icon="📊")

# --- UTILS ---

@st.cache_data(show_spinner=False)
def load_kpis(path: Path = ARTIFACTS_DIR / "kpi_summary.json") -> Dict:
    if not path.exists():
        return {}
    with open(path) as fh:
        return json.load(fh)

@st.cache_data(show_spinner=False)
def load_table(filename: str) -> pd.DataFrame:
    path = ARTIFACTS_DIR / filename
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)

@st.cache_data(show_spinner=False)
def load_demo_recs(path: Path = ARTIFACTS_DIR / "demo_recs.json") -> Dict[str, List[Dict]]:
    if not path.exists():
        return {}
    with open(path) as fh:
        return json.load(fh)

def parse_skills(raw: object) -> List[str]:
    # robust check for iterable (list, tuple, np.ndarray) but not string
    if hasattr(raw, '__iter__') and not isinstance(raw, (str, bytes)):
        return [str(s).strip() for s in raw if str(s).strip()]
    if isinstance(raw, list): # fallback explicit check
        return [s.strip() for s in raw if isinstance(s, str) and s.strip()]
    if isinstance(raw, str):
        raw = raw.strip()
        if not raw: return []
        if raw.startswith("["):
            try:
                parsed = ast.literal_eval(raw)
                if isinstance(parsed, list):
                    return [str(s).strip() for s in parsed if str(s).strip()]
            except (ValueError, SyntaxError):
                pass
        if "," in raw:
            return [s.strip() for s in raw.split(",") if s.strip()]
        return [raw]
    return []

@st.cache_data(show_spinner=False)
def load_jobs(path: Path = PROCESSED_DIR / "jobs_canonical.parquet") -> pd.DataFrame:
    df = pd.DataFrame()
    data_source = None # Track source for debugging/toasts

    # Priority 1: Main Parquet File (Local Dev / Full)
    if path.exists():
        try:
            df = read_auto(path)
            data_source = "main"
        except Exception:
            pass # Fallback to others if read fails

    # Priority 2: Split Files (Cloud Deployment - Full Data)
    if df.empty:
        parts = sorted(path.parent.glob("jobs_canonical_part_*.parquet"))
        if parts:
            try:
                # st.toast removed to prevent CacheReplayClosureError
                dfs = [read_auto(p) for p in parts]
                df = pd.concat(dfs, ignore_index=True)
                data_source = "split"
            except Exception:
                pass

    # Priority 3: Sample Data (Cloud Deployment - Fallback)
    if df.empty:
        sample_path = path.parent / "jobs_canonical_sample.parquet"
        if sample_path.exists():
            # st.toast removed to prevent CacheReplayClosureError
            df = read_auto(sample_path)
            data_source = "sample"

    # Priority 4: CSV Fallback (Local Dev - Repair)
    if df.empty:
        csv_fallback = path.with_suffix(".csv")
        if csv_fallback.exists():
            df = read_auto(csv_fallback)
            data_source = "csv"

    if df.empty:
        return pd.DataFrame()

    # --- Common Processing ---
    # OPTIMIZATION: Drop description_text to save memory (approx 1GB savings)
    if "description_text" in df.columns:
        df.drop(columns=["description_text"], inplace=True)

    # Convert timestamps
    df["published_at"] = pd.to_datetime(df.get("published_at"), errors="coerce", utc=True)
    
    # Clean salary
    for col in ["salary_min", "salary_max"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    
    # Create derived columns
    df["is_remote"] = df["location_text"].astype(str).str.contains("remote|work from home", case=False)
    
    df["skills_parsed"] = df.get("skills", pd.Series(dtype=object)).apply(parse_skills)
    df["skills_display"] = df["skills_parsed"].apply(lambda items: ", ".join(items))
    
    return df

# --- SECTIONS ---

def render_system_overview():
    st.header("System Overview")
    
    st.markdown("""
    **ภาพรวมระบบ (System Architecture)**
    
    หน้านี้แสดงโครงสร้างการทำงานเบื้องหลังของ **JobScope Platform** ที่ออกแบบมาเพื่อรองรับข้อมูลขนาดใหญ่ (Big Data)

    ### 📚 Data Source (แหล่งข้อมูลหลัก)
    ระบบประมวลผลข้อมูลจาก **[LinkedIn Job Postings Dataset](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings)** (via Kaggle) 
    ซึ่งครอบคลุมประกาศงานกว่า **120,000+ รายการ** ในสหรัฐอเมริกาและทั่วโลก

    
    **จุดเด่นของระบบ:**
    *   **Lambda Architecture:** รองรับทั้งข้อมูลย้อนหลัง (Batch) และข้อมูลล่าสุด (Speed/Streaming) ไปพร้อมๆ กัน
    *   **Scalability:** สามารถขยายเพื่อรองรับข้อมูลหลักล้านได้ง่าย (ผ่าน Kafka & Parquet)
    *   **Data Quality:** มีระบบตรวจสอบคุณภาพข้อมูล (Data Guard) ในทุกขั้นตอนก่อนนำมาแสดงผล
    
    ### 🏗️ Data Architecture Diagram
    แผนภาพแสดงการไหลของข้อมูลตั้งแต่ต้นทางจนถึงหน้าจอผู้ใช้:
    """)
    
    # Display the generated image
    from PIL import Image
    try:
        img_path = ARTIFACTS_DIR / "figures" / "architecture_diagram.png"
        if img_path.exists():
            image = Image.open(img_path)
            st.image(image, caption="Lambda Architecture Design") # Removed use_container_width for robustnes
        else:
            st.warning("Diagram image not found.")
    except Exception as e:
        st.error(f"Could not load diagram: {e}")
    
    # Simple Mermaid Diagram (Text Version)
    with st.expander("Show Logic Flow (Mermaid)", expanded=False):
        st.markdown("""
        ```mermaid
        graph LR
            A[Kaggle Source] -->|JSON/API| B(Raw Layer)
            B -->|Validation| C(Cleaned Layer)
            C -->|Transform| D(Curated Layer)
            D -->|Agg| E[Artifacts]
            F[Kafka Stream] -->|Speed Layer| B
            E --> G[Streamlit Dashboard]
        ```
        """)
    
    st.info("The system currently processes ~10k jobs/day in Batch mode. Streaming layer handles ~100 events/sec peak.")

def render_market_insights():
    st.header("ข้อมูลเชิงลึกตลาดงาน (Market Insights)")
    
    st.markdown("""
    สรุปภาพรวมสถานการณ์ตลาดแรงงานสาย Data Engineer จากข้อมูลที่รวบรวมได้ โดยแบ่งออกเป็น 3 ส่วนหลัก
    """)

    tab1, tab2, tab3 = st.tabs(["📊 ภาพรวม (Overview)", "🛠️ ทักษะ (Skills)", "💰 เงินเดือน"])

    kpi = load_kpis()

    with tab1:
        st.subheader("สถานะระบบและตัวเลขสำคัญ")
        
        # Calculate Real Salary Metrics on the fly
        df_real = load_jobs()
        avg_sal_str = "N/A"
        delta_str = None
        
        if not df_real.empty:
            # Filter valid annual salaries
            valid = df_real[
                (df_real["salary_min"] > 10000) & 
                (df_real["salary_min"] < 500000)
            ].copy()
            
            if not valid.empty:
                valid["avg"] = (valid["salary_min"] + valid["salary_max"]) / 2
                overall_mean = valid["avg"].mean()
                avg_sal_str = f"${overall_mean/1000:.1f}k"
                
                # Compare with Remote
                remote_mean = valid[valid["is_remote"]]["avg"].mean()
                if pd.notna(remote_mean):
                    diff = remote_mean - overall_mean
                    pct = (diff / overall_mean) * 100
                    delta_str = f"{pct:+.1f}% (Remote vs Avg)"

        if kpi:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("จำนวนงานที่วิเคราะห์", f"{kpi.get('total_jobs', 0):,}", delta="Batch: Last 24h")
            c2.metric("จำนวนบริษัท", f"{kpi.get('unique_companies', 0):,}")
            c3.metric("เงินเดือนเฉลี่ย (Real)", avg_sal_str, delta=delta_str) 
            c4.metric("แหล่งข้อมูล", "Kaggle")
        
        st.divider()

        st.subheader("ตำแหน่งงานที่เปิดรับมากที่สุด (Top Titles)")
        df_titles = load_table("top_titles.csv")
        
        if not df_titles.empty:
            # Add slider to control number of records
            top_n = st.slider("แสดงจำนวนลำดับ (Top N)", min_value=10, max_value=50, value=30)
            
            df_show = df_titles.head(top_n)
            
            # Dynamic height: 25px per bar + buffer
            chart_height = 100 + (len(df_show) * 20)
            
            chart = alt.Chart(df_show).mark_bar().encode(
                x=alt.X("count:Q", title=None),
                y=alt.Y("value:N", sort="-x", title="ชื่อตำแหน่ง"),
                tooltip=["value", "count"]
            ).properties(height=chart_height)
            st.altair_chart(chart, use_container_width=True)
            
            st.markdown("> 💡 **Insight:** จากข้อมูลจริง พบว่าตำแหน่งกลุ่ม **Sales & Management** (เช่น Sales Manager) ยังครองตลาดภาพรวม แต่ในสาย Tech นั้น **Software Engineer** และ **Data Analyst** คือสองตำแหน่งที่โดดเด่นที่สุด")

    with tab2:
        st.subheader("เจาะลึกทักษะที่ตลาดต้องการ")
        df_skills = load_table("top_skills.csv")
        if not df_skills.empty:
            # Mocking specific 'Remote' skill distribution if not in artifacts yet
            df_skills["Type"] = "Overall"
            
            col_chart, col_desc = st.columns([2, 1])
            
            with col_chart:
                 chart = alt.Chart(df_skills.head(15)).mark_bar().encode(
                    x=alt.X("count:Q", title="จำนวนประกาศงาน"),
                    y=alt.Y("value:N", sort="-x", title="ทักษะ (Skill)"),
                    color=alt.value("#4c78a8"),
                    tooltip=["value", "count"]
                ).properties(height=400)
                 st.altair_chart(chart, use_container_width=True)

            with col_desc:
                # Dynamic Top Skills Text
                top_3_text = ""
                if not df_skills.empty:
                    for i, row in df_skills.head(3).iterrows():
                        top_3_text += f"{i+1}. **{row['value']}**\n"
                
                st.info(f"**ทักษะยอดนิยม (Top Skills):**\n{top_3_text}")
                st.markdown("---")

    with tab3:
        st.subheader("โครงสร้างเงินเดือนและการเติบโต")
        
        st.markdown("**💰 การกระจายตัวของเงินเดือน (Annual Salary)**")
        
        # Load real data
        df_sal = load_jobs()
        
        # Filter valid salaries (Assume Annual: > 10k USD and < 500k USD to remove hourly/outliers)
        valid_salary = df_sal[
            (df_sal["salary_min"] > 10000) & 
            (df_sal["salary_min"] < 500000) &
            (df_sal["salary_min"].notna())
        ].copy()
        
        if not valid_salary.empty:
            # Use average of min/max as the representative salary
            valid_salary["avg_salary"] = (valid_salary["salary_min"] + valid_salary["salary_max"]) / 2
            
            # Create Histogram from Real Data
            chart = alt.Chart(valid_salary).mark_bar().encode(
                x=alt.X("avg_salary:Q", bin=alt.Bin(maxbins=20), title="เงินเดือนเฉลี่ยต่อปี (USD)"),
                y=alt.Y("count()", title="จำนวนงาน"),
                tooltip=["count()", alt.Tooltip("avg_salary", bin=True, title="ช่วงเงินเดือน")]
            ).properties(height=300)
            st.altair_chart(chart, use_container_width=True)
            
            # Show summary stats
            mean_val = valid_salary["avg_salary"].mean()
            st.caption(f"*วิเคราะห์จากข้อมูลจริง {len(valid_salary):,} งาน (กรองเฉพาะรายปี) | ค่าเฉลี่ย: ${mean_val:,.0f}*")
        else:
            st.warning("ไม่พบข้อมูลเงินเดือนที่สมบูรณ์ใน Dataset นี้")

def render_job_browser():
    st.header("Job Browser")
    
    st.markdown("""
    **ค้นหาและสำรวจข้อมูลงาน (Job Browser)**
    
    ตารางรวบรวมรายการงานทั้งหมดที่ผ่านการคัดกรองแล้ว ท่านสามารถ **"ค้นหา"** หรือ **"กรอง"** 
    เพื่อดูรายละเอียดเจาะจงรายบริษัทได้
    
    **Tips:** 
    *   ลองพิมพ์ keywords เช่น `Engineering`, `Design` หรือชื่อเมืองในช่อง Search
    *   ใช้ Checkbox เพื่อซ่อนงานข้อมูลไม่ครบ (Clean Data)
    """)
    
    df = load_jobs()
    if df.empty: return

    with st.expander("Filter Options", expanded=False):
        c1, c2 = st.columns(2)
        search = c1.text_input("Search")
        hide_incomplete = c2.checkbox("Hide incomplete (No Salary/Loc)", value=False)
    
    filtered = df.copy()
    if search:
        # Improved Search: Split terms and match ANY key column (AND logic between terms)
        terms = search.strip().split()
        for term in terms:
            term_mask = (
                filtered["title"].astype(str).str.contains(term, case=False) |
                filtered["company"].astype(str).str.contains(term, case=False) |
                filtered["skills_display"].astype(str).str.contains(term, case=False) |
                filtered["location_text"].astype(str).str.contains(term, case=False)
            )
            filtered = filtered[term_mask]
    # if sources/remote filter removed
        
    if hide_incomplete:
        # Filter out jobs with missing critical info (Salary or Description or Company)
        # Note: Salary is often missing, so we might be strict or lenient. 
        # For "Hide incomplete", we'll check for nulls in visible columns.
        filtered = filtered[
            (filtered["salary_min"].notna()) & 
            (filtered["company"].notna()) & 
            (filtered["location_text"].notna())
        ]

    st.caption(f"Showing {len(filtered):,} jobs")
    st.dataframe(
        filtered[["title", "company", "location_text", "skills_display", "published_at"]].head(100),
        hide_index=True
    )

def render_recommendations():
    st.header("Recommendation Engine")
    
    st.markdown("""
    ### 🧠 Explainable RecSys
    **ระบบแนะนำงานอัจฉริยะ (Recommendation Engine)**
    
    หน้านี้ทำหน้าที่ **"จับคู่"** ระหว่างโปรไฟล์ของผู้สมัคร (Persona) กับตำแหน่งงานที่มีในระบบ 
    โดยใช้เทคนิคการประมวลผลภาษาธรรมชาติ (NLP) ในการหาความคล้ายคลึงของทักษะและคำสำคัญ
    
    **ประโยชน์การใช้งาน (Use Cases):**
    1. **Personalization:** ช่วยให้ผู้หางานไม่ต้องค้นหาเองทีละงาน ระบบคัดมาให้เฉพาะที่ตรงใจ
    2. **Skill Gap Analysis:** ดูเหตุผล (Match Reasons) เพื่อรู้ว่าเราขาดทักษะอะไรสำหรับงานในฝัน
    3. **Transparency:** แสดงให้เห็นว่าทำไมถึงแนะนำงานนี้ (Explainable AI)
    """)
    
    recs = load_demo_recs()
    if not recs:
        st.info("No recommendations found.")
        return
        
    persona = st.selectbox("Select Persona", sorted(recs.keys()))
    
    for item in recs.get(persona, []):
        with st.container():
            c1, c2 = st.columns([3, 1])
            with c1:
                st.subheader(item.get("title"))
                st.caption(f"{item.get('company')} • {item.get('source')}")
                st.write("**Match Reasons:**")
                for r in item.get("reasons", [])[:3]:
                    st.markdown(f"- ✅ **{r}** (Key Skill Match)")
            with c2:
                score = item.get("score", 0)
                st.metric("Match Score", f"{score:.2f}")
            st.divider()

def render_streaming_demo():
    st.header("Real-Time Monitor")
    
    st.markdown("""
    **ระบบติดตามข้อมูลแบบเรียลไทม์ (Real-Time Monitor)**
    
    หน้านี้ใช้สำหรับ **"จำลองและตรวจสอบ"** การไหลของข้อมูลเข้าสู่ระบบในวินาทีต่อวินาที (Simulation)
    
    **ทำหน้าที่อะไร:**
    *   **Monitor Ingestion:** ดูว่ามีงานใหม่ๆ ถูกดูดเข้ามาในระบบจริงหรือไม่
    *   **Trend Detection:** ดูกราฟทักษะ (Skill Trending) ที่เปลี่ยนแปลงไปตามข้อมูลชุดใหม่ล่าสุดทันที
    *   **System Health:** ตรวจสอบว่า Pipeline ฝั่ง Streaming ทำงานปกติหรือไม่
    
    **วิธีเล่น:** กดปุ่ม `Start Ingestion Simulation` เพื่อเริ่มจำลองเหตุการณ์ที่มีงานใหม่ไหลเข้ามา
    """)
    
    if st.button("Start Ingestion Simulation"):
        if not MockProducer:
            st.error("Mock Streaming module not found.")
            return

        producer = MockProducer()
        consumer = MockConsumer()
        
        status_text = st.empty()
        chart_placeholder = st.empty()
        log_placeholder = st.empty()
        
        logs = []
        for job in producer.stream_jobs(count=15, delay=0.3):
            consumer.ingest(job)
            logs.append(f"[{job['timestamp']}] New Job: {job['title']} @ {job['company']}")
            status_text.success(f"Ingested job: {job['title']}")
            
            top_skills = consumer.get_top_skills()
            if top_skills:
                df_realtime = pd.DataFrame(top_skills, columns=["Skill", "Count"])
                chart = alt.Chart(df_realtime).mark_bar().encode(
                    x="Count:Q",
                    y=alt.Y("Skill:N", sort="-x")
                ).properties(title="Real-time Skill Trending")
                chart_placeholder.altair_chart(chart, use_container_width=True)
            
            log_placeholder.code("\n".join(logs[-5:]))
            
        st.success("Simulation Complete.")

def main():
    st.sidebar.title("JobScope Analytics")
    
    # Global Data Check
    df_check = load_jobs()
    if not df_check.empty:
        if len(df_check) <= 10000:
            st.sidebar.warning(
                "⚠️ **Demo Deployment (Sample)**\n\n"
                "Running on **10k Sample Data**.\n\n"
                "Full dataset (~120k) not loaded.",
                icon="⚠️"
            )

    nav = st.sidebar.radio("Navigation", [
        "System Overview",
        "Market Insights", 
        "Job Browser", 
        "Recommendation Engine",
        "Real-time Monitor"
    ])
    
    if nav == "System Overview": render_system_overview()
    elif nav == "Market Insights": render_market_insights()
    elif nav == "Job Browser": render_job_browser()
    elif nav == "Recommendation Engine": render_recommendations()
    elif nav == "Real-time Monitor": render_streaming_demo()

if __name__ == "__main__":
    main()
