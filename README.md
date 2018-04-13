# MegaMinerAITools
This is a repository of scripts to help with playing Python AIs in MegaMinerAI, an AI programming competition put on SIG-Game at Missouri S&T.  SIG-Game basically makes a video game that can be controlled by a program.  MegaMinerAI is competition held once per semester, where they will release the game and let people compete for 24 hours to write the best computer program to play the game.

[SIG-Game's Website](http://siggame.io/)

## About the AI (not these tools)
### File Structure of the AI
The standard AI distribution can be found at [https://github.com/siggame/Cadre](https://github.com/siggame/Cadre).  Cadre is the main folder of the AI.  A simple version of the file structure looks like
> /Cadre<br>
> &nbsp;&nbsp;&nbsp;&nbsp;/Joueur.py<br>
> &nbsp;&nbsp;&nbsp;&nbsp;/Joueur.cpp<br>
> &nbsp;&nbsp;&nbsp;&nbsp;etc.

<br>
Each Joueur folder contains blank AI in a different programming language.  To add code to an AI go to the AI file here:

> /Cadre<br>
> &nbsp;&nbsp;&nbsp;&nbsp;/[Joueur Folder]<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/Games<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/[Game Name]<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;AI.*

Where `[Joueur Folder]` is the name of your programming language's Joueur folder, `[Game Name]` is the name of the game you want to play, and `*` is the file extension of files of your programming language.  Inside each AI.* file, there will be a function named similar to `run_turn()`.  In that function you can put code to play the AI.  To see the APIs for various games, go to [http://docs.siggame.io/](http://docs.siggame.io/).

After writing code in your AI, you may need to build your code.  In languages like C++, you will have to run a Makefile builld it.  In Python, we can skip building code since it is interpreted on the fly.

## Playing games
Next, you will want to play a match.  Matches are play 1v1.  Two AI's will run against each other, and a ***game server*** will facilitate the game in the middle.  Those two AIs will use a ***Session Name***, a string to specifically play against each other.  Since matches are 1v1, you must start two AIs on the same game server and session name for them to battle.

To play your AI in a game you can use the `run` and `testRun` bash script.
`testRun` is the same as `run` except that it pre-specifies the game server to be SIG-Game's game server, **game.siggame.io**.  An example of the syntax or run is `./run -s [Server Name] -r [Session Name] [Game Name]` where `[Server Name]` is the name of the game server, `[Session Name]` is the name of the session you are playing on, and `[Game Name]` is the name of the game your are playing.  A real world example could be `./run -s game.siggame.io -r MySession Catastrophe`.  Also, you can run a game server locally on your own computer, and I have found that matches play faster on it because it is local.  To see SIG-Game's game server repository, go to [https://github.com/siggame/Cerveau](https://github.com/siggame/Cerveau).  If you run a game server locally, the game server name will be `localhost`.

Finally, games can be visualized in the visualizer.  This allows you to actually see what went on during the game.  The console will output a link to visual a game log of the game and you can go to link to see the game visualized.  Also outputted is whether the game was won or loss.  The visualizer can also be run on your own computer.  The repository for the visualizer can be found at [https://github.com/siggame/Viseur](https://github.com/siggame/Viseur).

## These MegaMinerAI tools
These tools are designed to help facilitate the creation of MegaMinerAI AIs.  They are three Python scripts, written for Python 3.  You can use them to determine which of you AIs is doing the best against the others, and in which direction you should continue your developement.<br>Along with these tools are 2 different Python AIs for the game Catastrophe.

Breakdown of each Python program

| Script         | Purpose                                              |
| -------------- | ---------------------------------------------------- |
| OneVsAll.py    | Plays 1 AI against all the rest                      |
| RunAll.py      | Plays all AIs against all AIs (like a cross product) |
| SimpleArena.py | Is a real time arena that graph AI performance       |

## Required Installations
The only dependency if matplotlib, and that is for the SimpleArena script.
To install matplotlib, enter into the console `pip3 install matplotlib`.

## How to use them

To use these, you must store your AIs in this type of structure of files:

> /<br>
> &nbsp;&nbsp;&nbsp;&nbsp;/1<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/Joueur.py<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;whatever<br>
> &nbsp;&nbsp;&nbsp;&nbsp;/2<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/Joueur.py<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;whatever<br>
> &nbsp;&nbsp;&nbsp;&nbsp;/etc.<br>

Where each numbered folder is a different version of your AI.

At the beginning of each program it asks you several questions:<br>
**How many matches do you want for each AI pairing?** - for each pair of AI's that the program makes, how many matches do you want it to play.<br>
**What is the maximum number of matches you want to run at once?** - how many games to run at once.  If this is too high, it can lock up your computer.<br>
**What is the name of the game server** - the game server to play the matches on.<br>
**What is the name of the game** - the game you want to play.<br>

## RunAll

This program will run all of the numbered AIs against every other one, including itself.  It will print out statistics of the matches while it is running and output the statistics to a text file at the end of the program, named `RunAllResults.txt`.

Sample usage: `python3 RunAll.py`


## OneVsAll

This program will run one numbered AI (called the juggernaut) against every other one, including itself.  It will prompt the user for the number of the AI to be the juggernaut.  It will print out statistics of the matches while it is running and output the statistics to a text file at the end of the program, named `OneVsAll.txt`.

Sample usage: `python3 OneVsAll.py`

## SimpleArena

This continuously run AIs against each other and graph them on a graph.  It has the ability to keep an AI from playing against itself while playing the AIs against each other.  At the beginning of the program it will ask an additional question:<br>**Should AIs play against themselves?** - Whether any AI should play against itself.

It will also output useful information from each match it plays, such as the result and the visualizer link.

## Frequently Asked Questions (FAQs)

**Can I put Cadre folders into the place of the Joueur folders in the file structure and make the tools work?**<br>
Yes.  Simply change the `ADDED_PATH` variable in scripts like this<br>
`ADDED_PATH = '/Joueur.py'`<br>
to<br>
`ADDED_PATH = '/Cadre/Joueur.py'`.

**How can I change the programs to accomodate AIs other than the Python AI?**
I'm not sure exactly but you could code after the<br>
`ChangePath = CalcWorkingDirectory ( self . Number1 , self . Number2 , self . Oppo , self . StartingFolder )`<br>
line in the MyClass class that runs a Makefile or a compilation command.
