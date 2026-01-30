#!/usr/bin/env python3
"""
Markdown Editor - Tools for Markdown files

This script provides tools for working with Markdown files:
- Heading Upgrade: Convert h2→h1, h3→h2, etc. (h1 remains h1)
- Heading Downgrade: Convert h1→h2, h2→h3, etc. (h6 remains h6)
- Heading Number Removal: Remove various numbering from headings
  (Chinese, numeric, multi-level, Roman numerals, letters, etc.)
- Heading Numbering Addition: Add structured numbering to headings
  (supports multiple numbering styles)

Usage:
    python markdown_editor.py input.md <action> [-o output.md] [--style STYLE]

Actions:
    upgrade        - Upgrade headings by one level (h2→h1, h3→h2, etc.)
    downgrade      - Downgrade headings by one level (h1→h2, h2→h3, etc.)
    remove_numbers - Remove all numbering from headings (1. 一、 I. (A) 等)
    add_numbers    - Add numbering to headings based on style (tech, academic, chinese_bidding, chinese_book)

Options:
    --style STYLE  - Numbering style for add_numbers action
                     Available styles:
                     - tech: Technical documentation (1. 1.1. 1.1.1.)
                     - academic: Academic paper (I. II. 1.1. 1.1.1.)
                     - chinese_bidding: Chinese bidding document (一、 二、 1.1. 1.1.1.)
                     - chinese_book: Chinese book (第一篇、 第二篇、 1.1. 1.1.1.)
    --template PATH - Path to custom template JSON file for add_numbers action
    --simple       - Use simple mode for remove_numbers (only remove numbering followed by spaces, safer for complex headings)

Examples:
    # Upgrade headings (h2→h1, h3→h2, etc.)
    python markdown_editor.py document.md upgrade
    
    # Downgrade headings (h1→h2, h2→h3, etc.)
    python markdown_editor.py document.md downgrade
    
    # Remove heading numbering
    python markdown_editor.py document.md remove_numbers
    
    # Add technical documentation style numbering (1. 1.1. 1.1.1.)
    python markdown_editor.py document.md add_numbers --style tech
    
    # Add Chinese bidding document style numbering (一、 二、 1.1. 1.1.1.)
    python markdown_editor.py document.md add_numbers --style chinese_bidding
    
    # Add academic paper style numbering (I. II. 1.1. 1.1.1.)
    python markdown_editor.py document.md add_numbers --style academic
    
    # Add Chinese book style numbering (第一篇、 第二篇、 1.1. 1.1.1.)
    python markdown_editor.py document.md add_numbers --style chinese_book
    
    # Write to different output file
    python markdown_editor.py document.md add_numbers --style tech -o document_numbered.md
"""

import argparse
import sys
import re
import json



def print_banner():
    """Print a banner showing markdown-tools"""
    print("=" * 60)
    print("                    markdown-tools")
    print("=" * 60)
    print()


def downgrade_headings(content):
    """
    Downgrade all Markdown headings by one level:
    - h1 (#) → h2 (##)
    - h2 (##) → h3 (###)
    - ...
    - h6 (######) → remains h6 (######)
    
    Args:
        content: Markdown content as string
        
    Returns:
        Modified content with headings downgraded
    """
    # Use regex to find all headings and add one more #
    # Pattern: ^(#+)(\s*)(.+)$ (matches headings at start of line)
    def replace_heading(match):
        hashes = match.group(1)
        spaces = match.group(2)
        content = match.group(3)
        
        # Only downgrade if less than 6 hashes (h6 can't be downgraded further)
        if len(hashes) < 6:
            hashes = '#' + hashes
        
        return f"{hashes}{spaces}{content}"
    
    return re.sub(r'^(#{1,6})(\s*)(.+)$', replace_heading, content, flags=re.MULTILINE)


