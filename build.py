from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")


name = "slackmoji"
default_task = "install_dependencies"


@init
def set_properties(project):
    project.depends_on_requirements("requirements.lock.txt")
