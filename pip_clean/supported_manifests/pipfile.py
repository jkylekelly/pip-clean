from pipfile import Pipfile
from packaging.utils import NormalizedName, canonicalize_name


def get_pipfile_deps(filename: str) -> set[NormalizedName]:
    explicit: set[NormalizedName] = set()

    parsed = Pipfile.load(filename=filename)
    # Only capture production dependencies (default)
    dep_list = parsed.data["default"]

    for dep in dep_list.keys():
        explicit.add(canonicalize_name(dep))
    return explicit
