
import streamlit as st
import json
import os
from datetime import datetime
from pytz import timezone
from PIL import Image

# ---------------- SETUP -------------------
DATA_FILES = {
    "ongoing_tasks": "ongoing_tasks.json",
    "institutions": "institutions.json",
    "edtech_platforms": "edtech_platforms.json",
    "bugs_updates": "bugs_updates.json",
    "messages": "messages.json",
    "ideas": "ideas.json",
    "campaigns": "campaigns.json",
    "interns": "interns.json",
    "work_distribution": "work_distribution.json",
    "last_access": "last_access.json"
}

USER_DATA = {
    "Anngha": {"password": "Q6D", "role": "editor"},
    "Shruti": {"password": "Q6D", "role": "editor"},
    "Laxman Sir": {"password": "222", "role": "laxman"},
}

ALL_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
    "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"
]
TIERS = ["Tier 1", "Tier 2", "Tier 3"]
TYPES = ["Government", "Private"]

# ---------------- HELPERS -------------------
def load_json(file):
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump([], f)
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

def log_access(user):
    now = datetime.now(timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
    save_json(DATA_FILES["last_access"], {"user": user, "time": now})

def display_last_access():
    data = load_json(DATA_FILES["last_access"])
    if data:
        st.sidebar.markdown(f"🕒 Last Access: `{data['user']}` at `{data['time']}`")

def render_tab(name, fields, editable=True, allow_file=False, checkbox_user_limit=None):
    st.subheader(name)
    db_file = DATA_FILES[name.replace(" ", "_").lower()]
    data = load_json(db_file)

    if editable:
        with st.form(f"form_{name}"):
            entry = {}
            for field in fields:
                if field == "state":
                    entry[field] = st.selectbox("State", ALL_STATES)
                elif field == "tier":
                    entry[field] = st.selectbox("Tier", TIERS)
                elif field == "type":
                    entry[field] = st.selectbox("Institution Type", TYPES)
                elif field == "priority":
                    entry[field] = st.selectbox("Priority (1 = High, 5 = Low)", list(range(1, 6)))
                elif field == "notes":
                    entry[field] = st.text_area(field.title(), height=100)
                elif field == "assign_to":
                    entry[field] = st.selectbox("Assign To", ["Anngha", "Shruti"])
                else:
                    entry[field] = st.text_input(field.title())
            if allow_file:
                uploaded = st.file_uploader("Upload Screenshot or File", type=["png", "jpg", "jpeg", "pdf"])
                if uploaded:
                    entry["file"] = uploaded.name
            if st.form_submit_button("Add"):
                if name == "work_distribution":
                    entry["done"] = False
                data.append(entry)
                save_json(db_file, data)
                st.success("Entry added.")

    st.write("### Current Entries")
    for i, item in enumerate(data):
        st.markdown("---")
        for k, v in item.items():
            if k == "file":
                st.download_button("📎 Download File", v, file_name=v)
            elif k == "done":
                if checkbox_user_limit == item.get("assign_to"):
                    done_state = st.checkbox(f"✅ Mark Done: {item.get('task')}", value=v, key=f"{i}_done")
                    item["done"] = done_state
            else:
                st.write(f"**{k.title()}**: {v}")
        if editable or (checkbox_user_limit == item.get("assign_to")):
            if st.button("❌ Delete", key=f"{i}_del_{name}"):
                data.pop(i)
                save_json(db_file, data)
                st.rerun()

# ------------------ MAIN -------------------
st.set_page_config(page_title="AceInt Dashboard", layout="wide")

if os.path.exists("logo.png"):
    st.sidebar.image(Image.open("logo.png"), width=120)

india_time = datetime.now(timezone("Asia/Kolkata")).strftime("%I:%M:%S %p")
st.markdown(f"<div style='position:fixed; top:10px; right:10px; font-size:20px;'>🕒 {india_time}</div>", unsafe_allow_html=True)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 AceInt Dashboard Login")
    username = st.text_input("Name")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USER_DATA and USER_DATA[username]["password"] == password:
            st.session_state.authenticated = True
            st.session_state.username = username
            log_access(username)
            st.rerun()
        else:
            st.error("Invalid credentials")
    st.stop()

if st.sidebar.button("🚪 Logout"):
    st.session_state.authenticated = False
    st.rerun()

username = st.session_state.username
role = USER_DATA[username]["role"]
is_editor = role == "editor"
is_laxman = role == "laxman"

display_last_access()
st.title(f"📊 Welcome, {username}")

tabs = st.tabs([
    "Ongoing Tasks", "Institutions", "EdTech Platforms", "Bugs Updates",
    "Messages", "Ideas", "Campaigns", "Interns", "Work Distribution"
])

with tabs[0]:
    render_tab("ongoing_tasks", ["task", "due_date", "status"], editable=is_editor)
with tabs[1]:
    render_tab("institutions", ["name", "type", "tier", "state", "officer", "contact", "notes"], editable=is_editor)
with tabs[2]:
    render_tab("edtech_platforms", ["name", "contact", "website", "state"], editable=is_editor)
with tabs[3]:
    render_tab("bugs_updates", ["issue", "priority", "notes"], editable=is_editor, allow_file=True)
with tabs[4]:
    render_tab("messages", ["message"], editable=is_laxman)
with tabs[5]:
    render_tab("ideas", ["idea", "notes"], editable=is_editor)
with tabs[6]:
    render_tab("campaigns", ["platform", "title", "start_date", "duration", "notes"], editable=is_editor)
with tabs[7]:
    render_tab("interns", ["name", "college", "reason", "role"], editable=is_editor, allow_file=True)
with tabs[8]:
    render_tab("work_distribution", ["task", "assign_to", "priority"], editable=is_editor, checkbox_user_limit=username)
