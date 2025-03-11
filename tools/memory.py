from cat.mad_hatter.decorators import tool

from cat.plugins.multicat.refactory.stray_cat.son import SonStrayCat
from cat.log import log


@tool(
    return_direct=True,
    examples=[
        "What file you know?"
    ]
)
def get_file_list(tool_input, cat):
    """What file you know? Input is None."""

    log.error(f"cat: {cat}")

    files = cat.get_file_list()

    return f"You have this files:\n {files}"