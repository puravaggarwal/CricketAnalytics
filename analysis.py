#grep -r teams: /Users/purav.aggarwal/Documents/Purav/ResearchMe/CricketAnalytics/odis/data/* -2 | grep India | awk -F'-' '{print $1}' | awk -F'/' '{print $NF}'
import yaml
import os
import subprocess

teamNames = []
teamNames.append("India")
teamNames.append("Pakistan")
teamNames.append("South Africa")
teamNames.append("Australia")
teamNames.append("England")
teamNames.append("New Zealand")
teamNames.append("Sri Lanka")
teamNames.append("West Indies")

teamNameFileName = []
teamNameFileName.append(("India","India"))
teamNameFileName.append(("Pakistan","Pakistan"))
teamNameFileName.append(("South Africa","SouthAfrica"))
teamNameFileName.append(("Australia","Australia"))
teamNameFileName.append(("England","England"))
teamNameFileName.append(("New Zealand","NewZealand"))
teamNameFileName.append(("Sri Lanka","SriLanka"))
teamNameFileName.append(("West Indies","WestIndies"))
bowlingStats = open("/Users/purav.aggarwal/Documents/Purav/ResearchMe/CricketAnalytics/odis/BowlingStats",'w')
stats = open("/Users/purav.aggarwal/Documents/Purav/ResearchMe/CricketAnalytics/odis/TeamStats",'w')
stats.write("teamName,totalBallingChangeWicketsByTeam,totalWicketsTakenByTeam,first,second,third,fourth,fifth,sixth,totalOversBowledByTeam"+"\n")
bowlingStats.write("teamName,BowlerName,first,second,third,fourth,fifth,sixth,totalBallingChangeWickets,totalWicketsTakenByBowler,totalBallingChangeWicketsByTeam,totalWicketsTakenByTeam,totalOversBowledByBowler,totalOversBowledByTeam"+"\n")


def initBowler(bowler) :
    bowlerOverChangeWicketsStats[bowler] = {}
    for i in range(6):
        bowlerOverChangeWicketsStats[bowler][i+1] = 0

