
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

    st.write("###Entries")
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

datetime.now().astimezone(pytz.timezone("Asia/Kolkata")).strftime("%I:%M:%S %p")
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

import pandas as pd

# ------------ TAB 0: Ongoing Tasks ------------
with tabs[0]:
    render_tab("ongoing_tasks", ["task", "due_date", "status"], editable=is_editor)

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

    search = st.text_input("🔍 Search by Name or State")
    filtered_data = [d for d in data if search.lower() in d.get("name", "").lower() or search.lower() in d.get("state", "").lower()]

    if is_editor:
        with st.form("form_edtech"):
            entry = {
                "name": st.text_input("Platform Name"),
                "website": st.text_input("Website URL"),
                "phone": st.text_input("Phone Number"),
                "email": st.text_input("Email"),
                "state": st.selectbox("State", ALL_STATES),
                "notes": st.text_area("Notes")
            }
            if st.form_submit_button("Add"):
                data.append(entry)
                save_json(db_file, data)
                st.success("Added!")
                st.rerun()

    st.write("### 📋 Current Platforms")
    for item in filtered_data:
        st.write(item)

    if filtered_data:
        df = pd.DataFrame(filtered_data)
        st.download_button("📥 Export CSV", df.to_csv(index=False), file_name="edtech_platforms.csv", mime="text/csv")

# ------------ TAB 3: Bugs & Updates ------------
with tabs[3]:
    render_tab("bugs_updates", ["issue", "priority", "notes"], editable=is_editor, allow_file=True)

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
    render_tab("ideas", ["idea", "notes"], editable=is_editor)

# ------------ TAB 6: Campaigns ------------
with tabs[6]:
    render_tab("campaigns", ["platform", "title", "start_date", "duration", "notes"], editable=is_editor)

# ------------ TAB 7: Interns with Resume Upload + CSV ------------
with tabs[7]:
   
    db_file = DATA_FILES["interns"]
    data = load_json(db_file)

    search = st.text_input("🔍 Search Intern by Name or College")
    filtered_data = [d for d in data if search.lower() in d.get("name", "").lower() or search.lower() in d.get("college", "").lower()]

    if is_editor:
        with st.form("form_interns"):
            entry = {
                "name": st.text_input("Name"),
                "college": st.text_input("College"),
                "reason": st.text_input("Reason"),
                "role": st.text_input("Role")
            }
            resume = st.file_uploader("📎 Upload Resume", type=["pdf", "doc", "docx"])
            if resume:
                entry["resume"] = resume.name
            if st.form_submit_button("Add"):
                data.append(entry)
                save_json(db_file, data)
                st.success("Intern added.")
                st.rerun()

    st.write("### 📋 Current Interns")
    for item in filtered_data:
        st.write(item)
        if "resume" in item:
            st.download_button("📄 Download Resume", item["resume"], file_name=item["resume"])

    if filtered_data:
        df = pd.DataFrame(filtered_data)
        st.download_button("📥 Export Interns CSV", df.to_csv(index=False), file_name="interns.csv", mime="text/csv")

# ------------ TAB 8: Work Distribution w/ Role-Specific Logic ------------
with tabs[8]:
    db_file = DATA_FILES["work_distribution"]
    data = load_json(db_file)

    if is_editor:
        with st.form("assign_work"):
            task = st.text_input("Task")
            assigned_to = st.selectbox("Assign To", ["Anngha", "Shruti"])
            priority = st.selectbox("Priority (1 = High, 5 = Low)", list(range(1, 6)))
            submitted = st.form_submit_button("Assign")
            if submitted and task:
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
