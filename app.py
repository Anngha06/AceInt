import streamlit as st
import json
import os
from datetime import datetime
import pytz
from pytz import timezone
from PIL import Image
import pandas as pd

# ------------- CONFIGURATION -------------
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
    # Default role for anyone else who logs in with 1111
}

# In your login section after successful login:
if username in USER_DATA and USER_DATA[username]["password"] == password:
    st.session_state.authenticated = True
    st.session_state.username = username
    st.session_state.role = USER_DATA[username]["role"]
    log_access(username)
    st.rerun()
elif password == "1111":  # new user allowed with view-only rights
    st.session_state.authenticated = True
    st.session_state.username = username
    st.session_state.role = "limited"
    log_access(username)
    st.rerun()
else:
    st.error("Invalid credentials")
    
def log_access(user):
    now = datetime.now(timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
    with open("last_access.json", "w") as f:
        json.dump({"user": user, "time": now}, f)
# Login
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
            st.session_state.role = USER_DATA[username]["role"]
            log_access(username)
            st.rerun()
        elif password == "1111":  # Anyone else with this password gets viewer role
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = "viewer"
            log_access(username)
            st.rerun()
        else:
            st.error("Invalid credentials")
    st.stop()

# Role Setup
username = st.session_state.username
role = st.session_state.role

is_editor = role == "editor"
is_laxman = role == "laxman"
is_viewer = role == "viewer"

ALL_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat",
    "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh",
    "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh",
    "Uttarakhand", "West Bengal"
]
TIERS = ["Tier 1", "Tier 2", "Tier 3"]
TYPES = ["Government", "Private"]

# ------------- HELPERS -------------
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

# ------------- MAIN ----------------
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

# TABS

tabs = st.tabs([
    "Ongoing Tasks", "Institutions", "EdTech Platforms", "Bugs Updates",
    "Messages", "Ideas", "Campaigns", "Interns", "Work Distribution"
])

# TAB 0
with tabs[0]:
    db_file = DATA_FILES["ongoing_tasks"]
    data = load_json(db_file)
    st.write("### 🛠️ Ongoing Tasks")

    if is_editor:
        with st.form("add_ongoing_task_form"):
            task_title = st.text_input("🔧 Task Title")
            description = st.text_area("📋 Task Description")
            assigned_to = st.selectbox("👤 Assigned To", ["Anngha", "Shruti"])
            status = st.selectbox("✅ Status", ["Not Started", "In Progress", "Completed"])
            due_date = st.date_input("📅 Due Date")
            priority = st.selectbox("⭐ Priority", ["High", "Medium", "Low"])

            if st.form_submit_button("➕ Add Task"):
                new_task = {
                    "title": task_title,
                    "description": description,
                    "assigned_to": assigned_to,
                    "status": status,
                    "due_date": str(due_date),
                    "priority": priority,
                    "created_at": datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
                }
                data.append(new_task)
                save_json(db_file, data)
                st.success("✅ Task Added")
                st.rerun()

    st.write("### 📋 Current Ongoing Tasks")
    for i, item in enumerate(data):
        st.markdown("---")
        st.write(f"🔧 **Title**: {item['title']}")
        st.write(f"📋 **Description**: {item['description']}")
        st.write(f"👤 **Assigned To**: `{item['assigned_to']}`")
        st.write(f"✅ **Status**: {item['status']}")
        st.write(f"📅 **Due Date**: {item['due_date']}")
        st.write(f"⭐ **Priority**: {item['priority']}")
        st.write(f"🕒 **Created At**: {item['created_at']}")

        if is_editor and st.button("🗑️ Delete", key=f"del_ongoing_{i}"):
            data.pop(i)
            save_json(db_file, data)
            st.rerun()
