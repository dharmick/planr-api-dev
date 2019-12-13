source = 143,
destination = 143

# starting from morning 9 AM
departure_time = 9

# 12 hours (till evening 9 PM)
time_budget = 12

# estimated user ratings
# key = poi id
# value = rating out of 5
user_ratings = {
    143: 3.556,
    2666: 4.007,
    345: 1.2223,
    4221: 4.996,
    23: 0.7445,
}

pois = {
    143:{
        'latitude': 10,
        'longitude': 10,
        'opening_time': 10,
        'closing_time': 18,
        'time_to_spend': 1,
    },
    2666:{
        'latitude': 10,
        'longitude': 15,
        'opening_time': 9,
        'closing_time': 21,
        'time_to_spend': 2,
    },
    345:{
        'latitude': 20,
        'longitude': 20,
        'opening_time': 12,
        'closing_time': 18,
        'time_to_spend': 1.5,
    },
    4221:{
        'latitude': 5,
        'longitude': 50,
        'opening_time': 10,
        'closing_time': 19,
        'time_to_spend': 2,
    },
    23:{
        'latitude': 80,
        'longitude': 80,
        'opening_time': 10,
        'closing_time': 18,
        'time_to_spend': 1,
    }
}

distance_matrix = {
    143: {
        143: 0,
        2666: 0.5,
        345: 1,
        4221: 3,
        23: 5.5,
    },
    2666: {
        143: 0.5,
        2666: 0,
        345: 0.8,
        4221: 2.5,
        23: 5.5,
    },
    345: {
        143: 1,
        2666: 0.8,
        345: 0,
        4221: 2.5,
        23: 4,
    },
    4221: {
        143: 3,
        2666: 2.5,
        345: 2.5,
        4221: 0,
        23: 3.5,
    },
    23: {
        143: 5.5,
        2666: 5.5,
        345: 4,
        4221: 3.5,
        23: 0,
    }
}