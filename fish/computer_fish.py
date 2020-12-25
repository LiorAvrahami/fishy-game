from .fish_base_class import Fish
from resources import computer_fish_texture_map

class ComputerFish(Fish):
    movement_speed: tuple

    def __init__(self, game_object, is_facing_right, x_pos, y_pos, size, speed):
        super().__init__(game_object=game_object, texture_map=computer_fish_texture_map, is_facing_right=is_facing_right, size=size)
        self.position = (x_pos, y_pos)
        x_velocity_sign = 1 if is_facing_right else -1
        self.velocity = (speed * x_velocity_sign, 0)

    @staticmethod
    def get_size_upper_limmit(scale):
        return [dimentional_limit*scale for dimentional_limit in computer_fish_texture_map.size_limit]

    def on_update(self, delta_time=None):
        super().on_update(delta_time=delta_time)
        # handle wall collision
        if (self.position[0] - self.width/2 > self.game_object.width and self.is_facing_right) or \
           (self.position[1] - self.height/2 > self.game_object.height) or \
           (self.position[0] + self.width / 2 < 0  and not self.is_facing_right) or \
           (self.position[1] + self.height / 2 < 0):
            self.handle_dispose_fish()
