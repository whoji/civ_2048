
#Importing all the modules
try:
    import random, sys
except ImportError:
    print("Make sure to have the time module")
    sys.exit()

try:
    import pygame
    from pygame.locals import *
except ImportError:
    print("Make sure you have python 3 and pygame.")
    sys.exit()
    
try:
    from board import Board
    from flags import F
    from controller import Controller
    from ui import StatusBar, GenUI
    from mover import Mover
    from sound import SoundPlayer
    from action import Action
    # from trophy import Trophy
except ImportError:
    print("Make sure you have all the project files.")
    sys.exit()


class CivGame(object):
    """
    This CivGame class was created when I converted main.py to be 
    more object-oriented (it used to be a big script). Now some part of this
    very hard to read and ugly :(
    """

    def __init__(self):
                
        # Starting the game components
        pygame.init()
        pygame.display.set_caption(F.game_name)
        self.board = Board()
        self.status_bar = StatusBar()
        self.gen_ui = GenUI()
        self.DISPLAYSUR = pygame.display.set_mode((F.window_w, F.window_h))
         # self.trophy = Trophy()self.
        self.controller = Controller(self.DISPLAYSUR)
        self.sound_player = SoundPlayer(pygame)
        self.mover = None
        self.clock = pygame.time.Clock()

        # setup a font for displaying block numbers
        self.GFONT = pygame.font.Font('freesansbold.ttf', F.block_font_size)
        self.GFONT_GG = pygame.font.Font('freesansbold.ttf', 66) 
        self.GFONTS = [
                    pygame.font.Font('freesansbold.ttf', int(F.block_font_size * F.block_font_size_perc[0])),
                    pygame.font.Font('freesansbold.ttf', int(F.block_font_size * F.block_font_size_perc[1])),
                    pygame.font.Font('freesansbold.ttf', int(F.block_font_size * F.block_font_size_perc[2])),
                    pygame.font.Font('freesansbold.ttf', int(F.block_font_size * F.block_font_size_perc[3])),
                    pygame.font.Font('freesansbold.ttf', int(F.block_font_size * F.block_font_size_perc[4])),
                    pygame.font.Font('freesansbold.ttf', int(F.block_font_size * F.block_font_size_perc[5]))   ]
        self.gen_ui.GFONTS = self.GFONTS

    def run(self):
        while True:
            self.clock.tick(F.game_fps)

            # ===================================
            # part 1. Game flow control
            # ===================================
            ret = self.game_flow_control()
            if ret == 0:
                continue

            # ===================================
            # part 2. render everything
            # ===================================
            self.render_everything()

            # ===================================
            # part 3. play sound effect
            # ===================================
            self.play_sound_effect()

            # ===================================
            # part 4. handle trophy
            # ===================================

            # if F.if_star:
            #     trophy_name = "c"+str(status_bar.star_score)
            #     if trophy_name in trophy.trophy_dict and not trophy.trophy_dict[trophy_name]:
            #         trophy.trigger(trophy_name)

            # ===================================
            # end of each frame
            # ===================================

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.controller.quit_game()
            elif event.type == KEYDOWN:
                action = Action.eventkey_to_action(event.key)
                if action in ['up','down','right','left']:
                    self.sound_player.play_action_sound()
                    if_moved = self.board.update_board(action)

                    if if_moved:
                        print("board updated !!")
                        print(self.board)
                        self.mover = Mover(self.board.prev_board, action, self.board.stars_cap)
                        self.controller.game_status = 21
                        self.status_bar.update_status()

                # can press q to exit the game only in debug_mode
                elif event.unicode == 'q' and F.debug_mod:
                    self.controller.quit_game()

                elif event.key == pygame.K_F1 or event.key == pygame.K_ESCAPE:
                    self.controller.call_option()

                elif F.debug_mod:
                    if event.key == pygame.K_F4: # Four for Die (si3)
                        self.board.if_gg = True
                    elif event.key == pygame.K_F5: # Five (V) for Victory
                        self.board.if_win = True

                else:
                    print("Invalid key input: <" + str(event.key) +">; Doing nothing...")
            else:
                pass
                #print("other event.type: " + str(event.type))


    def game_flow_control(self):
        # ===================================
        # part 1. Game flow control
        # ===================================

        controller = self.controller
        board = self.board
        status_bar = self.status_bar
        sound_player = self.sound_player
        self.DISPLAYSUR.fill(F.grey2)

        # when the app started
        if controller.game_status == 0:
            controller.start_application()
            return 0

        # at main menu
        elif controller.game_status == 1:
            sound_player.play_sound_effect(None, controller.game_status)        
            controller.show_main_menu()
            return 0

        # starting the board
        elif controller.game_status == 5:
            board = Board()
            controller.game_status = 2
            status_bar.board = board
            status_bar.update_status()
            #status_bar.controller = controller
            return 0

        # playing the game (at board view)
        elif controller.game_status == 2:

            self.event_handler()

            if board.if_gg:
                controller.lose_game()
            elif board.if_win:
                controller.win_game()
                board.if_win = False

        else:
            pass

        return 1


    def render_everything(self):
        # ===================================
        # part 2. render everything
        # ===================================

        controller = self.controller
        board = self.board
        status_bar = self.status_bar
        gen_ui = self.gen_ui
        mover = self.mover
        DISPLAYSUR = self.DISPLAYSUR
        
        DISPLAYSUR.fill(F.grey2)

        # render the board bg
        pygame.draw.rect(DISPLAYSUR, F.board_frame_color, F.board_outer_rect)
        for row in range(F.map_rows):
            for col in range(F.map_cols):
                pygame.draw.rect(DISPLAYSUR, F.board_frame_color,
                    (col*F.tile_size+F.board_offset_x, row*F.tile_size+
                        F.board_offset_y, F.tile_size, F.tile_size))
                pygame.draw.rect(DISPLAYSUR, F.board_color,(
                    col*F.tile_size+F.board_offset_x+F.board_frame_px,
                    row*F.tile_size+F.board_offset_y+F.board_frame_px, 
                    F.tile_size-2*F.board_frame_px, 
                    F.tile_size-2*F.board_frame_px))
        
        for star_pos in F.stars_pos.values():
            pygame.draw.rect(DISPLAYSUR, F.star_tile_color,(
                    star_pos[1]*F.tile_size+F.board_offset_x-F.board_frame_px,
                    star_pos[0]*F.tile_size+F.board_offset_y-F.board_frame_px, 
                    F.tile_size+2*F.board_frame_px, 
                    F.tile_size+2*F.board_frame_px))

        # render the moving blocks
        if controller.game_status == 21:
            if mover.remain_moving_frames > 0:
                mover.move_all()
                for row in range(F.map_rows):
                    for col in range(F.map_cols):
                        if mover.board_px[row][col]:
                            mover.board_px[row][col].draw(DISPLAYSUR, self.GFONTS, gen_ui)
            else:
                controller.game_status = 2

        # render the board (with blocks)
        if controller.game_status != 21:
            for row in range(F.map_rows):
                for col in range(F.map_cols):
                    if (row, col) in F.stars_pos.values():
                        # DISPLAYSUR.blit(F.castle_textures[board.board[row][col]],
                        #     (col*F.tile_size+F.board_offset_x+F.board_frame_px, 
                        #         row*F.tile_size+F.board_offset_y+F.board_frame_px))
                        block_rect = (col*F.tile_size+F.board_origin[0]+F.board_frame_px, 
                            row*F.tile_size+F.board_origin[1]+F.board_frame_px, 
                            F.tile_size-F.board_frame_px*2,F.tile_size-F.board_frame_px*2)
                        tile_color = F.get_tile_color(row, col)
                        pygame.draw.rect(DISPLAYSUR, tile_color, block_rect)
                        continue
                    if board.board[row][col]:
                        block_rect = (col*F.tile_size+F.board_origin[0]+F.board_frame_px, 
                            row*F.tile_size+F.board_origin[1]+F.board_frame_px, 
                            F.tile_size-F.board_frame_px*2,F.tile_size-F.board_frame_px*2)
                        tile_color = F.tile_color[board.board[row][col]]
                        pygame.draw.rect(DISPLAYSUR, tile_color, block_rect)

                        # DISPLAYSUR.blit(board.textures[board.board[row][col]],
                        #     (col*F.tile_size+F.board_offset_x+F.board_frame_px, 
                        #         row*F.tile_size+F.board_offset_y+F.board_frame_px))

        # render the text
        if controller.game_status != 21:
            for row in range(F.map_rows):
                for col in range(F.map_cols):
                    if board.board[row][col]:
                        text_obj = gen_ui.generate_block_text_obj(FONTS=self.GFONTS, n=board.board[row][col])
                        tile_pos = (col*F.tile_size+F.board_offset_x+F.board_frame_px, 
                            row*F.tile_size+F.board_offset_y+F.board_frame_px)
                        if F.block_font_center:
                            tile_pos = Mover.center_text(text_obj, tile_pos)
                        DISPLAYSUR.blit(text_obj, tile_pos)

                        
        # render the status bar
        status_bar.render(DISPLAYSUR)

        # render the pop up window (option menu / game over / etc)
        controller.render_pop_window()

        pygame.display.update()


    def play_sound_effect(self):        
        # ===================================
        # part 3. play sound effect
        # ===================================

        sound_event_monitor = (self.board.if_moved, self.board.if_merged, self.board.if_upgraded)
        self.sound_player.play_sound_effect(sound_event_monitor, self.controller.game_status)
        self.board.resest_event_monitor()



if __name__ == '__main__':
    CivGame().run()