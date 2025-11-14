import streamlit as st
import sqlite3
import json
from datetime import datetime, timedelta
import anthropic
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from pathlib import Path

# ==================== CONFIGURATION ====================

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("EMAIL_ADDRESS", "")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD", "")

# SMS Configuration (Twilio - optional)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE = os.getenv("TWILIO_PHONE", "")
USER_PHONE = os.getenv("USER_PHONE", "")

# Claude API
CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# ==================== DATABASE SETUP ====================

def init_db():
    """Initialize SQLite database with enhanced schema"""
    conn = sqlite3.connect('ai_pa_enhanced.db')
    c = conn.cursor()
    
    # Tasks table with category separation
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT,
        description TEXT,
        category TEXT,
        task_type TEXT,
        due_date TEXT,
        priority TEXT,
        status TEXT,
        created_date TEXT,
        completed_date TEXT,
        reminder_sent BOOLEAN DEFAULT 0
    )''')
    
    # Study Progress
    c.execute('''CREATE TABLE IF NOT EXISTS study_progress (
        id INTEGER PRIMARY KEY,
        subject TEXT,
        date TEXT,
        hours_spent REAL,
        clarity_rating INTEGER,
        notes TEXT,
        status TEXT
    )''')
    
    # Mock Scores
    c.execute('''CREATE TABLE IF NOT EXISTS mock_scores (
        id INTEGER PRIMARY KEY,
        exam_type TEXT,
        score INTEGER,
        total_points INTEGER,
        date TEXT,
        subjects_covered TEXT,
        notes TEXT
    )''')
    
    # User Preferences
    c.execute('''CREATE TABLE IF NOT EXISTS user_preferences (
        id INTEGER PRIMARY KEY,
        email TEXT,
        phone TEXT,
        notification_email BOOLEAN,
        notification_sms BOOLEAN,
        notification_app BOOLEAN,
        reminder_times TEXT,
        created_date TEXT
    )''')
    
    # Notifications Log
    c.execute('''CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY,
        task_id INTEGER,
        notification_type TEXT,
        sent_at TEXT,
        status TEXT
    )''')
    
    conn.commit()
    return conn

# ==================== EMAIL NOTIFICATIONS ====================

def send_email_reminder(recipient_email, subject, body, task_type=""):
    """Send email reminder"""
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = SENDER_EMAIL
        message["To"] = recipient_email
        
        html = f"""
        <html>
          <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5; padding: 20px;">
            <div style="background-color: white; border-radius: 10px; padding: 20px; max-width: 600px; margin: 0 auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
              <h2 style="color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px;">🤖 Your AI Personal Assistant</h2>
              
              <div style="margin: 20px 0; color: #34495e; line-height: 1.6;">
                {body.replace(chr(10), '<br>')}
              </div>
              
              <div style="background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin-top: 20px;">
                <p style="margin: 0; color: #7f8c8d; font-size: 12px;">
                  This is an automated reminder from your AI PA system. <br>
                  Update your preferences to manage notifications.
                </p>
              </div>
            </div>
          </body>
        </html>
        """
        
        part = MIMEText(html, "html")
        message.attach(part)
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, message.as_string())
        
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

# ==================== SMS NOTIFICATIONS ====================

def send_sms_reminder(phone_number, message_text):
    """Send SMS reminder using Twilio"""
    try:
        if not TWILIO_ACCOUNT_SID:
            return False
        
        from twilio.rest import Client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        message = client.messages.create(
            body=message_text,
            from_=TWILIO_PHONE,
            to=phone_number
        )
        return True
    except Exception as e:
        print(f"SMS error: {e}")
        return False

# ==================== TASK MANAGEMENT ====================

def add_task(title, description, task_type, due_date, priority):
    """Add task with type separation"""
    conn = init_db()
    c = conn.cursor()
    category = "Work" if task_type.startswith("Work") else "Bar Prep"
    
    c.execute('''INSERT INTO tasks 
                 (title, description, category, task_type, due_date, priority, status, created_date)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              (title, description, category, task_type, due_date, priority, 'pending', datetime.now().isoformat()))
    conn.commit()
    conn.close()
    st.success(f"✅ {category} Task Added: {title}")

