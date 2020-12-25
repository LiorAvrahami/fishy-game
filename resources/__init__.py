import os as os
__package__ = __package__ or "resources"
from .resources_path import resources_path
import arcade

class TextureMap(dict):
    size_limit:tuple
    b_ignore_left_right_keys:bool
    def __init__(self):
        super().__init__()
        self.size_limit = (0,0)
        for texture in self.values():
            self.update_size_limit(texture)

    def __setitem__(self, key, value):
        super().__setitem__(key,value)
        self.update_size_limit(value)

    def __getitem__(self, item):
        if isinstance(item,bool):
            return super().__getitem__((list(self.keys())[0][0],0,item))
        if isinstance(item,str):
            if not self.b_ignore_left_right_keys:
                raise ValueError("[] must have left or right if b_ignore_left_right_keys = False")
            return super().__getitem__((item,0,True))
        if len(item) == 2:
            if self.b_ignore_left_right_keys:
                return super().__getitem__((item[0], 0, item[1]))
            else:
                return super().__getitem__((item[0],0,item[1]))
        else:
            return super().__getitem__(item)

    def update_size_limit(self,texture:arcade.Texture):
        if texture.width > self.size_limit[0]:
            self.size_limit = (texture.width,self.size_limit[1])
        if texture.height > self.size_limit[0]:
            self.size_limit = (self.size_limit[0],texture.height)

    @staticmethod
    def from_path(path,ignore_left_right_keys=False,hit_box_algorithm="Detailed"):
        ret = TextureMap()
        ret.b_ignore_left_right_keys = ignore_left_right_keys
        for activity in os.listdir(path):
            frames = [frame_image for frame_image in os.listdir(os.path.join(path,activity)) if os.path.splitext(frame_image)[1] == ".png"]
            for frame_index,image_name in enumerate(frames):

                filename = os.path.join(path,activity,image_name)
                texture_right = arcade.load_texture(filename, flipped_horizontally=False,hit_box_algorithm=hit_box_algorithm,hit_box_detail=5)
                _ = texture_right.hit_box_points
                ret[(activity,frame_index,True)] = texture_right

                texture_left = arcade.load_texture(filename, flipped_horizontally=True,hit_box_algorithm=hit_box_algorithm,hit_box_detail=5)
                _ = texture_left.hit_box_points
                ret[(activity, frame_index, False)] = texture_left
        return ret

background_texture_map = TextureMap.from_path(os.path.join(resources_path, "background"),ignore_left_right_keys=True)

computer_fish_texture_map_path = os.path.join(resources_path, "fish_textures")
computer_fish_texture_map = TextureMap.from_path(computer_fish_texture_map_path)

player_fish_texture_map_path = os.path.join(resources_path, "player_textures")
player_fish_texture_map = TextureMap.from_path(player_fish_texture_map_path)

restart_button_texture_map = TextureMap.from_path(os.path.join(resources_path, "restart_button"),ignore_left_right_keys=True)
continue_button_texture_map = TextureMap.from_path(os.path.join(resources_path, "continue_button"),ignore_left_right_keys=True)
you_win_texture_map = TextureMap.from_path(os.path.join(resources_path,"you_win_poster"),ignore_left_right_keys=True)
you_lose_texture_map = TextureMap.from_path(os.path.join(resources_path,"you_lose_poster"),ignore_left_right_keys=True)
back_button_texture_map = TextureMap.from_path(os.path.join(resources_path, "back_button"),ignore_left_right_keys=True)
view_high_scores_button_texture_map = TextureMap.from_path(os.path.join(resources_path, "view_high_scores_button"),ignore_left_right_keys=True,hit_box_algorithm="Simple")
