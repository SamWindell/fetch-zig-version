import urllib.request
import shutil
import os
import argparse
import platform
from pathlib import Path

parser = argparse.ArgumentParser(
    prog='Install Zig version', description="Downloads and extracts a specific version of zig into a directory of your choosing. Doesn't check the minisig. Allows for multiple versions. A symlink to will be created.")
parser.add_argument("version", help="For example 0.12.0-dev.1769+bf5ab5451")
parser.add_argument("install_dir", help="Where to install zig too. The specific version will be installed to a subdirectory there (if it doesn't already exist). Then a 'zig' symlink will be created pointing into that specific version the base of the dir.")
args = parser.parse_args()

base_url = "https://ziglang.org/builds/zig"

infos = {
    "Windows": {
        "name": "windows-x86_64",
        "archive_ext": ".zip",
        "exe_ext": ".exe",
    },
    "Linux": {
        "name": "linux-x86_64",
        "archive_ext": ".tar.xz",
        "exe_ext": "",
    },
    "Darwin": {
        "name": "macos-aarch64",
        "archive_ext": ".tar.xz",
        "exe_ext": "",
    },
}

info = infos[platform.system()]

full_url = "{}-{}-{}{}".format(base_url,
                               info["name"], args.version, info["archive_ext"])

Path(args.install_dir).mkdir(parents=True, exist_ok=True)

archive_name = os.path.basename(full_url)
extracted_archive_path = os.path.join(
    args.install_dir, os.path.basename(full_url)[:-len(info["archive_ext"])])

if not os.path.exists(extracted_archive_path):
    urllib.request.urlretrieve(full_url, archive_name)
    shutil.unpack_archive(archive_name, args.install_dir)
    os.remove(archive_name)

# NOTE: on Windows you will probably need to enable permission to create symlinks: https://www.scivision.dev/windows-symbolic-link-permission-enable/
os.symlink(os.path.join(extracted_archive_path, "zig" + info["exe_ext"]),
           os.path.join(args.install_dir, "zig" + info["exe_ext"]))
