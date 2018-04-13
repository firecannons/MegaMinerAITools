import os
import threading
import subprocess
import time
import matplotlib.pyplot as plt
import datetime

COMMAND_NAME = './run'
ADDED_PATH = '/Joueur.py'
SPACE = ' '
SESSION_FLAG = '-r'
SESSION_ID = 'DSSession'
VERSUS_TEXT = 'VS'
FORWARD_SLASH = '/'
SERVER_FLAG = '-s'
MATCH_MULTIPLIER_STRING = 'How many matches do you want for each AI pairing?'
MATCH_PARALLEL_LIMIT_STRING = 'What is the maximum number of matches you want to run at once?'
SERVER_NAME_PROMPT_STRING = 'What is the name of the game server (\'localhost\' for example)?'
SCREEN_REFRESH_DELAY = 0.5
GAME_NAME_PROMPT_STRING = 'What is the name of the game (\'Catastrophe\' for example)?'
MODE_PROMPT_STRING = '''Choose Mode:\nMode 1: Every AI against every AI (cross product).
Mode 2: Top numbered AI against every AI.
Mode 3: AI pairing written to file.
Type Mode:'''
AI_SCORE_MAX = 1
AI_SCORE_MIN = 0
AI_SCORE_START = 0.5
RUN_AIS_TIME_DELAY = 0.5
MINUTES_IN_HOUR = 60
SECONDS_IN_MINUTE = 60
SECOND_TIME_DELAY = 10
AI_SCORE_CHANGE_DIVISOR = 4
PLAY_AGAINST_SELF_PROMPT_STRING = 'Should AIs play against themselves ("Yes" or "No")?'

class AI :
  def __init__( self , Number ) :
    self . Scores = [ ]
    self . Times = [ ]
    self . Number = Number
    self . CurrentScore = AI_SCORE_START

def GetSessionName ( Number1 , Number2 , MatchNumber ) :
  SessionName = SESSION_ID + str ( Number1 ) + VERSUS_TEXT + str ( Number2 ) + 'Number' + str ( MatchNumber )
  return SessionName

def CalcWorkingDirectory ( Number1 , Number2 , Opposite , StartingFolder ) :
  ChangePath = ''
  if Opposite == False :
      ChangePath = StartingFolder + FORWARD_SLASH + str ( Number1 ) + ADDED_PATH
  else :
      ChangePath = StartingFolder + FORWARD_SLASH + str ( Number2 ) + ADDED_PATH
  return ChangePath

def GetCommand ( SessionName , ServerName , GameName ) :
  Command = COMMAND_NAME + SPACE + GameName + SPACE + SESSION_FLAG + SPACE + SessionName + SPACE + SERVER_FLAG + SPACE + ServerName
  return Command


class MyClass(threading.Thread):
  def __init__(self, Number1 , Number2, MatchNumber , Oppo , StartingFolder , ServerName , GameName):
    self . Oppo = Oppo
    self . Number1 = Number1
    self . Number2 = Number2
    self . MatchNumber = MatchNumber
    self.stdout = None
    self.stderr = None
    self . StartingFolder = StartingFolder
    self . joined = False
    self . ServerName = ServerName
    self . GameName = GameName
    threading.Thread.__init__(self)

  def run(self):
    SessionName = GetSessionName ( self . Number1 , self . Number2 , self . MatchNumber )
    ChangePath = CalcWorkingDirectory ( self . Number1 , self . Number2 , self . Oppo , self . StartingFolder )
    Command = GetCommand ( SessionName , self . ServerName , self . GameName )
    p = subprocess.Popen(Command.split(),
                         shell=False,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         cwd=ChangePath)

    self.stdout, self.stderr = p.communicate()


def IsFolder ( FolderName ) :
  Output = os . path . isdir ( FolderName )
  return Output

def GetLink ( Text ) :
  Output = ''
  Array = Text . split ( )
  for i in Array :
    if 'http' in i :
      Output = i
  return Output

