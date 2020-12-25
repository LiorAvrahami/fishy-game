import arcade
import arcade.gui
import abc
import typing
from resources import *
if typing.TYPE_CHECKING:
    from game_class import MyGame

class HideableGuiElement(arcade.gui.UIImageButton):
    is_visible:bool

    def __init__(self,is_visible,center_x=0, center_y=0,
                 id: typing.Optional[str] = None,
                 style = None,**kwargs):
        self.is_visible = is_visible
        super().__init__(center_x = center_x, center_y = center_y, id = id, style = style, **kwargs)

class TextureButton(HideableGuiElement):
    game_object: 'MyGame'

    def __init__(self,game_object, texture_map,pos_rel_to_center,is_visible,*args,**kwargs):
        if "center_x" not in kwargs:
            x = game_object.width / 2 + pos_rel_to_center[0]
            kwargs["center_x"] = x
        if "center_y" not in kwargs:
            y =  game_object.height / 2 + pos_rel_to_center[0]
            kwargs["center_y"] = y
        kwargs["normal_texture"] = texture_map["mouse_out"]
        kwargs["hover_texture"] = texture_map["mouse_in"]
        kwargs["press_texture"] = texture_map["mouse_pressed"]
        super().__init__(is_visible=is_visible,*args,**kwargs)

        self.game_object = game_object

class Poster(HideableGuiElement):
    game_object: 'MyGame'
    def __init__(self,game_object, texture_map,pos_rel_to_center,is_visible,*args,**kwargs):
        if "center_x" not in kwargs:
            x = game_object.width / 2 + pos_rel_to_center[0]
            kwargs["center_x"] = x
        if "center_y" not in kwargs:
            y =  game_object.height / 2 + pos_rel_to_center[0]
            kwargs["center_y"] = y
        kwargs["normal_texture"] = texture_map["Poster"]
        kwargs["hover_texture"] = texture_map["Poster"]
        kwargs["press_texture"] = texture_map["Poster"]
        super().__init__(is_visible=is_visible,*args,**kwargs)

        self.game_object = game_object

class RestartGameButton(TextureButton):

    def __init__(self,game_object,is_visible,pos_rel_to_center = (0,0),*args,**kwargs):
        super().__init__(game_object,restart_button_texture_map,pos_rel_to_center,is_visible,*args,**kwargs)


    def on_release(self):
        super().on_release()
        self.game_object.restart_game()

class ContinueGameButton(TextureButton):
    def __init__(self,game_object,is_visible,pos_rel_to_center = (0,0),*args,**kwargs):
        super().__init__(game_object,continue_button_texture_map,pos_rel_to_center,is_visible,*args,**kwargs)

    def on_release(self):
        super().on_release()
        self.game_object.unpause()

class ViewHighScoresButton(TextureButton):
    def __init__(self,game_object,is_visible,pos_rel_to_center = (0,0),*args,**kwargs):
        super().__init__(game_object,view_high_scores_button_texture_map,pos_rel_to_center,is_visible,*args,**kwargs)

    def on_release(self):
        super().on_release()
        self.game_object.switch_to_high_scores_view()

class YouWinPoster(Poster):
    def __init__(self,game_object,is_visible,pos_rel_to_center = (0,0),*args,**kwargs):
        super().__init__(game_object,you_win_texture_map,pos_rel_to_center,is_visible,*args,**kwargs)

class YouLosePoster(Poster):
    def __init__(self,game_object,is_visible,pos_rel_to_center = (0,0),*args,**kwargs):
        super().__init__(game_object,you_lose_texture_map,pos_rel_to_center,is_visible,*args,**kwargs)


