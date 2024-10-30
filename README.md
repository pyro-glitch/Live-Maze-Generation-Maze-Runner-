# Live-Maze-Generation___Maze-Runner
## This project focuses on generating a perfect maze and simultaniously updating it. A perfect maze is where there is always a way to reach the goal cell and there should be no loops (multiple paths) or closures in the maze.

## Initializing the map-
The maze is generated using the 'Origin Shift' algorithm. Each walkable cell on the maze is assigned with a direction (left, right, up, down), while doing so we need to make sure that 
1. The arrows do not point to any other adjacent cells whose arrow is pointing back towards itself.
2. The arrows do not point outside the maze.

Except the last cell which will be our 'origin node', all the cells should have a direction pointing to any adjacent cell. 
The origin node will be our starting point for updating the maze.

## Updating The Map-
The map is updated in as many time as needed, following 3 steps each time:
1. Choose any 1 random cell pointing to the origin node.
2. Make that cell as the new origin node.
3. Set the arrow's direction on the older origin node pointing towards the new origin 


## Here a sample of the gameplay-

https://github.com/user-attachments/assets/916cc985-a6ca-42f7-86db-ec55c20cc416


## A Youtube video a found as a reference-

https://www.youtube.com/watch?v=zbXKcDVV4G0&ab_channel=CaptainLuma