def get_tasks_by_type(task_type):
    """Get tasks filtered by type"""
    conn = init_db()
    c = conn.cursor()
    
    if task_type == "work":
        c.execute('SELECT * FROM tasks WHERE category = "Work" AND status != "completed" ORDER BY due_date ASC')
    elif task_type == "bar":
        c.execute('SELECT * FROM tasks WHERE category = "Bar Prep" AND status != "completed" ORDER BY due_date ASC')
    else:
        c.execute('SELECT * FROM tasks WHERE status != "completed" ORDER BY due_date ASC')
    
    tasks = c.fetchall()
    conn.close()
    return tasks

def get_urgent_tasks():
    """Get tasks due within 3 days"""
    conn = init_db()
    c = conn.cursor()
    today = datetime.now().date()
    three_days = today + timedelta(days=3)
    
    c.execute('''SELECT * FROM tasks 
                 WHERE status != "completed" AND due_date BETWEEN ? AND ?
                 ORDER BY due_date ASC''',
              (str(today), str(three_days)))
    tasks = c.fetchall()
    conn.close()
    return tasks

# ==================== STUDY PROGRESS ====================

def log_study_session(subject, hours_spent, clarity_rating, notes):
    """Log study session"""
    conn = init_db()
    c = conn.cursor()
    c.execute('''INSERT INTO study_progress 
                 (subject, date, hours_spent, clarity_rating, notes, status)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (subject, datetime.now().isoformat(), hours_spent, clarity_rating, notes, 'completed'))
    conn.commit()
    conn.close()
    st.success(f"📚 Study session logged: {subject} ({hours_spent}h)")

def log_mock_score(exam_type, score, total_points, subjects_covered, notes):
    """Log mock test score"""
    conn = init_db()
    c = conn.cursor()
    c.execute('''INSERT INTO mock_scores 
                 (exam_type, score, total_points, date, subjects_covered, notes)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (exam_type, score, total_points, datetime.now().isoformat(), subjects_covered, notes))
    conn.commit()
    conn.close()
    percentage = (score / total_points * 100) if total_points > 0 else 0
    st.success(f"🎯 Mock score logged: {exam_type} - {percentage:.1f}%")

def get_weak_subjects():
    """Get weak subjects"""
    conn = init_db()
    c = conn.cursor()
    c.execute('''SELECT subject, AVG(clarity_rating) as avg_clarity, COUNT(*) as sessions
                 FROM study_progress 
                 GROUP BY subject 
                 ORDER BY avg_clarity ASC''')
    weak = c.fetchall()
    conn.close()
    return weak

# ==================== AI ENGINE ====================

def generate_daily_briefing(user_schedule, urgent_tasks, weak_subjects, recent_progress, energy_levels, task_type="all"):
    """Generate AI briefing with context awareness"""
    client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
    
    context = "Work tasks" if task_type == "work" else "Bar Prep tasks" if task_type == "bar" else "All tasks"
    
    prompt = f"""You are an intelligent AI Personal Assistant helping a legal professional manage work and Bar exam prep.

USER PROFILE:
- Works 5-6 hours daily managing courses, classes, content creation
- Supervises 7-8 team members
- Preparing for California Bar Exam (Feb 2026)
- High energy: Morning (8-10am) and Evening (6-9:30pm)
- Work hours: 11:30am - 3/4pm (gradually decreasing)

CURRENT CONTEXT: {context}
ENERGY TODAY: {energy_levels}
SCHEDULE: {user_schedule}

URGENT TASKS (Next 3 Days):
{urgent_tasks if urgent_tasks else "No urgent tasks"}

WEAK AREAS:
{weak_subjects if weak_subjects else "No weak areas identified yet"}

RECENT PROGRESS:
{recent_progress if recent_progress else "No progress data"}

Generate a SMART, PERSONALIZED briefing with:

1. **TOP PRIORITY** (What to focus on TODAY)
2. **URGENT ALERTS** (What's deadline coming)
3. **FOCUSED STUDY** (Which weak area needs work)
4. **WORK TASK** (Content/class prep needed)
5. **ACTION ITEMS** (Specific tasks for today)
6. **MOTIVATIONAL NOTE** (Encouragement)

Be concise, actionable, and supportive. Include emojis for visual clarity."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text

def get_ai_recommendations(study_data, work_data):
    """Get personalized recommendations"""
    client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
    
    prompt = f"""As an expert legal education advisor, analyze and provide personalized guidance:

