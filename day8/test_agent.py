import json, os, shutil, pytest
import agent_core as core

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "requisitions.json")) as f:
    REQS = json.load(f)
EXPECTED = {"PR1": "PO created", "PR2": "PO created", "PR3": "PO created",
            "PR4": "Sent to manager", "PR5": "Sent to manager"}


@pytest.fixture
def base(tmp_path):
    for n in ("suppliers.csv", "requisitions.json"):
        shutil.copy(os.path.join(HERE, n), tmp_path)
    return str(tmp_path)


@pytest.mark.parametrize("req", REQS, ids=lambda r: r["id"])
def test_five_cases(req, base):
    e = core.decide(req, base)
    assert e["decision"] == EXPECTED[req["id"]]
    assert e["reason"].strip()


def test_pr4_reason_is_new_supplier(base):
    assert "New supplier" in core.decide(REQS[3], base)["reason"]


def test_pr5_reason_is_amount(base):
    assert "25 lakh" in core.decide(REQS[4], base)["reason"]


def test_totals_3_auto_2_manager(base):
    core.process_all(base)
    assert len(core._read("po_created.json", base)) == 3
    assert len(core._read("manager_queue.json", base)) == 2
    log = core._read("decision_log.json", base)
    assert len(log) == 5 and all(e["reason"] for e in log)


def test_boundary_exactly_25_lakh_gets_po(base):
    e = core.decide({"id": "PR6", "supplier": "Sharma Steels", "amount": 2_500_000}, base)
    assert e["decision"] == "PO created"


def test_unknown_supplier_goes_to_manager(base):
    e = core.decide({"id": "PR7", "supplier": "Ghost Ltd", "amount": 1000}, base)
    assert e["decision"] == "Sent to manager"


def test_no_duplicate_po(base):
    core.decide(REQS[0], base)
    core.decide(REQS[0], base)
    assert len(core._read("po_created.json", base)) == 1
