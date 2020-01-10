import random

class Map_status():
    def __init__(self):
        self.status = {
            'waiting': ('o', 0),
            "clicked": ('x', 1),
            "unknown": ('?', 2),
            "flag": ('P', 3),
            "miner": ('#', 4),
        }



class game():
    def __init__(self, hard = 'Normal'):
        status = Map_status()
        self.status_sign = status.status
        self.status_mark = {}
        for key in self.status_sign.keys(): self.status_mark [self.status_sign[key][1]] = self.status_sign[key][0]
        self.pos = [0,0]

        self.game_running = False

        if hard == 'Normal':
            self.MAP_SIZE = 9
            self.MINERS_SIZE = 10
            self._hidden_map = self.__drop_miners()
            self.map = [[self.status_sign['waiting'][1] for i in range(self.MAP_SIZE)] for j in range(self.MAP_SIZE)]

    def __repr__(self):
        return self.__map_converter()

    def __drop_miners(self):
        # generate random int for miners position
        dic = set()
        up_limit, down_limit = self.MAP_SIZE **2 - 1, 0
        count = self.MINERS_SIZE
        while count > 0:
            temp = random.randint(down_limit, up_limit)
            if temp not in dic:
                dic.add(temp)
                count -= 1

        # initialize self.hidden_map
        hidden_map = [[False for i in range(self.MAP_SIZE)] for j in range(self.MAP_SIZE)]
        for num in dic:
            x,y = num % (self.MAP_SIZE), num // (self.MAP_SIZE)
            hidden_map[x][y] = True

        return hidden_map

    def __map_converter(self):
        Str = ' |'
        for num in range(self.MAP_SIZE): Str += str(num) + '|'
        Str += '\n'
        for i in range(self.MAP_SIZE):
            Str += str(i) + '|'
            for j in range(self.MAP_SIZE):
                if [i, j] == self.pos:
                    mark = self.status_mark[self.map[i][j]]
                    Str += '\033[1;30;43m' + mark + '\033[0m' + '|'
                else:
                    Str += self.status_mark[self.map[i][j]] + '|'
            Str += "\n"
        return Str

    def show_map(self):
        print( self.__map_converter())

    def __parse_input(self, player_input):
        command = []
        prev = False
        for ch in player_input:
            if ch.isnumeric():
                if prev: command[-1] += ch
                else: command.append(ch)
                prev = True
            elif ch == ' ':
                prev = False
            else: break
            if len(command) == 2: return command

        player_input = player_input.split()
        if player_input[0] in ['flag', 'unknown']: return [player_input[0]]
        elif player_input[0] in ['click','\n']: return ['click']
        elif player_input[0] in ['Q','q']: return ['Quit']
        else: return []

    def __update(self, player_input):
        command = self.__parse_input(player_input)
        if len(command) == 2:
            self.pos = [int(command[0]), int(command[1])]
        elif len(command) == 1:
            if command[0] == 'Quit':
                self.game_running = False
                print('Game Quit!')
            elif command[0] in ['flag', 'unknown']:
                print(self.status_sign[command[0]][1])
                self.map[self.pos[0]][self.pos[1]] = self.status_sign[command[0]][1]
            # TODO
            elif command[0] in ['click', 'Enter']:
                self.click()

    # TODO click the pos
    def __click(self):
        pass


    def game_start(self):
        # start game
        self.game_running = True
        print('Input format:\n'
              'num1 num2 -> to change current position\n'
              'flag/unknown -> to mark the position\n'
              'click/ Enter -> to click current position')
        while self.game_running:
            self.show_map()
            player_input = input('Change Position to (ex: 8 8):')
            self.__update(player_input)
