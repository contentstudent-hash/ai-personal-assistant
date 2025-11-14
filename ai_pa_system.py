import streamlit as st
import sqlite3
from datetime import datetime, timedelta

# Set page config
st.set_page_config(
    page_title="Kriti's PA Agent", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== MODERN, TRENDY CSS ====================

st.markdown("""
<style>
/* Global styles */
* {
    margin: 0;
    padding: 0;
}

body {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Main container */
.main {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
}

/* Header - Branded */
.header-container {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
    padding: 40px;
    border-radius: 20px;
    margin-bottom: 40px;
    box-shadow: 0 20px 40px rgba(99, 102, 241, 0.3);
    text-align: center;
}

.header-title {
    color: #ffffff;
    font-size: 3.2rem;
    font-weight: 900;
    margin: 0;
    letter-spacing: -1px;
    text-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.header-subtitle {
    color: #f0f4f8;
    font-size: 1.15rem;
    margin-top: 10px;
    font-weight: 500;
    letter-spacing: 0.5px;
}

/* Task cards - Modern */
.task-card {
    background: linear-gradient(135deg, #1e293b 0%, #293548 100%);
    border: 2px solid #334155;
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    color: #f1f5f9;
    cursor: pointer;
}

.task-card:hover {
    transform: translateY(-8px);
    border-color: #6366f1;
    box-shadow: 0 20px 40px rgba(99, 102, 241, 0.3);
    background: linear-gradient(135deg, #1e293b 0%, #2d3e52 100%);
}

/* Work tasks - Green accent */
.work-task {
    border-left: 6px solid #10b981;
}

.work-task:hover {
    border-left-color: #34d399;
    box-shadow: 0 20px 40px rgba(16, 185, 129, 0.25);
}

/* Bar prep tasks - Purple accent */
.bar-task {
    border-left: 6px solid #a78bfa;
}

.bar-task:hover {
    border-left-color: #c4b5fd;
    box-shadow: 0 20px 40px rgba(167, 139, 250, 0.25);
}

/* Urgent tasks - Red/Pink accent */
.urgent-task {
    border-left: 6px solid #f43f5e;
    background: linear-gradient(135deg, #1e293b 0%, #3a2a3a 100%);
}

.urgent-task:hover {
    border-left-color: #ff69b4;
    box-shadow: 0 20px 40px rgba(244, 63, 94, 0.35);
}

/* Task title */
.task-title {
    color: #f0f9ff;
    font-size: 1.15rem;
    font-weight: 700;
    margin-bottom: 8px;
    letter-spacing: 0.3px;
}

.task-meta {
    color: #cbd5e1;
    font-size: 0.95rem;
    margin: 4px 0;
    font-weight: 500;
}

/* Metrics */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1e293b 0%, #293548 100%);
    border: 2px solid #334155;
    border-radius: 15px;
    padding: 25px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    transition: all 0.4s ease;
}

[data-testid="metric-container"]:hover {
    border-color: #6366f1;
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(99, 102, 241, 0.25);
}

/* Alert banners */
.alert-warning {
    background: linear-gradient(135deg, #92400e 0%, #b45309 100%);
    border: 2px solid #d97706;
    padding: 20px;
    border-radius: 15px;
    margin: 25px 0;
    color: #fef3c7;
    font-weight: 600;
    font-size: 1.05rem;
    box-shadow: 0 10px 30px rgba(217, 119, 6, 0.2);
}

.alert-urgent {
    background: linear-gradient(135deg, #7c2d12 0%, #dc2626 100%);
    border: 2px solid #f87171;
    padding: 20px;
    border-radius: 15px;
    margin: 25px 0;
    color: #fee2e2;
    font-weight: 700;
    font-size: 1.1rem;
    box-shadow: 0 10px 30px rgba(220, 38, 38, 0.3);
    animation: pulse-warning 2s infinite;
}

@keyframes pulse-warning {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.95; }
}

.alert-success {
    background: linear-gradient(135deg, #065f46 0%, #059669 100%);
    border: 2px solid #10b981;
    padding: 20px;
    border-radius: 15px;
    margin: 20px 0;
    color: #d1fae5;
    font-weight: 600;
}

/* Form inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > select,
.stNumberInput > div > div > input {
    background-color: #1e293b !important;
    border: 2px solid #334155 !important;
    border-radius: 12px !important;
    padding: 14px !important;
    font-size: 1rem !important;
    color: #f0f9ff !important;
    font-weight: 500 !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stSelectbox > div > div > select:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 28px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
    box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 15px 40px rgba(99, 102, 241, 0.4) !important;
}

/* Section headers */
.section-header {
    color: #f0f9ff;
    font-size: 1.8rem;
    font-weight: 900;
    margin: 35px 0 25px 0;
    padding-bottom: 15px;
    border-bottom: 3px solid #6366f1;
    letter-spacing: -0.5px;
}

.section-header-green {
    border-bottom-color: #10b981;
}

.section-header-purple {
    border-bottom-color: #a78bfa;
}

.section-header-red {
    border-bottom-color: #f43f5e;
}

/* Tabs */
[role="tablist"] {
    background-color: transparent !important;
    border-bottom: 2px solid #334155 !important;
}

[role="tab"] {
    background-color: transparent !important;
    color: #cbd5e1 !important;
    border: none !important;
    border-bottom: 3px solid transparent !important;
    padding: 15px 25px !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    transition: all 0.3s ease !important;
    letter-spacing: 0.5px;
}

[role="tab"][aria-selected="true"] {
    color: #6366f1 !important;
    border-bottom-color: #6366f1 !important;
}

/* Dividers */
hr {
    margin: 35px 0 !important;
    border: none !important;
    border-top: 2px solid #334155 !important;
}

/* Text colors */
h1 {
    color: #f0f9ff !important;
    font-weight: 900 !important;
}

h2 {
    color: #f0f9ff !important;
    font-weight: 800 !important;
}

h3 {
    color: #e0e7ff !important;
    font-weight: 700 !important;
}

p {
    color: #cbd5e1 !important;
}

/* Progress bar */
[role="progressbar"] {
    background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
}

/* Success/Error/Info messages */
.stSuccess {
    background: linear-gradient(135deg, #065f46 0%, #059669 100%) !important;
    color: #d1fae5 !important;
    border: 2px solid #10b981 !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

.stError {
    background: linear-gradient(135deg, #7c2d12 0%, #dc2626 100%) !important;
    color: #fee2e2 !important;
    border: 2px solid #f87171 !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

.stInfo {
    background: linear-gradient(135deg, #0c4a6e 0%, #0369a1 100%) !important;
    color: #bae6fd !important;
    border: 2px solid #0ea5e9 !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

/* Slider */
[data-testid="stSlider"] {
    padding: 20px 0;
}

/* Label */
label {
    color: #e0e7ff !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    letter-spacing: 0.3px;
}

/* Number display */
.metric-value {
    font-size: 2.5rem !important;
    font-weight: 900 !important;
    color: #6366f1 !important;
}

/* Sidebar text */
[data-testid="stSidebar"] label {
    color: #f0f9ff !important;
}

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

# Header
st.markdown("""
<div class="header-container">
    <h1 class="header-title">✨ Kriti's PA Agent</h1>
    <p class="header-subtitle">Your Personal AI Assistant for Bar Exam & Work</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown("<h2 style='color: #e0e7ff; font-weight: 900; text-align: center; letter-spacing: 1px;'>📍 NAVIGATION</h2>", unsafe_allow_html=True)
    page = st.radio("", 
        ["📊 Dashboard", "💼 Work Tasks", "📚 Bar Prep", "📈 Analytics"],
        label_visibility="collapsed"
    )

init_db()

# ==================== DASHBOARD ====================

if page == "📊 Dashboard":
    
    all_tasks = get_all_tasks()
    work_tasks = get_tasks_by_type("work")
    bar_tasks = get_tasks_by_type("bar")
    urgent = get_urgent_tasks()
    
    st.markdown("<h2 class='section-header'>📊 Dashboard Overview</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4, gap="large")
    
    with col1:
        st.metric("📋 Total Tasks", len(all_tasks))
    with col2:
        st.metric("💼 Work", len(work_tasks))
    with col3:
        st.metric("📚 Bar Prep", len(bar_tasks))
    with col4:
        st.metric("⚠️ Urgent", len(urgent))
    
    st.divider()
    
    # Urgent Alerts
    if urgent:
        st.markdown('<div class="alert-urgent"><strong>🚨 URGENT - Next 3 Days!</strong></div>', unsafe_allow_html=True)
        
        for task in urgent:
            task_id, title, desc, category, task_type, due_date, priority, status, created = task
            st.markdown(f"""
            <div class="task-card urgent-task">
                <p class="task-title">⚠️ {title}</p>
                <p class="task-meta">📅 Due: {due_date} | 🎯 {priority}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("<h2 class='section-header'>Your Tasks</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("<h3 class='section-header section-header-green'>💼 Work Tasks</h3>", unsafe_allow_html=True)
        if work_tasks:
            for task in work_tasks[:5]:
                task_id, title, desc, category, task_type, due_date, priority, status, created = task
                col_t, col_b = st.columns([4, 1])
                with col_t:
                    st.markdown(f"""
                    <div class="task-card work-task">
                        <p class="task-title">✅ {title}</p>
                        <p class="task-meta">📅 {due_date}</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col_b:
                    if st.button("Done", key=f"w{task_id}", help="Mark complete"):
                        complete_task(task_id)
                        st.rerun()
        else:
            st.markdown("<div class='alert-success'><strong>✅ All work tasks done!</strong></div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h3 class='section-header section-header-purple'>📚 Bar Prep Tasks</h3>", unsafe_allow_html=True)
        if bar_tasks:
            for task in bar_tasks[:5]:
                task_id, title, desc, category, task_type, due_date, priority, status, created = task
                col_t, col_b = st.columns([4, 1])
                with col_t:
                    st.markdown(f"""
                    <div class="task-card bar-task">
                        <p class="task-title">📚 {title}</p>
                        <p class="task-meta">📅 {due_date}</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col_b:
                    if st.button("Done", key=f"b{task_id}", help="Mark complete"):
                        complete_task(task_id)
                        st.rerun()
        else:
            st.markdown("<div class='alert-success'><strong>✅ All Bar prep tasks done!</strong></div>", unsafe_allow_html=True)

# ==================== WORK TASKS ====================

elif page == "💼 Work Tasks":
    st.markdown("<h2 class='section-header section-header-green'>💼 Work Tasks Management</h2>", unsafe_allow_html=True)
    
    with st.form("work_form"):
        st.markdown("<p style='color: #e0e7ff; font-weight: 700; font-size: 1.1rem;'>➕ Add New Work Task</p>", unsafe_allow_html=True)
        
        title = st.text_input("Task Title", placeholder="e.g., Create Constitutional Law content")
        desc = st.text_area("Description (Optional)", placeholder="Add details", height=80)
        
        col1, col2 = st.columns(2)
        with col1:
            task_type = st.selectbox("Work Type", [
                "Work - Content Creation",
                "Work - Class Management",
                "Work - Team Reporting"
            ])
        with col2:
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
        
        due = st.date_input("Due Date")
        
        if st.form_submit_button("➕ Add Task"):
            if title:
                add_task(title, desc, task_type, str(due), priority)
                st.success(f"✅ Task added: {title}")
            else:
                st.error("❌ Please enter a task title")
    
    st.divider()
    
    st.markdown("<h3 class='section-header section-header-green'>📋 Your Work Tasks</h3>", unsafe_allow_html=True)
    
    work_tasks = get_tasks_by_type("work")
    
    if work_tasks:
        for task in work_tasks:
            task_id, title, desc, category, task_type, due_date, priority, status, created = task
            
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                <div class="task-card work-task">
                    <p class="task-title">{title}</p>
                    <p class="task-meta">{desc if desc else 'No description'}</p>
                    <p class="task-meta">📅 {due_date} | 🎯 {priority}</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("✓", key=f"comp_w{task_id}"):
                    complete_task(task_id)
                    st.rerun()
    else:
        st.markdown("<div class='alert-success'><strong>✅ No pending work tasks!</strong></div>", unsafe_allow_html=True)

# ==================== BAR PREP ====================

elif page == "📚 Bar Prep":
    st.markdown("<h2 class='section-header section-header-purple'>📚 Bar Exam Preparation</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📝 Tasks", "📖 Study", "🎯 Mocks"])
    
    with tab1:
        with st.form("bar_form"):
            st.markdown("<p style='color: #e0e7ff; font-weight: 700; font-size: 1.1rem;'>➕ Add New Bar Task</p>", unsafe_allow_html=True)
            
            title = st.text_input("Task Title", placeholder="e.g., Constitutional Law essay practice")
            desc = st.text_area("Description (Optional)", height=80)
            
            col1, col2 = st.columns(2)
            with col1:
                task_type = st.selectbox("Bar Task Type", [
                    "Bar Prep - Essay",
                    "Bar Prep - MBE",
                    "Bar Prep - Performance Test"
                ])
            with col2:
                priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
            
            due = st.date_input("Due Date")
            
            if st.form_submit_button("➕ Add Task"):
                if title:
                    add_task(title, desc, task_type, str(due), priority)
                    st.success(f"✅ Task added: {title}")
                else:
                    st.error("❌ Please enter a task title")
        
        st.divider()
        
        st.markdown("<h3 class='section-header section-header-purple'>📋 Bar Prep Tasks</h3>", unsafe_allow_html=True)
        
        bar_tasks = get_tasks_by_type("bar")
        
        if bar_tasks:
            for task in bar_tasks:
                task_id, title, desc, category, task_type, due_date, priority, status, created = task
                
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"""
                    <div class="task-card bar-task">
                        <p class="task-title">{title}</p>
                        <p class="task-meta">{desc if desc else 'No description'}</p>
                        <p class="task-meta">📅 {due_date} | 🎯 {priority}</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("✓", key=f"comp_b{task_id}"):
                        complete_task(task_id)
                        st.rerun()
        else:
            st.markdown("<div class='alert-success'><strong>✅ No pending Bar prep tasks!</strong></div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<p style='color: #e0e7ff; font-weight: 700; font-size: 1.1rem;'>📚 Log Study Session</p>", unsafe_allow_html=True)
        
        bar_subjects = [
            "Civil Procedure", "Constitutional Law", "Contracts", 
            "Criminal Law", "Criminal Procedure", "Torts", 
            "Property", "Evidence", "Business Organizations",
            "Community Property", "Wills & Trusts", "Remedies"
        ]
        
        with st.form("study_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                subject = st.selectbox("📚 Subject", bar_subjects)
                hours = st.number_input("⏱️ Hours", min_value=0.5, max_value=8.0, step=0.5, value=1.5)
            
            with col2:
                clarity = st.slider("🧠 Clarity (1=Confused, 5=Mastered)", 1, 5, 3)
            
            notes = st.text_area("📝 Notes", placeholder="What you learned", height=80)
            
            if st.form_submit_button("📚 Log Session"):
                log_study(subject, hours, clarity, notes)
                st.success(f"✅ Logged: {subject} ({hours}h)")
        
        st.divider()
        
        st.markdown("<h3 class='section-header section-header-purple'>📋 Recent Sessions</h3>", unsafe_allow_html=True)
        
        progress = get_study_progress()
        if progress:
            for p in progress[:10]:
                prog_id, subject, date, hours, clarity, notes = p
                clarity_emoji = "🔴" if clarity <= 2 else "🟡" if clarity == 3 else "🟢"
                st.markdown(f"""
                <div class="task-card">
                    <p class="task-title">{clarity_emoji} {subject}</p>
                    <p class="task-meta">{hours}h | Clarity: {clarity}/5 | {date[:10]}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<div class='alert-success'><strong>No sessions yet.</strong></div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("<p style='color: #e0e7ff; font-weight: 700; font-size: 1.1rem;'>🎯 Log Mock Score</p>", unsafe_allow_html=True)
        
        with st.form("mock_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                exam_type = st.selectbox("📋 Test Type", [
                    "Essay (Single)", "Essay (Multiple)",
                    "Performance Test", "MBE Section",
                    "Full MBE (200q)", "Full Practice Exam"
                ])
                score = st.number_input("📊 Score", min_value=0, step=1, value=0)
            
            with col2:
                total = st.number_input("📊 Total", min_value=1, step=1, value=100)
                subjects = st.text_input("🏷️ Subjects", placeholder="e.g., Constitutional Law, Torts")
            
            notes = st.text_area("💭 Notes", height=80)
            
            if st.form_submit_button("🎯 Log Score"):
                log_mock(exam_type, score, total, notes)
                percentage = (score / total * 100) if total > 0 else 0
                st.success(f"✅ Logged: {percentage:.1f}%")
        
        st.divider()
        
        st.markdown("<h3 class='section-header section-header-purple'>🎯 Score History</h3>", unsafe_allow_html=True)
        
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
                st.markdown(f"""
                <div class="task-card">
                    <p class="task-title">{pct_emoji} {exam_type}</p>
                    <p class="task-meta">{score}/{total} ({percentage:.1f}%) | {date[:10]}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<div class='alert-success'><strong>No scores yet.</strong></div>", unsafe_allow_html=True)

# ==================== ANALYTICS ====================

elif page == "📈 Analytics":
    st.markdown("<h2 class='section-header'>📈 Your Progress & Analytics</h2>", unsafe_allow_html=True)
    
    progress = get_study_progress()
    weak = get_weak_subjects()
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    if progress:
        total_hours = sum([p[2] for p in progress])
        with col1:
            st.metric("⏰ Study Hours", f"{total_hours:.1f}h")
    
    if weak:
        avg_clarity = sum([w[1] for w in weak]) / len(weak)
        with col2:
            st.metric("📊 Avg Clarity", f"{avg_clarity:.1f}/5")
    
    completed = len([t for t in get_all_tasks() if t[7] == "completed"])
    with col3:
        st.metric("✅ Completed", completed)
    
    st.divider()
    
    st.markdown("<h3 class='section-header section-header-red'>🔍 Areas That Need Focus</h3>", unsafe_allow_html=True)
    
    if weak:
        for subject in weak[:10]:
            subject_name, avg_clarity, sessions = subject
            clarity_pct = (avg_clarity / 5) * 100
            clarity_emoji = "🔴" if avg_clarity <= 2 else "🟡" if avg_clarity <= 3.5 else "🟢"
            
            col1, col2, col3 = st.columns([2, 3, 1])
            with col1:
                st.write(f"{clarity_emoji} **{subject_name}**")
            with col2:
                st.progress(clarity_pct / 100)
            with col3:
                st.write(f"{avg_clarity:.1f}/5")
    else:
        st.markdown("<div class='alert-success'><strong>Keep logging to see weak areas!</strong></div>", unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("<h3 class='section-header'>📚 Study Hours by Subject</h3>", unsafe_allow_html=True)
    
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
        st.markdown("<div class='alert-success'><strong>No data yet!</strong></div>", unsafe_allow_html=True)

# ==================== SIDEBAR ====================

st.sidebar.divider()
st.sidebar.markdown("<h3 style='color: #e0e7ff; font-weight: 900; text-align: center;'>📊 QUICK STATS</h3>", unsafe_allow_html=True)

all_tasks = get_all_tasks()
urgent = get_urgent_tasks()
progress = get_study_progress()
weak = get_weak_subjects()

col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("Pending", len(all_tasks), label_visibility="collapsed")
with col2:
    st.metric("Urgent", len(urgent), label_visibility="collapsed")

st.sidebar.metric("Sessions", len(progress), label_visibility="collapsed")

if weak:
    st.sidebar.markdown(f"<p style='color: #cbd5e1; font-size: 0.95rem; text-align: center;'><strong>Weakest:</strong><br>{weak[0][0]}</p>", unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.markdown("""
<p style='color: #cbd5e1; font-size: 0.85rem; text-align: center;'>
✨ Kriti's PA Agent<br>
Your personal AI assistant<br>
Data stored locally & secure
</p>
""", unsafe_allow_html=True)
