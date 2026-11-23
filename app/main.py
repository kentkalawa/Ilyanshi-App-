import streamlit as st
import joblib
import os
import pandas as pd
import bcrypt
import base64
import html
import plotly.express as px
from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Ilyashi Insurance Portal",
    page_icon="🛡️",
    layout="wide"
)

# ============================================================
# LOAD CUSTOM CSS
# ============================================================
def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
css_path = os.path.join(BASE_DIR, "app", "style.css")
load_css(css_path)

FIX_CSS = """
<style>
/* ---- text areas ---- */
[data-testid="stTextArea"] [data-baseweb],
[data-testid="stTextArea"] textarea {
    background: #eaf2ff !important;
    background-color: #eaf2ff !important;
    color: #0f1b2a !important;
    -webkit-text-fill-color: #0f1b2a !important;
    caret-color: #0f1b2a !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}
[data-testid="stTextArea"] [data-baseweb="textarea"] {
    border: 1px solid #bfdbfe !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}
[data-testid="stTextArea"] [data-baseweb="textarea"]:focus-within {
    border-color: #1f6feb !important;
    box-shadow: 0 0 0 1px #1f6feb !important;
}
/* ---- dropdown boxes ---- */
[data-testid="stSelectbox"] > div:not([data-testid="stWidgetLabel"]),
[data-testid="stSelectbox"] > div:not([data-testid="stWidgetLabel"]) *,
[data-testid="stSelectbox"] [data-baseweb="select"],
[data-testid="stSelectbox"] [data-baseweb="select"] * {
    background: #eaf2ff !important;
    background-color: #eaf2ff !important;
    color: #0f1b2a !important;
    -webkit-text-fill-color: #0f1b2a !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    border: 1px solid #bfdbfe !important;
    border-radius: 8px !important;
}
[data-testid="stSelectbox"] svg { fill: #0f1b2a !important; }
/* ---- number boxes ---- */
[data-testid="stNumberInput"] [data-baseweb],
[data-testid="stNumberInput"] input,
[data-testid="stNumberInputStepUp"],
[data-testid="stNumberInputStepDown"] {
    background: #eaf2ff !important;
    background-color: #eaf2ff !important;
    color: #0f1b2a !important;
    -webkit-text-fill-color: #0f1b2a !important;
}
[data-testid="stNumberInput"] svg { fill: #0f1b2a !important; }
/* ---- open dropdown lists ---- */
[role="listbox"], [role="listbox"] ul { background: #ffffff !important; }
[role="option"] { background: #ffffff !important; color: #0f1b2a !important; }
[role="option"]:hover, [role="option"][aria-selected="true"] { background: #eaf2ff !important; }
/* ---- message boxes ---- */
[data-testid="stAlert"],
[data-testid="stAlertContainer"] {
    background: #eaf2ff !important;
    background-color: #eaf2ff !important;
    border: 1px solid #bfdbfe !important;
    border-radius: 10px !important;
}
[data-testid="stAlert"] *,
[data-testid="stAlertContainer"] * {
    color: #0f1b2a !important;
}
/* ---- confidence pills under the AI results ---- */
[data-testid="stMetricDelta"] {
    background: #1f6feb !important;
    background-color: #1f6feb !important;
    border-radius: 999px !important;
    padding: 3px 14px !important;
    width: fit-content !important;
}
[data-testid="stMetricDelta"],
[data-testid="stMetricDelta"] * {
    color: #ffffff !important;
    fill: #ffffff !important;
}
[data-testid="stMetricDelta"] svg { display: none !important; }
/* ---- stat cards: outline with a coloured top edge ---- */
[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid #bfdbfe !important;
    border-top: 4px solid #1f6feb !important;
    border-radius: 10px !important;
    padding: 14px 18px !important;
    box-shadow: 0 1px 4px rgba(15, 27, 42, 0.08) !important;
}
.st-key-dash_stats [data-testid="stColumn"]:nth-child(1) [data-testid="stMetric"],
.st-key-dash_stats [data-testid="column"]:nth-child(1) [data-testid="stMetric"] { border-top-color: #1f6feb !important; }
.st-key-dash_stats [data-testid="stColumn"]:nth-child(2) [data-testid="stMetric"],
.st-key-dash_stats [data-testid="column"]:nth-child(2) [data-testid="stMetric"] { border-top-color: #f59e0b !important; }
.st-key-dash_stats [data-testid="stColumn"]:nth-child(3) [data-testid="stMetric"],
.st-key-dash_stats [data-testid="column"]:nth-child(3) [data-testid="stMetric"] { border-top-color: #60a5fa !important; }
.st-key-dash_stats [data-testid="stColumn"]:nth-child(4) [data-testid="stMetric"],
.st-key-dash_stats [data-testid="column"]:nth-child(4) [data-testid="stMetric"] { border-top-color: #10b981 !important; }
.st-key-my_stats [data-testid="stColumn"]:nth-child(1) [data-testid="stMetric"],
.st-key-my_stats [data-testid="column"]:nth-child(1) [data-testid="stMetric"] { border-top-color: #f59e0b !important; }
.st-key-my_stats [data-testid="stColumn"]:nth-child(2) [data-testid="stMetric"],
.st-key-my_stats [data-testid="column"]:nth-child(2) [data-testid="stMetric"] { border-top-color: #60a5fa !important; }
.st-key-my_stats [data-testid="stColumn"]:nth-child(3) [data-testid="stMetric"],
.st-key-my_stats [data-testid="column"]:nth-child(3) [data-testid="stMetric"] { border-top-color: #10b981 !important; }
.st-key-dash_stats2 [data-testid="stColumn"]:nth-child(1) [data-testid="stMetric"],
.st-key-dash_stats2 [data-testid="column"]:nth-child(1) [data-testid="stMetric"] { border-top-color: #1f6feb !important; }
.st-key-dash_stats2 [data-testid="stColumn"]:nth-child(2) [data-testid="stMetric"],
.st-key-dash_stats2 [data-testid="column"]:nth-child(2) [data-testid="stMetric"] { border-top-color: #10b981 !important; }
.st-key-dash_stats2 [data-testid="stColumn"]:nth-child(3) [data-testid="stMetric"],
.st-key-dash_stats2 [data-testid="column"]:nth-child(3) [data-testid="stMetric"] { border-top-color: #ef4444 !important; }
/* ---- simulated notification cards ---- */
.ily-note {
    border: 1px solid #bfdbfe;
    border-left: 4px solid #1f6feb;
    border-radius: 10px;
    background: #ffffff;
    padding: 12px 16px;
    margin-bottom: 10px;
}
.ily-note.sms { border-left-color: #10b981; }
.ily-note-head { display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap; color: #3a5a8c; font-size: 0.85rem; margin-bottom: 6px; }
.ily-note-body { color: #0f1b2a; }
.ily-note-foot { font-size: 0.8rem; margin-top: 6px; font-weight: 600; }
/* ---- tables ---- */
.ily-table-wrap {
    overflow: auto;
    border: 1px solid #bfdbfe;
    border-radius: 12px;
    background: #ffffff;
    margin-bottom: 1rem;
}
.ily-table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
.ily-table thead th {
    position: sticky; top: 0;
    background: #1f6feb !important;
    color: #ffffff !important;
    text-align: left !important;
    padding: 10px 14px !important;
    font-weight: 600 !important;
    white-space: nowrap;
    border: none !important;
    border-right: 1px solid rgba(255, 255, 255, 0.45) !important;
}
.ily-table thead th:last-child { border-right: none !important; }
.ily-table tbody td {
    padding: 9px 14px !important;
    color: #0f1b2a !important;
    background: #ffffff !important;
    border: 1px solid #bfdbfe !important;
}
.ily-table tbody td { min-width: 110px; }
.ily-table tbody td:first-child { border-left: none !important; white-space: nowrap; }
.ily-table tbody td:last-child { border-right: none !important; }
.ily-table tbody tr:first-child td { border-top: none !important; }
.ily-table tbody tr:nth-child(even) td { background: #f5f9ff !important; }
.ily-table tbody tr:hover td { background: #eaf2ff !important; }
</style>
"""
st.markdown(FIX_CSS, unsafe_allow_html=True)

