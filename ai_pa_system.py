import streamlit as st
import sqlite3
import json
from datetime import datetime, timedelta
import anthropic
from pathlib import Path

# ==================== DATABASE SETUP ====================

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect('ai_pa.db')
    c = conn.cursor()
    
    # Tasks table
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT,
        description TEXT,
        category TEXT,
        due_date TEXT,
        priority TEXT,
        status TEXT,
        created_date TEXT,
        completed_date TEXT
    )''')
    
    # Study Progress table
    c.execute('''CREATE TABLE IF NOT EXISTS study_progress (
        id INTEGER PRIMARY KEY,
        subject TEXT,
        date TEXT,
        hours_spent REAL,
        clarity_rating INTEGER,
        notes TEXT,
        status TEXT
    )''')
    
    # Mock/Practice Scores table
    c.execute('''CREATE TABLE IF NOT EXISTS mock_scores (
        id INTEGER PRIMARY KEY,
        exam_type TEXT,
        score INTEGER,
        total_points INTEGER,
        date TEXT,
        subjects_covered TEXT,
        notes TEXT
    )''')
    
    # Daily Log table
    c.execute('''CREATE TABLE IF NOT EXISTS daily_logs (
        id INTEGER PRIMARY KEY,
        date TEXT,
        energy_level TEXT,
        tasks_completed TEXT,
        study_hours REAL,
        notes TEXT
    )''')
    
    conn.commit()
    return conn

# ==================== TASK MANAGEMENT ====================

def add_task(title, description, category, due_date, priority):
    """Add a new task"""
    conn = init_db()
    c = conn.cursor()
    c.execute('''INSERT INTO tasks 
                 (title, description, category, due_date, priority, status, created_date)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (title, description, category, due_date, priority, 'pending', datetime.now().isoformat()))
    conn.commit()
    conn.close()
    st.success(f"✅ Task added: {title}")

def get_all_tasks():
    """Retrieve all tasks"""
    conn = init_db()
    c = conn.cursor()
    c.execute('SELECT * FROM tasks WHERE status != "completed" ORDER BY due_date ASC')
    tasks = c.fetchall()
    conn.close()
    return tasks

def get_urgent_tasks():
    """Get tasks due within 3 days"""
    conn = init_db()
    c = conn.cursor()
    today = datetime.now().date()
    three_days_later = today + timedelta(days=3)
    c.execute('''SELECT * FROM tasks 
                 WHERE status != "completed" AND due_date BETWEEN ? AND ?
                 ORDER BY due_date ASC''',
              (str(today), str(three_days_later)))
    tasks = c.fetchall()
    conn.close()
    return tasks

def complete_task(task_id):
    """Mark task as completed"""
    conn = init_db()
    c = conn.cursor()
    c.execute('UPDATE tasks SET status = ?, completed_date = ? WHERE id = ?',
              ('completed', datetime.now().isoformat(), task_id))
    conn.commit()
    conn.close()

# ==================== STUDY PROGRESS ====================

def log_study_session(subject, hours_spent, clarity_rating, notes):
    """Log a study session"""
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
    """Log a mock test score"""
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

def get_study_progress():
    """Get recent study progress"""
    conn = init_db()
    c = conn.cursor()
    c.execute('SELECT subject, hours_spent, clarity_rating, date FROM study_progress ORDER BY date DESC LIMIT 20')
    progress = c.fetchall()
    conn.close()
    return progress

def get_weak_subjects():
    """Identify weak subjects based on clarity ratings"""
    conn = init_db()
    c = conn.cursor()
    c.execute('''SELECT subject, AVG(clarity_rating) as avg_clarity, COUNT(*) as sessions
                 FROM study_progress 
                 GROUP BY subject 
                 ORDER BY avg_clarity ASC''')
    weak = c.fetchall()
    conn.close()
    return weak

def get_mock_scores():
    """Get all mock scores"""
    conn = init_db()
    c = conn.cursor()
    c.execute('SELECT * FROM mock_scores ORDER BY date DESC')
    scores = c.fetchall()
    conn.close()
    return scores

