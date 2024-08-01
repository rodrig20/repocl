import argparse
import tempfile
import shutil
import os
from git import Repo


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise argparse.ArgumentTypeError(f"{string} is not a valid directory")

def get_folder_name(folder_name):
    if not os.path.exists(folder_name):
        return os.path.abspath(folder_name)
    else:
        counter = 1
        while True:
            new_folder_name = f"{folder_name} ({counter})"
            if not os.path.exists(new_folder_name):
                return os.path.abspath(new_folder_name)
            counter += 1

parser = argparse.ArgumentParser(description ='Process some integers.')

parser.add_argument('git_repository', type=str, help='Url fromGit Repository')
parser.add_argument('-o', '--output-path', type=str, default='./', help='Output folder')
parser.add_argument('-d', '--directory-on-repository', type=str, default='./', help='Directory on Repository to obtain')


args = parser.parse_args()
with tempfile.TemporaryDirectory() as tmpdirname:
    repo_name = ".".join(args.git_repository.split("/")[-1].split(".")[:-1])
    print(f"> Clonning {repo_name}")
    Repo.clone_from(args.git_repository, tmpdirname,)
    path_on_repo = dir_path(os.path.join(tmpdirname, args.directory_on_repository))
    output_folder =  get_folder_name(os.path.join(args.output_path + repo_name))
    
    shutil.move(path_on_repo, output_folder)
    
    print(f"> \"{repo_name}\" segment successfully cloned to \"{output_folder}\"")
