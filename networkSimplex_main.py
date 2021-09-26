import json
import networkx as nx
from getHouseholdData import get_data_from_file, get_current_consumer_ids_to_demand_value, \
    get_current_producer_ids_to_supply_value, get_current_producer_list, get_current_consumer_list
from generateIntegerValues import make_demand_dict_intValues, make_supply_dict_intValues
import ast
from proportionalFairness import excess_demand, excess_supply
import timeit
import json
import os
import csv


def main():

    # -------------load input data ------------------------------
    # load pairsandReduction for tracking of used reductions
    with open('pairsAndReductions.json', 'r') as file:
        pairs_and_reductions = json.load(file)

    # cost dictionary to check for max and min price
    with open('tradingCost_prosumers_to_all_households_nested.json') as file:
        cost_dictionary = json.load(file)

    #  get cost dictionary
    with open('integer_tradingCost_tuples.json') as file:
        payload = json.load(file)
        edgeCostsDictionary = ast.literal_eval(payload)


    #-------------current household data ---------------------------------

    data = '07_01_2020_13_00_00.json'

    household_data = get_data_from_file(data)
    producerSupply, totalCurrentSupply = get_current_producer_ids_to_supply_value(household_data)
    consumerDemand, totalCurrentDemand = get_current_consumer_ids_to_demand_value(household_data)

    integerSupply, totalSupply = make_supply_dict_intValues(producerSupply)
    integerDemand, totalDemand = make_demand_dict_intValues(consumerDemand)

    # numbers of households
    dataPrep_startTime = timeit.default_timer()
    numberOfProducers = len(get_current_producer_list(household_data))
    dataPrep_endTime = timeit.default_timer()
    timeForDataPrep = dataPrep_endTime - dataPrep_startTime
    numberOfConsumers = len(get_current_consumer_list(household_data))

    #just run the algorithm if there is active producers
    if numberOfProducers > 0:

        dataPrep_startTime = timeit.default_timer()

        # set up a graph
        G = nx.DiGraph()

        # add edges to graph
        for producerId in integerSupply.keys():
            for consumerId in integerDemand.keys():
                costs = edgeCostsDictionary[producerId, consumerId]
                G.add_edge(str(consumerId), str(producerId), weight=costs)

        """ check which case is the current one
            totalDemand > totalSupply
            totalDemand < totalSupply"""
        # create a dictionary to store dummy type and dummy value
        dummy = {}

        # ---------------case 1: demand > supply------------------------

        if abs(totalCurrentDemand) > totalCurrentSupply:
            print("-------------------------------------")
            print("current demand exceeds current supply")
            print("-------------------------------------")

            #  dataPrep_startTime = timeit.default_timer()
            proportionalDemand, totalProportionalDemand = excess_demand(consumerDemand, totalCurrentDemand,
                                                                        totalCurrentSupply)

            # check if a dummy household needs to be included to eliminate rounding errors
            if abs(totalProportionalDemand) < totalSupply:
                dummy['type'] = 'propConsumerDummy'
                dummy['value'] = totalSupply - abs(totalProportionalDemand)

            if abs(totalProportionalDemand) > totalSupply:
                dummy['type'] = 'supplyDummy'
                dummy['value'] = abs(totalProportionalDemand) - totalSupply

            #adding producer nodes to the graph
            for producerId, supplyValue in integerSupply.items():
                # add producer node
                G.add_node(producerId, demand=supplyValue)

            #adding consumer nodes to the graph
            for consumerId, demandValue in proportionalDemand.items():
                # add consumer node
                G.add_node(consumerId, demand=demandValue)

            #check if a dummy household was needed
            if len(dummy) > 0:

                #adding dummy nodes and dummy edges to the graph
                if dummy['type'] == 'propConsumerDummy':
                    G.add_node('propConsumerDummy', demand=-dummy['value'])
                    for producerId in integerSupply.keys():
                        G.add_edge('propConsumerDummy', str(producerId), weight=0)

                if dummy['type'] == 'supplyDummy':
                    G.add_node('supplyDummy', demand=dummy['value'])
                    for consumerId in integerDemand.keys():
                        G.add_edge(str(consumerId), 'supplyDummy', weight=0)

            dataPrep_endTime = timeit.default_timer()
            timeForDataPrep = dataPrep_endTime - dataPrep_startTime

            totalTradedWatts = totalCurrentSupply / 1000

        # ---------------case 2: demand < supply------------------------

        if abs(totalCurrentDemand) < totalCurrentSupply:
            print("-------------------------------------")
            print("current supply exceeds current demand")
            print("-------------------------------------")

            proportionalSupply, totalProportionalSupply = excess_supply(producerSupply, totalCurrentDemand,
                                                                        totalCurrentSupply)

            # check if a dummy household needs to be included to eliminate rounding errors
            if totalProportionalSupply < abs(totalDemand):
                dummy['type'] = 'propProducerDummy'
                dummy['value'] = abs(totalDemand) - totalProportionalSupply

            if totalProportionalSupply > abs(totalDemand):
                dummy['type'] = 'demandDummy'
                dummy['value'] = -(totalProportionalSupply - abs(totalDemand))

            #adding producer nodes to the graph
            test = []
            for producerId, supplyValue in proportionalSupply.items():
                G.add_node(producerId, demand=supplyValue)
                test.append(supplyValue)

            #adding consumer nodes to the graph
            test2 = []
            for consumerId, demandValue in integerDemand.items():
                G.add_node(consumerId, demand=demandValue)
                test2.append(demandValue)

            #check if a dummy households was needed
            if len(dummy) > 0:
                #adding dummy nodes and dummy edges to the graph
                if dummy['type'] == 'propProducerDummy':
                    G.add_node('propProducerDummy', demand=dummy['value'])
                    for producerId in integerSupply.keys():
                        G.add_edge(str(consumerId), 'propProducerDummy', weight=0)

                if dummy['type'] == 'demandDummy':
                    G.add_node('demandDummy', demand=dummy['value'])
                    for consumerId in integerDemand.keys():
                        G.add_edge('demandDummy', str(producerId), weight=0)

            dataPrep_endTime = timeit.default_timer()
            timeForDataPrep = dataPrep_endTime - dataPrep_startTime

            totalTradedWatts = abs(totalCurrentDemand / 1000)

        # ---------------case 3: demand = supply------------------------

        if abs(totalCurrentDemand) == totalCurrentSupply:
            print("-------------------------------------")
            print("current supply is equal to current demand")
            print("-------------------------------------")

            dataPrep_startTime = timeit.default_timer()

            #adding producer nodes to the graph
            for producerId, supplyValue in integerSupply.items():
                G.add_node(producerId, demand=supplyValue)

            #adding consumer nodes to the graph
            for consumerId, demandValue in integerDemand.items():
                G.add_node(consumerId, demand=demandValue)

            dataPrep_endTime = timeit.default_timer()
            timeForDataPrep = dataPrep_endTime - dataPrep_startTime

            totalTradedWatts = abs(totalCurrentDemand / 1000)


        # ----------------algorithm---------------------------------------

        start_time = timeit.default_timer()
        flowCost, flowDict = nx.network_simplex(G)
        end_time = timeit.default_timer()

        runtime = end_time - start_time

        kWh = totalSupply * 10 ** (-8)

        print("tadedkWh")
        print(totalTradedWatts)

        totalCosts = flowCost * 10 ** (-13)

        print("reached price per kWh is:")
        print(totalCosts / totalTradedWatts)
        print("algorithm running time is:")
        print(runtime)


        # -----------------data for analysis------------------------------

        def flowDict_to_kWh(flowDict):
            """ function that transforms the returned dictionary
                from the network simplex algorithm into a dictionary
                with unit watts per hour"""
            flowDict_kWh = {}
            for consumerId, values in flowDict.items():
                flowDict_kWh[consumerId] = {}

                if len(values) > 0:
                    for producerId, tradedAmount in values.items():
                        # unit into watt per hour
                        flowDict_kWh[consumerId][producerId] = tradedAmount * 10 ** (-8)

            return flowDict_kWh

        # find tradingpairs
        def get_tradingPairs(flowDict_kWh):
            """ function that returns a list of all household pairs that have been
                found during this time intervall"""
            tradingpairs = []
            tradedAmounts = {}
            for consumerId, values in flowDict_kWh.items():
                if len(values) > 0:
                    for producerId, tradedValue in values.items():
                        if tradedValue > 0:
                            if str(consumerId) != 'propConsumerDummy' and str(
                                    producerId) != 'propProducerDummy':
                                tradingpairs.append((producerId, consumerId))
                                tradedAmounts[(producerId, consumerId)] = tradedValue

            return tradingpairs, tradedAmounts

        flowDict_kWh = flowDict_to_kWh(flowDict)
        tradingpairs, tradedAmounts = get_tradingPairs(flowDict_kWh)


        # load pairsandReduction for tracking of used reductions
        with open('pairsAndReductions.json', 'r') as file:
            pairs_and_reductions = json.load(file)

        #check which framework conditions have been used
        used_reductions = {}
        konz_difference = []
        konz_differencePairs = []
        net_difference = []
        net_differencePairs = []
        localDistancePairs = []
        localDistance = []

        for matchedhouseholds in tradingpairs:
            producerId = matchedhouseholds[0]
            consumerId = matchedhouseholds[1]

            try:
                if pairs_and_reductions[producerId][consumerId]['lokalDistance'] == True:
                    # this if checks if this householdpair is already in the current statistic
                    if matchedhouseholds not in localDistancePairs:
                        localDistancePairs.append(matchedhouseholds)
                        localDistance.append(1)

            except KeyError:
                continue

            try:
                if pairs_and_reductions[producerId][consumerId]['konzessionsDifference'] > 0:
                    # this if checks if this householdpair is already in the current statistic
                    if matchedhouseholds not in konz_differencePairs:
                        konz_differencePairs.append(matchedhouseholds)
                        konz_difference.append(1)
            except KeyError:
                continue

            try:
                if pairs_and_reductions[producerId][consumerId]['netCostDifference'] > 0:
                    # this if checks if this householdpair is already in the current statistic
                    if matchedhouseholds not in net_differencePairs:
                        net_differencePairs.append(matchedhouseholds)
                        net_difference.append(1)
            except KeyError:
                continue

        # used_reduction to track which price reduction have been used
        used_reductions['konzessionsDifference'] = sum(konz_difference)
        used_reductions['netCostDifference'] = sum(net_difference)
        used_reductions['lokalDistance'] = sum(localDistance)
        used_reductions['numberOfPairs'] = len(tradingpairs)

        def get_tradingPrices(tradingpairs):
            """ function that returns a list of all reached trading prices.
                this is needed to check the maximal and minimal reached price"""
            tradingPrices = []

            for matchedhouseholds in tradingpairs:
                producerId = matchedhouseholds[0]
                consumerId = matchedhouseholds[1]
                try:
                    tradingPrices.append(cost_dictionary[producerId][consumerId])

                except KeyError:
                    continue

            return tradingPrices

        # data for analysis
        results = {}
        results['totalCosts'] = abs(totalCosts)
        results['totalTradedWatts'] = totalTradedWatts
        results['averagePrice'] = abs(totalCosts) / totalTradedWatts
        results['maximumPrice'] = max(get_tradingPrices(tradingpairs))
        results['minimumPrice'] = min(get_tradingPrices(tradingpairs))
        results['runningTime'] = runtime
        results['dataPrepTime'] = timeForDataPrep
        results['numberOfProducers'] = numberOfProducers
        results['numberOfConsumers'] = numberOfConsumers
        results['usedReductions'] = used_reductions
        results['timestamp'] = household_data['time']
        results['tradedAmounts'] = tradedAmounts


    else:
        results = {}
        results['totalCosts'] = 0
        results['totalTradedWatts'] = 0
        results['averagePrice'] = 30
        results['maximumPrice'] = 30
        results['minimumPrice'] = 30
        results['runningTime'] = 0
        results['dataPrepTime'] = timeForDataPrep
        results['numberOfProducers'] = numberOfProducers
        results['numberOfConsumers'] = numberOfConsumers
        results['usedReductions'] = 0
        results['timestamp'] = household_data['time']
        results['tradedAmounts'] = 0

    print(results)


if __name__ == '__main__':
    main()