# ============================================================
# LOAD MODELS
# ============================================================
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
CONTACTS_FILE = os.path.join(BASE_DIR, "data", "contacts.csv")
NOTIFY_FILE = os.path.join(BASE_DIR, "data", "notifications.csv")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
ROUTING_MAP = {"Claim": "Claims Department", "Payment": "Finance Department", "Policy": "Policy Services", "Premium": "Billing Department", "Service": "Customer Service"}
os.makedirs(UPLOAD_DIR, exist_ok=True)

@st.cache_data(ttl=0)
def load_complaints():
    if os.path.exists(COMPLAINTS_FILE):
        df = pd.read_csv(COMPLAINTS_FILE)
        df = df.drop(columns=["policy_number"], errors="ignore")
        if "attachment" not in df.columns:
            df["attachment"] = ""
        if "submitted_by" not in df.columns:
            df["submitted_by"] = ""
        df["submitted_by"] = df["submitted_by"].fillna("")
        if "date_updated" not in df.columns:
            df["date_updated"] = df["date_submitted"]
        df["date_updated"] = df["date_updated"].fillna(df["date_submitted"])
        if "date_resolved" not in df.columns:
            df["date_resolved"] = ""
        df["date_resolved"] = df["date_resolved"].fillna("").astype(str)
        backfill = (df["status"] == "Resolved") & (df["date_resolved"] == "") & (df["date_updated"].astype(str) != df["date_submitted"].astype(str))
        df.loc[backfill, "date_resolved"] = df.loc[backfill, "date_updated"].astype(str)
        if "reference" not in df.columns:
            years = df["date_submitted"].astype(str).str[:4]
            df.insert(1, "reference", [f"ILY-{y}-{int(i):04d}" for y, i in zip(years, df["id"])])
        return df
    return pd.DataFrame(columns=["id", "reference", "customer_name", "complaint_text", "subject", "urgency", "sentiment", "status", "date_submitted", "attachment", "submitted_by", "date_updated", "date_resolved"])