def RetrieveTextUntilLinefeed ( Text , Pos ) :
  Length = len ( Text )
  Index = Pos
  while Index < Length and Text [ Index ] != '\n' :
    Index = Index + 1
  RetrievedText = Text [ Pos : Index ]
  return RetrievedText

def GetResultReason ( Text ) :
  Output = ''
  LostPos = Text . find ( 'Lost' )
  WonPos = Text . find ( 'Won' )
  if LostPos != -1 :
    Text = RetrieveTextUntilLinefeed ( Text , LostPos )
  else :
    Text = RetrieveTextUntilLinefeed ( Text , WonPos )
  return Text

def GetStartingFolder ( ) :
  ScriptPath = os.path.abspath(__file__)
  StartingFolder = os.path.dirname(ScriptPath)
  return StartingFolder

def FindNumberFolders ( ) :
  NumberFolders = 0
  while IsFolder ( str ( NumberFolders + 1 ) ) :
    NumberFolders = NumberFolders + 1
  return NumberFolders

def CalcNumberMatches ( NumberFolders ) :
  NumberMatches = NumberFolders * NumberFolders
  return NumberMatches

def CreateRunningThread ( Number1 , Number2 , MatchNumber , StartingFolder , ServerName , GameName ) :
  TempClass = MyClass ( Number1 , Number2 , MatchNumber , False , StartingFolder , ServerName , GameName )
  TempClass . start ( )
  return TempClass

def CreateOppoRunningThread ( Number1 , Number2 , MatchNumber , StartingFolder , ServerName , GameName ) :
  TempClass = MyClass ( Number1 , Number2 , MatchNumber , True , StartingFolder , ServerName , GameName)
  TempClass . start ( )
  return TempClass

def StartArena ( MatchMultiplier , StartingFolder , MatchParallelLimit , ServerName , GameName , StartTime , PlayAgainstSelf ) :
  StartArenaLoop ( MatchMultiplier , StartingFolder , MatchParallelLimit , ServerName , GameName , StartTime , PlayAgainstSelf )

def SetupThreads ( NumberFolders ) :
  Threads = [ ]
  OppoThreads = [ ]
  for Number1 in range ( NumberFolders ) :
    Threads . append ( [ ] )
    OppoThreads . append ( [ ] )
    for Number2 in range ( NumberFolders ) :
      Threads [ Number1 ] . append ( [ ] )
      OppoThreads [ Number1 ] . append ( [ ] )
  return Threads , OppoThreads
  
def UpdateNumberAIs ( AIs ) :
  NumberFolders = FindNumberFolders ( )
  AIs = CheckAINumber ( AIs , NumberFolders )

def StartArenaLoop ( MatchMultiplier , StartingFolder , MatchParallelLimit , ServerName , GameName , StartTime , PlayAgainstSelf ) :
  AIs = [ ]
  NumberGamesRunning = 0
  NumberGamesRanInCycle = 0
  NumberFolders = FindNumberFolders ( )
  AIs = CheckAINumber ( AIs , NumberFolders )
  Threads , OppoThreads = SetupThreads ( NumberFolders )
  LastTime = datetime . datetime(2013,12,31,23,59,59)
  while ( 1 == 1 ) :
    LastTime , AIs , NumberFolders = CheckForGraphUpdate ( AIs , StartTime , LastTime , Threads , OppoThreads , NumberFolders )
    NumberGamesRunning , NumberGamesRanInCycle = RunAIs ( MatchMultiplier , StartingFolder , MatchParallelLimit , ServerName , GameName , AIs , NumberGamesRunning , NumberGamesRanInCycle , Threads , OppoThreads , PlayAgainstSelf )
    Threads , OppoThreads , NumberGamesRanInCycle = CheckForMatchesPlayed ( NumberGamesRanInCycle , NumberFolders , Threads , OppoThreads , MatchMultiplier)
    time.sleep(RUN_AIS_TIME_DELAY)

def CheckForMatchesPlayed ( NumberGamesRanInCycle , NumberFolders , Threads , OppoThreads , MatchMultiplier ) :
  if ( NumberGamesRanInCycle >= NumberFolders * ( NumberFolders - 1 ) * MatchMultiplier ) :
    NumberGamesRanInCycle = 0
    Threads , OppoThreads = SetupThreads ( NumberFolders )
  return Threads , OppoThreads , NumberGamesRanInCycle

