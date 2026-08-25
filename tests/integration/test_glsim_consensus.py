from __future__ import annotations
import json
from pathlib import Path
from gltest import get_contract_factory, get_validator_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

PROMPT = "independently map release notes"
ARGS = ["August workspace update", "1. Added CSV report export.\n2. Fixed password-reset addresses containing plus signs.\n3. Added a visible 10 MB upload limit.", 3, "Each numbered user-facing feature, fix, and limitation requires a clear and accurate mention in the notes.", "Reports export as CSV. Password resets support plus signs. Uploads have a visible 10 MB limit."]

def context():
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {PROMPT: json.dumps({"coverage_mask": "111"})}})
    return {"validators": [v.to_dict() for v in validators]}

def test_five_validator_coverage_publish_gate():
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "release_note_check.py")
    deployed = factory.deploy_contract_tx(args=ARGS, wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(deployed)
    contract = factory.build_contract(extract_contract_address(deployed))
    audited = contract.audit_current_notes(args=[]).transact(transaction_context=context(), wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(audited)
    published = contract.publish(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(published)
    assert contract.get_state(args=[]).call()["phase"] == "PUBLISHED"

