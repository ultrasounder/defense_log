# logic.py

def check_lifecycle_status(part_number, description):
    """
    Analyzes part metadata to determine lifecycle risk.
    """
    # Normalize inputs
    part_upper = str(part_number).upper()
    desc_upper = str(description).upper()
    
    # The Logic Rules
    if "OBS" in part_upper or "OBS" in desc_upper or "LEGACY" in part_upper:
        return "OBSOLETE", "❌ Critical Risk: Component is end-of-life."
    elif "ATMEGA" in part_upper:
        return "NRND", "⚠️ Warning: Not Recommended for New Designs."
    else:
        return "Active", "✅ Safe: Active lifecycle."