def SecondsSince ( TempTime ) :
  CurrentTime = datetime . datetime . now ( )
  DifferenceTimeInterval = CurrentTime - TempTime
  DifferenceSeconds = DifferenceTimeInterval . total_seconds ( )
  return DifferenceSeconds

def GetHoursSince ( TempTime ) :
  DifferenceSeconds = SecondsSince ( TempTime )
  DifferenceHours = DifferenceSeconds / ( SECONDS_IN_MINUTE * MINUTES_IN_HOUR )
  return DifferenceHours

def HasEnoughTimePassed ( SecondsDelay , LastTime ) :
  Output = False
  DifferenceSeconds = SecondsSince ( LastTime )
  if ( DifferenceSeconds > SecondsDelay ) :
    Output = True
  return Output
    
def CheckForGraphUpdate ( AIs , StartTime , LastTime , Threads , OppoThreads , NumberFolders ) :
  if ( HasEnoughTimePassed ( SECOND_TIME_DELAY , LastTime ) == True ) :
    LastTime = datetime . datetime . now ( )
    NumberFolders = FindNumberFolders ( )
    AIs = CheckAINumber ( AIs , NumberFolders )
    Threads , OppoThreads = CheckThreads ( NumberFolders , Threads , OppoThreads )
    AIs = GraphAIs ( AIs , StartTime )
  return LastTime , AIs , NumberFolders

def AddNewAIThreads ( NumberFolders , Threads , OppoThreads ) :
  Threads . append ( [ ] )
  OppoThreads . append ( [ ] )
  for Number1 in range ( NumberFolders ) :
    while len ( Threads [ Number1 ] ) < NumberFolders :
      Threads [ Number1 ] . append ( [ ] )
      OppoThreads [ Number1 ] . append ( [ ] )
  return Threads , OppoThreads

def CheckThreads ( NumberFolders , Threads , OppoThreads ) :
  while ( NumberFolders > len ( Threads ) ) :
    AddNewAIThreads ( NumberFolders , Threads , OppoThreads )
  return Threads , OppoThreads

def CheckAINumber ( AIs , NumberFolders ) :
  while ( NumberFolders > len ( AIs ) ) :
    NewAI = AI ( len ( AIs ) + 1 )
    AIs . append ( NewAI )
  return AIs

def GraphAIs ( AIs , StartTime ) :
  for AIIndex in range ( len ( AIs ) ) :
    CurrentAI = AIs [ AIIndex ]
    CurrentAI . Scores . append ( CurrentAI . CurrentScore )
    CurrentAI . Times . append ( GetHoursSince ( StartTime ) )
    plt.plot( CurrentAI . Times , CurrentAI . Scores , label = "AI " + str ( CurrentAI . Number ) )
  
  # naming the x axis
  plt.xlabel('Time')
  # naming the y axis
  plt.ylabel('Win Probability')
  # giving a title to my graph
  plt.title('AI Statistics')
   
  # show a legend on the plot
  plt.legend()
  
  plt.draw()
  
  plt.pause(0.001)
  
  plt.clf()
  
  return AIs