def upgrade_headings(content):
    """
    Upgrade all Markdown headings by one level:
    - h1 (#) → remains h1 (#)
    - h2 (##) → h1 (#)
    - h3 (###) → h2 (##)
    - ...
    - h6 (######) → h5 (#####)
    
    Args:
        content: Markdown content as string
        
    Returns:
        Modified content with headings upgraded
    """
    # Use regex to find all headings and remove one # if possible
    # Pattern: ^(#+)(\s*)(.+)$ (matches headings at start of line)
    def replace_heading(match):
        hashes = match.group(1)
        spaces = match.group(2)
        content = match.group(3)
        
        # Only upgrade if more than 1 hash (h1 can't be upgraded further)
        if len(hashes) > 1:
            hashes = hashes[1:]  # Remove one hash
        
        return f"{hashes}{spaces}{content}"
    
    return re.sub(r'^(#{1,6})(\s*)(.+)$', replace_heading, content, flags=re.MULTILINE)


def remove_heading_numbers(content):
    """
    Remove all numbering from Markdown headings:
    - Chinese numbering: 一、 二、 三、 → 移除
    - Numeric numbering: 1. 2. 3. → 移除
    - Multi-level numbering: 1.1. 2.3.4. → 移除
    - Roman numerals: I. II. III. IV. → 移除
    - Letter numbering: A. B. C. → 移除
    - Parentheses format: (1) (一) (A) → 移除
    - Full-width numbering: １、 ２、 ３、 → 移除
    - Chinese chapter format: 第一章、 第二章、 → 移除
    
    Args:
        content: Markdown content as string
        
    Returns:
        Modified content with heading numbers removed
    """
    # Use regex to find all headings and remove numbering patterns
    # Pattern: ^(#+)(\s*)(.+)$ (matches headings at start of line)
    def replace_heading(match):
        hashes = match.group(1)
        spaces = match.group(2)
        heading_text = match.group(3)
        
        # Remove various numbering patterns from heading text
        # Chinese numbering: 一、 二、 三、 等
        heading_text = re.sub(r'^([一二三四五六七八九十百千万]+、)+', '', heading_text)
        
        # Chinese uppercase: 壹、 贰、 叁、 等
        heading_text = re.sub(r'^([壹贰叁肆伍陆柒捌玖拾佰仟万]+、)+', '', heading_text)
        
        # Roman numerals with dot: I. II. III. IV. 等
        heading_text = re.sub(r'^([IVXLCDM]+)\.\s*', '', heading_text, flags=re.IGNORECASE)
        
        # Numeric numbering (including multi-level): 1. 1.1. 1.1.1. 等
        heading_text = re.sub(r'^(\d+\.)*\d+\.?\s*', '', heading_text)
        
        # Numeric + letter numbering (academic style): 1.1.1.A 1.1.1.A.A 等
        heading_text = re.sub(r'^(\d+\.)*(\d+\.[A-Za-z])+\s*', '', heading_text)
        
        # Numeric with parentheses: (1) (2) (3) 等
        heading_text = re.sub(r'^\(\d+\)\s*', '', heading_text)
        
        # Chinese with parentheses: (一) (二) (三) 等
        heading_text = re.sub(r'^\([一二三四五六七八九十百千万]+\)\s*', '', heading_text)
        
        # Full-width numbering: １、 ２、 ３、 等
        heading_text = re.sub(r'^(\d+、)+', '', heading_text)
        
        # Roman with parentheses: (I) (II) (III) 等
        heading_text = re.sub(r'^\([IVXLCDM]+\)\s*', '', heading_text, flags=re.IGNORECASE)
        
        # Letter numbering: A. B. C. 或 a. b. c. 等
        heading_text = re.sub(r'^([A-Za-z])\.\s*', '', heading_text)
        
        # Multi-level letter numbering: .A .A.A .A.A.A 等
        heading_text = re.sub(r'^(\.[A-Za-z])+\s*', '', heading_text)
        
        # Letter with parentheses: (A) (B) (C) 或 (a) (b) (c) 等
        heading_text = re.sub(r'^\([A-Za-z]\)\s*', '', heading_text)
        
        # Mixed formats: 1） 2） 一） 二） 等
        heading_text = re.sub(r'^(\d+|[一二三四五六七八九十百千万]+)[）]\s*', '', heading_text)
        
        # Chinese book format: 第一篇、 第二篇、 等
        heading_text = re.sub(r'^第[一二三四五六七八九十百千万]+篇', '', heading_text)
        
        # Chinese chapter format: 第一章、 第二章、 等
        heading_text = re.sub(r'^第[一二三四五六七八九十百千万]+章', '', heading_text)
        
        # Remove any remaining leading whitespace after numbering removal
        heading_text = heading_text.strip()
        
        return f"{hashes}{spaces}{heading_text}"
    
    return re.sub(r'^(#{1,6})(\s*)(.+)$', replace_heading, content, flags=re.MULTILINE)


