from pathlib import Path
import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

ARGS = ["August workspace update", "1. Added CSV report export.\n2. Fixed password-reset addresses containing plus signs.\n3. Added a visible 10 MB upload limit.", 3, "Each numbered user-facing feature, fix, and limitation requires a clear and accurate mention in the notes.", "Reports export as CSV. Password resets support plus signs. Uploads have a visible 10 MB limit."]

@pytest.mark.integration
def test_studionet_release_coverage(default_account):
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "release_note_check.py")
    deployed = factory.deploy_contract_tx(args=ARGS, account=default_account, wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(deployed)
    address = extract_contract_address(deployed)
    contract = factory.build_contract(address, account=default_account)
    audited = contract.audit_current_notes(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(audited)
    version = contract.get_version(args=[1]).call()
    assert len(version["coverage_mask"]) == 3
    assert set(version["coverage_mask"]).issubset({"0", "1"})
    print(f"STUDIONET_ADDRESS={address}")
    print(f"STUDIONET_DEPLOY_TX={deployed['hash']}")
    print(f"STUDIONET_WRITE_TX={audited['hash']}")
    print(f"STUDIONET_RESULT={version['coverage_mask']}")

