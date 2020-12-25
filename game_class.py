import arcade
import arcade.gui

from modifications_to_python_arcade.gui_manager import ModifiedUIManager
from modifications_to_python_arcade.resizeable_window import ResizeableWindow

from arcade.gui.ui_style import UIStyle
import fish
from controls import PlayerControlsObject
from fish_generator import RandomFishGenerator,WaveFishGenerator,FishGenerator
import time
import pickle
import os
from game_sprite_buttons import RestartGameButton,ContinueGameButton,YouWinPoster,ViewHighScoresButton,YouLosePoster
import resources
GL_NEAREST = 9728  # open_gl scaling filter key for nearest neighbor
from game_sprite_buttons import TextureButton
SCREEN_TITLE = "Eat or Be eaten"
import resources
from game_constents import min_computer_fish_size,max_computer_fish_size,min_computer_fish_speed,max_computer_fish_speed,player_win_size,player_start_size
all_deltatimes = []

num_of_high_scores = 5

screen_size:list

main_game_view:arcade.View
game:ResizeableWindow

class MainGameView(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    fish_sprites: arcade.SpriteList
    ui_manager : ModifiedUIManager
    player_fish: fish.PlayerFish
    paused:bool

    # buttons def
    restart_button_game_lost:RestartGameButton
    continue_button_paused:ContinueGameButton
    continue_button_game_lost:ContinueGameButton
    you_win_poster: YouWinPoster
    you_lose_poster: YouLosePoster
    view_high_scores_button: ViewHighScoresButton

    time_played:float

    controls_handler: PlayerControlsObject

    fish_generator: FishGenerator

    b_did_win_already : bool
    FLAG_open_high_scores_menue : int

    @property
    def height(self):
        return screen_size[1]

    @property
    def width(self):
        return screen_size[0]

    def __init__(self):
        super().__init__()
        self.on_resize()
        self.restart_game()

    def restart_game(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here

        # set up buttons

        self.background_texture = resources.background_texture_map["idle"]

        self.fish_sprites = arcade.SpriteList()
        self.ui_manager = ModifiedUIManager(self.window)
        self.player_fish = fish.PlayerFish(self)
        self.fish_generator = RandomFishGenerator(1.1,self,min_fish_size=min_computer_fish_size,max_fish_size=max_computer_fish_size,min_fish_speed=min_computer_fish_speed,max_fish_speed=max_computer_fish_speed)
        self.fish_sprites.append(self.player_fish)
        self.paused = False
        self.controls_handler = PlayerControlsObject(change_player_direction=self.player_fish.change_movement_direction,
                                                     reset_game=self.restart_game, pause_game=self.toggle_game_paused)

        self.restart_button_game_lost = RestartGameButton(self,False)
        self.restart_button_game_won = self.restart_button_game_lost
        self.ui_manager.add_ui_element(self.restart_button_game_won)

        self.continue_button_paused = ContinueGameButton(self,False)
        self.ui_manager.add_ui_element(self.continue_button_paused)

        self.you_win_poster = YouWinPoster(self,False)
        self.you_win_poster.center_y += self.restart_button_game_won.height/2 + self.you_win_poster.height/2 + 10
        self.ui_manager.add_ui_element(self.you_win_poster)

        self.you_lose_poster = YouLosePoster(self,False)
        self.you_lose_poster.center_y = self.restart_button_game_lost.top + self.you_win_poster.height / 2 + 10
        self.ui_manager.add_ui_element(self.you_lose_poster)

        self.continue_button_game_won = ContinueGameButton(self, False)
        self.continue_button_game_won.center_y += -self.restart_button_game_won.height / 2 - self.continue_button_game_won.height / 2 - 10
        self.ui_manager.add_ui_element(self.continue_button_game_won)

        self.view_high_scores_button = ViewHighScoresButton(self,True)
        self.view_high_scores_button.center_x = self.window.width - self.view_high_scores_button.width/2 - 20
        self.view_high_scores_button.center_y = self.view_high_scores_button.height / 2 + 20
        self.ui_manager.add_ui_element(self.view_high_scores_button)

        self.time_played = 0
        self.b_did_win_already = False

        self.FLAG_open_high_scores_menue = -1

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        left, right, bottom, top = self.window.get_viewport()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            right, top,
                                            self.background_texture)
        self.fish_sprites.draw(filter=GL_NEAREST)

        self.ui_manager.on_draw()

        # draw time
        arcade.draw_text("time: {:.0f}".format(self.time_played),20,self.height - 40,color=(255,240,200,210),font_size=25,bold=True,anchor_y="bottom",font_name="ariblk")

        #draw score (only wen game is lost)
        arcade.draw_text("score: {:.0f}%".format((self.player_fish.size - player_start_size)/(player_win_size-player_start_size)*100), 20, self.height - 40,
                         color=(255, 240, 200, 210), font_size=25, bold=True, anchor_y="top", font_name="ariblk")

    last_time = None
    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        # calculate delta_time
        if self.last_time is not None:
            delta_time = time.time() - self.last_time
        self.last_time = time.time()
        if not self.is_game_lost and not self.b_did_win_already and not self.paused:
            self.time_played += delta_time

        # update game
        if not self.paused:
            self.fish_sprites.on_update(delta_time)
            self.fish_generator.update(delta_time)
            all_deltatimes.append(delta_time)

        if self.FLAG_open_high_scores_menue == 0:
            game.show_view(HighScoresView(self.time_played))
            self.FLAG_open_high_scores_menue = -1
        elif self.FLAG_open_high_scores_menue > 0:
            self.FLAG_open_high_scores_menue -= 1

    @property
    def is_game_lost(self):
        return not self.player_fish in self.fish_sprites

    def unpause(self):
        self.paused = False
        self.continue_button_paused.is_visible = False
        self.you_win_poster.is_visible = False
        self.restart_button_game_won.is_visible = False
        self.continue_button_game_won.is_visible = False

    def toggle_game_paused(self):
        if not self.is_game_lost:
            if self.paused:
                self.unpause()
            else:
                self.paused = True
                self.continue_button_paused.is_visible = True

        else:
            self.restart_game()

    def handle_game_lost(self):
        self.restart_button_game_lost.is_visible = True
        self.you_lose_poster.is_visible = True

    def handle_game_won(self):
        if not self.b_did_win_already:
            self.you_win_poster.is_visible = True
            self.continue_button_game_won.is_visible = True
            self.restart_button_game_won.is_visible = True
            self.b_did_win_already = True

            high_scores = HighScoresView.load_high_scores()
            if self.time_played < max([HighScoresView.try_parse(s[1]) for s in high_scores]):
                self.FLAG_open_high_scores_menue = 1

    def on_close(self):
        self.window.on_close()

    def switch_to_high_scores_view(self):
        if not ( self.paused or self.b_did_win_already or self.is_game_lost ):
            self.toggle_game_paused()
        game.show_view(HighScoresView())

    def on_show_view(self):
        self.last_time = time.time()
        self.controls_handler.reset_state()

    def on_resize(self, width: float = 0, height: float = 0):
        ratio = self.height/self.width
        self.window.height = int(self.window.width*ratio)
        return False

    #UI
    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        self.controls_handler.on_keyboard_press(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        self.controls_handler.on_keyboard_release(key, key_modifiers)

    def on_mouse_motion(self, *args,**kwargs):
        self.ui_manager.on_mouse_motion(*args,**kwargs)

    def on_mouse_press(self, *args, **kwargs):
        self.ui_manager.on_mouse_press(*args,**kwargs)

    def on_mouse_release(self, *args, **kwargs):
        self.ui_manager.on_mouse_release(*args,**kwargs)

class HighScoresView(arcade.View):
    text_input_box : arcade.gui.UIInputBox
    text_output_box : arcade.gui.UILabel
    high_scores_text_boxes : list
    ui_manager : arcade.gui.UIManager

    rectangle_background : arcade.SpriteSolidColor
    def __init__(self,new_high_score=None):
        super().__init__()
        arcade.set_background_color(arcade.color.AZURE)
        self.ui_manager = arcade.gui.UIManager(self.window)
        self.uistyle = UIStyle.default_style()
        font_color = (30, 50, 50)
        self.uistyle.set_class_attrs("label",font_color=font_color,font_color_hover=font_color,font_color_press=font_color)

        title_texture = arcade.load_texture(r"resources\high scores.png")
        self.title_poster = arcade.gui.UIImageButton(center_x=self.width / 2,center_y=self.height,normal_texture=title_texture,hover_texture=title_texture,press_texture=title_texture)
        self.title_poster.center_y -= self.title_poster.height/2
        self.ui_manager.add_ui_element(self.title_poster)

        self.rectangle_background = arcade.SpriteSolidColor(self.width//2,self.height,(140,150,200))
        self.rectangle_background.center_x = self.width / 2
        self.rectangle_background.center_y = self.height/ 2
        self.line_background = arcade.SpriteSolidColor(10,int(self.title_poster.bottom - 70),(20,30,60))
        self.line_background.center_x = self.width / 2
        self.line_background.center_y = self.title_poster.bottom - self.line_background.height/2 - 30

        # back button:
        back_button = arcade.gui.UIImageButton(center_x=0, center_y=0, normal_texture=resources.back_button_texture_map["mouse_out"], hover_texture=resources.back_button_texture_map["mouse_in"],
                                 press_texture=resources.back_button_texture_map["mouse_pressed"])
        back_button.center_x = self.width - back_button.width / 2 - 20
        back_button.center_y = self.height - back_button.height / 2 - 20
        self.ui_manager.add_ui_element(back_button)
        @back_button.event("on_click")
        def on_click():
            self.ui_manager.remove_handlers()
            self.ui_manager.purge_ui_elements()
            game.show_view(main_game_view)

        high_scores = self.load_high_scores()
        if new_high_score is not None:
            for index in range(len(high_scores)):
                if new_high_score < self.try_parse(high_scores[index][1]):
                    high_scores.insert(index,(None,"{:.3g}".format(new_high_score)))
                    high_scores.pop()
                    break
        self.draw_high_scores_table(high_scores)

    @property
    def height(self):
        return screen_size[1]

    @property
    def width(self):
        return screen_size[0]

    @staticmethod
    def try_parse(s):
        try:
            return float(s)
        except:
            return float("inf")

    def draw_high_scores_table(self,high_scores:list):
        self.names_boxes = [arcade.gui.UILabel(name,0,0, style=self.uistyle) if name is not None else
                            self.create_input_box() for name,score in high_scores]
        self.scores_boxes = [arcade.gui.UILabel(score,0,0, style=self.uistyle) for name,score in high_scores]
        for i in range(len(self.names_boxes)):
            y = (self.names_boxes[i-1].center_y - self.names_boxes[i-1].height/2 if i > 0 else self.title_poster.bottom - 50)\
                     - self.names_boxes[i-1].height / 2 - 20
            self.names_boxes[i].center_y = y
            self.names_boxes[i].center_x = self.width/2 - self.names_boxes[i].width/2 - 30
            self.scores_boxes[i].center_y = y
            self.scores_boxes[i].center_x = self.width / 2 + self.scores_boxes[i].width / 2 + 30
            self.ui_manager.add_ui_element(self.names_boxes[i])
            self.ui_manager.add_ui_element(self.scores_boxes[i])

    def create_input_box(self):
        ret = arcade.gui.UIInputBox(0, 0, (self.line_background.left - self.rectangle_background.left)//1.2, style=self.uistyle)
        @ret.event("on_enter")
        def on_enter():
            ret.text.replace("\n","\\n")
            high_scores = [(self.names_boxes[i].text,self.scores_boxes[i].text) for i in range(len(self.names_boxes))]
            self.save_high_scores(high_scores)

            # replace text box with label
            self.ui_manager._ui_elements.remove(ret)
            new_label = arcade.gui.UILabel(ret.text, 0, 0, style=self.uistyle)
            new_label.center_y = ret.center_y
            new_label.center_x = self.width/2 - new_label.width/2 - 30
            index = self.names_boxes.index(ret)
            high_scores[index] = (new_label,high_scores[index][1])
            self.ui_manager.add_ui_element(new_label)

        self.ui_manager.focused_element = ret
        return ret

    def save_high_scores(self,high_scores):
        with open("high_scores.pypickle", "wb+") as file:
            pickle.dump(high_scores, file)

    @staticmethod
    def load_high_scores():
        if os.path.exists("high_scores.pypickle"):
            with open("high_scores.pypickle", "rb") as file:
                high_scores = pickle.load(file)
        else:
            high_scores = []
        while len(high_scores) < num_of_high_scores:
            high_scores.append(("---","---"))
        return high_scores[:num_of_high_scores]

    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()
        self.rectangle_background.draw()
        self.line_background.draw()

    def on_resize(self, width: float = 0, height: float = 0):
        ratio = self.height/self.width
        self.window.height = int(self.window.width*ratio)
        return False

def main():
    """ Main method """
    global game,main_game_view,screen_size
    game = ResizeableWindow(1000, 500, "Fishy Game",resizable=True)
    game.maximize()
    game.dispatch_events()
    screen_size = game.get_size()
    game.stretch_game_with_window = True
    # game.set_viewport(0, self.width, 0, self.height)


    main_game_view = MainGameView()
    game.show_view(main_game_view)
    arcade.run()

if __name__ == "__main__":
    main()

