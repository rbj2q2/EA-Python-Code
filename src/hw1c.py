# Libraries needed for this program
######################################
import os, sys
import random
import time
import copy
from statistics import mean

# Set the total number of evaluations across all runs
totalEvals=0

class evolString:
    def __init__(self,babyMaking,conf, initDistro):
        # fitness variable initialized before evaluation
        self.fitness = 0
        # address sent to minisat initialized
        self.address="./solvers/minisat/minisat "

        # Self-Adaptivity Parameters
        self.mutation=random.randint(1,100)
        if (recAdapt==True):
            self.recombination=random.randint(1,100)
        else:
            self.recombination=1

        # generate values from seed for this member
        ###################################################

        # If distribution is Uniform Random
        if (initDistro == "Uniform Random"):
            # this bool tells us whether we're using Luby restart sequence, -luby or -no-luby
            self.luby=random.randint(0,1)
            # frequency of decision heuristic choosing a random double in the range [0,1] sent to -rnd-freq
            self.frequency=random.uniform(0,1)
            # Variable acticvity decay: double in [0,1] sent to -var-decay
            self.varDecay=random.uniform(.0000001,.9999999)
            # Clause activity decay: double in [0,1] sent to -cla-decay
            self.claDecay=random.uniform(.0000001,.9999999)
            # Restart interval activity factor, a double in (1, Infinity) sent to -rinc
            self.restart=random.uniform(1.0000001,1000000000)
            # Fraction of wasted memory allowed before grabage collection, double in (0, Infinity) sent to -gc-frac
            self.garbage=random.uniform(.0000001,1000000000)
            # Base interbal restart, any positive integer sent to -rfirst
            self.base=random.randint(1, 1000000000)
            # -ccmin-mode integer value for conflict minimization; 0=none,1=basic,2=deep
            self.conflict=random.randint(0, 2)
            # -phase-saving integer value for phase saving; 0=none,1=limited,2=full
            self.phase=random.randint(0, 2)

        elif (initDistro == "Biased towards small"):
            self.luby=random.expovariate(1.5)
            if (self.luby<1):
                self.luby=0
            else:
                self.luby=1
            self.frequency=random.expovariate(9999)
            if (self.frequency>1):
                self.frequency=1
            elif (self.frequency<0):
                self.frequency=0
            self.varDecay=random.expovariate(4)
            if (self.varDecay>=1):
                self.varDecay=.9999999
            elif (self.frequency<=0):
                self.frequency=.0000001
            self.claDecay=1-1/random.expovariate(4)
            if (self.claDecay>=1):
                self.claDecay=.9999999
            elif (self.claDecay<=0):
                self.claDecay=.0000001
            self.restart=random.expovariate(.0333333333333)
            if (self.restart<=1):
                self.restart=1.0000001
            self.garbage=random.expovariate(.0333333333333)
            if (self.garbage<=0):
                self.garbage=.0000001
            elif (self.garbage<=0):
                self.garbage=.0000001
            self.base=int(round(random.expovariate(0.25)))
            if (self.base<1):
                self.base=1
            elif (self.base<=0):
                self.base=.0000001
            self.conflict=random.expovariate(1)
            if (self.conflict<1):
                self.conflict=0
            elif (self.conflict<2):
                self.conflict=1
            else:
                self.conflict=2
            self.phase=random.expovariate(1)
            if (self.phase<1):
                self.phase=0
            elif (self.phase<2):
                self.phase=1
            else:
                self.phase=2

        elif (initDistro == "Biased towards large"):
            self.luby=1.0-random.expovariate(1.5)
            if (self.luby<1):
                self.luby=0
            else:
                self.luby=1
            self.frequency=1.0-random.expovariate(9999)
            if (self.frequency>1):
                self.frequency=1
            elif (self.frequency<0):
                self.frequency=0
            self.varDecay=1-1/random.expovariate(9999)
            if (self.varDecay>=1):
                self.varDecay=.9999999
            elif (self.varDecay<=0):
                self.varDecay=.0000001
            self.claDecay=1-1/random.expovariate(9999)
            if (self.claDecay>=1):
                self.claDecay=.9999999
            elif (self.claDecay<=0):
                self.claDecay=.0000001
            self.restart=9999999-random.expovariate(.0333333333333)
            if (self.restart<=1):
                self.restart=1.0000001
            print(self.restart)
            self.garbage=9999999-random.expovariate(.0333333333333)
            if (self.garbage<=0):
                self.garbage=.0000001
            self.base=9999999-int(round(random.expovariate(4)))
            if (self.base<1):
                self.base=1
            self.conflict=random.expovariate(.025)
            if (self.conflict<1):
                self.conflict=0
            elif (self.conflict<2):
                self.conflict=1
            else:
                self.conflict=2
            self.phase=random.expovariate(.025)
            if (self.phase<1):
                self.phase=0
            elif (self.phase<2):
                self.phase=1
            else:
                self.phase=2

        # If the random values are kept and recombination isn't used, set the address and evaluate
        if (babyMaking == False):
            if self.luby==0:
                self.address+="-no-luby "
            else:
                self.address+="-luby "
            self.address+="-rnd-freq=" + str(self.frequency) + " "
            self.address+="-var-decay=" + str(self.varDecay) + " "
            self.address+="-cla-decay=" + str(self.claDecay) + " "
            self.address+="-rinc=" + str(self.restart) + " "
            self.address+="-gc-frac=" + str(self.garbage) + " "
            self.address+="-rfirst=" + str(self.base) + " "
            self.address+="-ccmin-mode=" + str(self.conflict) + " "
            self.address+="-phase-saving=" + str(self.phase) + " " + str(conf) + " -cpu-lim=5 -verb=FALSE"
            self.evaluate()

    # Evaluate this object
    def evaluate(self):
        global totalEvals
        # send to miniSAT
        ########################################

        # thisTime is the time before minisat runs
        thisTime=time.time()

        # run the linux command specified in address
        os.system(self.address)
        # fitnessTime is how long it took minisat to run through the values
        fitnessTime=time.time()-thisTime
        totalEvals+=1

        # Evaluate
        #########################################

        # tempFitness is the value of this runs fitness
        self.fitness = 1/fitnessTime

    # Two parents are passed in and recombined. Overwrites the random values, mutates and evaluates
    def breeding(self,mother,father,conf):

        # Recombination
        ######################

        if (recAdapt==True):
            recSum=int(mother.recombination)+int(father.recombination)
        else:
            recSum=2
            # coin flip to determine which parent each gene comes from
            coin=random.randint(1,recSum)
            if (coin<=mother.recombination):
                self.luby=mother.luby
            else:
                self.luby=father.luby
            # coin flip to determine which parent each gene comes from
            coin=random.randint(1,recSum)
            if (coin<=mother.recombination):
                self.frequency=mother.frequency
            else:
                self.frequency=father.frequency
            # coin flip to determine which parent each gene comes from
            coin=random.randint(1,recSum)
            if (coin<=mother.recombination):
                self.varDecay=mother.varDecay
            else:
                self.varDecay=father.varDecay
            # coin flip to determine which parent each gene comes from
            coin=random.randint(1,recSum)
            if (coin<=mother.recombination):
                self.claDecay=mother.claDecay
            else:
                self.claDecay=father.claDecay
            # coin flip to determine which parent each gene comes from
            coin=random.randint(1,recSum)
            if (coin<=mother.recombination):
                self.restart=mother.restart
            else:
                self.restart=father.restart
            # coin flip to determine which parent each gene comes from
            coin=random.randint(1,recSum)
            if (coin<=mother.recombination):
                self.garbage=mother.garbage
            else:
                self.garbage=father.garbage
            # coin flip to determine which parent each gene comes from
            coin=random.randint(1,recSum)
            if (coin<=mother.recombination):
                self.base=mother.base
            else:
                self.base=father.base
            # coin flip to determine which parent each gene comes from
            coin=random.randint(1,recSum)
            if (coin<=mother.recombination):
                self.conflict=mother.conflict
            else:
                self.conflict=father.conflict
            # coin flip to determine which parent each gene comes from
            coin=random.randint(1,recSum)
            if (coin<=mother.recombination):
                self.phase=mother.phase
            else:
                self.phase=father.phase

            # coin flip to determine which parent each gene comes from
            coin=random.randint(1,recSum)
            if (coin<=mother.recombination):
                self.mutation=mother.phase
            else:
                self.mutation=father.phase

            # coin flip to determine which parent each gene comes from
            coin=random.randint(1,recSum)
            if (coin<=mother.recombination):
                self.recombination=mother.phase
            else:
                self.recombination=father.phase

        # Mutation
        ####################
        self.mutator()
        # Adjust address
        ####################
        if self.luby==0:
            self.address+="-no-luby "
        else:
            self.address+="-luby "
        self.address+="-rnd-freq=" + str(self.frequency) + " "
        self.address+="-var-decay=" + str(self.varDecay) + " "
        self.address+="-cla-decay=" + str(self.claDecay) + " "
        self.address+="-rinc=" + str(self.restart) + " "
        self.address+="-gc-frac=" + str(self.garbage) + " "
        self.address+="-rfirst=" + str(self.base) + " "
        self.address+="-ccmin-mode=" + str(self.conflict) + " "
        self.address+="-phase-saving=" + str(self.phase) + " " + str(conf) + " -cpu-lim=5 -verb=FALSE"
        # Evaluate Fitness
        self.evaluate()



    # Mutation
    ############################
    def mutator(self):
        mutationRate=10
        if (mutAdapt==True):
            mutationRate=self.mutation

        # for every gene, generate a random number between 1 and 10. If 10, mutate that gene
        for mutationCount in range (0,11):
            chance=random.randint(1, mutationRate)
            if (chance==mutationRate):
                if (mutationCount==0):
                    # If mutated, flip luby
                    if (self.luby==0):
                        self.luby=1
                    else:
                        self.luby=0
                elif (mutationCount==1):
                    # Obtain a random fraction of the frequency
                    mutationChange=self.frequency/random.randint(2, 10)
                    # Coin flip to determine addition or subtraction
                    coin=random.randint(0,1)
                    # Mutated frequency is original plus/minus a fraction of itself
                    if (coin==0):
                        self.frequency=self.frequency - mutationChange
                        # Ensure the value is within bounds
                        if (self.frequency < 0):
                            self.frequency=0
                    else:
                        self.frequency=self.frequency + mutationChange
                        # Ensure the value is within bounds
                        if (self.frequency > 1):
                            self.frequency=1
                elif (mutationCount==2):
                    # Obtain a random fraction of the varDecay
                    mutationChange=self.varDecay/random.randint(2, 10)
                    # Coin flip to determine addition or subtraction
                    coin=random.randint(0,1)
                    # Mutated varDecay is original plus/minus a fraction of itself
                    if (coin==0):
                        self.varDecay=self.varDecay - mutationChange
                        # Ensure the value is within bounds
                        if (self.varDecay <= 0):
                            self.varDecay=.0000001
                    else:
                        self.varDecay=self.varDecay + mutationChange
                        # Ensure the value is within bounds
                        if (self.varDecay >= 1):
                            self.varDecay=.9999999
                elif (mutationCount==3):
                    # Obtain a random fraction of the claDecay
                    mutationChange=self.claDecay/random.randint(2, 10)
                    # Coin flip to determine addition or subtraction
                    coin=random.randint(0,1)
                    # Mutated claDecay is original plus/minus a fraction of itself
                    if (coin==0):
                        self.claDecay=self.claDecay - mutationChange
                        # Ensure the value is within bounds
                        if (self.claDecay <= 0):
                            self.claDecay=.0000001
                    else:
                        self.claDecay=self.claDecay + mutationChange
                        # Ensure the value is within bounds
                        if (self.claDecay >= 1):
                            self.claDecay=.9999999
                elif (mutationCount==4):
                    # Obtain a random fraction of the restart
                    mutationChange=self.restart/random.randint(2, 10)
                    # Coin flip to determine addition or subtraction
                    coin=random.randint(0,1)
                    # Mutated restart is original plus/minus a fraction of itself
                    if (coin==0):
                        self.restart=self.restart - mutationChange
                        # Ensure the value is within bounds
                        if (self.restart <= 1):
                            self.restart=1.0000001
                    else:
                        self.restart=self.restart + mutationChange
                        # Ensure the value did not overflow
                        if (self.restart < 1):
                            self.restart=1000000000
                elif (mutationCount==5):
                    # Obtain a random fraction of the garbage
                    mutationChange=self.garbage/random.randint(2, 10)
                    # Coin flip to determine addition or subtraction
                    coin=random.randint(0,1)
                    # Mutated garbage is original plus/minus a fraction of itself
                    if (coin==0):
                        self.garbage=self.garbage - mutationChange
                        # Ensure the value is within bounds
                        if (self.garbage <= 1):
                            self.garbage=1.0000001
                    else:
                        self.garbage=self.garbage + mutationChange
                        # Ensure the value did not overflow
                        if (self.garbage < 1):
                            self.garbage=1000000000
                elif (mutationCount==6):
                    # Obtain a random fraction of the base
                    mutationChange=self.base/random.randint(2, 10)
                    # Coin flip to determine addition or subtraction
                    coin=random.randint(0,1)
                    # Mutated base is original plus/minus a fraction of itself
                    if (coin==0):
                        self.base=self.base - mutationChange
                        # Ensure the value is within bounds
                        if (self.base < 1):
                            self.base=1
                    else:
                        self.base=self.base + mutationChange
                        # Ensure the value did not overflow
                        if (self.base < 1):
                            self.base=1000000000
                elif (mutationCount==7):
                    # Only option for a change from a 0 or 2 is 1
                    if ((self.conflict==0) or (self.conflict==2)):
                        self.conflict=1
                    else:
                        # Coin flip to determine addition or subtraction
                        coin=random.randint(0,1)
                        if (coin==0):
                            self.conflict=0
                        else:
                            self.conflict=2
                elif (mutationCount==8):
                    # Only option for a change from a 0 or 2 is 1
                    if ((self.phase==0) or (self.phase==2)):
                        self.phase=1
                    else:
                        # Coin flip to determine addition or subtraction
                        coin=random.randint(0,1)
                        if (coin==0):
                            self.phase=0
                        else:
                            self.phase=2
                elif ((mutationCount==9) and (mutAdapt)):
                    # Obtain a random fraction of the mutation
                    mutationChange=self.mutation/random.randint(2, 10)
                    # Coin flip to determine addition or subtraction
                    coin=random.randint(0,1)
                    # Mutated mutation is original plus/minus a fraction of itself
                    if (coin==0):
                        self.mutation=round(self.mutation - mutationChange)
                        # Ensure the value is within bounds
                        if (self.mutation < 1):
                            self.mutation=1
                    else:
                        self.mutation=self.mutation + mutationChange
                        # Ensure the value did not overflow
                        if (self.mutation > 100):
                            self.mutation=100
                elif ((mutationCount==10) and (recAdapt)):
                    # Obtain a random fraction of the recombination
                    mutationChange=self.recombination/random.randint(2, 10)
                    # Coin flip to determine addition or subtraction
                    coin=random.randint(0,1)
                    # Mutated recombination is original plus/minus a fraction of itself
                    if (coin==0):
                        self.recombination=round(self.recombination - mutationChange)
                        # Ensure the value is within bounds
                        if (self.recombination < 1):
                            self.recombination=1
                    else:
                        self.recombination=self.recombination + mutationChange
                        # Ensure the value did not overflow
                        if (self.recombination > 100):
                            self.recombination=100