# ==================== AI ENGINE (CLAUDE) ====================

def generate_daily_briefing(user_schedule, urgent_tasks, weak_subjects, recent_progress, energy_levels):
    """Generate intelligent daily briefing using Claude"""
    client = anthropic.Anthropic()
    
    prompt = f"""You are an intelligent personal assistant helping a legal professional prepare for the California Bar Exam while managing work responsibilities.

USER PROFILE:
- Works 5-6 hours daily managing courses, classes, content creation
- Supervises 7-8 team members on various courses
- Studying for California Bar Exam (Feb 2026)
- High energy levels: Morning (8-10am) and Evening (6-9:30pm)
- Work hours: 11:30am - 3/4pm (gradually decreasing)
- Break: 10-11am, 6pm break
- Needs: Constant support, follow-ups, and interactions

TODAY'S CONTEXT:
- Current Time: {datetime.now().strftime('%A, %B %d, %Y %H:%M')}
- Energy Level Today: {energy_levels}
- Schedule: {user_schedule}

URGENT TASKS (Next 3 Days):
{urgent_tasks if urgent_tasks else "No urgent tasks"}

WEAK SUBJECTS (Needs Focus):
{weak_subjects if weak_subjects else "No data yet"}

RECENT STUDY PROGRESS:
{recent_progress if recent_progress else "No recent progress"}

Based on all this, provide a SMART, PERSONALIZED daily briefing:

1. **TODAY'S PRIORITY PLAN** (What to focus on given your energy and schedule)
2. **URGENT REMINDERS** (What deadline is coming)
3. **STUDY FOCUS** (Which weak area should you prioritize based on time availability)
4. **WORK TASK SUGGESTION** (What work content should you prep 1-2 days before classes)
5. **MOTIVATIONAL NOTE** (Brief encouragement tailored to your situation)
6. **NEXT STEPS** (What to prepare for tomorrow)

Be concise, actionable, and supportive. Remember this person is balancing intense work and Bar prep."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text

def get_personalized_recommendations(study_data, work_data):
    """Get personalized AI recommendations"""
    client = anthropic.Anthropic()
    
    prompt = f"""As an expert legal education advisor and personal development coach, analyze this person's data and provide personalized guidance:

STUDY DATA:
{study_data}

WORK DATA:
{work_data}

Provide 3-4 specific, actionable recommendations for:
1. Optimizing Bar exam prep
2. Managing work-life balance
3. Improving weak areas
4. Time management strategies

Keep it concise and practical."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=800,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text

# ==================== STREAMLIT UI ====================

st.set_page_config(page_title="AI Personal Assistant", layout="wide")
st.title("🤖 AI Personal Assistant - Bar Exam Prep & Work Manager")

# Initialize database
init_db()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", 
    ["📊 Dashboard", "➕ Add Task", "📚 Log Study Session", "🎯 Log Mock Score", "📈 Progress Analytics", "💡 AI Recommendations"])