def RunAIs ( MatchMultiplier , StartingFolder , MatchParallelLimit , ServerName , GameName , AIs , NumberGamesRunning , NumberGamesRanInCycle , Threads , OppoThreads , PlayAgainstSelf ) :
  for Number1 in range ( len ( AIs ) ) :
    for Number2 in range ( len ( AIs ) ) :
      if Number1 != Number2 or PlayAgainstSelf == True :
        for MatchNumber in range ( MatchMultiplier ) :
          if NumberGamesRunning < MatchParallelLimit and len ( Threads [ Number1 ] [ Number2 ] ) <= MatchNumber :
            NewThread = CreateRunningThread ( Number1 + 1 , Number2 + 1 , MatchNumber , StartingFolder , ServerName , GameName )
            NewOppoThread = CreateOppoRunningThread ( Number1 + 1 , Number2 + 1 , MatchNumber , StartingFolder , ServerName , GameName )
            Threads [ Number1 ] [ Number2 ] . append ( NewThread )
            OppoThreads [ Number1 ] [ Number2 ] . append ( NewOppoThread )
            NumberGamesRunning = NumberGamesRunning + 1
  for Number1 in range ( len ( Threads ) ) :
    for Number2 in range ( len ( Threads [ Number1 ] ) ) :
      if Number1 != Number2 or PlayAgainstSelf == True :
        for MatchIndex in range ( len ( Threads [ Number1 ] [ Number2 ] ) ) :
          if Threads [ Number1 ] [ Number2 ] [ MatchIndex ]  . is_alive ( ) == False :
            if Threads [ Number1 ] [ Number2 ] [ MatchIndex ] . joined == False :
              Threads [ Number1 ] [ Number2 ] [ MatchIndex ] . join ( )
              OppoThreads [ Number1 ] [ Number2 ] [ MatchIndex ] . join ( )
              Threads [ Number1 ] [ Number2 ] [ MatchIndex ] . joined = True
              OppoThreads [ Number1 ] [ Number2 ] [ MatchIndex ] . joined = True
              ChangeAIScore ( Threads [ Number1 ] [ Number2 ] [ MatchIndex ] , AIs [ Number1 ] )
              ChangeAIScore ( OppoThreads [ Number1 ] [ Number2 ] [ MatchIndex ] , AIs [ Number2 ] )
              OutputMatchString ( Threads [ Number1 ] [ Number2 ] [ MatchIndex ] , Number1 , Number2 )
              NumberGamesRunning = NumberGamesRunning - 1
              NumberGamesRanInCycle = NumberGamesRanInCycle + 1
  return NumberGamesRunning , NumberGamesRanInCycle

def ChangeAIScore ( Thread , AI ) :
  DidAIWin = DidWin ( Thread )
  TargetScore = AI_SCORE_START
  if ( DidAIWin == True ) :
    TargetScore = AI_SCORE_MAX
  else :
    TargetScore = AI_SCORE_MIN
  ScoreChange = TargetScore - AI . CurrentScore
  AI . CurrentScore = AI . CurrentScore + ( ScoreChange / AI_SCORE_CHANGE_DIVISOR )

def OutputMatchString ( Thread , Number1 , Number2 ) :
  AINumber1 = Number1 + 1
  AINumber2 = Number2 + 1
  AINumber1String = str ( AINumber1 )
  AINumber2String = str ( AINumber2 )
  WinnerNumber = 0
  if ( DidWin ( Thread ) == True ) :
    WinnerNumber = AINumber1
  else :
    WinnerNumber = AINumber2
  WinnerNumberString = str ( WinnerNumber )
  ThreadOutput = Thread . stdout . decode("utf-8")
  OutputString = ''
  OutputString = OutputString + str ( datetime . datetime . now ( ) )
  OutputString = OutputString + SPACE + SPACE
  OutputString = OutputString + 'AI ' + AINumber1String + ' vs ' + AINumber2String
  OutputString = OutputString + SPACE + SPACE
  OutputString = OutputString + 'Winner: AI ' + WinnerNumberString
  OutputString = OutputString + SPACE + SPACE
  OutputString = OutputString + ' Link to Visualizer: ' + GetLink ( ThreadOutput )
  OutputString = OutputString + '     '
  OutputString = OutputString + 'Reason for result: ' + GetResultReason ( ThreadOutput )
  print ( OutputString )

def PlayGames ( NumberFolders , MatchMultiplier , StartingFolder , MatchParallelLimit , ServerName , GameName , Mode ) :
  Threads = [ ]
  OppoThreads = [ ]
  if Mode == 1 :
    Threads , OppoThreads = PlayCrossProductGames ( NumberFolders , MatchMultiplier , StartingFolder , MatchParallelLimit , ServerName , GameName )
    WriteOutputToFileCrossProduct ( Threads , MatchMultiplier , NumberFolders )
  elif Mode == 2 :
    Threads , OppoThreads = PlayHighestNumberGames ( NumberFolders , MatchMultiplier , StartingFolder , MatchParallelLimit , ServerName , GameName )
    WriteOutputToFileHighestNumber ( Threads , MatchMultiplier , NumberFolders )
  else :
    Threads , OppoThreads = PlaySelectPairings ( NumberFolders , MatchMultiplier , StartingFolder , MatchParallelLimit , ServerName , GameName )
  return Threads , OppoThreads

