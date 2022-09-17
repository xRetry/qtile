from dataclasses import dataclass
from libqtile import bar, layout, widget, qtile, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = "alacritty"
browser = "chromium"

keys = [
    Key(['mod1'], 'Shift_L', lazy.widget["keyboardlayout"].next_keyboard(), desc="Next keyboard layout."),
    # Key('A-S', lazy.widget["keyboardlayout"].next_keyboard(), desc="Next keyboard layout."),
    # Launch programs
    Key([mod, "shift"], "m", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod, "shift"], "b", lazy.spawn(browser), desc="Launch browser"),
    Key([mod, "shift"], "z", lazy.spawn(terminal + " -e nnn"), desc="Launch file manager"),
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod, "shift"], "space", lazy.layout.normalize(), desc="Reset all window sizes"),
    ### Switch focus of monitors
    Key([mod], "period",
        lazy.next_screen(),
        desc='Move focus to next monitor'
    ),
    Key([mod], "comma",
        lazy.prev_screen(),
        desc='Move focus to prev monitor'
    ),
                      
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    # Toggle between different layouts as defined below
    Key([mod], "space", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "x", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

groups = [Group(i) for i in ["t", "c1", "c2", "w1", "w2", "w3", "m3", "m2", "m1"]]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

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
    

widget_defaults = dict(
    font=font,
    fontsize=12,
    padding=3,
)

extension_defaults = widget_defaults.copy()

layout_theme = {
    "border_width": 2,
    "margin": 3,
    "border_focus": colors.high,
    "border_normal": colors.fg3
}


layouts = [
    layout.Columns(border_on_single=True, **layout_theme),
    layout.Stack(num_stacks=1, **layout_theme),
]


def get_GroupBox() -> list:
    return [widget.GroupBox(
        font = font,
        fontsize = 9,
        margin_y = 3,
        margin_x = 0,
        padding_y = 5,
        padding_x = 3,
        borderwidth = 3,
        active = colors.fg1,
        inactive = colors.fg3,
        rounded = False,
        highlight_color = colors.bg0, #"#1c1f24",
        highlight_method = "line",
        this_current_screen_border = colors.high, #"#51afef",
        this_screen_border = colors.high, #"#98be65",
        other_current_screen_border = colors.bg3, #"#51afef",
        other_screen_border = colors.bg3, #"#98be65",
        foreground = colors.high,
        background = colors.bg0,
    )]

def get_Line() -> list:
    return [widget.TextBox(
        text = '|',
        font = font,
        background = colors.bg0,
        foreground = colors.fg3,
        padding = 2,
        fontsize = 14
    )]

def get_CurrentLayout() -> list:
    return [widget.CurrentLayout(
        font = font,
        foreground = colors.fg1,
        background = colors.bg0,
        padding = 5
    )]

def get_WindowCount() -> list:
    return [widget.WindowCount(
        font = font,
        foreground = colors.fg1,
        background = colors.bg0,
        padding = 2
    )]

def get_WindowName() -> list:
    return [widget.WindowName(
        font = font,
        foreground = colors.fg1,
        background = colors.bg0,
        padding = 0
    )]

def get_Systray() -> list:
    return [widget.Systray(
        font = font,
        background = colors.bg0,
        padding = 5
    )]

def get_Sep() -> list:
    return [widget.Sep(
        linewidth = 0,
        padding = 6,
        foreground = colors.bg0,
        background = colors.bg0
    )]

def get_ArrowElement(color_prev, color_bg, widget_elem, widget_kw=dict(), icon=None) -> list:
    elements = []
    elements.append(widget.TextBox(
        text = '',
        font = font,
        background = color_prev,
        foreground = color_bg,
        padding = -12,
        fontsize = 60
    ))
    if icon is not None:
        elements.append(widget.TextBox(
            text = icon,
            font = font,
            fontsize = 20,
            foreground = colors.fg1,
            background = color_bg,
            padding = 0
        ))
    elements.append(widget_elem(
        font = font,
        foreground = colors.fg1,
        background = color_bg,
        padding = 0,
        **widget_kw
    ))
    return elements

widget_list = \
    get_GroupBox() \
    +get_Line() \
    +get_CurrentLayout() \
    +get_Line() \
    +get_WindowCount() \
    +get_Line() \
    +get_WindowName() \
    +get_Systray() \
    +get_Sep() \
    +get_ArrowElement(colors.bg0, colors.bg4, widget.Net, dict(interface='enp3s0', format='{down}  {up} ')) \
    +get_ArrowElement(colors.bg4, colors.bg2, widget.ThermalZone, dict(                   
        fgcolor_normal = colors.fg1,
        crit = 70,
        format = ' {temp} '
    ), '糖') \
    +get_ArrowElement(colors.bg2, colors.bg4, widget.CPU, dict(                   
        format = '{load_percent:3.0f}% ',
    ), '') \
    +get_ArrowElement(colors.bg4, colors.bg2, widget.Memory, dict(                   
        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e htop')},
        format = '{MemPercent:3.0f}% '
    ), '') \
    +get_ArrowElement(colors.bg2, colors.bg4, widget.DF, dict(                   
        format = ' {uf:.0f}{m} ',
        visible_on_warn = False
    ), '') \
    +get_ArrowElement(colors.bg4, colors.bg2, widget.CheckUpdates, dict(                   
        update_interval = 1800,
        distro = "Arch_checkupdates",
        display_format = " {updates} ",
        no_update_string = " 0 ",
        colour_have_updates = colors.fg1,
        colour_no_updates = colors.fg1,
        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e sudo pacman -Syu')}
    ), 'ﮮ') \
    +get_ArrowElement(colors.bg2, colors.bg4, widget.KeyboardLayout, dict(                   
        configured_keyboards = ["us altgr-intl", "de"],
        fmt = ' {} ',
    ), '') \
    +get_ArrowElement(colors.bg4, colors.bg2, widget.Clock, dict(format="%A, %B %d - %H:%M "))
    

screens = [
    Screen(
        bottom=bar.Bar(
            widget_list,
            20,
        ),
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
