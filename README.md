### cx4242-hospital-selection-team-35

# Hospital Selection Project

### Description
This is the repository for the final project for Fall 2023's CX4242 Team 35.

The goal of this project is to produce an easily understandable application for
choosing hospitals based on user-weighted criteria. Due to the nature of 
Multi Criteria Decision Making models, the evaluation of this project 
will ultimately be determined by user feedback. 
While there is much research around the factors behind why users choose
certain hospitals, there is much less work on facilitating those choices
in a awy that is best for the user, despite evidence that hospital choice
can improve patient outcomes.

### Installation
To use this application for yourself, clone this repository.  
Alternatively, if you already have the files for this repository (say, if
you are a TA grading these submitted files), skip down to step 3.  
Then, create a [virtual environment](https://virtualenv.pypa.io/en/latest/installation.html).  
The link has a fairly straightforward walkthrough of the steps required to do so, but
they will also be listed here for convenience.  
1. Make sure Python is installed correctly on your computer.  
2. Make sure Git is installed on your computer and clone this repository
(The 'code' button on the top right will allow you to clone in multiple ways.)  
3. Open a terminal, and on the command line, enter the following command:

```
pip install virtualenv
```

4. Once this finishes executing, you now have the ability to create virtual environments
at any time. Navigate to the folder where you cloned your repository/where the
repository files are located.  
5. Create a virtual environment.
On the command line, enter

```
virtualenv venv
```

If this fails, instead use

```
python -m virtualenv venv
```

You should see a folder named 'venv' appear in your repository.  
6. Activate the virtual environment using your command line.  
On Windows:

```
venv\Scripts\activate
```

On Linux/Mac:

```
source venv/bin/activate
```

You should now see a (venv) at the beginning of your command line.  
7. While still on the command line (making sure you are still in the repository folder),
install all required packages with

```
pip install -r requirements.txt
```
  
while in the repository on the command line.  
Afterwards, simply run hospital_selection.py as you would a normal Python file.

```
python hospital_selection.py
```

### Execution
Once your environment is set up, running a demo should be as simple as
running the python file. Feel free to explore the app as you desire. 
Due to the nature of this project, this application is still currently in
"debugging" mode, where saving the [source code](hospital_selection.py)
will automatically reload and update the application.

### Usage Notes
The packages used to create our synthetic dataset for scalability testing
have different dependencies and therefore their own required packages.  
The data_generation_for_testing folder is a 'miniature' repository
with the files necessary to do this.
It is recommended to give these their own virtual environment, following
the steps listed above, but in a separate folder from the rest of the repository.  
The simplest way to do this is just to copy the data_generation_for_testing folder
outside of the folder in which your repository is stored locally, then
navigate to that area and create a virtual environment.  
Additionally, instead of requirements.txt, the file used to install all packages required is

```
pip install -r data_generation_requirements.txt
```

### Datasets
[Hospital Locations](https://hifld-geoplatform.opendata.arcgis.com/datasets/geoplatform::hospitals/explore?showTable=true)  
[Hospital Quality Measures](https://www.kaggle.com/datasets/thedevastator/hospital-care-quality-measures)  
[Customer Satisfaction](https://www.kaggle.com/datasets/abrambeyer/us-hospital-customer-satisfaction-20162020)  

### Contributors
The members of this group are Emily Yang, Melanie Webster, Claire Tran, Justin Lee, and Liam Das.

### Credits
[Emily Yang](https://github.gatech.edu/eyang82)  
[Melanie Webster](https://github.gatech.edu/mwebster33)  
[Claire Tran](https://github.gatech.edu/ctran68)  
[Justin Lee](https://github.gatech.edu/jlee3719)  
[Liam Das](https://github.gatech.edu/ldas8) 
