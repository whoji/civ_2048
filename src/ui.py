import pygame
from flags import F
from pygame.locals import *


class StatusBar(object):
    """docstring for StatusBar"""
    def __init__(self):
        #self.controller = None
        self.board = None
        self.top_score = 0
        self.cur_score = 0
        self.moves = 0
        self.pos = (0, F.window_h - F.status_bar_size)
        self.size = (F.window_w, F.status_bar_size)
        self.rect = (self.pos[0], self.pos[1], self.pos[0] + self.size[0], 
            self.pos[1]+self.size[1])
        if F.if_star:
            self.star_score = 0
            self.top_star_score = 0
            self.milestone_str = ""
        if F.if_stars:
            #self.bd = {}
            #self.mt = {}
            self.stars = {}

    def update_status(self):
        self.moves = self.board.total_moves
        self.cur_score = self.get_board_total_sum(self.board.board)
        if self.cur_score > self.top_score:
            self.top_score = self.cur_score
        if F.if_star:
            self.star_score = self.board.board[F.star_pos[0]][F.star_pos[1]]
            if self.star_score > self.top_star_score:
                self.top_star_score = self.star_score
        if F.if_stars:
            for name, pos in F.stars_pos.items():
                self.stars[name] = self.board.board[pos[0]][pos[1]]

    def render(self, DISPLAYSUR):    
        #bg = pygame.image.load(F.option_bg_img_path)
        #bg = pygame.transform.scale(bg, self.size)
        #DISPLAYSUR.blit(bg,self.pos)
        pygame.draw.rect(DISPLAYSUR, F.blue2, self.rect)

        GFONT_s = pygame.font.Font('freesansbold.ttf', 15)
        GFONT_b = pygame.font.Font('freesansbold.ttf', 30)

        tot_moves = GFONT_s.render("moves", True, F.white, None)
        tot_score = GFONT_s.render("score", True, F.white, None)
        tot_top_score = GFONT_s.render("top score", True, F.white, None)

        tov_moves = GFONT_b.render(str(self.moves), True, F.white, None)
        tov_score = GFONT_b.render(str(self.cur_score), True, F.white, None)
        tov_top_score = GFONT_b.render(str(self.top_score), True, F.white, None)

        DISPLAYSUR.blit(tot_moves, self.apply_offset(self.pos, (10, 10)))
        DISPLAYSUR.blit(tov_moves, self.apply_offset(self.pos, (10, 25)))

        DISPLAYSUR.blit(tot_score, self.apply_offset(self.pos, (110, 10)))
        DISPLAYSUR.blit(tov_score, self.apply_offset(self.pos, (110, 25)))

        DISPLAYSUR.blit(tot_top_score, self.apply_offset(self.pos, (710, 10)))
        DISPLAYSUR.blit(tov_top_score, self.apply_offset(self.pos, (710, 25)))

        if F.if_star:
            tot_castle = GFONT_s.render("castle", True, F.white, None)
            tot_top_castle = GFONT_s.render("top castle", True, F.white, None)
            tov_castle = GFONT_s.render(str(self.star_score), True, F.white, None)
            tov_top_castle = GFONT_b.render(str(self.top_star_score), True, F.white, None)
            
            DISPLAYSUR.blit(tot_top_castle, self.apply_offset(self.pos, (610, 10)))
            DISPLAYSUR.blit(tov_top_castle, self.apply_offset(self.pos, (610, 25)))

        if F.if_star and F.display_castle:
            # Display the castle icons
            x_start_pos = 200
            y_start_pos = 0
            # castle_list = [v for k,v in F.castle_textures.items() if k <= self.star_score]
            # if F.big_castle_icon:
            #     castle_list = [v for k,v in F.castle_textures.items() if k <= self.star_score
            #         and k in F.castle_list]
            # for i, c in enumerate(castle_list):
            #     cs = pygame.transform.scale(c, (F.castle_icon_px, F.castle_icon_px))
            #     DISPLAYSUR.blit(cs, self.apply_offset(self.pos, (x_start_pos +
            #         i*F.castle_icon_gap+i*F.castle_icon_px, y_start_pos)))
            #     if i == 8 and not  F.castle_list:
            #         x_start_pos -= (8+1)*(F.castle_icon_px+F.castle_icon_gap)
            #         y_start_pos = 30

        # if F.if_star:
        #     self.milestone_str = '* '*  (F.milestone.index(self.star_score)+1)
        #     text_obj_1 = GFONT.render("castle:[ %d ]     top casle:[ %d ]    %s" % 
        #         (self.star_score, self.top_star_score, self.milestone_str),
        #         True, F.white, None)
        #     DISPLAYSUR.blit(text_obj_1, self.apply_offset(self.pos, (10, 30) ))

        #pygame.display.update()

    @staticmethod
    def get_board_total_sum(b):
        ret = sum([sum(r) for r in b])
        return ret

    @staticmethod
    def apply_offset(pos,offset):
        return (pos[0]+offset[0], pos[1]+offset[1])

    def __draw_text_center():
        raise NotImplementedError
        # font = pygame.font.Font(None, 25)
        # text = font.render("You win!", True, BLACK)
        # text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        # screen.blit(text, text_rect)

