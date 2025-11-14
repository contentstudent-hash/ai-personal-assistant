# 🤖 AI Personal Assistant - Complete Setup Guide

Your AI PA system is ready! This guide will take you from zero to running in under 20 minutes.

---

## STEP 1: Get Your Claude API Key (2 minutes)

1. Go to: https://console.anthropic.com
2. Sign up or log in with Google/email
3. Click "API Keys" in the left sidebar
4. Click "Create Key"
5. Copy the key (it looks like: `sk-ant-...`)
6. **SAVE IT SOMEWHERE SAFE** - you'll need it in Step 4

💡 **Cost**: ~$1-2/month for your usage (very cheap!)

---

## STEP 2: Install Python (If You Don't Have It)

### On Mac:
1. Open Terminal
2. Copy-paste: `brew install python3`
3. Wait for installation
4. Done!

### On Windows:
1. Go to: https://www.python.org/downloads/
2. Click "Download Python 3.11"
3. Run the installer
4. **CHECK THE BOX** "Add Python to PATH"
5. Click Install
6. Done!

### On Linux:
```bash
sudo apt-get install python3 python3-pip
```

**Check it worked**:
- Open Terminal/Command Prompt
- Type: `python3 --version`
- Should show: Python 3.x.x

---

## STEP 3: Set Up Your Project Folder

### On Mac/Linux:
```bash
# Create a folder
mkdir ai-personal-assistant
cd ai-personal-assistant

# Create a Python environment (keeps things clean)
python3 -m venv venv
source venv/bin/activate
```

### On Windows (Command Prompt):
```bash
mkdir ai-personal-assistant
cd ai-personal-assistant

python -m venv venv
venv\Scripts\activate
```

**You should see `(venv)` at the start of your terminal line** - that means it worked!

---

## STEP 4: Install Dependencies