def PlaySelectPairings ( NumberFolders , MatchMultiplier , StartingFolder , MatchParallelLimit , ServerName , GameName ) :
  
  Threads = [ ]
  OppoThreads = [ ]
  return Threads , OppoThreads

def PlayHighestNumberGames ( NumberFolders , MatchMultiplier , StartingFolder , MatchParallelLimit , ServerName , GameName ) :
  NumberGamesTotal = NumberFolders * MatchMultiplier
  NumberGamesRun = 0
  NumberGamesRunning = 0
  Threads = [ ]
  OppoThreads = [ ]
  Threads . append ( [ ] )
  OppoThreads . append ( [ ] )
  for Number2 in range ( NumberFolders ) :
    Threads [ 0 ] . append ( [ ] )
    OppoThreads [ 0 ] . append ( [ ] )
  while NumberGamesRun < NumberGamesTotal :
    Number1 = 0
    for Number2 in range ( NumberFolders ) :
      for MatchNumber in range ( MatchMultiplier ) :
        if NumberGamesRunning < MatchParallelLimit and len ( Threads [ Number1 ] [ Number2 ] ) <= MatchNumber :
          NewThread = CreateRunningThread ( NumberFolders , Number2 + 1 , MatchNumber , StartingFolder , ServerName , GameName )
          NewOppoThread = CreateOppoRunningThread ( NumberFolders , Number2 + 1 , MatchNumber , StartingFolder , ServerName , GameName )
          Threads [ Number1 ] [ Number2 ] . append ( NewThread )
          OppoThreads [ Number1 ] [ Number2 ] . append ( NewOppoThread )
          NumberGamesRunning = NumberGamesRunning + 1
    for Number1 in range ( len ( Threads ) ) :
      for Number2 in range ( len ( Threads [ Number1 ] ) ) :
        for MatchIndex in range ( len ( Threads [ Number1 ] [ Number2 ] ) ) :
          if Threads [ Number1 ] [ Number2 ] [ MatchIndex ]  . is_alive ( ) == True :
            print ( 'Thread ' + str ( Number1 + 1 ) + ' ' + str ( Number2 + 1 ) + ' alive' )
          elif Threads [ Number1 ] [ Number2 ] [ MatchIndex ] . joined == False :
            print ( 'Thread ' + str ( Number1 + 1 ) + ' ' + str ( Number2 + 1 ) )
            Threads [ Number1 ] [ Number2 ] [ MatchIndex ] . join ( )
            OppoThreads [ Number1 ] [ Number2 ] [ MatchIndex ] . join ( )
            Threads [ Number1 ] [ Number2 ] [ MatchIndex ] . joined = True
            OppoThreads [ Number1 ] [ Number2 ] [ MatchIndex ] . joined = True
            NumberGamesRun = NumberGamesRun + 1
            NumberGamesRunning = NumberGamesRunning - 1
    time . sleep ( SCREEN_REFRESH_DELAY )
    UpdateConsoleHighestNumber ( Threads , MatchMultiplier , NumberFolders )
    print ( str ( NumberGamesRun ) + ' ' + str ( NumberGamesTotal ) )
    
  return Threads , OppoThreads

