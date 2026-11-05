'use strict';

const { validatePurchaseOrder } = require('../srv/validate');

const fields = (errors) => errors.map((e) => e.field);

describe('validatePurchaseOrder (unit)', () => {
  test('accepts a valid payload', () => {
    expect(validatePurchaseOrder({ vendorName: 'Acme GmbH', quantity: 10 })).toEqual([]);
  });

  test('rejects an empty vendor name', () => {
    const errors = validatePurchaseOrder({ vendorName: '', quantity: 10 });
    expect(fields(errors)).toEqual(['vendorName']);
    expect(errors[0].message).toBe('vendorName must not be empty');
  });

  test('rejects a whitespace-only vendor name', () => {
    expect(fields(validatePurchaseOrder({ vendorName: '   ', quantity: 10 }))).toEqual(['vendorName']);
  });

  test('rejects a missing vendor name on create', () => {
    expect(fields(validatePurchaseOrder({ quantity: 10 }))).toEqual(['vendorName']);
  });

  test('rejects a non-string vendor name', () => {
    expect(fields(validatePurchaseOrder({ vendorName: 42, quantity: 10 }))).toEqual(['vendorName']);
  });

  test('rejects quantity 0', () => {
    const errors = validatePurchaseOrder({ vendorName: 'Acme', quantity: 0 });
    expect(fields(errors)).toEqual(['quantity']);
    expect(errors[0].message).toBe('quantity must be greater than 0');
  });

  test('rejects a negative quantity', () => {
    expect(fields(validatePurchaseOrder({ vendorName: 'Acme', quantity: -5 }))).toEqual(['quantity']);
  });

  test('rejects a non-numeric quantity', () => {
    expect(fields(validatePurchaseOrder({ vendorName: 'Acme', quantity: 'ten' }))).toEqual(['quantity']);
  });

  test('rejects NaN and Infinity as quantity', () => {
    expect(fields(validatePurchaseOrder({ vendorName: 'Acme', quantity: NaN }))).toEqual(['quantity']);
    expect(fields(validatePurchaseOrder({ vendorName: 'Acme', quantity: Infinity }))).toEqual(['quantity']);
  });

  test('reports both fields when both are invalid', () => {
    const errors = validatePurchaseOrder({ vendorName: '', quantity: -1 });
    expect(fields(errors)).toEqual(['vendorName', 'quantity']);
  });

  test('partial (UPDATE) skips fields that are absent', () => {
    expect(validatePurchaseOrder({}, { partial: true })).toEqual([]);
    expect(validatePurchaseOrder({ quantity: 3 }, { partial: true })).toEqual([]);
  });

  test('partial (UPDATE) still rejects fields that are present but invalid', () => {
    expect(fields(validatePurchaseOrder({ vendorName: '' }, { partial: true }))).toEqual(['vendorName']);
    expect(fields(validatePurchaseOrder({ quantity: 0 }, { partial: true }))).toEqual(['quantity']);
    expect(fields(validatePurchaseOrder({ quantity: null }, { partial: true }))).toEqual(['quantity']);
  });
});
