"""Shocktail UI layer — enterprise market intelligence theme."""

from .theme import inject_theme
from .components import render_hero, render_platform_stats, render_value_props

__all__ = [
    "inject_theme",
    "render_hero",
    "render_platform_stats",
    "render_value_props",
]