import streamlit as st
import quiz
import dashboard

st.set_page_config(page_title="Sustainability Quiz App", layout="centered")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Home", "Take Quiz", "Dashboard"])

if page == "Home":
    st.title("🌿 Welcome to the Sustainability Quiz!")
    st.write("""This app helps you understand your sustainability habits.
Take the quiz to find out your score, and view progress on your dashboard.""")
    if st.button("Start Quiz ▶"):
        st.session_state.page = "Take Quiz"
        st.experimental_rerun()

if page == "Take Quiz":
    try:
        quiz.main()
    except:
        st.error("Error running quiz.")

if page == "Dashboard":
    try:
        dashboard.main()
    except:
        st.error("Error running dashboard.")
import datetime
#----------------------------------------------------------------------------------------------------------------------------------------
#The use of nested dictionary to store - ID : {desc,  points}
action = {
        "water":{"desc":"Avoid keeping taps running unnecessarily.",
                 "points":5},
        "sunlight":{"desc":"Use natural light in the morning instead of turning on the lights.",
                  "points":2.5},
        "bottle":{"desc":"Carry a reusable bottle instead of buying new plastic ones daily.",
                  "points":5},
        "light":{"desc":"Switch off unnecessary lights or fans.",
                 "points":2.5},
        "transport":{"desc":"Walk, carpool or use public transportation instead of driving alone.",
                     "points":7.5},
        "lunch":{"desc":"Pack your own lunch instead of ordering or purchasing packaged food.",
                 "points":7.5},
        "recycle":{"desc":"Recycle plastic bottles, cans or paper regularly.",
                   "points":7.5},
        "stairs":{"desc":"Take the stairs instead of using the elevator.",
           "points":5},
        "print":{"desc":"Minimize printing and instead use digital documents.",
                 "points":5},
        "fashion":{"desc":"Avoid fast fashion and instead buy clothes that last longer.",
                   "points":7.5},
        "meals":{"desc":"Plans meals ahead of time to avoid food waste.",
                "points":7.5},
        "reuse":{"desc":"Carry a reusable shopping bag or tote bag to avoid use of single use bags.",
                  "points":5},
         "thrift":{"desc":"Buy second-hand or recycled products.",
                   "points":5},
        "repair":{"desc":"Repair or donate old clothes and furniture instead of throwing them away.",
                  "points":5},
        "community":{"desc":"Participate in or support environmental or community cleanup events.",
                     "points":5},
        "support":{"desc":"Follow or support environmental organizations or social media pages.",
                   "points":5},
        "encourage":{"desc":"Encourage others to build simple sustainable habits.",
                     "points":5}
        }
#----------------------------------------------------------------------------------------------------------------------------------------
#One session 'data', simply lasts one session or lasts only one app run for TESTING purposes
task_count = {} #no of times task done overall
task = [] #list of tasks(wtv said answered no or sometimes to)
habit = [] #list of habits(wtv answered yes to) + (3 times task completion)
progress = 0 #progress %
last_done = {} #taskkey:lastdone, gets cleared during next day
#----------------------------------------------------------------------------------------------------------------------------------------
#getting a fake today and next day date to allow the whole UI to work according to 'days'
fake_date = datetime.date.today()

def get_today():
    return fake_date

    #using button in app to forward for TESTING
def next_day():
    global fake_date, last_done
    fake_date+=datetime.timedelta(days=1)
    last_done.clear()
    #clearing it for next day refresh of tasks
        
    return fake_date
#----------------------------------------------------------------------------------------------------------------------------------------
def generate_task(answers):
    global task, task_count, habit