def initializePopulation(initializer, initSeed, population, intSeedNum):
    # If we're using a seed to initialize the population
    if (initializer=="True"):
        # Initializer seed is opened and read into population
        file = open(initSeed,"r")
        readPopulation=file.readlines()
        file.close()
        # Add the number of individuals specified in configuration file
        for x in range(0, intSeedNum-1):
            population.append(readPopulation[x])

    # Fill the population
    while (len(population)<mu):

        # Initialize each member and add it to the list
        member=evolString(False,confTrain, initDistro)
        population.append(member)

def log(actionBest, actionAverage, evals, population, mu, testLog):
    global runAverage
    global runBest
    global totalEvals
    global bestTestFitness
    global bestTestAddress
    global bestTestMutation
    global bestTestRecombination
    global stagnantGenerations
    global numTests

    # Calculate average and best fitness
    tempAverage=0
    for x in range(0,mu):
        tempAverage+=population[x].fitness
    tempAverage=tempAverage/mu
    # If we use Average Convergence and the average is decreasing...
    if ((tempAverage<=runAverage+(.05*runAverage)) and (tempAverage>=runAverage-(.05*runAverage)) and (actionAverage=="Restart")):
        # Increment stagnation counter
        stagnantGenerations+=1
    # If we use Best Convergence and the average is decreasing...
    elif ((max(population, key=lambda member: member.fitness).fitness<=runBest) and (actionBest=="Restart")):
        # Increment stagnation counter
        stagnantGenerations+=1
    # Otherwise, reset stagnation counter
    else:
        stagnantGenerations=0
    runAverage=tempAverage
    runBest = max(population, key=lambda member: member.fitness).fitness


    # Update logs
    ###########################

    # Record average and best in the training log
    file = open(trainingLog, "a")
    file.write(str(totalEvals) + "\t" + str(runAverage) + "\t" + str(runBest) + "\n")
    file.close()

    # If the test set is used this time, run the testing set
    if ((totalEvals/100)>=numTests):
        file = open(testLog, "a")

        # Temp variables for finding best fitness individual
        testAddress=""
        tempBest=0
        # Iterate through entire population and get best fitness and its address
        for selected in range (0,mu):
            if (population[selected].fitness > tempBest):
                tempBest=population[selected].fitness
                testAddress=population[selected].address

        # Clock the time for the best individual before and after minisat to get total time
        thisTime=time.time()
        os.system(testAddress)
        fitnessTime=time.time()-thisTime

        #Fitness is inversely proportional to time
        testFitness=1/fitnessTime

        # Record best individual's test run
        file.write(str(totalEvals) + "\t" + str(testFitness) + "\n")
        file.close()

        # Increment the number of test set runs
        numTests+=1

        # If this individual had the best test run, store it
        if (bestTestFitness < testFitness):
            bestTestFitness=testFitness
            bestTestAddress=testAddress
            bestTestMutation=population[selected].mutation
            bestTestRecombination=population[selected].recombination

