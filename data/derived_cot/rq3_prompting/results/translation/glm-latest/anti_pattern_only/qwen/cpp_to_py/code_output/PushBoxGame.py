from typing import List, Optional, Tuple


class PushBoxGame:
    def __init__(self, map: Optional[List[str]] = None):
        if map is None:
            map = []
        self.map: List[str] = map
        self.player_row: int = 0
        self.player_col: int = 0
        self.targets: List[Tuple[int, int]] = []
        self.boxes: List[Tuple[int, int]] = []
        self.target_count: int = 0
        self._is_game_over: bool = False
        self.init_game()

    def gat_map(self) -> List[str]:
        return list(self.map)

    def is_game_over(self) -> bool:
        return self._is_game_over

    def get_player_col(self) -> int:
        return self.player_col

    def get_player_row(self) -> int:
        return self.player_row

    def get_targets(self) -> List[Tuple[int, int]]:
        return list(self.targets)

    def get_boxes(self) -> List[Tuple[int, int]]:
        return list(self.boxes)

    def get_target_count(self) -> int:
        return self.target_count

    def init_game(self) -> None:
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                if self.map[row][col] == 'O':
                    self.player_row = row
                    self.player_col = col
                elif self.map[row][col] == 'G':
                    self.targets.append((row, col))
                    self.target_count += 1
                elif self.map[row][col] == 'X':
                    self.boxes.append((row, col))

    def check_win(self) -> bool:
        box_on_target_count = 0
        for box in self.boxes:
            if box in self.targets:
                box_on_target_count += 1
        if box_on_target_count == self.target_count:
            self._is_game_over = True
        return self._is_game_over

    def move(self, direction: str) -> bool:
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

        if self.map[new_player_row][new_player_col] != '#':
            if (new_player_row, new_player_col) in self.boxes:
                new_box_row = new_player_row + (new_player_row - self.player_row)
                new_box_col = new_player_col + (new_player_col - self.player_col)

                if self.map[new_box_row][new_box_col] != '#':
                    box = (new_player_row, new_player_col)
                    if box in self.boxes:
                        self.boxes.remove(box)
                    self.boxes.append((new_box_row, new_box_col))
                    self.player_row = new_player_row
                    self.player_col = new_player_col
            else:
                self.player_row = new_player_row
                self.player_col = new_player_col

        return self.check_win()