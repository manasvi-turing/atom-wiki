---
tags: [testing, lists]
---

# Testing Nested Lists

## Unordered Nested Lists

- First level item 1
  - Second level item 1
  - Second level item 2
    - Third level item 1
    - Third level item 2
  - Second level item 3
- First level item 2
  - Second level under item 2
- First level item 3

## Ordered Nested Lists

1. First item
   1. Nested item 1
   2. Nested item 2
      1. Deep nested item 1
      2. Deep nested item 2
   3. Nested item 3
2. Second item
   1. Nested under second
3. Third item

## Mixed Nested Lists

1. Ordered first level
    - Unordered second level
    - Another unordered
        1. Ordered third level
        2. Another ordered
    - Back to second level
2. Second ordered item
    - Mixed nested again

## Complex Example

- **Features**
  - Core Features
    - Markdown support
    - Syntax highlighting
    - Dark/light themes
  - Advanced Features
    - Tag system
    - Search functionality
- **Installation**
  - Prerequisites
    - Python 3.11+
    - uv package manager
  - Steps
    1. Clone repository
    2. Install dependencies
    3. Run build
- **Usage**
  - Basic commands
  - Configuration options

## Lists

### Unordered Lists

- First item
- Second item
- Third item
  - Nested item 3.1
  - Nested item 3.2
    - Double nested item 3.2.1
    - Double nested item 3.2.2
- Fourth item

Alternative bullet styles:

* Item with asterisk
* Another item
  * Nested with asterisk

+ Item with plus
+ Another item

### Ordered Lists

1. First ordered item
2. Second ordered item
3. Third ordered item
    1. Nested numbered item 3.1
    2. Nested numbered item 3.2
    3. Nested numbered item 3.3
4. Fourth ordered item

### Mixed Lists

1. First item
    - Unordered sub-item
    - Another sub-item
2. Second item
    1. Ordered sub-item
    2. Another ordered sub-item
3. Third item