# TAB 1
with tabs[1]:
    db_file = DATA_FILES["institutions"]
    data = load_json(db_file)
    search = st.text_input("🔍 Search by Institution Name or State")
    filtered = [d for d in data if search.lower() in d.get("name", "").lower() or search.lower() in d.get("state", "").lower()]

    if is_editor:
        with st.form("institution_form"):
            new_entry = {
                "name": st.text_input("Institution Name"),
                "type": st.selectbox("Type", TYPES),
                "tier": st.selectbox("Tier", TIERS),
                "state": st.selectbox("State", ALL_STATES),
                "officer": st.text_input("Officer Name"),
                "contact": st.text_input("Contact"),
                "notes": st.text_area("Notes")
            }
            if st.form_submit_button("Add"):
                data.append(new_entry)
                save_json(db_file, data)
                st.success("Institution added!")
                st.rerun()

    st.write("### 📋 Institutions")
    for item in filtered:
        st.write(item)
    if filtered:
        df = pd.DataFrame(filtered)
        st.download_button("📥 Download CSV", df.to_csv(index=False), "institutions.csv")

# TAB 2
with tabs[2]:
    db_file = DATA_FILES["edtech_platforms"]
    data = load_json(db_file)
    st.write("### 💻 EdTech Platforms")

    if is_editor:
        with st.form("edtech_form"):
            new_platform = {
                "name": st.text_input("🏷️ Platform Name"),
                "website": st.text_input("🌐 Website URL"),
                "primary_email": st.text_input("📧 Primary Email ID"),
                "phone": st.text_input("📱 Phone Number"),
                "alt_emails": st.text_area("📨 Other Email IDs (comma-separated)", placeholder="e.g. help@xyz.com, contact@xyz.com"),
                "notes": st.text_area("📝 Notes or Remarks")
            }

            if st.form_submit_button("➕ Add Platform"):
                # Convert additional emails to list
                alt_emails = [e.strip() for e in new_platform["alt_emails"].split(",") if e.strip()]
                new_platform["alt_emails"] = alt_emails
                data.append(new_platform)
                save_json(db_file, data)
                st.success("✅ Platform Added")
                st.rerun()

    st.write("### 📋 Current EdTech Platforms")
    for i, item in enumerate(data):
        st.markdown("---")
        st.write(f"🏷️ **Name:** {item['name']}")
        st.write(f"🌐 **Website:** [{item['website']}]({item['website']})")
        st.write(f"📧 **Primary Email:** {item['primary_email']}")
        st.write(f"📱 **Phone:** {item['phone']}")
        if item["alt_emails"]:
            st.write(f"📨 **Other Emails:** {', '.join(item['alt_emails'])}")
        if item["notes"]:
            st.write(f"📝 **Notes:** {item['notes']}")

        if is_editor and st.button("🗑️ Delete", key=f"del_edtech_{i}"):
            data.pop(i)
            save_json(db_file, data)
            st.rerun()


# TAB 3
with tabs[3]:
    db_file = DATA_FILES["bugs_updates"]
    data = load_json(db_file)
    st.write("### 🐞 Bugs & Updates")

    if is_editor:
        with st.form("bug_update_form"):
            bug_title = st.text_input("🐛 Bug/Update Title")
            bug_description = st.text_area("📝 Description or Details")
            update_type = st.selectbox("📌 Type", ["Bug", "Feature Request", "Improvement", "UI Issue", "Other"])
            status = st.selectbox("✅ Status", ["Open", "In Progress", "Fixed", "Closed"])

            if st.form_submit_button("➕ Add Entry"):
                entry = {
                    "title": bug_title,
                    "description": bug_description,
                    "type": update_type,
                    "status": status,
                    "timestamp": datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
                }
                data.append(entry)
                save_json(db_file, data)
                st.success("✅ Bug/Update Logged")
                st.rerun()

    st.write("### 📋 Logged Bugs and Updates")
    for i, item in enumerate(data):
        st.markdown("---")
        st.write(f"🔹 **Title:** {item['title']}")
        st.write(f"📝 **Description:** {item['description']}")
        st.write(f"📌 **Type:** {item['type']}")
        st.write(f"✅ **Status:** {item['status']}")
        st.write(f"🕒 **Logged At:** {item['timestamp']}")

        if is_editor and st.button("🗑️ Delete", key=f"del_bug_{i}"):
            data.pop(i)
            save_json(db_file, data)
            st.rerun()

