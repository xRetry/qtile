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

groups = [Group(i) for i in "123456789"]

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
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )
font = "Hack Nerd Font Mono"
color1 = "#254863" #"#51afef"
color2 = "#051424" #"#adadad" #"#ffad61" "#c678dd"
color_dark = "#282c34"
color_bright = "#b8b8b8" #"#dfdfdf" 
color_faded = "474747"

widget_defaults = dict(
    font=font,
    fontsize=12,
    padding=3,
)

extension_defaults = widget_defaults.copy()

layout_theme = {
    "border_width": 2,
    "margin": 3,
    "border_focus": color1,
    "border_normal": color_faded#"1D2330"
}


layouts = [
    layout.Columns(border_on_single=True, **layout_theme),
    layout.Stack(num_stacks=1, **layout_theme),
    # layout.Max(**layout_theme),
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(panel_width=30, **layout_theme),
    # layout.VerticalTile(),
    # layout.Zoomy(),
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
        active = color_bright,
        inactive = color2,
        rounded = False,
        highlight_color = color_dark, #"#1c1f24",
        highlight_method = "line",
        this_current_screen_border = color1, #"#51afef",
        this_screen_border = color2, #"#98be65",
        other_current_screen_border = color1, #"#51afef",
        other_screen_border = color2, #"#98be65",
        foreground = color_bright,
        background = color_dark
    )]

def get_Line() -> list:
    return [widget.TextBox(
        text = '|',
        font = font,
        background = color_dark,
        foreground = '474747',
        padding = 2,
        fontsize = 14
    )]

def get_CurrentLayout() -> list:
    return [widget.CurrentLayout(
        font = font,
        foreground = color_bright,
        background = color_dark,
        padding = 5
    )]

def get_WindowCount() -> list:
    return [widget.WindowCount(
        font = font,
        foreground = color_bright,
        background = color_dark,
        padding = 2
    )]

def get_WindowName() -> list:
    return [widget.WindowName(
        font = font,
        foreground = color_bright,
        background = color_dark,
        padding = 0
    )]

def get_Systray() -> list:
    return [widget.Systray(
        font = font,
        background = color_dark,
        padding = 5
    )]

def get_Sep() -> list:
    return [widget.Sep(
        linewidth = 0,
        padding = 6,
        foreground = color_dark,
        background = color_dark
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
            foreground = color_bright,
            background = color_bg,
            padding = 0
        ))
    elements.append(widget_elem(
        font = font,
        foreground = color_bright,
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
    +get_ArrowElement(color_dark, color1, widget.Net, dict(interface='enp3s0', format='{down}  {up} ')) \
    +get_ArrowElement(color1, color2, widget.ThermalZone, dict(                   
        fgcolor_normal = color_bright,
        crit = 70,
        format = ' {temp} '
    ), '糖') \
    +get_ArrowElement(color2, color1, widget.CPU, dict(                   
        format = '{load_percent:3.0f}% ',
    ), '') \
    +get_ArrowElement(color1, color2, widget.Memory, dict(                   
        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e htop')},
        format = '{MemPercent:3.0f}% '
    ), '') \
    +get_ArrowElement(color2, color1, widget.DF, dict(                   
        format = ' {uf:.0f}{m} ',
        visible_on_warn = False
    ), '') \
    +get_ArrowElement(color1, color2, widget.CheckUpdates, dict(                   
        update_interval = 1800,
        distro = "Arch_checkupdates",
        display_format = " {updates} ",
        no_update_string = " 0 ",
        colour_have_updates = color_bright,
        colour_no_updates = color_bright,
        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e sudo pacman -Syu')}
    ), 'ﮮ') \
    +get_ArrowElement(color2, color1, widget.KeyboardLayout, dict(                   
        configured_keyboards = ["us altgr-intl", "de"],
        fmt = ' {} ',
    ), '') \
    +get_ArrowElement(color1, color2, widget.Clock, dict(format="%A, %B %d - %H:%M "))
    

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

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
