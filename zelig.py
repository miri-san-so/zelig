import speech_recognition as sr
import os
import pyttsx3
import engineio

# Initializing Programs Voice
engineio = pyttsx3.init()
voices = engineio.getProperty('voices')
engineio.setProperty('rate', 120)
engineio.setProperty('voice', voices[1].id)

def isValidCreateTask(user_input):

    strin = user_input
    strin = list(strin.split(' '))
    approved_words = []

    for i in strin:
        if i == "create":
            approved_words.append(i)
        elif i == "task":
            approved_words.append(i)
        elif i == "add":
            approved_words.append(i)
        elif i == "stop":
            approved_words.append(i)
        else:
            continue

    flag = 0
    stop = False
    for i in approved_words:
        if i == "create" or "add" or "task":
            flag += 1
        if i == "stop":
            stop = True

    if stop == True:
        return "stop"
    elif flag >= 2:
        return True
    else:
        return False

def isValidShowTask(user_input):
    strin = user_input.lower()
    print(strin)
    strin = list(strin.split(' '))
    approved_words = []

    for i in strin:
        if i == "show":
            approved_words.append(i)
        elif i == "task":
            approved_words.append(i)
        elif i == "read":
            approved_words.append(i)
        elif i == "view":
            approved_words.append(i)
        elif i == "display":
            approved_words.append(i)
        elif i == "stop":
            approved_words.append(i)
        else:
            continue

    flag = 0
    stop = False

    for i in approved_words:
        if i == "show" or "display" or "task" or "view" or "read":
            flag += 1
        if i == "stop":
            stop = True

    if stop == True:
        return "stop"
    elif flag >= 2:
        return True
    else:
        return False

def isValidClearTask(user_input):
    strin = user_input
    strin = list(strin.split(' '))
    approved_words = []

    for i in strin:
        if i == "clear":
            approved_words.append(i)
        elif i == "delete":
            approved_words.append(i)
        elif i == "all":
            approved_words.append(i)
        elif i == "remove":
            approved_words.append(i)
        elif i == "stop":
            approved_words.append(i)
        else:
            continue
        
    flag = 0
    stop = False

    for i in approved_words:
        if i == "clear" or "delete" or "all" or "remove":
            flag += 1
        if i == "stop":
            stop = True

    if stop == True:
        return "stop"
    elif flag >= 2:
        return True
    else:
        return False

def isValidYesOrNo(user_input):
    strin = user_input
    strin = list(strin.split(' '))
    approved_words = []

    for i in strin:
        if i == "yes":
            approved_words.append(i)
        elif i == "yup":
            approved_words.append(i)
        elif i == "yeah":
            approved_words.append(i)
        elif i == "sure":
            approved_words.append(i)
        elif i == "no":
            approved_words.append(i)
        elif i == "don't":
            approved_words.append(i)
        elif i == "do not":
            approved_words.append(i)
        elif i == "stop":
            approved_words.append(i)
        else:
            continue

    flag_yes = 0
    flag_no = 0
    stop = False
    for i in approved_words:
        if i == "yes" or "yeah" or "yup" or "sure":
            flag_yes += 1
        if i == "no" or "don't" or "do not":
            flag_no += 1
        if i == "stop":
            stop = True

    if flag_yes != 0:
        return "yes"
    if flag_no != 0:
        return "no"
    if stop == True:
        return "stop"

def speak(text):
    engineio.say(text)
    engineio.runAndWait()

def jarvisInput():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source, timeout=5)
        r.adjust_for_ambient_noise(source)

    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        words = r.recognize_google(audio)
        words.lower()
        print("Google Speech Recognition thinks you said \n>>> " +
              r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return "re-enter"
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(e))
    except ConnectionAbortedError:
        speak("no internet connection can be found!")
    finally:
        return r.recognize_google(audio)

def clearTask():
    with open('tasks.txt', 'w') as f:
        f.write("")

def commitTask(task):
    # Giving confirmation on adding it
    speak('adding the task')

    # Appending to file "tasks.txt"
    with open('tasks.txt', 'a') as f:
        f.write("{}\n".format(task))

def initializeTaskBot():
    speak('Do you wanna listen to task or add a new task?')
    while (True):
        words = jarvisInput()
        words = words.lower()
        
        if words == "re-enter":
            words = jarvisInput()
            words = words.lower()
        if isValidClearTask(words) == True:
            speak('clearing tasks')
            clearTask()
            
        if isValidShowTask(words) == True:
            print('in is valid show task')
            with open("tasks.txt") as f:
                content = f.readlines()
            content = [x.strip() for x in content]
            count = 0
            for i in content:
                count += 1
                print(i, count)
                if count <= len(content):
                    speak(i)

        if isValidCreateTask(words) == True:
            # Ask for the task
            speak('what is the task')

            # Save Task is variable
            task = jarvisInput()

            # Repeat the task back to user
            # and ask if they wanna re-enter or commit
            speak('the task is '+task+" should i add it?")
            ack = jarvisInput()

            # Check if user said "yes"
            if isValidYesOrNo(ack) == "yes":
                commitTask(task)

            # Check if user said "stop"
            if isValidYesOrNo(ack) == "stop":
                speak("byeee!!")
                break

            # Check if user said "no"
            if isValidYesOrNo(ack) == "no":

                # Ask if user wanna re-enter the task
                speak('do you want to re-enter?')
                ack = jarvisInput()

                # Ask for users new task
                if isValidYesOrNo(ack) == "yes":
                    speak('please say your task again')
                    task = jarvisInput()
                    commitTask(task)

            if isValidYesOrNo(ack) == None:
                speak('i did not get that')

        if isValidCreateTask(words) == "stop":
            speak("byeeeeeeee!!")
            break

initializeTaskBot()