'use strict';

/**
 * Pure validation rules for PurchaseOrders payloads. No CAP dependency,
 * so these can be unit-tested without starting a server.
 *
 * @param {object} data     The payload (req.data in CAP).
 * @param {object} [opts]
 * @param {boolean} [opts.partial=false]  When true (UPDATE), a field that is
 *        absent from the payload is treated as unchanged and not validated.
 *        A field that is present but null/invalid is still rejected.
 * @returns {{ field: string, message: string }[]} Empty array when valid.
 */
function validatePurchaseOrder(data, { partial = false } = {}) {
  const errors = [];
  const d = data || {};

  // vendorName: must be a non-empty string after trimming.
  if (d.vendorName !== undefined || !partial) {
    if (typeof d.vendorName !== 'string' || d.vendorName.trim() === '') {
      errors.push({ field: 'vendorName', message: 'vendorName must not be empty' });
    }
  }

  // quantity: must be a number strictly greater than 0.
  if (d.quantity !== undefined || !partial) {
    if (typeof d.quantity !== 'number' || !Number.isFinite(d.quantity) || d.quantity <= 0) {
      errors.push({ field: 'quantity', message: 'quantity must be greater than 0' });
    }
  }

  return errors;
}

module.exports = { validatePurchaseOrder };
