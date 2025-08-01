with import <nixpkgs> {};
mkShell.override { stdenv = llvmPackages_19.stdenv; } {
    buildInputs = [
        (python3.withPackages (ps: with ps; [
            beautifulsoup4
            black
            flake8
            flask
            lxml
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
