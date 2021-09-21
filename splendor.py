import pandas as pd
import random
from consts import *
from locate import locate
import os

class Card:

    def __init__(self, level_=0, points_=0, color_='white', white_=0, blue_=0, green_=0, red_=0, black_=0, empty_=False):
        self.empty = empty_
        self.level = level_
        self.points = points_
        self.color = color_
        self.cost = {'white':white_, 'blue':blue_, 'green':green_, 'red':red_, 'black':black_}

    def quick_draw(self):
        s = f'{self.color} | {self.points} | '

        for k, v in self.cost.items():
            s += f'{v}{CODES[k]}'

        return s

    def __str__(self):
        s = ''
        s += '+-----------+\n'
        s += '|           |\n'
        s += '+-----------+\n'
        s += '|           |\n'
        s += '|           |\n'
        s += '|           |\n'
        s += '|           |\n'
        s += '|           |\n'
        s += '+-----------+'

        if not self.empty:

            s = locate(s, self.color, 2, 1)
            s = locate(s, self.points, -3, 1)

            strCost = ''
            for k, v in self.cost.items():
                strCost += f'{v} {k}\n'
            s = locate(s, strCost[:-1], 2, 3)

        return s

class Noble:

    def __init__(self, points_=0, white_=0, blue_=0, green_=0, red_=0, black_=0):
        self.points = points_
        self.cost = {'white':white_, 'blue':blue_, 'green':green_, 'red':red_, 'black':black_}

    def __str__(self):
        s = ''
        s += '+-----------+\n'
        s += '|           |\n'
        s += '|           |\n'
        s += '|           |\n'
        s += '|           |\n'
        s += '+-----------+'

        s = locate(s, self.points, -3, 1)

        notZ = 0
        for k, v in self.cost.items():
            strGem = f'{v} {k}\n' if v != 0 else ''
            s = locate(s, strGem, 2, -2-notZ)
            if v != 0:
                notZ += 1

        return s

class Player:

    def __init__(self, name_='John Doe', white_=0, blue_=0, green_=0, red_=0, black_=0, gold_=0):

        self.name = name_

        self.nobles = []
        self.cards = {'white':[], 'blue':[], 'green':[], 'red':[], 'black':[]}
        self.gems = {'white':white_, 'blue':blue_, 'green':green_, 'red':red_, 'black':black_, 'gold':gold_}
        self.reserved = []

    def get_points(self):
        score = 0
        for color in self.cards.values():
            for card in color:
                score += card.points 
        for noble in self.nobles:
            score += noble.points
        return score

    def can_buy(self, card):

        if card == None:
            return None

        cost = card.cost.copy()
        balance = self.gems.copy()

        cost = {key: cost[key] - len(self.cards.get(key, 0)) for key in cost.keys()}
        
        for k in cost:
            if cost[k] < 0:
                cost[k] = 0

        bef = cost.copy()
        cost['gold'] = 0
        for k in cost:
            if cost[k] > balance[k]:
                cost['gold'] += cost[k] - balance[k]
                cost[k] -= cost[k] - balance[k]

        print(bef)
        print(cost)

        return cost if balance['gold'] >= cost['gold'] else None

    def __str__(self):
        s = f'{self.name} ({self.get_points()} points):\nCards: ['
        for k, v in self.cards.items():
            s += f'{len(v)} {k}, '
        s = s[:-2]+']\nGems:  ['
        for k, v in self.gems.items():
            s += f'{v} {k}, '
        s = s[:-2]+f']\n{len(self.nobles)} nobles, {len(self.reserved)} cards reserved'

        return s

