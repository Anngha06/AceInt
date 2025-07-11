
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

# User Roles
USERS = {
    "Anngha": {"password": "Q6D", "role": "Editor"},
    "Shruti": {"password": "Q6D", "role": "Editor"},
    "Laxman": {"password": "222", "role": "Admin"},
    "Viewer": {"password": "111", "role": "Viewer"},
}

# Initialize Session
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.role = ""

def login():
    st.title("🔐 AceInt Dashboard Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if user in USERS and USERS[user]["password"] == pwd:
            st.session_state.authenticated = True
            st.session_state.username = user
            st.session_state.role = USERS[user]["role"]
            st.success(f"Welcome, {user}!")
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")

def logout():
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.experimental_rerun()

@st.cache_data
def load_data(sheet):
    try:
        r = requests.get(f"{API_ENDPOINT}/search?sheet={sheet}")
        return pd.DataFrame(r.json())
    except:
        return pd.DataFrame()

def save_data(sheet, data):
    data["sheet"] = sheet
    return requests.post(API_ENDPOINT, json={"data": [data]})

def render_task_tab():
    st.subheader("📌 Ongoing Tasks")
    data = load_data("ongoing_tasks")
    if st.session_state.role in ["Editor", "Admin"]:
        with st.form("Add Task"):
            title = st.text_input("Title")
            desc = st.text_area("Description")
            assignee = st.text_input("Assignee")
            status = st.selectbox("Status", ["To Do", "In Progress", "Done"])
            due = st.date_input("Due Date")
            priority = st.selectbox("Priority", ["High", "Medium", "Low"])
            if st.form_submit_button("Add Task"):
                timestamp = datetime.now(pytz.timezone(TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S")
                save_data("ongoing_tasks", {
                    "title": title, "desc": desc, "assignee": assignee,
                    "status": status, "due": str(due),
                    "priority": priority, "timestamp": timestamp
                })
                st.success("Task added.")
    if not data.empty:
        st.dataframe(data)

def render_institutions():
    st.subheader("🏫 Institutions")
    data = load_data("institutions")
    if st.session_state.role in ["Editor", "Admin"]:
        with st.form("Add Institution"):
            name = st.text_input("Name")
            type_ = st.text_input("Type")
            tier = st.text_input("Tier")
            state = st.text_input("State")
            officer = st.text_input("Officer Name")
            contact = st.text_input("Contact Info")
            notes = st.text_area("Notes")
            if st.form_submit_button("Add Institution"):
                save_data("institutions", {
                    "name": name, "type": type_, "tier": tier,
                    "state": state, "officer": officer,
                    "contact": contact, "notes": notes
                })
                st.success("Institution added.")
    if not data.empty:
        st.download_button("📁 Export CSV", data.to_csv(index=False), "institutions.csv")
        st.dataframe(data)

def render_edtech():
    st.subheader("💻 EdTech Platforms")
    data = load_data("edtech_platforms")
    if not data.empty:
        st.dataframe(data)

def render_bugs_updates():
    st.subheader("🐞 Bugs & Updates")
    data = load_data("bugs")
    if st.session_state.role in ["Editor", "Admin"]:
        with st.form("Log Bug/Update"):
            title = st.text_input("Title")
            bug_type = st.selectbox("Type", ["Bug", "Feature", "Improvement"])
            status = st.selectbox("Status", ["Open", "In Progress", "Closed"])
            desc = st.text_area("Description")
            if st.form_submit_button("Submit"):
                timestamp = datetime.now(pytz.timezone(TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S")
                save_data("bugs", {
                    "title": title, "type": bug_type,
                    "status": status, "desc": desc,
                    "timestamp": timestamp
                })
                st.success("Entry submitted.")
    if not data.empty:
        st.dataframe(data)

def render_messages():
    st.subheader("📢 Internal Messages")
    data = load_data("messages")
    if st.session_state.username == "Laxman":
        with st.form("Post Message"):
            msg = st.text_area("Message")
            prio = st.selectbox("Priority", ["Low", "Medium", "High"])
            if st.form_submit_button("Post"):
                timestamp = datetime.now(pytz.timezone(TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S")
                save_data("messages", {"message": msg, "priority": prio, "timestamp": timestamp})
                st.success("Message posted.")
    if not data.empty:
        st.dataframe(data)

def render_ideas():
    st.subheader("💡 Ideas")
    data = load_data("ideas")
    if not data.empty:
        for _, row in data.iterrows():
            with st.expander(f"{row.get('type', 'Idea')}: {row.get('idea', '')}"):
                st.write(row.to_dict())

def render_campaigns():
    st.subheader("📆 Campaigns")
    data = load_data("campaigns")
    if not data.empty:
        st.dataframe(data)

def render_interns():
    st.subheader("👥 Interns")
    data = load_data("interns")
    if not data.empty:
        st.dataframe(data)

def render_work_distribution():
    st.subheader("🛠️ Work Distribution")
    data = load_data("work")
    if st.session_state.role in ["Editor", "Admin"]:
        with st.form("Assign Task"):
            task = st.text_input("Task Name")
            prio = st.selectbox("Priority", ["High", "Medium", "Low"])
            assignee = st.text_input("Assignee")
            status = st.selectbox("Status", ["⏳ Pending", "✅ Done"])
            if st.form_submit_button("Assign"):
                save_data("work", {"task": task, "priority": prio, "assignee": assignee, "status": status})
                st.success("Task assigned.")
    if not data.empty:
        st.dataframe(data)

def render_meeting_notes():
    st.subheader("📝 Meeting Notes")
    data = load_data("meetings")
    if st.session_state.role in ["Editor", "Admin"]:
        with st.form("Add Notes"):
            date = st.date_input("Date")
            attendees = st.text_input("Attendees")
            discussion = st.text_area("Discussion Points")
            actions = st.text_area("Action Items")
            if st.form_submit_button("Save"):
                save_data("meetings", {
                    "date": str(date), "attendees": attendees,
                    "discussion": discussion, "actions": actions
                })
                st.success("Notes added.")
    if not data.empty:
        st.dataframe(data)

def render_library():
    st.subheader("📚 Resource Library")
    data = load_data("resources")
    if not data.empty:
        for _, row in data.iterrows():
            st.markdown(f"**{row.get('name', '')}** - [{row.get('link', '')}]({row.get('link', '')})")

def render_help():
    st.info("""
    **Welcome to the AceInt Dashboard!**
    - Use the sidebar to navigate across tabs.
    - Your access level controls which sections you can edit.
    - All data is synced with a central database.
    """)

def main():
    st.set_page_config(layout="wide", page_title="AceInt Dashboard", page_icon="📊")
    st.markdown(f"<style>body{{color:{PRIMARY_COLOR};}}</style>", unsafe_allow_html=True)
    if not st.session_state.authenticated:
        login()
    else:
        st.sidebar.title("AceInt Ops Dashboard")
        st.sidebar.markdown(f"**User:** {st.session_state.username}")
        if st.sidebar.button("Logout"):
            logout()

        tab = st.sidebar.selectbox("Navigate", [
            "Ongoing Tasks", "Institutions", "EdTech Platforms", "Bugs & Updates",
            "Messages", "Ideas", "Campaigns", "Interns", "Work Distribution",
            "Meeting Notes", "Resource Library", "Help"
        ])
        st.write("⏱ Last Updated:", datetime.now(pytz.timezone(TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S"))

        if tab == "Ongoing Tasks": render_task_tab()
        elif tab == "Institutions": render_institutions()
        elif tab == "EdTech Platforms": render_edtech()
        elif tab == "Bugs & Updates": render_bugs_updates()
        elif tab == "Messages": render_messages()
        elif tab == "Ideas": render_ideas()
        elif tab == "Campaigns": render_campaigns()
        elif tab == "Interns": render_interns()
        elif tab == "Work Distribution": render_work_distribution()
        elif tab == "Meeting Notes": render_meeting_notes()
        elif tab == "Resource Library": render_library()
        elif tab == "Help": render_help()

if __name__ == "__main__":
    main()

