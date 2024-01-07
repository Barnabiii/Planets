# PLANETS
Planets is a personal project using Newton's law

## Setup
### Pygame
The project uses a python library called pygame which you can install by
```bash
pip install pygame
```
### Format of text file
**Explanations:**

The text file is used as an input for the program, by describing the parameters of each planet:

A planet is described on one line between {} with 5 parameters in it, each parameters are defined between parenthesis and they must be defined in this order:
Markup: * position (x,y)
 * velocity (x, y)
 * mass
 * radius
 * color (r,g,b)

**Example:**

```{(250,150):(0.3,0):20:10:(255,255,0)}```

in this example the planet:
Markup: * is positioned at x: 250 and y: 150. 
  * has a velocity of x: 0.3 and y: 0.
  * has a mass of 20.
  * has a radius of 10.
  * is colored purple.
