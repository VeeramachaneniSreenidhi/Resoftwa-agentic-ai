namespace po;

entity PurchaseOrders {
  key ID         : UUID;
      vendorName : String(111);
      quantity   : Integer;
      dueDate    : Date;
}
