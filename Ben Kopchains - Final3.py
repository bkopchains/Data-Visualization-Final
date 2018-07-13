# Ben Kopchains - Final Project Pt. 3

# I affirm that I have carried out the attached academic endeavors with full academic honesty,
# in accordance with the Union College Honor Code and the course syllabus.

import praw         # praw is reddit's custom web-scraping library
import datetime
import matplotlib.pyplot as plt

# might have to change this string to something else if you get
# an error from reddit
user_agent = "kopchaib 0.5"

r = praw.Reddit(user_agent = user_agent)

questions = {"who":0,"what":0,"where":0,"when":0,"why":0,"how":0}
scores = {"who":0,"what":0,"where":0,"when":0,"why":0,"how":0}
punctuation = {".":0,",":0,":":0,";":0,"?":0,"!":0,"(":0,")":0}
time_x_score = {}
time_x_numposts = {}

# ------------------------------------------

# gathers data from the top X posts (X = samplesize)
# of a specified subreddit, and uses the functions below
# to graph the relevant data
def top_all(subname, samplesize):
    print "\n---- Subreddit: " + subname + " -----------------"


    questions = {"who":0,"what":0,"where":0,"when":0,"why":0,"how":0}
    scores = {"who":0,"what":0,"where":0,"when":0,"why":0,"how":0}
    punctuation = {".":0,",":0,":":0,";":0,"?":0,"!":0,"(":0,")":0}
    time_x_score = {}


    subreddit = r.get_subreddit(subname)

    for submission in subreddit.get_top_from_all(limit = samplesize):

        time = submission.created
        time = datetime.datetime.fromtimestamp(time).time().strftime('%H')
        score = submission.score
        if int(time) in time_x_numposts:
            time_x_numposts[int(time)] += 1
        else:
            time_x_numposts[int(time)] = 1
        time_x_score[int(time)] = int(score)


        for x in submission.title.split(" "):
            if x.lower() in questions:
                questions[x.lower()] += 1
                scores[x.lower()] += score
            for char in x:
                if char in punctuation:
                    punctuation[char] += 1

    for i in questions:
        if questions[i] > 0:
            scores[i] /= questions[i]

    for i in time_x_score:
        if time_x_numposts[i] > 0:
            time_x_score[i] /= time_x_numposts[i]

    print "\n---- Top/All -----------------"
    time_x_numposts_plot(time_x_numposts, subname)
    time_x_score_plot(time_x_score, subname)
    score_vs_num_plot(time_x_score, time_x_numposts, subname)

    if "ask" in subname.lower():            # only returns question-based plots on "ask" subreddits
        qtype_x_score_plot(scores, subname)
        qtype_x_numq_plot(questions, subname)
        qscore_vs_qnum_plot(scores, questions, subname)

# plots a graph comparing the two time-related sets of data
# on a shared axis. This compares average score per hour and
# total posts per hour on a select subreddit
def score_vs_num_plot(scoredata, numdata, subreddit):
    f, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=False)
    x1 = [x[0] for x in scoredata.items()]
    y1 = [y[1] for y in scoredata.items()]
    ax1.bar(x1,y1,linewidth = 0, color = "slateblue")
    ax1.set_ylabel("Average Post Score")
    x2 = [x[0] for x in numdata.items()]
    y2 = [y[1] for y in numdata.items()]
    ax2.bar(x2,y2,linewidth = 0, color = "orange")
    ax2.set_ylabel("Number of Posts")
    f.subplots_adjust(hspace=0)
    plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
    plt.xlabel("Time of Day (24h)")
    ax1.set_title("Average Post Score per Hour posted vs. Number of Posts per Hour\nin the '" +subreddit+"' Subreddit")
    plt.show()

# plots a bar graph depicting the average post score based
# on the hour of the day they were posted
def time_x_score_plot(data, subreddit):
    f, ax = plt.subplots()
    x = [x[0] for x in data.items()]
    y = [y[1] for y in data.items()]
    ax.bar(x,y,linewidth = 0, color = "slateblue")
    ax.set_xlabel("Time of Day (24h)")
    ax.set_ylabel("Average Post Score")
    ax.set_title("Average Post Score by Time in the '" +subreddit+"' Subreddit")
    plt.show()

# plots a bar graph depicting the number of submissions (out of
# the top X posts) posted each hour of the day
def time_x_numposts_plot(data, subreddit):
    f, ax = plt.subplots()
    data = data.items()
    x = [x[0] for x in data]
    y = [y[1] for y in data]
    ax.bar(x,y,linewidth = 0, color = "orange")
    ax.set_xlabel("Time of Day (24h)")
    ax.set_ylabel("Number of Posts")
    ax.set_title("Posts per Hour in the '" +subreddit+"' Subreddit")
    plt.show()


# plots a graph comparing the two question-related sets of
# data on a shared axis. This set compares average score per
# question type with the number of posts from each question
# type on a select "ask___" subreddit
def qscore_vs_qnum_plot(scoredata, numdata, subreddit):
    f, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=False)
    x1 = [x for x in range(len(scoredata))]
    y1 = [y[1] for y in scoredata.items()]
    ax1.bar(x1,y1,linewidth = 0, color = "sage", align = "center")
    ax1.set_ylabel("Average Post Score")
    x2 = [x for x in range(len(numdata))]
    y2 = [y[1] for y in numdata.items()]
    ax2.bar(x2,y2,linewidth = 0, color = "tomato", align = "center")
    ax2.set_ylabel("Questions Asked")
    f.subplots_adjust(hspace=0)
    plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
    plt.xlabel("Question Type")
    ax1.set_title("Questions Asked vs. Average Score per Question Type\nin the '" +subreddit+"' Subreddit")
    plt.xticks(range(len(scoredata)), [x for x in scoredata])
    plt.show()

# plots a bar graph showing the average score recieved by each
# type of question on an "ask___" subreddit
def qtype_x_score_plot(data, subreddit):
    f, ax = plt.subplots()
    data = data.items()
    x = [x for x in range(len(data))]
    y = [y[1] for y in data]
    ax.bar(x,y,linewidth = 0, color = "sage", align = "center")
    ax.set_xlabel("Question Type")
    ax.set_ylabel("Average Post Score")
    ax.set_title("Average Post Score by Question Type in the '" +subreddit+"' Subreddit")
    plt.xticks(range(len(data)), [x[0] for x in data])
    plt.show()

# plots a bar graph showing the number of submissions (out of
# the top X posts) from each question type on an "ask___" subreddit
def qtype_x_numq_plot(data, subreddit):
    f, ax = plt.subplots()
    data = data.items()
    x = [x for x in range(len(data))]
    y = [y[1] for y in data]
    ax.bar(x,y,linewidth = 0, color = "tomato", align = "center")
    ax.set_xlabel("Question Type")
    ax.set_ylabel("Questions Asked")
    ax.set_title("Number of Posts by Question Type in the '" +subreddit+"' Subreddit")
    plt.xticks(range(len(data)), [x[0] for x in data])
    plt.show()

# ------------------------------------------
print "Subreddit Examples: Funny, AskReddit, Pics, DataIsBeautiful, "
input = raw_input("\nPlease enter a subreddit to explore: ")
ss = raw_input("\nPlease enter a sample size (Recommended 500): ")
print "~~~Please Wait~~~"
top_all(input, ss)