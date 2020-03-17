class Board:
    def __init__(self, initial_pos):
        self.board_dict = initial_pos
        self.update_grid()
        self.board_size = 8

    def update_player(self):
        player_format = {"white":[], "black": []}
        for coordinate in self.grid_dict.keys():
            x, y = coordinate
            player, n = self.grid_dict[coordinate]

            if player == 'w':
                player_format["white"].append([int(n), x, y])
            elif player == 'b':
                player_format["black"].append([int(n), x, y])

        self.board_dict = player_format
            

    def update_grid(self):
        grid_format = {}
        #Convert dictionary with players as keys into dictionary with coordinates as keys
        for player in self.board_dict.keys():
            for stack in self.board_dict[player]:
                grid_format[(stack[1], stack[2])] = ''.join([player[0], str(stack[0])])
        
        self.grid_dict = grid_format

    def move(self, n, x, y):
        pass

    def boom(self, x, y):
        self.boom_recursive(x, y)
        self.update_player()
        
    def boom_recursive(self, x, y):
        #Check bounds
        if not (0 <= x < self.board_size and 0 <= y < self.board_size):
            return
        
        #If a token is present, explode!        
        if (x,y) in self.grid_dict.keys():
            del(self.grid_dict[(x,y)])
            
            #Debug line
            print("removed token at" , x, y)

            #Recursive explosion
            for i in range(-1,2):
                for j in range(-1, 2):
                    self.boom(x+i, y+j)

        return