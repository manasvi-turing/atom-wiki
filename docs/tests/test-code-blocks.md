---
title: Code Block Test
tags: [testing, code, syntax-highlighting]
---

# Code Block Syntax Highlighting Test

This file tests how code blocks look with and without Prism.js (CDN).

## Python

```python
def fibonacci(n):
    """Generate Fibonacci sequence up to n terms."""
    a, b = 0, 1
    result = []
    for i in range(n):
        result.append(a)
        a, b = b, a + b
    return result

# Example usage
numbers = fibonacci(10)
print(f"First 10 Fibonacci numbers: {numbers}")
```

## JavaScript

```javascript
// Async/await example with error handling
async function fetchUserData(userId) {
    try {
        const response = await fetch(`https://api.example.com/users/${userId}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Failed to fetch user data:', error);
        return null;
    }
}

// Arrow function with destructuring
const processUser = ({ name, email, age }) => ({
    displayName: name.toUpperCase(),
    contact: email,
    isAdult: age >= 18
});
```

## Bash

```bash
#!/bin/bash

# Deploy script with error handling
set -e

PROJECT_DIR="/var/www/myapp"
BACKUP_DIR="/var/backups/myapp-$(date +%Y%m%d-%H%M%S)"

echo "🚀 Starting deployment..."

# Backup current version
mkdir -p "$BACKUP_DIR"
cp -r "$PROJECT_DIR" "$BACKUP_DIR"

# Pull latest changes
cd "$PROJECT_DIR"
git pull origin main

# Install dependencies
npm install --production

# Run database migrations
npm run migrate

# Restart services
sudo systemctl restart myapp

echo "✅ Deployment completed successfully!"
```

## SQL

```sql
-- Complex query with joins and aggregation
SELECT 
    u.user_id,
    u.username,
    u.email,
    COUNT(DISTINCT o.order_id) as total_orders,
    SUM(oi.quantity * oi.price) as total_spent,
    AVG(o.order_total) as avg_order_value,
    MAX(o.created_at) as last_order_date
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
WHERE u.status = 'active'
    AND o.created_at >= DATE_SUB(NOW(), INTERVAL 1 YEAR)
GROUP BY u.user_id, u.username, u.email
HAVING total_orders > 5
ORDER BY total_spent DESC
LIMIT 100;
```

## HTML

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modern Web Page</title>
    <style>
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Welcome to My Site</h1>
            <nav>
                <a href="#home">Home</a>
                <a href="#about">About</a>
                <a href="#contact">Contact</a>
            </nav>
        </header>
        <main>
            <article class="post">
                <h2>Latest Post</h2>
                <p>Content goes here...</p>
            </article>
        </main>
    </div>
</body>
</html>
```

## CSS

```css
/* Modern CSS with variables and grid */
:root {
    --primary-color: #3498db;
    --secondary-color: #2ecc71;
    --text-color: #333;
    --spacing: 1rem;
}

.grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: var(--spacing);
    padding: calc(var(--spacing) * 2);
}

.card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}
```

## JSON

```json
{
  "name": "atom-wiki",
  "version": "0.2.0",
  "description": "Turn your markdown folder into one HTML file",
  "main": "index.js",
  "scripts": {
    "build": "atom-wiki ./docs -o wiki.html",
    "test": "pytest tests/",
    "lint": "eslint src/"
  },
  "dependencies": {
    "markdown": "^3.9.0",
    "pyyaml": "^6.0.3"
  },
  "keywords": ["markdown", "wiki", "documentation", "static-site"],
  "author": "Manasvi Sharma",
  "license": "MIT"
}
```

## YAML

```yaml
# Kubernetes deployment configuration
apiVersion: apps/v1
kind: Deployment
metadata:
  name: atom-wiki-app
  labels:
    app: atom-wiki
    version: v1.0
spec:
  replicas: 3
  selector:
    matchLabels:
      app: atom-wiki
  template:
    metadata:
      labels:
        app: atom-wiki
    spec:
      containers:
      - name: wiki
        image: atom-wiki:latest
        ports:
        - containerPort: 8080
        env:
        - name: NODE_ENV
          value: "production"
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
```

## Ruby

```ruby
# Rails model with validations and callbacks
class User < ApplicationRecord
  has_many :posts, dependent: :destroy
  has_many :comments
  
  validates :email, presence: true, uniqueness: true,
            format: { with: URI::MailTo::EMAIL_REGEXP }
  validates :username, presence: true, length: { minimum: 3, maximum: 20 }
  validates :age, numericality: { greater_than_or_equal_to: 13 }
  
  before_save :normalize_email
  after_create :send_welcome_email
  
  scope :active, -> { where(status: 'active') }
  scope :premium, -> { where(subscription: 'premium') }
  
  def full_name
    "#{first_name} #{last_name}".strip
  end
  
  private
  
  def normalize_email
    self.email = email.downcase.strip
  end
  
  def send_welcome_email
    UserMailer.welcome_email(self).deliver_later
  end
end
```

## Go

```go
package main

import (
    "fmt"
    "net/http"
    "encoding/json"
    "log"
)

type User struct {
    ID       int    `json:"id"`
    Username string `json:"username"`
    Email    string `json:"email"`
}

func getUserHandler(w http.ResponseWriter, r *http.Request) {
    // Mock data
    user := User{
        ID:       1,
        Username: "johndoe",
        Email:    "john@example.com",
    }
    
    w.Header().Set("Content-Type", "application/json")
    
    if err := json.NewEncoder(w).Encode(user); err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
}

func main() {
    http.HandleFunc("/api/user", getUserHandler)
    
    fmt.Println("Server starting on :8080")
    if err := http.ListenAndServe(":8080", nil); err != nil {
        log.Fatal(err)
    }
}
```

## Inline Code

Here's some inline code: `const result = array.map(x => x * 2)` and more `pip install atom-wiki`.

You can also use inline code with backticks like `npm install` or `git commit -m "message"`.

## Mixed Content

When you run `atom-wiki ./docs -o wiki.html`, it processes all markdown files:

```bash
# Example command
atom-wiki ./my-docs -o output.html --enable-chat
```

Then you can open it in a browser:

```javascript
// Or embed it in a web app
window.open('output.html', '_blank');
```

## What to Look For

**With CDN (Prism.js loaded):**

- ✅ Colorful syntax highlighting
- ✅ Different colors for keywords, strings, comments
- ✅ Line numbers (if enabled)
- ✅ Language-specific styling

**Without CDN (Offline):**

- ⚠️ Plain monospace text
- ⚠️ No color highlighting
- ⚠️ Still readable and properly formatted
- ⚠️ Indentation preserved
