class PushBoxGame:
    def __init__(self, map):
        self.map = [row[:] for row in map]
        self.player_row = 0
        self.player_col = 0
        self.targets = []
        self.boxes = []
        self.target_count = 0
        self._is_game_over = False
        self._init_game()

    def _init_game(self):
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                if self.map[row][col] == 'O':
                    self.player_row = row
                    self.player_col = col
                elif self.map[row][col] == 'G':
                    self.targets.append([row, col])
                    self.target_count += 1
                elif self.map[row][col] == 'X':
                    self.boxes.append([row, col])

    def check_win(self):
        box_on_target_count = 0
        for box in self.boxes:
            for target in self.targets:
                if box == target:
                    box_on_target_count += 1
        self._is_game_over = (box_on_target_count == self.target_count)
        return self._is_game_over

    def move(self, direction):
        new_player_row = self.player_row
        new_player_col = self.player_col

        if direction == 'w':
            new_player_row -= 1
        elif direction == 's':
            new_player_row += 1
        elif direction == 'a':
            new_player_col -= 1
        elif direction == 'd':
            new_player_col += 1

        if self._is_valid_move(new_player_row, new_player_col):
            if self._is_box_at(new_player_row, new_player_col):
                box_position = self._get_box_position(new_player_row, new_player_col)
                new_box_row = new_player_row + (new_player_row - self.player_row)
                new_box_col = new_player_col + (new_player_col - self.player_col)

                if self._is_valid_move(new_box_row, new_box_col) and not self._is_box_at(new_box_row, new_box_col):
                    self._move_box(box_position, new_box_row, new_box_col)
                    self.player_row = new_player_row
                    self.player_col = new_player_col
            else:
                self.player_row = new_player_row
                self.player_col = new_player_col

        return self.check_win()

    def _is_valid_move(self, row, col):
        return 0 <= row < len(self.map) and 0 <= col < len(self.map[row]) and self.map[row][col] != '#'

    def _is_box_at(self, row, col):
        for box in self.boxes:
            if box == [row, col]:
                return True
        return False

    def _get_box_position(self, row, col):
        for box in self.boxes:
            if box == [row, col]:
                return box
        return None

    def _move_box(self, box_position, new_row, new_col):
        for i in range(len(self.boxes)):
            if self.boxes[i] == box_position:
                self.boxes[i] = [new_row, new_col]
                break

    def is_game_over(self):
        return self._is_game_over

    def get_player_col(self):
        return self.player_col

    def get_player_row(self):
        return self.player_row

    def get_targets(self):
        return list(self.targets)

    def get_target_count(self):
        return self.target_count

    def get_map(self):
        return self.map

    def get_boxes(self):
        return list(self.boxes)