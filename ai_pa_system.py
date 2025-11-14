import streamlit as st
import sqlite3
from datetime import datetime, timedelta
import anthropic
import os

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

# ==================== TASKS ====================

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

# ==================== STUDY ====================

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

# ==================== AI ENGINE ====================

def generate_briefing(urgent_tasks, weak_subjects, recent_progress, energy_level):
    """Generate daily briefing"""
    try:
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        prompt = f"""You are an AI Personal Assistant for a legal professional preparing for the California Bar Exam.

CONTEXT:
- Works 5-6 hours daily managing courses and team
- Preparing for Bar exam (Feb 2026)
- High energy: Morning (8-10am) and Evening (6-9:30pm)
- Today's energy: {energy_level}

URGENT TASKS (Next 3 Days):
{urgent_tasks if urgent_tasks else "None"}

WEAK SUBJECTS (Need Focus):
{weak_subjects if weak_subjects else "None"}

RECENT STUDY:
{recent_progress if recent_progress else "No data yet"}

Generate a SHORT, ACTIONABLE daily briefing with:
1. TOP 3 PRIORITIES for today
2. URGENT ALERTS
3. WEAK AREA TO FOCUS ON
4. QUICK MOTIVATIONAL NOTE

Keep it concise and practical."""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text
    except Exception as e:
        return f"Could not generate briefing: {str(e)}"

# ==================== UI ====================

st.set_page_config(page_title="AI Personal Assistant", layout="wide")

st.markdown("""
<style>
.work-task { background-color: #e8f5e9; padding: 15px; border-radius: 5px; margin: 10px 0; border-left: 4px solid #4caf50; }
.bar-task { background-color: #e3f2fd; padding: 15px; border-radius: 5px; margin: 10px 0; border-left: 4px solid #2196f3; }
.urgent-task { background-color: #ffebee; padding: 15px; border-radius: 5px; margin: 10px 0; border-left: 4px solid #f44336; }
</style>
""", unsafe_allow_html=True)

st.title("🤖 AI Personal Assistant")

# Sidebar
page = st.sidebar.radio("Navigation", ["📊 Dashboard", "💼 Work", "📚 Bar Prep", "📈 Analytics", "💡 AI Assistant"])

# ==================== DASHBOARD ====================

if page == "📊 Dashboard":
    col1, col2, col3, col4 = st.columns(4)
    
    all_tasks = get_all_tasks()
    work_tasks = get_tasks_by_type("work")
    bar_tasks = get_tasks_by_type("bar")
    urgent = get_urgent_tasks()
    
    with col1:
        st.metric("Total Tasks", len(all_tasks))
    with col2:
        st.metric("Work Tasks", len(work_tasks))
    with col3:
        st.metric("Bar Prep", len(bar_tasks))
    with col4:
        st.metric("Urgent", len(urgent))
    
    st.divider()
    
    st.subheader("📅 Your Daily Briefing")
    
    col1, col2 = st.columns(2)
    with col1:
        energy = st.selectbox("Energy Level:", ["High Morning & Evening ⚡", "Medium", "Low"])
    with col2:
        schedule = st.text_input("Special schedule?", "")
    
    if st.button("🚀 Generate Briefing", use_container_width=True):
        with st.spinner("🤔 Generating..."):
            urgent_str = "\n".join([f"- {t[1]} (Due: {t[5]})" for t in urgent[:3]]) if urgent else "None"
            weak = get_weak_subjects()
            weak_str = "\n".join([f"- {w[0]} ({w[1]:.1f}/5)" for w in weak[:3]]) if weak else "None"
            progress = get_study_progress()
            progress_str = f"{len(progress)} sessions logged" if progress else "No sessions yet"
            
            briefing = generate_briefing(urgent_str, weak_str, progress_str, energy)
            st.info(briefing)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💼 Work Tasks")
        for task in work_tasks[:5]:
            st.markdown(f'<div class="work-task"><b>{task[1]}</b><br>Due: {task[5]} | {task[6]}</div>', unsafe_allow_html=True)
    
    with col2:
        st.subheader("📚 Bar Prep Tasks")
        for task in bar_tasks[:5]:
            st.markdown(f'<div class="bar-task"><b>{task[1]}</b><br>Due: {task[5]} | {task[6]}</div>', unsafe_allow_html=True)

# ==================== WORK ====================

