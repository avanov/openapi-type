{
    pkgs ? import (builtins.fetchTarball {
             # Descriptive name to make the store path easier to identify
             name = "openapi-type-nixpkgs";
             # Commit hash for nixos-unstable as of 2021-04-29
             url = https://github.com/NixOS/nixpkgs/archive/f4c4ddae041241dc0c9d5628038826103958fdfc.tar.gz;
             # Hash obtained using `nix-prefetch-url --unpack <url>`
             sha256 = "192bnsjrccvix9kd1cg895alghpdd73hdpis2s03b1p2rn1y2pkp";
           }) {}
,   pyVersion ? "39"
,   isDevEnv  ? true
}:

let

    python = pkgs."python${pyVersion}Full";
    pythonPkgs = pkgs."python${pyVersion}Packages";
    devLibs = if isDevEnv then [ pythonPkgs.twine pythonPkgs.wheel ] else [ ];
in

# Make a new "derivation" that represents our shell
pkgs.stdenv.mkDerivation {
    name = "openapi-type";

    # The packages in the `buildInputs` list will be added to the PATH in our shell
    # Python-specific guide:
    # https://github.com/NixOS/nixpkgs/blob/master/doc/languages-frameworks/python.section.md
    buildInputs = with pkgs; [
        # see https://nixos.org/nixos/packages.html
        # Python distribution
        python
        pythonPkgs.virtualenv
        ncurses
        libxml2
        libxslt
        libzip
        zlib
        which
        jq
    ] ++ devLibs;
    shellHook = ''
        # set SOURCE_DATE_EPOCH so that we can use python wheels
        export SOURCE_DATE_EPOCH=$(date +%s)

        export VENV_DIR="$PWD/.venv${pyVersion}"

        export PATH=$VENV_DIR/bin:$PATH
        export PYTHONPATH=""
        export LANG=en_US.UTF-8

        # https://python-poetry.org/docs/configuration/
        export PIP_CACHE_DIR="$PWD/.local/pip-cache${pyVersion}"

        # Setup virtualenv
        if [ ! -d $VENV_DIR ]; then
            virtualenv $VENV_DIR
            $VENV_DIR/bin/python -m pip install -e $PWD
            $VENV_DIR/bin/python -m pip install -r $PWD/requirements/test.txt
            $VENV_DIR/bin/python -m pip install -r $PWD/requirements/extras/*
        fi
    '';
}