# TAB 4
with tabs[4]:
    data = load_json(DATA_FILES["messages"])
    st.write("### 💬 Messages")

    if is_laxman:
        with st.form("msg_form"):
            msg = st.text_area("New Message")
            if st.form_submit_button("Post") and msg:
                data.append({"message": msg})
                save_json(DATA_FILES["messages"], data)
                st.success("Posted!")
                st.rerun()

    for i, item in enumerate(data):
        st.markdown(f"📨 {item['message']}")
        if is_laxman and st.button("🗑️ Delete", key=f"del_msg_{i}"):
            data.pop(i)
            save_json(DATA_FILES["messages"], data)
            st.rerun()

# TAB 5
with tabs[5]:
    data = load_json(DATA_FILES["ideas"])
    st.write("### 💡 Ideas")

    if is_editor:  # Only Anngha and Shruti
        with st.form("idea_form"):
            idea = st.text_input("Idea")
            notes = st.text_area("Notes")
            if st.form_submit_button("Add Idea"):
                data.append({"idea": idea, "notes": notes})
                save_json(DATA_FILES["ideas"], data)
                st.success("💡 Idea added!")
                st.rerun()

    for i, item in enumerate(data):
        st.markdown(f"- **💡 {item['idea']}**")
        st.markdown(f"  📝 _{item['notes']}_")

        # Optional: allow delete for editors only
        if is_editor and st.button("🗑️ Delete", key=f"del_idea_{i}"):
            data.pop(i)
            save_json(DATA_FILES["ideas"], data)
            st.rerun()
# TAB 6
with tabs[6]:
    data = load_json(DATA_FILES["campaigns"])
    st.write("### 📣 Campaigns")

    campaign_types = [
        "Product Hunt Launch",
        "Unstop Event",
        "Instagram Campaign",
        "LinkedIn Campaign",
        "College WhatsApp Blast",
        "On-campus Posters",
        "Email Marketing",
        "YouTube Shorts",
        "Influencer Outreach",
        "Offline Event Booth",
        "Giveaway Contest",
        "Referral Program"
    ]

    platforms = [
        "Instagram", "LinkedIn", "Twitter", "YouTube", 
        "Unstop", "Product Hunt", "College WhatsApp", "Email", "Offline"
    ]

    if is_editor:
        with st.form("campaign_form"):
            new_campaign = {
                "campaign_type": st.selectbox("📌 Campaign Type", campaign_types),
                "title": st.text_input("📝 Campaign Title"),
                "platform": st.multiselect("🌐 Platforms Used", platforms),
                "start_date": st.date_input("📅 Start Date"),
                "duration_days": st.number_input("⏳ Duration (in days)", min_value=1, max_value=90),
                "budget_estimate": st.text_input("💰 Budget (Optional)"),
                "owner": st.selectbox("👤 Managed By", ["Anngha", "Shruti", "Laxman Sir"]),
                "goals": st.text_area("🎯 Campaign Goals (e.g., drive traffic, build brand awareness)"),
                "notes": st.text_area("🗒️ Additional Notes / Assets / Tracking Links")
            }

            if st.form_submit_button("🚀 Launch Campaign"):
                data.append(new_campaign)
                save_json(DATA_FILES["campaigns"], data)
                st.success("✅ Campaign Launched!")
                st.rerun()

    st.write("### 📅 Planned Campaigns")
    for i, item in enumerate(data):
        st.markdown("---")
        st.write(f"📌 **Type:** {item['campaign_type']}")
        st.write(f"📝 **Title:** {item['title']}")
        st.write(f"🌐 **Platforms:** {', '.join(item['platform'])}")
        st.write(f"📅 **Start Date:** {item['start_date']}")
        st.write(f"⏳ **Duration:** {item['duration_days']} days")
        st.write(f"💰 **Budget:** {item.get('budget_estimate', 'N/A')}")
        st.write(f"👤 **Owner:** {item['owner']}")
        st.write(f"🎯 **Goals:** {item['goals']}")
        st.write(f"🗒️ **Notes:** {item['notes']}")

        if is_editor and st.button("🗑️ Delete", key=f"del_camp_{i}"):
            data.pop(i)
            save_json(DATA_FILES["campaigns"], data)
            st.rerun()


