# STRUCTURE OF TREE
#
# tree = {
#     'ABC': {
#         'happiness': 23,
#         'categories': ['adventure', 'parks'],
#         'feasible_routes': [
#             {
#                 'route': ['B', 'A', 'C'],
#                 'ending_poi': 'C',
#                 'starting_time_of_ending_poi': 10
#             },
#             {
#                 'route': ['A', 'C', 'B'],
#                 'ending_poi': 'B',
#                 'starting_time_of_ending_poi': 12
#             },
#         ]
#     }
# }

import copy
from pprint import pprint
import math
# import matplotlib.pyplot as plt
# from pbdfs_input_map import pois, departure_time, time_budget, user_ratings, source, destination

output = {
    'route': [],
    'happiness': 0,
    'starting_time_of_ending_poi': 0,
}

tree = {}


# is it possible to go from i to j, get full service at j and still reach destination within time budget?
def sat(i, j, starting_i, user_ratings, pois, source, destination, departure_time, time_budget, distance_matrix):
    # print("in sat with ",i,j,starting_i)
    starting_i = float(starting_i)
    reaching_j = starting_i + pois[i]['time_to_spend'] + distance_matrix[i][j]
    opening_j = pois[j]['opening_time']
    starting_j = max(reaching_j, opening_j)

    closing_j = pois[j]['closing_time']
    spending_at_j  = pois[j]['time_to_spend']

    reaching_destination = starting_j + pois[j]['time_to_spend'] + distance_matrix[j][destination]
    # print("calc reaching j", )
    # print("reaching j and opening j", reaching_j, opening_j)
    # print("start and spend at j",starting_j, spending_at_j)
    # print("in sat comparing", starting_j + spending_at_j, closing_j, reaching_destination, departure_time + time_budget)
    if(starting_j + spending_at_j < closing_j and reaching_destination < departure_time + time_budget):
        return True
    else:
        return False

# prefix of element i in set j
def prefix(i, j):
    res = []
    for element in j:
        if element != i:
            res.append(element)
        else:
            return res


# main recursive algo
def prefixDFS(ordered_remaining_pois, current_node, user_ratings, pois, source, destination, departure_time, time_budget, distance_matrix):
    # print("\n\n*************************\n\n")
    # print('tree is ', tree)
    # print("ordered remainin pois: ", ordered_remaining_pois)
    # print("current node: ", current_node)
    for poi in ordered_remaining_pois:
        child_ordered_remaining_pois = prefix(poi, ordered_remaining_pois)
        child_node = copy.copy(current_node)
        child_node.append(poi)

        # print("poi: ", poi)

        # print("child rem nodes: ", child_ordered_remaining_pois),
        # print("child node: ", child_node)

        if len(child_node) == 1:
            if sat(source, poi, departure_time, user_ratings, pois, source, destination, departure_time, time_budget, distance_matrix):
                # print("\n\n sat returned true\n\n")
                node = {}
                node['happiness'] = user_ratings[poi]
                node['categories'] = [pois[poi]['category']]
                node['feasible_routes'] = [
                    {
                        'route': [source, poi],
                        'ending_poi': poi,
                        'starting_time_of_ending_poi': max(departure_time + distance_matrix[source][poi], pois[poi]['opening_time'])
                    }
                ]
                tree["*".join(str(x) for x in child_node)] = node
                prefixDFS(child_ordered_remaining_pois, child_node, user_ratings, pois, source, destination, departure_time, time_budget, distance_matrix)

        else:
            for k in child_node:
                temp_child_node = copy.copy(child_node)
                temp_child_node.remove(k)

                if "*".join(str(x) for x in temp_child_node) in tree:
                    for l in tree["*".join(str(x) for x in temp_child_node)]['feasible_routes']:
                        if sat(l['ending_poi'], k, l['starting_time_of_ending_poi'], user_ratings, pois, source, destination, departure_time, time_budget, distance_matrix):
                            child_node_string = "*".join(str(x) for x in child_node)
                            temp_child_node_string = "*".join(str(x) for x in temp_child_node)

                            new_happiness = tree[temp_child_node_string]['happiness'] + user_ratings[k]
                            new_categories = copy.copy(tree[temp_child_node_string]['categories'])
                            new_categories.append(pois[k]['category'])
                            new_starting_time_of_ending_poi = max(l['starting_time_of_ending_poi'] + pois[l['ending_poi']]['time_to_spend'] + distance_matrix[l['ending_poi']][k], pois[k]['opening_time'])
                            new_path = copy.copy(l['route'])
                            new_path.append(k)
                            new_route = {
                                    'route': new_path,
                                    'ending_poi': k,
                                    'starting_time_of_ending_poi': new_starting_time_of_ending_poi
                                }

                            if child_node_string in tree:
                                tree[child_node_string]['happiness'] = new_happiness
                                tree[child_node_string]['categories'] = new_categories
                                tree[child_node_string]['feasible_routes'].append(new_route)
                            else:
                                new_node = {}
                                new_node['happiness'] = new_happiness
                                new_node['categories'] = new_categories
                                new_node['feasible_routes'] = [new_route]
                                tree[child_node_string] = new_node

                            if (new_happiness > output['happiness']) or \
                            (new_happiness == output['happiness'] and \
                            new_starting_time_of_ending_poi + pois[k]['time_to_spend'] + distance_matrix[k][destination] < \
                            output['starting_time_of_ending_poi'] + pois[output['route'][-1]]['time_to_spend'] + distance_matrix[output['route'][-1]][destination]):
                                output['route'] = new_path
                                output['happiness'] = new_happiness
                                output['starting_time_of_ending_poi'] = new_starting_time_of_ending_poi


            if "*".join(str(x) for x in temp_child_node) in tree:
                prefixDFS(child_ordered_remaining_pois, child_node, user_ratings, pois, source, destination, departure_time, time_budget, distance_matrix)
    # print("ended")