def save_complaint(complaint):
    df = load_complaints()
    new_id = int(df["id"].max()) + 1 if len(df) else 1
    complaint["id"] = new_id
    complaint["reference"] = f"ILY-{datetime.now().year}-{new_id:04d}"
    complaint["status"] = "Open"
    complaint["date_submitted"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    complaint["date_updated"] = complaint["date_submitted"]
    complaint["date_resolved"] = ""
    if "attachment" not in complaint:
        complaint["attachment"] = ""
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

def filter_for_user(df):
    if st.session_state.role == "Officer":
        if st.session_state.username == "jbanda":
            return df[df["subject"].isin(["Claim", "Payment"])]
        if st.session_state.username == "mphiri":
            return df[df["subject"].isin(["Policy", "Premium"])]
    return df

def go_to(page_name):
    if page_name in ("Settings", "Help Center"):
        st.session_state.extra_page = page_name
    else:
        st.session_state.extra_page = None
        st.session_state.nav_radio = page_name

def clear_extra_page():
    st.session_state.extra_page = None

def select_page(name):
    st.session_state.nav_radio = name
    st.session_state.extra_page = None

def style_chart(fig, keep_titles=False):
    """Dark, readable text on a white page, with room for axis labels."""
    dark = "#0f1b2a"
    is_pie = any(getattr(t, "type", "") == "pie" for t in fig.data)
    fig.update_layout(
        font=dict(color=dark),
        margin=dict(l=20, r=20, t=30, b=20) if is_pie else dict(l=45, r=20, t=30, b=55),
    )
    if not is_pie:
        fig.update_xaxes(automargin=True, tickfont=dict(color=dark), linecolor="#93c5fd")
        fig.update_yaxes(automargin=True, tickfont=dict(color=dark), linecolor="#93c5fd")
        if not keep_titles:
            fig.update_xaxes(title_text="")
            fig.update_yaxes(title_text="")
        try:
            ymax = max(max(t.y) for t in fig.data if getattr(t, "y", None) is not None)
            if ymax <= 10:
                fig.update_yaxes(dtick=1)
        except Exception:
            pass
    return fig

def show_table(df, max_height=420):
    """Light, readable table that does not depend on Streamlit's theme."""
    clean = df.fillna("").astype(str)
    clean = clean.apply(lambda c: c.str.replace(r"\s+", " ", regex=True).str.strip())
    names = {"reference": "Reference ID"}
    clean.columns = [names.get(c, str(c).replace("_", " ").title()) for c in clean.columns]
    table = clean.to_html(index=False, escape=True, border=0, classes="ily-table")
    table = " ".join(table.split())
    st.markdown(
        "<div class='ily-table-wrap' style='max-height:" + str(max_height) + "px;'>" + table + "</div>",
        unsafe_allow_html=True,
    )

ESCALATION_HOURS = 24  # High-urgency complaints still unresolved after this many hours are escalated

def add_escalation(df):
    """Adds a True/False 'escalated' column."""
    df = df.copy()
    submitted = pd.to_datetime(df["date_submitted"], errors="coerce")
    age_hours = (datetime.now() - submitted).dt.total_seconds() / 3600
    df["escalated"] = (df["urgency"] == "High") & (df["status"] != "Resolved") & (age_hours > ESCALATION_HOURS)
    return df

def resolution_hours(df):
    """Average hours from submitted to resolved (None if nothing measurable yet)."""
    done = df[(df["status"] == "Resolved") & (df["date_resolved"].astype(str) != "")]
    if len(done) == 0:
        return None
    start = pd.to_datetime(done["date_submitted"], errors="coerce")
    end = pd.to_datetime(done["date_resolved"], errors="coerce")
    hours = ((end - start).dt.total_seconds() / 3600).dropna()
    return None if hours.empty else float(hours.mean())

def format_hours(h):
    """Whole numbers only: minutes, hours or days."""
    if h is None:
        return "—"
    if h < 1:
        return f"{round(h * 60)} min"
    if h < 24:
        n = round(h)
        return f"{n} hour" + ("" if n == 1 else "s")
    n = round(h / 24)
    return f"{n} day" + ("" if n == 1 else "s")

# ---------- Simulated notifications (nothing is really sent) ----------
NOTIFY_COLUMNS = ["timestamp", "channel", "to_user", "to_name", "destination", "reference", "event", "subject", "message", "status"]
CHANNEL_CHOICES = ["Email", "SMS", "Both", "None"]
DEPARTMENT_OFFICER = {"Claim": "jbanda", "Payment": "jbanda", "Policy": "mphiri", "Premium": "mphiri"}
STATUS_MESSAGES = {
    "Open": "ILYASHI: Your complaint {ref} has been reopened.",
    "In Progress": "ILYASHI: Your complaint {ref} is now being handled by our team.",
    "Resolved": "ILYASHI: Your complaint {ref} has been resolved. Quote this Reference ID if you need more help.",
}

def live_sms_enabled():
    """True only when Africa's Talking keys are saved in Streamlit secrets."""
    try:
        return bool(st.secrets.get("AT_API_KEY")) and bool(st.secrets.get("AT_USERNAME"))
    except Exception:
        return False

def to_international(phone):
    """0971234567 or 260971234567 -> +260971234567"""
    p = "".join(ch for ch in str(phone) if ch.isdigit() or ch == "+")
    if p.startswith("+"):
        return p
    if p.startswith("00"):
        return "+" + p[2:]
    if p.startswith("260"):
        return "+" + p
    if p.startswith("0"):
        return "+260" + p[1:]
    return "+260" + p

def send_real_sms(phone, message):
    """Sends a real SMS through Africa's Talking. Returns (ok, detail). Never raises."""
    try:
        import africastalking
        africastalking.initialize(st.secrets["AT_USERNAME"], st.secrets["AT_API_KEY"])
        sender = st.secrets.get("AT_SENDER_ID") or None
        response = africastalking.SMS.send(message, [to_international(phone)], sender_id=sender)
        data = response.get("SMSMessageData", {})
        recipients = data.get("Recipients", [])
        if recipients and recipients[0].get("statusCode") in (100, 101, 102):
            return True, "sent"
        reason = recipients[0].get("status") if recipients else data.get("Message", "no response")
        return False, str(reason)
    except Exception as e:
        return False, str(e)[:120]

def get_contact(username):
    default = {"channel": "Email", "email": f"{username}@ilyashi.demo", "phone": ""}
    if os.path.exists(CONTACTS_FILE):
        contacts = pd.read_csv(CONTACTS_FILE, dtype=str, keep_default_na=False)
        row = contacts[contacts["username"] == username]
        if len(row) > 0:
            r = row.iloc[0]
            return {"channel": r["channel"] or default["channel"],
                    "email": r["email"] or default["email"],
                    "phone": r["phone"]}
    return default

def save_contact(username, channel, email, phone):
    new_row = pd.DataFrame([{"username": username, "channel": channel, "email": email, "phone": phone}])
    if os.path.exists(CONTACTS_FILE):
        contacts = pd.read_csv(CONTACTS_FILE, dtype=str, keep_default_na=False)
        contacts = contacts[contacts["username"] != username]
        contacts = pd.concat([contacts, new_row], ignore_index=True)
    else:
        contacts = new_row
    contacts.to_csv(CONTACTS_FILE, index=False)

def load_notifications():
    if os.path.exists(NOTIFY_FILE):
        return pd.read_csv(NOTIFY_FILE, dtype=str, keep_default_na=False)
    return pd.DataFrame(columns=NOTIFY_COLUMNS)

def notify(username, event, reference, message):
    """Simulates sending an SMS / email. Returns how many messages were logged."""
    contact = get_contact(username)
    channels = {"Email": ["Email"], "SMS": ["SMS"], "Both": ["Email", "SMS"], "None": []}.get(contact["channel"], ["Email"])
    try:
        users = load_users()
        match = users[users["username"] == username]
        to_name = match.iloc[0]["name"] if len(match) else username
    except Exception:
        to_name = username
    rows = []
    for ch in channels:
        destination = contact["email"] if ch == "Email" else contact["phone"]
        if ch == "SMS" and not destination:
            destination = "(no phone number saved)"
            status = "Failed (simulated): add a phone number in Settings"
        elif ch == "SMS" and live_sms_enabled():
            ok, detail = send_real_sms(destination, message)
            status = "Delivered (live SMS)" if ok else f"Failed (live SMS): {detail}"
        else:
            status = "Delivered (simulated)"
        rows.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "channel": ch, "to_user": username, "to_name": to_name,
            "destination": destination, "reference": reference, "event": event,
            "subject": f"ILYASHI: {event}" if ch == "Email" else "",
            "message": message, "status": status,
        })
    if rows:
        out = pd.DataFrame(rows, columns=NOTIFY_COLUMNS)
        if os.path.exists(NOTIFY_FILE):
            out.to_csv(NOTIFY_FILE, mode="a", header=False, index=False)
        else:
            out.to_csv(NOTIFY_FILE, index=False)
    return len(rows)

def send_escalation_alerts():
    """Alerts the responsible officer once for each newly escalated complaint."""
    esc = add_escalation(load_complaints())
    esc = esc[esc["escalated"]]
    if esc.empty:
        return
    users = load_users()
    sent = load_notifications()
    for _, r in esc.iterrows():
        officer = DEPARTMENT_OFFICER.get(r["subject"])
        recipients = [officer] if officer else users[users["role"] == "Admin"]["username"].tolist()
        for u in recipients:
            already = ((sent["reference"] == r["reference"]) & (sent["to_user"] == u) & (sent["event"] == "Escalation alert")).any()
            if not already:
                notify(u, "Escalation alert", r["reference"],
                       f"ILYASHI ALERT: {r['reference']} ({r['subject']}, high urgency) is still unresolved after {ESCALATION_HOURS} hours. Please act now.")
                sent = load_notifications()

def notification_card(r):
    is_email = r["channel"] == "Email"
    ok = str(r["status"]).startswith("Delivered")
    colour = "#10b981" if ok else "#ef4444"
    icon = "✉️" if is_email else "📱"
    subject = f"<b>{html.escape(r['subject'])}</b><br>" if is_email and r["subject"] else ""
    return (
        f"<div class='ily-note {'email' if is_email else 'sms'}'>"
        f"<div class='ily-note-head'><span>{icon} <b>{html.escape(r['channel'])}</b> to {html.escape(r['to_name'])} ({html.escape(r['destination'])})</span>"
        f"<span>{html.escape(r['timestamp'])}</span></div>"
        f"<div class='ily-note-body'>{subject}{html.escape(r['message'])}</div>"
        f"<div class='ily-note-foot' style='color:{colour};'>{html.escape(r['status'])} · {html.escape(str(r['reference']))}</div>"
        f"</div>"
    )

def do_logout():
    log_action(st.session_state.username, "LOGOUT", "User logged out")
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.name = None
    st.session_state.extra_page = None
    st.session_state.pop("nav_radio", None)

LANGUAGES = {"English": "en", "Nyanja": "ny"}

TRANSLATIONS = {
    "ny": {
        "Settings": "Zokonda",
        "Help Center": "Thandizo",
        "Notifications": "Zidziwitso",
        "Language": "Chilankhulo",
    }
}