elif page == "💼 Work":
    st.subheader("💼 Work Tasks")
    
    with st.form("work_form"):
        title = st.text_input("Task Title")
        desc = st.text_area("Description")
        task_type = st.selectbox("Type", ["Work - Content", "Work - Class Management", "Work - Reporting"])
        due = st.date_input("Due Date")
        priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
        
        if st.form_submit_button("➕ Add Task"):
            add_task(title, desc, task_type, str(due), priority)
            st.success("Task added!")
    
    st.divider()
    
    st.subheader("Your Work Tasks")
    work_tasks = get_tasks_by_type("work")
    
    if work_tasks:
        for task in work_tasks:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f'<div class="work-task"><b>{task[1]}</b><br>{task[2][:80]}<br>Due: {task[5]}</div>', unsafe_allow_html=True)
            with col2:
                if st.button("✅", key=f"w{task[0]}"):
                    complete_task(task[0])
                    st.rerun()

# ==================== BAR PREP ====================

elif page == "📚 Bar Prep":
    tab1, tab2, tab3 = st.tabs(["📝 Tasks", "📖 Study", "🎯 Mocks"])
    
    with tab1:
        with st.form("bar_form"):
            title = st.text_input("Task Title")
            desc = st.text_area("Description")
            task_type = st.selectbox("Type", ["Bar Prep - Essay", "Bar Prep - MBE", "Bar Prep - PT"])
            due = st.date_input("Due Date")
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
            
            if st.form_submit_button("➕ Add Task"):
                add_task(title, desc, task_type, str(due), priority)
                st.success("Task added!")
        
        st.divider()
        
        bar_tasks = get_tasks_by_type("bar")
        for task in bar_tasks:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f'<div class="bar-task"><b>{task[1]}</b><br>{task[2][:80]}<br>Due: {task[5]}</div>', unsafe_allow_html=True)
            with col2:
                if st.button("✅", key=f"b{task[0]}"):
                    complete_task(task[0])
                    st.rerun()
    
    with tab2:
        st.subheader("📚 Log Study Session")
        
        bar_subjects = ["Civil Procedure", "Constitutional Law", "Contracts", "Criminal Law", 
                       "Criminal Procedure", "Torts", "Property", "Evidence", "Business Orgs",
                       "Community Property", "Wills & Trusts", "Remedies"]
        
        with st.form("study_form"):
            subject = st.selectbox("Subject", bar_subjects)
            hours = st.number_input("Hours", 0.5, 8.0, 1.5, 0.5)
            clarity = st.slider("Clarity (1-5)", 1, 5, 3)
            notes = st.text_area("Notes")
            
            if st.form_submit_button("📚 Log Session"):
                log_study(subject, hours, clarity, notes)
                st.success("Session logged!")
    
    with tab3:
        st.subheader("🎯 Log Mock Score")
        
        with st.form("mock_form"):
            exam_type = st.selectbox("Test Type", ["Essay", "MBE", "Performance Test", "Full Exam"])
            score = st.number_input("Score", 0)
            total = st.number_input("Total Points", 1, value=100)
            notes = st.text_area("Notes")
            
            if st.form_submit_button("🎯 Log Score"):
                log_mock(exam_type, score, total, notes)
                percentage = (score / total * 100) if total > 0 else 0
                st.success(f"Score logged: {percentage:.1f}%")

# ==================== ANALYTICS ====================

elif page == "📈 Analytics":
    st.subheader("📈 Your Progress")
    
    progress = get_study_progress()
    weak = get_weak_subjects()
    
    col1, col2, col3 = st.columns(3)
    
    if progress:
        total_hours = sum([p[2] for p in progress])
        with col1:
            st.metric("Total Study Hours", f"{total_hours:.1f}h")
    
    if weak:
        avg_clarity = sum([w[1] for w in weak]) / len(weak)
        with col2:
            st.metric("Avg Clarity", f"{avg_clarity:.1f}/5")
    
    completed = len([t for t in get_all_tasks() if t[7] == "completed"])
    with col3:
        st.metric("Tasks Completed", completed)
    
    st.divider()
    
    st.subheader("🔍 Weak Subjects")
    if weak:
        for subject in weak[:8]:
            st.write(f"**{subject[0]}**: {subject[1]:.1f}/5")
            st.progress(subject[1] / 5)

# ==================== AI ASSISTANT ====================

elif page == "💡 AI Assistant":
    st.subheader("💡 AI Recommendations")
    
    if st.button("Get Recommendations"):
        with st.spinner("Thinking..."):
            weak = get_weak_subjects()
            progress = get_study_progress()
            
            weak_str = "\n".join([f"- {w[0]}: {w[1]:.1f}/5" for w in weak]) if weak else "None"
            progress_str = f"{len(progress)} sessions" if progress else "No sessions"
            
            try:
                client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
                
                prompt = f"""Based on this Bar exam prep data:

Weak Areas: {weak_str}
Study Sessions: {progress_str}

Provide 3-4 specific, actionable recommendations."""

                message = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=400,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                st.success(message.content[0].text)
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.sidebar.divider()
st.sidebar.info("Your data is stored locally. Never shared.")
