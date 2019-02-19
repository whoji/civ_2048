import pygame
import random

from pygame.locals import *
from flags import F


class Block():
    '''
    TODO: merge this Block() from mover. make it a sprite
    '''
    def __init__(self, i, j, x=0, y=0, val=2):
        self.x = x          # pixel pos
        self.y = y          # pixel pos
        self.i = i          # tile pos
        self.j = j          # tile pos
        self.val = val      # face value
        self.status = 'stationary'
        self.if_disappear = False
        self.dest_i = None
        self.dest_j = None
        self.dest_x = None
        self.dest_y = None
        self.dx, self.dy = None, None

        self.bg_color = F.tile_color[val]
        self.image = pygame.Surface([F.tile_size, F.tile_size])
        self.image.fill(self.bg_color)
        self.image.set_colorkey(F.white)
        self.rect = self.image.get_rect()
        if self.x == 0 and self.y == 0:
            self.get_static_px_pos()

        # block / tile types
        self.type = self.__get_type()
        self.cap = self.__get_cap()

    def draw(self, DISPLAYSUR, font, gen_ui):
        o = F.board_frame_px
        moving_tile_pos = [self.x+o, self.y+o]
        moving_tile_rect = [self.x+o, self.y+o, F.tile_size-2*o, F.tile_size-2*o]
        if (self.i, self.j) in F.stars_pos.values():
            tile_color = F.get_tile_color(self.i, self.j)
        else:
            tile_color = F.tile_color[self.val]
        pygame.draw.rect(DISPLAYSUR, tile_color, moving_tile_rect)

        # the text (number)
        text_obj = gen_ui.generate_block_text_obj(font, self.val)
        if F.block_font_center:
            moving_tile_pos = Mover.center_text(text_obj,moving_tile_pos)
        DISPLAYSUR.blit(text_obj,moving_tile_pos)

    def get_speed(self):
        #import pdb; pdb.set_trace()
        #print("[%d,%d] to ..." % (self.x,self.y))
        print("ii (%d,%d) to (%d,%d) | " % (self.i,self.j,self.dest_i,self.dest_j), end="")
        print("px [%d,%d] to [%d,%d]" % (self.x,self.y,self.dest_x,self.dest_y))
        speed_x = (self.dest_x - self.x) * 1.0 / F.move_frame
        speed_y = (self.dest_y - self.y) * 1.0 / F.move_frame
        return speed_x, speed_y

    def get_static_px_pos(self):
        self.x = F.board_offset_x + self.j * F.tile_size
        self.y = F.board_offset_y + self.i * F.tile_size

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def __repr__(self):
        return "%d@(%d,%d)" % (self.val, self.x, self.y)

    def set_dest(self, dest_i, dest_j):
        self.dest_i = dest_i
        self.dest_j = dest_j
        self.dest_x, self.dest_y = self.ij_to_xy(dest_i, dest_j)
        self.dx, self.dy = self.get_speed()

    def __get_type(self):
        for name, pos in F.stars_pos.items():
            if (self.i, self.j) == pos:
                return name
        return 0

    def __get_cap(self):
        return 99999999

    @staticmethod
    def ij_to_xy(i,j):
        '''
        convert tile coordinates to pixel value coordinates
        '''
        x = F.board_pos[0] + j * F.tile_size
        y = F.board_pos[1] + i * F.tile_size
        return x, y


