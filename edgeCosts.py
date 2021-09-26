import ast
import json


def generate_integer_edgeCosts():
    """ this function reads in the json file
        tradingCost_prosumers_to_all_households_tuples.json
        and returns a cost dictionary with integer values
        """

    with open('tradingCost_prosumers_to_all_households_tuples.json') as file:
        api_data = json.load(file)

    total_trading_costs_for_prosumers_to_all_households_dict = ast.literal_eval(api_data)

    integer_total_costs = {}
    for key,value in total_trading_costs_for_prosumers_to_all_households_dict.items():
        integer_total_costs[key]= round(value,5)*10**5

    with open(('integer_tradingCost_tuples.json'), 'w') as file:
        json.dump(str(integer_total_costs), file)

    return 0


def main():

    integer_costs = generate_integer_edgeCosts()

    print(integer_costs)



if __name__ == '__main__':
    main()