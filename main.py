import pygame

class RB:
    def __init__(self):
        pygame.init()

        self.load_images()
        self.new_game()

        # self.current_y = 0
        # self.current_x = 0
        # self.neighbours = (0,0,0,0)

        self.coins = 0
        self.coins_needed = 0

        self.enemies = []

        self.height = len(self.map)
        self.width = len(self.map[0])
        self.scale = self.images[0].get_width()
        self.coins_needed = self.coins_needed_counter()
        # set enemies but what next??
        self.spawn_enemies()

        window_height = self.scale * self.height
        window_width = self.scale * self.width
        self.window = pygame.display.set_mode((window_width, window_height))

        pygame.display.set_caption("Robber Beyond")
        self.window = pygame.display.set_mode((window_width, window_height + self.scale))
        self.game_font = pygame.font.SysFont("Arial", 24)

        self.main_loop()
        # self.main_frame()

    def load_images(self):
        self.images = []
        for name in ["floor", "wall", "coin", "box", "robot", "done", "target_robot", "monster"]:
            self.images.append(pygame.image.load("Files/img/" + name + ".png"))

    def new_game(self):
        self.moves = 0
        self.map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 2, 1, 0, 0, 0, 1, 21, 22, 15, 1, 0, 1, 0, 1, 1],
                    [1, 14, 13, 12, 11, 1, 0, 0, 20, 1, 16, 0, 0, 0, 2, 1, 1],
                    [1, 1, 2, 1, 0, 0, 0, 1, 19, 18, 17, 1, 0, 1, 0, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    def get_address(self, number):
        if number > 10:
            for y in range(self.height):
                for x in range(self.width):
                    if self.map[y][x] == number:
                        return (y,x)
        else:
            print("get_address did not found address by number " + number)
            return

    def spawn_enemy(self, current_tile_number, is_loop=False):
        # creates enemy object on selected tile
        y = self.get_address(current_tile_number)[0]
        x = self.get_address(current_tile_number)[1]
        newEnemy = Enemy(y, x, self.get_neighbours(y, x), current_tile_number, is_loop, self)
        print("newEnemy.old_number " + str(newEnemy.old_number))
        self.enemies.append(newEnemy)

    def spawn_enemies(self):
        self.spawn_enemy(11)
        self.spawn_enemy(15, True)

    def move_enemies(self):
        for enemy in self.enemies:
            enemy.move()

    def main_loop(self):
        while True:
            self.check_events()
            self.draw_window()

    def main_frame(self):
        self.check_events()
        self.draw_window()

    def find_robot(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] in [4, 6]:
                    return (y, x)

    def get_neighbours(self, y, x):
        return (self.map[y-1][x], self.map[y][x+1], self.map[y+1][x], self.map[y][x-1])

    def coins_needed_counter(self):
        coins_needed = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == 2:
                    coins_needed += 1
        return coins_needed
                    # counting amount of coins needed for win

    def pick_up_coin(self, y, x):
        self.coins += 1
        self.map[y][x] = 0

    def move(self, move_y, move_x):
        if self.game_won():
            return
        # robot movement below
        robot_old_y, robot_old_x = self.find_robot()
        robot_new_y = robot_old_y + move_y
        robot_new_x = robot_old_x + move_x
        self.moves += 1

        if self.map[robot_new_y][robot_new_x] == 1:
            return
        if self.map[robot_new_y][robot_new_x] == 2:
            self.pick_up_coin(robot_new_y, robot_new_x)

        if self.map[robot_new_y][robot_new_x] in [3, 5]:
            box_new_y = robot_new_y + move_y
            box_new_x = robot_new_x + move_x

            if self.map[box_new_y][box_new_x] in [1, 3, 5]:
                return

            self.map[robot_new_y][robot_new_x] -= 3
            self.map[box_new_y][box_new_x] += 3

        self.map[robot_old_y][robot_old_x] -= 4
        self.map[robot_new_y][robot_new_x] += 4
        # drawing agqain afte player movement
        self.main_frame()

    def game_won(self):
        if self.coins == self.coins_needed:
            return True
        else:
            return False

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.move_enemies()
                print(self.map)

                # if event.key == pygame.K_LEFT:
                #     self.move(0, -1)
                # if event.key == pygame.K_RIGHT:
                #     self.move(0, 1)
                # if event.key == pygame.K_UP:
                #     self.move(-1, 0)
                # if event.key == pygame.K_DOWN:
                #     self.move(1, 0)

            if event.type == pygame.QUIT:
                exit()

    def draw_window(self):
        self.window.fill((0, 0, 0))

        for y in range(self.height):
            for x in range(self.width):
                square = self.map[y][x]
                if square > 10:
                    self.window.blit(self.images[0], (x * self.scale, y * self.scale))
                else:
                    self.window.blit(self.images[square], (x * self.scale, y * self.scale))
        game_text = self.game_font.render("Moves: " + str(self.moves), True, (255, 0, 0))
        self.window.blit(game_text, (25, self.height * self.scale + 10))
        game_text = self.game_font.render("Coins: " + str(self.coins) + "/" + str(self.coins_needed), True, (255, 0, 0))
        self.window.blit(game_text, (130, self.height * self.scale + 10))
        game_text = self.game_font.render("F2 = new game", True, (255, 0, 0))
        self.window.blit(game_text, (250, self.height * self.scale + 10))

        game_text = self.game_font.render("Esc = exit game", True, (255, 0, 0))
        self.window.blit(game_text, (400, self.height * self.scale + 10))
        if self.game_won():
            game_text = self.game_font.render("Congratulations, you won the game!", True, (255, 0, 0))
            game_text_x = self.scale * self.width / 2 - game_text.get_width() / 2
            game_text_y = self.scale * self.height / 2 - game_text.get_height() / 2
            pygame.draw.rect(self.window, (0, 0, 0),
                             (game_text_x, game_text_y, game_text.get_width(), game_text.get_height()))
            self.window.blit(game_text, (game_text_x, game_text_y))
        pygame.display.flip()


class Enemy:
    def __init__(self, y, x, neighbours, current_number_at, is_looper=False, rb_inst=None):
        self.rb_inst = rb_inst
        self.last_y = 0
        self.last_x = 0

        self.current_y = y
        self.current_x = x

        self.moving_forward = True
        self.moving_backward = False

        # self.current_number_at = current_number_at
        self.old_number = current_number_at

        self.is_looper = is_looper
        self.loop_start = current_number_at

        # spawning on the map
        # finally setting enemy to the new tile
        self.rb_inst.map[y][x] = 7


        self.neighbours = neighbours

    def change_way(self):
        self.moving_forward = not self.moving_forward
        self.moving_backward = not self.moving_backward

    def move(self):
        print(self.old_number)
        new_address_y = 0
        new_address_x = 0
        self.neighbours = self.rb_inst.get_neighbours(self.current_y, self.current_x)
        i = 0
        sides_to_move_to = []
        for neighbour in self.neighbours:
            if neighbour > 10:
                i += 1
                sides_to_move_to.append(neighbour)
        if i == 1:
            # at the start OR end of the path
            if self.moving_forward:
                if max(sides_to_move_to) > self.old_number:
                    # at the start
                    new_address_y = self.rb_inst.get_address(max(sides_to_move_to))[0]
                    new_address_x = self.rb_inst.get_address(max(sides_to_move_to))[1]
                    # new address is the biggest neighbour
                if max(sides_to_move_to) < self.old_number:
                    # at the end
                    new_address_y = self.rb_inst.get_address(min(sides_to_move_to))[0]
                    new_address_x = self.rb_inst.get_address(min(sides_to_move_to))[1]
                    self.change_way()
                    # new address is the smallest neighbour and we change way
            if self.moving_backward:
                if max(sides_to_move_to) < self.old_number:
                    # at the start (probably redundant)
                    new_address_y = self.rb_inst.get_address(min(sides_to_move_to))[0]
                    new_address_x = self.rb_inst.get_address(min(sides_to_move_to))[1]
                    # new address is the biggest neighbour
                if max(sides_to_move_to) > self.old_number:
                    # at the end
                    new_address_y = self.rb_inst.get_address(max(sides_to_move_to))[0]
                    new_address_x = self.rb_inst.get_address(max(sides_to_move_to))[1]
                    self.change_way()
                    # new address is the smallest neighbour and we change way
        if i > 1:
            if self.is_looper:
                if self.old_number == self.loop_start:
                    new_address_y = self.rb_inst.get_address(min(sides_to_move_to))[0]
                    new_address_x = self.rb_inst.get_address(min(sides_to_move_to))[1]
                else:
                    if min(sides_to_move_to) == self.loop_start and not self.old_number - 1  == self.loop_start:
                        new_address_y = self.rb_inst.get_address(min(sides_to_move_to))[0]
                        new_address_x = self.rb_inst.get_address(min(sides_to_move_to))[1]
                    else:
                        new_address_y = self.rb_inst.get_address(max(sides_to_move_to))[0]
                        new_address_x = self.rb_inst.get_address(max(sides_to_move_to))[1]
            else:
                # in the middle of the path
                if self.moving_forward:
                    new_address_y = self.rb_inst.get_address(max(sides_to_move_to))[0]
                    new_address_x = self.rb_inst.get_address(max(sides_to_move_to))[1]
                    # new address is the biggest neighbour
                if self.moving_backward:
                    new_address_y = self.rb_inst.get_address(min(sides_to_move_to))[0]
                    new_address_x = self.rb_inst.get_address(min(sides_to_move_to))[1]
                    # new address is the smallest neighbour
        # we have new address now we need to move enemy
        # current tile number becomes its old number
        self.rb_inst.map[self.current_y][self.current_x] = self.old_number
        # saving previous number at new tile
        self.old_number = self.rb_inst.map[new_address_y][new_address_x]
        # finally setting enemy to the new tile
        self.current_y = new_address_y
        self.current_x = new_address_x
        self.rb_inst.map[new_address_y][new_address_x] = 7
        # in the end we have resetted tiles with enemies in mind

if __name__ == "__main__":
    RB()


def check_events(self):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move(0, -1)
            if event.key == pygame.K_RIGHT:
                self.move(0, 1)
            if event.key == pygame.K_UP:
                self.move(-1, 0)
            if event.key == pygame.K_DOWN:
                self.move(1, 0)
            if event.key == pygame.K_F2:
                self.new_game()
            if event.key == pygame.K_ESCAPE:
                exit()

        if event.type == pygame.QUIT:
            exit()
