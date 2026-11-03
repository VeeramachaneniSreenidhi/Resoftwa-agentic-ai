// Business logic for POService
export default (srv) => {

  // Rule 1: before a new PO is saved, reject amount <= 0
  srv.before('CREATE', 'PurchaseOrders', (req) => {
    if (req.data.amount <= 0) {
      return req.reject(400, 'Amount must be greater than 0');
    }
  });

  // Rule 2: after reading POs, set isLate
  // isLate = true when the due date is in the past AND not everything is delivered
  srv.after('READ', 'PurchaseOrders', (data) => {
    if (!data) return;

    // Read can return one row or a list of rows
    const rows = Array.isArray(data) ? data : [data];

    // Today as text in the same format as dueDate (YYYY-MM-DD)
    const today = new Date().toISOString().slice(0, 10);

    for (const row of rows) {
      row.isLate = Boolean(row.dueDate)
        && row.dueDate < today
        && row.deliveredQty < row.orderedQty;
    }
  });
};
