'use strict';

const cds = require('@sap/cds');
const { validatePurchaseOrder } = require('./validate');

module.exports = class POService extends cds.ApplicationService {
  async init() {
    this.before(['CREATE', 'UPDATE'], 'PurchaseOrders', (req) => {
      const errors = validatePurchaseOrder(req.data, {
        partial: req.event === 'UPDATE',
      });
      // Report every problem in one response. req.error(400, ...) yields HTTP 400.
      for (const e of errors) {
        req.error(400, e.message, e.field);
      }
    });

    return super.init();
  }
};
