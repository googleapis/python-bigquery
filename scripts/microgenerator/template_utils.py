# TODO: Add a header if needed.

import os
import jinja2


def load_template(template_name):
    """
    Loads a Jinja2 template from the same directory as the script.
    """
    template_dir = os.path.dirname(os.path.abspath(__file__))
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        trim_blocks=True, # prevents blank lines by removing '\n' after block tags (e.g. {% if condition %}\n)
        lstrip_blocks=True, # prevents unwanted empty spaces before lines of text by removing non-explicit spaces, tabs, etc
    )
    return env.get_template(template_name)
