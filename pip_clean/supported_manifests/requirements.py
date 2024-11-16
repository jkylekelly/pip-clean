from pip._internal.req.req_file import parse_requirements
from pip._internal.req.constructors import install_req_from_line
from pip._internal.network.session import PipSession
from packaging.utils import NormalizedName, canonicalize_name


# This function is adapted from the pip-check-reqs project by adamtheturtle.
# Source: https://github.com/adamtheturtle/pip-check-reqs
def get_requirements_deps(filename: str) -> set[NormalizedName]:
    explicit: set[NormalizedName] = set()
    for requirement in parse_requirements(
        filename,
        session=PipSession(),
    ):
        requirement_name = install_req_from_line(
            requirement.requirement,
        ).name
        explicit.add(canonicalize_name(requirement_name))
    return explicit
