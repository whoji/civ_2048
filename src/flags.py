import math
import pygame
from pygame.locals import *

class Flags(object):
    """docstring for Flags"""

    def __init__(self):
        self.game_name = 'Civ 2048'
        self.game_ver = '0.01.apha.190207'
        self.proj_path = './'
        self.save_path = './save/'
        self.debug_mod = True
        self.game_fps = 60

        # colors
        self.grey1 = (28,32,38)
        self.grey2 = (14,22,14)
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.red = (250,50,50)
        self.blue = (50,50,250)
        self.blue2 = (2,39,99) # dark blue
        self.green = (50, 200, 100)
        self.yellow = (200,200,50)
        self.orange = (255, 153, 58)
        self.block_text_fg = self.white
        self.block_text_bg = None #self.black

        # size and pos conf (general and menu)
        self.window_w = 800
        self.window_h = 600
        self.tile_size = 50
        self.map_rows = 5
        self.map_cols = 5
        self.status_bar_size = 60
        self.board_offset_x, self.board_offset_y = self.__calculate_board_offset()
        self.text_offset_x = 10
        self.text_offset_y = 10
        self.text_offset = (10,10)
        self.menu_rect = (self.board_offset_x+50, self.board_offset_y+50,
            self.map_cols*self.tile_size-100, self.map_rows*self.tile_size-100)
        self.center_x  = round(self.window_w / 2)
        self.center_y  = round((self.window_h) / 2)
        self.blink_title = True
        self.blink_tile_fps = 20 # every 10 frames will change color

        # size and pos conf (board)
        self.board_color = self.grey1
        self.board_frame_color = self.orange
        self.board_frame_px = 2
        self.board_rect = (self.board_offset_x, self.board_offset_y,
            self.map_cols*self.tile_size, self.map_rows*self.tile_size)
        self.board_outer_rect = (self.board_offset_x-self.board_frame_px,
            self.board_offset_y-self.board_frame_px, 
            self.map_cols*self.tile_size+2*self.board_frame_px, 
            self.map_rows*self.tile_size+2*self.board_frame_px)
        self.init_board_blocks = 2
        self.block_font_center = True
        self.block_font_size = int(self.tile_size / 2)
        self.block_font_sizes = [int(self.tile_size / 2), # for 1 digit
            int(self.tile_size / 3), # for 2 digit
            int(self.tile_size / 4), # for 3 digit
            int(self.tile_size / 5) # for 4 digit
        ]
        self.block_font_size_perc = (1, 1, 0.9, 0.8, 0.5, 0.5, 0.5) 

        # status bar
        self.display_castle = True
        self.castle_icon_px  = 30
        self.castle_icon_gap = 1
        self.big_castle_icon = True
        if self.big_castle_icon:
            self.castle_icon_px = 50
            self.castle_icon_gap = 3
            self.castle_list = [1,4,16, 64,256,1024,4096,16384]
            

        # star 
        self.if_star = True
        self.star_pos = (2,2)
        self.star_tile_color = self.red
        self.star_tile_frame_color = self.red

        # game flow control
        self.win_condition_block = self.__calculate_win_block()
        self.milestone_mode = True
        self.milestone = [2**i for i in range(16)]

        # block moving effect
        self.if_movable = True
        self.move_frame = 10 # frames to finish the move

        # load texture
        #self.__get_textures()
        #self.__resize_texture()

        # load sound effects
        #self.__get_sound()

        # run self check
        #self.__self_check():

    def __self_check():
        raise NotImplementedError
        #raise Exception("Bad set up logic")

    def __calculate_win_block(self):
        ret = 2 ** (int(math.sqrt(self.map_rows * self.map_cols))*3 - 1)
        ret = 2048

        if self.debug_mod:
            if self.map_rows == 3:
                ret = 32
            if self.map_rows == 4:
                ret = 256
            ret = 1024

        return ret

    def __calculate_board_offset(self):
        offset_x = round(self.window_w / 2 - self.map_cols * self.tile_size / 2)
        offset_y = round((self.window_h - self.status_bar_size) / 2 - 
            self.map_rows * self.tile_size / 2)
        return offset_x, offset_y

    # def __get_textures(self):
    #     self.textures = {
    #         -1 : pygame.image.load(self.proj_path + 'asset/stone/stone_0.png'),
    #         1 : pygame.image.load(self.proj_path + 'asset/stone/stone_a.png'),
    #         2 : pygame.image.load(self.proj_path + 'asset/stone/stone_b.png'),
    #         4 : pygame.image.load(self.proj_path + 'asset/stone/stone_1.png'),
    #         8 : pygame.image.load(self.proj_path + 'asset/stone/stone_2.png'),
    #         16 : pygame.image.load(self.proj_path + 'asset/stone/stone_3.png'),
    #         32 : pygame.image.load(self.proj_path + 'asset/stone/stone_4.png'),
    #         64 : pygame.image.load(self.proj_path + 'asset/stone/stone_5.png'),
    #         128 : pygame.image.load(self.proj_path + 'asset/stone/stone_6.png'),
    #         256 : pygame.image.load(self.proj_path + 'asset/stone/stone_7.png'),
    #         512 : pygame.image.load(self.proj_path + 'asset/stone/stone_8.png'),
    #         1024 : pygame.image.load(self.proj_path + 'asset/stone/stone_9.png'),
    #         2048 : pygame.image.load(self.proj_path + 'asset/stone/stone_10.png'),
    #         4096 : pygame.image.load(self.proj_path + 'asset/stone/stone_11.png'),
    #         8192 : pygame.image.load(self.proj_path + 'asset/stone/stone_12.png'),
    #         16384 : pygame.image.load(self.proj_path + 'asset/stone/stone_13.png'),           
    #         32768 : pygame.image.load(self.proj_path + 'asset/stone/stone_14.png')       
    #     }

    #     self.castle_textures = {
    #         1 : pygame.image.load(self.proj_path + 'asset/castle/castle_0.png'),
    #         2 : pygame.image.load(self.proj_path + 'asset/castle/castle_0b.png'),
    #         4 : pygame.image.load(self.proj_path + 'asset/castle/castle_1.png'),
    #         8 : pygame.image.load(self.proj_path + 'asset/castle/castle_1b.png'),
    #         16 : pygame.image.load(self.proj_path + 'asset/castle/castle_2.png'),
    #         32 : pygame.image.load(self.proj_path + 'asset/castle/castle_2b.png'),
    #         64 : pygame.image.load(self.proj_path + 'asset/castle/castle_3.png'),
    #         128 : pygame.image.load(self.proj_path + 'asset/castle/castle_3b.png'),
    #         256 : pygame.image.load(self.proj_path + 'asset/castle/castle_x0.png'),
    #         512 : pygame.image.load(self.proj_path + 'asset/castle/castle_x0.png'),
    #         1024 : pygame.image.load(self.proj_path + 'asset/castle/castle_x1.png'),
    #         2048 : pygame.image.load(self.proj_path + 'asset/castle/castle_x2.png'),
    #         4096 : pygame.image.load(self.proj_path + 'asset/castle/castle_x3.png'),
    #         8192 : pygame.image.load(self.proj_path + 'asset/castle/castle_x4.png'),
    #         16384 : pygame.image.load(self.proj_path + 'asset/castle/castle_x5.png'),           
    #         32768 : pygame.image.load(self.proj_path + 'asset/castle/castle_x6.png')       
    #     }

    def __resize_texture(self):
        for k,v in self.textures.items():
            self.textures[k] = pygame.transform.scale(
                self.textures[k], (self.tile_size-2*self.board_frame_px, 
                    self.tile_size-2*self.board_frame_px))
        for k,v in self.castle_textures.items():
            self.castle_textures[k] = pygame.transform.scale(
                self.castle_textures[k], (self.tile_size-2*self.board_frame_px, 
                    self.tile_size-2*self.board_frame_px))


    # def __get_sound(self):
    #     self.sounds = {
    #         'move'   : pygame.mixer.Sound(self.proj_path + 'asset/sound/Coin_1.wav'), 
    #         'merge'  : pygame.mixer.Sound(self.proj_path + 'asset/sound/Coin_2.wav'), 
    #         'castle' : pygame.mixer.Sound(self.proj_path + 'asset/sound/Coin_3.wav')
    #     }

F = Flags()

