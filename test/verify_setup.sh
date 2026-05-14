#!/bin/bash

# Verification script for project setup

MISSING=0

check_dir() {
    if [ -d "$1" ]; then
        echo "✅ Directory $1 exists."
    else
        echo "❌ Directory $1 is missing."
        MISSING=$((MISSING+1))
    fi
}

check_file() {
    if [ -f "$1" ]; then
        echo "✅ File $1 exists."
    else
        echo "❌ File $1 is missing."
        MISSING=$((MISSING+1))
    fi
}

echo "Starting project setup verification..."

check_dir "src"
check_dir "test"
check_dir "specification"
check_dir "build"

check_file "README.md"
check_file "ROADMAP.md"
check_file "TECHNICAL_DEBTS.md"
check_file "CONCEPT.md"
check_file "DESIGN.md"

if [ $MISSING -eq 0 ]; then
    echo "Verification successful: All required directories and files are present."
    exit 0
else
    echo "Verification failed: $MISSING items are missing."
    exit 1
fi
