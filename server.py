import json
rank_list = []

def set_rank():
    global rank_list
    rank_list.sort(key=lambda a : a[0] + a[2] * 5.0)
    rank_list = rank_list[:5]
    with open('data.json', 'w') as json_file:
        json.dump(rank_list, json_file)
    pass

def get_rank():
    global  rank_list
    with open('data.json', 'r') as json_file:
        rank_list = json.load(json_file)
    pass