# Helper functions for number format conversion

def number_to_chinese(num):
    """
    Convert Arabic number to Chinese number characters (一、二、三...)
    
    Args:
        num: Integer number to convert (1-9999 recommended)
        
    Returns:
        Chinese number as string
    """
    chinese_nums = ['', '一', '二', '三', '四', '五', '六', '七', '八', '九']
    chinese_units = ['', '十', '百', '千', '万']
    
    if num == 0:
        return '零'
    if num < 0:
        return '负' + number_to_chinese(-num)
    
    result = ''
    num_str = str(num)
    length = len(num_str)
    has_trailing_zero = False
    
    for i, digit in enumerate(num_str):
        digit_int = int(digit)
        place = length - i - 1
        
        if digit_int == 0:
            # Mark that we have a zero, but don't add it yet
            has_trailing_zero = True
        else:
            # If we had a zero before, add it now
            if has_trailing_zero:
                result += '零'
                has_trailing_zero = False
            # Add the digit and unit
            result += chinese_nums[digit_int] + chinese_units[place]
    
    # Special case for 10-19
    if num >= 10 and num <= 19:
        result = result[1:]  # Remove leading '一'
    
    return result


def number_to_chinese_upper(num):
    """
    Convert Arabic number to Chinese upper case characters (壹、贰、叁...)
    
    Args:
        num: Integer number to convert (1-9999 recommended)
        
    Returns:
        Chinese upper case number as string
    """
    chinese_upper_nums = ['', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']
    chinese_units = ['', '拾', '佰', '仟', '万']
    
    if num == 0:
        return '零'
    if num < 0:
        return '负' + number_to_chinese_upper(-num)
    
    result = ''
    num_str = str(num)
    length = len(num_str)
    
    for i, digit in enumerate(num_str):
        digit_int = int(digit)
        place = length - i - 1
        
        if digit_int == 0:
            if result and not result.endswith('零'):
                result += '零'
        else:
            if result.endswith('零') and place > 0:
                result = result[:-1]
            result += chinese_upper_nums[digit_int] + chinese_units[place]
    
    # Special case for 10-19 (keep '壹' in upper case)
    if num >= 10 and num <= 19:
        result = '拾' + result[2:] if len(result) > 2 else '拾'
    
    return result


def number_to_roman(num):
    """
    Convert Arabic number to Roman numerals (I、II、III...)
    
    Args:
        num: Integer number to convert (1-3999 recommended)
        
    Returns:
        Roman numeral as string
    """
    roman_numerals = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ]
    
    if num <= 0 or num >= 4000:
        return str(num)
    
    result = ''
    for value, symbol in roman_numerals:
        while num >= value:
            result += symbol
            num -= value
    
    return result


def number_to_alpha(num, uppercase=True):
    """
    Convert Arabic number to alphabetic characters (A、B、C... or a、b、c...)
    
    Args:
        num: Integer number to convert (1-26 recommended)
        uppercase: Whether to use uppercase letters
        
    Returns:
        Alphabetic character as string
    """
    if num <= 0 or num > 26:
        return str(num)
    
    base = 65 if uppercase else 97
    return chr(base + num - 1)


