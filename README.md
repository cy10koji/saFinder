# saFinder - (Interesting) Strange Attractor Finder
It is a (interesting) Strange Attractor finder
that runs in the Python mode of Processing.

<p>
<img width="30%" border=1 alt="saFinder_example1" src="https://user-images.githubusercontent.com/95997592/187059138-a9226a51-2386-45f4-8dae-445dfec0e40c.png">
<img width="30%" border=1 alt="saFinder_example2" src="https://user-images.githubusercontent.com/95997592/187059258-ae5fd032-cbc7-4fb4-86af-0c7f76cb82cc.png">
<img width="30%" border=1 alt="saFinder_example3" src="https://user-images.githubusercontent.com/95997592/187059320-fd6c352e-144f-4753-802f-cf14085d6fb9.png">
</p>

## What is “interesting” ?
Everyone has their own definition of “interesting”.
In this program,
based on Sprott's method,
defines "interesting" of a strange attractor
that spreads across the entire screen as much as possible
using Lyapunov exponents and the fractal dimension.

For more information, please refer to his paper (see the below URL) and others:<br />
"Automatic Generation of Strange Attractors", J. C. Sprott,
Comput. & Graphics, Vol. 17, No. 3, pp.325-332, 1993.
[https://sprott.physics.wisc.edu/pubs/paper203.pdf](https://sprott.physics.wisc.edu/pubs/paper203.pdf)

## How to Use it
“Interesting” strange attractor is displayed when the program is executed.
Various operations can be performed by pressing the keys.
Please see below for the details.

### ' ' (space)
Search and display another “interesting" strange attractor.

### 's'
Saves the currently displays the strange attractor as a high-resolution image.
The image will be saved in the same directory where ‘saFinder.pyde' is located.

### '0'- '9', 'a', 'b'
Adjust the ID in Sprott format to fine-tune the strange attractor to be displayed.
Pressing the '0' key changes the first Sprott ID by one;
pressing the '1' key changes the second ID by one.
In the same way, pressing the '9' key changes the 10th ID by one.
And the 'a' and 'b' keys change the 11th and 12th IDs by one, respectively.

### '+', '-'
Changes the direction in which the ID changes
when the numeric keys or the 'a' and 'b' keys are pressed.

### 'p'
Displays the current strange attractor as if it was drawn on paper with ink.

### 'r'
Displays the current strange attractor in additive color mixing mode
(this is the default display mode).

### 't'
Generate the Processing program code that generates the displayed strange attractor.

