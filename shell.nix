with import <nixpkgs> {};
mkShell.override { stdenv = llvmPackages_19.stdenv; } {
    buildInputs = [
        (python3.withPackages (ps: with ps; [
            black
            flake8
            flask
            numpy
            pandas
            pykakasi
        ]))
        html-tidy
        jq
        nodePackages.jshint
        nodePackages.typescript
        tailwindcss
    ];
    shellHook = ''
        . .shellhook
    '';
}
