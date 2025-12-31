#!/usr/bin/env bash
set -euo pipefail

##################################################
#                  utils function                #
##################################################

on_sigint() {
# -------------------------------------------------
# Prompt until a string matches a supplied regex.
# -------------------------------------------------
    echo -e "\n🛑  Script interrupted."
    exit 130   # 130 = 128 + SIGINT
}

next_index() {
# -------------------------------------------------
# Find the highest numeric prefix (e.g. 1.foo, 2.bar, 10.baz)
# in a given directory and output that value + 1.
# -------------------
    local dir=$1
    local max=0

    if [[ -z $dir || ! -d $dir ]]; then
        echo "Error: supply a valid directory."
        return 1
    fi

    for entry in "$dir"/*; do
        [[ -e $entry ]] || continue
        name=$(basename "$entry")
        if [[ $name =~ ^([0-9]+)\. ]]; then
            num=${BASH_REMATCH[1]}
            (( num > max )) && max=$num
        fi
    done

    next_index_stage=$((max + 1))
}

prev_folder() {
# -------------------------------------------------
# Given a directory that contains entries named
#   1.xxx   2.xxx   3.xxx   …
# and a current index, print the name of the
# previous folder (index‑1). If the current folder is
# the first one, report that there is no previous entry.
# -------------------------------------------------

    local base_dir=$1
    local current=$2

    if (( current <= 1 )); then
        echo "No previous folder (already at the first entry)."
        return 1
    fi

    local target=$((current - 1))
    ## Build a glob that matches the exact numeric prefix
    local pattern="${base_dir}/${target}.*"

    ## Use globbing to find the matching entry (should be exactly one)
    shopt -s nullglob
    matches=($pattern)
    shopt -u nullglob

    if (( ${#matches[@]} == 0 )); then
        echo "Previous folder not found for index $target."
        return 1
    fi

    previous_stage_folder="${matches[0]##*/}"
}

##################################################
#                  prompt function                #
##################################################

prompt_stage() {
# -------------------------------------------------
# Prompt until a string matches a supplied regex.
# Arguments:
#   $1 – name of variable to store the result
# -------------------------------------------------
    local __resultvar=$1
    local prompt_msg="Please, enter a stage name : " 
    local pattern='^[a-zA-Z0-9_]{3,20}$'
    local input

    while true; do
        read -p "$prompt_msg" input
        input=$(echo "$input" | xargs)

        if [[ -z $input ]]; then
            echo "❌  Input cannot be empty."
        elif [[ $input =~ $pattern ]]; then
            printf -v "$__resultvar" '%s' "$input"
            break
        else
            echo "❌  Input does not match required format."
        fi
    done
}

confirm_or_fallback() {
# -------------------------------------------------
# confirm_or_fallback <prompt> <callback> [callback_args...]
#   * Shows <prompt> and reads a yes/no answer.
#   * “y”/“yes” → return 0 (caller proceeds).
#   * “n”/“no”  → invoke <callback> with the optional
#                 arguments that follow it, then return 1.
# -------------------------------------------------
    local prompt_msg=$1
    shift
    local callback=$1
    shift
    local callback_args=("$@")
    local reply

    while true; do
        read -p "$prompt_msg (y/n): " reply
        case "${reply,,}" in
            y|yes)  return 0 ;;
            n|no)   "$callback" "${callback_args[@]}" ; return 1 ;;
            *)      echo "Please answer y or n." ;;
        esac
    done
}

repeat_until_yes() {
# -------------------------------------------------
# repeat_until_yes <prompt> <fallback> [fallback_args...]
#   * Shows <prompt> and reads a yes/no answer.
#   * On “yes” → returns 0.
#   * On “no”  → runs the fallback (with optional args) and
#                then asks the same question again.
# -------------------------------------------------
    local prompt_msg=$1
    shift
    local fallback=$1
    shift
    local fallback_args=("$@")

    while true; do
        if confirm_or_fallback "$prompt_msg" "$fallback" "${fallback_args[@]}"; then
            return 0
        fi
    done
}

##################################################
#          markdown rendering function           #
##################################################

render_template() {
# -------------------------------------------------
# render_template <template_file> <output_file>
#   Replaces {{placeholder}} tokens with the
#   values of environment variables of the same name.
# -------------------------------------------------
    local tmpl=$1 out=$2

    local content
    content=$(<"$tmpl")

    ## Find all placeholders (e.g. {{title}})
    while [[ $content =~ \{\{([A-Za-z_][A-Za-z0-9_]*)\}\} ]]; do
        var="${BASH_REMATCH[1]}"
        val="${!var:-}"
        esc_val=$(printf '%s' "$val" | sed 's/[&/\]/\\&/g')
        content=$(printf '%s' "$content" | sed "0,/{{${var}}}/s//${esc_val}/")
    done

    printf '%s' "$content" > "$out"
}

##################################################
#                  main function                 #
##################################################

## script instruction
trap on_sigint SIGINT
echo "▶ To abort anytime, press Ctrl-C to exit script"

## Ask user stage name value
prompt_stage stage_name 
repeat_until_yes "Stage name '${stage_name}', will be use, confirm ?" prompt_stage stage_name

## Get the highest index stage value
next_index "."

## create a stage (folder and markdown)
export new_stage_name="${next_index_stage}.${stage_name}"
export date="$(date '+%Y-%m-%d')"
mkdir -p ${new_stage_name}
render_template "scripts/template.md" "${new_stage_name}/${new_stage_name}.md"
echo -e "\n✅ New stage markdown successfully created from template"

## copy previous content except mardown file
prev_folder "." $next_index_stage
rsync -avq --exclude='*.md' "$previous_stage_folder"/ "$new_stage_name"/
echo "✅ Content from previous stage (${previous_stage_folder}) successfully copied to new stage folder (${new_stage_name})"
echo "📝 You can now edit new stage markdown at '${new_stage_name}/${new_stage_name}.md'"
echo "📑 Don't forget to edit the main readme.md file to add this new stage in the table"