def PlayCrossProductGames ( NumberFolders , MatchMultiplier , StartingFolder , MatchParallelLimit , ServerName , GameName ) :
  NumberGamesTotal = NumberFolders * NumberFolders * MatchMultiplier
  NumberGamesRun = 0
  NumberGamesRunning = 0
  Threads = [ ]
  OppoThreads = [ ]
  for Number1 in range ( NumberFolders ) :
    Threads . append ( [ ] )
    OppoThreads . append ( [ ] )
    for Number2 in range ( NumberFolders ) :
      Threads [ Number1 ] . append ( [ ] )
      OppoThreads [ Number1 ] . append ( [ ] )
  while NumberGamesRun < NumberGamesTotal :
    for Number1 in range ( NumberFolders ) :
      for Number2 in range ( NumberFolders ) :
        for MatchNumber in range ( MatchMultiplier ) :
          if NumberGamesRunning < MatchParallelLimit and len ( Threads [ Number1 ] [ Number2 ] ) <= MatchNumber :
            NewThread = CreateRunningThread ( Number1 + 1 , Number2 + 1 , MatchNumber , StartingFolder , ServerName , GameName )
            NewOppoThread = CreateOppoRunningThread ( Number1 + 1 , Number2 + 1 , MatchNumber , StartingFolder , ServerName , GameName )
            Threads [ Number1 ] [ Number2 ] . append ( NewThread )
            OppoThreads [ Number1 ] [ Number2 ] . append ( NewOppoThread )
            NumberGamesRunning = NumberGamesRunning + 1
    for Number1 in range ( len ( Threads ) ) :
      for Number2 in range ( len ( Threads [ Number1 ] ) ) :
        for MatchIndex in range ( len ( Threads [ Number1 ] [ Number2 ] ) ) :
          if Threads [ Number1 ] [ Number2 ] [ MatchIndex ]  . is_alive ( ) == True :
            print ( 'Thread ' + str ( Number1 + 1 ) + ' ' + str ( Number2 + 1 ) + ' alive' )
          elif Threads [ Number1 ] [ Number2 ] [ MatchIndex ] . joined == False :
            print ( 'Thread ' + str ( Number1 + 1 ) + ' ' + str ( Number2 + 1 ) )
            Threads [ Number1 ] [ Number2 ] [ MatchIndex ] . join ( )
            OppoThreads [ Number1 ] [ Number2 ] [ MatchIndex ] . join ( )
            Threads [ Number1 ] [ Number2 ] [ MatchIndex ] . joined = True
            OppoThreads [ Number1 ] [ Number2 ] [ MatchIndex ] . joined = True
            NumberGamesRun = NumberGamesRun + 1
            NumberGamesRunning = NumberGamesRunning - 1
    time . sleep ( SCREEN_REFRESH_DELAY )
    UpdateConsoleCrossProduct ( Threads , MatchMultiplier , NumberFolders )
    print ( str ( NumberGamesRun ) + ' ' + str ( NumberGamesTotal ) )
    
  return Threads , OppoThreads

def UpdateConsoleCrossProduct ( Threads , MatchMultiplier , NumberFolders ) :
  ClearConsole ( )
  PrintReportCrossProduct ( Threads , MatchMultiplier , NumberFolders )

def UpdateConsoleHighestNumber ( Threads , MatchMultiplier , NumberFolders ) :
  ClearConsole ( )
  PrintReportHighestNumber ( Threads , MatchMultiplier , NumberFolders )

def GetReportLine ( Thread , Number1 , Number2 , MatchIndex ) :
  ReportLine = '\t\tMatch ' + str ( MatchIndex + 1 ) + ' : '
  if Thread != None :
    if Thread . is_alive ( ) == False :
      ThreadOutput = Thread . stdout . decode("utf-8")
      if 'Lost' in ThreadOutput :
        ReportLine = ReportLine + 'Lost'
      else :
        ReportLine = ReportLine + 'Won'
      ReportLine = ReportLine + ' Link to Visualizer: ' + GetLink ( ThreadOutput )
      ReportLine = ReportLine + '     '
      ReportLine = ReportLine + 'Reason for result: ' + GetResultReason ( ThreadOutput )
    else :
      ReportLine = ReportLine + 'Not Finished Yet'
  else :
    ReportLine = ReportLine + 'Not Finished Yet'
  return ReportLine

def ClearConsole ( ) :
  print('\033[H\033[J')

def DidWin ( Thread ) :
  DidWin = False
  ThreadOutput = Thread . stdout . decode("utf-8")
  WonPos = ThreadOutput . find ( 'Won' )
  if WonPos != -1 :
    DidWin = True
  return DidWin

