class Section:
    def __init__(self, pieces):
        self.pieces = list(pieces)

    def can_add(self, piece):
        return any((piece.is_joinable(s_piece) for s_piece in self.pieces))

    def can_add_section(self, section):
        for piece in section.pieces:
            if self.can_add(piece):
                return True
        return False

    def add_piece(self, piece_to_add):
        for piece in self.pieces:
            for side in piece_to_add.neighbors:
                if piece is piece_to_add.neighbors[side]:
                    if side == (-1, 0):
                        piece_to_add.rect.right = piece.rect.left
                        piece_to_add.rect.top = piece.rect.top
                    elif side == (1, 0):
                        piece_to_add.rect.left = piece.rect.right
                        piece_to_add.rect.top = piece.rect.top
                    elif side == (0, -1):
                        piece_to_add.rect.left = piece.rect.left
                        piece_to_add.rect.bottom = piece.rect.top
                    elif side == (0, 1):
                        piece_to_add.rect.left = piece.rect.left
                        piece_to_add.rect.top = piece.rect.bottom

                    self.pieces.append(piece_to_add)
                    return True

        return False

    def add_section(self, section):
        not_added = section.pieces
        while not_added:
            for piece in not_added:
                if self.add_piece(piece):
                    not_added.remove(piece)

    def check_collide(self, mouse_pos):
        for piece in self.pieces:
            if piece.rect.collidepoint(mouse_pos):
                return True
        return False

    def click(self, mouse_pos):
        for piece in self.pieces:
            piece.mouse_offset[0] = piece.rect.center[0] - mouse_pos[0]
            piece.mouse_offset[1] = piece.rect.center[1] - mouse_pos[1]

    def adjust_pos(self, mouse_pos):
        for piece in self.pieces:
            piece.rect.centerx = mouse_pos[0] + piece.mouse_offset[0]
            piece.rect.centery = mouse_pos[1] + piece.mouse_offset[1]

    def draw(self, surface):
        for piece in self.pieces:
            piece.draw(surface)
