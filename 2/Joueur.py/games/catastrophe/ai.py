# This is where you build your AI for the Catastrophe game.

from joueur.base_ai import BaseAI

# <<-- Creer-Merge: imports -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
# you can add additional import(s) here
# <<-- /Creer-Merge: imports -->>

MISSIONARY_NAME = 'missionary'
FRESH_NAME = 'fresh human'

class AI(BaseAI):
    """ The basic AI functions that are the same between games. """

    def get_name(self):
        """ This is the name you send to the server so your AI will control the player named this string.

        Returns
            str: The name of your Player.
        """
        # <<-- Creer-Merge: get-name -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        return "Catastrophe Python Player 2" # REPLACE THIS WITH YOUR TEAM NAME
        # <<-- /Creer-Merge: get-name -->>

    def start(self):
        """ This is called once the game starts and your AI knows its playerID and game. You can initialize your AI here.
        """
        # <<-- Creer-Merge: start -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your start logic
        # <<-- /Creer-Merge: start -->>

    def game_updated(self):
        """ This is called every time the game's state updates, so if you are tracking anything you can update it here.
        """
        # <<-- Creer-Merge: game-updated -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your game updated logic
        # <<-- /Creer-Merge: game-updated -->>

    def end(self, won, reason):
        """ This is called when the game ends, you can clean up your data and dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why you won or lost.
        """
        # <<-- Creer-Merge: end -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your end logic
        # <<-- /Creer-Merge: end -->>

    def DetectIfNeutral ( self , Unit ) :
      Output = False
      if Unit . owner == None :
        Output = True
      return Output

    def FindNeutralHumans ( self , GameUnits ) :
      NeutralHumans = []
      for Unit in GameUnits :
        if self . DetectIfNeutral ( Unit ) == True :
          NeutralHumans . append ( Unit )
      return NeutralHumans

    def GetDistanceBetweenTiles ( self , Tile1 , Tile2 ) :
      Path = self . find_path ( Tile1 , Tile2 )
      Distance = len ( Path )
      return Distance

    def DistanceToUnit ( self , Unit1 , Unit2 ) :
      Tile1 = Unit1 . tile
      Tile2 = Unit2 . tile
      Distance = self . GetDistanceBetweenTiles ( Tile1 , Tile2 )
      return Distance

    def FindClosestNeutral ( self , Unit , Neutrals ) :
      MinDist = 9999
      Target = None
      for Neutral in Neutrals :
        if self . DistanceToUnit ( Unit , Neutral ) < MinDist :
          Target = Neutral
      return Target

    def GetNextTile ( self , Unit , TargetTile ) :
      UnitTile = Unit . tile
      Path = self . find_path ( UnitTile , TargetTile )
      TargetTile = Path [ 0 ]
      return TargetTile

    def MissionaryAction ( self , Missionary ) :
      GameUnits = self . GetGameUnits ( )
      Target = self . FindClosestNeutral ( Missionary , GameUnits )
      if self . DistanceToUnit ( Missionary , Target ) <= 1 :
        Missionary . convert ( Target . tile )

    def MoveActionTypeSwitch ( self , Unit ) :
      Title = Unit . job . title
      if Title == 'missionary' :
        self . MissionaryAction ( Unit )

    def MoveIfTileOK ( self , Unit , TargetTile ) :
      Tile = self . GetNextTile ( Unit , TargetTile )
      Unit . move ( Tile )
      self . MoveActionTypeSwitch ( Unit )

    def IsMorePath ( self , Unit , TargetTile ) :
      OK = True
      Tile = self . GetNextTile ( Unit , TargetTile )
      if Tile == None :
        OK = False
      return OK

    def MoveToward ( self , Unit , TargetTile ) :
      self . MoveActionTypeSwitch ( Unit )
      MovesLeft = Unit . moves
      Distance = self . GetDistanceBetweenTiles ( Unit . tile , TargetTile )
      while MovesLeft > 0 and Distance > 1 :
        self . MoveIfTileOK ( Unit , TargetTile )
        Distance = self . GetDistanceBetweenTiles ( Unit . tile , TargetTile )
        MovesLeft = Unit . moves

    def GetGameUnits ( self ) :
      GameUnits = self . game . units
      return GameUnits

    def MoveMissionary ( self , Unit ) :
      GameUnits = self . GetGameUnits ( )
      Neutrals = self . FindNeutralHumans ( GameUnits )
      Target = self . FindClosestNeutral ( Unit , Neutrals )
      if Target != None :
        self . MoveToward ( Unit , Target . tile )

    def DoMissionary ( self , Unit ) :
      self . MoveMissionary ( Unit )

    def SwitchForType ( self , Unit ) :
      Title = Unit . job . title
      if Title == 'missionary' :
        self . DoMissionary ( Unit )

    def MoveUnits ( self , Units ) :
      for Unit in Units :
        self . SwitchForType ( Unit )

    def CreateMissionaryIfFresh ( self , Unit ) :
      Output = False
      Title = Unit . job . title
      print ( Title )
      if Title == 'fresh human' :
        Unit . change_job ( 'missionary' )
        Output = True
      return Output

    def GetMissionary ( self , PlayerUnits ) :
      HaveFresh = False
      for Unit in PlayerUnits :
        if HaveFresh == False :
          HaveFresh = self . CreateMissionaryIfFresh ( Unit )


    def InitialChangeJobs ( self , PlayerUnits ) :
      self . GetMissionary ( PlayerUnits )

    def run_turn(self):
        """ This is called every time it is this AI.player's turn.

        Returns:
            bool: Represents if you want to end your turn. True means end your turn, False means to keep your turn going and re-call this function.
        """

        print ( 'Running turn' )

        PlayerUnits = self . player . units

        Me = self . player
        if self . game . current_turn <= 1 :
          print ( 'changing jobs' )
          self . InitialChangeJobs ( PlayerUnits )

        self . MoveUnits ( PlayerUnits )





        # <<-- Creer-Merge: runTurn -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # Put your game logic here for runTurn
        return True
        # <<-- /Creer-Merge: runTurn -->>

    def find_path(self, start, goal):
        """A very basic path finding algorithm (Breadth First Search) that when given a starting Tile, will return a valid path to the goal Tile.
        Args:
            start (Tile): the starting Tile
            goal (Tile): the goal Tile
        Returns:
            list[Tile]: A list of Tiles representing the path, the the first element being a valid adjacent Tile to the start, and the last element being the goal.
        """

        if start == goal:
            # no need to make a path to here...
            return []

        # queue of the tiles that will have their neighbors searched for 'goal'
        fringe = []

        # How we got to each tile that went into the fringe.
        came_from = {}

        # Enqueue start as the first tile to have its neighbors searched.
        fringe.append(start)

        # keep exploring neighbors of neighbors... until there are no more.
        while len(fringe) > 0:
            # the tile we are currently exploring.
            inspect = fringe.pop(0)

            # cycle through the tile's neighbors.
            for neighbor in inspect.get_neighbors():
                # if we found the goal, we have the path!
                if neighbor == goal:
                    # Follow the path backward to the start from the goal and return it.
                    path = [goal]

                    # Starting at the tile we are currently at, insert them retracing our steps till we get to the starting tile
                    while inspect != start:
                        path.insert(0, inspect)
                        inspect = came_from[inspect.id]
                    return path
                # else we did not find the goal, so enqueue this tile's neighbors to be inspected

                # if the tile exists, has not been explored or added to the fringe yet, and it is pathable
                if neighbor and neighbor.id not in came_from and neighbor.is_pathable():
                    # add it to the tiles to be explored and add where it came from for path reconstruction.
                    fringe.append(neighbor)
                    came_from[neighbor.id] = inspect

        # if you're here, that means that there was not a path to get to where you want to go.
        #   in that case, we'll just return an empty path.
        return []

    # <<-- Creer-Merge: functions -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
    # if you need additional functions for your AI you can add them here
    # <<-- /Creer-Merge: functions -->>
