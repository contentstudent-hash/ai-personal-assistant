# ⚡ QUICK START (15 Minutes)

## What You're Getting
A **personal AI assistant** that:
- Tells you what to do each morning
- Tracks your Bar prep progress
- Reminds you of deadlines
- Identifies weak subjects
- Learns your patterns

---

## Installation (5 Minutes)

### 1. Get API Key
- Go to: https://console.anthropic.com
- Click "API Keys" → "Create Key"
- Copy the key

### 2. Install Python
- **Mac**: Terminal → `brew install python3`
- **Windows**: Download from https://www.python.org/downloads/
- **Linux**: `sudo apt-get install python3`

### 3. Setup Folder
```bash
mkdir ai-personal-assistant
cd ai-personal-assistant
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate  # Windows
```

### 4. Install Libraries
```bash
pip install streamlit anthropic
```

### 5. Create `.env` File
In your project folder, create a file with:
```
ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
```

---

## Running It (2 Minutes)

```bash
streamlit run ai_pa_system.py
```

Browser opens automatically → You're ready!

---

## Daily Usage (5-10 Minutes Daily)

### Morning Routine (5 min)
1. Open app
2. Go to **Dashboard**
3. Click **"Generate Today's Brief"**
4. Read recommendations
5. Start with first priority

### After Study (1 min)
1. Go to **Log Study Session**
2. Pick subject
3. Enter hours + clarity (1-5)
4. Add notes
5. Submit

### After Mock (2 min)
1. Go to **Log Mock Score**
2. Enter score + total
3. Add subjects + notes
4. Submit

---

## Features Overview

| Feature | What It Does | When to Use |
|---------|------------|-----------|
| **Dashboard** | Shows your day, urgent tasks, weak areas | Every morning |
| **Daily Briefing** | AI tells you what to focus on | Start of day |
| **Add Task** | Create work + Bar prep tasks | Anytime |
| **Log Study** | Track what you studied + clarity | After each study block |
| **Log Mock** | Track practice test scores | After each mock |
| **Progress** | See your improvement + weak areas | Weekly review |
| **AI Recommendations** | Get personalized advice | When stuck/need guidance |

---

## Your Schedule (As Built In)

- **8-10am**: Revisions + Planning (High Energy ⚡)
- **10-11am**: Break
- **11:30am-3/4pm**: Work (Gradually decreasing)
- **6pm**: Evening break
- **6pm-9:30pm**: Bar prep (High Energy ⚡)

→ AI uses this to suggest what to study when

---

## What the AI Recommends

Every morning, the AI tells you:

1. **TODAY'S PRIORITY PLAN** - What to focus on
2. **URGENT REMINDERS** - What's due soon
3. **STUDY FOCUS** - Which weak subject to tackle
4. **WORK PREP** - What content to create for classes
5. **MOTIVATIONAL NOTE** - Encouragement
6. **NEXT STEPS** - What to prepare for tomorrow

---

## Bar Subjects It Tracks

- Civil Procedure
- Constitutional Law
- Contracts
- Criminal Law
- Criminal Procedure
- Torts
- Property
- Evidence
- Business Organizations
- Community Property
- Wills & Trusts
- Remedies

---

## Your Work Categories

- Work - Content (Creating new course materials)
- Work - Class Management (Managing classes + students)
- Work - Reporting (Managing your 7-8 team members)
- Bar Prep - Essay
- Bar Prep - MBE
- Bar Prep - PT
- Administrative

---

## Cost

- **App**: Free (you're running it locally)
- **Claude API**: ~$1-2/month (very cheap!)
- **Total**: ~$2/month

---

## If Something Goes Wrong

### "Module not found"
```bash
source venv/bin/activate  # Mac/Linux
pip install streamlit anthropic
```

### "API key error"
1. Check `.env` file exists
2. Check key is correct (starts with `sk-ant-`)
3. Restart app

### "Port already in use"
```bash
streamlit run ai_pa_system.py --server.port 8502
```

---

## Pro Tips

✅ **Morning**: Always check your daily briefing first
✅ **Logging**: Log study sessions immediately (don't wait)
✅ **Mocks**: Log every mock score (builds AI understanding)
✅ **Weak Areas**: AI identifies them automatically - focus there!
✅ **Customization**: Ask me to modify anything
✅ **Backup**: Your data is saved locally in `ai_pa.db`

---

## Next Steps After Setup

1. ✅ Add today's tasks
2. ✅ Check your first daily briefing
3. ✅ Log a study session
4. ✅ Log a mock score (if you have one)
5. ✅ Review progress analytics
6. ✅ Get AI recommendations

---

## Commands You'll Use

```bash
# Start the app
streamlit run ai_pa_system.py

# Stop the app
Ctrl+C

# Access the app
http://localhost:8501

# Activate environment (Mac/Linux)
source venv/bin/activate

# Activate environment (Windows)
venv\Scripts\activate
```

---

## You're Ready! 🚀

Everything is set up. You can start using it immediately. The AI will get smarter as you log more data.

**First day**: Seems like just a task tracker
**Week 2**: AI starts giving really useful recommendations
**Month 2**: The briefings are eerily accurate about what you need to focus on

Enjoy! Let me know if you need any customization. 💪
