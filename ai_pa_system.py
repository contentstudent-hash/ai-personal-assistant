import streamlit as st
import sqlite3
from datetime import datetime, timedelta

# Set page config
st.set_page_config(
    page_title="AI Personal Assistant", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CLEAN, PROFESSIONAL CSS ====================

st.markdown("""
<style>
/* Overall styling */
body {
    background-color: #f8f9fa;
    color: #1a1a1a;
}

/* Main container */
.main {
    background-color: #ffffff;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #2c3e50;
}

[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* Header styling */
.header-container {
    background: linear-gradient(90deg, #2c3e50 0%, #34495e 100%);
    padding: 30px;
    border-radius: 10px;
    margin-bottom: 30px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-title {
    color: #ffffff;
    font-size: 2.8rem;
    font-weight: 800;
    margin: 0;
    text-align: center;
}

.header-subtitle {
    color: #ecf0f1;
    font-size: 1.1rem;
    text-align: center;
    margin-top: 10px;
}

/* Cards - Task cards */
.task-card {
    background-color: #ffffff;
    border: 2px solid #ecf0f1;
    border-radius: 8px;
    padding: 18px;
    margin: 12px 0;
    transition: all 0.3s ease;
}

.task-card:hover {
    border-color: #3498db;
    box-shadow: 0 4px 12px rgba(52, 152, 219, 0.15);
}

/* Work tasks - Green left border */
.work-task {
    border-left: 5px solid #27ae60;
    background-color: #f0fdf4;
}

.work-task:hover {
    border-color: #27ae60;
    background-color: #e8fde8;
}

/* Bar prep tasks - Blue left border */
.bar-task {
    border-left: 5px solid #2980b9;
    background-color: #f0f7fd;
}

.bar-task:hover {
    border-color: #2980b9;
    background-color: #e8f4fd;
}

/* Urgent tasks - Red left border */
.urgent-task {
    border-left: 5px solid #e74c3c;
    background-color: #fdf4f0;
    font-weight: 600;
}

.urgent-task:hover {
    border-color: #c0392b;
    background-color: #fde8e0;
}

/* Task title styling */
.task-title {
    color: #1a1a1a;
    font-size: 1.05rem;
    font-weight: 700;
    margin: 0 0 8px 0;
}

.task-meta {
    color: #555555;
    font-size: 0.9rem;
    margin: 0;
}

/* Metrics styling */
[data-testid="metric-container"] {
    background: #ffffff;
    border: 2px solid #ecf0f1;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
}

[data-testid="metric-container"]:hover {
    border-color: #3498db;
    box-shadow: 0 4px 12px rgba(52, 152, 219, 0.15);
}

/* Alert banners */
.alert-banner {
    background-color: #fff3cd;
    border: 2px solid #ffc107;
    padding: 18px;
    border-radius: 8px;
    margin: 20px 0;
    color: #856404;
}

.alert-critical {
    background-color: #f8d7da;
    border: 2px solid #f5c6cb;
    padding: 18px;
    border-radius: 8px;
    margin: 20px 0;
    color: #721c24;
    font-weight: 600;
}

.alert-success {
    background-color: #d4edda;
    border: 2px solid #c3e6cb;
    padding: 18px;
    border-radius: 8px;
    margin: 20px 0;
    color: #155724;
}

/* Form styling */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > select {
    border: 2px solid #ecf0f1 !important;
    border-radius: 6px !important;
    padding: 12px !important;
    font-size: 1rem !important;
    color: #1a1a1a !important;
    background-color: #ffffff !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stSelectbox > div > div > select:focus {
    border-color: #2980b9 !important;
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(41, 128, 185, 0.1) !important;
}

/* Buttons */
.stButton > button {
    background-color: #2980b9 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
    cursor: pointer !important;
    width: 100% !important;
}

.stButton > button:hover {
    background-color: #1e5f96 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(41, 128, 185, 0.3) !important;
}

/* Section headers */
.section-header {
    color: #2c3e50;
    font-size: 1.6rem;
    font-weight: 700;
    margin: 30px 0 20px 0;
    padding-bottom: 12px;
    border-bottom: 3px solid #2980b9;
}

.section-header-green {
    border-bottom-color: #27ae60;
    color: #27ae60;
}

.section-header-blue {
    border-bottom-color: #2980b9;
    color: #2980b9;
}

/* Tabs */
[role="tablist"] {
    background-color: transparent !important;
    border-bottom: 2px solid #ecf0f1 !important;
}

[role="tab"] {
    background-color: transparent !important;
    color: #555555 !important;
    border: none !important;
    border-bottom: 3px solid transparent !important;
    padding: 12px 20px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
}

[role="tab"][aria-selected="true"] {
    color: #2980b9 !important;
    border-bottom-color: #2980b9 !important;
}

/* Dividers */
hr {
    margin: 25px 0 !important;
    border: none !important;
    border-top: 2px solid #ecf0f1 !important;
}

/* Text colors */
h1 {
    color: #2c3e50 !important;
    font-weight: 700 !important;
}

h2 {
    color: #2c3e50 !important;
    font-weight: 700 !important;
}

h3 {
    color: #34495e !important;
    font-weight: 600 !important;
}

/* Progress bar */
[role="progressbar"] {
    background: linear-gradient(90deg, #2980b9, #3498db) !important;
}

/* Info/Success/Error messages */
.stSuccess {
    background-color: #d4edda !important;
    color: #155724 !important;
    border: 2px solid #c3e6cb !important;
}

.stError {
    background-color: #f8d7da !important;
    color: #721c24 !important;
    border: 2px solid #f5c6cb !important;
}

.stInfo {
    background-color: #d1ecf1 !important;
    color: #0c5460 !important;
    border: 2px solid #bee5eb !important;
}

/* Slider styling */
[data-testid="stSlider"] {
    padding: 20px 0;
}

/* Label styling */
label {
    color: #2c3e50 !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
}

/* Complete button styling */
.complete-btn {
    background-color: #27ae60 !important;
    color: #ffffff !important;
    border: none !important;
    padding: 8px 12px !important;
    border-radius: 4px !important;
    cursor: pointer !important;
    font-weight: 600 !important;
}

.complete-btn:hover {
    background-color: #229954 !important;
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
    <h1 class="header-title">🤖 AI Personal Assistant</h1>
    <p class="header-subtitle">Bar Exam Prep & Work Manager</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("📍 Navigation")
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
    
    # Quick Stats Row
    st.markdown("<h2 style='color: #2c3e50; margin-bottom: 20px;'>📊 Quick Overview</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4, gap="large")
    
    with col1:
        st.metric("📋 Total Tasks", len(all_tasks))
    with col2:
        st.metric("💼 Work Tasks", len(work_tasks))
    with col3:
        st.metric("📚 Bar Prep", len(bar_tasks))
    with col4:
        st.metric("⚠️ Urgent", len(urgent))
    
    st.divider()
    
    # Urgent Alerts
    if urgent:
        st.markdown("""
        <div class="alert-critical">
        <strong>🔴 URGENT TASKS - Next 3 Days</strong>
        </div>
        """, unsafe_allow_html=True)
        
        for task in urgent:
            task_id, title, desc, category, task_type, due_date, priority, status, created = task
            st.markdown(f"""
            <div class="task-card urgent-task">
                <p class="task-title">⚠️ {title}</p>
                <p class="task-meta">📅 Due: {due_date} | 🎯 Priority: {priority}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Task Overview
    st.markdown("<h2 style='color: #2c3e50; margin-bottom: 20px;'>Your Tasks</h2>", unsafe_allow_html=True)
    
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
                        <p class="task-title">{title}</p>
                        <p class="task-meta">📅 {due_date}</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col_b:
                    if st.button("✅", key=f"w{task_id}", help="Mark complete"):
                        complete_task(task_id)
                        st.rerun()
        else:
            st.markdown("<div class='alert-success'><strong>✅ No work tasks</strong></div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h3 class='section-header section-header-blue'>📚 Bar Prep Tasks</h3>", unsafe_allow_html=True)
        if bar_tasks:
            for task in bar_tasks[:5]:
                task_id, title, desc, category, task_type, due_date, priority, status, created = task
                col_t, col_b = st.columns([4, 1])
                with col_t:
                    st.markdown(f"""
                    <div class="task-card bar-task">
                        <p class="task-title">{title}</p>
                        <p class="task-meta">📅 {due_date}</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col_b:
                    if st.button("✅", key=f"b{task_id}", help="Mark complete"):
                        complete_task(task_id)
                        st.rerun()
        else:
            st.markdown("<div class='alert-success'><strong>✅ No Bar prep tasks</strong></div>", unsafe_allow_html=True)

# ==================== WORK TASKS ====================

elif page == "💼 Work Tasks":
    st.markdown("<h2 class='section-header section-header-green'>💼 Work Tasks Management</h2>", unsafe_allow_html=True)
    
    st.markdown("<p style='color: #555; font-size: 1.05rem; margin-bottom: 20px;'><strong>Add a New Work Task</strong></p>", unsafe_allow_html=True)
    
    with st.form("work_form"):
        title = st.text_input("Task Title", placeholder="e.g., Create Constitutional Law content")
        desc = st.text_area("Description (Optional)", placeholder="Add details about this task", height=80)
        
        col1, col2 = st.columns(2)
        with col1:
            task_type = st.selectbox("Work Type", [
                "Work - Content Creation",
                "Work - Class Management",
                "Work - Team Reporting"
            ])
        with col2:
            priority = st.selectbox("Priority Level", ["Low", "Medium", "High", "Urgent"])
        
        due = st.date_input("Due Date")
        
        if st.form_submit_button("➕ Add Work Task"):
            if title:
                add_task(title, desc, task_type, str(due), priority)
                st.success(f"✅ Task added: {title}")
            else:
                st.error("❌ Please enter a task title")
    
    st.divider()
    
    st.markdown("<h3 style='color: #27ae60; font-weight: 700; margin-bottom: 20px;'>📋 Your Work Tasks</h3>", unsafe_allow_html=True)
    
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
                    <p class="task-meta">📅 Due: {due_date} | 🎯 {priority}</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("✅ Done", key=f"comp_w{task_id}"):
                    complete_task(task_id)
                    st.rerun()
    else:
        st.markdown("<div class='alert-success'><strong>✅ No work tasks. Add one above!</strong></div>", unsafe_allow_html=True)

# ==================== BAR PREP ====================

elif page == "📚 Bar Prep":
    st.markdown("<h2 class='section-header section-header-blue'>📚 Bar Exam Preparation</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📝 Tasks", "📖 Study Sessions", "🎯 Mock Scores"])
    
    # ===== TASKS TAB =====
    with tab1:
        st.markdown("<p style='color: #555; font-size: 1.05rem; margin-bottom: 20px;'><strong>Add a New Bar Prep Task</strong></p>", unsafe_allow_html=True)
        
        with st.form("bar_form"):
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
                priority = st.selectbox("Priority Level", ["Low", "Medium", "High", "Urgent"])
            
            due = st.date_input("Due Date")
            
            if st.form_submit_button("➕ Add Bar Task"):
                if title:
                    add_task(title, desc, task_type, str(due), priority)
                    st.success(f"✅ Task added: {title}")
                else:
                    st.error("❌ Please enter a task title")
        
        st.divider()
        
        st.markdown("<h3 style='color: #2980b9; font-weight: 700; margin-bottom: 20px;'>📋 Your Bar Prep Tasks</h3>", unsafe_allow_html=True)
        
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
                        <p class="task-meta">📅 Due: {due_date} | 🎯 {priority}</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("✅ Done", key=f"comp_b{task_id}"):
                        complete_task(task_id)
                        st.rerun()
        else:
            st.markdown("<div class='alert-success'><strong>✅ No Bar prep tasks. Add one above!</strong></div>", unsafe_allow_html=True)
    
    # ===== STUDY TAB =====
    with tab2:
        st.markdown("<p style='color: #555; font-size: 1.05rem; margin-bottom: 20px;'><strong>Log Your Study Session</strong></p>", unsafe_allow_html=True)
        
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
            
            notes = st.text_area("📝 What did you learn?", placeholder="Key concepts, confusing areas, etc.", height=80)
            
            if st.form_submit_button("📚 Log Study Session"):
                log_study(subject, hours, clarity, notes)
                st.success(f"✅ Logged: {subject} ({hours}h, clarity {clarity}/5)")
        
        st.divider()
        
        st.markdown("<h3 style='color: #2980b9; font-weight: 700; margin-bottom: 20px;'>📋 Recent Study Sessions</h3>", unsafe_allow_html=True)
        
        progress = get_study_progress()
        if progress:
            for p in progress[:10]:
                prog_id, subject, date, hours, clarity, notes = p
                clarity_emoji = "🔴" if clarity <= 2 else "🟡" if clarity == 3 else "🟢"
                st.markdown(f"""
                <div class="task-card">
                    <p class="task-title">{clarity_emoji} {subject}</p>
                    <p class="task-meta">{hours}h | Clarity: {clarity}/5 | {date[:10]}</p>
                    <p class="task-meta">Note: {notes[:60]}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<div class='alert-success'><strong>No study sessions yet.</strong></div>", unsafe_allow_html=True)
    
    # ===== MOCKS TAB =====
    with tab3:
        st.markdown("<p style='color: #555; font-size: 1.05rem; margin-bottom: 20px;'><strong>Log a Mock Exam Score</strong></p>", unsafe_allow_html=True)
        
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
            
            if st.form_submit_button("🎯 Log Mock Score"):
                log_mock(exam_type, score, total, notes)
                percentage = (score / total * 100) if total > 0 else 0
                st.success(f"✅ Mock logged: {percentage:.1f}%")
        
        st.divider()
        
        st.markdown("<h3 style='color: #2980b9; font-weight: 700; margin-bottom: 20px;'>🎯 Mock Score History</h3>", unsafe_allow_html=True)
        
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
            st.markdown("<div class='alert-success'><strong>No mock scores yet.</strong></div>", unsafe_allow_html=True)

# ==================== ANALYTICS ====================

elif page == "📈 Analytics":
    st.markdown("<h2 class='section-header'>📈 Your Progress & Analytics</h2>", unsafe_allow_html=True)
    
    progress = get_study_progress()
    weak = get_weak_subjects()
    
    # Metrics
    col1, col2, col3 = st.columns(3, gap="large")
    
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
    st.markdown("<h3 style='color: #e74c3c; font-weight: 700; margin-bottom: 20px;'>🔍 Areas That Need Focus</h3>", unsafe_allow_html=True)
    
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
        st.markdown("<div class='alert-success'><strong>Keep logging study sessions to see your weak areas!</strong></div>", unsafe_allow_html=True)
    
    st.divider()
    
    # Study Progress Chart
    st.markdown("<h3 style='color: #2980b9; font-weight: 700; margin-bottom: 20px;'>📚 Total Study Hours by Subject</h3>", unsafe_allow_html=True)
    
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
        st.markdown("<div class='alert-success'><strong>No study data yet. Log sessions to see charts!</strong></div>", unsafe_allow_html=True)

# ==================== SIDEBAR ====================

st.sidebar.divider()
st.sidebar.markdown("<h3 style='color: #ecf0f1;'>📊 Quick Stats</h3>", unsafe_allow_html=True)

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
    st.sidebar.markdown(f"<p style='color: #ecf0f1; font-size: 0.9rem;'><strong>Weakest:</strong> {weak[0][0]}</p>", unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.markdown("""
<p style='color: #ecf0f1; font-size: 0.85rem; text-align: center;'>
✅ Your data is secure and stored locally
</p>
""", unsafe_allow_html=True)