class GenUI():
    """docstring for ClassName"""
    def __init__(self):
        self.GFONTS = None

    @staticmethod
    def shorten_block_text(n):
        if n > 1000000:
            return str(int(n / 1000000))+"m" # e.g. 1048576 -> 1m
        if n > 10000:
            return str(int(n / 1000))+"k" # e.g. 16384 -> 16k
        return str(n)

    #@staticmethod
    def generate_block_text_obj_obsolete(self, FONT, n):
        text_str = self.shorten_block_text(n)
        digits = len(text_str)        
        text_obj = FONT.render(text_str, True, F.block_text_fg, F.block_text_bg)
        text_obj_size = text_obj.get_rect().size
        text_obj_size = [int(s*F.block_font_size_perc[digits-1]) for s in text_obj_size]
        text_obj = pygame.transform.scale(text_obj, text_obj_size)
        return text_obj

    def generate_block_text_obj(self, FONTS, n):
        text_str = self.shorten_block_text(n)
        digits = len(text_str)
        FONT = FONTS[digits-1]
        text_obj = FONT.render(text_str, True, F.block_text_fg, F.block_text_bg)
        return text_obj

    @staticmethod
    def apply_offset(pos,offset):
        return (pos[0]+offset[0], pos[1]+offset[1])

    @staticmethod
    def draw_text_with_outline(SURF, FONT, text_str, fg_color, outline_color, 
        outline_px, pos_0, if8=True, if_center=True):
        text_obj_fg = FONT.render(text_str, True, fg_color, None)
        text_obj_bg = FONT.render(text_str, True, outline_color, None)
        if if_center:
            pos_0 = (
                pos_0[0] - int(text_obj_fg.get_size()[0] / 2),  
                pos_0[1] - int(text_obj_fg.get_size()[1] / 2)
            )
        SURF.blit(text_obj_bg,(pos_0[0]-outline_px, pos_0[1])) #for outline
        SURF.blit(text_obj_bg,(pos_0[0]+outline_px, pos_0[1])) #for outline
        SURF.blit(text_obj_bg,(pos_0[0], pos_0[1]-outline_px)) #for outline
        SURF.blit(text_obj_bg,(pos_0[0], pos_0[1]+outline_px)) #for outline
        if if8:
            SURF.blit(text_obj_bg,(pos_0[0]-outline_px, pos_0[1]-outline_px)) #for outline
            SURF.blit(text_obj_bg,(pos_0[0]+outline_px, pos_0[1]-outline_px)) #for outline
            SURF.blit(text_obj_bg,(pos_0[0]-outline_px, pos_0[1]+outline_px)) #for outline
            SURF.blit(text_obj_bg,(pos_0[0]+outline_px, pos_0[1]+outline_px)) #for outline
        SURF.blit(text_obj_fg, pos_0)        