import mechanicalsoup, threading, os, sys, re, random
from datetime import datetime

browser = mechanicalsoup.StatefulBrowser()
browser.set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

crimeCounter = 0
gtaCounter = 0
utpCounter = 0
fcCounter = 0
ab = False
startRank = ""
isBusy = False
setDefaultTime = True

def doLogin(username, password):
    global startRank
    browser.open("https://nordicmafia.org/")
    browser.select_form('form[method="Post"]')
    browser["username"] = username
    browser["password"] = password
    browser.submit_selected()
    if browser.get_url() == 'https://www.nordicmafia.org/index.php':
        startRank = browser.get_current_page().find('span', class_='value').text.strip()
        print("[", datetime.now().time().strftime('%H:%M:%S').strip(), "] ", "Logget inn som", username)
        isBusy = False
    else:
        sys.exit("Kunne ikke logge inn. Feil brukernavn/passord?")

def checkLogin():
    if browser.get_url() == 'https://www.nordicmafia.org/login.php':
        isBusy = True
        print("[", datetime.now().time().strftime('%H:%M:%S').strip(), "] ", "Bruker ikke logget inn. Logger inn på nytt.")
        doLogin(sys.argv[1], sys.argv[2])


def doAction(url, selForm, optionName, optionValue, sell):
    global isBusy
    browser.open("https://www.nordicmafia.org/index.php?p=" + url)
    checkLogin()
    try:
        if isBusy == False:
            isBusy = True
            global ab
            ab = checkAB()
            if ab == False:
                browser.select_form(selForm)
                browser[optionName] = optionValue
                browser.submit_selected()
                checkSuccess()
                if sell == True:
                    sellCars()
            else:
                sendNotification("pNM", "Antibot")
                pauseAndWaitForInput()
            isBusy = False
            setDefaultTime = True
        else:
            extendTime(url)
    except:
        isBusy = False
        getTimeRemaining(url)

def sendNotification(title, message):
    try:
        os.system('notify-send "{}" "{}"'.format(title, message))
    except:
        print("Antibot")

def pauseAndWaitForInput():
    global setDefaultTime
    try:
        setDefaultTime = False
        input("Trykk enter når du har utført antiboten\n")
        setDefaultTime = True
    except SyntaxError:
        pass
        setDefaultTime = True


def extendTime(url):
    global crimeCounter, gtaCounter, utpCounter, fcCounter
    timeToExtend = random.randint(5,15)
    if url == 'kriminalitet':
        crimeCounter += timeToExtend
    elif url == 'gta':
        gtaCounter += timeToExtend
    elif url == 'blackmail':
        utpCounter += timeToExtend
    elif url == 'fightclub':
        fcCounter += timeToExtend


def checkAB():
    global startRank
    newRank = browser.get_current_page().find('span', class_='value').text.strip()
    if newRank != startRank:
        print("Gratulerer! Du har ranket opp til", newRank)
        startRank = newRank
    abString = browser.get_current_page().find('div', class_='bHeader').text.strip()
    bool = False
    if abString == "Anti-bot":
        bool = True
    return bool

def sellCars():
    try:
        browser.open("https://www.nordicmafia.org/index.php?p=gta")
        form = browser.select_form('form[action="index.php?p=garage"]')
        form.choose_submit('sellAllVehicles')
        browser.submit_selected()
        checkSuccess()
        #putMoneyInBank()
    except:
        print("Fengsel?")

def putMoneyInBank():
    #try:
    browser.open("https://nordicmafia.org/index.php?p=bank")
    form = browser.select_form('form[method="post"]')
    form.choose_submit('depositAll')
    broswer.submit_selected()
    checkSuccess()
    #except:
    print("Kunne ikke putte penger i bank.")

def checkSuccess():
    global setDefaultTime
    try:
        getOutput = browser.get_current_page().find('div', class_='successBox').text.strip().split("\n")
        print("[", datetime.now().time().strftime('%H:%M:%S').strip(), "] ", getOutput[0], "-", getOutput[1])
    except:
        getOutput = browser.get_current_page().find('div', class_='errorBox').text.strip().split("\n")
        print("[", datetime.now().time().strftime('%H:%M:%S').strip(), "] ", getOutput[0], "-", getOutput[1])

    setDefaultTime = True

def getTimeRemaining(url):
    try:
        global crimeCounter, gtaCounter, utpCounter, fcCounter, setDefaultTime
        timeLeft = browser.get_current_page().find('span', id="js_countdown").text.strip().split(" sekunder")
        if url == 'kriminalitet':
            crimeCounter = int(timeLeft[0])
        elif url == 'gta':
            gtaCounter = int(timeLeft[0])
        elif url == 'blackmail':
            utpCounter = int(timeLeft[0])
        elif url == 'fightclub':
            fcCounter = int(timeLeft[0])

        setDefaultTime = False

        print("[", datetime.now().time().strftime('%H:%M:%S').strip(), "] ", browser.get_current_page().find('div', class_="defpadding").text.strip())
    except:
        print("Kunne ikke hente ut tid, setter tilfeldig tid under 20 sekunder.")
        extendTime(url)

def generalCounter():
    threading.Timer(5.0, generalCounter).start()
    global crimeCounter, utpCounter, gtaCounter, fcCounter, setDefaultTime
    randomInt = random.randint(1,20)

    if crimeCounter <= 0:
        doAction('kriminalitet', 'form[method="post"]', 'krimValg', '3', False)
        if setDefaultTime == True:
            crimeCounter = 180 + int(randomInt)
    else:
        crimeCounter = crimeCounter - 5

    if utpCounter <= 0:
        doAction('blackmail', 'form[method="POST"]', 'blackmailPlayer', '1', False)
        if setDefaultTime == True:
            utpCounter = 960 + int(randomInt)
    else:
        utpCounter = utpCounter - 5

    if gtaCounter <= 0:
        doAction('gta', 'form[method="post"]', 'theftsel', '3', True)
        if setDefaultTime == True:
            gtaCounter = 380 + int(randomInt)
    else:
        gtaCounter = gtaCounter - 5

    if fcCounter <= 0:
        doAction('fightclub', 'form[method="POST"]', 'trening', '3', False)
        if setDefaultTime == True:
            fcCounter = 120 + int(randomInt)
    else:
        fcCounter = fcCounter - 5



def main():
    if len(sys.argv) < 2:
        print("Vennligst skriv inn brukernavn og passord. Slik:")
        print("python nmBot.py brukernavn passord")
    else:
        doLogin(sys.argv[1], sys.argv[2])
        generalCounter()

main()