# Preset numbering styles
PRESET_STYLES = {
    'tech': {
        'name': 'Technical Documentation',
        'description': 'Technical documentation style (1. 1.1. 1.1.1.)',
        'templates': {
            1: '{level1} ',
            2: '{level1}.{level2} ',
            3: '{level1}.{level2}.{level3} ',
            4: '{level1}.{level2}.{level3}.{level4} ',
            5: '{level1}.{level2}.{level3}.{level4}.{level5} ',
            6: '{level1}.{level2}.{level3}.{level4}.{level5}.{level6} '
        }
    },
    'academic': {
        'name': 'Academic Paper',
        'description': 'Academic paper style (I. II. 1.1. 1.1.1.)',
        'templates': {
            1: '{level1:roman}. ',
            2: '{level1}.{level2} ',
            3: '{level1}.{level2}.{level3} ',
            4: '{level1}.{level2}.{level3}.{level4:alpha} ',
            5: '{level1}.{level2}.{level3}.{level4:alpha}.{level5:alpha} ',
            6: '{level1}.{level2}.{level3}.{level4:alpha}.{level5:alpha}.{level6:alpha} '
        }
    },
    'chinese_bidding': {
        'name': 'Chinese Bidding Document',
        'description': 'Chinese bidding document style (一、 二、 1.1. 1.1.1.)',
        'templates': {
            1: '{level1:chinese}、',
            2: '{level1}.{level2} ',
            3: '{level1}.{level2}.{level3} ',
            4: '{level1}.{level2}.{level3}.{level4} ',
            5: '{level1}.{level2}.{level3}.{level4}.{level5} ',
            6: '{level1}.{level2}.{level3}.{level4}.{level5}.{level6} '
        }
    },
    'chinese_book': {
        'name': 'Chinese Book',
        'description': 'Chinese book style (第一篇  第二篇  1.1. 1.1.1.)',
        'templates': {
            1: '第{level1:chinese}篇 ',
            2: '{level1}.{level2} ',
            3: '{level1}.{level2}.{level3} ',
            4: '{level1}.{level2}.{level3}.{level4} ',
            5: '{level1}.{level2}.{level3}.{level4}.{level5} ',
            6: '{level1}.{level2}.{level3}.{level4}.{level5}.{level6} '}
    }
}


def render_template(template, level_counters):
    """
    Render a template string by replacing placeholders with actual numbers
    
    Args:
        template: Template string with placeholders like {level1:number}, {level2:chinese}
        level_counters: Dictionary with current level counts {1: 1, 2: 3, 3: 2}
        
    Returns:
        Rendered string with placeholders replaced by actual numbers
    """
    # Map format types to conversion functions
    format_handlers = {
        'number': str,
        'chinese': number_to_chinese,
        'chinese_upper': number_to_chinese_upper,
        'roman': number_to_roman,
        'alpha': lambda num: number_to_alpha(num, uppercase=True),
        'alpha_lower': lambda num: number_to_alpha(num, uppercase=False)
    }
    
    # Regular expressions for different placeholder formats
    placeholder_with_format = r'\{level(\d+):([a-z_]+)\}'
    placeholder_simple = r'\{level(\d+)\}'
    
    # Handler for {levelN:format_type} format
    def replace_with_format(match):
        level_str = match.group(1)
        format_type = match.group(2)
        
        level = int(level_str)
        if level not in level_counters:
            return match.group(0)
        
        number = level_counters[level]
        if format_type in format_handlers:
            return format_handlers[format_type](number)
        else:
            return str(number)
    
    # Handler for {levelN} format (default to number)
    def replace_simple(match):
        level_str = match.group(1)
        
        level = int(level_str)
        if level not in level_counters:
            return match.group(0)
        
        number = level_counters[level]
        return str(number)
    
    # Replace all placeholders in the template
    # First replace {levelN:format_type} format
    template = re.sub(placeholder_with_format, replace_with_format, template)
    # Then replace {levelN} format
    return re.sub(placeholder_simple, replace_simple, template)


