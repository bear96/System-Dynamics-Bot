# System-Dynamics-Bot
This repository contains the code for the paper "From Text to Map: A System Dynamics Bot for Constructing Causal Loop Diagrams"  

## Installation for Windows

Step 1. If you're installing the required packages on Windows, you need to make sure that you have Python 3.8+ as well as C++ installed in your system. If you do not have Python, you can download Python from their official website. Make sure you have Python on PATH. 
For C++, I have included the .exe file [here](cld\vs_BuildTools.exe). These are important prerequisites to running the code, so please make sure you have them installed before proceeding further. 

Step 2. The next step is to install [Graphviz](cld\stable_windows_10_cmake_Release_x64_graphviz-install-2.46.0-win64.exe). While installing, make sure that you check the option of adding Graphviz to PATH. Sometimes, despite everything, Grpahviz doesn't get added to PATH. You can easily check if Graphviz is on PATH by opening a new terminal and running `dot -v`. If `dot` is not recognized as a command, then you need to manually add Graphviz to PATH. Typically, the directory is something like `C:\Program Files\Graphviz\bin`. Once you have manually added Graphviz to PATH, open a new terminal and run `dot -v` again. You should be able to see the version details now.

Step 3. Run the following command to install Pygraphviz: ```python -m pip install --use-pep517 --config-setting="--global-option=build_ext" --config-setting="--global-option=-IC:\Program Files\Graphviz\include" --config-setting="--global-option=-LC:\Program Files\Graphviz\lib" pygraphviz```. Please verify that the locations `C:\Program Files\Graphviz\include` and `C:\Program Files\Graphviz\lib` are correct before you run this code. 

Step 5. Run `pip install -r requirements.txt` to install the required python packages.

Step 6. Set your OpenAI API key as your environment variable. You can do this easily by typing `set OPENAI_API_KEY=your-api-key` or `$env:OPENAI_API_KEY = "your-api-key"` if you are using Powershell. 

## Installation for Linux/Other Unix based systems

Step 1. Unix based systems already have C++ and Python installed, so you 

