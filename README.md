# network_simplex_algorithm
 This repository contains an implementation of the network_simplex_algorithm for electricity p2p-matching

edgeCosts.py
- this script transforms the cost dictionary values into integer values which
  is a necessary condition for the network simplex algorithm
  

getHouseholdData.py
- this module gets the current demand and supply values of the producer and 
  consumer households for a netting interval
  

proportionalFairness.py
- this module contains functions which guarantee proportional fairness for
  the different cases. A more specific explanation of how proportional fairness
  is guaranteed could be found in the thesis.
  
 
 generateIntegerValues.py
 - this module contains functions to make the current supply and demand values
   integer values
   
 
 networkSimplex_main.py
- this programm contains the implementation of the network simplex algorithm.
  