class Board:

    def __init__(self, white_=7, blue_=7, green_=7, red_=7, black_=7, gold_=7):

        self.cards = {
            1: [],
            2: [],
            3: []
        }
        self.nobles = []
        self.gems = {'white':white_, 'blue':blue_, 'green':green_, 'red':red_, 'black':black_, 'gold':gold_}

    def __str__(self):
        s = ''

        # Nobles
        for i, noble in enumerate(self.nobles):
            s = locate(s, str(noble) if noble != None else '', i*14, 0)

        # Cards
        for k, v in self.cards.items():
            for i,c in enumerate(v):
                s = locate(s, str(c) if c != None else '', i*15, 7+(3-k)*10)

        # Gems
        s = locate(s, ' Gems \n------', 26, s.count('\n')+2)
        
        startY = s.count('\n')+1
        itemCnt = 0
        for k, v in self.gems.items():
            s = locate(s, f'{v} {k}', 13+(itemCnt%3 * 13), startY+itemCnt//3)
            itemCnt += 1

        return s

class Game:

    def __init__(self):

        self.cards = load_all_cards()
        self.board = Board()
        self.players = [Player(),Player()]
        self.current_player = 0

    def start_game(self):
        self.cards = load_all_cards()
        for k in self.cards:
            random.shuffle(self.cards[k])
        
        self.board = Board()
        
        for k in self.cards:
            for i in range(4):
                self.board.cards[k].append(self.cards[k].pop())
        
        self.players = [Player('Théo'),Player('Mathieu')]
        self.players[0].cards['red'].append(Card())
        self.players[0].cards['red'].append(Card())
        self.players[0].cards['red'].append(Card())
        self.players[0].cards['blue'].append(Card())
        self.players[0].cards['blue'].append(Card())
        self.players[0].cards['white'].append(Card())
        self.players[0].cards['white'].append(Card())
        self.current_player = 0

        self.board.nobles = load_nobles(len(self.players)+1)

    def play_turn(self):

        while 1:
            move = input('Move: ')

            if len(move) < 2:
                continue

            player = self.players[self.current_player]

            if move[0] == 'g':
                gems = move[1:]
                
                if any(c not in CODES for c in gems):
                    continue

                # 3 differents
                if gems == "".join(dict.fromkeys(gems)) and len(gems) == 3:
                    if any(self.board.gems[CODES[gem]] for gem in gems) <= 0:
                        continue

                    for gem in gems:
                        player.gems[CODES[gem]] += 1
                        self.board.gems[CODES[gem]] -= 1
                
                    return

                if gems != "".join(dict.fromkeys(gems)) and len(gems) == 2:
                    if not self.board.gems[CODES[gems[0]]] >= 4:
                        continue

                    for gem in gems:
                        player.gems[CODES[gem]] += 1
                        self.board.gems[CODES[gem]] -= 1

                    return

            if move[0] == 'b' and len(move) == 3:
                if move[1] == 'r':
                    try:
                        card = int(move[2])-1
                    except:
                        print('Error')
                        continue

                    if 0 < card+1 <= len(player.reserved):
                        if (cost := player.can_buy(player.reserved[card])) != None:
                            player.cards[player.reserved[card].color].append(player.reserved.pop(card))
                            
                            for k,v in cost.items():
                                player.gems[k] -= v
                                self.board.gems[k] += v
                                
                            return
                        else:
                            print('Can\'t buy this card') 
                else:
                    try:
                        lvl = int(move[1])
                        card = int(move[2])-1
                    except:
                        print('Error')
                        continue
                    
                    if (cost := player.can_buy(self.board.cards[lvl][card])) != None:
                        player.cards[self.board.cards[lvl][card].color].append(self.board.cards[lvl].pop(card))
                        self.board.cards[lvl].insert(card, self.cards[lvl].pop() if len(self.cards[lvl]) > 0 else None)
                        
                        for k,v in cost.items():
                            player.gems[k] -= v
                            self.board.gems[k] += v
                        
                        return
                    else:
                        print('Can\'t buy this card') 
                
            if move[0] == 'r' and len(move) == 3:
                try:
                    lvl = int(move[1])
                    card = int(move[2])-1
                except:
                    print('Error')
                    continue
                
                if len(player.reserved) < 3 and self.cards[lvl][card] != None:
                    player.reserved.append(self.board.cards[lvl].pop(card))
                    self.board.cards[lvl].insert(card, self.cards[lvl].pop() if len(self.cards[lvl]) > 0 else None)
                    
                    if self.board.gems['gold'] > 0:
                        player.gems['gold'] += 1
                        self.board.gems['gold'] -= 1

                    return

                else:
                    if not len(player.reserved) < 3:
                        print('Can\'t reserve more than 3 cards') 
                    if not self.cards[lvl][card] != None:
                        print('No card found')

    def too_many_gems(self):
        nbGems = sum(self.players[self.current_player].gems.values()) 
        if nbGems > 10:
            while 1:
                gems = input(f'You need to give {nbGems-10} gems back :')
                if any(gem not in CODES for gem in gems) or len(gems) != nbGems-10:
                    continue

                bal = self.players[self.current_player].gems.copy()
                for gem in gems:
                    bal[CODES[gem]] -= 1

                if any(g < 0 for g in bal.values()):
                    continue

                for gem in gems:
                    self.players[self.current_player].gems[CODES[gem]] -= 1
                    self.board.gems[CODES[gem]] += 1
                return

    def check_nobles(self):
        player = self.players[self.current_player]

        toGet = []
        for i in sorted(range(len(self.board.nobles)), reverse=True):
            noble = self.board.nobles[i]
            for color, value in noble.cost.items():
                if len(player.cards[color]) < value:
                    canHave = False
                    break

            if canHave:
                player.nobles.append(self.board.nobles.pop(i))

    def run(self):
        run = True
        while run:

            os.system('cls')

            print(self)

            self.play_turn()
            self.check_nobles()
            self.too_many_gems()

            run = False if any(p.get_points() >= 15 for p in self.players) and self.current_player == 0 else True

            self.current_player = (self.current_player+1)%len(self.players)

    def __str__(self):
        s = str(self.board)        
        
        # Players
        for i, p in enumerate(self.players):
            s = locate(s, str(p), 70, 11+i*6)

        s = locate(s, '+---\n|\n|\n|\n|\n+---', 68, 11+self.current_player*6-1)
        s = locate(s, '---+\n   |\n   | Current player\n   |\n   |\n---+', 125, 11+self.current_player*6-1, ignore=[' '])

        p = self.players[self.current_player]
        s = locate(s, str(p), 0, -1, shifty=2)

        nbRes = len(p.reserved)
        for i in range(nbRes):
            s = locate(s, str(i+1)+'- '+p.reserved[i].quick_draw(), 4, -1, shifty=1)       


        return s+'\n'

def load_all_cards(filename = 'card_list.csv'):

    df = pd.read_csv(filename, delimiter=';')
    
    cards = {1:[], 2:[], 3:[]}

    for index, card in df.iterrows():
        cards[card['Level']].append(Card(card['Level'], card['PV'], card['Gem color'], card['white'], card['blue'], card['green'], card['red'], card['black']))
    
    return cards

def load_nobles(nbNobles, filename = 'noble_list.csv'):

    df = pd.read_csv(filename, delimiter=';')
    
    nobles = []

    for index, card in df.iterrows():
        nobles.append(Noble(card['PV'], card['white'], card['blue'], card['green'], card['red'], card['black']))
    
    return random.sample(nobles, nbNobles)

if __name__ == '__main__':
    
    g = Game()
    g.start_game()
    g.run()

    print("\n\nEnded\n\n")