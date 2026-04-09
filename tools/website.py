import os
from pathlib import Path
from shutil import copyfile
import re

import click

ADDON_FILTER = re.compile(r"^(ps_|dv_)")
_DATA_DIR = Path(__file__).parent / "template_addon_static" / "description"
TEMPLATE_INDEX = str(_DATA_DIR / "index.html")
TEMPLATE_HERO = str(_DATA_DIR / "assets" / "doovate_hero.jpg")
TEMPLATE_FULL_LOGO = str(_DATA_DIR / "assets" / "doovate_full_logo.png")
TEMPLATE_ICON = str(_DATA_DIR / "icon.png")

INDEX_FIRST_LINE = "<!--doovate index.html template-->"


@click.command()
def main():
    # Calculate template hash, this is used to check if the template has been updated
    template_hash = hash(open(TEMPLATE_INDEX, "r").read())

    # List folders in current directory and extract valid addons
    filtered_addons = [
        folder for folder in os.listdir(".") if ADDON_FILTER.match(folder)
    ]
    changed = False
    for addon in filtered_addons:
        # Create missing folder
        index_file = os.path.join(addon, "static", "description", "index.html")
        icon_file = os.path.join(addon, "static", "description", "icon.png")
        asset_folder = os.path.join(addon, "static", "description", "assets")
        hero_file = os.path.join(asset_folder, "doovate_hero.jpg")
        full_logo_file = os.path.join(asset_folder, "doovate_full_logo.png")
        if not os.path.exists(os.path.join(addon, "static", "description")):
            print(f"Creating description folder for {addon}")
            Path(addon, "static", "description").mkdir(parents=True, exist_ok=True)
            changed = True
        if not os.path.exists(index_file):
            print(f"Creating index.html for {addon}")
            copyfile(TEMPLATE_INDEX, index_file)
            changed = True
        # Read index.html and check if it's the template, if the template has been updated, replace it, else keep the existing content
        if os.path.exists(index_file):
            with open(index_file, "r") as f:
                lines = f.readlines()
            if INDEX_FIRST_LINE in lines[0] and hash("".join(lines)) != template_hash:
                print(f"Updating index.html for {addon}")
                copyfile(TEMPLATE_INDEX, index_file)
                changed = True
        if not os.path.exists(asset_folder):
            print(f"Creating assets folder for {addon}")
            Path(asset_folder).mkdir(parents=True, exist_ok=True)
            changed = True
        if not os.path.exists(icon_file):
            print(f"Creating icon.png for {addon}")
            copyfile(TEMPLATE_ICON, icon_file)
            changed = True
        if not os.path.exists(hero_file):
            print(f"Creating hero image for {addon}")
            copyfile(TEMPLATE_HERO, hero_file)
            changed = True
        if not os.path.exists(full_logo_file):
            print(f"Creating full logo image for {addon}")
            copyfile(TEMPLATE_FULL_LOGO, full_logo_file)
            changed = True
    if changed:
        raise SystemExit(1)