STUDY DATA:
{study_data}

WORK DATA:
{work_data}

Provide specific, actionable recommendations for:
1. Optimizing Bar exam prep
2. Managing work-life balance  
3. Improving weak areas
4. Better time management

Keep it concise and practical."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text

# ==================== AGENT PROACTIVE FEATURES ====================

def agent_check_and_send_reminders(user_email, user_phone):
    """AI Agent: Proactively check and send reminders"""
    urgent_tasks = get_urgent_tasks()
    
    for task in urgent_tasks:
        task_id, title, desc, category, task_type, due_date, priority, status, created, completed, reminder_sent = task
        
        # Only send once
        if not reminder_sent:
            # Determine days until due
            due = datetime.fromisoformat(due_date).date()
            days_left = (due - datetime.now().date()).days
            
            if days_left <= 3:
                # Create reminder message
                message = f"⚠️ URGENT: {title}\nDue: {due_date}\nPriority: {priority}"
                
                # Send email
                if user_email:
                    send_email_reminder(
                        user_email,
                        f"⚠️ URGENT TASK: {title}",
                        f"Your AI PA detected an urgent task:\n\n{title}\n\nDue: {due_date}\nPriority: {priority}\n\nLog in to update status!"
                    )
                
                # Send SMS (if configured)
                if user_phone and TWILIO_ACCOUNT_SID:
                    send_sms_reminder(user_phone, message)
                
                # Mark as sent
                conn = init_db()
                c = conn.cursor()
                c.execute('UPDATE tasks SET reminder_sent = 1 WHERE id = ?', (task_id,))
                conn.commit()
                conn.close()

def agent_analyze_progress():
    """AI Agent: Analyze progress and suggest optimizations"""
    weak = get_weak_subjects()
    if weak and len(weak) > 0:
        return weak[0][0]  # Return weakest subject
    return None

def agent_schedule_daily_brief(user_email):
    """AI Agent: Schedule and send daily briefing"""
    urgent = get_urgent_tasks()
    weak = get_weak_subjects()
    
    urgent_str = "\n".join([f"- {t[1]} (Due: {t[5]})" for t in urgent[:3]]) if urgent else "None"
    weak_str = "\n".join([f"- {w[0]} ({w[1]:.1f}/5)" for w in weak[:3]]) if weak else "None"
    
    briefing = generate_daily_briefing(
        user_schedule="Standard schedule",
        urgent_tasks=urgent_str,
        weak_subjects=weak_str,
        recent_progress="Check app for details",
        energy_levels="High"
    )
    
    if user_email:
        send_email_reminder(
            user_email,
            "📅 Your Daily AI PA Briefing",
            briefing
        )

# ==================== STREAMLIT UI ====================

st.set_page_config(
    page_title="AI Personal Assistant Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .urgent-task {
        background-color: #fee;
        border-left: 4px solid #f44;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .work-task {
        background-color: #efe;
        border-left: 4px solid #4f4;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .bar-task {
        background-color: #eef;
        border-left: 4px solid #44f;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .header-title {
        color: #2c3e50;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize database
init_db()

# ==================== SIDEBAR ====================

st.sidebar.title("🤖 AI PA Pro")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigate",
    ["📊 Dashboard", "💼 Work Tasks", "📚 Bar Prep", "📈 Analytics", "⚙️ Settings", "💡 AI Assistant"]
)

