
import time, urwid
import utils

class ViewNote(urwid.ListBox):

    def __init__(self, config, args):
        self.config = config
        self.ndb = args['ndb']
        self.key = args['key']
        self.note = self.ndb.get_note(self.key) if self.key else None
        self.tabstop = int(self.config.get_config('tabstop'))
        super(ViewNote, self).__init__(
                  urwid.SimpleFocusListWalker(self.get_note_content_as_list()))

    def get_note_content_as_list(self):
        lines = []
        if not self.key:
            return lines
        for l in self.note['content'].split('\n'):
            lines.append(
                urwid.AttrMap(urwid.Text(l.replace('\t', ' ' * self.tabstop)),
                              'note_content',
                              'note_content_focus'))
        return lines

    def update_note(self, key):
        self.key = key
        self.note = self.ndb.get_note(self.key) if self.key else None
        self.body[:] = \
            urwid.SimpleFocusListWalker(self.get_note_content_as_list())
        self.focus_position = 0

    def get_status_bar(self):
        if not self.key:
            return \
                urwid.AttrMap(urwid.Text(u'No note...'),
                              'status_bar')

        cur   = -1
        total = 0
        if len(self.body.positions()) > 0:
            cur   = self.focus_position
            total = len(self.body.positions())

        t = time.localtime(float(self.note['modifydate']))
        mod_time = time.strftime('%a, %d %b %Y %H:%M:%S', t)
        tags = '%s' % ','.join(self.note['tags'])
        status_title = \
            urwid.AttrMap(urwid.Text(u'Title: ' +
                                     utils.get_note_title(self.note),
                                     wrap='clip'),
                          'status_bar')
        status_key_index = \
            ('pack', urwid.AttrMap(urwid.Text(u' [' + self.note['key'] + u'] ' +
                                              str(cur + 1) +
                                              u'/' +
                                              str(total)),
                                   'status_bar'))
        status_date = \
            urwid.AttrMap(urwid.Text(u'Date: ' +
                                     mod_time,
                                     wrap='clip'),
                          'status_bar')
        flags = ''
        if self.note.has_key("systemtags"):
            if 'pinned' in self.note['systemtags']:   flags = flags + u'*'
            if 'markdown' in self.note['systemtags']: flags = flags + u'm'
        status_tags_flags = \
            ('pack', urwid.AttrMap(urwid.Text(u'[' + tags + u'] [' + flags + u']'),
                                   'status_bar'))
        pile_top = urwid.Columns([ status_title, status_key_index ])
        pile_bottom = urwid.Columns([ status_date, status_tags_flags ])
        return \
            urwid.AttrMap(urwid.Pile([ pile_top, pile_bottom ]),
                          'status_bar')

    def keypress(self, size, key):
        if key == self.config.get_keybind('tabstop2'):
            self.tabstop = 2
            self.body[:] = \
                urwid.SimpleFocusListWalker(self.get_note_content_as_list())

        elif key == self.config.get_keybind('tabstop4'):
            self.tabstop = 4
            self.body[:] = \
                urwid.SimpleFocusListWalker(self.get_note_content_as_list())

        elif key == self.config.get_keybind('tabstop8'):
            self.tabstop = 8
            self.body[:] = \
                urwid.SimpleFocusListWalker(self.get_note_content_as_list())

        else:
            return key

        return None
