import unittest
import arcade.geometry
import fish
import numpy as np
import matplotlib.pyplot as plt

class test_hitbox_after_rescaling(unittest.TestCase):

    def test(self):
        f1 = fish.player.PlayerFish(None,(0,0))
        h0 = np.array(f1.get_adjusted_hit_box())
        f1.is_facing_right = False
        h1 = np.array(f1.get_adjusted_hit_box())
        f1.size *= 2
        h2 = np.array(f1.get_adjusted_hit_box())
        plt.plot(h0[:, 0], h0[:, 1])
        plt.plot(h1[:, 0], h1[:, 1])
        plt.plot(h2[:, 0], h2[:, 1])
        plt.show()



