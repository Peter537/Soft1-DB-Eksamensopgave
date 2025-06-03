## Categories of users

1. Logged-in users

    1.1 Company users

    1.2 Normal users

2. Non-logged-in users

## Use-case diagram

## Functional Requirements

1. As a User, I want to be able to buy a product, regardless of whether I am logged in or not.
2. As a User, I want to be able to do my shopping without having to log in or create an account.
3. As a User, I want to be able to create my own listing.
4. As a User, I want to be able to search for products using keywords and apply filters (e.g., category, price range).
5. As a logged-in User, I want to be able to view my past order history.
6. As a logged-in User, I want to be able to make reviews on products I have purchased.
7. As a User, I want to be able to view detailed information about a product, including description, price, and images.
8. As a User, I want to be able to add products to a shopping cart and modify the cart contents (e.g., change quantity, remove items).

## Non-Functional Requirements

1. The design of the system doesn't have to be finalized, since this is a proof of concept.
2. When a User searchs for products, the system should be able to return the results in less than 2 seconds.
3. The product catalog data structure in MongoDB should be flexible enough to accommodate diverse product attributes without requiring schema changes.
4. The system should have session management to handle the user's cart, login-state, frequently searched terms and more that does not require persistence.
5. The system should be intuitive and easy to navigate for all user types.
6. The system should provide clear feedback to users for actions performed (e.g., item added to cart, successful login).

Use-case (AC) format
---

# Acceptance Criteria Table

| ID  | Requirement Type | Requirement Description                                                                 | Acceptance Criteria (Use-Case Style)                                                                 |
|-----|------------------|------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| F1  | Functional        | Users can buy a product without logging in                                              | Given a user (logged in or not), when they add a product to cart and proceed to checkout, then they can purchase it |
| F2  | Functional        | Users can shop without creating an account                                              | Given a user, when they browse or add products to cart, then no login or account creation is required  |
| F3  | Functional        | Users can create their own listings                                                     | Given a logged-in user, when they fill out a product form, then the listing is created and published   |
| F4  | Functional        | Users can search and filter products                                                    | Given a user, when they use the search bar and filters, then relevant products are returned            |
| F5  | Functional        | Logged-in users can view order history                                                  | Given a logged-in user, when they access the profile/orders section, then past orders are displayed    |
| F6  | Functional        | Logged-in users can review purchased products                                           | Given a logged-in user, when they view a previously purchased product, then they can leave a review    |
| F7  | Functional        | Users can view product details                                                          | Given a user, when they click on a product, then the details page is shown with description, price, images |
| F8  | Functional        | Users can add/modify cart items                                                         | Given a user, when they view their cart, then they can add, update quantity, or remove products        |
| NF1 | Non-Functional    | System design not finalized                                                             | Given this is a POC, then design flexibility is permitted                                               |
| NF2 | Non-Functional    | Search results should return in <2 seconds                                              | Given a user performs a search, then the results load within 2 seconds                                 |
| NF3 | Non-Functional    | MongoDB product schema must be flexible                                                 | Given new or varying product attributes, then MongoDB accepts the data without schema issues           |
| NF4 | Non-Functional    | Session management for carts, search history, etc.                                     | Given a session exists, then temporary user data is available (cart, login state, searches) without saving to DB |
| NF5 | Non-Functional    | System should be easy to use                                                            | Given any user interacts with the system, then the UI/UX is intuitive and accessible                   |
| NF6 | Non-Functional    | System provides feedback for user actions                                               | Given a user performs an action (e.g., add to cart), then feedback is shown (e.g., confirmation message)|


# Glossary

| Term                      | Explanation                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| Listing                   | A product entry created by a user, containing details like name, price, etc.|
| Shopping cart             | A virtual basket where users add products they intend to purchase           |
| Checkout                  | The process of finalizing a purchase, including entering payment and delivery info |
| Review                    | Feedback or rating submitted by a user about a purchased product            |
| Filters                   | Search modifiers like category, price range, or brand used to narrow results|
| POC (Proof of Concept)    | A basic implementation to demonstrate feasibility, not necessarily production-ready |
| Schema                    | The structure or format that defines how data is organized in a database    |
| Session                   | Temporary storage of user data while they are browsing or interacting with the system (e.g., cart contents) |
| Feedback (System)         | Visual confirmation or alert shown to users after they take an action (e.g., “Item added to cart”) |
| Order History             | A list of past purchases made by a logged-in user                            |
