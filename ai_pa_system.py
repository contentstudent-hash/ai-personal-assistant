import streamlit as st
import sqlite3
from datetime import datetime, timedelta
import os

# Set page config
st.set_page_config(page_title="AI Personal Assistant", layout="wide")

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

# ==================== CSS STYLING ====================

st.markdown("""
<style>
.work-task { 
    background-color: #e8f5e9; 
    padding: 15px; 
    border-radius: 8px; 
    margin: 10px 0; 
    border-left: 5px solid #4caf50;
}
.bar-task { 
    background-color: #e3f2fd; 
    padding: 15px; 
    border-radius: 8px; 
    margin: 10px 0; 
    border-left: 5px solid #2196f3;
}
.urgent-task { 
    background-color: #ffebee; 
    padding: 15px; 
    border-radius: 8px; 
    margin: 10px 0; 
    border-left: 5px solid #f44336;
    font-weight: bold;
}
.alert-banner {
    background-color: #fff3cd;
    padding: 15px;
    border-radius: 8px;
    margin: 15px 0;
    border-left: 5px solid #ffc107;
}
</style>
""", unsafe_allow_html=True)

# ==================== MAIN APP ====================

st.title("🤖 AI Personal Assistant")
st.subheader("Bar Exam Prep & Work Manager")

# Sidebar
page = st.sidebar.radio("📍 Navigation", 
    ["📊 Dashboard", "💼 Work Tasks", "📚 Bar Prep", "📈 Analytics"])

init_db()

# ==================== DASHBOARD ====================

if page == "📊 Dashboard":
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    all_tasks = get_all_tasks()
    work_tasks = get_tasks_by_type("work")
    bar_tasks = get_tasks_by_type("bar")
    urgent = get_urgent_tasks()
    
    with col1:
        st.metric("📋 Total Tasks", len(all_tasks))
    with col2:
        st.metric("💼 Work", len(work_tasks))
    with col3:
        st.metric("📚 Bar Prep", len(bar_tasks))
    with col4:
        st.metric("⚠️ Urgent", len(urgent))
    
    st.divider()
    
    # ===== ALERTS =====
    if urgent:
        st.markdown("""
        <div class="alert-banner">
        <b>🔴 URGENT TASKS (Next 3 Days)</b>
        </div>
        """, unsafe_allow_html=True)
        
        for task in urgent:
            task_id, title, desc, category, task_type, due_date, priority, status, created = task
            st.markdown(f'<div class="urgent-task">⚠️ {title}<br>📅 Due: {due_date} | Priority: {priority}</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # ===== TASK OVERVIEW =====
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💼 Work Tasks")
        if work_tasks:
            for task in work_tasks[:5]:
                task_id, title, desc, category, task_type, due_date, priority, status, created = task
                col_t, col_b = st.columns([4, 1])
                with col_t:
                    st.markdown(f'<div class="work-task"><b>{title}</b><br>📅 {due_date}</div>', unsafe_allow_html=True)
                with col_b:
                    if st.button("✅", key=f"w{task_id}"):
                        complete_task(task_id)
                        st.rerun()
        else:
            st.success("✅ No work tasks!")
    
    with col2:
        st.subheader("📚 Bar Prep Tasks")
        if bar_tasks:
            for task in bar_tasks[:5]:
                task_id, title, desc, category, task_type, due_date, priority, status, created = task
                col_t, col_b = st.columns([4, 1])
                with col_t:
                    st.markdown(f'<div class="bar-task"><b>{title}</b><br>📅 {due_date}</div>', unsafe_allow_html=True)
                with col_b:
                    if st.button("✅", key=f"b{task_id}"):
                        complete_task(task_id)
                        st.rerun()
        else:
            st.success("✅ No Bar prep tasks!")

# ==================== WORK TASKS ====================

elif page == "💼 Work Tasks":
    st.subheader("💼 Work Tasks Management")
    
    with st.form("work_form"):
        st.write("**Add a new work task:**")
        title = st.text_input("Task Title", placeholder="e.g., Create Constitutional Law content")
        desc = st.text_area("Description", placeholder="Details about this task")
        
        col1, col2 = st.columns(2)
        with col1:
            task_type = st.selectbox("Work Type", [
                "Work - Content Creation",
                "Work - Class Management",
                "Work - Team Reporting"
            ])
            due = st.date_input("Due Date")
        
        with col2:
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
        
        if st.form_submit_button("➕ Add Work Task", use_container_width=True):
            if title:
                add_task(title, desc, task_type, str(due), priority)
                st.success(f"✅ Task added: {title}")
            else:
                st.error("Please enter a task title")
    
    st.divider()
    st.subheader("📋 Your Work Tasks")
    
    work_tasks = get_tasks_by_type("work")
    
    if work_tasks:
        for task in work_tasks:
            task_id, title, desc, category, task_type, due_date, priority, status, created = task
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f'<div class="work-task"><b>{title}</b><br>{desc[:100]}<br>📅 Due: {due_date} | Priority: {priority}</div>', unsafe_allow_html=True)
            with col2:
                if st.button("✅ Complete", key=f"comp_w{task_id}"):
                    complete_task(task_id)
                    st.rerun()
    else:
        st.info("No work tasks yet. Add one above!")

# ==================== BAR PREP ====================

