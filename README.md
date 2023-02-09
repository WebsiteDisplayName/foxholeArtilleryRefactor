# foxholeArtilleryRefactor
Developed using DearPyGui <br/>
&emsp;https://github.com/hoffstadt/DearPyGui 

Download CUDA/GPU drivers to use EasyOCR in GPU mode

To use: <br/>
&emsp;cd foxholeArtilleryRefactor root folder <br/>
&emsp;pip install -r requirements.txt <br/>
&emsp;cd into src <br/>
&emsp;run in command line: py view.py

Should use with OnTopReplica for in-game overlay <br/>
&emsp;https://github.com/LorenzCK/OnTopReplica/releases <br/>
&emsp;alt + tab: to enter inputs

Global hotkey keybinds can be altered by changing the keybinds.txt file <br/>
&emsp;column 1: indicates keybind <br/>
&emsp;column 2: indicates which firing solution row is referred to <br/>
&emsp;column 3: target = distST & aziST | gun = distSG & aziSG <br/>
&emsp;&emsp;1,global = changes ST values for all rows <br/>
&emsp;&emsp;2,global = changes spotter to gun values for all rows by first inputting reference values for one spotter to gun  

![Screenshot](images/appAppearance.png)