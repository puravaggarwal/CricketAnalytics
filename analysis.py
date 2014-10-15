#grep -r teams: /Users/purav.aggarwal/Documents/Purav/ResearchMe/CricketAnalytics/odis/data/* -2 | grep India | awk -F'-' '{print $1}' | awk -F'/' '{print $NF}'
import yaml
import os
teamName = "Sri Lanka"
fileN = "Sri_Lanka" #teamName
fileName = "/Users/purav.aggarwal/Documents/Purav/ResearchMe/CricketAnalytics/odis/"+fileN+"Match"
folderPath = "/Users/purav.aggarwal/Documents/Purav/ResearchMe/CricketAnalytics/odis/data/"
command = "grep -r teams: %s -2 | grep \"%s\" | awk -F'-' '{print $1}' | awk -F'/' '{print $NF}' >  %s"%(folderPath,teamName,fileName)
print command
os.system(command)

matchstream = open("/Users/purav.aggarwal/Documents/Purav/ResearchMe/CricketAnalytics/odis/"+fileN+"Match",'r')
totalWicketsTakenByIndia = 0
totalBallingChangeWicketsByIndia = 0
for match in matchstream:
    stream = open("/Users/purav.aggarwal/Documents/Purav/ResearchMe/CricketAnalytics/odis/data/"+match.strip(),'r')
    data = yaml.load(stream)
    info = data.get('info')
    innings = data.get('innings')

    requiredInnings = innings[0].get('1st innings')
    if(requiredInnings.get('team') == teamName):
        if(len(innings) == 2):
            requiredInnings = innings[1].get('2nd innings')
            if(requiredInnings.get('team') == teamName):
                print "ERROR:"+match
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
    
            #0. Check if it's a wicket ball
            itsAWicketBall = False
            if(deliveries[i].get(ballKey).get('wicket')):
                total_wickets += 1
                itsAWicketBall = True

            if(itsABallingChangeOver and itsAWicketBall and (numOfAccountableBalls <= targetBowlingChangeNumberOfBalls)):
                bowling_change_wickets += 1
                #print("Bowling Change:")
                #print currentBowlerA
                #print currentBowlerB
                #print previousBowler
                #print overNumber
                #print ballKey
                print numOfAccountableBalls
    
            if(numOfAccountableBalls == 6):
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
    totalBallingChangeWicketsByIndia += bowling_change_wickets
    totalWicketsTakenByIndia += total_wickets

print "bowling_change_wickets: " + str(totalBallingChangeWicketsByIndia)
print "total_wickets: " + str(totalWicketsTakenByIndia)

'''
Interesting:

    Seems an extra ball was bowled here : 597926.yaml - observe over 1.1 - india bowling
    Seems a 5 ball over was bowled here : 392619.yaml - 4.5 - Australia bowling
    Seems a 7 ball over - 352667.yaml - WestIndies batting England Balling - 1st over
    Extra ball over - Australia England - 36th over England Balling
    5 Ball Over - 567360.yaml - - South Africa        - New Zealand 48th over SA
    7 ball over - 385749.yaml - Pak Lanka - 28th over Pak batting
    5 ball over - 518960.yaml India Lanka - lanka bowling - 29th over

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
''' 
