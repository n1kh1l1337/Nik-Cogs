import discord
from redbot.core import menus, commands


class BadArgument(menus.MenuError):
    def __init__(self, message):
        super().__init__(message)


class EmbedPagesData(menus.ListPageSource):
    def __init__(self, data, per_page=1):
        if not isinstance(data[0], discord.Embed):
            raise BadArgument(f"Expected discord.Embed, got {data[0].__class__}")
        self.original_footer = data[0].footer.text
        super().__init__(data, per_page=per_page)

    async def format_page(self, menu, entry):
        footer = f'{self.original_footer}\nPage {menu.current_page + 1} of {self.get_max_pages()}'
        entry.set_footer(text=footer)
        return entry


class TextPagesData(menus.ListPageSource):
    def __init__(self, data, *, prefix='```', suffix='```', max_size=1980, per_page=1):
        if isinstance(data, str):
            command_paginator = commands.Paginator(prefix=prefix, suffix=suffix, max_size=max_size)
            split = data.split('\n')
            for line in split:
                command_paginator.add_line(line)
        elif isinstance(data, list):
            command_paginator = commands.Paginator(prefix=prefix, suffix=suffix, max_size=max_size)
            for line in data:
                command_paginator.add_line(line)
        elif isinstance(data, commands.Paginator):
            command_paginator = data
        else:
            raise BadArgument(f"Expected `str`, `list` or `commands.Paginator`, got {data.__class__.__name__}")
        super().__init__(command_paginator.pages, per_page=per_page)

    async def format_page(self, menu, page):
        return '\n'.join((page, f'*Page {menu.current_page + 1} of {self.get_max_pages()}*'))


class BloodyMenuPages(menus.MenuPages, inherit_buttons=False):

    def __init__(self, source, **kwargs):
        if 'delete_message_after' not in kwargs:
            kwargs['delete_message_after'] = True
        super().__init__(source, **kwargs)

    # noinspection PyProtectedMember
    async def update(self, payload):
        if self._can_remove_reactions:
            if payload.event_type == 'REACTION_ADD':
                await self.bot.http.remove_reaction(
                    payload.channel_id, payload.message_id,
                    discord.Message._emoji_reaction(payload.emoji), payload.member.id
                )
            elif payload.event_type == 'REACTION_REMOVE':
                return
        await super().update(payload)

    @menus.button('<:backward:656488824129454080>', skip_if=menus.MenuPages._skip_double_triangle_buttons)
    async def go_to_first_page(self, payload):
        await super().go_to_first_page(payload)

    @menus.button('<:previous:656488303243034654>')
    async def go_to_previous_page(self, payload):
        await super().go_to_previous_page(payload)

    @menus.button('<:next:656487474297569318>')
    async def go_to_next_page(self, payload):
        await super().go_to_next_page(payload)

    @menus.button('<:forward:656487435957698560>', skip_if=menus.MenuPages._skip_double_triangle_buttons)
    async def go_to_last_page(self, payload):
        await super().go_to_last_page(payload)

    @menus.button('<:stop:678961746869747739>')
    async def stop_pages(self, payload):
        await super().stop_pages(payload)
