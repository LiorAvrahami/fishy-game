import arcade
from fish import ComputerFish, Fish
import random
import math
import abc

class FishGenerator(abc.ABC):
    @abc.abstractmethod
    def update(self,delta_t):
        pass

class RandomFishGenerator(FishGenerator):
    generation_rate: float
    game_object: "MyGame"
    generation_timer: float  # timer until next fish generation in seconds

    def __init__(self, generation_rate, game_object,
                 min_fish_size, max_fish_size, min_fish_speed, max_fish_speed):
        self.generation_rate = generation_rate
        self.game_object = game_object
        self.generation_timer = 2
        self.min_fish_size = min_fish_size
        self.max_fish_size = max_fish_size
        self.min_fish_speed = min_fish_speed
        self.max_fish_speed = max_fish_speed

    def update(self, delta_t):
        while True:
            self.generation_timer -= delta_t
            if self.generation_timer <= 0:
                self.generation_timer += self.generation_rate
                self.generate_random_fish()
            else:
                break

    def generate_random_fish(self):
        screen_height = self.game_object.height
        screen_width = self.game_object.width

        # roll size
        if random.choices([True,False],(0.2,0.8))[0]:
            # make player sized fish
            new_fish_size = min(self.game_object.player_fish.size*0.8,self.max_fish_size/2)
        else:
            new_fish_size = math.exp(random.uniform(math.log(self.min_fish_size), math.log(self.max_fish_size)))

        # roll speed
        new_fish_speed = random.uniform(self.min_fish_speed, self.max_fish_speed)

        # roll x_pos
        fish_width = ComputerFish.get_size_upper_limmit(scale=new_fish_size)[0]
        new_fish_is_on_left = random.choice([True, False])
        new_fish_x_pos = -fish_width/2 if new_fish_is_on_left else screen_width + fish_width/2

        # roll y_pos
        y_pos_probability_density_reshaper = lambda x: 3 * x - 6 * x ** 2 + 4 * x ** 3
        new_fish_y_pos = y_pos_probability_density_reshaper(random.uniform(0, 1)) * screen_height

        new_fish = ComputerFish(game_object=self.game_object, is_facing_right=new_fish_is_on_left, x_pos=new_fish_x_pos, y_pos=new_fish_y_pos, size=new_fish_size,
                                speed=new_fish_speed)

        self.game_object.fish_sprites.append(new_fish)

class WaveFishGenerator(FishGenerator):
    generation_rate: float
    game_object: "MyGame"
    generation_timer: float  # timer until next fish generation in seconds

    def __init__(self, generation_rate, game_object,
                 fish_size=0.1,fish_speed=1000):
        self.generation_rate = generation_rate
        self.game_object = game_object
        self.generation_timer = 2
        self.fish_size = fish_size
        self.fish_speed = fish_speed

    def update(self, delta_t):
        while True:
            self.generation_timer -= delta_t
            if self.generation_timer <= 0:
                self.generation_timer += self.generation_rate
                self.generate_wave_of_fish()
            else:
                break

    def generate_wave_of_fish(self):
        screen_height = self.game_object.height
        screen_width = self.game_object.width
        for new_fish_y_pos in range(0,screen_height,30):
            # roll x_pos
            new_fish_is_on_left = False
            new_fish_x_pos = screen_width

            # roll size
            new_fish_size = self.fish_size

            # roll speed
            new_fish_speed = self.fish_speed

            new_fish = ComputerFish(game_object=self.game_object, is_facing_right=new_fish_is_on_left, x_pos=new_fish_x_pos, y_pos=new_fish_y_pos, size=new_fish_size,
                                    speed=new_fish_speed)

            self.game_object.fish_sprites.append(new_fish)