1. Copy the code I provided into a file called `ai_pa_system.py` in your project folder
2. In terminal (make sure you're in the project folder), run:

```bash
pip install -r requirements.txt
```

Wait for it to finish (shows lots of text, that's normal).

---

## STEP 5: Set Your Claude API Key

The system needs to know your API key. Create a file called `.env` in your project folder with:

```
ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
```

Replace `sk-ant-YOUR_KEY_HERE` with the actual key you got in Step 1.

---

## STEP 6: Run It!

In your terminal (in the project folder), type:

```bash
streamlit run ai_pa_system.py
```

**What happens:**
- Your browser opens automatically to `http://localhost:8501`
- You see the AI PA dashboard
- Everything is working! 🎉

**If it doesn't open automatically**: Go to `http://localhost:8501` in your browser

---

## STEP 7: Start Using It

### Dashboard (`📊 Dashboard`)
- See all your tasks, urgent deadlines, study progress
- **Generate Your Daily Briefing**: Tells you exactly what to focus on today based on:
  - Your energy levels (high morning/evening)
  - Urgent tasks coming up
  - Your weak subjects
  - Your study history
  - Your work schedule

### Add Task (`➕ Add Task`)
- Add work tasks: "Create content for Corporate Governance class"
- Add Bar prep tasks: "Study Constitutional Law essays"
- Set due dates and priority
- The AI will remind you of urgent ones

### Log Study Session (`📚 Log Study Session`)
- After each study block, log what you studied
- Rate your clarity (1-5)
- Add notes on what you learned
- **The AI tracks this and identifies weak areas**

### Log Mock Score (`🎯 Log Mock Score`)
- Log practice test scores (essays, MBE sections, full exams)
- Add notes on how you felt
- Track your progress over time

### Progress Analytics (`📈 Progress Analytics`)
- See your total study hours
- Identify weak subjects (automatically prioritized)
- Track mock score trends
- Visualize your improvement

### AI Recommendations (`💡 AI Recommendations`)
- Click to get personalized advice from Claude on:
  - What to focus on next
  - How to improve weak areas
  - Better time management
  - Work-life balance strategies

---

## YOUR DAILY WORKFLOW

### Morning (8-10am) - High Energy ⚡
1. **Start here**: Open Dashboard
2. **Click**: "Generate Today's Brief"
3. **Review**: What the AI recommends
4. **Log**: Any study from yesterday
5. **Action**: Work on the AI's top priority

### Mid-Day (11:30am-3/4pm) - Work Hours
1. Use "Add Task" to organize content creation for classes
2. The AI reminds you of what's due
3. Focus on work tasks

### Evening (6pm-9:30pm) - High Energy ⚡
1. Log your Bar prep study session
2. If you took a mock: Log the score
3. Get tomorrow's briefing by asking the AI

### Key Habits:
- **Every study session**: Log it (subject, hours, clarity)
- **Every mock/practice test**: Log the score
- **Every morning**: Check your daily briefing
- **Every week**: Review progress analytics to see weak areas

---

## CUSTOMIZING FOR YOUR COURSES

### Your Teaching Subjects at LawSikho:
The system recognizes these categories:
- Work - Content
- Work - Class Management  
- Work - Reporting
- Bar Prep - Essay
- Bar Prep - MBE
- Bar Prep - PT

**When you add a task**, just pick the right category!

### Bar Subjects Tracked:
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

(These are from your LawSikho course)

---

## TROUBLESHOOTING

### "ModuleNotFoundError: No module named 'streamlit'"
**Solution**: Make sure your virtual environment is activated
- Mac/Linux: `source venv/bin/activate`
- Windows: `venv\Scripts\activate`

Then run: `pip install -r requirements.txt`

### "ANTHROPIC_API_KEY not found"
**Solution**: 
1. Create a file called `.env` in your project folder
2. Add: `ANTHROPIC_API_KEY=sk-ant-YOUR_KEY`
3. Save and restart the app

### "Port 8501 is already in use"
**Solution**: Close any other Streamlit apps, or run:
```bash
streamlit run ai_pa_system.py --server.port 8502
```

### "Command not found: streamlit"
**Solution**: 
1. Make sure you're in the project folder
2. Activate venv: `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows)
3. Try again

---

## NEXT STEPS

### Week 1: Get Comfortable
- Add all your current tasks
- Log a few study sessions
- Check the daily briefing

### Week 2-4: Establish Routine
- Daily briefing every morning
- Log every study session
- Log mock scores
- Let the AI learn your patterns

### Week 5+: Optimization
- Use weak areas identified by AI
- Adjust study focus based on recommendations
- Track your improvement in mock scores

---

## ADVANCED: How to Modify It Later

Once you're comfortable, you can customize:

1. **Change Bar subjects**: Edit line 78-89 in `ai_pa_system.py`
2. **Change task categories**: Edit line 75-76 in `ai_pa_system.py`
3. **Add new features**: Add new functions in the same file
4. **Change the AI prompt**: Find "generate_daily_briefing" function and modify the prompt

**Pro tip**: Ask me questions! I can help you customize it.

---

## Your AI PA is Fully Functional! 🚀

You now have:
✅ Task management (work + Bar prep)
✅ Study progress tracking
✅ Mock score logging
✅ Weak area identification
✅ Personalized daily briefings (powered by Claude)
✅ Progress analytics
✅ AI recommendations

**This is a REAL system** that will help you:
- Never forget tasks
- Track your progress
- Identify weak areas
- Get daily guidance
- Balance work + Bar prep
- Stay motivated

---

## Quick Command Reference

### To start the app:
```bash
streamlit run ai_pa_system.py
```

### To stop it:
Press `Ctrl+C` in terminal

### To restart:
```bash
streamlit run ai_pa_system.py
```

### To open in browser:
Go to `http://localhost:8501`

---

## SUPPORT

If anything breaks or you want to add features:
1. Tell me what's wrong
2. I'll fix the code
3. You update your file
4. Done!

You've got this! 💪

---

**Last Updated**: November 2025
**System**: AI Personal Assistant v1.0
**Status**: Ready to use! 🎉
