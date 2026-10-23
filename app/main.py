import streamlit as st
import joblib
import os
import pandas as pd
import bcrypt
import base64
import plotly.express as px
from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Insurance Complaints Management",
    page_icon="🛡️",
    layout="wide"
)
# ============================================================
# LOAD CUSTOM CSS
# ============================================================
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Use the absolute path so it works on the cloud
css_path = os.path.join(BASE_DIR, "app", "style.css")
load_css(css_path)
# ============================================================
# HELPER — Load image as base64
# ============================================================
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# ============================================================
# LOAD MODELS
# ============================================================
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@st.cache_resource
def load_models():
    vectorizer = joblib.load(os.path.join(BASE_DIR, "models", "vectorizer.pkl"))
    subject_model = joblib.load(os.path.join(BASE_DIR, "models", "subject_model.pkl"))
    urgency_model = joblib.load(os.path.join(BASE_DIR, "models", "urgency_model.pkl"))
    sentiment_model = joblib.load(os.path.join(BASE_DIR, "models", "sentiment_model.pkl"))
    return vectorizer, subject_model, urgency_model, sentiment_model

if not os.path.exists(os.path.join(BASE_DIR, "models", "vectorizer.pkl")):
    st.error("⚠️ Models not found. Please check the models folder.")
    st.stop()

vectorizer, subject_model, urgency_model, sentiment_model = load_models()

# ============================================================
# FILES & HELPERS
# ============================================================
COMPLAINTS_FILE = os.path.join(BASE_DIR, "data", "submitted_complaints.csv")
USERS_FILE = os.path.join(BASE_DIR, "data", "users_hashed.csv")
AUDIT_FILE = os.path.join(BASE_DIR, "data", "audit_log.csv")

def load_complaints():
    if os.path.exists(COMPLAINTS_FILE):
        return pd.read_csv(COMPLAINTS_FILE)
    return pd.DataFrame(columns=[
        "id", "customer_name", "policy_number", "complaint_text",
        "subject", "urgency", "sentiment", "status", "date_submitted"
    ])

