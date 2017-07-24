"""
#----------------------------------------------------------------
# VHDL Mode Utility Module
# Contains methods that were useful in more than one location
#----------------------------------------------------------------
"""
import re
import sublime
import sublime_plugin

def move_up(self, point):
    """
    Moves up one line, attempting to maintain column position.
    """
    x, y = self.view.rowcol(point)
    if x == 0:
        return self.view.text_point(0, 0)
    else:
        return self.view.text_point(x-1, y)

#----------------------------------------------------------------------------
def move_down(self, point):
    """
    Moves down one line, attempting to maintain column position.
    """
    eof_x, eof_y = self.view.rowcol(self.view.size())
    x, y = self.view.rowcol(point)
    #print('row={} col={} eof_row={} eof_col={}'.format(x, y, eof_x, eof_y))
    if x == eof_x:
        # The size is the number of characters and the point is
        # zero indexed, so subtract one from the size.
        return self.view.size()-1
    else:
        return self.view.text_point(x+1, y)

#----------------------------------------------------------------------------
def move_to_bol(self, point):
    """
    Moves the point to the beginning of the line for searching.
    """
    x, y = self.view.rowcol(point)
    return self.view.text_point(x, 0)

#----------------------------------------------------------------------------
def is_top_line(self, point):
    """
    A simple check for the top line of the file.
    """
    x, y = self.view.rowcol(point)
    return bool(x == 0)

#----------------------------------------------------------------------------
def is_end_line(self, point):
    """
    A simple check for the bottom line of the file
    (not necessarily the end of file.)
    """
    x, y = self.view.rowcol(point)
    # The size is the number of characters and the
    # point is zero indexed, so subtract on from the size
    # for the final character.
    eof_x, eof_y = self.view.rowcol(self.view.size()-1)
    return bool(x == eof_x)

#----------------------------------------------------------------------------
def set_cursor(self, point):
    """
    Just setting the point to a particular location.
    """
    self.view.sel().clear()
    self.view.sel().add(sublime.Region(point))
    self.view.show(point)

#----------------------------------------------------------------------------
def line_at_point(self, point):
    """
    Shorthand string extraction method.
    """
    return self.view.substr(self.view.line(point))

#----------------------------------------------------------------------------
def is_vhdl_file(line):
    """
    Receives a string formatted as identifying the
    language scope of the point.  Scope identifiers all
    end with the language name as the trailing clause,
    so we look for 'vhdl'
    """
    s = re.search(r'vhdl', line)
    return bool(s)

#----------------------------------------------------------------------------
def extract_scopes(self):
    """
    This method scans column zero of each line and extracts
    the scope at that point.  Aids in alignment.
    """
    scope_list = []
    point = 0
    while not is_end_line(self, point):
        scope_list.append(self.view.scope_name(point))
        point = move_down(self, point)
    # One final append for the last line.
    scope_list.append(self.view.scope_name(point))
    # Debug
    for i in range(len(scope_list)):
        print('{}: {}'.format(i, scope_list[i]))
    return scope_list