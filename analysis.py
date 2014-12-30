#grep -r teams: /Users/purav.aggarwal/Documents/Purav/ResearchMe/CricketAnalytics/odis/data/* -2 | grep India | awk -F'-' '{print $1}' | awk -F'/' '{print $NF}'
import yaml
import os
import subprocess
import sys

teamNames = []
teamNames.append("India")
teamNames.append("Pakistan")
teamNames.append("South Africa")
teamNames.append("Australia")
teamNames.append("England")
teamNames.append("New Zealand")
teamNames.append("Sri Lanka")
teamNames.append("West Indies")

num2alpha = {}
num2alpha[1] = "st"
num2alpha[2] = "nd"
num2alpha[3] = "rd"
num2alpha[4] = "th"

if(len(sys.argv) == 1):
    print "Arguments required - specify if the processing is for odis to tests"
    sys.exit()
else:
    if(sys.argv[1] == "tests"):
        bowlingStats = open("/Users/purav.aggarwal/Documents/Purav/ResearchMe/CricketAnalytics/tests/BowlingStats",'w')
        stats = open("/Users/purav.aggarwal/Documents/Purav/ResearchMe/CricketAnalytics/tests/TeamStats",'w')
        stats.write("teamName,totalBowlingChangeWicketsTakenByTeam,totalWicketsTakenByTeam,first,second,third,fourth,fifth,sixth,totalOversBowledByTeam"+"\n")
        bowlingStats.write("teamName,BowlerName,first,second,third,fourth,fifth,sixth,totalBallingChangeWickets,totalWicketsTakenByBowler,totalBowlingChangeWicketsTakenByTeam,totalWicketsTakenByTeam,totalOversBowledByBowler,totalOversBowledByTeam"+"\n")
        folderPath = "/Users/purav.aggarwal/Documents/Purav/ResearchMe/CricketAnalytics/tests/data/"
        lastAnalysisOver = 450
    elif(sys.argv[1] == "odis"):
        bowlingStats = open("/Users/purav.aggarwal/Documents/Purav/ResearchMe/CricketAnalytics/odis/BowlingStats",'w')
        stats = open("/Users/purav.aggarwal/Documents/Purav/ResearchMe/CricketAnalytics/odis/TeamStats",'w')
        stats.write("teamName,totalBowlingChangeWicketsTakenByTeam,totalWicketsTakenByTeam,first,second,third,fourth,fifth,sixth,totalOversBowledByTeam"+"\n")
        bowlingStats.write("teamName,BowlerName,first,second,third,fourth,fifth,sixth,totalBallingChangeWickets,totalWicketsTakenByBowler,totalBowlingChangeWicketsTakenByTeam,totalWicketsTakenByTeam,totalOversBowledByBowler,totalOversBowledByTeam"+"\n")
        folderPath = "/Users/purav.aggarwal/Documents/Purav/ResearchMe/CricketAnalytics/odis/data/"
        lastAnalysisOver = 50
    else:
        print "Allowed arguments : odis or tests"
        sys.exit()

def initGlobalBowler(bowler) :
    totalBowlingChangeWicketsTakenByBowler[bowler] = {}
    for i in range(6):
        totalBowlingChangeWicketsTakenByBowler[bowler][i+1] = 0
    totalBowlingChangeWicketsTakenByBowler[bowler][7] = 0 # Total Bowling Change Wickets Taken by the team with the Bowler

