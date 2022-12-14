from libqtile import widget, qtile
from libqtile.lazy import lazy

import os
CONFIG_ID = int(os.environ.get("CONFIG_ID", 2)) # 1: notebook, 2: work pc


def get_sep_line(font, colors):
    return widget.TextBox(
        text = '|',
        font = font,
        background = colors.bg0,
        foreground = colors.fg3,
        padding = 2,
        fontsize = 14
    )


def create_widgets(font, colors, terminal):
    general_kws = dict(
        font = font,
        foreground = colors.fg1,
        background = colors.bg0
    )

    widgets_left = [
        widget.CurrentLayout(
            padding = 5,
            **general_kws
        ),
        get_sep_line(font, colors),
        widget.GroupBox(
            fontsize = 9,
            margin_y = 3,
            margin_x = 0,
            padding_y = 5,
            padding_x = 3,
            borderwidth = 3,
            active = colors.fg1,
            inactive = colors.fg3,
            rounded = False,
            highlight_color = colors.bg4,
            highlight_method = "line",
            this_current_screen_border = colors.high,
            this_screen_border = colors.bg4,
            other_current_screen_border = colors.high,
            other_screen_border = colors.bg4,
            **general_kws
        ),
    ]

    widgets_center = [
        get_sep_line(font, colors),
        widget.WindowCount(
            padding = 2,
            **general_kws
        ),
        get_sep_line(font, colors),
        widget.WindowName(
            padding = 0,
            **general_kws
        ),
        widget.Systray(
            font = font,
            background = colors.bg0,
            padding = 5
        ),
        widget.Sep(
            linewidth = 0,
            padding = 6,
            foreground = colors.bg0,
            background = colors.bg0
        ),
    ]


    widgets_right = [
        widget.Net(
            font = font,
            foreground = colors.fg1,
            background = colors.bg4 if CONFIG_ID == 1 else colors.bg2,
            interface='wlo1' if CONFIG_ID == 1 else 'enp3s0',
            format='{up} [UD] {down} ',
        ),
        widget.PulseVolume(
            font = font,
            foreground = colors.fg1,
            background = colors.bg4,
            device = "default",
            fmt = ' [V] {} ',
            volume_app = 'pavucontrol'
        ),
        widget.CPU(
            font = font,
            foreground = colors.fg1,
            background = colors.bg2,
            mouse_callbacks = {'Button3': lambda: qtile.cmd_spawn(terminal + ' -e htop')},
            format = ' [C]{load_percent:3.0f}% '
        ),
        widget.Memory(                   
            font = font,
            foreground = colors.fg1,
            background = colors.bg4,
            mouse_callbacks = {'Button3': lambda: qtile.cmd_spawn(terminal + ' -e htop')},
            format = ' [M]{MemPercent:3.0f}% ',
        ),
        widget.DF(
            font = font,
            foreground = colors.fg1,
            background = colors.bg2,
            format = ' [D] {uf:.0f}{m} ',
            visible_on_warn = False
        ),
        widget.CheckUpdates(
            font = font,
            foreground = colors.fg1,
            background = colors.bg4,
            update_interval = 1800,
            distro = "Arch_checkupdates",
            display_format = " [U] {updates} ",
            no_update_string = " [U] 0 ",
            colour_have_updates = colors.fg1,
            colour_no_updates = colors.fg1,
            mouse_callbacks = {'Button3': lambda: qtile.cmd_spawn(terminal + ' -e sudo pacman -Syu')}
        ),
        widget.KeyboardLayout(
            font = font,
            foreground = colors.fg1,
            background = colors.bg2,
            configured_keyboards = ["us altgr-intl", "de"],
            fmt = ' {} '
        ),
        widget.Clock(
            font = font,
            foreground = colors.fg1,
            background = colors.bg4,
            format=" %A, %B %d - %H:%M "
        )
    ]

    if CONFIG_ID == 1:
        widgets_right.insert(1,
            widget.Battery(
                foreground = colors.fg1,
                background = colors.bg2,
                format = ' [B] {percent:3.0%} ',
                show_short_text = False
            )
        )

    return widgets_left + widgets_center + widgets_right
