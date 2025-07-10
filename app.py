# app.py
import streamlit as st
import os
import json
from datetime import datetime

# ---------- CONFIG ----------
LOGO_PATH = "logo.png"
EDITOR_CREDENTIALS = ["Anngha", "Shruti"]
EDITOR_PASSWORD = "Q6D"
LAXMAN_NAME = "Laxman Sir"
LAXMAN_PASSWORD = "222"

# ---------- UTILITIES ----------
def load_json(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return []

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

def record_last_access(user):
    save_json("last_access.json", {"user": user, "time": str(datetime.now())})

def get_last_access():
    data = load_json("last_access.json")
    return data.get("user", "N/A"), data.get("time", "N/A")

# ---------- LOGIN ----------
def login():
    st.image(LOGO_PATH, width=100)
    st.title("🔐 AceInt Dashboard Login")
    user = st.text_input("Enter your name")
    pw = st.text_input("Enter password", type="password")

    if st.button("Login"):
        if user in EDITOR_CREDENTIALS and pw == EDITOR_PASSWORD:
            st.session_state.user = user
            st.session_state.role = "editor"
        elif user == LAXMAN_NAME and pw == LAXMAN_PASSWORD:
            st.session_state.user = user
            st.session_state.role = "laxman"
        elif pw == EDITOR_PASSWORD:
            st.session_state.user = user
            st.session_state.role = "viewer"
        else:
            st.error("Access Denied")
            st.stop()

        record_last_access(user)
        st.success("Login successful! Reloading...")
        st.experimental_set_query_params(refresh="1")
        st.stop()

if "user" not in st.session_state:
    login()
    st.stop()

# ---------- ROLE FLAGS ----------
is_editor = st.session_state.role == "editor"
is_laxman = st.session_state.role == "laxman"
user = st.session_state.user

# ---------- SIDEBAR ----------
last_user, last_time = get_last_access()
st.sidebar.image(LOGO_PATH, width=80)
st.sidebar.markdown(f"**👤 Logged in as:** {user}")
st.sidebar.markdown(f"**🕒 Last Access:** {last_user} at {last_time}")

# ---------- MAIN TABS ----------
tabs = st.tabs([
    "📋 Ongoing Tasks", "🏫 Institutions", "🎓 EdTech Platforms", "🐞 Bugs & Updates",
    "💬 Laxman Messages", "💡 Ideas", "📣 Campaigns", "👩‍💻 Interns", "✅ Work Distribution"
])

def render_tab(title, file, fields, allow_edit=True, file_upload=False, checkbox_logic=None):
    data = load_json(file)

    if (is_editor or (is_laxman and title == "💬 Laxman Messages")) and allow_edit:
        with st.form(f"add_{title}"):
            inputs = [st.text_input(f, key=f"{file}_{f}") for f in fields]
            uploaded_file = st.file_uploader("Upload file (optional)", key=file) if file_upload else None
            if st.form_submit_button("Add"):
                item = dict(zip(fields, inputs))
                if uploaded_file:
                    item["file"] = uploaded_file.name
                data.append(item)
                save_json(file, data)
                st.experimental_rerun()

    for i, entry in enumerate(data):
        with st.expander(f"{entry.get(fields[0], 'Item')}"):
            for f in fields:
                st.write(f"**{f}:** {entry.get(f, '')}")
            if file_upload and entry.get("file"):
                st.write(f"📎 Attached: {entry['file']}")
            if checkbox_logic:
                checkbox_logic(data, i, entry)
            if is_editor or (is_laxman and title == "💬 Laxman Messages"):
                col1, col2 = st.columns(2)
                if col1.button("Edit", key=f"edit_{file}_{i}"):
                    with st.form(f"editform_{file}_{i}"):
                        edits = [st.text_input(f"Edit {f}", value=entry.get(f, ""), key=f"edit_{file}_{i}_{f}") for f in fields]
                        if st.form_submit_button("Save"):
                            data[i] = dict(zip(fields, edits))
                            save_json(file, data)
                            st.experimental_rerun()
                if col2.button("Delete", key=f"del_{file}_{i}"):
                    data.pop(i)
                    save_json(file, data)
                    st.experimental_rerun()

# ---------- INDIVIDUAL TABS ----------
with tabs[0]:
    st.header("📋 Ongoing Tasks")
    render_tab("Ongoing Tasks", "ongoing.json", ["Task", "Due Date", "Status"])

with tabs[1]:
    st.header("🏫 Institutions")
    render_tab("Institutions", "institutions.json", ["Name", "Type", "State", "TPO Name", "Contact", "Notes"])

with tabs[2]:
    st.header("🎓 EdTech Platforms")
    render_tab("EdTech", "edtech.json", ["Platform", "Number", "Website", "State"])

with tabs[3]:
    st.header("🐞 Bugs & Updates")
    render_tab("Bugs", "bugs.json", ["Issue", "Priority", "Notes"], file_upload=True)

with tabs[4]:
    st.header("💬 Laxman Messages")
    render_tab("Messages", "messages.json", ["Message"])

with tabs[5]:
    st.header("💡 Ideas")
    render_tab("Ideas", "ideas.json", ["Idea"])

with tabs[6]:
    st.header("📣 Campaigns")
    render_tab("Campaigns", "campaigns.json", ["Platform", "Title", "Start Date", "Duration", "Notes"])

with tabs[7]:
    st.header("👩‍💻 Interns")
    render_tab("Interns", "interns.json", ["Name", "College", "Reason", "Task", "Resume Uploaded"])

with tabs[8]:
    st.header("✅ Work Distribution")
    def checkbox_control(data, i, entry):
        if (entry['Assigned To'] == user):
            if st.checkbox(f"Mark as done", key=f"check_{i}"):
                data[i]['Done'] = True
                save_json("work.json", data)
                st.experimental_rerun()
        elif entry.get("Done"):
            st.success("✅ Completed")

    render_tab("Work Distribution", "work.json", ["Task", "Assigned To"], checkbox_logic=checkbox_control)

# 🎨 Optional: config.toml for theming stored in .streamlit/config.toml
