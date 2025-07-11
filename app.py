import streamlit as st
import requests
from datetime import datetime
import pytz
from PIL import Image
import pandas as pd
import os 
# ---------------- CONFIG ----------------
SHEETDB_URLS = {
    "ongoing_tasks": "https://sheetdb.io/api/v1/t7v2r5fwzk0zt?sheet=ongoing_tasks",
    "institutions": "https://sheetdb.io/api/v1/t7v2r5fwzk0zt?sheet=institutions",
    "edtech_platforms": "https://sheetdb.io/api/v1/t7v2r5fwzk0zt?sheet=edtech",
    "bugs_updates": "https://sheetdb.io/api/v1/t7v2r5fwzk0zt?sheet=bugs",
    "messages": "https://sheetdb.io/api/v1/t7v2r5fwzk0zt?sheet=messages",
    "ideas": "https://sheetdb.io/api/v1/t7v2r5fwzk0zt?sheet=ideas",
    "campaigns": "https://sheetdb.io/api/v1/t7v2r5fwzk0zt?sheet=campaigns",
    "interns": "https://sheetdb.io/api/v1/t7v2r5fwzk0zt?sheet=interns",
    "work_distribution": "https://sheetdb.io/api/v1/t7v2r5fwzk0zt?sheet=work_distribution",
    "last_access": "https://sheetdb.io/api/v1/t7v2r5fwzk0zt?sheet=last_access"
}

USER_DATA = {
    "Anngha": {"password": "Q6D", "role": "editor"},
    "Shruti": {"password": "Q6D", "role": "editor"},
    "Laxman Sir": {"password": "222", "role": "laxman"},
}

# ---------------- HELPERS ----------------
def load_sheetdb_json(tab_key):
    url = SHEETDB_URLS[tab_key]
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.json()
    except:
        pass
    return []

def save_to_sheetdb(tab_key, data):
    url = SHEETDB_URLS[tab_key]
    try:
        requests.put(url, json={"data": data})
        return True
    except:
        return False

def log_access(user):
    now = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
    save_to_sheetdb("last_access", [{"user": user, "time": now}])

def display_last_access():
    data = load_sheetdb_json("last_access")
    if data:
        latest = data[-1]
        st.sidebar.markdown(f"🕒 Last Access: `{latest['user']}` at `{latest['time']}`")

ALL_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat",
    "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh",
    "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh",
    "Uttarakhand", "West Bengal"
]
TIERS = ["Tier 1", "Tier 2", "Tier 3"]
TYPES = ["Government", "Private"]

# ---------------- LOGIN ----------------
st.set_page_config(page_title="AceInt Dashboard", layout="wide")

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
        elif password == "1111":
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = "viewer"
            log_access(username)
            st.rerun()
        else:
            st.error("Invalid credentials")
    st.stop()

if st.sidebar.button("🚪 Logout"):
    st.session_state.authenticated = False
    st.rerun()

username = st.session_state.username
role = st.session_state.role
is_editor = role == "editor"
is_laxman = role == "laxman"
is_viewer = role == "viewer"

if os.path.exists("logo.png"):
    st.sidebar.image(Image.open("logo.png"), width=120)

india_time = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%I:%M:%S %p")
st.markdown(f"<div style='position:fixed; top:10px; right:10px; font-size:20px;'>🕒 {india_time}</div>", unsafe_allow_html=True)

display_last_access()
st.title(f"📊 Welcome, {username}")

# ---------------- TABS ----------------
tabs = st.tabs([
    "Ongoing Tasks", "Institutions", "EdTech Platforms", "Bugs Updates",
    "Messages", "Ideas", "Campaigns", "Interns", "Work Distribution"
])

# TAB: Ongoing Tasks
with tabs[0]:
    data = load_sheetdb_json("ongoing_tasks")
    st.write("### 🛠️ Ongoing Tasks")

    if is_editor:
        with st.form("add_task"):
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
                save_to_sheetdb("ongoing_tasks", data)
                st.success("✅ Task Added")
                st.rerun()

    st.write("### 📋 Current Ongoing Tasks")
    for i, item in enumerate(data):
        st.markdown("---")
        st.write(f"🔧 **Title**: {item.get('title', '')}")
        st.write(f"📋 **Description**: {item.get('description', '')}")
        st.write(f"👤 **Assigned To**: `{item.get('assigned_to', '')}`")
        st.write(f"✅ **Status**: {item.get('status', '')}")
        st.write(f"📅 **Due Date**: {item.get('due_date', '')}")
        st.write(f"⭐ **Priority**: {item.get('priority', '')}")
        st.write(f"🕒 **Created At**: {item.get('created_at', '')}")

        if is_editor and st.button("🗑️ Delete", key=f"del_task_{i}"):
            data.pop(i)
            save_to_sheetdb("ongoing_tasks", data)
            st.rerun()

