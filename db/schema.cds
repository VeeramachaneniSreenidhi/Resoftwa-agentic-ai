// Data model for purchase orders (sample data only)
namespace resoftwa.po;

// A vendor (supplier)
entity Vendors {
  key ID : String(10);
  name   : String(80);
  rating : String(10); // good | new | poor
}

// A purchase order, linked to one vendor
entity PurchaseOrders {
  key poNumber : String(10);
  vendor       : Association to Vendors;
  dueDate      : Date;
  orderedQty   : Integer;
  deliveredQty : Integer;
  amount       : Decimal(15,2);
  virtual isLate : Boolean; // not stored in the database, computed in srv/po-service.js
}
