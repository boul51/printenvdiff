#!/usr/bin/env python3

import argparse
import os
import subprocess


def env_string_to_dict(env_string):
    ret = {}
    lines = env_string.splitlines()
    for line in lines:
        tokens = line.split("=", 1)
        ret[tokens[0]] = tokens[1]
    return ret


def get_env_string(env_script=None):
    if env_script:
        command = ". " + env_script + "; env"
    else:
        command = "env"
    return subprocess.run(command, capture_output=True, shell=True).stdout.decode("utf8")


def env_dict_diff(old, new, no_compound):
    ret = {}
    for key in new.keys():
        if key not in old.keys():
            ret[key] = new[key]
        else:
            if old[key] != new[key]:
                if no_compound:
                    ret[key] = new[key]
                else:
                    if new[key].startswith(old[key]):
                        ret[key] = "${" + key + "}" + new[key].split(old[key])[1]
                    elif new[key].endswith(old[key]):
                        ret[key] = new[key].split(old[key])[0] + "${" + key + "}"
                    elif old[key] in new[key]:
                        ret[key] = new[key].split(old[key])[0] + "${" + key + "}" + new[key].split(old[key])[1]
                    else:
                        ret[key] = new[key]

    return ret


def print_dict(env_dict):
    keys = sorted(env_dict.keys())
    for key in keys:
        print(key + "=" + env_dict[key].strip())


def main():
    description = '''\
Print modified environment variables after a script that modifies the environment has been sourced.
It was written to insert yocto environment variables into QtCreator, but it should be usable for different things.
'''

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--script", required=True,
                        help="Path of the script that modifies the environment")
    parser.add_argument("--no-compound", action="store_true",
                        help="Do not print new variables as a compound of old variables, eg. PATH=XXX:${PATH}:YYY")
    args = parser.parse_args()

    original_env_dict = env_string_to_dict(get_env_string())
    new_env_dict = env_string_to_dict(get_env_string(args.script))
    diff = env_dict_diff(original_env_dict, new_env_dict, args.no_compound)
    print_dict(diff)


if __name__ == "__main__":
    main()