elif page == "📚 Bar Prep":
    st.subheader("📚 Bar Exam Preparation")
    
    tab1, tab2, tab3 = st.tabs(["📝 Tasks", "📖 Study Sessions", "🎯 Mock Scores"])
    
    # ===== TASKS TAB =====
    with tab1:
        st.write("**Add a Bar prep task:**")
        
        with st.form("bar_form"):
            title = st.text_input("Task Title", placeholder="e.g., Constitutional Law essay practice")
            desc = st.text_area("Description")
            
            col1, col2 = st.columns(2)
            with col1:
                task_type = st.selectbox("Bar Task Type", [
                    "Bar Prep - Essay",
                    "Bar Prep - MBE",
                    "Bar Prep - Performance Test"
                ])
                due = st.date_input("Due Date")
            
            with col2:
                priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
            
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
                    st.markdown(f'<div class="bar-task"><b>{title}</b><br>{desc[:100]}<br>📅 Due: {due_date} | Priority: {priority}</div>', unsafe_allow_html=True)
                with col2:
                    if st.button("✅ Complete", key=f"comp_b{task_id}"):
                        complete_task(task_id)
                        st.rerun()
        else:
            st.info("No Bar prep tasks yet. Add one above!")
    
    # ===== STUDY TAB =====
    with tab2:
        st.write("**Log your study session:**")
        
        bar_subjects = [
            "Civil Procedure", "Constitutional Law", "Contracts", 
            "Criminal Law", "Criminal Procedure", "Torts", 
            "Property", "Evidence", "Business Organizations",
            "Community Property", "Wills & Trusts", "Remedies"
        ]
        
        with st.form("study_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                subject = st.selectbox("Subject Studied", bar_subjects)
                hours = st.number_input("Hours Spent", min_value=0.5, max_value=8.0, step=0.5, value=1.5)
            
            with col2:
                clarity = st.slider("Concept Clarity (1=Confused, 5=Mastered)", 1, 5, 3)
                notes = st.text_area("What did you learn?", placeholder="Key concepts, confusing areas, etc.")
            
            if st.form_submit_button("📚 Log Study Session", use_container_width=True):
                log_study(subject, hours, clarity, notes)
                st.success(f"✅ Study session logged: {subject} ({hours}h)")
        
        st.divider()
        st.write("**Recent Study Sessions:**")
        
        progress = get_study_progress()
        if progress:
            for p in progress[:10]:
                prog_id, subject, date, hours, clarity, notes = p
                st.markdown(f"📚 **{subject}** - {hours}h (Clarity: {clarity}/5)")
                st.caption(f"Date: {date[:10]} | Notes: {notes[:50]}")
        else:
            st.info("No study sessions logged yet.")
    
    # ===== MOCKS TAB =====
    with tab3:
        st.write("**Log a mock exam score:**")
        
        with st.form("mock_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                exam_type = st.selectbox("Test Type", [
                    "Essay (Single)",
                    "Essay (Multiple)",
                    "Performance Test",
                    "MBE Section",
                    "Full MBE (200q)",
                    "Full Practice Exam"
                ])
                score = st.number_input("Your Score", min_value=0, step=1, value=0)
            
            with col2:
                total = st.number_input("Total Points", min_value=1, step=1, value=100)
                subjects = st.text_input("Subjects Covered (comma-separated)", placeholder="e.g., Constitutional Law, Torts")
            
            notes = st.text_area("How did you feel? What went well?", placeholder="Your notes on the test")
            
            if st.form_submit_button("🎯 Log Mock Score", use_container_width=True):
                log_mock(exam_type, score, total, notes)
                percentage = (score / total * 100) if total > 0 else 0
                st.success(f"✅ Mock score logged: {percentage:.1f}%")
        
        st.divider()
        st.write("**Mock Score History:**")
        
        # Read mock scores
        conn = init_db()
        c = conn.cursor()
        c.execute('SELECT * FROM mock_scores ORDER BY date DESC LIMIT 10')
        mocks = c.fetchall()
        conn.close()
        
        if mocks:
            for m in mocks:
                mock_id, exam_type, score, total, date, notes = m
                percentage = (score / total * 100) if total > 0 else 0
                st.markdown(f"🎯 **{exam_type}**: {score}/{total} ({percentage:.1f}%)")
                st.caption(f"Date: {date[:10]}")
        else:
            st.info("No mock scores logged yet.")

# ==================== ANALYTICS ====================

elif page == "📈 Analytics":
    st.subheader("📈 Your Progress & Analytics")
    
    progress = get_study_progress()
    weak = get_weak_subjects()
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    
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
    st.subheader("🔍 Weak Subject Areas")
    
    if weak:
        for subject in weak[:10]:
            subject_name, avg_clarity, sessions = subject
            clarity_pct = (avg_clarity / 5) * 100
            
            st.write(f"**{subject_name}**")
            st.write(f"Clarity: {avg_clarity:.1f}/5 | Sessions: {sessions}")
            st.progress(clarity_pct / 100)
            st.write("")
    else:
        st.info("No weak subjects identified yet. Keep logging study sessions!")
    
    st.divider()
    
    # Study Progress Chart
    st.subheader("📚 Study Activity")
    
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
        st.info("No study data yet. Log some sessions to see charts!")

# ==================== SIDEBAR ====================

st.sidebar.divider()
st.sidebar.subheader("📊 Quick Stats")

all_tasks = get_all_tasks()
urgent = get_urgent_tasks()
progress = get_study_progress()
weak = get_weak_subjects()

st.sidebar.metric("Pending Tasks", len(all_tasks))
st.sidebar.metric("Urgent (3 days)", len(urgent))
st.sidebar.metric("Study Sessions", len(progress))

if weak:
    st.sidebar.metric("Weakest Subject", weak[0][0])

st.sidebar.divider()
st.sidebar.info("✅ Your data is stored locally and private.")
