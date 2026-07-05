"""Shocktail UI layer — enterprise market intelligence theme."""

from .theme import inject_theme
from .components import render_hero, render_platform_stats, render_vs_alphasense

__all__ = [
    "inject_theme",
    "render_hero",
    "render_platform_stats",
    "render_vs_alphasense",
]