def CalcOneAIAverageScoreString ( OneAIThreads ) :
  AverageScoreString = ''
  NumItems = len ( OneAIThreads )
  AverageScore = 0
  DoneThreads = 0
  for Threads in OneAIThreads :
    AverageString = CalcAverageScoreString ( Threads )
    if AverageString != '??' :
      DoneThreads = DoneThreads + 1
      AverageScore = AverageScore + float ( AverageString )
  if DoneThreads != 0 :
    AverageScore = AverageScore / DoneThreads
    AverageScoreString = str ( AverageScore )
  else :
    AverageScoreString = '??'
  return AverageScoreString


def CalcAverageScoreString ( OnePairThreads ) :
  AverageScoreString = ''
  NumItems = len ( OnePairThreads )
  AverageScore = 0.0
  DonePairs = 0
  for Thread in OnePairThreads :
    if Thread . is_alive ( ) == False :
      DonePairs = DonePairs + 1
      if DidWin ( Thread ) == True :
        AverageScore = AverageScore + 1
  if DonePairs != 0 :
    AverageScore = AverageScore / NumItems
    AverageScoreString = str ( AverageScore )
  else :
    AverageScoreString = '??'
  return AverageScoreString

def CalcSummaryPairingString( OnePairThreads , Number1 , Number2 , NumberFolders ) :
  SummaryParingString = '\tAI ' + str ( Number1 + 1 ) + ' against AI ' + str ( Number2 + 1 )
  SummaryParingString = SummaryParingString + ' - '
  AverageScoreString = CalcAverageScoreString ( OnePairThreads )
  SummaryParingString = SummaryParingString + 'Average : ' + AverageScoreString
  return SummaryParingString

def CalcAIString ( OneAIThreads , Number1 , NumberFolders ) :
  AIString = ''
  AIString = AIString + 'AI ' + str ( Number1 + 1 ) + ' --------- : '
  AverageScoreString = CalcOneAIAverageScoreString ( OneAIThreads )
  AIString = AIString + 'Average : ' + AverageScoreString
  return AIString

def CalcReportStringHighestNumber ( Threads , MatchMultiplier , NumberFolders ) :
  ReportString = ''
  for Number1 in range ( len ( Threads ) ) :
    AIString = CalcAIString ( Threads [ Number1 ] , Number1 , NumberFolders )
    ReportString = ReportString + AIString + '\n'
    for Number2 in range ( len ( Threads [ Number1 ] ) ) :
      SummaryPairingString = CalcSummaryPairingString ( Threads [ Number1 ] [ Number2 ] , NumberFolders - 1 , Number2 , NumberFolders )
      ReportString = ReportString + SummaryPairingString + '\n'
      for MatchIndex in range ( MatchMultiplier ) :
        ReportLine = ''
        if MatchIndex < len ( Threads [ Number1 ] [ Number2 ] ) :
          TempThread = Threads [ Number1 ] [ Number2 ] [ MatchIndex ]
          '''print ( Threads [ Number1 ] [ Number2 ] . stdout )'''
        else :
          TempThread = None
        ReportLine = GetReportLine ( TempThread , Number1 , Number2 , MatchIndex )
        ReportString = ReportString + ReportLine + '\n'
        ReportString = ReportString + '\n'
  return ReportString

def CalcReportStringCrossProduct ( Threads , MatchMultiplier , NumberFolders ) :
  ReportString = ''
  for Number1 in range ( len ( Threads ) ) :
    AIString = CalcAIString ( Threads [ Number1 ] , Number1 , NumberFolders )
    ReportString = ReportString + AIString + '\n'
    for Number2 in range ( len ( Threads [ Number1 ] ) ) :
      SummaryPairingString = CalcSummaryPairingString ( Threads [ Number1 ] [ Number2 ] , Number1 , Number2 , NumberFolders )
      ReportString = ReportString + SummaryPairingString + '\n'
      for MatchIndex in range ( MatchMultiplier ) :
        ReportLine = ''
        if MatchIndex < len ( Threads [ Number1 ] [ Number2 ] ) :
          TempThread = Threads [ Number1 ] [ Number2 ] [ MatchIndex ]
          '''print ( Threads [ Number1 ] [ Number2 ] . stdout )'''
        else :
          TempThread = None
        ReportLine = GetReportLine ( TempThread , Number1 , Number2 , MatchIndex )
        ReportString = ReportString + ReportLine + '\n'
        ReportString = ReportString + '\n'
  return ReportString

