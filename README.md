# Marble shell theme
Shell theme for GNOME. Fork of the https://www.pling.com/p/1939902/.

## Screenshots
Icon theme: https://github.com/vinceliuice/Colloid-icon-theme

Wallpaper: https://www.androidpolice.com/chromebook-chrome-os-wallpapers/#radiance

#### Overview
![Overview look](./readme-images/overview.png?raw=true "Overview look")
#### Panel
![Panel look](./readme-images/panel.png?raw=true "Panel look")
#### Quick settings
![Quick settings look](./readme-images/qs.png?raw=true "Quick settings look")
#### Calendar & notifications
![Calendar & notifications look](./readme-images/notifications.png?raw=true)
#### Dash ([Dash To Dock](https://extensions.gnome.org/extension/307/dash-to-dock/ "Dash To Dock"))
![Dash look](./readme-images/dash.png?raw=true "Dash look")

## Requirements
1. GNOME 42+. I do not guarantee correct functionality on older versions.
2. [User Themes](https://extensions.gnome.org/extension/19/user-themes/ "User Themes") extension.
3. [GNOME Tweaks](https://gitlab.gnome.org/GNOME/gnome-tweaks "GNOME Tweaks").
4. Python 3.10+.

## Installation
1. Open terminal;
2. Clone git and change directory:
```shell
git clone https://github.com/imarkoff/Marble-shell-theme.git && cd Marble-shell-theme
```
3. Run the program: 
```shell
python install.py
```
4. Folllow instructions inside the program;
5. After successful file creation open up GNOME Tweaks, go to `Appearance - Themes - Shell`;
6. Select shell theme you want.
## Installation tweaks
#### Install default color
| Option | Theme mode (optional) | Description |
| ------------ | ------------ | ------------ |
| -A, --all |  | Install all available accent colors. Light & dark mode. |
| --red |  | red theme only |
| --pink |  | pink theme only |
| --purple |  | purple theme only |
| --blue |  | blue theme only |
| --green |  | green theme only |
| --yellow |  | pink theme only |
|--gray |  | gray theme only |
#### Install custom color
| Option | Hue degree | Theme name (optional) | Theme mode (optional) | Description |
| ------------ | ------------ | ------------ | ------------ | ------------ |
| --hue |  |  |  |Generate theme from Hue prompt [0 - 360] |
#### Theme mode
| Option | Secondary option | Description |
| ------------ | ------------ | ------------ |
|  | --light | light theme only |
|  | --dark | dark theme only |
#### Examples
| Command | Description |
| ------------ | ------------ |
| -A | Install all accent colors with light & dark mode |
| --all --dark | Install all accent colors with dark mode only |
| --purple --light | Install purple accent color with light mode only |
| --hue 180 | Install hue=180 accent color with light & dark mode |
| --hue 145 coldgreen --dark | Install hue=145 coldgreen accent color with dark mode only |
