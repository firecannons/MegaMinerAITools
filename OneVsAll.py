import os
import threading
import subprocess
import time

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
JUGG_NUMBER_PROMPT_STRING = 'What is the folder number of the juggernaut AI?'
OUTPUT_FILE_NAME = 'OneVsAllResults.txt'

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
    print ('Done' )


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

def PlayGames ( NumberFolders , MatchMultiplier , StartingFolder , MatchParallelLimit , ServerName , GameName , JuggNumber ) :
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
    for Number2 in range ( NumberFolders ) :
      for MatchNumber in range ( MatchMultiplier ) :
        if NumberGamesRunning < MatchParallelLimit and len ( Threads [ 0 ] [ Number2 ] ) <= MatchNumber :
          NewThread = CreateRunningThread ( JuggNumber + 1 , Number2 + 1 , MatchNumber , StartingFolder , ServerName , GameName )
          NewOppoThread = CreateOppoRunningThread ( JuggNumber + 1 , Number2 + 1 , MatchNumber , StartingFolder , ServerName , GameName )
          Threads [ 0 ] [ Number2 ] . append ( NewThread )
          OppoThreads [ 0 ] [ Number2 ] . append ( NewOppoThread )
          NumberGamesRunning = NumberGamesRunning + 1
    for Number2 in range ( len ( Threads [ 0 ] ) ) :
      for MatchIndex in range ( len ( Threads [ 0 ] [ Number2 ] ) ) :
        if Threads [ 0 ] [ Number2 ] [ MatchIndex ]  . is_alive ( ) == True :
          print ( 'Thread ' + str ( 0 + 1 ) + ' ' + str ( Number2 + 1 ) + ' alive' )
        elif Threads [ 0 ] [ Number2 ] [ MatchIndex ] . joined == False :
          print ( 'Thread ' + str ( 0 + 1 ) + ' ' + str ( Number2 + 1 ) )
          Threads [ 0 ] [ Number2 ] [ MatchIndex ] . join ( )
          OppoThreads [ 0 ] [ Number2 ] [ MatchIndex ] . join ( )
          Threads [ 0 ] [ Number2 ] [ MatchIndex ] . joined = True
          OppoThreads [ 0 ] [ Number2 ] [ MatchIndex ] . joined = True
          NumberGamesRun = NumberGamesRun + 1
          NumberGamesRunning = NumberGamesRunning - 1
    time . sleep ( SCREEN_REFRESH_DELAY )
    UpdateConsole ( Threads , MatchMultiplier , NumberFolders , JuggNumber )
    print ( str ( NumberGamesRun ) + ' ' + str ( NumberGamesTotal ) )
    
  return Threads , OppoThreads

def UpdateConsole ( Threads , MatchMultiplier , NumberFolders , JuggNumber ) :
  ClearConsole ( )
  PrintReport ( Threads , MatchMultiplier , NumberFolders , JuggNumber )

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


def CalcReportString ( Threads , MatchMultiplier , NumberFolders , JuggNumber ) :
  ReportString = ''
  AIString = CalcAIString ( Threads [ 0 ] , JuggNumber , NumberFolders )
  ReportString = ReportString + AIString + '\n'
  for Number2 in range ( NumberFolders ) :
    SummaryPairingString = CalcSummaryPairingString ( Threads [ 0 ] [ Number2 ] , JuggNumber , Number2 , NumberFolders )
    ReportString = ReportString + SummaryPairingString + '\n'
    for MatchIndex in range ( MatchMultiplier ) :
      ReportLine = ''
      if MatchIndex < len ( Threads [ 0 ] [ Number2 ] ) :
        TempThread = Threads [ 0 ] [ Number2 ] [ MatchIndex ]
        '''print ( Threads [ 0 ] [ Number2 ] . stdout )'''
      else :
        TempThread = None
      ReportLine = GetReportLine ( TempThread , JuggNumber , Number2 , MatchIndex )
      ReportString = ReportString + ReportLine + '\n'
      ReportString = ReportString + '\n'
  return ReportString

def PrintReport ( Threads , MatchMultiplier , NumberFolders , JuggNumber ) :
  ReportString = CalcReportString ( Threads , MatchMultiplier , NumberFolders , JuggNumber )
  print ( ReportString )

def PromptForMatchMultiplier ( ) :
  print ( MATCH_MULTIPLIER_STRING )

def PromptForMatchParallelLimit ( ) :
  print ( MATCH_PARALLEL_LIMIT_STRING )

def PromptForServerName ( ) :
  print ( SERVER_NAME_PROMPT_STRING )

def PromptForGameName ( ) :
  print ( GAME_NAME_PROMPT_STRING )

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
  
def WriteOutputToFile ( Threads , MatchMultiplier , NumberFolders , JuggNumber ) :
  ReportString = CalcReportString ( Threads , MatchMultiplier , NumberFolders , JuggNumber )
  FileHandle = open ( OUTPUT_FILE_NAME , "w" )
  FileHandle . write ( ReportString )
  FileHandle . close ( )

def PromptForJuggNumber ( ) :
  print ( JUGG_NUMBER_PROMPT_STRING )

def GetJuggNumber ( ) :
  PromptForJuggNumber ( )
  JuggNumberString = input ( )
  JuggNumber = int ( JuggNumberString ) - 1
  return JuggNumber

def Main ( ) :

  MatchMultiplier = GetMatchMultiplier ( )
  
  MatchParallelLimit = GetMatchParallelLimit ( )
  
  ServerName = GetServerName ( )
  
  GameName = GetGameName ( )

  StartingFolder = GetStartingFolder ( )
  
  NumberFolders = FindNumberFolders ( )

  NumberMatches = CalcNumberMatches ( NumberFolders )
  
  JuggNumber = GetJuggNumber ( )

  print ( str ( NumberFolders ) + 'Folders' )

  print ( 'Creating Threads' )

  Threads , OppoThreads = PlayGames ( NumberFolders , MatchMultiplier , StartingFolder , MatchParallelLimit , ServerName , GameName , JuggNumber )
  
  WriteOutputToFile ( Threads , MatchMultiplier , NumberFolders , JuggNumber)

Main ( )
