# Python-Game
This is a basic game I designed in Intro to Computer Science.

## How to use: 
The goal of the game is to not get hit by the missiles. User (jet) can press the up, down, left, and right keys to move within the screen and dodge the missiles. User can also press the spacebar to shoot bullets. The bullets kill any missiles it first hits. This is a fast paced game. Each level is 30 seconds. At every level, the speed of the missiles increases. The user can collide with flying pigs to decrease the speed of the missiles. However, as the levels increase, the flyings pigs will not slow down the speed as much.

## Assumptions:
1. User will not press 2 or more direction keys at the same time.
2. User will not be able to move diagonally nor shoot bullets simultaneously while doing this. 

## Miscellaneous
**Comments:** Overlapping of clouds needs to fixed. They go over a lot of the sprites so sometimes the missile will be hidden under a cloud. Additionally, I need to figure out how to remove the flying pig from the screen once the player collides with it. Instead, it just keeps traveling off the screen. I compensated by adding a noise to allow the user to know/confirm that they’ve collided with the flying pig.

**Resources:**
  * [Pygame Documentation](https://www.pygame.org/docs/ref/sprite.html)
  * [Coding the timer](http://programarcadegames.com/python_examples/f.php?file=timer.py)
