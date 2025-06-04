# Glossary

| Term                  | Explanation                                                                                                 |
| --------------------- | ----------------------------------------------------------------------------------------------------------- |
| Posting               | A product entry created by a user, containing details like name, price, etc.                                |
| Shopping cart or Cart | A virtual basket where users add products they intend to purchase                                           |
| Checkout              | The process of finalizing a purchase, including entering payment and delivery info                          |
| Review                | Feedback or rating submitted by a user about a purchased product                                            |
| Filters               | Search modifiers like category, price range, or brand used to narrow results                                |
| Schema                | The structure or format that defines how data is organized in a database                                    |
| Session               | Temporary storage of user data while they are browsing or interacting with the system (e.g., cart contents) |
| Feedback (System)     | Visual confirmation or alert shown to users after they take an action (e.g., "Item added to cart")          |
| Order History         | A list of past purchases made by a logged-in user                                                           |

# Categories of users

1. Logged-in users

   1.1 Company users

   1.2 Normal users

2. Non-logged-in users

3. User

   Could be either a logged-in user or a non-logged-in user. This term is used to refer to anyone interacting with the system, regardless of their login status.

# Functional Requirements

1. As a User, I want to be able to buy a product, regardless of whether I am logged in or not.
2. As a User, I want to be able to do my shopping without having to log in or create an account.
3. As a logged-in User, I want to be able to create my own posting.
4. As a User, I want to be able to search for products using keywords and apply filters.
5. As a logged-in User, I want to be able to view my past order history.
6. As a logged-in User, I want to be able to make reviews on products I have purchased.
7. As a User, I want to be able to view detailed information about a product, including description, price, etc.
8. As a User, I want to be able to add products to a shopping cart and modify the cart contents (e.g., remove items).

# Non-Functional Requirements

1. When a User searchs for products, the system should be able to return the results in less than 2 seconds.
2. The product catalog data structure in MongoDB should be flexible enough to accommodate diverse product attributes without requiring schema changes.
3. The system should have session management to handle the user's cart, login-state, frequently searched terms.
4. The system should provide clear feedback to users for actions performed (e.g., item added to cart).

# Use-case diagram

![alt text](./img/use-case%20diagram.png)

# Acceptance Criteria Table

| ID  | Requirement Type | Requirement Description                       | Acceptance Criteria                                                                                                                               |
| --- | ---------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| F1  | Functional       | Users can buy a product without logging in    | Given a User, when they add a product to cart and proceed to checkout, then they can purchase it                                                  |
| F2  | Functional       | Users can shop without creating an account    | Given a User, when they browse or add products to cart, then no login or account creation is required                                             |
| F3  | Functional       | Users can create their own postings           | Given a Logged-in User, when they fill out a product form, then the posting is created and published                                              |
| F4  | Functional       | Users can search and filter products          | Given a User, when they use the search bar and filters, then relevant products are returned                                                       |
| F5  | Functional       | Logged-in users can view order history        | Given a Logged-in User, when they access the profile/orders section, then past orders are displayed                                               |
| F6  | Functional       | Logged-in users can review purchased products | Given a Logged-in User, when they view a previously purchased product, then they can leave a review                                               |
| F7  | Functional       | Users can view product details                | Given a User, when they click on a product, then a detailed product page is shown                                                                 |
| F8  | Functional       | Users can add/modify cart items               | Given a User, when they view their cart, then they can add or remove products                                                                     |
| NF1 | Non-Functional   | Search results should return in <2 seconds    | Given a User, when they perform a search, then the results should load within 2 seconds                                                           |
| NF2 | Non-Functional   | MongoDB product schema must be flexible       | Given new or varying product attributes, when the product data is stored in MongoDB, then the system should accept the data without schema issues |
| NF3 | Non-Functional   | Session management                            | Given a user session is active, when the user leaves the website and returns, then their information should still be there                        |
| NF4 | Non-Functional   | System provides feedback for user actions     | Given a User, when they perform an action, then feedback is shown                                                                                 |
