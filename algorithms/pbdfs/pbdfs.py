# STRUCTURE OF A NODE
#
# nodes = {
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

from pbdfs_input_map import distance_matrix, pois, departure_time, time_budget, user_ratings, source, destination
output = {
    'route': [],
    'happiness': 0
}

# is it possible to go from i to j, get full service at j and still reach destination within time budget?
def sat(i, j, starting_i):
    reaching_j = starting_i + pois[i]['time_to_spend'] + distance_matrix[i][j],
    opening_j = pois[j]['opening_time']
    starting_j = max(reaching_j, opening_j)

    closing_j = pois[j]['closing_time']
    spending_at_j  = pois[j]['time_to_spend']

    reaching_destination = starting_j + pois[j]['time_to_spend'] + distance_matrix[j][destination]

    if(starting_j + spending_at_j < closing_j and reaching_destination < departure_time + time_budget):
        return True
    else:
        return False


# def prefixDFS(ordered_remaining_pois, current_node):


if __name__ == '__main__':
