# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 13:47:37 2017

@author: joelb
"""

import random

def execute_algo(algo,vector):
    """executes an algorithm on a boolean input vector
    algorithmes are represented as a list of values that represent terms of a nand algorithm
    for example, if the first three terms are 1,6,17, this means x1=x6 nand x17"""
    v=list(vector)
    i=0
    while(i<len(algo)):
        try:
            z=algo[i]
            x=algo[i+1]
            y=algo[i+2]
            v[z]=1-v[x]*v[y]
        except:
            print(algo)
            1/0
        i=i+3
    return v

def expectation_fitness(algo,input_vector,expected_output):
    """input_vector and expected_output represent an instance of training data
    The goal is to create an algorithm that most matches a list of inputs and corresponding outputs
    This function calculates the contribution of one such pair to the fitness of the algorithm
    Note that if an element of expected_output is -1, this means we do not care about the output of that variable.
    """
    output=execute_algo(algo,input_vector)
    s=0
    for i in range(len(output)):
        if(expected_output[i]!=-1):
            s+=abs(expected_output[i]-output[i])
    return len(output)-s

def fitness(algo,expectation_vector):
    """This function calculates the total fitness of an algorith given an expectation vector
    Each element of said vector is a pair of input and matching expected output vectors
    The closer the algorithm matches their constraints, the higher its fitness"""
    s=0
    for i in range(len(expectation_vector)):
        input_vector=expectation_vector[i][0]
        expected_output=expectation_vector[i][1]
        s+=expectation_fitness(algo,input_vector,expected_output)
    return s
    
def build_fitness_function(expectation_vector):
    """This builds an output function given the expectation_vector
    Returned function can than be passed as-is to the genetic algorithm"""
    def f(algo):
        return fitness(algo,expectation_vector)
    return f
        
    
def initialize_population(population_size,member_size,num_variables):
    pop=[]
    for i in range(population_size):
        member=[]
        for j in range(member_size):
            r=int(num_variables*random.random())
            member.append(min(r,num_variables-1))
        pop.append(member)
    return pop

def fitness_ranking(population,fitness_function):
    """Creates a list of all population members sorted by fitness"""
    fitness_list=[]
    for i in range(len(population)):
        fit=fitness_function(population[i])
        fitness_list.append([fit,population[i]])
    fitness_list.sort()
    return fitness_list

def get_probability_list(population,ranking):
    """Converts the ranking list into a where only the fitnesses are kept
    (with the ordering of elements assumed to be the same)
    This is to efficiently choose a member with a probability proportional to the fitness of each member"""
    prob=[]
    for i in range(len(population)):
        prob.append(ranking[i][0])
    return (prob,sum(prob))

def choose_winner(population,prob):
    """Randomly chooses a winner using probability list"""
    r=prob[1]*random.random()
    s=0
    winner=0
    for i in range(len(prob[0])):
        s+=prob[0][i]
        if(s>=r):
            winner=i
            break
    return winner

def breed(parent1,parent2):
    """Breeds two parents to create a child
    Child is created by randomly choosing which parent will provide each gene"""
    child=[]
    for i in range(len(parent1)):
        if(random.random()>0.5):
            child.append(parent2[i])
        else:
            child.append(parent1[i])
    return child

def mutate(member,nb_var):
    if(random.random()>0.5):
        delta=1
    else:
        delta=-1
    var=int(len(member)*random.random())
    member[var]+=delta
    member[var]=min(max(member[var],0),nb_var-1)
    return member
    

def breed_winners(population,fitness_function,nb_winners,nb_var,mutation_rate):
    """Selects specified number of winners, selected
    with a probability proportional to the fitness of each member
    Note that a member can be selected twice if it has a high probability
    Every one in a while, a child is mutaded"""
    ranking=fitness_ranking(population,fitness_function)
    prob=get_probability_list(population,ranking)
    winners=[]
    for i in range(nb_winners):
        winners.append(choose_winner(population,prob))
    i=0
    children=[]
    while(i+1<nb_winners):
        child=breed(population[winners[i]],population[winners[i+1]])
        if(random.random()<mutation_rate):
            child=mutate(child,nb_var)
        children.append(child)
        i=i+2
    for i in range(len(population)):
        try:
            population[i]=children[i]
        except:
            population[i]=ranking[i][1]
    return population

def average_fitness(population,fitness_function):
    """Calculates average fitness of population for analysis purposes"""
    s=0
    for i in range(len(population)):
        s+=fitness_function(population[i])
    return s/len(population)
        
    
    
        
    
#Example of evolution of a bite-inverting algorithm
#The fitness converges to the maximum of 24 (an algorithm that perfectly implements the inversion)
#Both the algorithm and its fitness are displayed here
expectation_vector=[[[0,0,0],[1,1,1]],[[0,0,1],[1,1,0]],[[0,1,0],[1,0,1]],[[0,1,1],[1,0,0]],[[1,0,0],[0,1,1]],[[1,0,1],[0,1,0]],[[1,1,0],[0,0,1]],[[1,1,1],[0,0,0]]]
f=build_fitness_function(expectation_vector)

pop=initialize_population(100,9,3)
while(True):
    pop=(breed_winners(pop,f,20,3,0.01))
    print(average_fitness(pop,f))
    print(pop[-1])
    print('*************************************')