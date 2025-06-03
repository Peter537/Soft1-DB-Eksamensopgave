![alt text](./img/conceptual%20diagram.png.png)

```dbml
// Use DBML to define your database structure
// Docs: https://dbml.dbdiagram.io/docs

Table User {
  Id l
  Email l
  Name l
  IsCompany l
  CreatedAt l
}

Table Posting {
  Id l
  Title l
  Price l
  Status l
  Category l
  Location l
  Description l
  ItemCount l
  SpecificationList l
}

Table Review {
  Reviewer l
  ReviewedUser l
  ReviewedPosting l
  Rating l
  Description l
  CreatedAt l
}

Ref: User.Id < Review.Reviewer
Ref: User.Id < Review.ReviewedUser
Ref: Posting.Id < Review.ReviewedPosting

Table PaymentLog {
  PayerId l
  TotalAmount l
  CreatedAt l
  PurchaseList l
}

Ref: PaymentLog.PurchaseList <> Posting.Id
Ref: User.Id < PaymentLog.PayerId

Table ShoppingCart {
  SessionId l
  CreatedAt l
  CartItemList l
}

Ref "Would use something to store UserId to SessionId": User.Id < ShoppingCart.SessionId
Ref: Posting.Id <> ShoppingCart.CartItemList

Table TopViewedPostingsFeed {
  PostingsList l
}

Ref: Posting.Id <> TopViewedPostingsFeed.PostingsList
```
