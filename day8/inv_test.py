"""Unit tests for invoice validation rules and the audit log. Run: python3 -m unittest -v inv_test"""
import json
import os
import tempfile
import unittest

from inv_tools import BASE, validate_invoice


def make(**changes):
    """A valid invoice for PO-4501 (Sharma Steels, PO amount 450000), overridden by changes."""
    inv = {"invoice_no": "INV-T1", "vendor": "Sharma Steels", "po_number": "PO-4501",
           "invoice_date": "2026-11-02", "net_amount": 450000, "tax_amount": 81000,
           "total_amount": 531000}
    inv.update(changes)
    return inv


class InvoiceOutcomeTests(unittest.TestCase):
    """The five invoices in invoices.json, with their expected outcomes."""

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(BASE, "invoices.json"), encoding="utf-8") as f:
            cls.invoices = {i["invoice_no"]: i for i in json.load(f)}

    def _check(self, inv_no, status, reason_fragment=None):
        seen = []
        r = validate_invoice(self.invoices[inv_no], seen)
        self.assertEqual(r["status"], status, r["reasons"])
        if reason_fragment:
            self.assertTrue(any(reason_fragment in x for x in r["reasons"]), r["reasons"])

    def test_inv_1001_clean(self):
        self._check("INV-1001", "clean")

    def test_inv_1002_clean(self):
        self._check("INV-1002", "clean")

    def test_inv_1003_clean_within_tolerance(self):
        # net 985000 vs PO 980000 = +0.51%, inside the 2% tolerance
        self._check("INV-1003", "clean")

    def test_inv_1004_exception_po_not_found(self):
        self._check("INV-1004", "exception", "PO not found: PO-4599")

    def test_inv_1005_exception_exceeds_po(self):
        self._check("INV-1005", "exception", "exceeds PO amount")


class ToleranceTests(unittest.TestCase):
    """PO-4501 amount is 450000; the limit is 2% = 459000."""

    def test_net_at_limit_is_clean(self):
        r = validate_invoice(make(net_amount=459000, tax_amount=81000, total_amount=540000))
        self.assertEqual(r["status"], "clean", r["reasons"])

    def test_net_one_rupee_over_limit_is_exception(self):
        r = validate_invoice(make(net_amount=459001, tax_amount=81000, total_amount=540001))
        self.assertEqual(r["status"], "exception")
        self.assertTrue(any("exceeds PO amount" in x for x in r["reasons"]), r["reasons"])


class VendorTests(unittest.TestCase):

    def test_vendor_case_and_spaces_ignored(self):
        r = validate_invoice(make(vendor="  sharma STEELS  "))
        self.assertEqual(r["status"], "clean", r["reasons"])

    def test_vendor_mismatch_is_exception(self):
        r = validate_invoice(make(vendor="Vizag Paints"))
        self.assertEqual(r["status"], "exception")
        self.assertTrue(any(x.startswith("Vendor mismatch") for x in r["reasons"]), r["reasons"])


class RuleTests(unittest.TestCase):

    def test_closed_po_is_exception(self):
        # PO-4505 is closed; amounts and vendor match, so only the status should fail
        r = validate_invoice(make(vendor="Guntur Cables", po_number="PO-4505",
                                  net_amount=100000, tax_amount=18000, total_amount=118000))
        self.assertEqual(r["status"], "exception")
        self.assertTrue(any("closed" in x for x in r["reasons"]), r["reasons"])

    def test_missing_field_is_exception(self):
        inv = make()
        del inv["vendor"]
        r = validate_invoice(inv)
        self.assertEqual(r["status"], "exception")
        self.assertIn("Missing required field: vendor", r["reasons"])

    def test_duplicate_invoice_number_is_exception(self):
        r = validate_invoice(make(invoice_no="INV-1001"), seen_invoice_nos=["inv-1001"])
        self.assertEqual(r["status"], "exception")
        self.assertTrue(any(x.startswith("Duplicate invoice number") for x in r["reasons"]), r["reasons"])

    def test_total_mismatch_is_exception(self):
        r = validate_invoice(make(total_amount=531500))  # net + tax = 531000, off by 500
        self.assertEqual(r["status"], "exception")
        self.assertTrue(any(x.startswith("Total ") for x in r["reasons"]), r["reasons"])

    def test_non_numeric_amount_is_exception(self):
        r = validate_invoice(make(net_amount="four lakh"))
        self.assertEqual(r["status"], "exception")
        self.assertIn("Amount is not a number", r["reasons"])

    def test_missing_po_master_fails_safe(self):
        # an empty folder has no inv_po_master.csv: must be an exception, never a pass
        with tempfile.TemporaryDirectory() as empty:
            r = validate_invoice(make(), base=empty)
        self.assertEqual(r["status"], "exception")
        self.assertTrue(any("PO master unavailable" in x for x in r["reasons"]), r["reasons"])


class AuditLogTests(unittest.TestCase):

    def test_audit_log_has_5_entries_all_not_posted(self):
        path = os.path.join(BASE, "inv_audit_log.json")
        self.assertTrue(os.path.exists(path), "inv_audit_log.json missing: run inv_pipeline.py first")
        with open(path, encoding="utf-8") as f:
            entries = json.load(f)
        self.assertEqual(len(entries), 5)
        self.assertTrue(all(e["posted"] is False for e in entries))


if __name__ == "__main__":
    unittest.main()