def save_complaint(complaint):
    df = load_complaints()
    new_id = len(df) + 1
    complaint["id"] = new_id
    complaint["status"] = "Open"
    complaint["date_submitted"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    df = pd.concat([df, pd.DataFrame([complaint])], ignore_index=True)
    df.to_csv(COMPLAINTS_FILE, index=False)
    return new_id

def load_users():
    return pd.read_csv(USERS_FILE)

def verify_password(password, hashed):
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False

def log_action(username, action, details=""):
    log_entry = pd.DataFrame([{
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "username": username,
        "action": action,
        "details": details
    }])
    if os.path.exists(AUDIT_FILE):
        log_entry.to_csv(AUDIT_FILE, mode='a', header=False, index=False)
    else:
        log_entry.to_csv(AUDIT_FILE, index=False)

# Feature B: Status Badge Helper
def status_badge(status):
    colors = {
        "Open": ("#f39c12", "#fff5e6"),
        "In Progress": ("#3498db", "#e6f4ff"),
        "Resolved": ("#27ae60", "#e6ffe6")
    }
    text_color, bg_color = colors.get(status, ("#666", "#f0f0f0"))
    return f"""
        <span style='background: {bg_color}; color: {text_color};
                     padding: 0.3rem 0.9rem; border-radius: 20px;
                     font-weight: 600; font-size: 0.85rem;
                     border: 1px solid {text_color}30;'>
            {status}
        </span>
    """

# ============================================================
# SESSION STATE
# ============================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.name = None

# ============================================================
# LOGIN & LANDING PAGE
# ============================================================
if "show_login" not in st.session_state:
    st.session_state.show_login = False

if not st.session_state.logged_in:
    
    if not st.session_state.show_login:
       
                # --- LANDING PAGE ---
        
        img_path = os.path.join(BASE_DIR, "app", "images", "hero.jpg")
        if os.path.exists(img_path):
            with open(img_path, "rb") as f:
                hero_b64 = base64.b64encode(f.read()).decode()
        else:
            hero_b64 = ""

        # Inject Full Screen CSS for Landing Page
        st.markdown(f"""
            <style>
            /* Force the app background to be the image ONLY on this page */
            [data-testid="stAppViewContainer"] {{
                background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.8)), url('data:image/jpeg;base64,{hero_b64}') !important;
                background-size: cover !important;
                background-position: center !important;
                background-attachment: fixed !important;
                background-repeat: no-repeat !important;
            }}
            
            /* Make the main container transparent so the image shows through */
            .main .block-container {{
                background-color: transparent !important;
                box-shadow: none !important;
            }}
            
            /* Hide Streamlit header */
            [data-testid="stHeader"] {{ background: transparent !important; }}
            
            /* Force ALL text to be white */
            .hero-text h1, .hero-text h1 * {{
                font-size: clamp(2rem, 8vw, 4.5rem) !important;
                white-space: nowrap !important;
                font-weight: 800 !important;
                line-height: 1.1 !important;
                color: #ffffff !important;
                -webkit-text-fill-color: #ffffff !important;
                font-family: Georgia, serif !important;
                text-shadow: 2px 2px 10px rgba(0,0,0,0.9) !important;
                border-bottom: none !important;
                margin: 0 !important;
            }}
            
            .hero-text p {{
                font-size: 1.2rem !important;
                max-width: 600px !important;
                margin: 20px auto !important;
                color: #ffffff !important;
                -webkit-text-fill-color: #ffffff !important;
                line-height: 1.5 !important;
                text-shadow: 1px 1px 5px rgba(0,0,0,0.9) !important;
            }}
            
            .hero-logo {{
                font-size: 2rem !important;
                font-weight: 900 !important;
                margin-bottom: 1rem !important;
                letter-spacing: 2px !important;
                color: #ffffff !important;
                -webkit-text-fill-color: #ffffff !important;
            }}
            </style>
        """, unsafe_allow_html=True)

        # Add spacing to push text down
        st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
        
        # The Text
        st.markdown("""
            <div class="hero-text" style='text-align: center;'>
                <div class="hero-logo">🛡️ ILYASHI</div>
                <h1>From Complaint<br>To Resolution</h1>
                <p>The AI-powered platform that always listens. 
                Submit your insurance complaints anywhere, anytime, and let our system route it to the right department instantly.</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)

        # The Buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Get Started", use_container_width=True, type="primary"):
                st.session_state.show_login = True
                st.rerun()
                
            st.markdown("<p style='text-align:center; color:white; margin-top:1rem; text-shadow: 1px 1px 3px black;'>Already have an account? <b>Log In</b></p>", unsafe_allow_html=True)
            if st.button("Log In", use_container_width=True):
                st.session_state.show_login = True
                st.rerun()
                
        st.stop()

 else:
        # --- SPLIT SCREEN LOGIN FORM ---
        
        # Create two columns: Left (Image), Right (Login)
        left_col, right_col = st.columns([1.2, 1], gap="large")

        with left_col:
            # Load and show the image on the left
            login_img_path = os.path.join(BASE_DIR, "app", "images", "login_image.jpg")
            if os.path.exists(login_img_path):
                st.image(login_img_path, use_container_width=True)
            else:
                # Fallback if image isn't uploaded yet
                st.markdown("<div style='height: 400px; background: #1e3c72; border-radius: 15px; display: flex; align-items: center; justify-content: center;'><h2 style='color: white;'>🛡️ ILYASHI</h2></div>", unsafe_allow_html=True)
            
            st.markdown("""
                <div style='margin-top: 20px;'>
                    <h2 style='color: white !important; font-size: 1.8rem; margin-bottom: 10px;'>Welcome to ILYASHI</h2>
                    <p style='color: #ddd; font-size: 1rem; line-height: 1.5;'>
                        Your AI-powered insurance complaint management platform. 
                        Log in to submit complaints, track resolutions, and view analytics.
                    </p>
                </div>
            """, unsafe_allow_html=True)

        with right_col:
            # Back button
            if st.button("← Back to Home"):
                st.session_state.show_login = False
                st.rerun()
                
            # White card for the login form
            st.markdown("""
                <div style='background-color: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); margin-top: 20px;'>
                    <h2 style='color: #1e3c72; margin-top: 0;'>Welcome back</h2>
                    <p style='color: #666; font-size: 0.9rem; margin-bottom: 20px;'>Log in to your account</p>
                </div>
            """, unsafe_allow_html=True)

            # The actual Streamlit form
            with st.form("login_form"):
                username = st.text_input("👤 Username", placeholder="Enter your username")
                password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
                
                st.markdown("<br>", unsafe_allow_html=True)
                login_btn = st.form_submit_button("Log In", use_container_width=True, type="primary")

                if login_btn:
                    users = load_users()
                    user_row = users[users["username"] == username]
                    if len(user_row) > 0:
                        stored_hash = user_row.iloc[0]["password"]
                        if verify_password(password, stored_hash):
                            st.session_state.logged_in = True
                            st.session_state.username = user_row.iloc[0]["username"]
                            st.session_state.role = user_row.iloc[0]["role"]
                            st.session_state.name = user_row.iloc[0]["name"]
                            st.session_state.show_login = False 
                            log_action(username, "LOGIN", "Successful login")
                            st.rerun()
                        else:
                            st.error("❌ Invalid password")
                    else:
                        st.error("❌ User not found")

            with st.expander("🔍 View Demo Accounts"):
                st.markdown("""
                    | Role | Username | Password |
                    |------|----------|----------|
                    | **Admin** | kent | admin2026 |
                    | **Officer** | jbanda | officer123 |
                    | **Viewer** | dmwale | viewer123 |
                """)
        st.stop()
# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    logo_b64 = get_base64_image("images/logo.png")
    if logo_b64:
        st.markdown(f"""
            <div style='text-align: center; padding: 1rem 0;'>
                <img src='data:image/png;base64,{logo_b64}' style='width: 80px;'/>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<h1 style='text-align:center; font-size:3rem; border:none;'>🛡️</h1>",
                    unsafe_allow_html=True)

    st.markdown("<h3 style='text-align:center; border:none;'>ICMS</h3>",
                unsafe_allow_html=True)
    st.markdown("<hr style='border-color: rgba(255,255,255,0.2);'>",
                unsafe_allow_html=True)

    st.markdown(f"""
        <div style='text-align: center; padding: 1rem;
                    background: rgba(255,255,255,0.12);
                    border-radius: 12px; margin-bottom: 1.5rem;
                    border: 1px solid rgba(255,255,255,0.2);'>
            <p style='margin: 0; font-size: 1.05rem; font-weight: 700;'>
                👤 {st.session_state.name}
            </p>
            <p style='margin: 0.3rem 0 0 0; font-size: 0.85rem; opacity: 0.85;'>
                🎭 {st.session_state.role}
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h4 style='border:none;'>📋 Navigation</h4>", unsafe_allow_html=True)
if st.button("☰ Open Menu", use_container_width=True):
    st.info("👉 Tap the `>` arrow in the top-left corner of the screen to open the menu.")   

menu_items = ["📝 Submit Complaint", "📋 View Complaints", "📊 Dashboard"]
if st.session_state.role == "Admin":
    menu_items.append("👥 Manage Users")
    menu_items.append("📜 Audit Log")

page = st.sidebar.radio("", menu_items, label_visibility="collapsed")

if st.sidebar.button("🚪 Logout", use_container_width=True):
    log_action(st.session_state.username, "LOGOUT", "User logged out")
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.name = None
    st.rerun()

# ============================================================
# PAGE 1: SUBMIT COMPLAINT
# ============================================================
if page == "📝 Submit Complaint":
    st.title("📝 Submit a Complaint")
    st.markdown("Fill in the form below. The AI will automatically classify your complaint.")

    with st.form("complaint_form"):
        col1, col2 = st.columns(2)
        with col1:
            customer_name = st.text_input("👤 Customer Name")
        with col2:
            policy_number = st.text_input("📄 Policy Number")

        complaint_text = st.text_area("💬 Complaint Description", height=150,
                                       placeholder="Describe your complaint in detail...")

        submitted = st.form_submit_button("🚀 Submit Complaint", use_container_width=True)

        if submitted:
            if complaint_text and customer_name:
                text_vec = vectorizer.transform([complaint_text])
                subject = subject_model.predict(text_vec)[0]
                urgency = urgency_model.predict(text_vec)[0]
                sentiment = sentiment_model.predict(text_vec)[0]

                complaint = {
                    "customer_name": customer_name,
                    "policy_number": policy_number,
                    "complaint_text": complaint_text,
                    "subject": subject,
                    "urgency": urgency,
                    "sentiment": sentiment
                }
                new_id = save_complaint(complaint)
                log_action(st.session_state.username, "SUBMIT_COMPLAINT", f"Complaint #{new_id}")

                st.success(f"✅ Complaint #{new_id} submitted successfully!")
                st.balloons()

                st.markdown("### 🤖 AI Analysis Results")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📂 Subject", subject)
                with col2:
                    st.metric("⚡ Urgency", urgency)
                with col3:
                    st.metric("😊 Sentiment", sentiment)

                st.markdown("### 🔀 Routing")
                routing_map = {
                    "Claim": "Claims Department",
                    "Payment": "Finance Department",
                    "Policy": "Policy Services",
                    "Premium": "Billing Department",
                    "Service": "Customer Service"
                }
                dept = routing_map.get(subject, "Customer Service")
                st.info(f"→ Routed to: **{dept}**")
            else:
                st.error("Please enter customer name and complaint description.")

# ============================================================
# PAGE 2: VIEW COMPLAINTS
# ============================================================
elif page == "📋 View Complaints":
    st.title("📋 All Complaints")

    df = load_complaints()

    if len(df) == 0:
        # Feature D: Empty State Illustration
        st.markdown("""
            <div style='text-align: center; padding: 4rem 2rem;
                        background: #f8f9fa; border-radius: 20px;
                        border: 2px dashed #667eea;'>
                <div style='font-size: 5rem;'>📭</div>
                <h3 style='color: #667eea !important;'>No complaints yet</h3>
                <p style='color: #888;'>Submit your first complaint to see it here.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Status", ["All"] + list(df["status"].unique()))
        with col2:
            subject_filter = st.selectbox("Subject", ["All"] + list(df["subject"].unique()))
        with col3:
            urgency_filter = st.selectbox("Urgency", ["All"] + list(df["urgency"].unique()))

        filtered = df.copy()
        if status_filter != "All":
            filtered = filtered[filtered["status"] == status_filter]
        if subject_filter != "All":
            filtered = filtered[filtered["subject"] == subject_filter]
        if urgency_filter != "All":
            filtered = filtered[filtered["urgency"] == urgency_filter]

        st.write(f"Showing **{len(filtered)}** of **{len(df)}** complaints")
        
        # Feature B: Status Badges in Table
        display_df = filtered.copy()
        display_df["status"] = display_df["status"].apply(status_badge)
        st.write(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)

        if st.session_state.role in ["Admin", "Officer"]:
            st.subheader("🔄 Update Complaint Status")
            complaint_id = st.number_input("Complaint ID", min_value=1, max_value=len(df), step=1)
            new_status = st.selectbox("New Status", ["Open", "In Progress", "Resolved"])

            if st.button("Update Status"):
                df.loc[df["id"] == complaint_id, "status"] = new_status
                df.to_csv(COMPLAINTS_FILE, index=False)
                log_action(st.session_state.username, "UPDATE_STATUS", f"Complaint #{complaint_id} → {new_status}")
                st.success(f"✅ Complaint #{complaint_id} updated to **{new_status}**")
                st.rerun()
        else:
            st.info("🔒 Viewers cannot update complaints.")

# ============================================================
# PAGE 3: DASHBOARD (Features A, D, E)
# ============================================================
elif page == "📊 Dashboard":
    
    # Feature A: Welcome Banner
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 2rem; border-radius: 15px; margin-bottom: 2rem;
                    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);'>
            <h1 style='color: white !important; border-bottom: none; margin: 0;'>
                👋 Welcome back, {st.session_state.name}!
            </h1>
            <p style='color: rgba(255,255,255,0.9); margin-top: 0.5rem;
                      font-size: 1rem;'>
                📅 {datetime.now().strftime("%A, %d %B %Y")}
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.title("📊 Analytics Dashboard")

    df = load_complaints()

    if len(df) == 0:
        # Feature D: Empty State Illustration
        st.markdown("""
            <div style='text-align: center; padding: 4rem 2rem;
                        background: #f8f9fa; border-radius: 20px;
                        border: 2px dashed #667eea;'>
                <div style='font-size: 4rem;'>📊</div>
                <h3 style='color: #667eea !important;'>No complaints yet</h3>
                <p style='color: #888;'>Submit your first complaint to see analytics here.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📋 Total", len(df))
        with col2:
            st.metric("🟡 Open", len(df[df["status"] == "Open"]))
        with col3:
            st.metric("🔵 In Progress", len(df[df["status"] == "In Progress"]))
        with col4:
            st.metric("🟢 Resolved", len(df[df["status"] == "Resolved"]))

        st.divider()

        # Feature E: Beautiful Plotly Charts
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📂 Complaints by Subject")
            subject_counts = df["subject"].value_counts().reset_index()
            subject_counts.columns = ["Subject", "Count"]
            fig = px.pie(
                subject_counts, names="Subject", values="Count", hole=0.45,
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=13)
            fig.update_layout(
                font=dict(family="Inter, Segoe UI", size=13),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                height=400, margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("⚡ Complaints by Urgency")
            urgency_counts = df["urgency"].value_counts().reset_index()
            urgency_counts.columns = ["Urgency", "Count"]
            fig = px.bar(
                urgency_counts, x="Urgency", y="Count", color="Urgency",
                color_discrete_map={"High": "#e74c3c", "Medium": "#f39c12", "Low": "#27ae60"},
                text="Count"
            )
            fig.update_traces(textposition='outside', textfont_size=14, marker_line_width=0)
            fig.update_layout(
                font=dict(family="Inter, Segoe UI", size=13),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False, height=400, xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.05)"),
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("😊 Complaints by Sentiment")
            sentiment_counts = df["sentiment"].value_counts().reset_index()
            sentiment_counts.columns = ["Sentiment", "Count"]
            fig = px.pie(
                sentiment_counts, names="Sentiment", values="Count", hole=0.45, color="Sentiment",
                color_discrete_map={"Negative": "#e74c3c", "Neutral": "#95a5a6", "Positive": "#27ae60"}
            )
            fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=13)
            fig.update_layout(
                font=dict(family="Inter, Segoe UI", size=13),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                height=400, margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("🔄 Complaints by Status")
            status_counts = df["status"].value_counts().reset_index()
            status_counts.columns = ["Status", "Count"]
            fig = px.bar(
                status_counts, x="Status", y="Count", color="Status",
                color_discrete_map={"Open": "#f39c12", "In Progress": "#3498db", "Resolved": "#27ae60"},
                text="Count"
            )
            fig.update_traces(textposition='outside', textfont_size=14, marker_line_width=0)
            fig.update_layout(
                font=dict(family="Inter, Segoe UI", size=13),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False, height=400, xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.05)"),
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)

        st.divider()
        st.subheader("📥 Export Data")
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Complaints as CSV",
            data=csv,
            file_name="complaints_export.csv",
            mime="text/csv"
        )

# ============================================================
# PAGE 4: MANAGE USERS
# ============================================================
elif page == "👥 Manage Users":
    st.title("👥 Manage Users")

    users = load_users()
    display_users = users.copy()
    display_users["password"] = "••••••••"
    st.dataframe(display_users, use_container_width=True)

    st.subheader("➕ Add New User")
    with st.form("add_user_form"):
        col1, col2 = st.columns(2)
        with col1:
            new_username = st.text_input("Username")
            new_role = st.selectbox("Role", ["Admin", "Officer", "Viewer"])
        with col2:
            new_password = st.text_input("Password", type="password")
            new_name = st.text_input("Full Name")

        if st.form_submit_button("Add User"):
            if new_username and new_password and new_name:
                hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                new_user = pd.DataFrame([{
                    "username": new_username,
                    "password": hashed,
                    "role": new_role,
                    "name": new_name
                }])
                users = pd.concat([users, new_user], ignore_index=True)
                users.to_csv(USERS_FILE, index=False)
                log_action(st.session_state.username, "ADD_USER", f"Added {new_username}")
                st.success(f"✅ User **{new_username}** added.")
                st.rerun()
            else:
                st.error("Please fill in all fields.")

# ============================================================
# PAGE 5: AUDIT LOG
# ============================================================
elif page == "📜 Audit Log":
    st.title("📜 Audit Log")
    if os.path.exists(AUDIT_FILE):
        logs = pd.read_csv(AUDIT_FILE)
        st.dataframe(logs.tail(100), use_container_width=True)
    else:
        st.info("No audit logs yet.")