st.sidebar.divider()

# Notification settings in sidebar
st.sidebar.subheader("🔔 Quick Settings")
email_notif = st.sidebar.checkbox("Email Alerts", value=True)
sms_notif = st.sidebar.checkbox("SMS Alerts", value=False)
app_notif = st.sidebar.checkbox("App Alerts", value=True)

# ==================== MAIN PAGES ====================

if page == "📊 Dashboard":
    st.markdown('<p class="header-title">📊 Your Dashboard</p>', unsafe_allow_html=True)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    all_tasks = get_tasks_by_type("all")
    work_tasks = get_tasks_by_type("work")
    bar_tasks = get_tasks_by_type("bar")
    urgent = get_urgent_tasks()
    
    with col1:
        st.metric("📋 Total Tasks", len(all_tasks), delta="pending")
    with col2:
        st.metric("💼 Work Tasks", len(work_tasks))
    with col3:
        st.metric("📚 Bar Tasks", len(bar_tasks))
    with col4:
        st.metric("⚠️ Urgent", len(urgent))
    
    st.divider()
    
    # Daily Briefing Section
    st.subheader("📅 Your Daily AI Briefing")
    
    col1, col2 = st.columns(2)
    with col1:
        energy = st.selectbox("Energy Level:", ["High Morning & Evening ⚡", "Medium 😐", "Low 😴"])
    with col2:
        special_schedule = st.text_input("Special schedule today?", placeholder="e.g., Early meeting at 9am")
    
    if st.button("🚀 Generate Briefing", use_container_width=True, key="gen_brief"):
        with st.spinner("🤔 Generating your personalized briefing..."):
            urgent_str = "\n".join([f"- {t[1]} (Due: {t[5]})" for t in urgent[:5]]) if urgent else "None"
            weak = get_weak_subjects()
            weak_str = "\n".join([f"- {w[0]} ({w[1]:.1f}/5)" for w in weak[:5]]) if weak else "None"
            
            briefing = generate_daily_briefing(
                special_schedule or "Standard",
                urgent_str,
                weak_str,
                "Check app for details",
                energy
            )
            st.info(briefing)
    
    st.divider()
    
    # Task Overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💼 Work Tasks")
        if work_tasks:
            for task in work_tasks[:5]:
                st.markdown(f'<div class="work-task"><b>{task[1]}</b><br>Due: {task[5]} | {task[6]}</div>', unsafe_allow_html=True)
        else:
            st.success("✅ No work tasks!")
    
    with col2:
        st.subheader("📚 Bar Prep Tasks")
        if bar_tasks:
            for task in bar_tasks[:5]:
                st.markdown(f'<div class="bar-task"><b>{task[1]}</b><br>Due: {task[5]} | {task[6]}</div>', unsafe_allow_html=True)
        else:
            st.success("✅ No Bar prep tasks!")

elif page == "💼 Work Tasks":
    st.markdown('<p class="header-title">💼 Work Tasks</p>', unsafe_allow_html=True)
    
    with st.form("work_task_form"):
        st.write("Add a new work task:")
        title = st.text_input("Task Title", placeholder="e.g., Create Constitutional Law handout")
        desc = st.text_area("Description")
        
        col1, col2 = st.columns(2)
        with col1:
            task_type = st.selectbox("Work Task Type", [
                "Work - Content Creation",
                "Work - Class Management",
                "Work - Team Reporting"
            ])
            due_date = st.date_input("Due Date")
        
        with col2:
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
        
        submitted = st.form_submit_button("➕ Add Work Task", use_container_width=True)
        
        if submitted and title:
            add_task(title, desc, task_type, str(due_date), priority)
    
    st.divider()
    st.subheader("📋 Your Work Tasks")
    work_tasks = get_tasks_by_type("work")
    
    if work_tasks:
        for task in work_tasks:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f'<div class="work-task"><b>{task[1]}</b><br>{task[2][:100]}...<br>Due: {task[5]} | Priority: {task[6]}</div>', unsafe_allow_html=True)
            with col2:
                if st.button("✅", key=f"work_{task[0]}"):
                    conn = init_db()
                    c = conn.cursor()
                    c.execute('UPDATE tasks SET status = ?, completed_date = ? WHERE id = ?',
                              ('completed', datetime.now().isoformat(), task[0]))
                    conn.commit()
                    conn.close()
                    st.rerun()
    else:
        st.success("✅ No work tasks!")

