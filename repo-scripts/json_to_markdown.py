#!/usr/bin/env python3
"""
Script to convert JSON entries to individual markdown files.
Each entry will become a markdown file with the agent name as title and system prompt as content.
"""

import json
import os
import re

def slugify(text):
    """
    Convert text to a URL and filesystem friendly format.
    This creates the "machine readable" version of the agent name.
    """
    # Convert to lowercase
    text = text.lower()
    # Replace spaces and special characters with hyphens
    text = re.sub(r'[^a-z0-9]+', '-', text)
    # Remove leading/trailing hyphens
    text = text.strip('-')
    return text

def create_markdown_files(json_file):
    """
    Read JSON file and create markdown files for each entry.
    """
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(json_file), 'markdown_prompts')
    os.makedirs(output_dir, exist_ok=True)
    
    # Read the JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    print(f"Found {len(data)} entries in the JSON file.")
    
    # Process each entry
    for entry in data:
        agent_name = entry.get('agent-name', '')
        system_prompt = entry.get('system-prompt', '')
        
        if not agent_name:
            print("Skipping entry with no agent name")
            continue
        
        # Create filename from agent name
        filename = slugify(agent_name) + '.md'
        filepath = os.path.join(output_dir, filename)
        
        # Create markdown content
        markdown_content = f"# {agent_name}\n\n## System Prompt\n\n{system_prompt}\n"
        
        # Write to file
        with open(filepath, 'w') as f:
            f.write(markdown_content)
        
        print(f"Created markdown file: {filename}")
    
    print(f"\nAll markdown files have been created in: {output_dir}")

if __name__ == "__main__":
    json_file = os.path.abspath("orchestration.json")
    create_markdown_files(json_file)