def PrintReportCrossProduct ( Threads , MatchMultiplier , NumberFolders ) :
  ReportString = CalcReportStringCrossProduct ( Threads , MatchMultiplier , NumberFolders )
  print ( ReportString )

def PrintReportHighestNumber ( Threads , MatchMultiplier , NumberFolders ) :
  ReportString = CalcReportStringHighestNumber ( Threads , MatchMultiplier , NumberFolders )
  print ( ReportString )

def PromptForMatchMultiplier ( ) :
  print ( MATCH_MULTIPLIER_STRING )

def PromptForMatchParallelLimit ( ) :
  print ( MATCH_PARALLEL_LIMIT_STRING )

def PromptForServerName ( ) :
  print ( SERVER_NAME_PROMPT_STRING )

def PromptForGameName ( ) :
  print ( GAME_NAME_PROMPT_STRING )

def PromptForMode ( ) :
  print ( MODE_PROMPT_STRING )

def PromptForPlayAgainstSelf ( ) :
  print ( PLAY_AGAINST_SELF_PROMPT_STRING )

def GetMatchMultiplier ( ) :
  PromptForMatchMultiplier ( )
  MatchMultiplierString = input ( )
  MatchMultiplier = int ( MatchMultiplierString )
  return MatchMultiplier

def GetMatchParallelLimit ( ) :
  PromptForMatchParallelLimit ( )
  MatchParallelLimitString = input ( )
  MatchParallelLimit = int ( MatchParallelLimitString )
  return MatchParallelLimit

def GetServerName ( ) :
  PromptForServerName ( )
  ServerName = input ( )
  return ServerName

def GetGameName ( ) :
  PromptForGameName ( )
  GameName = input ( )
  return GameName
  
def GetMode ( ) :
  PromptForMode ( )
  ModeString = input ( )
  Mode = int ( ModeString )
  return Mode

def GetPlayAgainstSelf ( ) :
  PromptForPlayAgainstSelf ( )
  PASInput = input ( )
  PlayAgainstSelf = False
  if PASInput == 'Yes' or PASInput == 'yes' :
    PlayAgainstSelf = True
  return PlayAgainstSelf
  
def WriteOutputToFileCrossProduct ( Threads , MatchMultiplier , NumberFolders ) :
  ReportString = CalcReportStringCrossProduct ( Threads , MatchMultiplier , NumberFolders )
  FileHandle = open ( "RunAllResults.txt" , "w" )
  FileHandle . write ( ReportString )
  FileHandle . close ( )

def WriteOutputToFileHighestNumber ( Threads , MatchMultiplier , NumberFolders ) :
  ReportString = CalcReportStringHighestNumber ( Threads , MatchMultiplier , NumberFolders )
  FileHandle = open ( "RunAllResults.txt" , "w" )
  FileHandle . write ( ReportString )
  FileHandle . close ( )

def InitGraph ( ) :
  plt.ion()
  plt.show()

def Main ( ) :

  MatchMultiplier = GetMatchMultiplier ( )
  
  MatchParallelLimit = GetMatchParallelLimit ( )
  
  ServerName = GetServerName ( )
  
  GameName = GetGameName ( )

  StartingFolder = GetStartingFolder ( )
  
  PlayAgainstSelf = GetPlayAgainstSelf ( )
  
  NumberFolders = FindNumberFolders ( )
  
  InitGraph ( )
  
  StartTime = datetime . datetime . now ( )

  StartArena ( MatchMultiplier , StartingFolder , MatchParallelLimit , ServerName , GameName , StartTime , PlayAgainstSelf )

Main ( )
