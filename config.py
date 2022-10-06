from dataclasses import dataclass
from libqtile import bar, layout
from libqtile.config import Click, Drag, Group, Match, Screen
from libqtile.lazy import lazy

from keymaps import create_keys
from bar import create_widgets


terminal = "alacritty"
browser = "chromium"
mod = "mod4"
font = "Hack Nerd Font Mono"

@dataclass
class colors:
    bg0     = "#131a24" # Dark bg (status line and float)
    bg1     = "#192330" # Default bg
    bg2     = "#212e3f" # Lighter bg (colorcolm folds)
    bg3     = "#29394f" # Lighter bg (cursor line)
    bg4     = "#39506d" # Conceal, border fg
    fg0     = "#d6d6d7" # Lighter fg
    fg1     = "#cdcecf" # Default fg
    fg2     = "#aeafb0" # Darker fg (status line)
    fg3     = "#71839b" # Darker fg (line numbers, fold colums)
    sel0    = "#2b3b51" # Popup bg, visual selection bg
    sel1    = "#3c5372" # Popup sel bg, search bg
    high    = "#719cd6"

groups = [Group(i) for i in "123456789"]

keys = create_keys(mod, terminal, browser, groups)


widget_defaults = dict(
    font=font,
    fontsize=12,
    padding=3,
)

extension_defaults = widget_defaults.copy()

layout_theme = {
    "border_width": 3,
    "margin": 3,
    "border_focus": colors.high,
    "border_normal": colors.bg2
}

layouts = [
    layout.Columns(border_on_single=True, **layout_theme),
    layout.Stack(num_stacks=1, **layout_theme),
]

widgets = create_widgets(font, colors, terminal) 


screens = [
    Screen(
        bottom=bar.Bar(widgets, 20)
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(wm_class="Matplotlib"),
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wmname = "LG3D"
