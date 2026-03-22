#!/usr/bin/env bash
# clean_py_multi.sh  –  usage:
#   ./clean_py_multi.sh file1.py dir/*.py   # writes cleaned files with “.clean.py” suffix
#   ./clean_py_multi.sh -i file1.py        # edit files in-place (creates backup *.bak)

# ---------- Helper: clean a single file ----------
clean_file() {
    local src="$1"
    local dst="$2"

    awk '
      BEGIN { in_doc=0 }

      /"""/ {
        n = gsub(/"""/, "&")
        for (i=0; i<n; i++) in_doc = !in_doc
        print
        next
      }

      in_doc { print; next }

      {
        line = $0
        while (match(line, /([^'"'"'"]*("[^"]*"|'"'"'[^'"'"']*'"'"'))*#/) ) {
          line = substr(line, 1, RSTART-1)
          break
        }
        sub(/[ \t]+$/, "", line)
        if (line == "") next
        print line
      }
    ' "$src" > "$dst"
}

# ---------- Argument parsing ----------
inplace=false
while [[ "$1" == -* ]]; do
    case "$1" in
        -i|--inplace) inplace=true; shift ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
done

if [[ $# -eq 0 ]]; then
    echo "Usage: $0 [-i] <file-or-dir> [...]" >&2
    exit 1
fi

# ---------- Process each argument ----------
for path in "$@"; do
    if [[ -d "$path" ]]; then
        # Recursively find *.py files in a directory
        while IFS= read -r -d '' pyfile; do
            if $inplace; then
                tmp="${pyfile}.tmp"
                clean_file "$pyfile" "$tmp" && mv "$pyfile" "${pyfile}.bak" && mv "$tmp" "$pyfile"
            else
                clean_file "$pyfile" "${pyfile%.py}.clean.py"
            fi
        done < <(find "$path" -type f -name "*.py" -print0)
    elif [[ -f "$path" && "$path" == *.py ]]; then
        if $inplace; then
            tmp="${path}.tmp"
            clean_file "$path" "$tmp" && mv "$path" "${path}.bak" && mv "$tmp" "$path"
        else
            clean_file "$path" "${path%.py}.clean.py"
        fi
    else
        echo "Skipping non-Python file: $path" >&2
    fi
done
