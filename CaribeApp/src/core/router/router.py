import flet as ft

from enum import Enum
from src.modules.pullovers.container.pullovers import Pullovers
from src.modules.about.container.about import About
from src.core.router.pages import Pages
from src.core.components.sidebar import Sidebar
from src.core.components.navbar import Navbar


def initial_view(page: ft.Page):
    routes = {
        Pages.PULLOVERS: Pullovers(page),
        Pages.ABOUT: About(),
    }

    ALL_VIEWS = [
        ft.View(
            "/",
            controls=[routes[Pages.PULLOVERS]],
        ),
        ft.View(
            "/about",
            controls=[routes[Pages.ABOUT]],
        ),
    ]

    def on_route_change(page: ft.Page, e: ft.RouteChangeEvent):
        print(f"Route changed to: {e.route}")
        for view in ALL_VIEWS:
            if view.route == e.route:
                page.controls = view.controls

        page.update()

    page.on_route_change = lambda e: on_route_change(page, e)
    page.go(Pages.PULLOVERS.value)