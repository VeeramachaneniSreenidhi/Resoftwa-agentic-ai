using po from '../db/schema';

@path: '/odata/v4/po'
service POService {
  entity PurchaseOrders as projection on po.PurchaseOrders;
}
