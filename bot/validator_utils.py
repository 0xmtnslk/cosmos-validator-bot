import re
import subprocess

def validate_validator_address(address: str) -> bool:
    validator_address_regex = r'^(dymvaloper|valoper)[0-9a-z]{39}$'
    return bool(re.match(validator_address_regex, address, re.IGNORECASE))

def sanitize_input(input_str: str) -> str:
    return ''.join(c for c in input_str if c.isalnum())

def restart_tenderduty():
    try:
        subprocess.run(['systemctl', 'restart', 'tenderduty'], check=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to restart Tenderduty: {str(e)}")
