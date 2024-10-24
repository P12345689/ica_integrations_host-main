#!/bin/bash

# Author: Mihai Criveti
# Description: download, resize an SVG file to 48x48 pixels, extract its content, and produce a JSON object with the SVG properly formatted as a string.
#   produce a JSON object with the SVG properly formatted as a string
#   for use with Watson Orchestrate
# Reference: https://www.ibm.com/docs/en/watson-orchestrate?topic=skills-understanding-x-properties#adding-an-icon-to-the-app
# Usage: ./svg_to_json.sh [--verbose] [--resize] <path_to_svg_file_or_url>

# Default settings
verbose=0
resize=0

# Function to log basic messages
basic_log() {
    echo "$1"
}

# Function to check if required tools are installed
check_dependencies() {
    local dependencies=('convert' 'jq' 'curl')
    local missing=0
    for dep in "${dependencies[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            echo "Error: Required tool $dep is not installed." >&2
            missing=1
        fi
    done
    if [ $missing -eq 1 ]; then
        echo "Please install the missing dependencies and try again." >&2
        exit 1
    fi
}

# Function to download SVG from URL
download_svg() {
    local url="$1"
    local temp_file=$(mktemp "${TMPDIR:-/tmp/}svg_download.XXXXXX.svg")
    if [[ $verbose -eq 1 ]]; then
        if ! curl -vL "$url" -o "$temp_file"; then
            echo "Error: Failed to download the file. Check the URL and network connectivity." >&2
            [ -f "$temp_file" ] && rm "$temp_file"
            exit 1
        fi
    else
        if ! curl -sL "$url" -o "$temp_file"; then
            echo "Error: Failed to download the file. Check the URL and network connectivity." >&2
            [ -f "$temp_file" ] && rm "$temp_file"
            exit 1
        fi
    fi
    echo "$temp_file"
}

# Function to resize SVG using ImageMagick
resize_svg() {
    local file="$1"
    basic_log "Resizing SVG..."
    if ! convert "$file" -resize 48x48 "$file"; then
        echo "Error: Failed to resize the SVG file." >&2
        exit 1
    fi
}

# Function to extract SVG content and format it for JSON
format_svg_for_json() {
    local file="$1"
    local svg_content
    svg_content=$(tr -d '\n' < "$file")
    echo "$svg_content"
}

# Main function
main() {
    # Parse command-line options
    while [[ "$1" =~ ^- && ! "$1" == "--" ]]; do case $1 in
        --verbose )
            verbose=1
            shift ;;
        --resize )
            resize=1
            shift ;;
        -- )
            shift; break ;;
        * )
            echo "Error: Invalid option: $1" >&2
            exit 1 ;;
    esac; done

    if [ $# -eq 0 ]; then
        echo "Usage: $0 [--verbose] [--resize] <path_to_svg_file_or_url>" >&2
        exit 1
    fi

    local svg_source=$1
    local svg_file

    # Check if required tools are installed
    check_dependencies

    # Determine if the source is a URL or a local file
    if [[ $svg_source =~ ^https?:// ]]; then
        svg_file=$(download_svg "$svg_source")  # Capture the file path correctly
    elif [ -f "$svg_source" ]; then
        svg_file=$svg_source
    else
        echo "Error: File does not exist and URL is not valid: $svg_source" >&2
        exit 1
    fi

    # Resize the SVG file if requested
    if [[ $resize -eq 1 ]]; then
        resize_svg "$svg_file"
    else
        basic_log "Skipping resize as per user request."
    fi

    # Format SVG content for JSON
    basic_log "Formatting SVG content for JSON..."
    local svg_json_content
    svg_json_content=$(format_svg_for_json "$svg_file")

    # Create JSON object using jq
    local json_output
    json_output=$(echo "{\"info\": {\"x-ibm-application-icon\": \"$svg_json_content\"}}" | jq .)

    # Output the final JSON
    echo "$json_output"

    # Clean up downloaded file if it was from a URL
    [[ $svg_source =~ ^https?:// ]] && rm "$svg_file"
}

# Run the main function with all provided arguments
main "$@"
