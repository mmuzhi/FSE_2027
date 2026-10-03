class PushBoxGame:
    def __init__(self, map_data):
        # Deep copy the map to avoid reference issues
        self.map = [row[:] for row in map_data]
        self.player_row = 0
        self.player_col = 0
        self.targets = []
        self.boxes = []
        self.target_count = 0
        self.is_game_over = False
        self.init_game()

    def init_game(self):
        for row_idx, row in enumerate(self.map):
            for col_idx, cell in enumerate(row):
                if cell == 'O':
                    self.player_row = row_idx
                    self.player_col = col_idx
                elif cell == 'G':
                    self.targets.append([row_idx, col_idx])
                    self.target_count += 1
                elif cell == 'X':
                    self.boxes.append([row_idx, col_idx])

    def check_win(self):
        box_on_target_count = 0
        for box in self.boxes:
            if box in self.targets:
                box_on_target_count += 1
        self.is_game_over = (box_on_target_count == self.target_count)
        return self.is_game_over

    def move(self, direction):
        new_player_row, new_player_col = self.player_row, self.player_col

        if direction == 'w':
            new_player_row -= 1
        elif direction == 's':
            new_player_row += 1
        elif direction == 'a':
            new_player_col -= 1
        elif direction == 'd':
            new_player_col += 1

        if self.is_valid_move(new_player_row, new_player_col):
            if self.is_box_at(new_player_row, new_player_col):
                box_pos = self.get_box_position(new_player_row, new_player_col)
                new_box_row = new_player_row + (new_player_row - self.player_row)
                new_box_col = new_player_col + (new_player_col - self.player_col)

                if self.is_valid_move(new_box_row, new_box_col) and not self.is_box_at(new_box_row, new_box_col):
                    self.move_box(box_pos, new_box_row, new_box_col)
                    self.player_row, self.player_col = new_player_row, new_player_col
            else:
                self.player_row, self.player_col = new_player_row, new_player_col

        return self.check_win()

    def is_valid_move(self, row, col):
        return (0 <= row < len(self.map) and 
                0 <= col < len(self.map[row]) and 
                self.map[row][col] != '#')

    def is_box_at(self, row, col):
        return any([box_row, box_col] == [row, col] for box_row, box_col in self.boxes)

    def get_box_position(self, row, col):
        for box in self.boxes:
            if box[0] == row and box[1] == col:
                return box
        return None

    def move_box(self, box_pos, new_row, new_col):
        idx = self.boxes.index(box_pos)
        self.boxes[idx] = [new_row, new_col]

    def is_game_over(self):
        return self.is_game_over

    def get_player_col(self):
        return self.player_col

    def get_player_row(self):
        return self.player_row

    def get_targets(self):
        return self.targets.copy()

    def get_target_count(self):
        return self.target_count

    def get_map(self):
        return self.map

    def get_boxes(self):
        return self.boxes.copy()