def t(text):
    lang = st.session_state.get("lang", "en")
    return TRANSLATIONS.get(lang, {}).get(text, text)

def set_language():
    st.session_state.lang = LANGUAGES[st.session_state.lang_choice]

# ============================================================
# SESSION STATE
# ============================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.name = None

if "show_login" not in st.session_state:
    st.session_state.show_login = False

if "nav_page" not in st.session_state:
    st.session_state.nav_page = None

if "extra_page" not in st.session_state:
    st.session_state.extra_page = None

if "lang" not in st.session_state:
    st.session_state.lang = "en"

# ============================================================
# LANDING PAGE + LOGIN (split-screen)
# ============================================================
LOGIN_CSS = """
<style>
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #ffffff !important;
    background-image: none !important;
}
[data-testid="stMainBlockContainer"], .main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
[data-testid="stHorizontalBlock"] { gap: 0 !important; }

.st-key-login_left {
    height: 100vh !important;
    min-height: 100vh !important;
    width: 100% !important;
    background-image: linear-gradient(rgba(0,0,0,0.25), rgba(0,0,0,0.25)), url('data:image/jpeg;base64,__HERO__') !important;
    background-size: cover !important;
    background-position: center !important;
    background-repeat: no-repeat !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 0 !important;
}
.login-card {
    background: rgba(25, 80, 170, 0.80);
    padding: 30px 34px;
    border-radius: 6px;
    max-width: 520px;
    text-align: center;
    margin: 0 auto !important;
}
.login-card h2 {
    color: #ffffff !important;
    font-size: 2rem !important;
    font-weight: 600 !important;
    margin: 0 0 14px 0 !important;
    border: none !important;
}
.login-card p {
    color: #ffffff !important;
    font-size: 1.05rem !important;
    line-height: 1.5 !important;
    margin: 0 0 14px 0 !important;
}
.login-stats { display: flex; justify-content: space-around; margin-top: 18px; }
.login-stats div { color: #ffffff; text-align: center; }
.login-stats b { display: block; font-size: 1.4rem; }
.login-stats span { font-size: 0.95rem; }

.st-key-login_panel {
    background: #ffffff;
    min-height: 100vh;
    padding: 60px 9% 30px 9%;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.st-key-login_panel h2,
.st-key-login_panel p,
.st-key-login_panel label,
.st-key-login_panel label p {
    color: #0f1b2a !important;
    border: none !important;
}
.st-key-login_panel [data-testid="stTextInputRootElement"] {
    background: #eaf2ff !important;
    border: 1px solid #bfdbfe !important;
    border-radius: 8px !important;
    box-shadow: none !important;
    overflow: hidden !important;
}
.st-key-login_panel [data-testid="stTextInputRootElement"]:focus-within {
    border-color: #1f6feb !important;
    box-shadow: 0 0 0 1px #1f6feb !important;
}
.st-key-login_panel [data-testid="stTextInputRootElement"] > div,
.st-key-login_panel [data-baseweb="input"],
.st-key-login_panel [data-baseweb="base-input"] {
    background: #eaf2ff !important;
    background-color: #eaf2ff !important;
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    outline: none !important;
}
.st-key-login_panel input,
.st-key-login_panel input:focus,
.st-key-login_panel input:-webkit-autofill {
    background: #eaf2ff !important;
    background-color: #eaf2ff !important;
    color: #0f1b2a !important;
    -webkit-text-fill-color: #0f1b2a !important;
    caret-color: #0f1b2a !important;
    border: none !important;
    outline: none !important;
    -webkit-box-shadow: 0 0 0 1000px #eaf2ff inset !important;
}
.st-key-login_panel [data-testid="stTextInputRootElement"] button {
    background: #eaf2ff !important;
    background-color: #eaf2ff !important;
    border: none !important;
    box-shadow: none !important;
}
.st-key-login_panel [data-testid="stTextInputRootElement"] button svg {
    fill: #3a5a8c !important;
    color: #3a5a8c !important;
}
.st-key-login_panel input::placeholder {
    color: #3a5a8c !important;
    -webkit-text-fill-color: #3a5a8c !important;
}
.st-key-login_panel [data-testid="stForm"] { border: none !important; padding: 0 !important; }
.st-key-login_panel [data-testid="stFormSubmitButton"] button,
.st-key-login_panel [data-testid="stBaseButton-primaryFormSubmit"],
.st-key-login_panel button[data-testid="stBaseButton-primaryFormSubmit"],
.st-key-login_panel button[kind="primaryFormSubmit"] {
    background: #1f6feb !important;
    background-color: #1f6feb !important;
    border: 1px solid #1f6feb !important;
    border-radius: 8px !important;
    color: #ffffff !important;
    font-weight: 600 !important;
}
.st-key-login_panel [data-testid="stFormSubmitButton"] button:hover,
.st-key-login_panel [data-testid="stBaseButton-primaryFormSubmit"]:hover,
.st-key-login_panel button[kind="primaryFormSubmit"]:hover {
    background: #388bfd !important;
    background-color: #388bfd !important;
    border-color: #388bfd !important;
}
.st-key-login_panel [data-testid="stFormSubmitButton"] button p,
.st-key-login_panel button p { color: #ffffff !important; }

.st-key-login_panel p.login-sub { color: #3a5a8c !important; }

@media (max-width: 768px) {
    .st-key-login_left { display: none !important; }
    .st-key-login_panel { padding: 40px 24px !important; min-height: auto; }
}
</style>
"""

if not st.session_state.logged_in:

    img_path = os.path.join(BASE_DIR, "app", "images", "hero.jpg")
    hero_b64 = ""
    if os.path.exists(img_path):
        with open(img_path, "rb") as f:
            hero_b64 = base64.b64encode(f.read()).decode()

    logo_file = os.path.join(BASE_DIR, "app", "images", "logo.png")
    if os.path.exists(logo_file):
        with open(logo_file, "rb") as f:
            logo_data = base64.b64encode(f.read()).decode()
        logo_html = "<img src='data:image/png;base64," + logo_data + "' style='height:70px; margin-bottom:24px;'/>"
    else:
        logo_html = "<div style='font-size:2rem; font-weight:900; letter-spacing:2px; color:#1f4fbf; margin-bottom:24px;'>🛡️ ILYASHI</div>"

    st.markdown(LOGIN_CSS.replace("__HERO__", hero_b64), unsafe_allow_html=True)

    left, right = st.columns([1.15, 1])

    with left:
        with st.container(key="login_left"):
            st.markdown(
                "<div class='login-card'>"
                "<h2>Welcome to ILYASHI</h2>"
                "<p>The AI-powered platform that always listens. Submit your insurance complaints anywhere, anytime, and let our system route them to the right department instantly.</p>"
                "<div class='login-stats'>"
                "<div><b>3</b><span>AI models</span></div>"
                "<div><b>5</b><span>departments</span></div>"
                "<div><b>24/7</b><span>access</span></div>"
                "</div></div>",
                unsafe_allow_html=True,
            )

    with right:
        with st.container(key="login_panel"):
            st.markdown(logo_html, unsafe_allow_html=True)
            st.markdown(
                "<h2 style='font-size:2.2rem; font-weight:500; margin:0 0 4px 0;'>Welcome back</h2>"
                "<p class='login-sub' style='margin:0 0 24px 0;'>Log in to the ILYASHI Insurance Portal</p>",
                unsafe_allow_html=True,
            )

            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                login_btn = st.form_submit_button("Log in", use_container_width=True, type="primary")

                if login_btn:
                    users = load_users()
                    user_row = users[users["username"] == username]
                    if len(user_row) > 0 and verify_password(password, user_row.iloc[0]["password"]):
                        st.session_state.logged_in = True
                        st.session_state.username = user_row.iloc[0]["username"]
                        st.session_state.role = user_row.iloc[0]["role"]
                        st.session_state.name = user_row.iloc[0]["name"]
                        log_action(username, "LOGIN", "Successful login")
                        st.rerun()
                    else:
                        log_action(username or "unknown", "LOGIN_FAILED", "Invalid credentials")
                        st.error("❌ Invalid username or password")

            st.markdown(
                "<p class='login-sub' style='text-align:center; margin-top:18px; font-size:0.9rem;'>Forgot your password? Contact IT Support: support@ilyashi.co.zm</p>"
                "<p class='login-sub' style='text-align:center; margin-top:30px; font-size:0.8rem;'>© 2026 ILYASHI Insurance. All rights reserved.</p>",
                unsafe_allow_html=True,
            )
    st.stop()

