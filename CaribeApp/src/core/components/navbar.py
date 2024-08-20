import flet as ft
from src.lib.findView import find_view


class Navbar(ft.AppBar):
    def __init__(
        self,
        /,
        page: ft.Page,
        title: str = "Caribe Demo",
    ) -> None:

        ft.AppBar.__init__(self)
        self.page = page
        self.leading = ft.IconButton(
            ft.icons.MENU_SHARP,
            on_click=lambda _: {
                setattr(find_view(self.page).drawer, "open", True),
                find_view(self.page).drawer.update(),
            },
            icon_size=24,
        )

        self.title = ft.Text(title)
        self.center_title = False

        self.switchComponent = ft.Switch(
            thumb_icon=(
                ft.cupertino_icons.SUN_MAX
                if self.page.theme_mode == ft.ThemeMode.LIGHT
                else ft.cupertino_icons.MOON
            ),
            active_color=("#210339"),
            track_color=(
                ft.colors.ORANGE_600
                if self.page.theme_mode == ft.ThemeMode.LIGHT
                else "#210339"
            ),
            track_outline_color="transparent",
            inactive_thumb_color=(ft.colors.ORANGE_900),
            on_change=self.switch_theme,
        )

        self.actions = [self.switchComponent]

    def switch_theme(self, _) -> None:
        self.page.theme_mode = (
            ft.ThemeMode.DARK
            if self.page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        self.switchComponent.thumb_icon = (
            ft.cupertino_icons.SUN_MAX
            if self.page.theme_mode == ft.ThemeMode.LIGHT
            else ft.cupertino_icons.MOON
        )

        self.switchComponent.track_color = (
            ft.colors.ORANGE_600
            if self.page.theme_mode == ft.ThemeMode.LIGHT
            else "#210339"
        )

        self.page.update()
