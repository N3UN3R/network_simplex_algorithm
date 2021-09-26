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
  

# needed files
integer_tradingCost_tuples.json
- contains trading costs for all possible trading pairs within the community

pairsAndReductions.json
- contains the used redutions to calculate the trading costs of household pairs

tradingCost_prosumers_to_all_households_nested.json
- contains a nested dictionary which contains all the trading costs of every
  possible household pair within the community

