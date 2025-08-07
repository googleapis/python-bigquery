import os
import jinja2


def load_template(template_name):
    """
    Loads a Jinja2 template from the same directory as the script.
    """
    template_dir = os.path.dirname(os.path.abspath(__file__))
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    return env.get_template(template_name)