#mapping- exact question : ID
    mapping = {
        "Do you avoid keeping taps running unnecessarily?":"water",
        "Do you use natural light in the morning instead of turning on lights?":"sunlight",
        "Do you carry a reusable water bottle instead of buying new plastic ones each day?": "bottle",
        "Do you switch off unnecessary lights or fans before leaving your home?": "light",
        "Do you usually walk, carpool, or use public transport instead of driving alone?": "transport",
        "Do you pack your own lunch instead of buying single-use packaged food?": "lunch",
        "Do you recycle plastic bottles, cans, or paper regularly?": "recycle",
        "Do you take the stairs instead of the elevator when possible?": "stairs",
        "Do you minimize printing and rely on digital documents?": "print",
        "Do you avoid fast fashion and buy clothes that last longer?": "fashion",
        "Do you plan your meals ahead of time to avoid food waste?": "meals",
        "Do you bring your own reusable bags when shopping?": "reuse",
        "Do you make an effort to buy second-hand or recycled products when possible?": "thrift",
        "Do you repair or donate old clothes, electronics, or furniture instead of throwing them away?": "repair",
        "Do you participate in or support any environmental or community cleanup events?": "community",
        "Do you follow or support environmental organizations or social media pages to stay informed?": "support",
        "Do you encourage others to adopt simple sustainable habits?": "encourage"
        }
#clearing prev session
    task.clear()
    task_count.clear()
    last_done.clear() 

#assigning pre fill habits for 'yes' ans
    for question, ans in answers.items():
        if question in mapping and ans=="yes":
            key=mapping[question]
            habit.append(key)

#assigning tasks now
    for question, ans in answers.items():
        if question in mapping and ans in ['no','sometimes']:
            key = mapping[question]
            if key not in task and key not in habit:
                task.append(key)
                task_count[key] = 0

    return task
#------------------------------------------------------------------------------------------------------------------------------------------
def complete_task(key):
#mark done for today, update progress and habits
    global progress, task_count, task, habit, last_done

    today = get_today()

    if key not in action:
        return {"status":"ERROR","message":f"Unkown task '{key}'","progress": progress}

#daily task limit
    if last_done.get(key)==today:
        return {"status":"Already done today.","message":"Please try again next day.","progress":progress}

#mark done for today    
    last_done[key]=today

#total times task done
    task_count.setdefault(key, 0)
    task_count[key] += 1

#adding points to progress
    max_points=sum([v["points"] for v in action.values()])
    progress+=(action[key]["points"])
    progress = min(progress, max_points)

#adding to habit after 3 completion    
    if task_count[key] >= 3:
        if key not in habit:
            habit.append(key)
        if key in task:
            task.remove(key)

        return {"status":"Habit formed","progress":progress}

    return {"status":"Task done","progress":progress}
#------------------------------------------------------------------------------------------------------------------------------------------
def get_progress():
    index= (progress/max_points*100)
    return index

def get_habit():
    return habit
#------------------------------------------------------------------------------------------------------------------------------------------
def reset_task():
    global task_count, habit, task, progress, last_done 
    task_count.clear()
    habit.clear()
    task.clear()
    progress = 0
    last_done.clear()

    return "Reset complete."

#resetting all data js in case, manually.
import streamlit as st
import random
# -----------------------------------------------------------------------------------------------------------------------------------------
# question, points system
question_dict = {
    "Do you avoid keeping taps running unnecessarily?": 5,
    "Do you use natural light in the morning instead of turning on lights?": 2.5,
    "Do you carry a reusable water bottle instead of buying new plastic ones each day?": 5,
    "Do you switch off unnecessary lights or fans before leaving your home?": 2.5,
    "Do you usually walk, carpool, or use public transport instead of driving alone?": 7.5,
    "Do you pack your own lunch instead of buying single-use packaged food?": 7.5,
    "Do you recycle plastic bottles, cans, or paper regularly?": 7.5,
    "Do you take the stairs instead of the elevator when possible?": 5,
    "Do you minimize printing and rely on digital documents?": 5,
    "Do you avoid fast fashion and buy clothes that last longer?": 7.5,
    "Do you plan your meals ahead of time to avoid food waste?": 7.5,
    "Do you bring your own reusable bags when shopping?": 5,
    "Do you make an effort to buy second-hand or recycled products when possible?": 5,
    "Do you repair or donate old clothes, electronics, or furniture instead of throwing them away?": 5,
    "Do you participate in or support any environmental or community cleanup events?": 5,
    "Do you follow or support environmental organizations or social media pages to stay informed?": 5,
    "Do you encourage others to adopt simple sustainable habits?": 5
}
# -----------------------------------------------------------------------------------------------------------------------------------------
st.title("The Sustainability Quiz")
st.write("=" * 50)
st.write("This quiz helps curate your unique sustainability index")
st.write("=" * 50)