class Mover(object):
    """docstring for Mover"""
    def __init__(self, b, action, stars_cap):
        self.board = [r[:] for r in b]
        self.board_px = None
        self.action = action
        self.total_moving_frames = F.move_frame
        self.remain_moving_frames = self.total_moving_frames
        self.stars_cap = stars_cap
        self.init_board_px()
        self.get_all_blocks_destination(self.board, self.action)

    def init_board_px(self):
        self.board_px = [[None for w in range(F.map_cols)] 
            for h in range (F.map_rows)]

        # add Block according to self.board
        for i in range(F.map_rows):
            for j in range(F.map_cols):
                if self.board[i][j] != 0:
                    self.board_px[i][j] = Block(i=i,j=j,val=self.board[i][j])


    def render(self, DISPLAYSUR):
        pass

    def move_all(self):
        assert self.remain_moving_frames > 0
        m = F.map_rows
        n = F.map_cols
        for i in range(m):
            for j in range(n):
                if isinstance(self.board_px[i][j], Block):
                    self.board_px[i][j].move()
        self.remain_moving_frames -= 1

    def get_all_blocks_destination(self, b, action):
        m = F.map_rows
        n = F.map_cols
        if action == 'up':
            for i in range(m):
                for j in range(n):
                    dest_i, dest_j, if_disappear = self.get_block_destination(b,i,j,action)
                    if dest_i is None: continue
                    self.board_px[i][j].set_dest(dest_i, dest_j)
                    v = b[i][j]
                    b[i][j] = 0
                    b[dest_i][dest_j] = v
        elif action == 'down':
            for i in reversed(range(m)):
                for j in range(n):
                    dest_i, dest_j, if_disappear = self.get_block_destination(b,i,j,action)
                    if dest_i is None: continue
                    self.board_px[i][j].set_dest(dest_i, dest_j)
                    v = b[i][j]
                    b[i][j] = 0
                    b[dest_i][dest_j] = v
        elif action == 'right':
            for i in range(m):
                for j in reversed(range(n)):
                    dest_i, dest_j, if_disappear = self.get_block_destination(b,i,j,action)
                    if dest_i is None: continue
                    self.board_px[i][j].set_dest(dest_i, dest_j)
                    v = b[i][j]
                    b[i][j] = 0
                    b[dest_i][dest_j] = v
        elif action == 'left':
            for i in range(m):
                for j in range(n):
                    dest_i, dest_j, if_disappear = self.get_block_destination(b,i,j,action)
                    if dest_i is None: continue                    
                    self.board_px[i][j].set_dest(dest_i, dest_j)
                    v = b[i][j]
                    b[i][j] = 0
                    b[dest_i][dest_j] = v
        else:
            raise Exception("WTF is this action: %s" % str(action))


    def get_block_destination(self, b, i, j, action):
        '''
        return: dest_i
        return: dest_j
        return: if_disappear
        '''
        assert 0 <= i < F.map_rows
        assert 0 <= j < F.map_rows
    
        if F.if_stars and (i,j) in F.stars_pos.values():
            return i, j, False
        elif b[i][j] == 0:
            return None, None, None
        else:
            v = b[i][j]
            if_disappear = False

            if action == 'up':
                cap = self.get_target_cap(pos=(i-1,j))
                while i >= 1:
                    if b[i-1][j] == 0: 
                        if_disappear = False
                        i -= 1
                    elif b[i-1][j] == v and b[i-1][j] + v <= cap:
                        if_disappear = True
                        i -= 1
                        break
                    else:
                        return i, j, False
                return i, j, if_disappear

            elif action == 'down':
                cap = self.get_target_cap(pos=(i+1,j))
                while i < F.map_rows - 1:
                    if b[i+1][j] == 0: 
                        if_disappear = False
                        i += 1
                    elif b[i+1][j] == v and b[i+1][j] + v <= cap:
                        if_disappear = True
                        i += 1
                        break
                    else:
                        return i, j, False
                return i, j, if_disappear

            elif action == 'left':
                cap = self.get_target_cap(pos=(i,j-1))
                while j >= 1:
                    if b[i][j-1] == 0: 
                        if_disappear = False
                        j -= 1
                    elif b[i][j-1] == v and b[i][j-1] + v <= cap:
                        if_disappear = True
                        j -= 1
                        break
                    else:
                        return i, j, False
                return i, j, if_disappear

            elif action == 'right':
                cap = self.get_target_cap(pos=(i,j+1))
                while j < F.map_cols - 1:
                    if b[i][j+1] == 0: 
                        if_disappear = False
                        j += 1
                    elif b[i][j+1] == v and b[i][j+1] + v <= cap:
                        if_disappear = True
                        j += 1
                        break
                    else:
                        return i, j, False
                return i, j, if_disappear

            else:
                raise Exception("invalid actoin.")


    def get_coordinates(self):
        pass

    def get_target_cap(self, pos):
        if pos in  F.stars_pos.values():
            return self.stars_cap[F.get_star_name(pos)]
        else:
            return 99999999

    @staticmethod
    def center_text(text_obj, moving_tile_pos):
        """
        return the postion (x,y) for the centered text, (center relative to block/tile)
        """
        x_adj = int((F.tile_size - text_obj.get_size()[0])/2)
        y_adj = int((F.tile_size - text_obj.get_size()[1])/2)
        new_pos = (moving_tile_pos[0]+x_adj, moving_tile_pos[1]+y_adj)
        return new_pos



