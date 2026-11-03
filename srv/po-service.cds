// The OData service for purchase orders
using resoftwa.po from '../db/schema';

// Service at /odata/v4/po
service POService @(path: '/odata/v4/po') {
  // Expose both entities as they are
  entity Vendors as projection on po.Vendors;
  entity PurchaseOrders as projection on po.PurchaseOrders;
}
