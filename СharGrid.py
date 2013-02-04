#! /usr/bin/env python3

class CharGrid:
    """CharGrid provides functionality for writing characters on a grid.

    This class provides functions for adding lines, rectangles, circles, text.
	The result may look like:
	************************************
	*                T                 *
	*   Hello!       e                 *
	*                s                 *
	*                t                 *
	************************************

    All char arguments must be strings of length 1; these are guarded by assertions.
    All position arguments must be 2-tuple (x or colomn, y or row); these are also
    guarded by assertions.
    """
    def __init__ (self, colomns = 80, rows = 25, background_char = ' '):
        """Init CharGrid object.

        colomns - number of colomns. Must be more then 0
        rows - number of rows. Must be more then 0
        background_char - char to fill new positions. Must be string of lenght 1
        """
        self.__colomns, self.__rows = colomns, rows
        self.colomns = colomns
        self.rows = rows
        self.background_char = background_char
        self.__grid = [[background_char for colomn in range (colomns)]
                       for row in range (rows)]

    @property
    def size (self):
        """Size of the grid is 2-tuple.
        First element is number of colomns, second is number of rows.
        You can change it. New positions will fill background_char.
        """
        return self.colomns, self.rows

    @size.setter
    def size (self, size):
        assert len (size) == 2, __TUPLE_ASSERT_TEMPLATE.format ('size')
        self.resize (*size)

    def resize (self, colomns, rows):
        """Changes the size of the grid, wiping out the contents.
        New positions will fill background_char.

        colomns - new number of colomns. Must be more then 0
        rows - new number of colomns. Must be more then 0
        """
        self.colomns = colomns
        self.rows = rows

    @property
    def colomns (self):
        """Number of colomns of the grid. You cna change it.
        New positions will fill background_char.
        """
        return self.__colomns

    @colomns.setter
    def colomns (self, colomns):
        assert colomns > 0, 'colomns must be more then 0'

        if (colomns - self.colomns > 0):
            for i in range (rows):
                self.__grid[i].append ((colomns - self.colomns) *
                                        background_char)
        self.__colomns = colomns


    @property
    def rows (self):
        """Number of rows of the grid. You can change it.
        New positions will fill background_char.
        """
        return self.__rows

    @rows.setter
    def rows (self, rows):
        assert rows > 0, 'rows must be more then 0'

        for i in range (rows - self.__rows):
            self.__grid.append (colomns * self.background_char)
        self.__rows = rows

    @property
    def background_char (self):
        """Background char - char who fills new position as default.
        You can change it.
        """
        return self.__background_char

    @background_char.setter
    def background_char (self, background_char):
        assert len (background_char) == 1, __CHAR_ASSERT_TEMPLATE.format (background_char)
        self.__background_char = background_char

    def __str__ (self):
        return '\n'.join (''.join (self.__grid[row]) for row in range (self.rows))

    def clear (self):
        """Clear grid - fill all positions background_char."""
        self.add_rectangle (0, 0, self.colomns - 1, self.rows - 1, need_fill = True)

    def __getitem__ (self, position):
        assert len (position) == 2, __TUPLE_ASSERT_TEMPLATE.format ('position')
        return self.__grid[position[1]][position[0]]

    def get_char (self, x, y, d = None):
        """Return the character at the given position if position inside otherwise d.

        x - x-coordinate (colomn)
        y - y-coordinate (row)
        d - returns if position outside grid. d defaults to None.
        """
        if (0 <= x <= self.colomns and 0 <= y < self.rows):
            return self.__grid[y][x]
        return d

    def __setitem__ (self, position, char):
        assert len (position) == 2, __TUPLE_ASSERT_TEMPLATE.format ('position')
        assert len (char) == 1, __CHAR_ASSERT_TEMPLATE.format (char)
        self.__grid[position[1]][position[0]] = char

    def set_char (self, x, y, char = None):
        """Set char at given position if this position inside grid.

        x - x-coordinate (colomn)
        y - y-coordinate (row)
        char - character to set. If char = None this position will be set background_char.
               char defaults to None.
        """
        char = self.background_char if char is None else char
        assert len (char) == 1, __CHAR_ASSERT_TEMPLATE.format (char)
        if (0 <= x < self.colomns and 0 <= y < self.rows):
            self.__grid[y][x] = char

    #Bresenham's line algorithm implementation
    def add_line (self, x1, y1, x2, y2, char = None):
        """Add line from position (x1, y1) to position (x2, y2) using the given char.
        If some positions outside the grid this position will not set.

        x1 - start x-coordinate (colomn)
        y1 - start y-coordinate (row)
        x2 - finish x-coordinate (colomn)
        y2 - finish y-coordinate (row)
        char - charecher to use. char defaults to None.
        """
        char = self.background_char if char is None else char

        DELTA_X = abs (x2 - x1)
        DELTA_Y = abs (y2 - y1)
        SIGN_X = 1 if x1 < x2 else -1
        SIGN_Y = 1 if y1 < y2 else -1

        error = DELTA_X - DELTA_Y
        self.set_char (x2, y2, char)
        while x1 != x2 or y1 != y2:
            self.set_char (x1, y1, char)

            if (2 * error > -DELTA_Y):
                error -= DELTA_Y
                x1 += SIGN_X
            if (2 * error < DELTA_X):
                error += DELTA_X
                y1 += SIGN_Y

    def add_rectangle (self, x1, y1, x2, y2, char = None, need_fill = False):
        """Add a rectangle to the grid using the given char for the outline.
        If need_fill is True, fills the rectangle with the given char.
        If some positions outside the grid this position will not set.

        x1 - x-coordinate (colomn) of top left corner
        y1 - y-coordinate (row) of top left corner
        x2 - x-coordinate (colomn) of down right corner
        y2 - y-coordinate (row) of down right corner

        x1 must be <= x2 and y1 must be <= y2 if need_fill = True
        """
        char = self.background_char if char is None else char

        if need_fill:
            for dx in range (x2 - x1 + 1):
                for dy in range (y2 - y1 + 1):
                    self.set_char (x1 + dx, y1 + dy, char)
        else:
            self.add_line (x1, y1, x2, y1, char)
            self.add_line (x1, y1, x1, y2, char)
            self.add_line (x2, y1, x2, y2, char)
            self.add_line (x1, y2, x2, y2, char)

    #Bresenham's circle algorithm implementation
    def add_circle (self, x, y, radius, char = None):
        """Add a circle to the grid using the given char for the outline.
        If some positions outside the grid this position will not set.

        x - x-coordinate (colomn) center of circle
        y - y-coordinate (row) center of circle
        radius - circle's radius
        """
        char = self.background_char if char is None else char
        x0 = 0
        y0 = radius
        delta = 2 - 2 * radius
        error = 0
        while (y0 >= 0):
            self.set_char (x + x0, y + y0, char)
            self.set_char (x + x0, y - y0, char)
            self.set_char (x - x0, y + y0, char)
            self.set_char (x - x0, y - y0, char)

            error = 2 * (delta + y0) - 1
            if (delta < 0 and error <= 0):
                x0 += 1
                delta += 2 * x0 + 1
                continue

            error = 2 * (delta - x0) - 1
            if (delta > 0 and error > 0):
                y0 -= 1
                delta += 1 - 2 * y0
                continue

            x0 += 1
            delta += 2 * (x0 - y0)
            y0 -= 1

    def add_text (self, x, y, text, direction = 'horizont', border_char = None):
        """Add a string of text to the grid.
        If some positions outside the grid this position will not set.
        If border_char is not None, draws a box around the text with the given char.

        x - x-coordinate (colomn) text position
        y - y-coordinate (row) text position
        text - string to add
        direction - direction for text - 'horizont' or 'vetrical'
        border_char - char for border around text. If border_char = None border
                      will not draw. border_char defaults to None.
        """
        direction = direction.lower ()
        assert direction == 'horizont' or direction == 'vertical', 'direction must be "horizon" or "vertical"'
        ix = 0 if direction == 'vertical' else 1
        iy = 0 if direction == 'horizont' else 1
        for i in range (len (text)):
            self.set_char (x + i * ix, y + i * iy, text[i])
        if border_char is not None:
            if direction == 'vertical':
                self.add_rectangle (x - 1, y - 1, x + 1, y + len (text), border_char)
            else:
                self.add_rectangle (x - 1, y - 1, x + len (text), y + 1, border_char)


    __CHAR_ASSERT_TEMPLATE = 'char must be a single character: {0} is not appropriate'
    __TUPLE_ASSERT_TEMPLATE = '{0} must be 2-tuple'

if __name__ == '__main__':
    pass