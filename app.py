
import streamlit as st
import json
import os
from datetime import datetime

DATA_FOLDER = "data"

def load_json(file):
    try:
        with open(os.path.join(DATA_FOLDER, file), "r") as f:
            return json.load(f)
    except:
        return []

def save_json(file, data):
    with open(os.path.join(DATA_FOLDER, file), "w") as f:
        json.dump(data, f, indent=4)

def login():
    st.image("static/logo.png", width=120)
    st.title("🔐 Login")
    name = st.text_input("Enter your name")
    password = st.text_input("Enter password", type="password")
    if st.button("Login"):
        if (name in ["Anngha", "Shruti"] and password == "Q6D"):
            st.session_state.user = name
            st.session_state.role = "editor"
        elif (name == "Laxman Sir" and password == "222"):
            st.session_state.user = name
            st.session_state.role = "laxman"
        elif password == "111":
            st.session_state.user = name
            st.session_state.role = "viewer"
        else:
            st.error("Access denied.")
            return
        save_json("last_access.json", {"user": name, "time": str(datetime.now())})
        st.success("Login successful! Please refresh.")
        st.stop()

if "user" not in st.session_state:
    login()
    st.stop()

last_user = load_json("last_access.json")
if not isinstance(last_user, dict):
    last_user = {"user": "N/A", "time": "N/A"}

st.sidebar.image("static/logo.png", width=100)
st.sidebar.title("AceInt Dashboard")
st.sidebar.markdown(f"**Logged in as:** {st.session_state.user}")
st.sidebar.markdown(f"**Last Access:** {last_user.get('user')} at {last_user.get('time')}")

# Roles
is_editor = st.session_state.role == "editor"
is_laxman = st.session_state.role == "laxman"

tabs = st.tabs([
    "Ongoing", "Institutions", "EdTech", "Interns", "Bugs", "Ideas", "Campaigns", "Messages"
])

def render_json_tab(tabname, fields, editable=False):
    data = load_json(f"{tabname}.json")
    if editable:
        with st.form(f"add_{tabname}"):
            inputs = [st.text_input(f) for f in fields]
            if st.form_submit_button(f"Add to {tabname}"):
                data.append(dict(zip(fields, inputs)))
                save_json(f"{tabname}.json", data)
                st.success("Added successfully.")
                st.experimental_rerun()
    for idx, item in enumerate(data):
        with st.expander(f"{item.get(fields[0], f'Row {idx+1}')}"):
            for field in fields:
                st.write(f"**{field}**: {item.get(field, '')}")

with tabs[0]:
    st.header("🛠️ Ongoing Tasks")
    render_json_tab("ongoing", ["title", "due", "status"], editable=is_editor)

with tabs[1]:
    st.header("🏫 Institutions")
    render_json_tab("institutions", ["name", "type", "state", "officer", "contact", "notes"], editable=is_editor)

with tabs[2]:
    st.header("🎓 EdTech Partners")
    render_json_tab("edtech", ["name", "contact", "website", "state"], editable=is_editor)

with tabs[3]:
    st.header("🧑‍💻 Interns")
    render_json_tab("interns", ["name", "college", "reason", "task", "resume_uploaded"], editable=is_editor)

with tabs[4]:
    st.header("🐞 Bugs")
    render_json_tab("bugs", ["issue", "priority", "screenshot"], editable=is_editor)

with tabs[5]:
    st.header("💡 Ideas")
    render_json_tab("ideas", ["idea"], editable=is_editor)

with tabs[6]:
    st.header("📢 Campaigns")
    render_json_tab("campaigns", ["platform", "title", "duration", "start_date", "notes"], editable=is_editor)

with tabs[7]:
    st.header("📩 Messages")
    data = load_json("messages.json")
    if is_laxman:
        with st.form("add_msg"):
            msg = st.text_area("New Message")
            if st.form_submit_button("Post"):
                data.append({"message": msg})
                save_json("messages.json", data)
                st.success("Message posted.")
                st.experimental_rerun()
    for item in data:
        st.markdown(f"💬 {item['message']}")