def add_numbers(content, style='tech', custom_templates=None):
    """
    Add numbering to all Markdown headings based on the specified style
    
    Args:
        content: Markdown content as string
        style: Numbering style to use (tech, academic, chinese_bidding, chinese_book)
        custom_templates: Dictionary with custom templates {1: '{level1:...}', 2: '{level2:...}'}
        
    Returns:
        Modified content with numbered headings
    """
    # First remove any existing numbering to ensure clean start
    content = remove_heading_numbers(content)
    
    # Get templates based on style or custom templates
    if custom_templates:
        templates = custom_templates
    elif style in PRESET_STYLES:
        templates = PRESET_STYLES[style]['templates']
    else:
        # Default to tech style if unknown
        templates = PRESET_STYLES['tech']['templates']
    
    # Level counters to track current numbering for each heading level
    level_counters = {}
    
    # Use regex to find all headings and add numbering
    # Pattern: ^(#+)(\s*)(.+)$ (matches headings at start of line)
    def replace_heading(match):
        hashes = match.group(1)
        spaces = match.group(2)
        heading_text = match.group(3)
        
        # Get heading level (number of #)
        current_level = len(hashes)
        
        # Update counters based on current level
        if current_level not in level_counters:
            # First time seeing this level, initialize it
            level_counters[current_level] = 1
        else:
            # Already seen this level, increment it
            level_counters[current_level] += 1
        
        # Initialize all parent levels if not present
        # For example, if current_level is 3 and level 2 doesn't exist, set it to 1
        for level in range(1, current_level):
            if level not in level_counters:
                level_counters[level] = 1
        
        # Reset all child levels (higher than current level)
        for level in list(level_counters.keys()):
            if level > current_level:
                del level_counters[level]
        
        # Get template for current level, fallback to default if not found
        template = templates.get(current_level, f"{{level{current_level}:number}} ")
        
        # Render the template with current level counters
        numbering = render_template(template, level_counters)
        
        # Return modified heading with numbering
        return f"{hashes}{spaces}{numbering}{heading_text}"
    
    return re.sub(r'^(#{1,6})(\s*)(.+)$', replace_heading, content, flags=re.MULTILINE)


def main():
    print_banner()
    
    parser = argparse.ArgumentParser(description='Markdown Editor - Tools for Markdown files')
    parser.add_argument('input_file', help='Path to the input Markdown file')
    parser.add_argument('action', choices=['upgrade', 'downgrade', 'remove_numbers', 'add_numbers'], help='Action to perform: upgrade (h2→h1, etc.), downgrade (h1→h2, etc.), remove_numbers (remove heading numbering), or add_numbers (add heading numbering)')
    parser.add_argument('-o', '--output_file', help='Path to the output file (optional, defaults to input_file)')
    parser.add_argument('--style', choices=['tech', 'academic', 'chinese_bidding', 'chinese_book'], default='tech', help='Numbering style for add_numbers action (tech, academic, chinese_bidding, chinese_book)')
    parser.add_argument('--template', help='Path to custom template JSON file for add_numbers action')
    
    args = parser.parse_args()
    
    try:
        # Read input file
        with open(args.input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply heading action based on user choice
        if args.action == 'upgrade':
            fixed_content = upgrade_headings(content)
            action_name = 'upgrade'
        elif args.action == 'downgrade':
            fixed_content = downgrade_headings(content)
            action_name = 'downgrade'
        elif args.action == 'remove_numbers':
            fixed_content = remove_heading_numbers(content)
            action_name = 'number removal'
        else:  # add_numbers
            # Handle custom template if provided
            custom_templates = None
            if args.template:
                try:
                    with open(args.template, 'r', encoding='utf-8') as f:
                        # Load JSON and convert string keys to integers
                        custom_templates_dict = json.load(f)
                        custom_templates = {}
                        for key, value in custom_templates_dict.items():
                            try:
                                level = int(key)
                                custom_templates[level] = value
                            except ValueError:
                                print(f"Warning: Invalid level '{key}' in template (must be integer)")
                    action_name = 'custom numbering addition'
                except json.JSONDecodeError:
                    print(f"Error: Invalid JSON format in template file '{args.template}'")
                    sys.exit(1)
                except FileNotFoundError:
                    print(f"Error: Template file '{args.template}' not found")
                    sys.exit(1)
            else:
                action_name = 'numbering addition'
            
            fixed_content = add_numbers(content, style=args.style, custom_templates=custom_templates)
        
        # Determine output file
        output_file = args.output_file if args.output_file else args.input_file
        
        # Write output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"✓ Heading {action_name} completed!")
        print(f"✓ Output saved to: {output_file}")
        return 0
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())