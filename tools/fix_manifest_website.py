import os
import re

import click

from .manifest import get_manifest_path, parse_manifest

WEBSITE_KEY_RE = re.compile(r"""(["']website["']\s*:\s*["'])([^"']*)(["'])""")


@click.command()
@click.argument("url")
@click.argument("manifest_files", nargs=-1, type=click.Path())
def main(url, manifest_files):
    for file in manifest_files:
        try:
            with open(file) as manifest_file:
                parse_manifest(manifest_file.read())
        except Exception:
            raise click.ClickException(
                "Error parsing manifest {}.".format(file)
            )
        with open(file) as manifest_file:
            manifest_str = manifest_file.read()
        new_manifest_str, n = WEBSITE_KEY_RE.subn(
            r"\g<1>" + url + r"\g<3>", manifest_str
        )
        # Create the website key if it doesn't exist
        if n == 0:
            print(f"Creating missing website key in manifest {file}.")
            if manifest_str.strip().endswith("}"):
                # Delete the closing brace, add comma, key, and close
                base_str = manifest_str.strip()[:-1].strip()
                # Ensure there's a comma before adding
                suffix = "," if not base_str.endswith(",") else ""
                new_manifest_str = f"{base_str}{suffix}\n    'website': '{url}',\n}}"
        if n > 1:
            print(f"Deleting duplicated website keys in manifest {file}.")
            # Find all the website keys and delete then all except the last one
            split_manifest = new_manifest_str.splitlines()
            duplicate_keys = [line for line in split_manifest if url in line]
            duplicate_keys.pop()
            for key in duplicate_keys:
                new_manifest_str = new_manifest_str.replace(key + "\n", "", 1)

        # Write the new manifest
        if new_manifest_str != manifest_str:
            with open(file, "w") as manifest_file:
                manifest_file.write(new_manifest_str)
