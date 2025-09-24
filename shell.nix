{ pkgs ? import <nixpkgs> {} }:
(pkgs.buildFHSEnv {
  name = "samsung_remote_dev";
  targetPkgs = pkgs: [
    pkgs.gcc
    pkgs.python313
    pkgs.python313.pkgs.virtualenv
    pkgs.ruff
  ];

  profile = ''

    source .venv/bin/activate
  '';

  runScript = ''

    if [ ! -d .venv ]; then
      python -m venv .venv
      source .venv/bin/activate
      pip install -e ".[dev]"
    fi

    exec bash --login
  '';
}).env
