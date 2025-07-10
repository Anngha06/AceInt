import streamlit as st
import json
import os
from datetime import datetime
import pytz
from pytz import timezone
from PIL import Image
import pandas as pd

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

# ------------------ MAIN -------------------
st.set_page_config(page_title="AceInt Dashboard", layout="wide")

if os.path.exists("logo.png"):
    st.sidebar.image(Image.open("logo.png"), width=120)

india_time = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%I:%M:%S %p")
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

# ------------ TAB 0: Ongoing Tasks ------------
with tabs[0]:
    db_file = DATA_FILES["ongoing_tasks"]
    data = load_json(db_file)
    st.write("### 🛠️ Ongoing Tasks")
    for item in data:
        st.write(item)

# ------------ TAB 1: Institutions ------------
with tabs[1]:
    db_file = DATA_FILES["institutions"]
    data = load_json(db_file)

    search = st.text_input("🔍 Search by Institution Name or State")
    filtered_data = [d for d in data if search.lower() in d.get("name", "").lower() or search.lower() in d.get("state", "").lower()]

    if is_editor:
        with st.form("form_institutions"):
            entry = {
                "name": st.text_input("Institution Name"),
                "type": st.selectbox("Type", TYPES),
                "tier": st.selectbox("Tier", TIERS),
                "state": st.selectbox("State", ALL_STATES),
                "officer": st.text_input("Officer Name"),
                "contact": st.text_input("Contact"),
                "notes": st.text_area("Notes")
            }
            if st.form_submit_button("Add"):
                data.append(entry)
                save_json(db_file, data)
                st.success("Added!")
                st.rerun()

    st.write("### 📋 Current Institutions")
    for item in filtered_data:
        st.write(item)

    if filtered_data:
        df = pd.DataFrame(filtered_data)
        st.download_button("📥 Export CSV", df.to_csv(index=False), file_name="institutions.csv", mime="text/csv")

# ------------ TAB 2: EdTech Platforms ------------
with tabs[2]:
    db_file = DATA_FILES["edtech_platforms"]
    data = load_json(db_file)

    st.write("### 💻 EdTech Platforms")
    for item in data:
        st.write(item)

# ------------ TAB 3: Bugs & Updates ------------
with tabs[3]:
    db_file = DATA_FILES["bugs_updates"]
    data = load_json(db_file)
    st.write("### 🐞 Bugs & Updates")
    for item in data:
        st.write(item)

# ------------ TAB 4: Laxman Sir Messages Only ------------
with tabs[4]:
    db_file = DATA_FILES["messages"]
    data = load_json(db_file)

    if is_laxman:
        with st.form("add_msg"):
            message = st.text_area("Enter your message")
            if st.form_submit_button("Post") and message:
                data.append({"message": message})
                save_json(db_file, data)
                st.success("Message posted.")
                st.rerun()

    for i, item in enumerate(data):
        st.markdown(f"💬 {item['message']}")
        if is_laxman and st.button("🗑️ Delete", key=f"del_msg_{i}"):
            data.pop(i)
            save_json(db_file, data)
            st.rerun()

# ------------ TAB 5: Ideas ------------
with tabs[5]:
    db_file = DATA_FILES["ideas"]
    data = load_json(db_file)
    st.write("### 💡 Ideas")
    for item in data:
        st.write(item)

# ------------ TAB 6: Campaigns ------------
with tabs[6]:
    db_file = DATA_FILES["campaigns"]
    data = load_json(db_file)
    st.write("### 📣 Campaigns")
    for item in data:
        st.write(item)

# ------------ TAB 7: Interns ------------
with tabs[7]:
    db_file = DATA_FILES["interns"]
    data = load_json(db_file)
    st.write("### 👩‍💻 Interns")
    for item in data:
        st.write(item)

# ------------ TAB 8: Work Distribution with Role Logic ------------
with tabs[8]:
    db_file = DATA_FILES["work_distribution"]
    data = load_json(db_file)

    if is_editor:
        with st.form("assign_work"):
            task = st.text_input("Task")
            assigned_to = st.selectbox("Assign To", ["Anngha", "Shruti"])
            priority = st.selectbox("Priority (1 = High, 5 = Low)", list(range(1, 6)))
            if st.form_submit_button("Assign") and task:
                data.append({
                    "task": task,
                    "assigned_to": assigned_to,
                    "priority": priority,
                    "done": False
                })
                save_json(db_file, data)
                st.success("✅ Task assigned.")
                st.rerun()

    st.write("### 📝 Assigned Tasks")
    for i, item in enumerate(data):
        st.markdown("---")
        st.write(f"📌 **Task**: {item['task']}")
        st.write(f"👤 **Assigned To**: `{item['assigned_to']}`")
        st.write(f"⭐ **Priority**: {item['priority']}")

        if username == item["assigned_to"]:
            done_state = st.checkbox("✅ Mark as Done", value=item.get("done", False), key=f"done_{i}")
            if done_state != item.get("done", False):
                item["done"] = done_state
                save_json(db_file, data)

        else:
            if item.get("done"):
                st.success("✅ Done")
            else:
                st.info("❗ Pending")

        if username == item["assigned_to"]:
            if st.button("🗑️ Delete", key=f"del_task_{i}"):
                data.pop(i)
                save_json(db_file, data)
                st.rerun()