def showPlot(user_ratings, pois, source, destination, departure_time, time_budget, distance_matrix):
    x = []
    y = []
    text = []
    for poi in pois:
        x.append(pois[poi]['longitude'])
        y.append(pois[poi]['latitude'])
        text.append(str(poi) + " (" + str(user_ratings[poi]) + ")")

    fig, ax = plt.subplots()
    ax.scatter(x, y)
    for i, txt in enumerate(text):
        ax.annotate(txt, (x[i], y[i]))

    line_x = []
    line_y = []
    for poi in output['route']:
        line_x.append(pois[poi]['longitude'])
        line_y.append(pois[poi]['latitude'])
    line_x.append(pois[destination]['longitude'])
    line_y.append(pois[destination]['latitude'])
    plt.plot(line_x, line_y)
    plt.show()


def decimalToTime(time):
    hours = str(int(time)).zfill(2)
    minutes = str(int((time*60) % 60)).zfill(2)
    return hours + ":" + minutes




def get_pbdfs_schedule(user_ratings, pois, source, destination, departure_time, time_budget, distance_matrix):
    global output
    output = {
        'route': [],
        'happiness': 0,
        'starting_time_of_ending_poi': 0,
    }

    global tree
    tree = {}

    places = list(user_ratings.keys())

    # for from_place in places:
    #     distance_matrix[from_place] = {}
    #     for to_place in places:
    #         distance_matrix[from_place][to_place] =  math.sqrt((pois[from_place]['latitude'] - pois[to_place]['latitude'])**2 + \
    #         (pois[from_place]['longitude'] - pois[to_place]['longitude'])**2) / 20
    # pprint(distance_matrix)


    # if source in places:
    #     places.remove(source)
    # if destination in places:
    #     places.remove(destination)


    sorted_places = sorted(places, key=user_ratings.get, reverse=True)
    sorted_places = sorted_places[:20]
    prefixDFS(sorted_places, [], user_ratings, pois, source, destination, departure_time, time_budget, distance_matrix)
    output['route'].append(destination)

    schedule = []
    time = departure_time

    for index, poi in enumerate(output['route']):
        # print("*****************", poi)
        item_at_poi = {}
        item_at_poi['type'] = 'at_poi'
        item_at_poi['place_id'] = poi
        item_at_poi['place_name'] = pois[poi]['name']
        item_at_poi['latitude'] = float(pois[poi]['latitude'])
        item_at_poi['longitude'] = float(pois[poi]['longitude'])
        item_at_poi['starting_time'] = decimalToTime(time)

        if poi != source and poi != destination:
            item_at_poi['average_rating'] = pois[poi]['average_rating']
            item_at_poi['ending_time'] = decimalToTime(time + pois[poi]['time_to_spend'])
            time += pois[poi]['time_to_spend']
        schedule.append(item_at_poi)

        if poi != destination:
            item_between_poi = {}
            item_between_poi['type'] = 'between_poi'
            item_between_poi['travel_mode'] = 'car'
            item_between_poi['starting_time'] = decimalToTime(time)
            item_between_poi['ending_time'] = decimalToTime(time + distance_matrix[poi][output['route'][index+1]])
            time += distance_matrix[poi][output['route'][index+1]]
            schedule.append(item_between_poi)

    # pprint(tree)
    # print(output)
    # pprint(schedule)
    return schedule




# if __name__ == '__main__':

#     get_pbdfs_schedule(user_ratings, pois, source, destination, departure_time, time_budget, distance_matrix)

#     showPlot()