#!/bin/bash

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
# Configuration
# ============================================

# Configuration - parameters for vc2sng
GRAPH1="test-data/networks-of-individuals/tensorFlowGitLog-2015-git-log-outpuyt-by-Jose.IN.NetworkFile.graphML"
GRAPH2="test-data/networks-of-individuals/tensorFlowGitLog-2016-git-log-outpuyt-by-Jose.IN.NetworkFile.graphML"
COLOR_DICT="org-color-dict/firm_color_dict.json"
AFFILIATION_KEY="affiliation"

# ============================================
# Main Script
# ============================================

print_header

print_section "Checking configuration"

print_separator
echo -e "$GRAPH1"
echo -e "$GRAPH2"
echo -e "$COLOR_DICT"
echo -e "$AFFILIATION_KEY"
print_separator


# ============================================
# Command 1: Visualizing the networks to compare
# ============================================
print_section "visualizing the networks to compare"

print_info "Visualizing graph 1before comparing "


print_command ../ScrapLogGit2Net/formatFilterAndViz-nofi-GraphML.py $GRAPH1

../ScrapLogGit2Net/formatFilterAndViz-nofi-GraphML.py  -lp $GRAPH1


if [ $? -eq 0 ]; then
    print_success "Graph1 visualized successfully"
else
    print_warning "Graph1 visualized with warnings"
fi


print_separator

print_info "Visualizing graph 2 before comparing "


print_command ../ScrapLogGit2Net/formatFilterAndViz-nofi-GraphML.py $GRAPH2

../ScrapLogGit2Net/formatFilterAndViz-nofi-GraphML.py  -lp $GRAPH2


if [ $? -eq 0 ]; then
    print_success "Graph2 visualized successfully"
else
    print_warning "Graph2 visualized with warnings"
fi
print_separator


# ============================================
# Command 2: Comparing the networks
# ============================================
print_section "visualizing the networks to compare"

echo -e "$GRAPH1"
echo -e "$GRAPH2"
echo -e "$COLOR_DICT"
echo -e "$AFFILIATION_KEY"

print_separator
print_command  ./vc2sng.py  -l --color-dict $COLOR_DICT $GRAPH1 $GRAPH2

 ./vc2sng.py  -l --color-dict $COLOR_DICT $GRAPH1 $GRAPH2

if [ $? -eq 0 ]; then
    print_success "Networks compared"
else
    print_warning "Networks compared with warnings"
fi

print_separator