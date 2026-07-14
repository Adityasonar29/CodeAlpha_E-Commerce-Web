## Refined plan: admin dashboard and store management upgrade

The admin experience should feel like a polished control center rather than a bare Django page. I will keep the strong Django admin-style workflow, but improve the look and structure so it feels modern, clean, and professional.

### 1. Admin dashboard experience
- Use the Django admin-style dashboard as the base structure for store management.
- Make it look modern with better spacing, cards, stats, color accents, and clear sectioning.
- Show summary cards for:
  - total users
  - total orders
  - total products
  - featured products
  - normal products
- Add inventory warnings for:
  - low stock in yellow
  - out of stock in red
- Show the latest 5 orders in a polished table or card layout.

### 2. Product data model improvements
- Add these fields to the product model:
  - Brand: text field for manufacturer name
  - Category: text field for product grouping
- Keep the description field rich enough for longer content.
- Support Markdown-style formatting in product descriptions.
- Display:
  - a short preview on the home page and product list page
  - the full formatted description on the product detail page

### 3. Admin user management
- Add a custom admin-only user management section.
- Support:
  - view all users
  - add a new user
  - update a user name and email only
  - remove a user
  - view each user’s order history

### 4. Product analytics
- Add product-level insights such as:
  - how many times each product was ordered
  - total quantity sold
  - latest order activity for that product

### 5. Currency and UI polish
- Change the displayed currency to Rs.
- Use a configurable base-rate conversion approach if possible.
- Improve the overall UI/UX of the dashboard, product pages, and admin views so they feel more attractive and less lifeless.

### 6. Future auth improvement
- Password reset can be added later.
- Email-based reset is the best option to add next if you want it.

### Implementation focus
- Keep the admin flow familiar and practical.
- Make the pages more attractive with modern cards, badges, status chips, and a better visual hierarchy.
- Ensure the dashboard feels useful immediately to an admin.