for row in teamNameFileName:
    teamName = row[0]
    fileN = row[1]
    fileName = "/Users/purav.aggarwal/Documents/Purav/ResearchMe/CricketAnalytics/odis/"+fileN+"Match"
    folderPath = "/Users/purav.aggarwal/Documents/Purav/ResearchMe/CricketAnalytics/odis/data/"
    command = "grep -r teams: %s -2 | grep \"%s\" | awk -F'-' '{print $1}' | awk -F'/' '{print $NF}'"%(folderPath,teamName)
    print command
    output = subprocess.check_output(command, shell=True)
    output = output.split("\n")

    totalWicketsTakenByTeam = 0
    totalBallingChangeWicketsByTeam = 0
    teamBallNumberCount = {}
    bowlerOverChangeWicketsStats = {}
    totalWicketsTakenByBowler = {}
    totalOversBowledByBowler = {}
    totalOversBowledByTeam = {}

    for matchIndex in range(len(output)-1):
        stream = open("/Users/purav.aggarwal/Documents/Purav/ResearchMe/CricketAnalytics/odis/data/"+output[matchIndex],'r')
        data = yaml.load(stream)
        info = data.get('info')
        innings = data.get('innings')
        team1 = info.get('teams')[0]
        team2 = info.get('teams')[1]

        if(not(team1 in teamNames and team2 in teamNames)):
            continue # We want to analyse matches between competetive teams only        
  
        bowlingQuota = {}

        requiredInnings = innings[0].get('1st innings')
        if(requiredInnings.get('team') == teamName):                    #Implies the required team is batting - we want it to be balling
            if(len(innings) == 2):
                requiredInnings = innings[1].get('2nd innings')
                if(requiredInnings.get('team') == teamName):
                    print "ERROR:"+output[matchIndex]
                    continue
            else:
                continue

        deliveries = requiredInnings.get('deliveries')
        OVER_LENGTH = 6

        currentBowlerA = deliveries[0].get(0/6+0.1).get('bowler')
        currentBowlerB = currentBowlerA
        previousBowler = currentBowlerA

        total_wickets = 0
        bowling_change_wickets = 0
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

            #print  str(match) +":::"+str(i) + ":" + str(ballKey) + ":" + ":" + str(ballsThrownInCurrentOver) + ":" + str(numOfAccountableBalls) + ":" + str(deliveries[i]) + ":" + str(deliveries[i].get(ballKey))
            #1 Check if it's an accountable delivery
            ballKey = round(ballKey,rounder)
            if(not(deliveries[i].get(ballKey).get('extras')) or deliveries[i].get(ballKey).get('extras').get('legbyes') or deliveries[i].get(ballKey).get('extras').get('byes') or deliveries[i].get(ballKey).get('extras').get('penalty')):
                numOfAccountableBalls += 1
                if(firstBall):
                    firstBall = False
                    bowler = deliveries[i].get(ballKey).get('bowler')
                    if(currentBowlerB != bowler and currentBowlerA == currentBowlerB): #Only for the second over which we do not otherwise know where it starts.
                        currentBowlerB = bowler
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

                    if(bowlingQuota.has_key(previousBowler) and (bowlingQuota[previousBowler] == 10)):
                        itsABallingChangeOver = False
    
                #0. Check if it's a wicket ball
                itsAWicketBall = False
                if(deliveries[i].get(ballKey).get('wicket')):
                    total_wickets += 1
                    itsAWicketBall = True
                    wicketKind = deliveries[i].get(ballKey).get('wicket').get('kind')
                    if(wicketKind != 'obstructing the field' and wicketKind != 'retired hurt' and wicketKind != 'run out'):
                        if(totalWicketsTakenByBowler.has_key(bowler)):
                            totalWicketsTakenByBowler[bowler] += 1
                        else:
                            totalWicketsTakenByBowler[bowler] = 1
                        if(itsABallingChangeOver and (numOfAccountableBalls <= targetBowlingChangeNumberOfBalls) and (overNumber <= 45)):
                            if(not(bowlerOverChangeWicketsStats.has_key(bowler))):
                                initBowler(bowler)
                            bowlerOverChangeWicketsStats[bowler][numOfAccountableBalls] += 1

                if(itsABallingChangeOver and itsAWicketBall and (numOfAccountableBalls <= targetBowlingChangeNumberOfBalls) and (overNumber <= 45)):
                    bowling_change_wickets += 1
                    if(teamBallNumberCount.has_key(numOfAccountableBalls)):
                        teamBallNumberCount[numOfAccountableBalls] += 1
                    else:
                        teamBallNumberCount[numOfAccountableBalls] = 1
   
                # Over finish - Last ball just happened.
                if(numOfAccountableBalls == 6):
                    if(bowlingQuota.has_key(bowler)):
                        if(bowlingQuota[bowler] == 10):
                            print "ERROR: More than 10 over bowled:"+str(bowler)+":"+str(teamName)+":"
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
            if(totalOversBowledByBowler.has_key(bowlerName)):
                totalOversBowledByBowler[bowlerName] += bowlingQuota[bowlerName]
            else:
                totalOversBowledByBowler[bowlerName] = bowlingQuota[bowlerName]

        if(totalOversBowledByTeam.has_key(teamName)):
            totalOversBowledByTeam[teamName] += overNumber
        else:
            totalOversBowledByTeam[teamName] = overNumber

        totalBallingChangeWicketsByTeam += bowling_change_wickets
        totalWicketsTakenByTeam += total_wickets

    stats.write(str(teamName)+","+str(totalBallingChangeWicketsByTeam)+","+str(totalWicketsTakenByTeam)+","+str(teamBallNumberCount[1])+","+str(teamBallNumberCount[2])+","+str(teamBallNumberCount[3])+","+str(teamBallNumberCount[4])+","+str(teamBallNumberCount[5])+","+str(teamBallNumberCount[6])+","+str(totalOversBowledByTeam[teamName])+str("\n"))
    print(str(teamName)+","+str(totalBallingChangeWicketsByTeam)+","+str(totalWicketsTakenByTeam)+","+str(teamBallNumberCount[1])+","+str(teamBallNumberCount[2])+","+str(teamBallNumberCount[3])+","+str(teamBallNumberCount[4])+","+str(teamBallNumberCount[5])+","+str(teamBallNumberCount[6])+","+str(totalOversBowledByTeam[teamName])+str("\n"))
    for key, val in bowlerOverChangeWicketsStats.items():
        bowlingStats.write(str(teamName)+","+str(key)+","+str(val[1])+","+str(val[2])+","+str(val[3])+","+str(val[4])+","+str(val[5])+","+str(val[6])+"," + str(val[1]+val[2]+val[3]+val[4]+val[5]+val[6])+","+str(totalWicketsTakenByBowler[key])+","+str(totalBallingChangeWicketsByTeam)+","+str(totalWicketsTakenByTeam)+","+str(totalOversBowledByBowler[key])+","+str(totalOversBowledByTeam[teamName])+"\n")

    #print "bowling_change_wickets: " + str(totalBallingChangeWicketsByTeam)
    #print "total_wickets: " + str(totalWicketsTakenByTeam)

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

    India Bowling : = 40
        bowling_change_wickets: 473
        total_wickets: 1182
              81 1 = 6.85
                85 2
                  88 3
                    64 4
                      76 5
                        79 6

awk -F'.' '{print $2}' ../IndiaBowlingChangeStats | sort | uniq -c

    Australia Bowling: = 37
        bowling_change_wickets: 407
        total_wickets: 1098
              65 1 = 5.9
                67 2
                  66 3
                    74 4
                      61 5
                        74 6c

    England Bowling: 40
        bowling_change_wickets: 371
        total_wickets: 916
              50 1 = 5.45
                62 2
                  53 3
                    71 4
                      74 5
                        61 6

    Pakistan Bowling 32
        bowling_change_wickets: 298
        total_wickets: 933
              39 1 = 4.18
                45 2
                  52 3
                    56 4
                      59 5
                        47 6
    SA 40
        bowling_change_wickets: 339
        total_wickets: 835
              48 1 = 5.74
                58 2
                  49 3
                    66 4
                      67 5
                        51 6
    NZ 31
        bowling_change_wickets: 230
        total_wickets: 729
              33 1 = 4.5
                44 2
                  35 3
                    51 4
                      34 5
                        33 6
    SL 36.6
        bowling_change_wickets: 398
        total_wickets: 1087
              59 1 = 5.4
                70 2
                  69 3
                    63 4
                      67 5
                        70 6

    WI = 32.1
        bowling_change_wickets: 248
        total_wickets: 772
              49 1 = 6.3
                36 2
                  44 3
                    40 4
                      41 5
                        38 6

''' 
