from .fish_base_class import Fish
import arcade
from resources import player_fish_texture_map,restart_button_texture_map
import typing
if typing.TYPE_CHECKING:
    from game_class import MyGame
from game_constents import player_fish_speed,player_start_size,player_win_size,player_start_size_acceleration_time_constant,player_final_size_acceleration_time_constant


class PlayerFish(Fish):

    movement_speed: tuple

    def __init__(self, game_object,position = None):
        super().__init__(game_object=game_object, texture_map=player_fish_texture_map, size=player_start_size, is_facing_right=True)
        if position is None:
            self.position = (game_object.width / 2, game_object.height / 2)
        else:
            self.position = position
        self.velocity = (0, 0)
        self.target_velocity = (0,0)

    def change_movement_direction(self, direction: tuple):
        norm = (direction[0] ** 2 + direction[1] ** 2) ** 0.5
        if norm == 0:
            norm = 1
        self.target_velocity = (direction[0] / norm * player_fish_speed, direction[1] / norm * player_fish_speed)

    def update_facing_direction(self):
        if self.target_velocity[0] < 0:
            self.is_facing_right = False
        if self.target_velocity[0] > 0:
            self.is_facing_right = True

    def handle_dispose_fish(self):
        super().handle_dispose_fish()
        self.game_object.handle_game_lost()

    @Fish.size.setter
    def size(self,val):
        Fish.size.fset(self,val)
        if self.size >= player_win_size:
            self.game_object.handle_game_won()

    def on_update(self: "PlayerFish", delta_time=None):
        super().on_update(delta_time)

        self.update_facing_direction()

        # handle acceleration
        player_acceleration_time_constant = \
            (player_start_size_acceleration_time_constant - player_final_size_acceleration_time_constant)/(player_start_size - player_win_size)*\
            (self.size - player_start_size) + player_start_size_acceleration_time_constant
        slipperiness = min(max(1-delta_time/(player_acceleration_time_constant),0),0.97) #typically is 0.8 for 60 FPS
        self.velocity = (self.velocity[0]*(slipperiness) + self.target_velocity[0]*(1-slipperiness)),(self.velocity[1]*(slipperiness) + self.target_velocity[1]*(1-slipperiness))
        # cycle if out of bounds

        # handle eating
        # check for collisions
        collisions = arcade.check_for_collision_with_list(self,self.game_object.fish_sprites)
        for fish in collisions:
            fish:Fish
            if fish is self:
                continue
            if self.size < fish.size:
                small_fish = self
                big_fish = fish
            else:
                small_fish = fish
                big_fish = self
            big_fish.size = (big_fish.size**3 + small_fish.size**3)**(1/3)
            small_fish.handle_dispose_fish()
            if small_fish is self:
                break

        # handle wall collision
        self.handle_wall_collision()


    def handle_wall_collision(self):
        if self.width < self.game_object.width:
            if self.position[0] > self.game_object.width - self.width / 2:
                self.position = (self.game_object.width - self.width / 2, self.position[1])
            elif self.position[0] < self.width / 2:
                self.position = (self.width / 2, self.position[1])
        else:
            self.center_x = self.game_object.width / 2
        if self.height < self.game_object.height:
            if self.position[1] > self.game_object.height:
                self.position = (self.position[0], self.game_object.height)
            elif self.position[1] < 0:
                self.position = (self.position[0], 0)
        else:
            self.center_y = self.game_object.height / 2