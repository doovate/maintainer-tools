import os
from pathlib import Path
from shutil import copyfile
import re

import click

WEBSITE_KEY_RE = re.compile(r"""(["']website["']\s*:\s*["'])([^"']*)(["'])""")
ADDON_FILTER = re.compile(r"^(ps_|dv_)")
TEMPLATE_INDEX = os.path.join("..", "data", "template_addon", "static", "description", "index.html")
TEMPLATE_HERO = os.path.join("..", "data", "template_addon", "static", "description", "assets", "doovate_hero.jpg")
TEMPLATE_FULL_LOGO = os.path.join("..", "data", "template_addon", "static", "description", "assets",
                                  "doovate_full_logo.png")
TEMPLATE_ICON = os.path.join("..", "data", "template_addon", "static", "description", "icon.png")

INDEX_FIRST_LINE = "<!--doovate index.html template-->"


@click.command()
def main():
    template_hash = hash(open(TEMPLATE_INDEX, 'r').read())
    # List folders in current directory and extract valid addons
    filtered_addons = [folder for folder in os.listdir(".") if ADDON_FILTER.match(folder)]


    for addon in filtered_addons:
        base_website = False
        # Create missing folder
        index_file = os.path.join(addon, "static", "description", "index.html")
        icon_file = os.path.join(addon, "static", "description", "icon.png")
        asset_folder = os.path.join(addon, "static", "description", "assets")
        hero_file = os.path.join(asset_folder, "doovate_hero.jpg")
        full_logo_file = os.path.join(asset_folder, "doovate_full_logo.png")
        if not os.path.exists(os.path.join(addon, "static", "description")):
            print(f"Creating description folder for {addon}")
            Path(addon, "static", "description").mkdir(parents=True, exist_ok=True)
        if not os.path.exists(index_file):
            print(f"Creating index.html for {addon}")
            copyfile(TEMPLATE_INDEX, index_file)
        # Read index.html and check if it's the template, if the template has been updated, replace it, else keep the existing content
        if os.path.exists(index_file):
            with open(index_file, "r") as f:
                lines = f.readlines()
            if INDEX_FIRST_LINE in lines[0] and hash(''.join(lines)) != template_hash:
                print(f"Updating index.html for {addon}")
                copyfile(TEMPLATE_INDEX, index_file)
        if not os.path.exists(asset_folder):
            print(f"Creating assets folder for {addon}")
            Path(asset_folder).mkdir(parents=True, exist_ok=True)
        if not os.path.exists(icon_file):
            print(f"Creating icon.png for {addon}")
            copyfile(TEMPLATE_ICON, icon_file)
        if not os.path.exists(hero_file):
            print(f"Creating hero image for {addon}")
            copyfile(TEMPLATE_HERO, hero_file)
        if not os.path.exists(full_logo_file):
            print(f"Creating full logo image for {addon}")
            copyfile(TEMPLATE_FULL_LOGO, full_logo_file)