# TAB 1 - Institutions
with tabs[1]:
    data = load_sheetdb_json("institutions")

    search = st.text_input("🔍 Search by Institution Name or State")
    filtered = [
        d for d in data
        if search.lower() in d.get("name", "").lower()
        or search.lower() in d.get("state", "").lower()
    ]

    if is_editor:
        with st.form("institution_form"):
            new_entry = {
                "name": st.text_input("🏛️ Institution Name"),
                "type": st.selectbox("🏷️ Type", TYPES),
                "tier": st.selectbox("🎓 Tier", TIERS),
                "state": st.selectbox("📍 State", ALL_STATES),
                "officer": st.text_input("👤 Officer Name"),
                "contact": st.text_input("📞 Contact"),
                "notes": st.text_area("📝 Notes")
            }

            if st.form_submit_button("➕ Add Institution"):
                data.append(new_entry)
                save_to_sheetdb("institutions", data)
                st.success("✅ Institution added!")
                st.rerun()

    st.write("### 🏫 Institution Directory")

    if filtered:
        for item in filtered:
            st.markdown("---")
            st.write(f"🏛️ **{item.get('name', '')}**")
            st.write(f"🏷️ Type: {item.get('type', '')}")
            st.write(f"🎓 Tier: {item.get('tier', '')}")
            st.write(f"📍 State: {item.get('state', '')}")
            st.write(f"👤 Officer: {item.get('officer', '')}")
            st.write(f"📞 Contact: {item.get('contact', '')}")
            st.write(f"📝 Notes: {item.get('notes', '')}")

        df = pd.DataFrame(filtered)
        st.download_button("📥 Download CSV", df.to_csv(index=False), "institutions.csv")
    else:
        st.info("🔍 No matching institutions found.")


# TAB 2 - EdTech Platforms
with tabs[2]:
    data = load_sheetdb_json("edtech_platforms")
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
                # Clean up alt_emails
                new_platform["alt_emails"] = ", ".join([e.strip() for e in new_platform["alt_emails"].split(",") if e.strip()])
                
                # Validation (optional)
                if not new_platform["name"] or not new_platform["website"]:
                    st.warning("⚠️ Name and Website are required.")
                else:
                    data.append(new_platform)
                    save_to_sheetdb("edtech_platforms", data)
                    st.success("✅ Platform Added")
                    st.rerun()

    st.write("### 📋 Current EdTech Platforms")
    for i, item in enumerate(data):
        st.markdown("---")
        st.write(f"🏷️ **Name:** {item.get('name', '')}")
        st.write(f"🌐 **Website:** {item.get('website', '')}")
        st.write(f"📧 **Primary Email:** {item.get('primary_email', '')}")
        st.write(f"📱 **Phone:** {item.get('phone', '')}")
        if item.get("alt_emails"):
            st.write(f"📨 **Other Emails:** {item.get('alt_emails', '')}")
        if item.get("notes"):
            st.write(f"📝 **Notes:** {item.get('notes', '')}")

        if is_editor and st.button("🗑️ Delete", key=f"del_edtech_{i}"):
            data.pop(i)
            save_to_sheetdb("edtech_platforms", data)
            st.rerun()

# TAB 3 - Bugs/Updates
elif selected_tab == tabs[3]:  # 🐞 Bugs & Updates
    data = load_sheetdb_json("bugs")
    st.write("### 🐞 Bugs & Updates")

    if is_editor:
        with st.form("bug_update_form"):
            entry = {
                "title": st.text_input("🐛 Bug/Update Title"),
                "description": st.text_area("📝 Description"),
                "type": st.selectbox("📌 Type", ["Bug", "Feature Request", "Improvement"]),
                "status": st.selectbox("✅ Status", ["Open", "In Progress", "Closed"]),
                "timestamp": datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
            }

            # Screenshot upload
            screenshot = st.file_uploader("📸 Upload Screenshot (optional)", type=["png", "jpg", "jpeg"])
            if screenshot:
                # Convert to base64 string or just note the filename (Streamlit won't persist it unless saved elsewhere)
                entry["screenshot"] = f"https://example.com/screenshots/{screenshot.name}"  # <-- Replace with real path if you upload elsewhere
            else:
                entry["screenshot"] = ""

            if st.form_submit_button("➕ Add Entry"):
                data.append(entry)
                save_to_sheetdb("bugs", data)
                st.success("✅ Entry Logged")
                st.rerun()

    st.write("---")
    st.subheader("📋 All Bugs / Updates")

    for i, item in enumerate(data):
        with st.expander(f"{item['title']} – {item['status']} – {item['type']}"):
            st.markdown(f"**📝 Description:** {item['description']}")
            st.markdown(f"**🕒 Timestamp:** {item['timestamp']}")

            # If screenshot is available
            if item.get("screenshot") and item["screenshot"].startswith("http"):
                st.image(item["screenshot"], caption="Screenshot", use_column_width=True)

            if is_editor and st.button("🗑️ Delete", key=f"del_bug_{i}"):
                data.pop(i)
                save_to_sheetdb("bugs", data)
                st.rerun()

