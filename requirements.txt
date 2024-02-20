This file describes the steps necessary to execute the "reproduce".sh file to produce
the main results of this repository.

1. Make sure you have conda, or preferably mamba installed. See either of the links below
for instructions on installing the program of your choice for your machine.
- conda: https://conda.io/projects/conda/en/latest/user-guide/install/index.html
- mamba: https://mamba.readthedocs.io/en/latest/installation.html

2. Once installed, open the terminal so that your present working directory (pwd)
is the one associated with the location of the local version of this repository on 
your machine.

3. Navigate to the "binder" folder and make sure a file called "environment.yml"
lives there. Run the following command:
- mamba env create -f environment.yal

Once this command has completed, you are ready to run the reproduce.sh script!