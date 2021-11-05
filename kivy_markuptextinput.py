from kivy.core.text.markup import MarkupLabel as Label
from kivy.cache import Cache
from kivy.graphics.texture import Texture
from kivy.uix.textinput import TextInput

Cache_get = Cache.get
Cache_append = Cache.append

class MarkupTextInput(TextInput):
    def _create_line_label(self, text, hint=False):
        # Create a label from a text, using line options
        ntext = text.replace(u'\n', u'').replace(u'\t', u' ' * self.tab_width)
        if self.password and not hint:  # Don't replace hint_text with *
            ntext = self.password_mask * len(ntext)
        kw = self._get_line_options()
        cid = '%s\0%s' % (ntext, str(kw))
        texture = Cache_get('textinput.label', cid)

        if texture is None:
            # FIXME right now, we can't render very long line...
            # if we move on "VBO" version as fallback, we won't need to
            # do this. try to found the maximum text we can handle
            label = None
            label_len = len(ntext)
            ld = None

            # check for blank line
            if not ntext:
                texture = Texture.create(size=(1, 1))
                Cache_append('textinput.label', cid, texture)
                return texture

            while True:
                try:
                    label = Label(text=ntext[:label_len], **kw)
                    label.refresh()
                    if ld is not None and ld > 2:
                        ld = int(ld / 2)
                        label_len += ld
                    else:
                        break
                except:
                    # exception happen when we tried to render the text
                    # reduce it...
                    if ld is None:
                        ld = len(ntext)
                    ld = int(ld / 2)
                    if ld < 2 and label_len:
                        label_len -= 1
                    label_len -= ld
                    continue

            # ok, we found it.
            texture = label.texture
            Cache_append('textinput.label', cid, texture)
        return texture