'use strict';

const cds = require('@sap/cds');
const { POST, PATCH, GET, expect: cdsExpect } = cds.test(__dirname + '/..');

const ENTITY = '/odata/v4/po/PurchaseOrders';
const validBody = { vendorName: 'Acme GmbH', quantity: 10 };

describe('PurchaseOrders service (HTTP)', () => {
  test('POST a valid payload returns 201', async () => {
    const { status, data } = await POST(ENTITY, validBody);
    expect(status).toBe(201);
    expect(data.vendorName).toBe('Acme GmbH');
    expect(data.quantity).toBe(10);
  });

  test('POST with an empty vendor name returns 400', async () => {
    const { status, data } = await POST(ENTITY, { vendorName: '', quantity: 10 }).catch((e) => e.response);
    expect(status).toBe(400);
    expect(JSON.stringify(data)).toContain('vendorName');
  });

  test('POST with a whitespace-only vendor name returns 400', async () => {
    const res = await POST(ENTITY, { vendorName: '  ', quantity: 10 }).catch((e) => e.response);
    expect(res.status).toBe(400);
  });

  test.each([0, -5])('POST with quantity %p returns 400 and names the field', async (quantity) => {
    const res = await POST(ENTITY, { vendorName: 'Acme', quantity }).catch((e) => e.response);
    expect(res.status).toBe(400);
    expect(JSON.stringify(res.data)).toContain('quantity');
  });

  test('POST with both fields invalid reports both problems', async () => {
    const res = await POST(ENTITY, { vendorName: '', quantity: 0 }).catch((e) => e.response);
    expect(res.status).toBe(400);
    const body = JSON.stringify(res.data);
    expect(body).toContain('vendorName');
    expect(body).toContain('quantity');
  });

  test('PATCH with an invalid quantity returns 400 and does not change the record', async () => {
    const { data: created } = await POST(ENTITY, validBody);
    const res = await PATCH(`${ENTITY}(${created.ID})`, { quantity: 0 }).catch((e) => e.response);
    expect(res.status).toBe(400);

    const { data: after } = await GET(`${ENTITY}(${created.ID})`);
    expect(after.quantity).toBe(10);
  });

  test('PATCH with a valid quantity returns 200', async () => {
    const { data: created } = await POST(ENTITY, validBody);
    const { status, data } = await PATCH(`${ENTITY}(${created.ID})`, { quantity: 25 });
    expect(status).toBe(200);
    expect(data.quantity).toBe(25);
  });

  test('PATCH with an empty vendor name returns 400', async () => {
    const { data: created } = await POST(ENTITY, validBody);
    const res = await PATCH(`${ENTITY}(${created.ID})`, { vendorName: '' }).catch((e) => e.response);
    expect(res.status).toBe(400);
  });
});
