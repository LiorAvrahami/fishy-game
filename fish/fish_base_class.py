import abc
import arcade
import typing
if typing.TYPE_CHECKING:
    from game_class import MyGame

class Fish(abc.ABC, arcade.Sprite):
    _is_facing_right: bool
    texture_map: dict
    game_object: 'MyGame'

    def __init__(self, game_object, texture_map, is_facing_right, size, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.game_object = game_object

        self.texture_map = texture_map

        self._is_facing_right = None
        self.is_facing_right = is_facing_right
        self.size = size

    def handle_dispose_fish(self):
        # remove self from fish sprites
        self.game_object.fish_sprites.remove(self)

    def update_texture(self):
        self.texture = self.texture_map[self.is_facing_right]

    def on_update(self, delta_time=None):
        self.position = [self._position[0] + self.velocity[0]*delta_time, self._position[1] + self.velocity[1]*delta_time]

    @property
    def size(self):
        return self.scale

    @size.setter
    def size(self, val):
        self.scale = val
        self.collision_radius = None

    @property
    def is_facing_right(self):
        return self._is_facing_right

    @is_facing_right.setter
    def is_facing_right(self, val):
        if val != self._is_facing_right or self.texture is None:
            self._is_facing_right = val
            self.update_texture()
            if self._is_facing_right == False:
                self.hit_box = self.texture.hit_box_points
            else:
                self.hit_box = self.texture.hit_box_points