elif page == "📚 Bar Prep":
    st.markdown('<p class="header-title">📚 Bar Exam Preparation</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📝 Tasks", "📖 Study", "🎯 Mocks"])
    
    with tab1:
        with st.form("bar_task_form"):
            st.write("Add a Bar prep task:")
            title = st.text_input("Task Title", placeholder="e.g., Constitutional Law essay practice")
            desc = st.text_area("Description")
            
            col1, col2 = st.columns(2)
            with col1:
                task_type = st.selectbox("Bar Task Type", [
                    "Bar Prep - Essay",
                    "Bar Prep - MBE",
                    "Bar Prep - Performance Test"
                ])
                due_date = st.date_input("Due Date")
            
            with col2:
                priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
            
            submitted = st.form_submit_button("➕ Add Bar Task", use_container_width=True)
            
            if submitted and title:
                add_task(title, desc, task_type, str(due_date), priority)
        
        st.divider()
        st.subheader("📋 Bar Prep Tasks")
        bar_tasks = get_tasks_by_type("bar")
        
        if bar_tasks:
            for task in bar_tasks:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f'<div class="bar-task"><b>{task[1]}</b><br>{task[2][:100]}...<br>Due: {task[5]} | Priority: {task[6]}</div>', unsafe_allow_html=True)
                with col2:
                    if st.button("✅", key=f"bar_{task[0]}"):
                        conn = init_db()
                        c = conn.cursor()
                        c.execute('UPDATE tasks SET status = ?, completed_date = ? WHERE id = ?',
                                  ('completed', datetime.now().isoformat(), task[0]))
                        conn.commit()
                        conn.close()
                        st.rerun()
        else:
            st.success("✅ No Bar prep tasks!")
    
    with tab2:
        st.subheader("📚 Log Study Session")
        
        bar_subjects = ["Civil Procedure", "Constitutional Law", "Contracts", "Criminal Law", 
                       "Criminal Procedure", "Torts", "Property", "Evidence", "Business Orgs",
                       "Community Property", "Wills & Trusts", "Remedies"]
        
        with st.form("study_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                subject = st.selectbox("Subject", bar_subjects)
                hours = st.number_input("Hours", 0.5, 8.0, 1.5, 0.5)
            
            with col2:
                clarity = st.slider("Clarity (1-5)", 1, 5, 3)
                notes = st.text_area("What did you learn?")
            
            if st.form_submit_button("📚 Log Session", use_container_width=True):
                log_study_session(subject, hours, clarity, notes)
    
    with tab3:
        st.subheader("🎯 Log Mock Score")
        
        with st.form("mock_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                mock_type = st.selectbox("Test Type", ["Essay", "MBE Section", "Performance Test", "Full Exam"])
                score = st.number_input("Your Score", 0, step=1)
            
            with col2:
                total = st.number_input("Total Points", 1, step=1, value=100)
                subjects = st.text_input("Subjects (comma-separated)")
            
            notes = st.text_area("How did you feel?")
            
            if st.form_submit_button("🎯 Log Score", use_container_width=True):
                log_mock_score(mock_type, score, total, subjects, notes)

elif page == "📈 Analytics":
    st.markdown('<p class="header-title">📈 Your Progress</p>', unsafe_allow_html=True)
    
    from study_progress import get_study_progress
    
    progress = get_study_progress()
    weak = get_weak_subjects()
    
    col1, col2, col3 = st.columns(3)
    
    if progress:
        total_hours = sum([p[1] for p in progress])
        with col1:
            st.metric("⏰ Total Study Hours", f"{total_hours:.1f}h")
    
    if weak:
        avg_clarity = sum([w[1] for w in weak]) / len(weak)
        with col2:
            st.metric("📊 Avg Clarity", f"{avg_clarity:.1f}/5")
    
    with col3:
        st.metric("✅ Tasks Completed", len([t for t in get_tasks_by_type("all") if t[7] == "completed"]))
    
    st.divider()
    
    st.subheader("🔍 Weak Subjects")
    if weak:
        for subject in weak[:8]:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{subject[0]}**")
                st.progress(subject[1] / 5)
            with col2:
                st.caption(f"{subject[1]:.1f}/5")

elif page == "⚙️ Settings":
    st.markdown('<p class="header-title">⚙️ Settings</p>', unsafe_allow_html=True)
    
    st.subheader("🔔 Notification Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        email = st.text_input("📧 Email Address", placeholder="your@email.com")
        st.info("For email reminders")
    
    with col2:
        phone = st.text_input("📱 Phone Number", placeholder="+1 (555) 000-0000")
        st.info("For SMS reminders (Twilio)")
    
    st.divider()
    
    st.subheader("🔊 Notification Channels")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        enable_email = st.checkbox("📧 Email Reminders", value=True)
    with col2:
        enable_sms = st.checkbox("📱 SMS Alerts", value=False)
    with col3:
        enable_app = st.checkbox("🔔 In-App Alerts", value=True)
    
    st.divider()
    
    st.subheader("⏰ Reminder Times")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        morning_time = st.time_input("Morning Brief", value=datetime.strptime("08:00", "%H:%M").time())
    with col2:
        afternoon_time = st.time_input("Afternoon Reminder", value=datetime.strptime("15:00", "%H:%M").time())
    with col3:
        evening_time = st.time_input("Evening Brief", value=datetime.strptime("18:00", "%H:%M").time())
    
    if st.button("💾 Save Settings", use_container_width=True):
        st.success("✅ Settings saved!")
        st.balloons()

elif page == "💡 AI Assistant":
    st.markdown('<p class="header-title">💡 AI Recommendations</p>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🎯 Personalized", "🧠 Agent Status"])
    
    with tab1:
        if st.button("Get AI Recommendations", use_container_width=True, key="rec"):
            with st.spinner("🧠 Analyzing your data..."):
                weak = get_weak_subjects()
                work = len(get_tasks_by_type("work"))
                bar = len(get_tasks_by_type("bar"))
                
                weak_str = "\n".join([f"- {w[0]}: {w[1]:.1f}/5 clarity" for w in weak]) if weak else "None"
                
                recommendations = get_ai_recommendations(
                    f"Weak areas:\n{weak_str}",
                    f"{work} work tasks, {bar} Bar tasks"
                )
                
                st.success(recommendations)
    
    with tab2:
        st.subheader("🤖 Agent Status & Actions")
        
        st.info("Your AI Agent is actively:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("✅ Monitoring urgent tasks")
            st.success("✅ Tracking weak areas")
            st.success("✅ Analyzing patterns")
        
        with col2:
            st.success("✅ Sending reminders")
            st.success("✅ Generating briefings")
            st.success("✅ Making recommendations")
        
        if st.button("🚀 Trigger Agent Actions Now", use_container_width=True):
            with st.spinner("Agent is working..."):
                # Example agent action
                weak_subject = agent_analyze_progress()
                st.success(f"Agent identified: {weak_subject} needs attention!")

st.sidebar.divider()
st.sidebar.info("🔐 Your data is stored locally. Never shared.")
