import subprocess, os
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

######## VARIABLES #########

cmd = "mod4"
alt = "mod1"

terminal = "termite"
editor = "vim"
browser = "surf google.com"
# dmenu, feh, tty-clock, ranger, neofetch are also used in this config

colors = {
    "black" : "#1D181b",
    "white" : "#D9D9D9",
    "third" : "#3DA2FF"
}

######## AUTOSTART #########

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

######## KEYBINDING #########

keys = [
    # Launch apps
    Key([cmd], "Return", 
        lazy.spawn(terminal), 
        desc="Launch terminal"
    ),
    Key([cmd], "b", 
        lazy.spawn(browser), 
        desc="Launch browser"
    ),
    Key([cmd], "f", 
        lazy.spawn(fm), 
        desc="Launch file manager"
    ),
    Key([cmd], "space", 
        lazy.spawn('dmenu_run'), 
        desc='Run Launcher'
    ),
    Key([cmd], "c", 
        lazy.spawn("tty-clock -C 4 -c"), 
        desc="Show the clock"
    ),

    # Switch between windows
    Key([cmd], "h", 
        lazy.layout.left(), 
        desc="Move focus to left"
    ),
    Key([cmd], "l", 
        lazy.layout.right(), 
        desc="Move focus to right"
    ),
    Key([cmd], "j", 
        lazy.layout.down(), 
        desc="Move focus down"
    ),
    Key([cmd], "k", 
        lazy.layout.up(), 
        desc="Move focus up"
    ),
    Key([cmd], "q", 
        lazy.window.kill(), 
        desc="Kill focused window"
    ),

    # Switch between screens & layout
    Key([cmd], "s", 
        lazy.to_screen(0), 
        desc='Keyboard focus to monitor 1'
    ),
    Key([cmd], "d", 
        lazy.to_screen(1), 
        desc='Keyboard focus to monitor 2'
    ),
    Key([cmd], "Tab", 
        lazy.next_layout(), 
        desc="Toggle between layouts"
    ),
    Key([cmd, "shift"],"Return", 
            lazy.layout.toggle_split(), 
            desc="Toggle between split and unsplit sides of stack"
    ),

    # Move windows
    Key([cmd, "shift"], "h", 
        lazy.layout.shuffle_left(), 
        desc="Move window to the left"
    ),
    Key([cmd, "shift"], "l", 
        lazy.layout.shuffle_right(), 
        desc="Move window to the right"
    ),
    Key([cmd, "shift"], "j", 
        lazy.layout.shuffle_down(),
        desc="Move window down"
    ),
    Key([cmd, "shift"], "k", 
        lazy.layout.shuffle_up(), 
        desc="Move window up"
    ),

    # Grow windows
    Key([cmd, "control"], "h", 
        lazy.layout.grow_left(), 
        desc="Grow window to the left"
    ),
    Key([cmd, "control"], "l", 
        lazy.layout.grow_right(), 
        desc="Grow window to the right"
    ),
    Key([cmd, "control"], "j", 
        lazy.layout.grow_down(), 
        desc="Grow window down"
    ),
    Key([cmd, "control"], "k", 
        lazy.layout.grow_up(), 
        desc="Grow window up"
    ),
    Key([cmd], "n", 
        lazy.layout.normalize(),
        desc="Reset all window sizes"
    ),
    Key([alt], "h", 
        lazy.layout.shrink(), lazy.layout.decrease_nmaster(), 
        desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
    ),
    Key([alt], "l", 
        lazy.layout.grow(), lazy.layout.increase_nmaster(), 
        desc='Expand window (MonadTall), increase number in master pane (Tile)'
    ),

    # Session & config
    Key([cmd, "control"], "r", 
        lazy.reload_config(), 
        desc="Reload the config"
    ),
    Key([cmd, "control"], "q", 
        lazy.shutdown(), 
        desc="Shutdown Qtile"
    ),
    Key([cmd, "control"], "s",
        lazy.spawn(terminal + "-e" + editor + ""),
        desc="Open config file"
    )
]

######## GROUPS AND LAYOUT #########

defaultLayout='monadtall'

groups = [
    Group("1", layout=defaultLayout),
    Group("2", layout=defaultLayout),
    Group("3", layout=defaultLayout),
    Group("4", layout=defaultLayout),
    Group("5", layout=defaultLayout),
    Group("6", layout=defaultLayout)
]

grpsAzertyKeys = ["a","z","e","r","t","y"]

for i, group in enumerate(groups, 0):
    keys.extend(
        [
            # Switch between workspaces
            Key([cmd], grpsAzertyKeys[i], 
                lazy.group[group.name].toscreen(toggle=False),
                desc=f"Switch to group {group.name}"
            ),
            # Move focused window to workspace
            Key([cmd, "shift"], grpsAzertyKeys[i], 
                lazy.window.togroup(group.name), 
                desc=f"Move focused window to group {group.name}"
            )
        ]
    )

layout_theme = {
    "border_width": 2,
    "margin":7,
    "border_focus": colors["third"],
    "border_normal": colors["black"]
}

layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(),
    #layout.Columns(**layout_theme),
    #layout.Floating(**layout_theme)
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

######## SCREENS, BAR AND WIDGET #########


widget_defaults = dict(
    font="Ubuntu Mono",
    foreground= colors["white"],
    background= colors["black"] ,
    fontsize=16,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(),
    Screen(
        '''top=bar.Bar(
            widgets=[
                widget.Spacer(),
                widget.GroupBox(),
                widget.Spacer()
            ],
            size=25,
            margin=[7,7,0,7]
        )'''
    )
]

######## MOUSE & FLOATING #########
mouse = [
    Drag(
        [cmd], "Button1", 
        lazy.window.set_position_floating(), 
        start=lazy.window.get_position()),
    Drag(
        [cmd], "Button3", 
        lazy.window.set_size_floating(), 
        start=lazy.window.get_size()),
    Click(
        [cmd], "Button2", 
        lazy.window.bring_to_front()),
]

############  OTHER  #############

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
        Match(title="pcmanfs"),
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
