import os
import tkinter as tk

from functools import partial

from activitymanager import ActivityManager


class UI:
    def __init__(self, activity_manager: ActivityManager):
        self.activity_manager = activity_manager
    
    
    def get_plugin_frame(self, parent: tk.Frame) -> tk.Frame:
        self.frame = tk.Frame(parent)

        tk.Label(self.frame, text='PP Tracker').grid(row=0, column=0)
        self.latest_tallies_button = tk.Button(self.frame, text='Latest PP Tally', command=self._show_activity_window)
        self.latest_tallies_button.grid(row=0, column=1)
        self.previous_tallies_button = tk.Button(self.frame, text="Previous PP Tallies", command=self._previous_tallies_popup)
        self.previous_tallies_button.grid(row=0, column=2)

        return self.frame


    def _show_activity_window(self, file=''):
        if file == '':
            system_tallies = self.activity_manager.system_tallies
        else:
            system_tallies = self.activity_manager._load_tallies(file)
            if system_tallies is None:
                return

        self.toplevel = tk.Toplevel(self.frame)
        self.toplevel.title('PP Tracker - Total Merits')
        self.toplevel.protocol("WM_DELETE_WINDOW", self._window_closed)

        self.table = tk.Frame(self.toplevel)
        self.table.pack(fill=tk.BOTH, side=tk.TOP, padx=5, pady=5, expand=tk.YES)

        col = 0
        tk.Label(self.table, text="System").grid(row=0, column=0, padx=2, pady=2); col += 1
        tk.Frame(self.table, width=1, bg="black").grid(row=0, column=col, rowspan=len(system_tallies)+2, sticky="ns", padx=5); col += 1

        # Total
        tk.Label(self.table, text="Total").grid(row=0, column=col, padx=2, pady=2); col += 1
        tk.Frame(self.table, width=2, bg="black").grid(row=0, column=col, rowspan=len(system_tallies)+2, sticky="ns", padx=5); col += 1

        # Aid activities
        tk.Label(self.table, text="Aid (WIP)").grid(row=0, column=col, columnspan=3, padx=2, pady=2)
        tk.Label(self.table, text="Donate").grid(row=1, column=col, padx=2, pady=2); col += 1
        tk.Label(self.table, text="Pods (X)").grid(row=1, column=col, padx=2, pady=2); col += 1
        tk.Label(self.table, text="Salv").grid(row=1, column=col, padx=2, pady=2); col += 1
        tk.Frame(self.table, width=1, bg="black").grid(row=0, column=col, rowspan=len(system_tallies)+2, sticky="ns", padx=5); col += 1

        # Combat activities
        tk.Label(self.table, text="Combat").grid(row=0, column=col, columnspan=2, padx=2, pady=2)
        tk.Label(self.table, text="BH").grid(row=1, column=col, padx=2, pady=2); col += 1
        tk.Label(self.table, text="PK").grid(row=1, column=col, padx=2, pady=2); col += 1
        tk.Frame(self.table, width=1, bg="black").grid(row=0, column=col, rowspan=len(system_tallies)+2, sticky="ns", padx=5); col += 1

        # Exploration activities
        tk.Label(self.table, text="Exploration").grid(row=0, column=col, columnspan=2, padx=2, pady=2)
        tk.Label(self.table, text="ExoBio").grid(row=1, column=col, padx=2, pady=2); col += 1
        tk.Label(self.table, text="Expl").grid(row=1, column=col, padx=2, pady=2); col += 1
        tk.Frame(self.table, width=1, bg="black").grid(row=0, column=col, rowspan=len(system_tallies)+2, sticky="ns", padx=5); col += 1

        # Odyssey activities
        tk.Label(self.table, text="Odyssey (WIP)").grid(row=0, column=col, columnspan=4, padx=2, pady=2)
        tk.Label(self.table, text="Reboots").grid(row=1, column=col, padx=2, pady=2); col += 1
        tk.Label(self.table, text="Goods").grid(row=1, column=col, padx=2, pady=2); col += 1
        tk.Label(self.table, text="Data").grid(row=1, column=col, padx=2, pady=2); col += 1
        tk.Label(self.table, text="Mal").grid(row=1, column=col, padx=2, pady=2); col += 1
        tk.Frame(self.table, width=1, bg="black").grid(row=0, column=col, rowspan=len(system_tallies)+2, sticky="ns", padx=5); col += 1

        # Trade activities
        tk.Label(self.table, text="Trade").grid(row=0, column=col, columnspan=5, padx=2, pady=2)
        tk.Label(self.table, text="Low").grid(row=1, column=col, padx=2, pady=2); col += 1
        tk.Label(self.table, text="Profit").grid(row=1, column=col, padx=2, pady=2); col += 1
        tk.Label(self.table, text="Mine").grid(row=1, column=col, padx=2, pady=2); col += 1
        tk.Label(self.table, text="Comod").grid(row=1, column=col, padx=2, pady=2); col += 1
        tk.Label(self.table, text="Rare (X)").grid(row=1, column=col, padx=2, pady=2); col += 1
        tk.Frame(self.table, width=1, bg="black").grid(row=0, column=col, rowspan=len(system_tallies)+2, sticky="ns", padx=5); col += 1

        # Misc activities
        tk.Label(self.table, text="Misc").grid(row=0, column=col, columnspan=4, padx=2, pady=2)
        tk.Label(self.table, text="Crimes").grid(row=1, column=col, padx=2, pady=2); col += 1
        tk.Label(self.table, text="Holo (WIP)").grid(row=1, column=col, padx=2, pady=2); col += 1
        tk.Label(self.table, text="Scan").grid(row=1, column=col, padx=2, pady=2); col += 1
        tk.Label(self.table, text="M-Scan (WIP)").grid(row=1, column=col, padx=2, pady=2); col += 1
        tk.Label(self.table, text="Unknown").grid(row=1, column=col, padx=2, pady=2); col += 1

        # Add system activity tallies
        row = 2
        for system, tally in system_tallies.items():
            col = 0
            tk.Label(self.table, text=system).grid(row=row, column=col, padx=2, pady=2); col += 1
            col += 1

            # Total
            tk.Label(self.table, text=tally.get_total()).grid(row=row, column=col, padx=2, pady=2); col += 1
            col += 1

            # Aid activities
            tk.Label(self.table, text=str(tally.donation_missions)).grid(row=row, column=col, padx=2, pady=2); col += 1
            tk.Label(self.table, text=str(tally.escape_pods)).grid(row=row, column=col, padx=2, pady=2); col += 1
            tk.Label(self.table, text=str(tally.salvage)).grid(row=row, column=col, padx=2, pady=2); col += 1
            col += 1

            # Combat activitie
            tk.Label(self.table, text=str(tally.bounties)).grid(row=row, column=col, padx=2, pady=2); col += 1
            tk.Label(self.table, text=str(tally.power_kills)).grid(row=row, column=col, padx=2, pady=2); col += 1
            col += 1

            # Exploration activities
            tk.Label(self.table, text=str(tally.exobiology)).grid(row=row, column=col, padx=2, pady=2); col += 1
            tk.Label(self.table, text=str(tally.exploration)).grid(row=row, column=col, padx=2, pady=2); col += 1
            col += 1

            # Odyssey activities
            tk.Label(self.table, text=str(tally.reboot_missions)).grid(row=row, column=col, padx=2, pady=2); col += 1
            tk.Label(self.table, text=str(tally.odyssey_goods)).grid(row=row, column=col, padx=2, pady=2); col += 1
            tk.Label(self.table, text=str(tally.odyssey_data)).grid(row=row, column=col, padx=2, pady=2); col += 1
            tk.Label(self.table, text=str(tally.odyssey_malware)).grid(row=row, column=col, padx=2, pady=2); col += 1
            col += 1

            # Trade activities
            tk.Label(self.table, text=str(tally.flood_low_value)).grid(row=row, column=col, padx=2, pady=2); col += 1
            tk.Label(self.table, text=str(tally.sell_profit)).grid(row=row, column=col, padx=2, pady=2); col += 1
            tk.Label(self.table, text=str(tally.mining)).grid(row=row, column=col, padx=2, pady=2); col += 1
            tk.Label(self.table, text=str(tally.pp_commodities)).grid(row=row, column=col, padx=2, pady=2); col += 1
            tk.Label(self.table, text=str(tally.rare_goods)).grid(row=row, column=col, padx=2, pady=2); col += 1
            col += 1

            # Misc activities
            tk.Label(self.table, text=str(tally.crimes)).grid(row=row, column=col, padx=2, pady=2); col += 1
            tk.Label(self.table, text=str(tally.holoscreen_hacking)).grid(row=row, column=col, padx=2, pady=2); col += 1
            tk.Label(self.table, text=str(tally.ship_wake_scans)).grid(row=row, column=col, padx=2, pady=2); col += 1
            tk.Label(self.table, text=str(tally.megaship_scans)).grid(row=row, column=col, padx=2, pady=2); col += 1
            tk.Label(self.table, text=str(tally.unknown)).grid(row=row, column=col, padx=2, pady=2); col += 1
            row += 1

        # Add button for creating new report
        if file == '':
            new_report_text = "Create a new report:"
            tk.Label(self.table, text=new_report_text).grid(row=row, column=0, columnspan=4, padx=2, pady=2)
            tk.Button(self.table, text='Create new PP report', command=self._create_new_report).grid(row=row, column=4, columnspan=3, padx=2, pady=2)


    def _window_closed(self):
        self.toplevel.destroy()


    def _create_new_report(self):
        self.activity_manager._create_new_tally()
        self._window_closed()
        self._show_activity_window()


    def _previous_tallies_popup(self):
        menu = tk.Menu(self.frame, tearoff = 0)

        files = os.listdir(self.activity_manager.tallies_dir)
        # Iterate files in reverse order, so latest tallies show first.
        for file in files[::-1]:
            if file == 'tally.json':
                continue
            
            timestamp = file.replace('tally.', '').replace('.json', '')
            parts = timestamp.split('T')
            timestamp = parts[0] + "T" + parts[1].replace('-', ':')
            menu.add_command(label=timestamp, command=partial(self._show_activity_window, file))

        try:
            menu.tk_popup(self.previous_tallies_button.winfo_rootx(), self.previous_tallies_button.winfo_rooty())
        finally:
            menu.grab_release()