# ============================================================
# SIDEBAR (OPERATIONS ONLY)
# ============================================================
with st.sidebar:
    logo_b64 = None
    logo_path = os.path.join(BASE_DIR, "app", "images", "logo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()

    if logo_b64:
        st.markdown(f"""
            <div style='text-align: center; padding: 1rem 0;'>
                <img src='data:image/png;base64,{logo_b64}' style='width: 80px;'/>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<h1 style='text-align:center; font-size:3rem; border:none;'>🛡️</h1>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align:center; border:none; letter-spacing: 4px;'>ILYASHI</h3>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: rgba(255,255,255,0.2);'>", unsafe_allow_html=True)

    # User Profile Card
    st.markdown(f"""
        <div style='text-align: center; padding: 1rem;
                    background: rgba(31,111,235,0.18);
                    border-radius: 12px; margin-bottom: 1.5rem;
                    border: 1px solid rgba(96,165,250,0.55);'>
            <p style='margin: 0; font-size: 1.05rem; font-weight: 700;'>
                {st.session_state.name}
            </p>
            <p style='margin: 0.3rem 0 0 0; font-size: 0.85rem; opacity: 0.85;'>
                {st.session_state.role}
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar Navigation (Operations only)
    menu_items = ["Dashboard", "Submit Complaint"]
    if st.session_state.role in ("Admin", "Officer"):
        menu_items.append("View Complaints")
    if st.session_state.role == "Viewer":
        menu_items.append("My Complaints")
    if st.session_state.role == "Admin":
        menu_items.append("Manage Users")
        menu_items.append("Audit Log")
        menu_items.append("Export Data")

    # Settings and Help Center sit at the bottom of the menu for all roles
    menu_items.append("Notifications")
    menu_items.append("Settings")
    menu_items.append("Help Center")

    if st.session_state.get("nav_radio") not in menu_items:
        st.session_state.nav_radio = "Dashboard"

    with st.container(key="side_nav"):
        for i, item in enumerate(menu_items):
            is_active = (st.session_state.nav_radio == item) and not st.session_state.extra_page
            st.button(t(item), key=f"nav_{i}", on_click=select_page, args=(item,),
                      use_container_width=True,
                      type="primary" if is_active else "secondary")

    page = st.session_state.extra_page or st.session_state.nav_radio
    if page == "View Complaints" and st.session_state.role not in ("Admin", "Officer"):
        page = "Dashboard"
    if page == "My Complaints" and st.session_state.role != "Viewer":
        page = "Dashboard"
    if page in ("Manage Users", "Audit Log", "Export Data") and st.session_state.role != "Admin":
        page = "Dashboard"

    st.button("Logout", key="sidebar_logout", on_click=do_logout, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# PAGE 1: DASHBOARD
# ============================================================
if page == "Dashboard":
    if st.session_state.role in ("Admin", "Officer"):
        send_escalation_alerts()
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        if st.session_state.role == "Admin":
            st.markdown(f"""
                <h1 style='color: #0f1b2a; font-size: 2.5rem; font-weight: 800; margin-bottom: 5px; border-bottom: none;'>
                    Admin Dashboard
                </h1>
                <p style='color: #3a5a8c; font-size: 1rem; margin-bottom: 30px;'>
                    System Administrator: {st.session_state.name} | {datetime.now().strftime('%d %B %Y')}
                </p>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <h1 style='color: #0f1b2a; font-size: 2.5rem; font-weight: 800; margin-bottom: 5px; border-bottom: none;'>
                    Welcome, {st.session_state.name}
                </h1>
                <p style='color: #3a5a8c; font-size: 1rem; margin-bottom: 30px;'>
                    {st.session_state.role} View | {datetime.now().strftime('%d %B %Y')}
                </p>
            """, unsafe_allow_html=True)

        df = filter_for_user(load_complaints())

        if len(df) == 0:
            st.info("No complaints yet. Submit some first.")
        else:
            with st.container(key="dash_stats"):
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.metric("TOTAL COMPLAINTS", len(df))
                with c2:
                    st.metric("OPEN", len(df[df["status"] == "Open"]))
                with c3:
                    st.metric("IN PROGRESS", len(df[df["status"] == "In Progress"]))
                with c4:
                    st.metric("RESOLVED", len(df[df["status"] == "Resolved"]))

            resolved_n = len(df[df["status"] == "Resolved"])
            esc_count = int(add_escalation(df)["escalated"].sum())
            st.markdown("<br>", unsafe_allow_html=True)
            with st.container(key="dash_stats2"):
                k1, k2, k3 = st.columns(3)
                with k1:
                    st.metric("AVG RESOLUTION TIME", format_hours(resolution_hours(df)))
                with k2:
                    st.metric("RESOLUTION RATE", f"{round(100 * resolved_n / len(df))}%")
                with k3:
                    st.metric("ESCALATED", esc_count)
            st.caption(f"Escalated = high-urgency complaints still unresolved after {ESCALATION_HOURS} hours.")

            st.markdown("<br>", unsafe_allow_html=True)
            chart_col1, chart_col2 = st.columns(2)
            with chart_col1:
                st.markdown("#### Complaints by Urgency")
                urgency_counts = df["urgency"].value_counts().reset_index()
                urgency_counts.columns = ["Urgency", "Count"]
                fig = px.bar(urgency_counts, x="Urgency", y="Count", color="Urgency", color_discrete_map={"High": "#ef4444", "Medium": "#f59e0b", "Low": "#10b981"}, text="Count")
                fig.update_traces(textposition='outside', textfont_size=12)
                fig.update_layout(margin=dict(l=10, r=10, t=30, b=10), height=350, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#0f1b2a"), showlegend=False, xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#dbeafe"))
                st.plotly_chart(style_chart(fig), use_container_width=True, theme=None, config={"displayModeBar": False})

            with chart_col2:
                st.markdown("#### Complaints by Status")
                status_counts = df["status"].value_counts().reset_index()
                status_counts.columns = ["Status", "Count"]
                fig = px.bar(status_counts, x="Status", y="Count", color="Status", color_discrete_map={"Open": "#f59e0b", "In Progress": "#3b82f6", "Resolved": "#10b981"}, text="Count")
                fig.update_traces(textposition='outside', textfont_size=12)
                fig.update_layout(margin=dict(l=10, r=10, t=30, b=10), height=350, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#0f1b2a"), showlegend=False, xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#dbeafe"))
                st.plotly_chart(style_chart(fig), use_container_width=True, theme=None, config={"displayModeBar": False})

            st.markdown("<br>", unsafe_allow_html=True)
            chart_col3, chart_col4 = st.columns(2)
            with chart_col3:
                st.markdown("#### Complaints by Subject")
                subject_counts = df["subject"].value_counts().reset_index()
                subject_counts.columns = ["Subject", "Count"]
                fig = px.pie(subject_counts, names="Subject", values="Count", hole=0.5, color_discrete_sequence=['#1f6feb', '#60a5fa', '#0f1b2a', '#bfdbfe', '#1e3a8a'])
                fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=12)
                fig.update_layout(margin=dict(l=10, r=10, t=30, b=10), height=350, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#0f1b2a"), showlegend=False)
                st.plotly_chart(style_chart(fig), use_container_width=True, theme=None, config={"displayModeBar": False})

            with chart_col4:
                st.markdown("#### Complaints by Sentiment")
                sentiment_counts = df["sentiment"].value_counts().reset_index()
                sentiment_counts.columns = ["Sentiment", "Count"]
                fig = px.bar(sentiment_counts, x="Sentiment", y="Count", color="Sentiment", color_discrete_map={"Negative": "#ef4444", "Neutral": "#60a5fa", "Positive": "#10b981"}, text="Count")
                fig.update_traces(textposition='outside', textfont_size=12)
                fig.update_layout(margin=dict(l=10, r=10, t=30, b=10), height=350, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#0f1b2a"), showlegend=False, xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#dbeafe"))
                st.plotly_chart(style_chart(fig), use_container_width=True, theme=None, config={"displayModeBar": False})

# ============================================================
# PAGE 2: SUBMIT COMPLAINT
# ============================================================
elif page == "Submit Complaint":
    st.title("Submit a Complaint")
    st.markdown("Fill in the form below. The AI will automatically classify your complaint.")

    with st.form("complaint_form"):
        customer_name = st.text_input("Customer Name")

        complaint_text = st.text_area("Complaint Description", height=150, placeholder="Describe your complaint in detail...")
        uploaded_file = st.file_uploader("Attach Evidence (Optional)", type=["pdf", "jpg", "png"])

        submitted = st.form_submit_button("Submit Complaint", use_container_width=True)

        if submitted:
            if complaint_text and customer_name:
                text_vec = vectorizer.transform([complaint_text])
                subject = subject_model.predict(text_vec)[0]
                urgency = urgency_model.predict(text_vec)[0]
                sentiment = sentiment_model.predict(text_vec)[0]

                subj_conf = round(max(subject_model.predict_proba(text_vec)[0]) * 100, 1)
                urg_conf = round(max(urgency_model.predict_proba(text_vec)[0]) * 100, 1)
                sent_conf = round(max(sentiment_model.predict_proba(text_vec)[0]) * 100, 1)

                attachment_filename = ""
                if uploaded_file is not None:
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    attachment_filename = f"{timestamp}_{os.path.basename(uploaded_file.name)}"
                    file_path = os.path.join(UPLOAD_DIR, attachment_filename)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                complaint = {
                    "customer_name": customer_name,
                    "complaint_text": complaint_text,
                    "subject": subject,
                    "urgency": urgency,
                    "sentiment": sentiment,
                    "attachment": attachment_filename,
                    "submitted_by": st.session_state.username
                }
                new_id = save_complaint(complaint)
                log_action(st.session_state.username, "SUBMIT_COMPLAINT", f"Complaint #{new_id} ({complaint['reference']})")

                st.success("✅ Complaint submitted successfully!")
                st.info(f"📌 Reference ID: **{complaint['reference']}**. Please quote it when you contact the insurance company about this complaint.")

                st.markdown("### AI Analysis Results")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Subject", subject, f"{subj_conf}% Confidence")
                with col2:
                    st.metric("Urgency", urgency, f"{urg_conf}% Confidence")
                with col3:
                    st.metric("Sentiment", sentiment, f"{sent_conf}% Confidence")

                st.markdown("### Routing")
                dept = ROUTING_MAP.get(subject, "Customer Service")
                sent_count = notify(st.session_state.username, "Complaint received", complaint["reference"],
                                    f"ILYASHI: Your complaint {complaint['reference']} has been received and routed to {dept}. Quote this Reference ID when you contact us.")
                if sent_count:
                    st.caption("📨 A confirmation message was sent to you (simulated). See Notifications.")
                st.info(f"→ Routed to: **{dept}**")
            else:
                st.error("Please enter customer name and complaint description.")

# ============================================================
# PAGE 3: VIEW COMPLAINTS
# ============================================================
elif page == "View Complaints":
    st.title("All Complaints")
    if st.session_state.get("flash"):
        st.success(st.session_state.pop("flash"))

    df = load_complaints()

    if st.session_state.role == "Officer":
        if st.session_state.username == "jbanda":
            df = df[df["subject"].isin(["Claim", "Payment"])]
            st.info("🔒 **Department Filter Active:** You are only viewing Claims and Payments.")
        elif st.session_state.username == "mphiri":
            df = df[df["subject"].isin(["Policy", "Premium"])]
            st.info("🔒 **Department Filter Active:** You are only viewing Policy and Premium.")

    df = add_escalation(df)

    if len(df) == 0:
        st.info("No complaints yet. Submit one first.")
    else:
        search = st.text_input("🔍 Search", placeholder="Reference number, customer name or keyword")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            status_filter = st.selectbox("Status", ["All"] + list(df["status"].unique()))
        with col2:
            subject_filter = st.selectbox("Subject", ["All"] + list(df["subject"].unique()))
        with col3:
            urgency_filter = st.selectbox("Urgency", ["All"] + list(df["urgency"].unique()))
        with col4:
            escalation_filter = st.selectbox("Escalation", ["All", "Escalated only"])

        filtered = df.copy()
        if status_filter != "All":
            filtered = filtered[filtered["status"] == status_filter]
        if subject_filter != "All":
            filtered = filtered[filtered["subject"] == subject_filter]
        if urgency_filter != "All":
            filtered = filtered[filtered["urgency"] == urgency_filter]
        if escalation_filter == "Escalated only":
            filtered = filtered[filtered["escalated"]]

        if search.strip():
            q = search.strip().lower()
            filtered = filtered[
                filtered["reference"].astype(str).str.lower().str.contains(q, regex=False)
                | filtered["customer_name"].astype(str).str.lower().str.contains(q, regex=False)
                | filtered["complaint_text"].astype(str).str.lower().str.contains(q, regex=False)
            ]

        st.write(f"Showing **{len(filtered)}** of **{len(df)}** complaints")
        shown = filtered.drop(columns=["id"]).copy()
        shown.insert(shown.columns.get_loc("status") + 1, "escalation",
                     shown["escalated"].map({True: "⚠️ Escalated", False: ""}))
        show_table(shown.drop(columns=["escalated"]))

        if st.session_state.role in ["Admin", "Officer"]:
            st.subheader("Update Complaint Status")
            ref_options = df.sort_values("id", ascending=False)["reference"].tolist()
            chosen_ref = st.selectbox("Reference ID", ref_options)
            new_status = st.selectbox("New Status", ["Open", "In Progress", "Resolved"])
            if st.button("Update Status"):
                full_df = load_complaints()
                row_match = full_df[full_df["reference"] == chosen_ref]
                old_status = row_match.iloc[0]["status"]
                owner = row_match.iloc[0]["submitted_by"]
                full_df.loc[full_df["reference"] == chosen_ref, "status"] = new_status
                full_df.loc[full_df["reference"] == chosen_ref, "date_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                full_df.loc[full_df["reference"] == chosen_ref, "date_resolved"] = (
                    datetime.now().strftime("%Y-%m-%d %H:%M") if new_status == "Resolved" else "")
                full_df.to_csv(COMPLAINTS_FILE, index=False)
                log_action(st.session_state.username, "UPDATE_STATUS", f"{chosen_ref} → {new_status}")
                if owner and old_status != new_status:
                    notify(owner, "Status update", chosen_ref, STATUS_MESSAGES[new_status].format(ref=chosen_ref))
                st.session_state.flash = f"✅ {chosen_ref} updated to {new_status}"
                st.rerun()
        else:
            st.info("🔒 Viewers cannot update complaints.")

        if st.session_state.role in ["Admin", "Officer"]:
            st.subheader("Download Attachments")
            complaints_with_files = filtered[filtered["attachment"].notna() & (filtered["attachment"] != "")]
            if len(complaints_with_files) > 0:
                for index, row in complaints_with_files.iterrows():
                    col_a, col_b = st.columns([3, 1])
                    with col_a:
                        st.write(f"**{row['reference']}** - {row['customer_name']} ({row['attachment']})")
                    with col_b:
                        file_path = os.path.join(UPLOAD_DIR, str(row['attachment']))
                        if os.path.exists(file_path):
                            with open(file_path, "rb") as file:
                                st.download_button(label="Download", data=file, file_name=str(row['attachment']), key=f"download_{row['id']}")
            else:
                st.info("No attachments found for these complaints.")

# ============================================================
# MY COMPLAINTS (Viewer: track what you submitted)
# ============================================================
elif page == "My Complaints":
    st.title("My Complaints")
    st.markdown("Track the complaints you have submitted. Quote the Reference ID if you contact the insurance company.")

    all_df = load_complaints()
    mine = all_df[all_df["submitted_by"] == st.session_state.username]

    if len(mine) == 0:
        st.info("You have not submitted any complaints yet.")
    else:
        with st.container(key="my_stats"):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("OPEN", len(mine[mine["status"] == "Open"]))
            with c2:
                st.metric("IN PROGRESS", len(mine[mine["status"] == "In Progress"]))
            with c3:
                st.metric("RESOLVED", len(mine[mine["status"] == "Resolved"]))

        meaning = {
            "Open": "Received, waiting for a team member",
            "In Progress": "Being handled",
            "Resolved": "Dealt with",
        }
        view = mine.sort_values("id", ascending=False).copy()
        view["handled_by"] = view["subject"].map(ROUTING_MAP).fillna("Customer Service")
        view["what_it_means"] = view["status"].map(meaning).fillna("")
        show_table(view[["reference", "subject", "handled_by", "status", "what_it_means", "date_submitted", "date_updated"]])

# ============================================================
# NOTIFICATIONS (simulated SMS and email)
# ============================================================
elif page == "Notifications":
    st.title("Notifications")
    st.markdown("Messages the system sends when something happens to a complaint. Email messages are simulated. SMS messages are simulated too, unless live SMS is switched on.")
    if live_sms_enabled():
        st.caption("🟢 Live SMS is on: SMS messages go to real phones through Africa's Talking.")
    else:
        st.caption("🟡 Simulation mode: nothing is really sent.")

    log = load_notifications()
    if st.session_state.role != "Admin":
        log = log[log["to_user"] == st.session_state.username]

    if len(log) == 0:
        st.info("No messages yet. Submit a complaint or change a complaint's status to see messages appear here.")
    else:
        channel_filter = st.selectbox("Channel", ["All", "Email", "SMS"])
        if channel_filter != "All":
            log = log[log["channel"] == channel_filter]
        if st.session_state.role == "Admin":
            st.caption("As an Admin you can see every message the system sent.")
        st.write(f"Showing the latest **{min(len(log), 30)}** of **{len(log)}** messages")
        for _, r in log.sort_values("timestamp", ascending=False).head(30).iterrows():
            st.markdown(notification_card(r), unsafe_allow_html=True)

# ============================================================
# SETTINGS
# ============================================================
elif page == "Settings":
    st.title("Profile Settings")
    st.markdown("Manage your account preferences and security.")

    with st.expander("Change Password"):
        with st.form("change_password"):
            st.write("Update your password below.")
            current_pass = st.text_input("Current Password", type="password")
            new_pass = st.text_input("New Password", type="password")
            confirm_pass = st.text_input("Confirm New Password", type="password")
            if st.form_submit_button("Update Password"):
                users = load_users()
                idx = users.index[users["username"] == st.session_state.username]
                if len(idx) == 0:
                    st.error("Account not found.")
                elif not verify_password(current_pass, users.loc[idx[0], "password"]):
                    st.error("Current password is incorrect.")
                elif len(new_pass) < 8:
                    st.error("New password must be at least 8 characters.")
                elif new_pass != confirm_pass:
                    st.error("New passwords do not match.")
                else:
                    users.loc[idx[0], "password"] = bcrypt.hashpw(
                        new_pass.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                    users.to_csv(USERS_FILE, index=False)
                    log_action(st.session_state.username, "CHANGE_PASSWORD", "Password changed")
                    st.success("✅ Password updated.")

    with st.expander("Language"):
        st.selectbox("🌐 " + t("Language"), list(LANGUAGES),
                     index=list(LANGUAGES.values()).index(st.session_state.get("lang", "en")),
                     key="lang_choice", on_change=set_language)

    with st.expander("Notification Preferences"):
        contact = get_contact(st.session_state.username)
        channel = st.selectbox("How should we notify you?", CHANNEL_CHOICES,
                               index=CHANNEL_CHOICES.index(contact["channel"]) if contact["channel"] in CHANNEL_CHOICES else 0,
                               key="pref_channel")
        email_value = st.text_input("Email address", value=contact["email"], key="pref_email")
        phone_value = st.text_input("Phone number (for SMS)", value=contact["phone"], key="pref_phone")
        p1, p2 = st.columns(2)
        with p1:
            if st.button("Save Preferences"):
                save_contact(st.session_state.username, channel, email_value.strip(), phone_value.strip())
                log_action(st.session_state.username, "CHANGE_NOTIFICATION_PREFS", f"Channel: {channel}")
                st.success("✅ Preferences saved.")
        with p2:
            if st.button("Send me a test message"):
                count = notify(st.session_state.username, "Test message", "—", "ILYASHI: This is a test notification.")
                if count:
                    st.success("📨 Test message sent (simulated). See Notifications.")
                else:
                    st.info("Notifications are switched off. Choose Email, SMS or Both and save first.")
        st.caption("Messages are simulated for this prototype. Your contact details are kept only so the demo can show who a message would go to.")

# ============================================================
# HELP CENTER
# ============================================================
elif page == "Help Center":
    st.title("Help & Support")
    st.markdown("""
Welcome to the ILYASHI Help Center. Here you can find answers to common questions or contact our support team.

### Frequently Asked Questions (FAQ)

**Q: How does the AI classify my complaint?**
*A: The AI uses Natural Language Processing (NLP) to read the text of the complaint. It then predicts the Subject, Urgency, and Sentiment based on patterns learned from previous complaints.*

**Q: Can I upload a picture of my damaged car?**
*A: Yes! When submitting a complaint, use the "Attach Evidence" button to upload PDFs, JPGs, or PNGs.*

**Q: How do I know my complaint has been dealt with?**
*A: Open "My Complaints" from the menu. Each complaint you submitted shows its status: Open (received), In Progress (being handled) or Resolved (dealt with), plus the date it last changed.*

**Q: How will I be told about updates?**
*A: The system sends a message by email or SMS (simulated in this prototype) when your complaint is received and whenever its status changes. Choose your channel in Settings and read the messages under Notifications.*

**Q: Who can see my complaint?**
*A: For this prototype, Administrators and Officers assigned to your specific department can view and update complaint details.*

---
### Contact IT Support
If you are experiencing technical issues, please contact:
*   **Email:** support@ilyashi.co.zm
*   **Phone:** +260 760425101
*   **Hours:** Monday - Friday, 08:00 - 17:00
""")

# ============================================================
# MANAGE USERS (Admin Only)
# ============================================================
elif page == "Manage Users":
    st.title("Manage Users")
    users = load_users()
    display_users = users.copy()
    display_users["password"] = "••••••••"
    show_table(display_users)

    st.subheader("Add New User")
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
                new_user = pd.DataFrame([{"username": new_username, "password": hashed, "role": new_role, "name": new_name}])
                users = pd.concat([users, new_user], ignore_index=True)
                users.to_csv(USERS_FILE, index=False)
                log_action(st.session_state.username, "ADD_USER", f"Added {new_username}")
                st.success(f"✅ User **{new_username}** added.")
                st.rerun()
            else:
                st.error("Please fill in all fields.")

# ============================================================
# AUDIT LOG (Admin Only)
# ============================================================
elif page == "Audit Log":
    st.title("Audit Log")
    if os.path.exists(AUDIT_FILE):
        logs = pd.read_csv(AUDIT_FILE)
        show_table(logs.tail(100)[::-1], max_height=520)
    else:
        st.info("No audit logs yet.")

# ============================================================
# EXPORT DATA (Admin Only)
# ============================================================
elif page == "Export Data":
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        st.markdown("""
            <h1 style='color: #0f1b2a; font-size: 2.5rem; font-weight: 800; margin-bottom: 5px; border-bottom: none;'>
                Export Data
            </h1>
            <p style='color: #3a5a8c; font-size: 1rem; margin-bottom: 30px;'>
                Download the complete complaints database for offline analysis.
            </p>
        """, unsafe_allow_html=True)

        df = load_complaints()

        if len(df) == 0:
            st.info("There are no complaints to export yet.")
        else:
            st.write(f"Total records available: **{len(df)}**")
            st.markdown("<br>", unsafe_allow_html=True)

            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Complaints as CSV",
                data=csv,
                file_name="complaints_export.csv",
                mime="text/csv",
                use_container_width=True,
                type="primary"
            )

# ============================================================
# FOOTER
# ============================================================
footer_html = """<div style='background-color: transparent; padding: 30px 20px;'>
<div style='display: flex; justify-content: space-between; flex-wrap: wrap; gap: 20px 30px; color: #3a5a8c; font-size: 0.85rem;'>
<div style='margin-bottom: 20px;'>
<h4 style='color: #0f1b2a; margin-bottom: 15px; white-space: nowrap;'>Support</h4>
<p style='margin: 5px 0;'>Manage your account</p>
<p style='margin: 5px 0;'>Contact IT Support</p>
<p style='margin: 5px 0;'>Safety Resource Center</p>
</div>
<div style='margin-bottom: 20px;'>
<h4 style='color: #0f1b2a; margin-bottom: 15px; white-space: nowrap;'>Discover</h4>
<p style='margin: 5px 0;'>AI Classification</p>
<p style='margin: 5px 0;'>System Updates</p>
<p style='margin: 5px 0;'>ILYASHI for Business</p>
</div>
<div style='margin-bottom: 20px;'>
<h4 style='color: #0f1b2a; margin-bottom: 15px; white-space: nowrap;'>Terms and settings</h4>
<p style='margin: 5px 0;'>Privacy Notice</p>
<p style='margin: 5px 0;'>Terms of Service</p>
<p style='margin: 5px 0;'>Accessibility Statement</p>
</div>
<div style='margin-bottom: 20px;'>
<h4 style='color: #0f1b2a; margin-bottom: 15px; white-space: nowrap;'>Partners</h4>
<p style='margin: 5px 0;'>Extranet login</p>
<p style='margin: 5px 0;'>Partner help</p>
<p style='margin: 5px 0;'>List your institution</p>
</div>
<div style='margin-bottom: 20px;'>
<h4 style='color: #0f1b2a; margin-bottom: 15px; white-space: nowrap;'>About</h4>
<p style='margin: 5px 0;'>About ILYASHI</p>
<p style='margin: 5px 0;'>How We Work</p>
<p style='margin: 5px 0;'>Sustainability</p>
<p style='margin: 5px 0;'>Careers</p>
</div>
</div>
<hr style='border-color: #dbeafe; margin: 20px 0;'>
<div style='text-align: center; color: #3a5a8c; font-size: 0.75rem;'>
<p>ILYASHI is part of Mulungushi University ICT431 Capstone Project: an AI-based insurance customer complaints management system.</p>
<p>© 2026 ILYASHI. All rights reserved.</p>
<p style='margin-top: 10px;'>
<span style='color: #3b82f6; font-weight: bold; font-size: 1rem; margin: 0 10px;'>ILYASHI</span>
<span style='color: #0f1b2a; font-weight: bold; font-size: 1rem; margin: 0 10px;'>ZAMBIA</span>
<span style='color: #0f1b2a; font-weight: bold; font-size: 1rem; margin: 0 10px;'>AFRICA</span>
</p>
</div>
</div>"""

st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown(footer_html, unsafe_allow_html=True)
