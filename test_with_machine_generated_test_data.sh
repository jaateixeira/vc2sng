#!/bin/bash

# ============================================
# Configuration
# ============================================

# Configuration - parameters for vc2sng
#GRAPH1="test-data/3nodes_3edges.graphML"
#GRAPH2="test-data/4nodes_4edges.graphML"

GRAPH1="test-data/4nodes_4edges.graphML"
GRAPH2="test-data/4nodes_6edges.graphML"

AFFILIATION_KEY="affiliation"
COLOR_DICT="org-color-dict/firm_color_dict.json"


# Function to validate configuration files
validate_configuration() {
    local all_valid=true

    echo "Validating configuration files..."
    echo "================================"

    # Check GRAPH1
    if [ -f "$GRAPH1" ]; then
        echo -e "${GREEN}✓ $GRAPH1 exists${NC}"
    else
        echo -e "${RED}✗ $GRAPH1 NOT FOUND${NC}"
        all_valid=false
    fi

    # Check GRAPH2
    if [ -f "$GRAPH2" ]; then
        echo -e "${GREEN}✓ $GRAPH2 exists${NC}"
    else
        echo -e "${RED}✗ $GRAPH2 NOT FOUND${NC}"
        all_valid=false
    fi

    # Check COLOR_DICT (optional - warn if missing but don't fail)
    if [ -f "$COLOR_DICT" ]; then
        echo -e "${GREEN}✓ $COLOR_DICT exists${NC}"
    else
        echo -e "${YELLOW}! $COLOR_DICT not found (optional)${NC}"
    fi

    echo "================================"

    if [ "$all_valid" = true ]; then
        echo -e "${GREEN}All required files exist. Validation passed.${NC}"
        return 0
    else
        echo -e "${RED}Validation failed. Missing required files.${NC}"
        return 1
    fi
}

# Run validation
validate_configuration || exit 1


# ============================================
# Color Definitions
# ============================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# ============================================
# Utility Functions
# ============================================

print_header() {
    echo -e "${CYAN}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                     Testing vc2sng TOOL                    ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_section() {
    echo -e "${YELLOW}┌─────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${YELLOW}│ $1${NC}"
    echo -e "${YELLOW}└─────────────────────────────────────────────────────────────┘${NC}"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_command() {
    echo -e "${MAGENTA}▶${NC} Running: ${WHITE}$1${NC}"
}

print_separator() {
    echo -e "${CYAN}──────────────────────────────────────────────────────────────${NC}"
}




# ============================================
# Main Script
# ============================================

print_header

print_section "Checking configuration"

print_separator
echo -e "$GRAPH1"
echo -e "$GRAPH2"
echo -e "$AFFILIATION_KEY"
echo -e "$COLOR_DICT"
print_separator


# ============================================
# Command 1:  Comparing the network in one direction
# ============================================

print_info "Visualizing diff --   $GRAPH1  $GRAPH2 "

print_command  "./vc2sng.py  -l  --color-dict=$COLOR_DICT $GRAPH1  $GRAPH2"
./vc2sng.py  -l --color-dict=$COLOR_DICT  $GRAPH1  $GRAPH2


if [ $? -eq 0 ]; then
    print_success "Diff visualized successfully"
else
    print_warning "Diff visualized with warnings"
fi

print_info "Visualizing diff --  $GRAPH2  $GRAPH1"
print_command  "./vc2sng.py  -l  --color-dict=$COLOR_DICT  $GRAPH2  $GRAPH1"
./vc2sng.py  -l --color-dict=$COLOR_DICT  $GRAPH2  $GRAPH1

if [ $? -eq 0 ]; then
    print_success "Diff visualized successfully"
else
    print_warning "Diff visualized with warnings"
fi