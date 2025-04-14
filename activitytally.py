from dataclasses import dataclass, fields


@dataclass
class ActivityTally:
    # Aid
    donation_missions: int = 0  # Complete Aid and Humanitarian Missions
    escape_pods: int = 0  # (Disabled) Collect Escape Pods
    salvage: int = 0  # Hand in Salvage

    # Combat
    bounties: int = 0  # Bounty Hunting
    power_kills: int = 0  # Power Kills

    # Exploration
    exobiology: int = 0  # Hand in Biological Research Samples
    exploration: int = 0  # Hand in Cartography Data

    # Odyssey
    reboot_missions: int = 0  # Reboot Mission Completion
    odyssey_goods: int = 0  # Retrieve Specific Goods (Odyssey PP containers)
    odyssey_data: int = 0  # Transport Power Classified/Association/Political/Research/Industrial Data
    odyssey_malware: int = 0  # Upload Powerplay-Specific Malware

    # Trade
    flood_low_value: int = 0  # Flood Markets with Low Value Goods (<500 Cr)
    sell_profit: int = 0  # Sell for Large Profits (>40%)
    mining: int = 0  # Sell Mined Resources
    pp_commodities: int = 0  # Transport Power Commodities (papers)
    rare_goods: int = 0  # (Disabled) Sell Rare Goods

    # Misc
    crimes: int = 0  # Commit Crimes
    holoscreen_hacking: int = 0  # Holoscreen Hacking
    ship_wake_scans: int = 0  # Scan Ships and Wakes
    megaship_scans: int = 0  # Scan Datalinks (at Megaships)

    unknown: int = 0

    def get_total(self):
        sum = 0
        for field in fields(self):
            if field.type is int:
                sum += getattr(self, field.name)
        return sum