# ==================== DASHBOARD PAGE ====================
if page == "📊 Dashboard":
    col1, col2, col3 = st.columns(3)
    
    with col1:
        all_tasks = get_all_tasks()
        st.metric("Total Pending Tasks", len(all_tasks))
    
    with col2:
        urgent = get_urgent_tasks()
        st.metric("⚠️ Urgent Tasks (3 days)", len(urgent))
    
    with col3:
        progress = get_study_progress()
        st.metric("Study Sessions Logged", len(progress))
    
    st.divider()
    
    # Daily Briefing Section
    st.subheader("📅 Your Daily Briefing")
    
    energy_input = st.selectbox("Your energy level today:", ["High Morning & Evening ⚡", "Medium", "Low"])
    custom_schedule = st.text_input("Any special schedule today? (e.g., 'Early meeting at 12pm, no evening study')")
    
    if st.button("Generate Today's Brief", key="brief"):
        with st.spinner("🤔 Generating your personalized briefing..."):
            urgent_tasks_str = "\n".join([f"- {t[1]} (Due: {t[4]})" for t in urgent[:5]]) if urgent else "None"
            weak_subjects_str = "\n".join([f"- {w[0]} (Avg Clarity: {w[1]:.1f}/5)" for w in get_weak_subjects()[:5]]) if get_weak_subjects() else "None"
            recent_prog = get_study_progress()
            recent_str = "\n".join([f"- {p[0]}: {p[1]}h (Clarity: {p[2]}/5)" for p in recent_prog[:5]]) if recent_prog else "None"
            
            briefing = generate_daily_briefing(
                user_schedule=custom_schedule or "Standard schedule",
                urgent_tasks=urgent_tasks_str,
                weak_subjects=weak_subjects_str,
                recent_progress=recent_str,
                energy_levels=energy_input
            )
            st.info(briefing)
    
    st.divider()
    
    # Quick Status
    st.subheader("Quick Status")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Urgent Tasks (Next 3 Days):**")
        if urgent:
            for task in urgent[:5]:
                st.warning(f"🔴 {task[1]} - Due: {task[4]}")
        else:
            st.success("✅ No urgent tasks!")
    
    with col2:
        st.write("**Weak Subjects (Focus Areas):**")
        weak = get_weak_subjects()
        if weak:
            for subject in weak[:5]:
                st.error(f"📉 {subject[0]} - Clarity: {subject[1]:.1f}/5")
        else:
            st.info("No weak areas identified yet. Keep studying!")

# ==================== ADD TASK PAGE ====================
elif page == "➕ Add Task":
    st.subheader("Add a New Task")
    
    col1, col2 = st.columns(2)
    
    with col1:
        task_title = st.text_input("Task Title")
        task_category = st.selectbox("Category", ["Work - Content", "Work - Class Management", "Work - Reporting", "Bar Prep - Essay", "Bar Prep - MBE", "Bar Prep - PT", "Administrative"])
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
    
    with col2:
        task_due_date = st.date_input("Due Date")
        task_description = st.text_area("Description/Notes")
    
    if st.button("Add Task"):
        if task_title:
            add_task(task_title, task_description, task_category, str(task_due_date), task_priority)
        else:
            st.error("Please enter a task title")
    
    st.divider()
    st.subheader("Your Tasks")
    tasks = get_all_tasks()
    for task in tasks:
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.write(f"**{task[1]}** ({task[3]})")
            st.caption(f"Due: {task[4]} | Priority: {task[5]}")
        with col2:
            st.caption(task[7])  # status
        with col3:
            if st.button("✅ Complete", key=f"complete_{task[0]}"):
                complete_task(task[0])
                st.rerun()

