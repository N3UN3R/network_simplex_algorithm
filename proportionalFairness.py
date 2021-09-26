from getHouseholdData import get_data_from_file, get_current_consumer_ids_to_demand_value, get_current_producer_ids_to_supply_value
from decimal import Decimal


def excess_demand(consumerDemand, totalCurrentDemand, totalCurrentSupply):
    """ function that insures that every consumer household gets its
        proportional share of the available supply from producer households
        in the community
        input: consumerDemand dictionry, totalCurrentDemand, totalCurrentSupply
        returns: dictionary with proportional shares of demands as integers.
                 input float values are rounded after 5 digits."""

    proportionalDemand = {}
    demand = []

    for consumerId, demandValue in consumerDemand.items():
        #abs is needed as values are negative
        propShare = Decimal((abs(demandValue)/abs(totalCurrentDemand))*totalCurrentSupply)
        roundedProbShare = -int(round(propShare,5)*10**5)
        proportionalDemand[consumerId] = roundedProbShare
        demand.append(roundedProbShare)

    totalProportionalDemand = sum(demand)

    return proportionalDemand, totalProportionalDemand


def excess_supply(producerSupply, totalCurrentDemand, totalCurrentSupply):
    """ function that insures that every consumer household gets its
        proportional share of the available supply from producer households
        in the community
        input: consumerDemand dictionry, totalCurrentDemand, totalCurrentSupply
        returns: dictionary with proportional shares of demands as integers.
                 input float values are rounded after 5 digits."""

    proportionalSupply= {}
    supply = []

    for producerId, supplyValue in producerSupply.items():
        #abs is needed as values are negative
        propShare = Decimal((supplyValue/totalCurrentSupply)*abs(totalCurrentDemand))
        roundedProbShare = int(round(propShare,5)*10**5)
        proportionalSupply[producerId] = roundedProbShare
        supply.append(roundedProbShare)

    totalProportionalSupply = sum(supply)

    return proportionalSupply, totalProportionalSupply


