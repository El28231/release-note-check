from pathlib import Path
import json

CONTRACT = Path(__file__).resolve().parents[2] / "contracts" / "release_note_check.py"
SDK = "v0.2.16"
PROMPT = "independently map release notes"
ARGS = (
    "August workspace update",
    "1. Added CSV report export.\n2. Fixed password-reset addresses containing plus signs.\n3. Added a visible 10 MB upload limit.",
    3,
    "Each numbered user-facing feature, fix, and limitation requires a clear and accurate mention in the notes.",
    "Reports can now be exported as CSV. Password resets now work for addresses containing plus signs.",
)


def deploy(vm, direct_deploy, alice):
    vm.sender = alice
    return direct_deploy(str(CONTRACT), *ARGS, sdk_version=SDK)


def test_coverage_mask_revision_and_publish_gate(direct_vm, direct_deploy, direct_alice):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    direct_vm.mock_llm(PROMPT, json.dumps({"coverage_mask": "110"}))
    contract.audit_current_notes()
    assert contract.get_state()["phase"] == "GAPS_FOUND"
    contract.submit_revision("Reports can now be exported as CSV. Password resets support plus signs. Uploads now have a visible 10 MB limit.")
    direct_vm.clear_mocks()
    direct_vm.mock_llm(PROMPT, json.dumps({"coverage_mask": "111"}))
    contract.audit_current_notes()
    assert contract.get_state()["phase"] == "PUBLISHABLE"
    contract.publish()
    assert contract.get_version(2)["published"] is True
    leader = direct_vm._captured_validators[-1][0]
    assert direct_vm.run_validator(leader_result=leader) is True


def test_only_owner_revises_and_publish_requires_full_mask(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    with direct_vm.expect_revert("release_not_publishable"):
        contract.publish()
    direct_vm.mock_llm(PROMPT, json.dumps({"coverage_mask": "100"}))
    contract.audit_current_notes()
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("only_owner"):
        contract.submit_revision("A replacement note long enough to pass text bounds but submitted by the wrong account.")


def test_bad_mask_length_fails_closed(direct_vm, direct_deploy, direct_alice):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    direct_vm.mock_llm(PROMPT, json.dumps({"coverage_mask": "11"}))
    with direct_vm.expect_revert("invalid_mask_length"):
        contract.audit_current_notes()
    assert contract.get_state()["phase"] == "DRAFT"

