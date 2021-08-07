from getHouseholdData import get_data_from_file, get_current_consumer_ids_to_demand_value, get_current_producer_ids_to_supply_value, get_current_producer_list, get_current_consumer_list


def make_supply_dict_intValues(producerSupply):
    integerSupply = {}
    for producerId, supplyValue in producerSupply.items():
        integerSupply[producerId] = int((supplyValue*10**5))

    totalSupply = int(sum(integerSupply.values()))

    return integerSupply, totalSupply


def make_demand_dict_intValues(consumerDemand):
    integerDemand = {}
    for consumerId, demandValue in consumerDemand.items():
        integerDemand[consumerId] = int((demandValue*10**5))

    totalDemand = sum(integerDemand.values())

    return integerDemand, totalDemand

