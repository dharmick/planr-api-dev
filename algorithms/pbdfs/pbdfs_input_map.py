source = 1232
destination = 887

# starting from morning 9 AM
departure_time = 9

# 12 hours (till evening 9 PM)
time_budget = 12.5

# estimated user ratings
# key = poi id
# value = rating out of 5
user_ratings = {
    143: 3.556,
    2666: 4.007,
    345: 4.2223,
    4221: 0.996,
    23: 0.7445,
    445: 2.556,
    887: 4.507,
    3: 3.0223,
    666: 1.996,
    1232: 4.7445,
    2: 4.556,
    50: 1.007,
    2231: 4.2223,
    99: 1.996,
    100: 4.7445,
    101: 0.556,
    509: 4.507,
    9997: 3.3223,
    890: 1.996,
    3359: 4.9445,
}

pois = {
    143:{
        'latitude': 10,
        'longitude': 10,
        'opening_time': 10,
        'closing_time': 18,
        'time_to_spend': 1,
        'category': 'Adventure'
    },
    2666:{
        'latitude': 10,
        'longitude': 30,
        'opening_time': 9,
        'closing_time': 21,
        'time_to_spend': 2,
        'category': 'Parks'
    },
    345:{
        'latitude': 50,
        'longitude': 20,
        'opening_time': 12,
        'closing_time': 18,
        'time_to_spend': 1.5,
        'category': 'Adventure'
    },
    4221:{
        'latitude': 5,
        'longitude': 50,
        'opening_time': 10,
        'closing_time': 19,
        'time_to_spend': 2,
        'category': 'Entertainment'
    },
    23:{
        'latitude': 80,
        'longitude': 80,
        'opening_time': 10,
        'closing_time': 18,
        'time_to_spend': 1,
        'category': 'Nature'
    },
    445:{
        'latitude': 45,
        'longitude': 60,
        'opening_time': 10,
        'closing_time': 18,
        'time_to_spend': 1,
        'category': 'Entertainment'
    },
    887:{
        'latitude': 60,
        'longitude': 80,
        'opening_time': 10,
        'closing_time': 18,
        'time_to_spend': 2.5,
        'category': 'Nature'
    },
    3:{
        'latitude': 25,
        'longitude': 50,
        'opening_time': 9,
        'closing_time': 18,
        'time_to_spend': 1.5,
        'category': 'Adventure'
    },
    666:{
        'latitude': 70,
        'longitude': 20,
        'opening_time': 10,
        'closing_time': 18,
        'time_to_spend': 1,
        'category': 'Nature'
    },
    1232:{
        'latitude': 30,
        'longitude': 30,
        'opening_time': 10,
        'closing_time': 19,
        'time_to_spend': 2,
        'category': 'Parks'
    },
    2:{
        'latitude': 15,
        'longitude': 70,
        'opening_time': 10,
        'closing_time': 18,
        'time_to_spend': 1,
        'category': 'Adventure'
    },
    50:{
        'latitude': 45,
        'longitude': 88,
        'opening_time': 9,
        'closing_time': 21,
        'time_to_spend': 2,
        'category': 'Parks'
    },
    2231:{
        'latitude': 24,
        'longitude': 60,
        'opening_time': 12,
        'closing_time': 18,
        'time_to_spend': 1.5,
        'category': 'Adventure'
    },
    99:{
        'latitude': 59,
        'longitude': 59,
        'opening_time': 10,
        'closing_time': 19,
        'time_to_spend': 2,
        'category': 'Entertainment'
    },
    100:{
        'latitude': 30,
        'longitude': 58,
        'opening_time': 10,
        'closing_time': 18,
        'time_to_spend': 1,
        'category': 'Nature'
    },
    101:{
        'latitude': 40,
        'longitude': 88,
        'opening_time': 10,
        'closing_time': 18,
        'time_to_spend': 1,
        'category': 'Entertainment'
    },
    509:{
        'latitude': 90,
        'longitude': 10,
        'opening_time': 10,
        'closing_time': 18,
        'time_to_spend': 2.5,
        'category': 'Nature'
    },
    9997:{
        'latitude': 85,
        'longitude': 30,
        'opening_time': 9,
        'closing_time': 18,
        'time_to_spend': 1.5,
        'category': 'Adventure'
    },
    890:{
        'latitude': 24,
        'longitude': 83,
        'opening_time': 10,
        'closing_time': 18,
        'time_to_spend': 1,
        'category': 'Nature'
    },
    3359:{
        'latitude': 10,
        'longitude': 90,
        'opening_time': 10,
        'closing_time': 19,
        'time_to_spend': 2,
        'category': 'Parks'
    }
}

# distance_matrix = {
#     143: {
#         143: 0,
#         2666: 1,
#         345: 2,
#         4221: 2,
#         23: 5.5,

#         445: 2.556,
#         887: 4.507,
#         3: 3.0223,
#         666: 1.996,
#         1232: 4.7445,
#     },
#     2666: {
#         143: 1,
#         2666: 0,
#         345: 0.8,
#         4221: 2.5,
#         23: 5.5,

#         445: 2.556,
#         887: 4.507,
#         3: 3.0223,
#         666: 1.996,
#         1232: 4.7445,
#     },
#     345: {
#         143: 2,
#         2666: 0.8,
#         345: 0,
#         4221: 2.5,
#         23: 4,

#         445: 2.556,
#         887: 4.507,
#         3: 3.0223,
#         666: 1.996,
#         1232: 4.7445,
#     },
#     4221: {
#         143: 3,
#         2666: 2.5,
#         345: 2.5,
#         4221: 0,
#         23: 3.5,

#         445: 2.556,
#         887: 4.507,
#         3: 3.0223,
#         666: 1.996,
#         1232: 4.7445,
#     },
#     23: {
#         143: 5.5,
#         2666: 5.5,
#         345: 4,
#         4221: 3.5,
#         23: 0,

#         445: 2.556,
#         887: 4.507,
#         3: 3.0223,
#         666: 1.996,
#         1232: 4.7445,
#     },
#     445: {
#         143: 5.5,
#         2666: 5.5,
#         345: 4,
#         4221: 3.5,
#         23: 0,

#         445: 2.556,
#         887: 4.507,
#         3: 3.0223,
#         666: 1.996,
#         1232: 4.7445,
#     },
#     887: {
#         143: 5.5,
#         2666: 5.5,
#         345: 4,
#         4221: 3.5,
#         23: 0,

#         445: 2.556,
#         887: 4.507,
#         3: 3.0223,
#         666: 1.996,
#         1232: 4.7445,
#     },
#     3: {
#         143: 5.5,
#         2666: 5.5,
#         345: 4,
#         4221: 3.5,
#         23: 0,

#         445: 2.556,
#         887: 4.507,
#         3: 3.0223,
#         666: 1.996,
#         1232: 4.7445,
#     },
#     666: {
#         143: 5.5,
#         2666: 5.5,
#         345: 4,
#         4221: 3.5,
#         23: 0,

#         445: 2.556,
#         887: 4.507,
#         3: 3.0223,
#         666: 1.996,
#         1232: 4.7445,
#     },
#     1232: {
#         143: 5.5,
#         2666: 5.5,
#         345: 4,
#         4221: 3.5,
#         23: 0,

#         445: 2.556,
#         887: 4.507,
#         3: 3.0223,
#         666: 1.996,
#         1232: 4.7445,
#     }
# }