def checkTermination(nConvergence):
    global totalEvals
    global stillRunning
    global runAverage
    global terminationBest
    global terminationLimit

    # Termination
    ############################

    # Check if the total evaluation limit has been reached
    if (totalEvals >= evalLimit):
        totalEvals=0
        stillRunning=False
    # If termination for stagnant average individual is enabled
    elif (actionAverage == "Terminate"):
        # If the average has stagnated, increment stagnation counter; otherwise, reset
        if ((runAverage <= terminationBest+(.05*terminationBest)) and (runAverage >= terminationBest-(.05*terminationBest))):
            terminationLimit += 1
            # If we've reached the limit of n, terminate
            if (terminationLimit >= nConvergence):
                stillRunning=False
        else:
            terminationLimit = 0
            terminationBest = runAverage
    # If termination for stagnant best individual is enabled
    elif(actionBest == "Terminate"):
        # If the best has stagnated, increment stagnation counter; otherwise, reset
        if (runBest == terminationBest):
            terminationLimit += 1
            # If we've reached the limit of n, terminate
            if (terminationLimit >= nConvergence):
                stillRunning=False
        else:
            terminationLimit = 0
            terminationBest = runBest



if (__name__=="__main__"):
    global totalEvals
    global stillRunning
    global terminationBest
    global terminationLimit
    global runAverage
    global runBest
    global totalEvals
    global bestTestFitness
    global bestTestAddress
    global bestTestMutation
    global bestTestRecombination
    global stagnantGenerations
    global numTests

    # Value for stagnant population termination limit
    terminationLimit=0
    # Value of best used for termination limit
    terminationBest=0

    bestTestAddress=""
    bestTestFitness=0
    bestTestMutation=0
    bestTestRecombination=0

    # read in values from conf file passed into this program as an argument
    #######################################################################

    # This is the linux command of the best solution over all runs
    best=""
    # The value of the highest fitness over all Runs
    maxFitness=0

    # argument is saved as a value and stripped into readable form
    argvalue = sys.argv[1:]
    argvalue=str(argvalue).strip('[\\\'/]')

    # argument file is opened and read into a list
    file = open(argvalue,"r")
    data=file.readlines()
    file.close()

    #     Solution output directory:    '<repo-directory>/solutions/config1.sol'
    solution=((((data[3].split('\'',1))[1]).replace("'","")).replace(" ","")).rstrip()
    #     Training Log Output directory:'logs/training1.log'
    trainingLog=((((data[4].split('\'',1))[1]).replace("'","")).replace(" ","")).rstrip()
    #     Test Log output directory:    'logs/test1.log'
    testLog=((((data[5].split('\'',1))[1]).replace("'","")).replace(" ","")).rstrip()
    #     CNF Set to Train on:          'datasets/set1/training'
    confTrain=((((data[7].split('\'',1))[1]).replace("'","")).replace(" ","")).rstrip()
    #     CNF Set to Test with:         'datasets/set1/testing'
    confTest=((((data[8].split('\'',1))[1]).replace("'","")).replace(" ","")).rstrip()
    #     Number of Runs:               5
    runs=int(((data[10].split(':'))[1]).replace(" ",""))
    #     Number of Evals per Run:      200
    evals=int(((data[12].split(':'))[1]).replace(" ",""))
    #     Timer initilized seed:        False
    timer=(((data[14].split(':'))[1]).replace(" ","")).rstrip()
    #     Initial Survivor Seed:        0
    initSeed=((((data[3].split('\'',1))[1]).replace("'","")).replace(" ","")).rstrip()
    #    Number Selected From Initial Survivor Seed:    (integer)
    intSeedNum=int(((data[20].split(':'))[1]).replace(" ",""))
    #     Initial Distribution:         Uniform Random
    initDistro=(((data[22].split(':'))[1]).lstrip()).rstrip()
    #    Initialization Seed Flag:      ("True" or "False")
    initializer=(((data[25].split(':'))[1]).lstrip()).rstrip()
    #    Parent Selection:                            Fitness Proportional Selection, k-Tournament Selection with replacement
    parentSelection=(((data[27].split(':'))[1]).lstrip()).rstrip()
    #    Survival Strategy:                           Plus, Comma
    survivorStrategy=(((data[31].split(':'))[1]).lstrip()).rstrip()
    #    Survival Selection:                          Truncation, k-Tournament Selection without replacement
    survivorSelection=(((data[33].split(':'))[1]).lstrip()).rstrip()
    #    mu:                                         5
    mu=int(((data[39].split(':'))[1]).replace(" ",""))
    #    lambda:                                      5
    lambdaValue=int(((data[41].split(':'))[1]).replace(" ",""))
    #    tournament size for parent selection:        5
    tournamentSizeP=int(((data[43].split(':'))[1]).replace(" ",""))
    #    tournament size for survival selection:      5
    tournamentSizeS=int(((data[45].split(':'))[1]).replace(" ",""))
    #    Number of evals till termination:            5000
    evalLimit=int(((data[47].split(':'))[1]).replace(" ",""))
    #    n for termination convergence criterion:     5000
    nConvergence=int(((data[49].split(':'))[1]).replace(" ",""))
    #    r to control the r-elitist restart option:   1
    r=int(((data[51].split(':'))[1]).replace(" ",""))
    #    Action on best convergence:       ("Restart", "Terminate" or "Nothing")
    actionBest=(((data[53].split(':'))[1]).replace(" ","")).rstrip()
    #    Action on average convergence:    ("Restart", "Terminate" or "Nothing")
    actionAverage=(((data[55].split(':'))[1]).lstrip()).rstrip()
    #    Number of generations before r restart :            ("True" or "False")
    rGeneration=int(((data[57].split(':'))[1]).replace(" ",""))
    #    Mutation Self-Adaptation Enabled:                   ("True" or "False")
    mutAdapt=(((data[59].split(':'))[1]).replace(" ","")).rstrip()
    #    Recombination Self-Adaptation Enabled:              ("True" or "False")
    recAdapt=(((data[61].split(':'))[1]).replace(" ","")).rstrip()
    #    Restarts Used:                                      ("True" or "False")

    # If we're seeding with time, store time. otherwise, store configuration seed
    if ((timer=="true") or (timer=="True") or (timer==1)):
        rSeed=time.time()
    else:
        rSeed=int(((data[16].split(':'))[1]).replace(" ",""))

    # Seed with chosen seed
    random.seed(rSeed)

    # open the training log file and label it
    file = open(trainingLog, "w")
    file.write("Training Result Log\n")
    file.write("CNF Training File Path:\t" + str(confTrain) + "\n")
    file.write("CNF Testing File Path:\t" + str(confTest) + "\n")
    file.write("Config File Path:\t" + str(argvalue) + "\n")
    file.write("Initialization Seed File Path:\t" + str(initSeed) + "\n")
    file.write("Using Time-Generated Seed:\t" + str(timer) + "\n")
    file.write("Random Seed Value:\t" + str(rSeed) + "\n")

    file.write("\nMu:\t" + str(mu) + "\n")
    file.write("Lambda:\t" + str(lambdaValue) + "\n")
    file.write("R-Elitism Value:\t" + str(r) + "\n")
    file.write("Number of Generations Before Restart:\t" + str(rGeneration) + "\n")
    file.write("Number Selected From Initial Survivor Seed:\t" + str(intSeedNum) + "\n")
    file.write("Initialization Scheme:\t" + str(initDistro) + "\n")
    file.write("Parent Selection Scheme:\t" + str(parentSelection) + "\n")
    file.write("Survivor Selection Scheme:\t" + str(survivorSelection) + "\n")
    file.write("Survivor Strategy Scheme:\t" + str(survivorStrategy) + "\n")
    file.write("Survivor k-Tournament:\t" + str(tournamentSizeS) + "\n")
    file.write("Parent k-Tournament:\t" + str(tournamentSizeP) + "\n")

    file.write("Number of Generations for Convergence:\t" + str(nConvergence) + "\n")
    file.write("Timer Initialized Seed:\t" + str(timer) + "\n")
    file.write("Initialization From Seed Flag:\t" + str(initializer) + "\n")
    file.write("Action on Best Convergence:\t" + str(actionBest) + "\n")
    file.write("Action on Average Convergence:\t" + str(actionAverage) + "\n")
    file.write("Mutation Self-Adaptivity Used:\t" + str(mutAdapt) + "\n")
    file.write("Recombination Self-Adaptivity Used:\t" + str(recAdapt) + "\n")
    file.write("Evaluation Limit:\t" + str(evalLimit) + "\n\n")

    file.write("Number of Runs:\t" + str(runs) + "\n")
    file.write("Evaluations per Run:\t" + str(evals) + "\n\n")
    file.close()


    # open the result log file and label it
    file = open(testLog, "w")
    file.write("Test Result Log\n")
    file.write("CNF Training File Path:\t" + str(confTrain) + "\n")
    file.write("CNF Testing File Path:\t" + str(confTest) + "\n")
    file.write("Config File Path:\t" + str(argvalue) + "\n")
    file.write("Initialization Seed File Path:\t" + str(initSeed) + "\n")
    file.write("Using Time-Generated Seed:\t" + str(timer) + "\n")
    file.write("Random Seed Value:\t" + str(rSeed) + "\n")

    file.write("\nMu:\t" + str(mu) + "\n")
    file.write("Lambda:\t" + str(lambdaValue) + "\n")
    file.write("R-Elitism Value:\t" + str(r) + "\n")
    file.write("Number of Generations Before Restart:\t" + str(rGeneration) + "\n")
    file.write("Number Selected From Initial Survivor Seed:\t" + str(intSeedNum) + "\n")
    file.write("Initialization Scheme:\t" + str(initDistro) + "\n")
    file.write("Parent Selection Scheme:\t" + str(parentSelection) + "\n")
    file.write("Survivor Selection Scheme:\t" + str(survivorSelection) + "\n")
    file.write("Survivor Strategy Scheme:\t" + str(survivorStrategy) + "\n")
    file.write("Survivor k-Tournament:\t" + str(tournamentSizeS) + "\n")
    file.write("Parent k-Tournament:\t" + str(tournamentSizeP) + "\n")

    file.write("Number of Generations for Convergence:\t" + str(nConvergence) + "\n")
    file.write("Timer Initialized Seed:\t" + str(timer) + "\n")
    file.write("Initialization From Seed Flag:\t" + str(initializer) + "\n")
    file.write("Action on Best Convergence:\t" + str(actionBest) + "\n")
    file.write("Action on Average Convergence:\t" + str(actionAverage) + "\n")
    file.write("Mutation Self-Adaptivity Used:\t" + str(mutAdapt) + "\n")
    file.write("Recombination Self-Adaptivity Used:\t" + str(recAdapt) + "\n")
    file.write("Evaluation Limit:\t" + str(evalLimit) + "\n\n")

    file.write("Number of Runs:\t" + str(runs) + "\n")
    file.write("Evaluations per Run:\t" + str(evals) + "\n\n")
    file.close()


    # Run through evolutionary process 'run' number of times
    for run in range (1, runs+1):
        # Set the number of the next test run to 1
        numTests=1

        # Label each run
        file = open(trainingLog, "a")
        file.write("\nRun " + str(run) + "\n")
        file.close()

        file = open(testLog, "a")
        file.write("\nRun " + str(run) + "\n")
        file.close()

        # Initialize population
        ############################
        # Create the population list
        population = []
        # New population used for Comma strategy
        newPopulation = []

        #S et Usage variables
        ############################
        # Initialize count of stagnant generations to 0
        stagnantGenerations=0
        # Initialize variable to remember fitness of most fit individual
        runBest=0
        # Initialize variable to remember average fitness of all individuals
        runAverage=0
        # This value is used for termination condition
        stillRunning=True

        initializePopulation(initializer, initSeed, population, intSeedNum)
        log(actionBest, actionAverage, evals, population, mu, testLog)

        # While the termination condition hasn't been met, continue running
        while (stillRunning):

            # Parent Selection
            ############################
            # Initialize pool of parents
            parentGroup=[]
            for parents in range (0,2*lambdaValue):
                # If we're using fitness proportional selection
                if (parentSelection == "Fitness Proportional Selection"):
                    sumOfF=0
                    for allThePopulation in range (0, mu):
                        # Add all of the population members' fitnesses
                        sumOfF += population[allThePopulation].fitness
                    decision=-1
                    # Randomly choose a floating point number in between 0 and max fitness
                    chosen=random.uniform(0,sumOfF-.0001)
                    # In the unlikely event 0 is chosen, set the decision to the first individual
                    if (chosen==0):
                        decision=0
                    # Subtract each individual's fitness until an individual is reached
                    # Each individual takes away from every other individual's chance of reproduction in this way
                    while (chosen > 0):
                        decision+=1
                        chosen -= population[decision].fitness
                    parentGroup.append(population[decision])
                # If we're using k-tournament selection with replacement
                elif (parentSelection == "k-Tournament Selection with replacement"):
                    # Initialize pool for tournament-round
                    battleRoyalle=[]
                    for k in range (0,tournamentSizeP):
                        # Randomly choose k individuals and add them to pool
                        randChosen=random.randint(0, mu-1)
                        battleRoyalle.append(population[randChosen])
                    # Add the best fitness individual to the parent pool
                    parentGroup.append(max(battleRoyalle, key=lambda member: member.fitness))
                # If we're using Uniform Random parent selection
                elif (parentSelection == "Uniform Random"):
                    # Randomly choose a member of the population
                    randChosen=random.randint(0, len(population)-1)
                    # Add the population member to parent list
                    parentGroup.append(population[randChosen])

            # Make Offspring
            ############################
            for numBabies in range (0,lambdaValue):
                # Recombination
                ############################
                # Make a new individual
                newBaby=evolString(True,confTrain, initDistro)
                # Use two parents to recombine, mutate and evaluate individual
                newBaby.breeding(parentGroup[(numBabies*2)],parentGroup[((numBabies*2)+1)],confTrain)
                # If Plus strategy is used...
                if (survivorStrategy == "Plus"):
                    # Add the individual to the population
                    population.append(newBaby)
                # If Comma strategy is used...
                elif (survivorStrategy == "Comma"):
                    # Add the individual to separate population
                    newPopulation.append(newBaby)

            # Competition
            ############################

            # Initialize a survivor pool
            survivorList=[]

            # Initialize a population used for survivor selection
            testPopulation=[]
            # If Plus strategy is used, set testPopulation equal to it
            if (survivorStrategy == "Plus"):
                testPopulation=list(copy.deepcopy(list(population)))
            elif (survivorStrategy == "Comma"):
                testPopulation=list(copy.deepcopy(list(newPopulation)))

            if (survivorSelection == "Truncation"):
                # Remove the worst individual until population reaches size mu
                while(len(testPopulation) > mu):
                    testPopulation.remove(min(testPopulation, key=lambda member: member.fitness))
                # Set survivor list to remainder
                survivorList=list(copy.deepcopy(list(testPopulation)))
            # If we're using k-tournament without replacement
            elif (survivorSelection == "k-Tournament Selection without replacement"):
                for size in range (0, mu):
                    # Initialize a tournament-round pool
                    battleRoyalle=[]
                    for k in range (0,tournamentSizeP):
                        # Randomly choose tournament participants and add to pool
                        randChosen=random.randint(0, len(testPopulation)-1)
                        battleRoyalle.append(testPopulation[randChosen])
                        # Remove the randomly selected from the population
                        del testPopulation[randChosen]
                    # Add the best fitness indiviual to the survivor list
                    survivorList.append(max(battleRoyalle, key=lambda member: member.fitness))
                    # remove survivor from pool of combatants
                    battleRoyalle.remove(max(battleRoyalle, key=lambda member: member.fitness))
                    while (battleRoyalle):
                        # append all losers to original population and remove them from pool
                        testPopulation.append(battleRoyalle[0])
                        battleRoyalle.remove(battleRoyalle[0])
            # If we're using Uniform Random Survival
            elif (survivorSelection == "Uniform Random"):
                for k in range (0, mu):
                    # Randomly choose a member of the population
                    randChosen=random.randint(0, len(testPopulation)-1)
                    # Add the population member to survivor list
                    survivorList.append(testPopulation[randChosen])
                    # Remove the randomly selected from the population
                    del testPopulation[randChosen]
            # If we're using Fitness Proportional
            elif (survivorSelection == "Fitness Proportional Selection"):
                # Get mu number of individuals
                for x in range (0, mu):
                    sumOfF=0
                    for allThePopulation in range (0, len(testPopulation)-1):
                        # Add all of the population members' fitnesses
                        sumOfF += testPopulation[allThePopulation].fitness
                    decision=-1
                    # Randomly choose a floating point number in between 0 and max fitness
                    chosen=random.uniform(0,sumOfF-.0001)
                    # Subtract each individual's fitness until an individual is reached
                    # Each individual takes away from every other individual's chance of reproduction in this way
                    while (chosen > decision):
                        decision+=1
                        chosen -= testPopulation[decision].fitness
                    # In the unlikely event 0 is chosen, choose the first individual
                    if (decision==-1):
                        decision=0
                    # Add the population member to survivor list
                    survivorList.append(testPopulation[decision])
                    # Remove the randomly selected from the population
                    del testPopulation[decision]
            # the new population is all of the survivors
            population=list(copy.deepcopy(list(survivorList)))

            log(actionBest, actionAverage, evals, population, mu, testLog)

            checkTermination(nConvergence)

            # Restart
            ###########################

            # If we're using restarts
            if ((actionBest=="Restart") or (actionAverage=="Restart")):
                if (stagnantGenerations>=rGeneration):
                    rGeneration=0
                    # Initialize survivor population
                    weSurvive=[]
                    # Remove the worst individual until population reaches size mu
                    while(len(weSurvive) < r):
                        weSurvive.append(max(population, key=lambda member: member.fitness))
                        population.remove(max(population, key=lambda member: member.fitness))

                    population=list(copy.deepcopy(list(weSurvive)))
                    initializePopulation(initializer, initSeed, population, intSeedNum)
                    log(actionBest, actionAverage, evals, population, mu, testLog)
                    checkTermination(nConvergence)


        run+=1


    # Record the best individual in terms of test result across all runs
    solFile = open(solution, 'w')
    tempWord=str(bestTestAddress) + "\nRecombination Weight: " + str(bestTestRecombination) + "\nMutation Rate: " + str(float(1.0/float(bestTestMutation))*100.0) + "%"
    solFile.write(tempWord)
    solFile.close()
