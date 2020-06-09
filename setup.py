import sys
from cx_Freeze import setup, Executable

executables = [Executable("read_incident_flows_xml_TimeStamp.py"),Executable("run_script_v_02.py"),Executable("encryption.py")]

packages = ["idna","subprocess","datetime","pathlib","xlrd","sys","fnmatch","os","paramiko","re","json","xml.etree.ElementTree","logging","time","cffi","base64","csv","pysnow","dicttoxml"]
options = {
    'build_exe': {
        'packages':packages
    },
}

setup(
    name = "Custom_Orch",
    options = options,
    version = "1.0",
    description = 'Custom_Orch',
    executables = executables
)