# ==================== LOG STUDY SESSION ====================
elif page == "📚 Log Study Session":
    st.subheader("Log Your Study Session")
    
    bar_subjects = ["Civil Procedure", "Constitutional Law", "Contracts", "Criminal Law", 
                    "Criminal Procedure", "Torts", "Property", "Evidence", "Business Orgs",
                    "Community Property", "Wills & Trusts", "Remedies"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        study_subject = st.selectbox("Subject Studied", bar_subjects)
        study_hours = st.number_input("Hours Spent", min_value=0.5, max_value=8.0, step=0.5)
    
    with col2:
        study_clarity = st.slider("Concept Clarity (1=Confused, 5=Perfect)", 1, 5, 3)
        study_notes = st.text_area("What did you cover? Key learnings?")
    
    if st.button("Log Study Session"):
        log_study_session(study_subject, study_hours, study_clarity, study_notes)
    
    st.divider()
    st.subheader("Recent Study Sessions")
    progress = get_study_progress()
    if progress:
        for p in progress[:10]:
            st.write(f"📚 **{p[0]}** - {p[1]}h (Clarity: {p[2]}/5)")
            st.caption(p[3])
    else:
        st.info("No study sessions logged yet")

# ==================== LOG MOCK SCORE ====================
elif page == "🎯 Log Mock Score":
    st.subheader("Log Mock/Practice Test Score")
    
    col1, col2 = st.columns(2)
    
    with col1:
        mock_type = st.selectbox("Test Type", ["Essay (Single)", "Essay (Multiple)", "Performance Test", "MBE Section", "Full MBE (200q)", "Full Practice Exam"])
        mock_score = st.number_input("Your Score", min_value=0, step=1)
    
    with col2:
        mock_total = st.number_input("Total Points", min_value=1, step=1, value=100)
        mock_subjects = st.text_input("Subjects Covered (comma-separated)")
    
    mock_notes = st.text_area("How did you feel? What went well? What struggled?")
    
    if st.button("Log Mock Score"):
        log_mock_score(mock_type, mock_score, mock_total, mock_subjects, mock_notes)
    
    st.divider()
    st.subheader("Mock Scores History")
    scores = get_mock_scores()
    if scores:
        for s in scores[:10]:
            percentage = (s[1] / s[2] * 100) if s[2] > 0 else 0
            st.write(f"🎯 **{s[1]}/{s[2]}** ({percentage:.1f}%) - {s[2]} ({s[4]})")
            st.caption(f"Subjects: {s[5]} | Notes: {s[6]}")
    else:
        st.info("No mock scores logged yet")

# ==================== PROGRESS ANALYTICS ====================
elif page == "📈 Progress Analytics":
    st.subheader("Your Bar Prep Progress")
    
    progress = get_study_progress()
    weak = get_weak_subjects()
    scores = get_mock_scores()
    
    col1, col2, col3 = st.columns(3)
    
    if progress:
        total_hours = sum([p[1] for p in progress])
        with col1:
            st.metric("Total Study Hours", f"{total_hours:.1f}h")
    
    if scores:
        latest_score = scores[0]
        latest_percentage = (latest_score[1] / latest_score[2] * 100) if latest_score[2] > 0 else 0
        with col2:
            st.metric("Latest Mock Score", f"{latest_percentage:.1f}%")
    
    if weak:
        avg_clarity = sum([p[1] for p in weak]) / len(weak)
        with col3:
            st.metric("Avg Concept Clarity", f"{avg_clarity:.1f}/5")
    
    st.divider()
    
    st.subheader("🔍 Weak Subjects Analysis")
    if weak:
        for subject in weak[:10]:
            clarity = subject[1]
            sessions = subject[2]
            bar_value = int((clarity / 5) * 100)
            st.write(f"**{subject[0]}** - Clarity: {clarity:.1f}/5 ({sessions} sessions)")
            st.progress(bar_value / 100)
    
    st.divider()
    
    st.subheader("📊 Mock Score Trend")
    if scores:
        for s in scores[:5]:
            percentage = (s[1] / s[2] * 100) if s[2] > 0 else 0
            st.write(f"{s[1]}/{s[2]} ({percentage:.1f}%) - {s[3]}")

# ==================== AI RECOMMENDATIONS ====================
elif page == "💡 AI Recommendations":
    st.subheader("Personalized AI Recommendations")
    
    if st.button("Get AI Insights", key="recommendations"):
        with st.spinner("🧠 Analyzing your progress..."):
            weak = get_weak_subjects()
            progress = get_study_progress()
            scores = get_mock_scores()
            tasks = get_all_tasks()
            
            weak_str = "\n".join([f"- {w[0]}: {w[1]:.1f}/5 clarity" for w in weak]) if weak else "None"
            progress_str = f"Total sessions: {len(progress)}, Total hours: {sum([p[1] for p in progress]):.1f}h" if progress else "No data"
            scores_str = f"Latest: {scores[0][1]}/{scores[0][2]} ({(scores[0][1]/scores[0][2]*100):.1f}%)" if scores else "No mocks"
            work_load = f"{len([t for t in tasks if 'Work' in t[3]])} work tasks, {len([t for t in tasks if 'Bar' in t[3]])} Bar tasks"
            
            recommendations = get_personalized_recommendations(
                study_data=f"Weak areas:\n{weak_str}\n\nProgress:\n{progress_str}\n\nMock Scores:\n{scores_str}",
                work_data=f"Task load: {work_load}"
            )
            
            st.success(recommendations)

st.sidebar.divider()
st.sidebar.info("💡 Tip: Check your Daily Briefing regularly for personalized guidance!")