# TAB 4 - Messages
with tabs[4]:
    data = load_sheetdb_json("messages")
    st.write("### 💬 Messages")

    if is_laxman:
        with st.form("msg_form"):
            msg = st.text_area("New Message")
            if st.form_submit_button("Post") and msg:
                data.append({"message": msg})
                save_to_sheetdb("messages", data)
                st.success("✅ Posted!")
                st.rerun()

    for i, item in enumerate(data):
        st.markdown(f"📨 {item['message']}")
        if is_laxman and st.button("🗑️ Delete", key=f"del_msg_{i}"):
            data.pop(i)
            save_to_sheetdb("messages", data)
            st.rerun()


# TAB 5 - Ideas
with tabs[5]:
    data = load_sheetdb_json("ideas")
    st.write("### 💡 Ideas")

    if is_editor:
        with st.form("idea_form"):
            entry = {
                "idea": st.text_input("💡 Idea"),
                "notes": st.text_area("📝 Notes or Details")
            }
            if st.form_submit_button("➕ Add Idea"):
                if entry["idea"].strip():  # basic validation
                    data.append(entry)
                    save_to_sheetdb("ideas", data)
                    st.success("✅ Idea added!")
                    st.rerun()
                else:
                    st.warning("⚠️ Please enter an idea.")

    st.write("### 📋 Submitted Ideas")
    for i, item in enumerate(data):
        st.markdown(f"- **💡 {item.get('idea', '')}** – _{item.get('notes', '')}_")
        if is_editor and st.button("🗑️ Delete", key=f"del_idea_{i}"):
            data.pop(i)
            save_to_sheetdb("ideas", data)
            st.rerun()



# TAB 6 - Campaigns
with tabs[6]:
    data = load_sheetdb_json("campaigns")
    st.write("### 📣 Campaigns")

    if is_editor:
        with st.form("campaign_form"):
            entry = {
                "campaign_type": st.selectbox("Type", ["Instagram", "LinkedIn", "Offline", "Email"]),
                "title": st.text_input("Title"),
                "platform": st.text_input("Platforms Used (comma-separated)"),
                "start_date": str(st.date_input("Start Date")),
                "duration_days": st.number_input("Duration (in days)", min_value=1, step=1),
                "owner": st.text_input("Owner"),
                "notes": st.text_area("Notes")
            }

            if st.form_submit_button("Launch Campaign"):
                entry["platform"] = entry["platform"]
                data.append(entry)
                save_to_sheetdb("campaigns", data)
                st.success("✅ Campaign Added")
                st.rerun()

    for i, item in enumerate(data):
        st.write(f"📌 **{item['campaign_type']}** – **{item['title']}**")
        st.write(f"🗓 {item['start_date']} | ⏳ {item['duration_days']} days | 👤 {item['owner']}")
        st.write(f"📝 {item['notes']}")
        if is_editor and st.button("🗑️ Delete", key=f"del_camp_{i}"):
            data.pop(i)
            save_to_sheetdb("campaigns", data)
            st.rerun()


# TAB 7 - Interns
with tabs[7]:
    data = load_sheetdb_json("interns")
    st.write("### 👩‍💻 Interns")

    if is_editor:
        with st.form("intern_form"):
            entry = {
                "name": st.text_input("Name"),
                "email": st.text_input("Email"),
                "college": st.text_input("College"),
                "branch": st.text_input("Branch"),
                "phone": st.text_input("Phone")
            }

            if st.form_submit_button("Add Intern"):
                data.append(entry)
                save_to_sheetdb("interns", data)
                st.success("✅ Intern Added")
                st.rerun()

    for i, item in enumerate(data):
        st.write(f"👤 {item['name']} | 📧 {item['email']} | 🎓 {item['college']}")
        if is_editor and st.button("🗑️ Delete", key=f"del_intern_{i}"):
            data.pop(i)
            save_to_sheetdb("interns", data)
            st.rerun()


# TAB 8 - Work Distribution
with tabs[8]:
    data = load_sheetdb_json("work_distribution")
    st.write("### ✅ Assigned Tasks")

    if is_editor:
        with st.form("assign_work"):
            task = {
                "task": st.text_input("Task"),
                "assigned_to": st.selectbox("Assign to", ["Anngha", "Shruti"]),
                "priority": st.selectbox("Priority", ["1", "2", "3", "4", "5"]),
                "done": False
            }
            if st.form_submit_button("Assign"):
                data.append(task)
                save_to_sheetdb("work_distribution", data)
                st.success("✅ Task Assigned")
                st.rerun()

    for i, item in enumerate(data):
        st.write(f"📌 {item['task']} → {item['assigned_to']} | ⭐ {item['priority']}")
        if username == item["assigned_to"]:
            done = st.checkbox("✅ Done?", value=item.get("done", False), key=f"chk_{i}")
            if done != item.get("done", False):
                item["done"] = done
                save_to_sheetdb("work_distribution", data)

            if st.button("🗑️ Delete", key=f"del_task_{i}"):
                data.pop(i)
                save_to_sheetdb("work_distribution", data)
                st.rerun()
        else:
            st.info("⏳ Pending" if not item.get("done") else "✅ Done")