st.write("Following are 10 questions")
st.write("Answer each of the following with either - yes / no / sometimes")
st.write("-" * 50)

# maintain quiz state
if "quiz" not in st.session_state:
    st.session_state.quiz=random.sample(list(question_dict.keys()), 10)
if "answers" not in st.session_state:
    st.session_state.answers={}
if "submitted" not in st.session_state:
    st.session_state.submitted=False

quiz=st.session_state.quiz
# -----------------------------------------------------------------------------------------------------------------------------------------
#questions
for i, q in enumerate(quiz, start=1):
    st.write(f"### Question {i}: {q}")
    st.session_state.answers[q]=st.radio(
        f"Select your answer for Question {i}:",
        ["yes", "no", "sometimes"],
        key=f"q_{i}"
    )
# -----------------------------------------------------------------------------------------------------------------------------------------
# submit button
if st.button("Submit Quiz"):
    st.session_state.submitted=True
# -----------------------------------------------------------------------------------------------------------------------------------------
if st.session_state.submitted:
    
    answers=st.session_state.answers
    score=0

    st.success("Quiz submitted!")
    st.write("You can now head to the dashboard to view you progress")
# -----------------------------------------------------------------------------------------------------------------------------------------
# retake button
 if st.button("Retake Quiz"):
     st.session_state.quiz=random.sample(list(question_dict.keys()), 10)
     st.session_state.answers={}
     st.session_state.submitted=False
     st.experimental_rerun()
else:
    st.write("You can now head to the dashboard to view you progress")


def main():
    # Original quiz code executed on import, so call the function if exists
    pass
Import streamlit as st
from logic import generate_task, complete_task, get_progress, get_habit, next_day, get_today, reset_task
#-----------------------------------------------------------------------------------------------------------------
#dashboard
st.title("LifestyleIndex")
st.write(f"**Current Day:** {get_today()}")
#-----------------------------------------------------------------------------------------------------------------
#next day button
if st.button("➡ Next Day"):
    new_day=next_day()
    st.success("New day.")
#-----------------------------------------------------------------------------------------------------------------
if st.button("Reset all Data:"):
    reset_task()
    st.warning("Data reset.")
#-----------------------------------------------------------------------------------------------------------------
#ensures quiz answers exist in session state
if "answers" not in st.session_state:
    st.info("Please complete the quiz to view your tasks :(")
else:
    tasks=generate_task(st.session_state.answers)
#-----------------------------------------------------------------------------------------------------------------
#task list
st.header("Today's Tasks 📝")

if len(tasks)==0:
    st.info("No tasks available for today")
else:
    for t in tasks:
        t=desc
        sti.write(f"->{t})

#completing task
            if st.button(f"Complete task: {t}", key="btn_{t}"):
                  result=complete_task(t) #marks task done
                  st.write(result["status"]) #task done, habit formed, already done
                  st.write(f"Progress: {get_progress(): .2f}%") #progress %
            else:
                pass
#-----------------------------------------------------------------------------------------------------------------
#habit list
st.header("Habits formed:")
habits=get_habit()
if len(habits)==0:
    st.info("No habits formed yet. Complete a task 3 times to get your first habit!")
else:
    for h in habits:
        st.success(f"->{h}")
#-----------------------------------------------------------------------------------------------------------------
#progress bar
st.header("Sustainability Index")
st.progress(get_progress()/100)
st.write(f"Your current sustainability progress is:{get_progress():.2f}%")


def main():
    # Execute dashboard content; assumed code runs on import
    pass
