import random

class Map_status():
    def __init__(self):
        self.status = {
            'waiting': ('o', 0),
            "clicked": (' ', 1),
            "unknown": ('?', 2),
            "flag": ('P', 3),
            "miner": ('#', 4),
        }



class game():
    def __init__(self, hard='Normal'):
        status = Map_status()
        self.status_sign = status.status
        self.status_mark = {}
        for key in self.status_sign.keys():
            self.status_mark[self.status_sign[key][1]] = self.status_sign[key][0]

        self.pos = [0, 0]
        self.hard = hard
        self.game_running = False
        self.miner_initialize = False

    def __repr__(self):
        return self.__map_converter()

    def __game_initialize(self):
        if self.hard == 'Normal':
            self.MAP_SIZE = 9
            self.MINERS_SIZE = 10
            self._hidden_map = None
            self.map = [[self.status_sign['waiting'][1] for i in range(self.MAP_SIZE)] for j in range(self.MAP_SIZE)]

        self.game_running = True

    def __drop_miners(self):
        # generate random int for miners position
        dic = set()
        dic.add(self.pos[0]+9*self.pos[1])  # exclude the first clicked position
        up_limit, down_limit = self.MAP_SIZE ** 2 - 1, 0
        count = self.MINERS_SIZE
        while count > 0:
            temp = random.randint(down_limit, up_limit)
            if temp not in dic:
                dic.add(temp)
                count -= 1

        self.miner_initialize = True


        # initialize self.hidden_map
        hidden_map = [[False for i in range(self.MAP_SIZE)] for j in range(self.MAP_SIZE)]
        for num in dic:
            x,y = num % self.MAP_SIZE, num // self.MAP_SIZE
            hidden_map[x][y] = True if [x,y] != self.pos else False

        self._hidden_map = hidden_map

    def __map_converter(self):
        Str = ' |'
        for num in range(self.MAP_SIZE): Str += str(num) + '|'
        Str += '\n'
        for i in range(self.MAP_SIZE):
            Str += str(i) + '|'
            for j in range(self.MAP_SIZE):
                mark = self.status_mark[self.map[i][j]] if isinstance(self.map[i][j], int) else self.map[i][j]
                if [i, j] == self.pos:
                    Str += '\033[1;30;43m' + mark + '\033[0m' + '|'
                else:
                    Str += mark + '|'
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
            elif ch in [' ', ',', '.']:  prev = False
            else:  break
            if len(command) == 2: return command

        player_input = player_input.split()
        if len(player_input) == 0: return ['click']
        if player_input[0] in ['flag', 'unknown']: return [player_input[0]]
        elif player_input[0] in ['Q','q']: return ['Quit']
        else: return []

    def __update(self, player_input):
        command = self.__parse_input(player_input)
        if len(command) == 2:
            self.pos = [int(command[0]), int(command[1])] if int(command[0]) < self.MAP_SIZE and int(command[1]) < self.MAP_SIZE else self.pos
        elif len(command) == 1:
            if command[0] == 'Quit':
                self.game_running = False
                print('Game Quit!')
            elif command[0] in ['flag', 'unknown']:
                print(self.status_sign[command[0]][1])
                self.map[self.pos[0]][self.pos[1]] = self.status_sign[command[0]][1]

            # TODO
            elif command[0] in ['click']:
                self.__click()

    # TODO click the pos
    def __click(self):
        if self.miner_initialize == False:
            self.__drop_miners()
            self.miner_initialize = True

        if self.map[self.pos[0]][self.pos[1]] in [self.status_sign['clicked'][1]]:
            return None
        elif self._hidden_map[self.pos[0]][self.pos[1]]:
            self.map[self.pos[0]][self.pos[1]] = self.status_sign['miner'][1]
            self.show_map()
            self.miner_initialize = False
            self.game_running = False
            print('Game Over')
        else:
            self.map[self.pos[0]][self.pos[1]] = self.status_sign['clicked'][1]
            stack = [[self.pos[0],self.pos[1]]]
            miner_options = {(+1,+1), (+1,-1), (+1,0), (0,+1), (0,-1), (-1, 0), (-1, -1), (-1, +1)}
            next_step_options = {(+1,0), (0,+1), (0,-1), (-1, 0)}
            while stack:
                x,y = stack.pop()
                for option in next_step_options:
                    _x, _y = x+option[0], y+option[1]
                    if 0 <= _x < self.MAP_SIZE and 0 <= _y < self.MAP_SIZE and self.map[_x][_y] not in [self.status_sign['clicked'][1], self.status_sign['miner'][1]]:
                        miner_count = 0
                        explore_next = True
                        # TODO judge the explore series
                        for op in miner_options:
                            op_x, op_y = _x + op[0], _y + op[1]
                            if 0<= op_x < self.MAP_SIZE and 0 <= op_y < self.MAP_SIZE and self._hidden_map[op_x][op_y] == True: miner_count += 1
                            # if 0<= op_x < self.MAP_SIZE and 0 <= op_y < self.MAP_SIZE and isinstance(self.map[op_x][op_y], str): explore_next = True
                        if miner_count == 0 and explore_next == True:
                            stack.append([_x,_y])
                            self.map[_x][_y] = self.status_sign['clicked'][1]
                        elif miner_count > 0:
                            self.map[_x][_y] = str(miner_count)


                        # if miner_count == 0 and



    def game_start(self):
        # start game
        self.__game_initialize()

        print('Input format:\n'
              'num1 num2 -> to change current position\n'
              'flag/unknown -> to mark the position\n'
              'click/ Enter -> to click current position')
        while self.game_running:
            self.show_map()
            player_input = input('Change Position to (ex: 8 8):')
            self.__update(player_input)
