# From Text to Map: A System Dynamics Bot for Constructing Causal Loop Diagrams

This repository includes the code and supplementary materials for the paper: **From Text to Map: A System Dynamics Bot for Constructing Causal Loop Diagrams** ([arXiv link](https://arxiv.org/abs/2402.11400)) ([Paper](https://doi.org/10.1002/sdr.1782))

>**Abstract:** We introduce and test the System Dynamics Bot, a computer program leveraging a large language model to automate the creation of causal loop diagrams from textual data. To evaluate its performance, we ensembled two distinct databases. The first dataset includes 20 causal loop diagrams and associated texts sourced from system dynamics literature. The second dataset comprises responses from 30 participants to the Lake Urmia Vignette, along with causal loop diagrams coded by three system dynamics modelers. The bot uses textual data and successfully identifies approximately sixty percent of the links between variables and feedback loops in both datasets. This paper outlines our approach, provides examples, and presents evaluation results.
>We discuss encountered challenges and implemented solutions in developing the System Dynamics Bot. The Bot can facilitate extracting mental models from textual data and improve model building processes. Moreover, the two datasets can serve as a testbed for similar programs.

An OpenAI API key is required to use this application. A user can [create an account](https://platform.openai.com/login) with OpenAI, navigate to the [API key page](https://platform.openai.com/account/api-keys) and click on "Create new secret key", optionally naming the key. Make sure that you have [GPT-4 access](https://help.openai.com/en/articles/7102672-how-can-i-access-gpt-4), and **save your API key somewhere safe and do not share it with anyone.**

## Update
Since some people have been having trouble with running the SD Bot, I have created a very simple [application](https://github.com/bear96/System-Dynamics-Bot/blob/main/cld/dist/SD-Bot.exe) to run on Windows. Just download it and double click on the .exe file to get started. If you are a developer wanting to modify this program, you are free to follow the steps I have outlined below.

## Installation for Windows

### Step 1: Install Python and C++

Ensure that you have Python 3.8+ and C++ installed. If you do not have Python, you can download it from the [official website](https://www.python.org/). Make sure Python is added to your PATH.

For C++, I have included the executable file [here](cld/vs_BuildTools.exe). These are essential prerequisites, so ensure they are installed before proceeding.

### Step 2: Install Graphviz

Download and install [Graphviz](cld/stable_windows_10_cmake_Release_x64_graphviz-install-2.46.0-win64.exe). During installation, ensure the option to add Graphviz to PATH is checked. Verify Graphviz is on PATH by running `dot -V` in a new terminal. If `dot` is not recognized, manually add Graphviz to PATH. Typically, the directory is something like `C:\Program Files\Graphviz\bin`. After adding it, run `dot -V` again to confirm.

### Step 3: Install Pygraphviz

Run the following command to install Pygraphviz:
```bash
python -m pip install --use-pep517 --config-setting="--global-option=build_ext" --config-setting="--global-option=-IC:\Program Files\Graphviz\include" --config-setting="--global-option=-LC:\Program Files\Graphviz\lib" pygraphviz
```
Please verify that the locations `C:\Program Files\Graphviz\include` and `C:\Program Files\Graphviz\lib` are correct before you run this code. 

### Step 4.  Install Required Python Packages
Run `pip install -r requirements.txt` to install the required python packages.

### Step 5. Set OpenAI API Key
Set your OpenAI API key as your environment variable. You can do this easily by typing `set OPENAI_API_KEY=your-api-key` or `$env:OPENAI_API_KEY = "your-api-key"` if you are using Powershell. 

## Installation for Linux/Other Unix based systems

### Step 1. Install Graphviz
Unix based systems already have C++ and Python installed, so you can skip those installation processes. You can install Graphviz by running `sudo apt-get install graphviz graphviz-dev`. As before, please ensure that Graphviz installation directory is on PATH. In Linux systems, it usually gets added to PATH by default.

### Step 2. Install Required Python Packages
The next step is installing the required packages by running `pip install -r requirements.txt`. Please install pygraphviz separately by running `pip install pygraphviz`. 

### Step 3. Set OpenAI API Key
Set your OpenAI API key as your environment variable by running `export OPENAI_API_KEY="your_api_key"`. You can verify that you've added the API key by running `printenv OPENAI_API_KEY`. 

Remember that this environment variable exists only during this session so you have to do this every time you want to run the code. I'd recommend not adding the API key permanently due to security concerns.

## Running the System Dynamics Bot

You can run the System Dynamics Bot by navigating to the cld folder and running `python main.py --arg1 --arg2`. 

The list of arguments are given below:

- --verbose: Specifying this flag allows you to see all the inner workings of the System Dynamics Bot
- --diagram: Specifying this flag tells the System Dynamics Bot to actually create the CLD diagram and saves it in the current working directory. 


## Citation
If you use this code, please cite the following:

Hosseinichimeh, N., Majumdar, A., Williams, R., & Ghaffarzadegan, N. (2024). From Text to Map: A System Dynamics Bot for Constructing Causal Loop Diagrams. ArXiv, abs/2402.11400.

```bibtex
@article{https://doi.org/10.1002/sdr.1782,
author = {Hosseinichimeh, Niyousha and Majumdar, Aritra and Williams, Ross and Ghaffarzadegan, Navid},
title = {From text to map: a system dynamics bot for constructing causal loop diagrams},
journal = {System Dynamics Review},
volume = {n/a},
number = {n/a},
pages = {e1782},
doi = {https://doi.org/10.1002/sdr.1782},
url = {https://onlinelibrary.wiley.com/doi/abs/10.1002/sdr.1782},
eprint = {https://onlinelibrary.wiley.com/doi/pdf/10.1002/sdr.1782},
abstract = {Abstract We introduce and test the System Dynamics Bot, a computer program leveraging a large language model to automate the creation of causal loop diagrams from textual data. To evaluate its performance, we ensembled two distinct databases. The first dataset includes 20 causal loop diagrams and associated texts sourced from the system dynamics literature. The second dataset comprises responses from 30 participants to a vignette, along with causal loop diagrams coded by three system dynamics modelers. The bot uses textual data and successfully identifies approximately 60\% of the links between variables and feedback loops in both datasets. This article outlines our approach, provides examples, and presents evaluation results. We discuss encountered challenges and implemented solutions in developing the System Dynamics Bot. The bot can facilitate extracting mental models from textual data and improve model-building processes. Moreover, the two datasets can serve as a test-bed for similar programs. © 2024 The Author(s). System Dynamics Review published by John Wiley \& Sons Ltd on behalf of System Dynamics Society.}
}
```

## Questions

If you have any questions about the code, please feel free to open an issue in this repository. 

## License

This code is provided for non-commercial use only. You are free to use, modify, and distribute the code for personal or educational purposes. However, any commercial use is strictly prohibited without prior written consent as stated in [Attribution-NonCommercial 4.0 International](LICENSE). 
