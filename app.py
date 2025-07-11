import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import pytz

# Constants
API_ENDPOINT = "https://sheetdb.io/api/v1/t7v2r5fwzk0zt"
TIMEZONE = "Asia/Kolkata"
PRIMARY_COLOR = "#2A5C82"
SECONDARY_COLOR = "#5CB3FF"

# Users
USERS = {
    "Anngha": {"password": "Q6D", "role": "Editor"},
    "Shruti": {"password": "Q6D", "role": "Editor"},
    "Laxman": {"password": "222", "role": "Admin"},
    "Viewer": {"password": "111", "role": "Viewer"},
}

# Session setup
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.role = ""
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# Login function
def login():
    st.title("🔐 AceInt Dashboard Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = USERS[username]["role"]
            st.rerun()
        else:
            st.error("Invalid credentials")

# Logout
def logout():
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.rerun()

# Load & Save
@st.cache_data(ttl=5)
def load_data(sheet):
    try:
        return pd.DataFrame(requests.get(f"{API_ENDPOINT}/search?sheet={sheet}").json())
    except:
        return pd.DataFrame()

def save_data(sheet, data):
    data["sheet"] = sheet
    requests.post(API_ENDPOINT, json={"data": [data]})

# Tabs
def render_tab(name, df):
    st.subheader(f"📊 {name}")
    if not df.empty:
        st.dataframe(df)
    else:
        st.warning("No data found.")

def render_institutions():
    df = load_data("institutions").rename(columns={
        "name": "Name", "type": "Type", "tier": "Tier", "state": "State",
        "officer": "Officer", "contact": "Contact", "notes": "Notes"
    })
    if st.session_state.role in ["Editor", "Admin"]:
        with st.form("add_inst"):
            name = st.text_input("Name")
            type_ = st.text_input("Type")
            tier = st.text_input("Tier")
            state = st.text_input("State")
            officer = st.text_input("Officer Name")
            contact = st.text_input("Contact")
            notes = st.text_area("Notes")
            if st.form_submit_button("Add"):
                save_data("institutions", {
                    "name": name, "type": type_, "tier": tier,
                    "state": state, "officer": officer, "contact": contact, "notes": notes
                })
                st.success("Institution added.")
                st.rerun()
    render_tab("Institutions", df)

def render_meeting_notes():
    df = load_data("meetings").rename(columns={
        "date": "Date", "meeting_with": "Meeting With",
        "agenda": "Agenda", "points": "Points to be noted"
    })
    if st.session_state.role in ["Editor", "Admin"]:
        with st.form("add_meeting"):
            date = st.date_input("Date")
            with_ = st.text_input("Meeting With")
            agenda = st.text_area("Agenda")
            points = st.text_area("Points to be noted")
            if st.form_submit_button("Add"):
                save_data("meetings", {
                    "date": str(date), "meeting_with": with_,
                    "agenda": agenda, "points": points
                })
                st.success("Note added.")
                st.rerun()
    render_tab("Meeting Notes", df)

# Add other render_tab() functions for edtech_platforms, bugs, ideas, etc.
def render_edtech_platforms():
    df = load_data("edtech_platforms").rename(columns={
        "name": "Name", "website": "Website", "primary_email": "Primary Email",
        "phone": "Phone", "alt_emails": "Alt Emails", "notes": "Notes"
    })
    render_tab("EdTech Platforms", df)


def render_bugs():
    df = load_data("bugs").rename(columns={
        "title": "Title", "description": "Description", "type": "Type",
        "screenshot": "Screenshot", "status": "Status", "timestamp": "Timestamp"
    })
    if st.session_state.role in ["Editor", "Admin"]:
        with st.form("add_bug"):
            title = st.text_input("Title")
            desc = st.text_area("Description")
            bug_type = st.selectbox("Type", ["Bug", "Feature", "Improvement"])
            screenshot = st.text_input("Screenshot Link (optional)")
            status = st.selectbox("Status", ["Open", "In Progress", "Closed"])
            if st.form_submit_button("Submit"):
                timestamp = datetime.now(pytz.timezone(TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S")
                save_data("bugs", {
                    "title": title, "description": desc, "type": bug_type,
                    "screenshot": screenshot, "status": status, "timestamp": timestamp
                })
                st.success("Entry submitted.")
                st.rerun()
    render_tab("Bugs & Updates", df)


def render_ideas():
    df = load_data("ideas").rename(columns={
        "idea": "Idea", "notes": "Notes", "file": "Supporting Document"
    })
    if st.session_state.role in ["Editor", "Admin"]:
        with st.form("add_idea"):
            idea = st.text_input("Idea")
            notes = st.text_area("Notes")
            file = st.file_uploader("Supporting Document (optional)")
            file_link = f"https://example.com/{file.name}" if file else ""
            if st.form_submit_button("Submit"):
                save_data("ideas", {
                    "idea": idea, "notes": notes, "file": file_link
                })
                st.success("Idea submitted.")
                st.rerun()
    render_tab("Ideas", df)


def render_campaigns():
    df = load_data("campaigns").rename(columns={
        "title": "Title", "platform": "Platform", "start_date": "Start Date",
        "duration": "Duration", "notes": "Notes"
    })
    render_tab("Campaigns", df)


def render_interns():
    df = load_data("interns").rename(columns={
        "name": "Name", "college": "College", "reason": "Reason",
        "task": "Task", "resume_uploaded": "Resume Uploaded"
    })
    render_tab("Interns", df)


def render_work_distribution():
    df = load_data("work").rename(columns={
        "task": "Task", "assigned_to": "Assigned To", "completed": "Completed",
        "assigned_date": "Assigned Date", "completion_date": "Date of Completion",
        "last_access": "Last Access"
    })
    if st.session_state.role in ["Editor", "Admin"]:
        with st.form("assign_task"):
            task = st.text_input("Task")
            assignee = st.text_input("Assigned To")
            completed = st.selectbox("Completed", ["✅", "⏳"])
            assign_date = st.date_input("Assigned Date")
            completion_date = st.date_input("Completion Date")
            last_access = datetime.now(pytz.timezone(TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S")
            if st.form_submit_button("Assign"):
                save_data("work", {
                    "task": task, "assigned_to": assignee, "completed": completed,
                    "assigned_date": str(assign_date),
                    "completion_date": str(completion_date),
                    "last_access": f"{st.session_state.username} on {last_access}"
                })
                st.success("Task assigned.")
                st.rerun()
    render_tab("Work Distribution", df)
# Main Dashboard
def main():
    st.set_page_config(layout="wide", page_title="AceInt Dashboard")
    st.sidebar.image("logo.png", width=160)
    st.sidebar.title("AceInt Ops Dashboard")

    # 🌗 Theme toggle
    theme = st.sidebar.toggle("🌗 Toggle Theme", value=(st.session_state.theme == "dark"))
    st.session_state.theme = "dark" if theme else "light"
    st.markdown(f"<style>body{{background-color:{'#0e1117' if theme else '#ffffff'};}}</style>", unsafe_allow_html=True)

    st.sidebar.markdown(f"👤 Logged in as: **{st.session_state.username}**")
    if st.sidebar.button("Logout"):
        logout()

    # 🔐 Role-based tabs
    all_tabs = {
        "Ongoing Tasks": None,
        "Institutions": render_institutions,
        "EdTech Platforms": lambda: render_tab("EdTech Platforms", load_data("edtech_platforms")),
        "Meeting Notes": render_meeting_notes,
        "Help": lambda: st.info("Need help? Contact team@aceint.ai")
    }
    role_tabs = {
        "Admin": list(all_tabs.keys()),
        "Editor": [k for k in all_tabs if k != "Messages"],
        "Viewer": [k for k in all_tabs if k in ["Institutions", "EdTech Platforms", "Meeting Notes", "Help"]],
    }
    user_tabs = role_tabs.get(st.session_state.role, [])

    # Navigation
    tab = st.sidebar.selectbox("Navigate", user_tabs, key="main_tab_select")

    # View Tab dropdown
    st.sidebar.markdown("### 🔍 View Tab Data")
    view_tab = st.sidebar.selectbox("Select Tab to View", user_tabs, key="view_tab_select")
    if st.sidebar.button("🔄 Refresh", key="refresh_button"):
        st.rerun()

    # ⏱ Timestamp
    st.write("⏱ Last Updated:", datetime.now(pytz.timezone(TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S"))
    st.markdown("📡 Live data from Google Sheet.")

    # Render main tab
    if all_tabs.get(tab):
        all_tabs[tab]()

    # View Tab Mode
    if view_tab != tab and all_tabs.get(view_tab):
        st.markdown(f"---\n### 👁️ View-only mode: {view_tab}")
        all_tabs[view_tab]()

if not st.session_state.authenticated:
    login()
else:
    main()

