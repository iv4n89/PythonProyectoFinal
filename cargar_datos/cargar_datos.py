import csv

def csv_to_dict(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        dict_list = []
        for row in reader:
            dict_list.append(row)
    return dict_list

elcsv = csv_to_dict('datos/metacritic_game_info.csv')

games = []

for game in elcsv:
    newgame = {
        'tit_juego': None,
        'plataforma': None,
        'f_publicacion': None
    }
    newgame['tit_juego'] = game['Title']
    newgame['plataforma'] = game['Platform']
    newgame['f_publicacion'] = game['Year']
    games.append(newgame)
    
print(games)