# TAB 7
with tabs[7]:
    data = load_json(DATA_FILES["interns"])
    st.write("### 👩‍💻 Interns")

    if is_editor:
        with st.form("intern_form"):
            new_intern = {
                "name": st.text_input("👤 Full Name"),
                "email": st.text_input("📧 Email"),
                "college": st.text_input("🎓 College/University"),
                "branch": st.text_input("📚 Department / Branch"),
                "year": st.selectbox("📅 Year of Study", ["1st Year", "2nd Year", "3rd Year", "Final Year", "Graduate"]),
                "city": st.text_input("🌆 City"),
                "state": st.selectbox("📍 State", ALL_STATES),
                "phone": st.text_input("📱 Phone Number"),
                "internship_type": st.selectbox("💼 Internship Type", ["Technical", "Marketing", "Design", "Operations", "Business", "Campus Ambassador", "Content"]),
                "skills": st.text_area("🛠️ Skills / Tools Known (comma-separated)"),
                "project_assigned": st.text_area("📂 Project / Task Assigned"),
                "mentor": st.text_input("🧑‍🏫 Assigned Mentor"),
                "start_date": st.date_input("⏳ Start Date"),
                "duration_weeks": st.number_input("📆 Duration (in weeks)", min_value=1, max_value=52),
                "status": st.selectbox("🚦 Status", ["Active", "Completed", "Dropped"])
            }

            if st.form_submit_button("➕ Add Intern"):
                data.append(new_intern)
                save_json(DATA_FILES["interns"], data)
                st.success("✅ Intern Added!")
                st.rerun()

    st.write("### 📋 Current Interns")
    for i, item in enumerate(data):
        st.markdown("---")
        st.write(f"👤 **Name:** {item['name']}")
        st.write(f"📧 **Email:** {item['email']}")
        st.write(f"🎓 **College:** {item['college']}")
        st.write(f"📚 **Branch:** {item['branch']}")
        st.write(f"📅 **Year:** {item['year']}")
        st.write(f"🌆 **City:** {item['city']}, 📍 {item['state']}")
        st.write(f"📱 **Phone:** {item['phone']}")
        st.write(f"💼 **Internship Type:** {item['internship_type']}")
        st.write(f"🛠️ **Skills:** {item['skills']}")
        st.write(f"📂 **Project Assigned:** {item['project_assigned']}")
        st.write(f"🧑‍🏫 **Mentor:** {item['mentor']}")
        st.write(f"⏳ **Start Date:** {item['start_date']}")
        st.write(f"📆 **Duration:** {item['duration_weeks']} weeks")
        st.write(f"🚦 **Status:** {item['status']}")

        if is_editor and st.button("🗑️ Delete", key=f"del_intern_{i}"):
            data.pop(i)
            save_json(DATA_FILES["interns"], data)
            st.rerun()

# TAB 8
with tabs[8]:
    data = load_json(DATA_FILES["work_distribution"])
    if is_editor:
        with st.form("assign_work"):
            task = st.text_input("Task")
            assigned_to = st.selectbox("Assign to", ["Anngha", "Shruti"])
            priority = st.selectbox("Priority (1 = High, 5 = Low)", list(range(1, 6)))
            if st.form_submit_button("Assign"):
                data.append({"task": task, "assigned_to": assigned_to, "priority": priority, "done": False})
                save_json(DATA_FILES["work_distribution"], data)
                st.success("✅ Task Assigned")
                st.rerun()

    st.write("### 📝 Assigned Tasks")
    for i, item in enumerate(data):
        st.markdown("---")
        st.write(f"📌 Task: {item['task']}")
        st.write(f"👤 Assigned To: `{item['assigned_to']}`")
        st.write(f"⭐ Priority: {item['priority']}")

        if username == item["assigned_to"]:
            done = st.checkbox("✅ Mark as Done", value=item.get("done", False), key=f"chk_{i}")
            if done != item.get("done", False):
                item["done"] = done
                save_json(DATA_FILES["work_distribution"], data)

            if st.button("🗑️ Delete", key=f"del_task_{i}"):
                data.pop(i)
                save_json(DATA_FILES["work_distribution"], data)
                st.rerun()
        else:
            st.info("❗ Pending" if not item.get("done") else "✅ Done")
