import streamlit as st
import sqlite3
from datetime import datetime, timedelta
import os

# Set page config
st.set_page_config(
    page_title="AI Personal Assistant", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== BEAUTIFUL CSS STYLING ====================

st.markdown("""
<style>
/* Main theme colors */
:root {
    --primary: #667eea;
    --secondary: #764ba2;
    --success: #4caf50;
    --warning: #ff9800;
    --danger: #f44336;
    --info: #2196f3;
}

/* Page background */
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
}

/* Main content area */
.main {
    background-color: #f8f9fa;
}

/* Custom header */
.header-title {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    font-size: 2.5rem;
    font-weight: bold;
}

/* Metric cards - Beautiful */
[data-testid="metric-container"] {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    border-top: 4px solid #667eea;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

/* Work tasks - Green theme */
.work-task {
    background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);
    padding: 18px;
    border-radius: 12px;
    margin: 12px 0;
    border-left: 5px solid #4caf50;
    box-shadow: 0 4px 12px rgba(76, 175, 80, 0.15);
    transition: all 0.3s ease;
}

.work-task:hover {
    transform: translateX(5px);
    box-shadow: 0 6px 20px rgba(76, 175, 80, 0.25);
}

/* Bar prep tasks - Blue theme */
.bar-task {
    background: linear-gradient(135deg, #e3f2fd 0%, #f1f5fe 100%);
    padding: 18px;
    border-radius: 12px;
    margin: 12px 0;
    border-left: 5px solid #2196f3;
    box-shadow: 0 4px 12px rgba(33, 150, 243, 0.15);
    transition: all 0.3s ease;
}

.bar-task:hover {
    transform: translateX(5px);
    box-shadow: 0 6px 20px rgba(33, 150, 243, 0.25);
}

/* Urgent tasks - Red theme with animation */
.urgent-task {
    background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
    padding: 18px;
    border-radius: 12px;
    margin: 12px 0;
    border-left: 5px solid #f44336;
    box-shadow: 0 4px 12px rgba(244, 67, 54, 0.2);
    font-weight: 600;
    transition: all 0.3s ease;
    animation: pulse 2s infinite;
}

.urgent-task:hover {
    transform: translateX(8px);
    box-shadow: 0 8px 24px rgba(244, 67, 54, 0.3);
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.95; }
}

/* Alert banners */
.alert-banner {
    background: linear-gradient(135deg, #fff3cd 0%, #ffe0b2 100%);
    padding: 20px;
    border-radius: 12px;
    margin: 20px 0;
    border-left: 5px solid #ffc107;
    box-shadow: 0 4px 15px rgba(255, 193, 7, 0.2);
    font-weight: 600;
    color: #f57c00;
}

.alert-critical {
    background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
    padding: 20px;
    border-radius: 12px;
    margin: 20px 0;
    border-left: 5px solid #f44336;
    box-shadow: 0 4px 15px rgba(244, 67, 54, 0.2);
    font-weight: 600;
    color: #c62828;
}

/* Form inputs - Beautiful */
input, textarea, select {
    border-radius: 8px !important;
    border: 2px solid #e0e0e0 !important;
    padding: 12px !important;
    transition: all 0.3s ease !important;
}

input:focus, textarea:focus, select:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
}

/* Buttons - Modern */
button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
}

button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
}

/* Section headers */
.section-header {
    color: #1a1a2e;
    font-size: 1.5rem;
    font-weight: bold;
    margin-top: 30px;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 3px solid #667eea;
}

/* Tabs styling */
[role="tablist"] {
    background-color: transparent !important;
    border-bottom: 2px solid #e0e0e0 !important;
}

[role="tab"] {
    background-color: transparent !important;
    color: #666 !important;
    border: none !important;
    border-bottom: 3px solid transparent !important;
    padding: 15px 20px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

[role="tab"][aria-selected="true"] {
    color: #667eea !important;
    border-bottom: 3px solid #667eea !important;
}

/* Info boxes */
.info-box {
    background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);
    padding: 20px;
    border-radius: 12px;
    border-left: 5px solid #4caf50;
    margin: 15px 0;
}

/* Success message */
.success-message {
    background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);
    color: #2e7d32;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    border-left: 4px solid #4caf50;
}

/* Error message */
.error-message {
    background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
    color: #c62828;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    border-left: 4px solid #f44336;
}

/* Expander styling */
[data-testid="stExpander"] {
    border: 2px solid #e0e0e0 !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
}

/* Divider styling */
hr {
    background: linear-gradient(90deg, transparent, #667eea, transparent) !important;
    margin: 30px 0 !important;
}

/* Text styling */
h1 {
    color: #1a1a2e !important;
    font-weight: 700 !important;
}

h2 {
    color: #2c3e50 !important;
    font-weight: 600 !important;
}

h3 {
    color: #34495e !important;
    font-weight: 600 !important;
}

/* Sidebar text */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: white !important;
}

/* Progress bar styling */
[role="progressbar"] {
    background: linear-gradient(90deg, #667eea, #764ba2) !important;
    border-radius: 10px !important;
}

/* Custom card for metrics */
.custom-metric {
    background: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    text-align: center;
    transition: all 0.3s ease;
    border-top: 4px solid #667eea;
}

.custom-metric:hover {
    transform: translateY(-8px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.custom-metric .metric-value {
    font-size: 2.5rem;
    font-weight: bold;
    color: #667eea;
    margin: 10px 0;
}

.custom-metric .metric-label {
    font-size: 0.9rem;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Spacing utilities */
.mt-3 { margin-top: 30px; }
.mb-3 { margin-bottom: 30px; }
.p-3 { padding: 30px; }

</style>
""", unsafe_allow_html=True)

# ==================== DATABASE ====================

def init_db():
    """Initialize database"""
    conn = sqlite3.connect('ai_pa.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT,
        description TEXT,
        category TEXT,
        task_type TEXT,
        due_date TEXT,
        priority TEXT,
        status TEXT,
        created_date TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS study_progress (
        id INTEGER PRIMARY KEY,
        subject TEXT,
        date TEXT,
        hours_spent REAL,
        clarity_rating INTEGER,
        notes TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS mock_scores (
        id INTEGER PRIMARY KEY,
        exam_type TEXT,
        score INTEGER,
        total_points INTEGER,
        date TEXT,
        notes TEXT
    )''')
    
    conn.commit()
    return conn

# ==================== TASK FUNCTIONS ====================

def add_task(title, description, task_type, due_date, priority):
    conn = init_db()
    c = conn.cursor()
    category = "Work" if task_type.startswith("Work") else "Bar Prep"
    c.execute('''INSERT INTO tasks 
                 (title, description, category, task_type, due_date, priority, status, created_date)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              (title, description, category, task_type, due_date, priority, 'pending', datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_all_tasks():
    conn = init_db()
    c = conn.cursor()
    c.execute('SELECT * FROM tasks WHERE status = "pending" ORDER BY due_date ASC')
    tasks = c.fetchall()
    conn.close()
    return tasks

def get_tasks_by_type(task_type):
    conn = init_db()
    c = conn.cursor()
    if task_type == "work":
        c.execute('SELECT * FROM tasks WHERE category = "Work" AND status = "pending" ORDER BY due_date ASC')
    elif task_type == "bar":
        c.execute('SELECT * FROM tasks WHERE category = "Bar Prep" AND status = "pending" ORDER BY due_date ASC')
    tasks = c.fetchall()
    conn.close()
    return tasks

def get_urgent_tasks():
    conn = init_db()
    c = conn.cursor()
    today = datetime.now().date()
    three_days = today + timedelta(days=3)
    c.execute('''SELECT * FROM tasks 
                 WHERE status = "pending" AND due_date BETWEEN ? AND ?
                 ORDER BY due_date ASC''',
              (str(today), str(three_days)))
    tasks = c.fetchall()
    conn.close()
    return tasks

def complete_task(task_id):
    conn = init_db()
    c = conn.cursor()
    c.execute('UPDATE tasks SET status = ? WHERE id = ?', ('completed', task_id))
    conn.commit()
    conn.close()

# ==================== STUDY FUNCTIONS ====================

def log_study(subject, hours, clarity, notes):
    conn = init_db()
    c = conn.cursor()
    c.execute('''INSERT INTO study_progress 
                 (subject, date, hours_spent, clarity_rating, notes)
                 VALUES (?, ?, ?, ?, ?)''',
              (subject, datetime.now().isoformat(), hours, clarity, notes))
    conn.commit()
    conn.close()

def log_mock(exam_type, score, total, notes):
    conn = init_db()
    c = conn.cursor()
    c.execute('''INSERT INTO mock_scores 
                 (exam_type, score, total_points, date, notes)
                 VALUES (?, ?, ?, ?, ?)''',
              (exam_type, score, total, datetime.now().isoformat(), notes))
    conn.commit()
    conn.close()

def get_study_progress():
    conn = init_db()
    c = conn.cursor()
    c.execute('SELECT * FROM study_progress ORDER BY date DESC LIMIT 20')
    progress = c.fetchall()
    conn.close()
    return progress

def get_weak_subjects():
    conn = init_db()
    c = conn.cursor()
    c.execute('''SELECT subject, AVG(clarity_rating) as avg_clarity, COUNT(*) as sessions
                 FROM study_progress 
                 GROUP BY subject 
                 ORDER BY avg_clarity ASC''')
    weak = c.fetchall()
    conn.close()
    return weak

# ==================== MAIN APP ====================

st.markdown('<div class="header-title">🤖 AI Personal Assistant</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666; font-size: 1.1rem; margin-bottom: 30px;">Your Bar Exam Prep & Work Manager</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("📍 Navigation")
    page = st.radio("", ["📊 Dashboard", "💼 Work Tasks", "📚 Bar Prep", "📈 Analytics"], label_visibility="collapsed")

init_db()

# ==================== DASHBOARD ====================

if page == "📊 Dashboard":
    # Metrics Row
    all_tasks = get_all_tasks()
    work_tasks = get_tasks_by_type("work")
    bar_tasks = get_tasks_by_type("bar")
    urgent = get_urgent_tasks()
    
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    with col1:
        st.metric("📋 Total Tasks", len(all_tasks), delta="pending")
    with col2:
        st.metric("💼 Work", len(work_tasks), delta="active")
    with col3:
        st.metric("📚 Bar Prep", len(bar_tasks), delta="study")
    with col4:
        st.metric("⚠️ Urgent", len(urgent), delta="next 3 days")
    
    st.divider()
    
    # Alerts
    if urgent:
        st.markdown('<div class="alert-critical"><b>🔴 URGENT TASKS - Next 3 Days</b></div>', unsafe_allow_html=True)
        
        for task in urgent:
            task_id, title, desc, category, task_type, due_date, priority, status, created = task
            st.markdown(f'<div class="urgent-task">⚠️ <b>{title}</b><br>📅 Due: {due_date} | Priority: {priority}</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Task Overview
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown('<h3 style="color: #4caf50; margin-bottom: 20px;">💼 Work Tasks</h3>', unsafe_allow_html=True)
        if work_tasks:
            for task in work_tasks[:5]:
                task_id, title, desc, category, task_type, due_date, priority, status, created = task
                col_t, col_b = st.columns([4, 1])
                with col_t:
                    st.markdown(f'<div class="work-task"><b>{title}</b><br>📅 {due_date} | {priority}</div>', unsafe_allow_html=True)
                with col_b:
                    if st.button("✅", key=f"w{task_id}", help="Mark as complete"):
                        complete_task(task_id)
                        st.rerun()
        else:
            st.markdown('<div class="info-box">✅ No work tasks</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<h3 style="color: #2196f3; margin-bottom: 20px;">📚 Bar Prep Tasks</h3>', unsafe_allow_html=True)
        if bar_tasks:
            for task in bar_tasks[:5]:
                task_id, title, desc, category, task_type, due_date, priority, status, created = task
                col_t, col_b = st.columns([4, 1])
                with col_t:
                    st.markdown(f'<div class="bar-task"><b>{title}</b><br>📅 {due_date} | {priority}</div>', unsafe_allow_html=True)
                with col_b:
                    if st.button("✅", key=f"b{task_id}", help="Mark as complete"):
                        complete_task(task_id)
                        st.rerun()
        else:
            st.markdown('<div class="info-box">✅ No Bar prep tasks</div>', unsafe_allow_html=True)

# ==================== WORK TASKS ====================

elif page == "💼 Work Tasks":
    st.markdown('<h2 style="color: #4caf50; margin-bottom: 30px;">💼 Work Tasks Management</h2>', unsafe_allow_html=True)
    
    with st.form("work_form"):
        st.write("**➕ Add a new work task:**")
        title = st.text_input("📝 Task Title", placeholder="e.g., Create Constitutional Law content")
        desc = st.text_area("📄 Description", placeholder="Details about this task", height=80)
        
        col1, col2 = st.columns(2)
        with col1:
            task_type = st.selectbox("🏷️ Work Type", [
                "Work - Content Creation",
                "Work - Class Management",
                "Work - Team Reporting"
            ])
            due = st.date_input("📅 Due Date")
        
        with col2:
            priority = st.selectbox("🎯 Priority", ["Low", "Medium", "High", "Urgent"])
        
        if st.form_submit_button("➕ Add Work Task", use_container_width=True):
            if title:
                add_task(title, desc, task_type, str(due), priority)
                st.success(f"✅ Task added: {title}")
            else:
                st.error("Please enter a task title")
    
    st.divider()
    st.markdown('<h3 style="color: #4caf50;">📋 Your Work Tasks</h3>', unsafe_allow_html=True)
    
    work_tasks = get_tasks_by_type("work")
    
    if work_tasks:
        for task in work_tasks:
            task_id, title, desc, category, task_type, due_date, priority, status, created = task
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f'<div class="work-task"><b>{title}</b><br>{desc[:100]}<br>📅 {due_date} | 🎯 {priority}</div>', unsafe_allow_html=True)
            with col2:
                if st.button("✅", key=f"comp_w{task_id}"):
                    complete_task(task_id)
                    st.rerun()
    else:
        st.markdown('<div class="info-box">No work tasks yet. Add one above!</div>', unsafe_allow_html=True)

# ==================== BAR PREP ====================

elif page == "📚 Bar Prep":
    st.markdown('<h2 style="color: #2196f3; margin-bottom: 30px;">📚 Bar Exam Preparation</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📝 Tasks", "📖 Study Sessions", "🎯 Mock Scores"])
    
    with tab1:
        st.write("**➕ Add a Bar prep task:**")
        
        with st.form("bar_form"):
            title = st.text_input("📝 Task Title", placeholder="e.g., Constitutional Law essay practice")
            desc = st.text_area("📄 Description", height=80)
            
            col1, col2 = st.columns(2)
            with col1:
                task_type = st.selectbox("🏷️ Bar Task Type", [
                    "Bar Prep - Essay",
                    "Bar Prep - MBE",
                    "Bar Prep - Performance Test"
                ])
                due = st.date_input("📅 Due Date")
            
            with col2:
                priority = st.selectbox("🎯 Priority", ["Low", "Medium", "High", "Urgent"])
            
            if st.form_submit_button("➕ Add Bar Task", use_container_width=True):
                if title:
                    add_task(title, desc, task_type, str(due), priority)
                    st.success(f"✅ Task added: {title}")
                else:
                    st.error("Please enter a task title")
        
        st.divider()
        st.write("**Your Bar Prep Tasks:**")
        
        bar_tasks = get_tasks_by_type("bar")
        
        if bar_tasks:
            for task in bar_tasks:
                task_id, title, desc, category, task_type, due_date, priority, status, created = task
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f'<div class="bar-task"><b>{title}</b><br>{desc[:100]}<br>📅 {due_date} | 🎯 {priority}</div>', unsafe_allow_html=True)
                with col2:
                    if st.button("✅", key=f"comp_b{task_id}"):
                        complete_task(task_id)
                        st.rerun()
        else:
            st.markdown('<div class="info-box">No Bar prep tasks yet. Add one above!</div>', unsafe_allow_html=True)
    
    with tab2:
        st.write("**📚 Log your study session:**")
        
        bar_subjects = [
            "Civil Procedure", "Constitutional Law", "Contracts", 
            "Criminal Law", "Criminal Procedure", "Torts", 
            "Property", "Evidence", "Business Organizations",
            "Community Property", "Wills & Trusts", "Remedies"
        ]
        
        with st.form("study_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                subject = st.selectbox("📚 Subject Studied", bar_subjects)
                hours = st.number_input("⏱️ Hours Spent", min_value=0.5, max_value=8.0, step=0.5, value=1.5)
            
            with col2:
                clarity = st.slider("🧠 Concept Clarity (1=Confused, 5=Mastered)", 1, 5, 3)
                notes = st.text_area("📝 What did you learn?", height=80)
            
            if st.form_submit_button("📚 Log Study Session", use_container_width=True):
                log_study(subject, hours, clarity, notes)
                st.success(f"✅ Study session logged: {subject} ({hours}h)")
        
        st.divider()
        st.write("**Recent Study Sessions:**")
        
        progress = get_study_progress()
        if progress:
            for p in progress[:10]:
                prog_id, subject, date, hours, clarity, notes = p
                clarity_emoji = "🔴" if clarity <= 2 else "🟡" if clarity == 3 else "🟢"
                st.markdown(f"{clarity_emoji} **{subject}** - {hours}h (Clarity: {clarity}/5) | {date[:10]}")
        else:
            st.markdown('<div class="info-box">No study sessions logged yet.</div>', unsafe_allow_html=True)
    
    with tab3:
        st.write("**🎯 Log a mock exam score:**")
        
        with st.form("mock_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                exam_type = st.selectbox("📋 Test Type", [
                    "Essay (Single)", "Essay (Multiple)",
                    "Performance Test", "MBE Section",
                    "Full MBE (200q)", "Full Practice Exam"
                ])
                score = st.number_input("📊 Your Score", min_value=0, step=1, value=0)
            
            with col2:
                total = st.number_input("📊 Total Points", min_value=1, step=1, value=100)
                subjects = st.text_input("🏷️ Subjects Covered", placeholder="e.g., Constitutional Law, Torts")
            
            notes = st.text_area("💭 How did you feel?", height=80)
            
            if st.form_submit_button("🎯 Log Mock Score", use_container_width=True):
                log_mock(exam_type, score, total, notes)
                percentage = (score / total * 100) if total > 0 else 0
                st.success(f"✅ Mock score logged: {percentage:.1f}%")
        
        st.divider()
        st.write("**Mock Score History:**")
        
        conn = init_db()
        c = conn.cursor()
        c.execute('SELECT * FROM mock_scores ORDER BY date DESC LIMIT 10')
        mocks = c.fetchall()
        conn.close()
        
        if mocks:
            for m in mocks:
                mock_id, exam_type, score, total, date, notes = m
                percentage = (score / total * 100) if total > 0 else 0
                pct_emoji = "🔴" if percentage < 60 else "🟡" if percentage < 75 else "🟢"
                st.markdown(f"{pct_emoji} **{exam_type}**: {score}/{total} ({percentage:.1f}%) | {date[:10]}")
        else:
            st.markdown('<div class="info-box">No mock scores logged yet.</div>', unsafe_allow_html=True)

# ==================== ANALYTICS ====================

elif page == "📈 Analytics":
    st.markdown('<h2 style="color: #667eea; margin-bottom: 30px;">📈 Your Progress & Analytics</h2>', unsafe_allow_html=True)
    
    progress = get_study_progress()
    weak = get_weak_subjects()
    
    # Metrics
    col1, col2, col3 = st.columns(3, gap="medium")
    
    if progress:
        total_hours = sum([p[2] for p in progress])
        with col1:
            st.metric("⏰ Total Study Hours", f"{total_hours:.1f}h")
    
    if weak:
        avg_clarity = sum([w[1] for w in weak]) / len(weak)
        with col2:
            st.metric("📊 Average Clarity", f"{avg_clarity:.1f}/5")
    
    completed = len([t for t in get_all_tasks() if t[7] == "completed"])
    with col3:
        st.metric("✅ Tasks Completed", completed)
    
    st.divider()
    
    # Weak Subjects
    st.markdown('<h3 style="color: #f44336; margin-bottom: 20px;">🔍 Weak Subject Areas (Needs Focus)</h3>', unsafe_allow_html=True)
    
    if weak:
        for subject in weak[:10]:
            subject_name, avg_clarity, sessions = subject
            clarity_pct = (avg_clarity / 5) * 100
            clarity_emoji = "🔴" if avg_clarity <= 2 else "🟡" if avg_clarity <= 3.5 else "🟢"
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"{clarity_emoji} **{subject_name}**")
                st.progress(clarity_pct / 100)
            with col2:
                st.write(f"{avg_clarity:.1f}/5")
    else:
        st.markdown('<div class="info-box">No weak subjects identified yet. Keep logging study sessions!</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Study Progress Chart
    st.markdown('<h3 style="color: #667eea; margin-bottom: 20px;">📚 Study Activity by Subject</h3>', unsafe_allow_html=True)
    
    if progress:
        study_by_subject = {}
        for p in progress:
            subject = p[1]
            hours = p[2]
            if subject not in study_by_subject:
                study_by_subject[subject] = 0
            study_by_subject[subject] += hours
        
        st.bar_chart({s: h for s, h in study_by_subject.items()})
    else:
        st.markdown('<div class="info-box">No study data yet. Log some sessions to see charts!</div>', unsafe_allow_html=True)

# ==================== SIDEBAR INFO ====================

st.sidebar.divider()
st.sidebar.markdown("<h3 style='color: white;'>📊 Quick Stats</h3>", unsafe_allow_html=True)

all_tasks = get_all_tasks()
urgent = get_urgent_tasks()
progress = get_study_progress()
weak = get_weak_subjects()

col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("Pending", len(all_tasks), label_visibility="collapsed")
with col2:
    st.metric("Urgent", len(urgent), label_visibility="collapsed")

st.sidebar.metric("Study Sessions", len(progress), label_visibility="collapsed")

if weak:
    st.sidebar.metric("Weakest", weak[0][0], label_visibility="collapsed")

st.sidebar.divider()
st.sidebar.markdown("""
<div style='background: rgba(102, 126, 234, 0.1); padding: 15px; border-radius: 8px; border-left: 4px solid #667eea;'>
<p style='color: white; font-size: 0.9rem; margin: 0;'>✅ Your data is stored locally and secure.</p>
</div>
""", unsafe_allow_html=True)
