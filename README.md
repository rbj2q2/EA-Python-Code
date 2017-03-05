## Edits by Robert B. Jones II
The file that is run by the run.sh is located at src/hw1a.py and is written for python 3

The configuration files are located in the configurations directory
     Configuration files have file names in the format res(num)adapt(ad)DS(set).cfg
          num is the number of restarts
          ad is the adaptation used(No: None, Re: Recombination, Mu: Mutation, ReMu: Recombination and Mutation)
          set is the dataset used(1 for dataset 1, 2 for dataset 2)
     Valid configurations for each parameter are listed beneath each parameter
     Strings with quotation marks indicate valid strings; strings without quotation marks indicate valid data types

The training log files are located at logs/training1.log and logs/training2.log

The test log files are located at logs/test1.log and logs/test2.log

The solution files are located at solutions/config1.sol and solutions/config2.sol

The pdf with evaluation plots and statistical analysis is located at plots.pdf
The .tex and .ping files used to create the pdf are included in case you wish to recompile the .pdf

## Coding Standards
Code formatting and style for C, C++, C# and Java should roughly follow [MST's C++ coding guidelines.](http://web.mst.edu/~cpp/cpp_coding_standard_v1_1.pdf)
For python, [PEP8](https://www.python.org/dev/peps/pep-0008/) is ideal.

Because this course is more about the algorithms, we won't strictly hold you to thsese standards as long as your code is readable.
Having said that, we want you to comment and document the core algorithms very well so that it's clear you understand them. (Recombinations, Mutations, Selections, etc...)



## Submission Rules

This repo is your submission for CS5401, Assignment 1A. To submit, all you need to do is push your submission to the master branch on git-classes by the submission deadline.


In order for your submission to count, you **MUST** adhere to the following:

1. Fill out the provided configruation files with the specified parameters, but in any format specific to your program.
    * The configuration that must go in these files will be specified in the files themselves.
2. Leave the provided configuration files in the *configurations* folder and do **not** change their names or paths, only their contents.
3. Change the *run.sh* script to **compile and run** your submission. This script must take a configuration file as an argument.
    * Note: This script must run on the standard MST campus linux machines.
4. Place the log files that you generate in the **logs** directory.
5. Place the solution files that you generate in the **solutions** directory.
6. Commit and push the submission you wish to be graded to git-classes.mst.edu in the **master** branch, by the sumbmission deadline.
    * If for any reason you do/will miss this deadline, please e-mail the TA's ASAP.


Feel free to:
1. Add any files or folders you require.
2. Add other configuration files.
3. Commit, branch, and clone this repo to your heart's desire. (We'll only look at *master* for grading)



## Comipiling and Running
As mentioned above, we will be using the *run.sh* bash script to compile and run your submissions. This script must work on campus linux machines. Therefore, when testing and running your submission, I suggest always using the command:
```
./run.sh <config file>

E.g:

./run.sh configurations/config1.cfg
```

I've also provided you with an example of what this script might look like for a simple C++ compilation and execution, HelloEC. Feel free to reuse parts of this for your own
project, though i suggest instead using a makefile for compilation.


## Minisat - The SAT Solver
To help you in solving your SAT problems, we will give you the SAT solver to configure, binary and source.
This solver is called *minisat* and is located in the *solvers/* directory.
We've configured minisat to take either a directory or file as an input.
When given a directory, minisat will evaluate all CNF files in the directory, in a single run.
Alternatively, you can provide minisat a single CNF file.

The commands to do both:
```
./solvers/minisat/minisat [parameters] <single-file>


./solvers/minisat/minisat [parameters] <directory>
```

One example of using a directory and configuring (some of) minisat's parameters:
```
./solvers/minisat/minisat -luby -rinc=1.5 datasets/set1/
```
This configuration will run minisat on every SAT instance in the datasets/set1 directory, with values specified for one of the boolean parameters (luby) and one of the float parameters (rinc) and leaving all other parameters at default values. For the assignment, you will need to specify values for all of the parameters to be optimized: -luby/-noluby, -rnd-freq, -var-decay, -cla-decay, -rinc, -gc-frac, -rfirst, -ccmin-mode, -phase-saving

For more information on minisat and the configurable parameters, you can run:
```
./solvers/minisat/minisat --help-verb
```
