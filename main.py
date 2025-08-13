import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="Dheeraj Gajula Portfolio", page_icon=":wave:", layout="wide")

# --- SIDEBAR ---
st.sidebar.title("Dheeraj Gajula")
st.sidebar.markdown("""
- 💼 [LinkedIn](https://www.linkedin.com/in/dheeraj-gajula-8776381ba/)
- 💻 [GitHub](https://github.com/dheerajgajula02)
- 📧 dheerajgajula2202@gmail.com
""")
st.sidebar.markdown("#### Currently at")
st.sidebar.write("**University of Colorado Boulder**")

# --- HEADER ---
st.title("Dheeraj Gajula")
st.write("**Machine Learning Engineer | Graduate Student @ University of Colorado Boulder**")

st.write("""
Passionate software developer and ML engineer skilled in Python, Go, Deep Learning & Cloud.
Winner at Smart India Hackathon | Finalist at UNESCO Hackathon | Published at International Conference
""")

# --- RESUME DOWNLOAD BUTTON ---
with open("dheeraj_gajula_resume.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()
st.download_button(
    label="📄 Download My Resume",
    data=PDFbyte,
    file_name="Dheeraj_Gajula_Resume.pdf",
    mime="application/pdf"
)

# --- ABOUT ME SECTION ---
st.header("About Me")
st.write("""
A forward-thinking, solution-driven Computer Science graduate student at CU Boulder. I enjoy building real-world solutions blending machine learning, data engineering, and cloud tech. Experienced across multiple industry and research roles, I thrive on impact, collaboration, and technical learning.
""")

# --- EXPERIENCE SECTION ---
st.header("Experience")
st.markdown("""
**Versa Networks**  
_Software Engineer – 1 (June 2024 – Present)_  
- Developed REST APIs in Go and Cassandra serving 3,000+ req/s; monitored via Prometheus and Grafana dashboards.  
- Built ML models and pipelines (Python, BigQuery), and deployed reinforcement models to predict malicious feed outcomes.  
- Containerized multiple services (Docker, K8s) and deployed in GCP.

_Software Engineer – Intern (Feb 2024 – June 2024)_  
- Automated device usage tracking, reducing billing process from 7 days to 1 hour.  
- Designed anomaly-detection systems, processed director logs with Python/MongoDB, provided insights dashboards.

**Appsynergies (Minglewise)**  
_Machine Learning Research Intern (Jan 2024 – March 2024)_  
- Reduced fake profiles by 35% using ensemble models (NER, Regex, HuggingFace, DeepFace).

**IIT Bhilai (Nirmaya)**  
_Research Intern (Apr 2023 – Jan 2024)_  
- Built collateral-free loan system using NER, RNN, clustering, and DeepFace-based liveness auth.

**Other internships:** Amazon (ML apprenticeship), IISc (YOLOv8 for drones), Brane Enterprises (backend dev).
""")

# --- EDUCATION SECTION ---
st.header("Education")
st.markdown("""
**University of Colorado Boulder**
- MS in Computer Science, Expected May 2027

**Dayananda Sagar College of Engineering**
- BE in Computer Science and Engineering, 2024 | CGPA: 8.78/10
""")

# --- PROJECTS SECTION ---
st.header("Key Projects")

with st.expander("Schizo AI"):
    st.write("""
    - Built explainable AI pipeline for early schizophrenia detection on EEG data.
    - Fine-tuned ResNet; used GradCAM, Streamlit UI, memory-efficient deployment (8GB RAM).
    - **Skills:** Deep Learning, XAI, GradCAM, Streamlit, FastAPI
    """)

with st.expander("Green Guru"):
    st.write("""
    - Smart agri advisor: predicts optimal crops, detects plant disease, chatbot for pesticide advice.
    - Integrates geolocation, weather API, soil data, NLP, and CV for farm support.
    - **Skills:** Deep Learning, NLP, Computer Vision, API integration
    """)

with st.expander("Tenali (Hackathon winner)"):
    st.write("""
    - ML project for court case urgency and automatic judgment suggestion; won Smart India Hackathon 2022.
    - NLP case matching, neural classifier, summary via BART.
    """)

# --- SKILLS SECTION ---
st.header("Technical Skills")
st.markdown("""
- **Languages:** Python, Go, C/C++, Java, Bash, SQL
- **Frameworks:** FastAPI, Flask, Streamlit, Docker, Kubernetes, GCP, AWS
- **AI/ML:** TensorFlow, PyTorch, scikit-learn, OpenCV, GradCAM, HuggingFace
- **Databases:** MongoDB, Cassandra, BigQuery, Firebase, Redis, Postgres
- **Visualization:** Prometheus, Grafana, Matplotlib, Seaborn
""")

# --- AWARDS & PUBLICATIONS ---
st.header("Awards & Achievements")
st.markdown("""
- 🏆 Smart India Hackathon Winner 2022 (@DRDO)
- 🥇 UNESCO India Africa Hackathon Finalist 2023
- 📰 Published: Explainable AI in Schizophrenia Detection, International Conference for Advanced Data Driven Intelligence (2024)
- 🥇 ServiceNow Certified Developer, Coursera ML, Infosys NLP
""")

# --- FOOTER ---
st.write("---")
st.write("© 2025 Dheeraj Gajula | Site built with Streamlit")
