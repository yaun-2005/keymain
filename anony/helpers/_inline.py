# Khithlainhtet

from pyrogram import types
from pyrogram.enums import ButtonStyle

from anony import app, config, lang
from anony.core.lang import lang_codes


class Inline:
    def __init__(self):
        self.ikm = types.InlineKeyboardMarkup
        self.ikb = types.InlineKeyboardButton

    def cancel_dl(self, text) -> types.InlineKeyboardMarkup:
        return self.ikm([[self.ikb(text=text, callback_data="cancel_dl", style=ButtonStyle.DANGER)]])

    def controls(
        self,
        chat_id: int,
        _lang: dict,
        status: str = None,
        timer: str = None,
        remove: bool = False,
    ) -> types.InlineKeyboardMarkup:
        keyboard = []
        if status:
            keyboard.append([self.ikb(text=status, callback_data=f"controls status {chat_id}", style=ButtonStyle.PRIMARY)])
        elif timer:
            keyboard.append([self.ikb(text=timer, callback_data=f"controls status {chat_id}", style=ButtonStyle.PRIMARY)])
        
        if not remove:
            
            keyboard.append(
                [
                    self.ikb(text="▷", callback_data=f"controls resume {chat_id}", style=ButtonStyle.PRIMARY),
                    self.ikb(text="⥁", callback_data=f"controls replay {chat_id}", style=ButtonStyle.DANGER),
                    self.ikb(text="II", callback_data=f"controls pause {chat_id}", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="6185994856163185048"),
                    self.ikb(text="▢", callback_data=f"controls stop {chat_id}", style=ButtonStyle.DANGER),
                    self.ikb(text="‣‣I", callback_data=f"controls skip {chat_id}", style=ButtonStyle.PRIMARY),    
                ]
            )
            
            keyboard.append(
                [self.ikb(text=f"{_lang['close']}", callback_data="help close", style=ButtonStyle.DANGER, icon_custom_emoji_id="6095794508518137100")]
            )
        return self.ikm(keyboard)

    def help_markup(self, _lang: dict, back: bool = False) -> types.InlineKeyboardMarkup:
        if back:
            rows = [[
                self.ikb(text=f"{_lang['back']}", callback_data="help back", style=ButtonStyle.DANGER ),
                self.ikb(text=f"{_lang['close']}", callback_data="help close", style=ButtonStyle.DANGER),
            ]]
        else:
            cbs = ["admins", "auth", "blist", "lang", "ping", "play", "queue", "stats", "sudo"]
            buttons = [self.ikb(text=f"✦ {_lang[f'help_{i}']}", callback_data=f"help {cb}", style=ButtonStyle.PRIMARY) for i, cb in enumerate(cbs)]
            rows = [buttons[i:i + 3] for i in range(0, len(buttons), 3)]
        return self.ikm(rows)

    def lang_markup(self, _lang: str) -> types.InlineKeyboardMarkup:
        langs = lang.get_languages()
        buttons = [
            self.ikb(
                text=f"{name} ({code}) {'✔️' if code == _lang else ''}",
                callback_data=f"lang_change {code}",
                style=ButtonStyle.PRIMARY if code == _lang else ButtonStyle.DEFAULT,
            )
            for code, name in langs.items()
        ]
        rows = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
        return self.ikm(rows)

    def ping_markup(self, text: str) -> types.InlineKeyboardMarkup:
        return self.ikm([[self.ikb(text=text, url=config.SUPPORT_CHAT, style=ButtonStyle.PRIMARY)]])

    def play_queued(self, chat_id: int, item_id: str, _text: str) -> types.InlineKeyboardMarkup:
        return self.ikm([[self.ikb(text=_text, callback_data=f"controls force {chat_id} {item_id}", style=ButtonStyle.PRIMARY)]])

    def queue_markup(self, chat_id: int, _text: str, playing: bool) -> types.InlineKeyboardMarkup:
        _action = "pause" if playing else "resume"
        return self.ikm([[self.ikb(text=_text, callback_data=f"controls {_action} {chat_id} q", style=ButtonStyle.PRIMARY)]])

    def settings_markup(
        self, lang: dict, admin_only: bool, cmd_delete: bool, language: str, chat_id: int
    ) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(text=f"• {lang['play_mode']}", callback_data="settings"),
                    self.ikb(text=str(admin_only), callback_data="settings play", style=ButtonStyle.PRIMARY),
                ],
                [
                    self.ikb(text=f"• {lang['cmd_delete']}", callback_data="settings"),
                    self.ikb(text=str(cmd_delete), callback_data="settings delete"),
                ],
                [
                    self.ikb(text=f"• {lang['language']}", callback_data="settings"),
                    self.ikb(text=lang_codes[language], callback_data="language"),
                ],
            ]
        )

    def start_key(self, lang: dict, private: bool = False) -> types.InlineKeyboardMarkup:
        if not private:
            rows = [
                [self.ikb(text=f"{lang['add_me']}", url=f"https://t.me/{app.username}?startgroup=true", style=ButtonStyle.PRIMARY)],
                [self.ikb(text=f"{lang['language']}", callback_data="language", style=ButtonStyle.DANGER)],
            ]
        else:
            rows = [
                [self.ikb(text=f"{lang['add_me']}", url=f"https://t.me/{app.username}?startgroup=true", style=ButtonStyle.PRIMARY,icon_custom_emoji_id="6183677764256666403")],
                [self.ikb(text=f"{lang['help']}", callback_data="help", style=ButtonStyle.DANGER, icon_custom_emoji_id="5384466886857614542")],
                [
                    self.ikb(text=f"{lang['support']}", url=config.SUPPORT_CHAT, style=ButtonStyle.SUCCESS, icon_custom_emoji_id="6208548360794677149"),
                    self.ikb(text=f"{lang['channel']}", url=config.SUPPORT_CHANNEL, style=ButtonStyle.SUCCESS,icon_custom_emoji_id="6208548360794677149"),
                ],
                [
                    self.ikb(text=f"{lang['source']}", user_id=config.OWNER_ID, style=ButtonStyle.PRIMARY, icon_custom_emoji_id="6208694634495876948"),
                    self.ikb(text=f"𝑪𝒓𝒂𝒕𝒆𝒓", user_id=config.CREATOR, style=ButtonStyle.PRIMARY,icon_custom_emoji_id="6185994856163185048"),
                ]
            ]
        return self.ikm(rows)

    def yt_key(self, link: str) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [[
                self.ikb(text="❐", copy_text=link, style=ButtonStyle.PRIMARY),
                self.ikb(text="Youtube", url=link, style=ButtonStyle.DANGER),
            ]]
        )
