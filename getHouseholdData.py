import json
from collections import OrderedDict


def get_data_from_file(data):
    """ This function gets data from the BloGPV API.
        It returns a python dictionary called api_data.
        """#
    with open(data) as file:
        household_data = json.load(file)

    return household_data


def get_current_producer_list(household_data):
    """ this function returns a list with meter-Ids of currently
        active producers."""
    producerList = []
    for producer in household_data['producers']:
        producerList.append(producer['meterId'])
    return producerList


def get_current_consumer_list(household_data):
    """ this function returns a list with meter-Ids of currently
        active consumers"""
    consumerList = []
    for consumer in household_data['consumers']:
        consumerList.append(consumer['meterId'])
    return consumerList


def get_current_producer_ids_to_supply_value(household_data):
    """ this function returns a dictionary where active producer Ids are matched
        to their current supply values.
        This dictionary includes all meterIds that are in the API.
        As there are less producers in assetListe.json than in the API
        those have to be removed later
        """
    producerSupply = {}
    currentSupply = []
    for producer in household_data['producers']:
        #this changes entity to kWh= (power/1000)
        producerSupply[producer['meterId']] = (abs(producer['values']['PAvg']))
        currentSupply.append(abs(producer['values']['PAvg']))

    totalCurrentSupply = round(sum(currentSupply),5)
    return producerSupply, totalCurrentSupply


def get_current_consumer_ids_to_demand_value(household_data):
    """   this function returns a dictionary where active consumer Ids are matched
          to their current supply values.
          This dictionary includes all meterIds that are in the API.
          As there are less consumers in assetListe.json those have to be removed
          later
          """
    consumerDemand = OrderedDict()
    currentDemand = []
    for consumer in household_data['consumers']:
        consumerDemand[consumer['meterId']] = -(consumer['values']['PAvg'])
        currentDemand.append(-consumer['values']['PAvg'])

    totalCurrentDemand = round(sum(currentDemand),5)
    return consumerDemand, totalCurrentDemand

