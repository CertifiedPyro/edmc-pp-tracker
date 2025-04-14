import copy
import dataclasses
import json
import os

from datetime import datetime, timezone
from logging import Logger
from typing import Any

from activitytally import ActivityTally


class ActivityManager:
    def __init__(self, logger: Logger):
        self.logger = logger

        # TODO: Keep track of cmdr name
        self.cmdr_power: str = ''

        self.system: str = ''
        self.system_powerplay_state: str = ''
        self.system_controlling_power: str = ''

        self.last_pp_entry: dict[str, Any] = {}
        self.system_tallies: dict[str, ActivityTally] = {}


    def plugin_start3(self, plugin_dir: str):
        self.plugin_dir = plugin_dir
        self.tallies_dir = os.path.join(self.plugin_dir, 'tallies')
        self.tally_file = os.path.join(self.tallies_dir, 'tally.json')

        tallies = self._load_tallies()
        if tallies is not None:
            self.system_tallies = tallies


    def journal_entry(self, cmdr: str, is_beta: bool, system: str, station: str, entry: dict[str, Any], state: dict[str, Any]):
        event = entry['event']

        # Get cmdr's powerplay power.
        if event == 'Powerplay':
            self.cmdr_power = str(entry.get('Power', ''))
            self.logger.error(f'Commander pledged power {self.cmdr_power}')
            return

        # If system has changed, store Powerplay state for the system if it exists.
        if system != self.system:
            self.system = system
            if 'PowerplayState' in entry:
                system_controlling_power = entry.get('ControllingPower')
                system_powerplay_state = entry.get('PowerplayState')
        
        if event == 'PowerplayMerits':
            merits = int(entry['MeritsGained'])
            self._add_merits(merits)
        
        self._store_relevant_entry(entry)


    def _add_merits(self, merits):
        entry = self.last_pp_entry
        event: str = entry.get('event', '')

        tally: ActivityTally
        if self.system in self.system_tallies:
            tally = self.system_tallies[self.system]
        else:
            tally = ActivityTally()
            self.system_tallies[self.system] = tally

        reset_last_entry = True

        # Aid
        if event == 'SearchAndRescue':
            # Assume this is salvage, since escape pods are disabled
            # TODO: Update once escape pods are re-enabled
            # TODO: Handle potential UM system
            tally.salvage += merits

        # Combat
        elif event == 'Bounty':
            tally.bounties += merits
        elif event == 'FactionKillBond':
            tally.power_kills += merits
        
        # Exploration
        elif event == 'SellOrganicData':
            tally.exobiology += merits
        elif event in ['SellExplorationData', 'MultiSellExplorationData']:
            tally.exploration += merits
        
        # Odyssey (+ Transport Power Commodities)
        # TODO: Need to handle more complicated logic around ACQ/REINF/UM
        elif event == 'PowerplayDeliver':
            # Check if this is power data
            if entry['Type'] in [
                'poweremployeedata',  # Power Association Data
                'powerclassifieddata',  # Power Classified Data
                'powerpropagandadata',  # Power Political Data
                'powerfinancialrecords',  # Power Industrial Data
                'powerresearchdata'  # Power Research Data
            ]:
                tally.odyssey_data += merits
            # Check if this is a specific good (from Odyssey PP containers)
            elif entry['Type'] in [
                'poweragriculture',  # Agricultural Sample
                'powercomputer',  # Computer Parts
                'powermisccomputer', # Data Storage Device
                'powerelectronics',  # Electronics Package
                'powerpower',  # Energy Regulator
                'powerexperiment',  # Experiment Prototype
                'powerextraction',  # Extraction Sample
                'powerindustrial',  # Industrial Component
                'powermiscindust',  # Industrial Machinery
                'powerinventory',  # Inventory Record
                'powermedical',  # Medical Sample
                'powerplaymilitary',  # Military Schematic
                'powerequipment',  # Personal Protective Equipment
                'powerresearch',  # Research Notes
                'powersecurity',  # Security Logs
            ]:
                tally.odyssey_goods += merits
            else:
                # Assume this is a power commodity
                tally.pp_commodities += merits
        
        # Trade
        elif event == 'MarketSell':
            # Assume that 0 price commodities only come from mining, and they aren't mixed with bought commodities.
            if entry['AvgPricePaid'] == 0:
                tally.mining += merits
            # TODO: Check if this includes commodities that are exactly 500Cr.
            elif entry['SellPrice'] < 500:
                tally.flood_low_value += merits
            else:
                tally.sell_profit += merits

        # Misc
        elif event == 'CommitCrime':
            tally.crimes += merits
        # Assume if merits is 20, it was from a ship scan after checking all other options.
        elif merits == 20:
            tally.ship_wake_scans += merits
            reset_last_entry = False
        else:
            tally.unknown += merits
            self.logger.error(f"Unknown event earned {merits} merits: {self.last_pp_entry}")
        
        if reset_last_entry:
            self.last_pp_entry = {}
        self._save_tallies()


    def _store_relevant_entry(self, entry: dict[str, Any]):
        event = entry['event']
        
        # Ignore ship/wake scans
        if event in [
                # Bounty Hunting
                'Bounty',
                # Power Kills
                'FactionKillBond'
                # Hand in Biological Research Samples
                'SellOrganicData',
                # Hand in Cartography Data
                'SellExplorationData',  # Single system
                'MultiSellExplorationData',  # Page of systems
                # Retrieve Specific Goods
                # Transport Power Classified/Association/Political/Research/Industrial Data
                # Transport Power Commodities
                'PowerplayDeliver',
                # Flood Markets with Low Value Goods
                # Sell for Large Profits
                # Sell Mined Resources
                'MarketSell',
                # Commit Crimes
                'CommitCrime',
                # Hand in Salvage
                'SearchAndRescue']:
            self.last_pp_entry = copy.deepcopy(entry)


    def _save_tallies(self):
        serialized_tallies = {}
        for system_name, tally in self.system_tallies.items():
            serialized_tallies[system_name] = dataclasses.asdict(tally)
        
        if not os.path.exists(self.tallies_dir):
            os.makedirs(self.tallies_dir)

        try:
            with open(self.tally_file, 'w') as f:
                json.dump(serialized_tallies, f)
        except IOError as e:
            self.logger.error(f"Error writing to file '{self.tally_file}': {e}")


    def _load_tallies(self, filename='') -> dict[str, ActivityTally]|None:
        if not os.path.exists(self.tallies_dir):
            return
        
        if filename == '':
            filename = self.tally_file
        else:
            filename = os.path.join(self.tallies_dir, filename)
        if not os.path.exists(filename):
            return

        try:
            with open(filename, 'r') as f:
                loaded_data = json.load(f)

            tallies = {}
            for key, tally_data in loaded_data.items():
                tallies[key] = ActivityTally(**tally_data)
            self.logger.error(f"System tallies loaded from '{filename}'")
            return tallies
        except Exception as e:
            self.logger.error(f"An unexpected error occurred while loading from '{filename}': {e}")


    def _create_new_tally(self):
        try:
            new_file_name = self.tally_file
            formatted_datetime = datetime.now(timezone.utc).isoformat(timespec='seconds')
            formatted_datetime = formatted_datetime.replace('+00:00', '').replace(':', '-')
            new_file_name = new_file_name.replace('.json', f".{formatted_datetime}.json")
            os.rename(self.tally_file, new_file_name)

            self.last_pp_entry = {}
            self.system_tallies = {}
        except FileExistsError:
            self.logger.error(f"Error: A file with the name '{new_file_name}' already exists.")
        except OSError as e:
            self.logger.error(f"Error renaming tally file: {e}")
