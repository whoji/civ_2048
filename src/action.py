from pygame.locals import *

class Action(object):
    """docstring for action"""
    def __init__(self):
        pass
        
    @staticmethod
    def eventkey_to_action(eventkey):
        action = None
        if eventkey in [K_RIGHT, K_l, K_d]:
            action = 'right'
        elif eventkey  in [K_LEFT, K_h, K_a]:
            action = 'left'
        elif eventkey in [K_DOWN, K_j, K_s]:
            action = 'down'
        elif eventkey in [K_UP, K_k, K_w]:
            action = 'up'
        else:
            #print("bad event key!!")
            pass
        return action
