import unittest
import arcade
import numpy as np
import matplotlib.pyplot as plt

b_plot_hitboxes_before_assertions = False

class test_hitbox_after_rescaling(unittest.TestCase):

    def test_hitbox_changes_with_texture_change_with_manually_reseting_points(self):
        f1 = arcade.Sprite(":resources:images/enemies/bee.png")
        h0 = np.array(f1.get_adjusted_hit_box())
        f1.texture = arcade.load_texture(":resources:images/enemies/fishGreen.png")
        h1 = np.array(f1.get_adjusted_hit_box())
        if b_plot_hitboxes_before_assertions:
            plt.plot(h0[:, 0], h0[:, 1])
            plt.plot(h1[:, 0], h1[:, 1])
            plt.show()
        self.assertFalse(np.all(h0 == h1))

    def test_hitbox_changes_with_texture_change_without_manually_reseting_points(self):
        f1 = arcade.Sprite(":resources:images/enemies/bee.png")
        h0 = np.array(f1.get_adjusted_hit_box())
        f1._points = None
        f1.texture = arcade.load_texture(":resources:images/enemies/fishGreen.png")
        h1 = np.array(f1.get_adjusted_hit_box())
        if b_plot_hitboxes_before_assertions:
            plt.plot(h0[:, 0], h0[:, 1])
            plt.plot(h1[:, 0], h1[:, 1])
            plt.show()
        self.assertFalse(np.all(h0 == h1))