for row in teamNames:
    teamName = row
    command = "grep -r teams: %s -2 | grep \"%s\" | awk -F'-' '{print $1}' | awk -F'/' '{print $NF}'"%(folderPath,teamName)
    print command
    output = subprocess.check_output(command, shell=True)
    output = output.split("\n")

    # Team Global Stats
    totalWicketsTakenByTeam = 0
    totalBowlingChangeWicketsTakenByTeam = 0
    totalTeamBallNumberCountBowlingChangeWickets = {}
    totalOversBowledByTeam = 0

    # Bowler Global Stats
    totalBowlingChangeWicketsTakenByBowler = {}
    totalWicketsTakenByBowler = {}
    totalOversBowledByBowler = {}

    for matchIndex in range(len(output)-1):
        stream = open(folderPath+output[matchIndex],'r')
        data = yaml.load(stream)
        info = data.get('info')
        innings = data.get('innings')
        team1 = info.get('teams')[0]
        team2 = info.get('teams')[1]
        matchType = info.get('match_type')

        #Settings variables for ODI and TEST matches seperately:
        if(matchType == "Test"):
            maxOversAllowedPerBowler = 180
        elif(matchType == "ODI"):
            maxOversAllowedPerBowler = 10
        else:
            maxOversAllowedPerBowler = 10

        if(not(team1 in teamNames and team2 in teamNames)):
            continue # We want to analyse matches between competetive teams only        
  
        bowlingQuota = {}

        for inningsItr in range(len(innings)):
            requiredInnings = innings[inningsItr].get(str(inningsItr+1)+num2alpha[inningsItr+1]+" innings")
            if(requiredInnings.get('team') == teamName):                    #Implies the required team is batting - we want it to be balling
                continue
            else:
                requiredInnings = innings[inningsItr].get(str(inningsItr+1)+num2alpha[inningsItr+1]+" innings")

            deliveries = requiredInnings.get('deliveries')
            OVER_LENGTH = 6

            currentBowlerA = deliveries[0].get(0/6+0.1).get('bowler')
            currentBowlerB = currentBowlerA
            previousBowler = currentBowlerA

            localWicketsTakenByTeam = 0
            localBowlingChangeWicketsTakenByTeam = 0
            localOversBowledByTeam = 0
            localWicketsTakenByBowler = {}
            localOversBowledByBowler = {}


            itsABallingChangeOver = False
            targetBowlingChangeNumberOfBalls = 6
            overNumber = 0
            ballKey = overNumber + 1.0/10
            firstBall = True
            numOfAccountableBalls = 0
            ballIterator = 1.0/10
            ballsThrownInCurrentOver = 1.0
            rounder = 1

            for i in range(0,len(deliveries)):
                round(ballsThrownInCurrentOver,1)
                ballsThrownInCurrentOver += 1.0
                if(ballsThrownInCurrentOver >= 10.0):
                    rounder = 2

                #print  ":::"+str(i) + ":" + str(ballKey) + ":" + ":" + str(ballsThrownInCurrentOver) + ":" + str(numOfAccountableBalls) + ":" + str(deliveries[i]) + ":" + str(deliveries[i].get(ballKey))
                #1 Check if it's an accountable delivery
                ballKey = round(ballKey,rounder)
                ballFirstKey = deliveries[i].keys()[0]
                
                if(str(ballKey).split('.')[0] != str(ballFirstKey).split('.')[0]):
                    print "An anomalous Over:"
                    print "Details:"
                    print "Team:"+teamName + ":Match:" + str(output[matchIndex]) + ":ExpectedBall:"+str(ballKey) + ":FoundBall:" + str(ballFirstKey) +":"+str(ballsThrownInCurrentOver) + ":" + str(numOfAccountableBalls) + ":" + str(deliveries[i]) + ":" + str(deliveries[i].get(ballKey))
                    if(int(str(ballKey).split('.')[0]) < int(str(ballFirstKey).split('.')[0])):
                        print "Short Ball Over"
                        ballKey = float(ballFirstKey)
                        #It's an anomlous over change - we would have to reset variables
                        rounder = 1
                        numOfAccountableBalls = 0
                        ballIterator = 1.0/10
                        ballsThrownInCurrentOver = 1.0
                        ballsThrownInCurrentOver += 1.0
                        overNumber += 1
                        firstBall = True
                        print "Newly assigned BallKey:"+str(ballKey)

                    else:
                        print "Extra Ball Over"
                        # It's an anomalous extension of the over - the easiest way out is to move to the next delivery
                        ballsThrownInCurrentOver = 1.0
                        continue


                if(not(deliveries[i].get(ballKey).get('extras')) or deliveries[i].get(ballKey).get('extras').get('legbyes') or deliveries[i].get(ballKey).get('extras').get('byes') or deliveries[i].get(ballKey).get('extras').get('penalty')):
                    numOfAccountableBalls += 1
                    if(firstBall):
                        firstBall = False
                        bowler = deliveries[i].get(ballKey).get('bowler')
                        if(currentBowlerB != bowler and currentBowlerA == currentBowlerB): #Only for the second over which we do not otherwise know where it starts.
                            currentBowlerB = bowler
                            itsABallingChangeOver = True
                        elif(currentBowlerA == bowler or currentBowlerB == bowler):
                            itsABallingChangeOver = False
                        elif(currentBowlerA != bowler):
                            previousBowler = currentBowlerA
                            currentBowlerA = currentBowlerB
                            currentBowlerB = bowler
                            itsABallingChangeOver = True
                        elif(currentBowlerB != bowler):
                            previousBowler = currentBowlerB
                            currentBowlerB = bowler
                            itsABallingChangeOver = True
                        else:
                            itsABallingChangeOver = False
    
                        if(i == 0): #Hack for the first over
                            itsABallingChangeOver = True
    
    
                        if(bowlingQuota.has_key(previousBowler) and (bowlingQuota[previousBowler] == maxOversAllowedPerBowler)):
                            itsABallingChangeOver = False
    
                    #0. Check if it's a wicket ball
                    itsAWicketBall = False
                    if(deliveries[i].get(ballKey).get('wicket')):
                        localWicketsTakenByTeam += 1
                        itsAWicketBall = True
                        wicketKind = deliveries[i].get(ballKey).get('wicket').get('kind')
                        if(wicketKind != 'obstructing the field' and wicketKind != 'retired hurt' and wicketKind != 'run out'):
                            if(localWicketsTakenByBowler.has_key(bowler)):
                                localWicketsTakenByBowler[bowler] += 1
                            else:
                                localWicketsTakenByBowler[bowler] = 1
                            if(itsABallingChangeOver and (numOfAccountableBalls <= targetBowlingChangeNumberOfBalls) and (overNumber <= lastAnalysisOver)):
                                if(not(totalBowlingChangeWicketsTakenByBowler.has_key(bowler))):
                                    initGlobalBowler(bowler)
                                totalBowlingChangeWicketsTakenByBowler[bowler][numOfAccountableBalls] += 1

                    if(itsABallingChangeOver and itsAWicketBall and (numOfAccountableBalls <= targetBowlingChangeNumberOfBalls) and (overNumber <= lastAnalysisOver)):
                        localBowlingChangeWicketsTakenByTeam += 1
                        if(totalTeamBallNumberCountBowlingChangeWickets.has_key(numOfAccountableBalls)):
                            totalTeamBallNumberCountBowlingChangeWickets[numOfAccountableBalls] += 1
                        else:
                            totalTeamBallNumberCountBowlingChangeWickets[numOfAccountableBalls] = 1
   
                    # Over finish - Last ball just happened.
                    if(numOfAccountableBalls == 6):
                        if(bowlingQuota.has_key(bowler)):
                            if(bowlingQuota[bowler] == maxOversAllowedPerBowler):
                                print "ERROR: More than maxOversAllowedPerBowler over bowled:"+str(bowler)+":"+str(teamName)+":"
                            else:
                                bowlingQuota[bowler] += 1
                        else:
                            bowlingQuota[bowler] = 1
                        rounder = 1
                        numOfAccountableBalls = 0
                        ballIterator = 1.0/10
                        ballsThrownInCurrentOver = 1.0
                        overNumber += 1
                        ballKey = overNumber + ballIterator
                        firstBall = True
                    else:
                        ballKey = overNumber + ballsThrownInCurrentOver/pow(10,rounder)
                else: #Extras - unaccountable ball
                    ballKey = overNumber + ballsThrownInCurrentOver/pow(10,rounder)

            for bowlerName in bowlingQuota.keys():
                if(localOversBowledByBowler.has_key(bowlerName)):
                    localOversBowledByBowler[bowlerName] += bowlingQuota[bowlerName]
                else:
                    localOversBowledByBowler[bowlerName] = bowlingQuota[bowlerName]

            totalOversBowledByTeam += overNumber
            localOversBowledByTeam = overNumber

            #Innings Over - Update the Global DataStructures now
            totalBowlingChangeWicketsTakenByTeam += localBowlingChangeWicketsTakenByTeam
            totalWicketsTakenByTeam += localWicketsTakenByTeam
            for k,v in localWicketsTakenByBowler.items():
                if(totalBowlingChangeWicketsTakenByBowler.has_key(k)):
                    totalBowlingChangeWicketsTakenByBowler[k][7] += localBowlingChangeWicketsTakenByTeam
                if(totalWicketsTakenByBowler.has_key(k)):
                    totalWicketsTakenByBowler[k][0] += v
                    totalWicketsTakenByBowler[k][1] += localWicketsTakenByTeam
                else:
                    totalWicketsTakenByBowler[k] = {}
                    totalWicketsTakenByBowler[k][0] = v
                    totalWicketsTakenByBowler[k][1] = localWicketsTakenByTeam

            for k,v in localOversBowledByBowler.items():
                if(totalOversBowledByBowler.has_key(k)):
                    totalOversBowledByBowler[k][0] += v
                    totalOversBowledByBowler[k][1] += localOversBowledByTeam
                else:
                    totalOversBowledByBowler[k] = {}
                    totalOversBowledByBowler[k][0] = v
                    totalOversBowledByBowler[k][1] = localOversBowledByTeam


    stats.write(str(teamName)+","+str(totalBowlingChangeWicketsTakenByTeam)+","+str(totalWicketsTakenByTeam)+","+str(totalTeamBallNumberCountBowlingChangeWickets[1])+","+str(totalTeamBallNumberCountBowlingChangeWickets[2])+","+str(totalTeamBallNumberCountBowlingChangeWickets[3])+","+str(totalTeamBallNumberCountBowlingChangeWickets[4])+","+str(totalTeamBallNumberCountBowlingChangeWickets[5])+","+str(totalTeamBallNumberCountBowlingChangeWickets[6])+","+str(totalOversBowledByTeam)+str("\n"))
    print(str(teamName)+","+str(totalBowlingChangeWicketsTakenByTeam)+","+str(totalWicketsTakenByTeam)+","+str(totalTeamBallNumberCountBowlingChangeWickets[1])+","+str(totalTeamBallNumberCountBowlingChangeWickets[2])+","+str(totalTeamBallNumberCountBowlingChangeWickets[3])+","+str(totalTeamBallNumberCountBowlingChangeWickets[4])+","+str(totalTeamBallNumberCountBowlingChangeWickets[5])+","+str(totalTeamBallNumberCountBowlingChangeWickets[6])+","+str(totalOversBowledByTeam)+str("\n"))
    for key, val in totalBowlingChangeWicketsTakenByBowler.items():
        bowlingStats.write(str(teamName)+","+str(key)+","+str(val[1])+","+str(val[2])+","+str(val[3])+","+str(val[4])+","+str(val[5])+","+str(val[6])+"," + str(val[1]+val[2]+val[3]+val[4]+val[5]+val[6])+","+str(totalWicketsTakenByBowler[key][0])+","+str(val[7])+","+str(totalWicketsTakenByBowler[key][1])+","+str(totalOversBowledByBowler[key][0])+","+str(totalOversBowledByBowler[key][1])+"\n")

        #print "localBowlingChangeWicketsTakenByTeam: " + str(totalBowlingChangeWicketsTakenByTeam)
        #print "localWicketsTakenByTeam: " + str(totalWicketsTakenByTeam)

        #Print Bowling Stats here



stats.close()
bowlingStats.close()
'''
Interesting:

    Seems an extra ball was bowled here : 597926.yaml - observe over 1.1 - india bowling
    Seems a 5 ball over was bowled here : 392619.yaml - 4.5 - Australia bowling
    Seems a 7 ball over - 352667.yaml - WestIndies batting England Balling - 1st over
    Extra ball over - Australia England - 36th over England Balling
    5 Ball Over - 567360.yaml - - South Africa        - New Zealand 48th over SA
    7 ball over - 385749.yaml - Pak Lanka - 28th over Pak batting
    5 ball over - 518960.yaml India Lanka - lanka bowling - 29th over
    5 ball over - 2011-10-15  531984.yaml Bangladesh WI - 14th over
'''
