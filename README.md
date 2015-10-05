# round-robin-simulator
For Operating System class, I've created a minimal round-robin scheduling simulator with Python. 

This project has two dependencies: CPython interpreter and the Python binding for Qt framework (PyQt v4.8).

You can download CPython 2.7.6 from here: https://www.python.org/download/releases/2.7.6/  
You can download PyQt 4.8 from here https://www.riverbankcomputing.com/software/pyqt/download  

To run the program: Put the content of source folder in some directory, navigate to this folder, be sure that Python is in your PATH and call start-rr-simulator.py.  
$ python -B start-rr-simulator.py

Now, you're probably seeing the Setup Window. I'll explain it a bit:  

- Quantum: For how many cicles each process can lock the processor. When the number of cicles in the current process reaches quantum, the current process goes to the ready queue and the next process in this queue is popped to the processor.
- Maximum life time: Each process has a life time, what means that a process has to be processed N times until it get finished, and this N is the maximum life time. Of course, this number is expressed in cicles.
- Processes per minute: At every 60 seconds some processes will be created. Here you decide how many.
- Chance to be I/O bound: Each process in its creation can be randomly setted to be I/O bound. Here you say what is the chance of a given new process be I/O bound. This number has to be between 0 and 100 (inclusive), meaning 0% and 100%, respectively.
- Duration of each cicle: The simulator will wait for a while between each cicle, because you have to see what's going on in the screen, and here you decide how much it will wait. This number is expressed in milliseconds, and I do not recommend a number lesser than 10 (1/100 second) nor higher than 1000 (1 second).  

For the first shot, I'd recommend these values, from the top to the bottom: 10 20 90 100 100.  

When you click in the Start button, a new window will be shown to you. This new window has two lists, ready and waiting, and some informations. These two lists represents the ready queue and the waiting list, respectively. Other informations are very clear, so I don't have to explain each one.  

When you get tired for seeing the current simulation, you can close the Simulator Window and set up another simulation.
