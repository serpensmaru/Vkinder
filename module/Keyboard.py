from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class Keyboard:
    def __init__(self, one_time: bool = False, inline: bool = False):
        self.one_time = one_time
        self.inline = inline
        self.kb = self._kb_obj()

    def _kb_obj(self):
        """ Настройка отображения клавиатуры"""
        return VkKeyboard(one_time=self.one_time, inline=self.inline)

    def pattern_kb(self, *args):
        """ Создание кнопок из списка, если попадает на False, то создаем новую строку кнопок"""
        for one in args:
            if one == 0:
                self.kb.add_line()
            else:
                self.kb.add_button(label=one, color=VkKeyboardColor.NEGATIVE)
        return self.kb.get_keyboard()
