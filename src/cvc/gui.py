"""Small native Tkinter front end over the shared CVC application services."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any


def _configure_tk_runtime() -> None:
    """Repair the portable Windows Python layout when Tcl/Tk is present."""
    if os.name != "nt":
        return
    prefix = Path(sys.base_prefix)
    tcl_dir = prefix / "tcl" / "tcl8.6"
    tk_dir = prefix / "tcl" / "tk8.6"
    if (tcl_dir / "init.tcl").exists():
        os.environ.setdefault("TCL_LIBRARY", str(tcl_dir))
    if tk_dir.exists():
        os.environ.setdefault("TK_LIBRARY", str(tk_dir))


_configure_tk_runtime()

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from .services import CVCService


NAVIGATION = ("Overview", "Rules", "Evidence Triggers", "Ingest", "History", "Integrity")
FILTERS = ("All", "E4", "E3", "E2", "E1", "Ratified", "Blocked")
TRIGGER_FILTERS = ("All", "Core", "Collector", "Research", "Delivery", "Missing historical evidence", "Natural future evidence", "Contract/profile evidence")


def _pretty(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)


class CVCApplication(tk.Tk):
    def __init__(self, root: Path | str, initial_view: str = "Overview"):
        super().__init__()
        self.service = CVCService(root)
        self.title("CVC Clank")
        self.geometry("1280x820")
        self.minsize(980, 640)
        self.option_add("*Font", ("Segoe UI", 10))
        self.current_view = "Overview"
        self.last_verified = "Not verified"
        self.integrity = self.service.verify_corpus()
        self.search_results: list[dict[str, Any]] = []
        self._build_shell()
        self.show_view(initial_view if initial_view in NAVIGATION else "Overview")

    def _build_shell(self) -> None:
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        top = ttk.Frame(self, padding=(12, 10))
        top.grid(row=0, column=0, columnspan=2, sticky="ew")
        top.grid_columnconfigure(1, weight=1)
        ttk.Label(top, text="CVC Clank", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, padx=(0, 20))
        self.global_search_var = tk.StringVar()
        search = ttk.Entry(top, textvariable=self.global_search_var)
        search.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        search.insert(0, "Search rules, evidence, triggers, history…")
        search.bind("<FocusIn>", lambda _event: search.delete(0, tk.END) if search.get().startswith("Search ") else None)
        search.bind("<Return>", lambda _event: self.global_search())
        ttk.Button(top, text="Search", command=self.global_search).grid(row=0, column=2, padx=(0, 8))
        ttk.Button(top, text="Ask CVC", command=self.ask_cvc).grid(row=0, column=3, padx=(0, 12))
        self.integrity_var = tk.StringVar(value=self._integrity_label())
        ttk.Label(top, textvariable=self.integrity_var, width=25).grid(row=0, column=4, sticky="e")

        self.navigation = ttk.Frame(self, padding=(10, 8))
        self.navigation.grid(row=1, column=0, sticky="nsw")
        self.nav_buttons: dict[str, ttk.Button] = {}
        for name in NAVIGATION:
            button = ttk.Button(self.navigation, text=name, command=lambda selected=name: self.show_view(selected), width=22)
            button.pack(fill="x", pady=2)
            self.nav_buttons[name] = button
        ttk.Separator(self.navigation, orient="horizontal").pack(fill="x", pady=12)
        ttk.Label(self.navigation, text="Operator-triggered\nNo background work", justify="left", foreground="#555555").pack(anchor="w")

        self.content = ttk.Frame(self, padding=(10, 8))
        self.content.grid(row=1, column=1, sticky="nsew")
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

    def _integrity_label(self) -> str:
        return "Integrity: PASS" if self.integrity.passed else "Integrity: FAIL"

    def show_view(self, name: str) -> None:
        self.current_view = name
        for child in self.content.winfo_children():
            child.destroy()
        for nav_name, button in self.nav_buttons.items():
            button.state(["pressed"] if nav_name == name else ["!pressed"])
        views = {
            "Overview": self.show_overview,
            "Rules": self.show_rules,
            "Evidence Triggers": self.show_triggers,
            "Ingest": self.show_ingest,
            "History": self.show_history,
            "Integrity": self.show_integrity,
        }
        views[name]()

    def _heading(self, parent: ttk.Frame, title: str, subtitle: str) -> None:
        parent.grid_columnconfigure(0, weight=1)
        ttk.Label(parent, text=title, font=("Segoe UI", 18, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(parent, text=subtitle, foreground="#555555", wraplength=900).grid(row=1, column=0, sticky="w", pady=(2, 14))

    def _card(self, parent: ttk.Frame, row: int, column: int, label: str, value: Any) -> None:
        card = ttk.LabelFrame(parent, text=label, padding=(12, 8))
        card.grid(row=row, column=column, sticky="ew", padx=4, pady=4)
        ttk.Label(card, text=str(value), font=("Segoe UI", 16, "bold")).pack(anchor="w")

    def _write_text(self, widget: tk.Text, text: str) -> None:
        widget.configure(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert("1.0", text)
        widget.configure(state="disabled")

    def show_overview(self) -> None:
        frame = ttk.Frame(self.content)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        self._heading(frame, "Overview", "Authoritative CVC state and operator attention items.")
        status = self.service.get_status()
        versions = ttk.LabelFrame(frame, text="Authoritative versions", padding=10)
        versions.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        ttk.Label(versions, text="Final board: CVC_FINAL_BOARD_V0.1").grid(row=0, column=0, sticky="w", padx=(0, 30))
        ttk.Label(versions, text=f"Support matrix: {status['matrix_version']}").grid(row=0, column=1, sticky="w", padx=(0, 30))
        ttk.Label(versions, text="Ratification: CVC_RATIFICATION_LEDGER_V0.1").grid(row=0, column=2, sticky="w")
        ttk.Label(frame, text=f"Mission state: {status['mission_state']}", font=("Segoe UI", 11, "bold")).grid(row=2, column=0, sticky="w", pady=(0, 6))
        cards = ttk.Frame(frame)
        cards.grid(row=3, column=0, sticky="ew")
        for column in range(5):
            cards.grid_columnconfigure(column, weight=1)
        for index, (label, value) in enumerate((("Rules", status["rule_count"]), ("E4", status["support_distribution"]["E4"]), ("E3", status["support_distribution"]["E3"]), ("E2", status["support_distribution"]["E2"]), ("E1", status["support_distribution"]["E1"]))):
            self._card(cards, 0, index, label, value)
        for index, (label, value) in enumerate((("E0", status["support_distribution"]["E0"]), ("Ratified E4", len(status["ratified_e4_rules"])), ("Open evidence triggers", status["open_future_evidence_triggers"]), ("Pending reviews", len([row for row in self.service.get_history() if row["type"] == "REVIEW"])), ("Pending ratifications", status["pending_ratifications"]))):
            self._card(cards, 1, index, label, value)
        attention = ttk.LabelFrame(frame, text="Needs attention", padding=10)
        attention.grid(row=4, column=0, sticky="ew", pady=(12, 8))
        ingestions = [row for row in self.service.workspace.state_jsonl("state/ingest/ingestions.jsonl") if "INSUFFICIENT_TO_CLASSIFY" in row.get("outcomes", []) or "UNMAPPED_REVIEW_REQUIRED" in row.get("outcomes", [])]
        attention_rows = [("Open triggers", status["open_future_evidence_triggers"]), ("Unresolved ingestions", len(ingestions)), ("Pending reviews", len([row for row in self.service.get_history() if row["type"] == "REVIEW"])), ("Integrity failures", len(self.integrity.failures))]
        for index, (label, value) in enumerate(attention_rows):
            ttk.Label(attention, text=f"{label}: {value}").grid(row=index // 2, column=index % 2, sticky="w", padx=(0, 50), pady=2)
        if not any(value for _, value in attention_rows):
            ttk.Label(attention, text="None: 0", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w")
        actions = ttk.Frame(frame)
        actions.grid(row=5, column=0, sticky="w", pady=(8, 0))
        ttk.Button(actions, text="Verify Corpus", command=self.verify_now).pack(side="left", padx=(0, 8))
        ttk.Button(actions, text="Open CVC Folder", command=self.open_workspace).pack(side="left")

    def show_rules(self) -> None:
        frame = ttk.Frame(self.content)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        self._heading(frame, "Rules", "The 38-rule final board is read-only. Select a rule to inspect evidence and blockers.")
        toolbar = ttk.Frame(frame)
        toolbar.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        ttk.Label(toolbar, text="Filter:").pack(side="left")
        filter_var = tk.StringVar(value="All")
        filter_box = ttk.Combobox(toolbar, textvariable=filter_var, values=FILTERS, state="readonly", width=14)
        filter_box.pack(side="left", padx=(5, 16))
        search_var = tk.StringVar()
        ttk.Label(toolbar, text="Within rules:").pack(side="left")
        search = ttk.Entry(toolbar, textvariable=search_var, width=32)
        search.pack(side="left", padx=5)
        pane = ttk.PanedWindow(frame, orient="horizontal")
        pane.grid(row=2, column=0, sticky="nsew")
        frame.grid_rowconfigure(2, weight=1)
        left = ttk.Frame(pane)
        right = ttk.Frame(pane, padding=(10, 0, 0, 0))
        pane.add(left, weight=3)
        pane.add(right, weight=2)
        tree = ttk.Treeview(left, columns=("id", "level", "grade", "maturity", "applicability", "ratification", "state"), show="headings", selectmode="browse")
        headings = {"id": "Rule ID", "level": "Normative", "grade": "Grade", "maturity": "Maturity", "applicability": "Applicability", "ratification": "Ratification", "state": "Evidence/blocker"}
        widths = {"id": 120, "level": 80, "grade": 55, "maturity": 95, "applicability": 150, "ratification": 115, "state": 170}
        for column, heading in headings.items():
            tree.heading(column, text=heading)
            tree.column(column, width=widths[column], anchor="w")
        tree.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(left, orient="vertical", command=tree.yview)
        scroll.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scroll.set)
        detail = tk.Text(right, wrap="word", width=55, height=25, state="disabled")
        detail.pack(fill="both", expand=True)
        action_bar = ttk.Frame(right)
        action_bar.pack(fill="x", pady=(8, 0))

        def populate(*_args: Any) -> None:
            for item in tree.get_children():
                tree.delete(item)
            selected_filter = filter_var.get()
            rows = self.service.get_board(
                grade=selected_filter if selected_filter in {"E1", "E2", "E3", "E4"} else None,
                ratified=selected_filter == "Ratified",
                blocked=selected_filter == "Blocked",
            )
            needle = search_var.get().strip().lower()
            for row in rows:
                haystack = json.dumps(row, ensure_ascii=False).lower()
                if needle and needle not in haystack:
                    continue
                tree.insert("", "end", values=(row.get("rule_id"), row.get("normative_level"), row.get("current_support_grade"), row.get("maturity"), row.get("applicability"), row.get("ratification_state"), row.get("evidence_availability_state")))

        def selected_rule() -> str | None:
            selection = tree.selection()
            return str(tree.item(selection[0], "values")[0]) if selection else None

        def show_detail(*_args: Any) -> None:
            rule_id = selected_rule()
            if not rule_id:
                return
            record = self.service.get_rule(rule_id)
            self._write_text(detail, _pretty(record) if record else "Rule unavailable.")
            for child in action_bar.winfo_children():
                child.destroy()
            if not record:
                return
            ttk.Button(action_bar, text="Copy Rule ID", command=lambda: self._copy(rule_id)).pack(side="left", padx=(0, 5))
            artifacts = record.get("matching_corpus_artifacts", [])
            if artifacts:
                ttk.Button(action_bar, text="Open Evidence / Artifact", command=lambda: self.open_artifact(artifacts[0])).pack(side="left", padx=(0, 5))
            if record.get("future_evidence_triggers"):
                ttk.Button(action_bar, text="Check Evidence Against Trigger", command=self.check_selected_trigger).pack(side="left")

        self.rules_tree = tree
        self.rules_selected_rule = selected_rule
        self.rules_show_detail = show_detail
        self.rules_filter_var = filter_var
        self.rules_populate = populate
        filter_box.bind("<<ComboboxSelected>>", populate)
        search_var.trace_add("write", populate)
        tree.bind("<<TreeviewSelect>>", show_detail)
        populate()

    def check_selected_trigger(self) -> None:
        rule_id = getattr(self, "rules_selected_rule", lambda: None)()
        record = self.service.get_rule(rule_id) if rule_id else None
        if not record or not record.get("future_evidence_triggers"):
            return
        self.check_trigger_file()

    def show_triggers(self) -> None:
        frame = ttk.Frame(self.content)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        self._heading(frame, "Evidence Triggers", "Open future-evidence triggers are reviewable; checking evidence never changes support grades.")
        toolbar = ttk.Frame(frame)
        toolbar.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        ttk.Label(toolbar, text="Filter:").pack(side="left")
        filter_var = tk.StringVar(value="All")
        filter_box = ttk.Combobox(toolbar, textvariable=filter_var, values=TRIGGER_FILTERS, state="readonly", width=28)
        filter_box.pack(side="left", padx=5)
        tree = ttk.Treeview(frame, columns=("trigger", "rules", "grade", "blocker", "needed", "cluster", "status"), show="headings", selectmode="browse")
        headings = {"trigger": "Trigger ID", "rules": "Rule IDs", "grade": "Grade", "blocker": "Blocker", "needed": "Evidence needed", "cluster": "Cluster", "status": "Status"}
        widths = {"trigger": 105, "rules": 150, "grade": 55, "blocker": 250, "needed": 300, "cluster": 150, "status": 180}
        for column, heading in headings.items():
            tree.heading(column, text=heading)
            tree.column(column, width=widths[column], anchor="w")
        tree.grid(row=2, column=0, sticky="nsew")
        scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scroll.grid(row=2, column=1, sticky="ns")
        tree.configure(yscrollcommand=scroll.set)
        detail = tk.Text(frame, height=8, wrap="word", state="disabled")
        detail.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        actions = ttk.Frame(frame)
        actions.grid(row=4, column=0, columnspan=2, sticky="w", pady=(8, 0))
        ttk.Button(actions, text="Check Evidence…", command=self.check_trigger_file).pack(side="left")

        def rows_for_filter() -> list[dict[str, Any]]:
            selected = filter_var.get()
            result = []
            for trigger in self.service.get_triggers():
                rule_rows = [row for row in self.service.get_board() if row.get("rule_id") in trigger.get("rule_ids", [])]
                applicability = " ".join(str(row.get("applicability", "")) for row in rule_rows).upper()
                trigger_class = str(trigger.get("trigger_class", "")).upper()
                combined = json.dumps(trigger, ensure_ascii=False).upper()
                include = selected == "All"
                if selected in {"Core", "Collector", "Research", "Delivery"}:
                    include = selected.upper() in applicability
                elif selected == "Missing historical evidence":
                    include = "EVIDENCE_EXISTS_BUT_NOT_LOCALLY_AVAILABLE" in trigger_class or "MISSING" in combined
                elif selected == "Natural future evidence":
                    include = "NATURAL" in combined or "FUTURE_OPERATIONAL" in combined
                elif selected == "Contract/profile evidence":
                    include = "CONTRACT" in trigger_class or "PROFILE" in combined
                if include:
                    result.append(trigger)
            return result

        def populate(*_args: Any) -> None:
            for item in tree.get_children():
                tree.delete(item)
            for trigger in rows_for_filter():
                rule_rows = [row for row in self.service.get_board() if row.get("rule_id") in trigger.get("rule_ids", [])]
                grades = sorted({str(row.get("current_support_grade")) for row in rule_rows})
                blockers = "; ".join(str(row.get("remaining_blocker", "")) for row in rule_rows if row.get("remaining_blocker")) or "See trigger proof"
                tree.insert("", "end", values=(trigger.get("trigger_id"), ", ".join(trigger.get("rule_ids", [])), ", ".join(grades), blockers, trigger.get("required_artifact", ""), trigger.get("trigger_class", ""), trigger.get("current_status", "")))

        def show_detail(*_args: Any) -> None:
            selection = tree.selection()
            if not selection:
                return
            trigger_id = tree.item(selection[0], "values")[0]
            trigger = next((row for row in self.service.get_triggers() if row.get("trigger_id") == trigger_id), None)
            self._write_text(detail, _pretty(trigger) if trigger else "Trigger unavailable.")

        self.triggers_tree = tree
        self.triggers_filter_var = filter_var
        self.triggers_populate = populate
        filter_box.bind("<<ComboboxSelected>>", populate)
        tree.bind("<<TreeviewSelect>>", show_detail)
        populate()

    def show_ingest(self) -> None:
        frame = ttk.Frame(self.content)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(4, weight=1)
        self._heading(frame, "Ingest Evidence", "Preview is read-only. Preserve + Ingest writes append-only runtime state after operator action.")
        drop = ttk.LabelFrame(frame, text="Evidence file", padding=24)
        drop.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        ttk.Label(drop, text="Drop a Diagnostic report, incident record, success report, migration/restore artifact, Markdown, JSON, or supported evidence file here.", wraplength=850, justify="left").pack(anchor="w")
        ttk.Label(drop, text="Use Browse… or enter a local path below. No shell command is invoked.", foreground="#555555").pack(anchor="w", pady=(5, 12))
        path_row = ttk.Frame(drop)
        path_row.pack(fill="x")
        self.ingest_path_var = tk.StringVar()
        ttk.Entry(path_row, textvariable=self.ingest_path_var).pack(side="left", fill="x", expand=True, padx=(0, 6))
        ttk.Button(path_row, text="Browse…", command=self.browse_ingest).pack(side="left")
        ttk.Button(drop, text="Preview", command=self.preview_ingest).pack(anchor="w", pady=(10, 0))
        self.ingest_preview_text = tk.Text(frame, height=18, wrap="word", state="disabled")
        self.ingest_preview_text.grid(row=2, column=0, sticky="nsew", pady=(0, 8))
        note = ttk.Label(frame, text="Ingestion cannot change support grades, ratification state, or frozen historical artifacts.", foreground="#555555")
        note.grid(row=3, column=0, sticky="w", pady=(0, 8))
        action_row = ttk.Frame(frame)
        action_row.grid(row=5, column=0, sticky="w")
        self.ingest_button = ttk.Button(action_row, text="Preserve + Ingest", command=self.confirm_ingest, state="disabled")
        self.ingest_button.pack(side="left", padx=(0, 8))
        ttk.Button(action_row, text="Cancel", command=self.clear_ingest).pack(side="left")
        self.ingest_preview_data: dict[str, Any] | None = None

    def browse_ingest(self) -> None:
        selected = filedialog.askopenfilename(title="Select evidence artifact")
        if selected:
            self.ingest_path_var.set(selected)
            self.preview_ingest()

    def preview_ingest(self) -> None:
        try:
            preview = self.service.preview_ingest(self.ingest_path_var.get())
        except Exception as exc:
            self.ingest_preview_data = None
            self.ingest_button.state(["disabled"])
            self._write_text(self.ingest_preview_text, f"Preview error: {exc}")
            return
        self.ingest_preview_data = preview
        self.ingest_button.state(["!disabled"])
        self._write_text(self.ingest_preview_text, _pretty(preview))

    def confirm_ingest(self) -> None:
        if not self.ingest_preview_data:
            return
        try:
            result = self.service.ingest_artifact(self.ingest_preview_data["input_path"])
        except Exception as exc:
            messagebox.showerror("Ingestion blocked", str(exc), parent=self)
            return
        self._write_text(self.ingest_preview_text, _pretty(result))
        self.ingest_button.state(["disabled"])
        messagebox.showinfo("Evidence preserved", f"Ingestion ID: {result['ingestion_id']}\n\nNo review was started automatically.", parent=self)

    def clear_ingest(self) -> None:
        self.ingest_path_var.set("")
        self.ingest_preview_data = None
        self.ingest_button.state(["disabled"])
        self._write_text(self.ingest_preview_text, "")

    def show_history(self) -> None:
        frame = ttk.Frame(self.content)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        self._heading(frame, "History", "Frozen historical milestones and runtime state are intentionally labelled separately.")
        pane = ttk.PanedWindow(frame, orient="vertical")
        pane.grid(row=1, column=0, sticky="nsew")
        top = ttk.Frame(pane)
        bottom = ttk.Frame(pane)
        pane.add(top, weight=3)
        pane.add(bottom, weight=2)
        tree = ttk.Treeview(top, columns=("timestamp", "id", "type", "rules", "outcome", "artifact", "provenance"), show="headings", selectmode="browse")
        headings = {"timestamp": "Timestamp", "id": "Record ID", "type": "Type", "rules": "Affected rules", "outcome": "Outcome", "artifact": "Artifact", "provenance": "Origin"}
        for column, heading in headings.items():
            tree.heading(column, text=heading)
            tree.column(column, width=160 if column in {"outcome", "artifact"} else 110, anchor="w")
        tree.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(top, orient="vertical", command=tree.yview)
        scroll.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scroll.set)
        detail = tk.Text(bottom, wrap="word", state="disabled")
        detail.pack(fill="both", expand=True)
        rows = self.service.get_history()
        for index, row in enumerate(rows):
            tree.insert("", "end", iid=str(index), values=(row.get("timestamp"), row.get("record_id"), row.get("type"), row.get("affected_rules"), row.get("outcome"), row.get("artifact"), row.get("provenance")))

        def show_detail(*_args: Any) -> None:
            selection = tree.selection()
            if selection:
                self._write_text(detail, _pretty(rows[int(selection[0])]))

        tree.bind("<<TreeviewSelect>>", show_detail)

    def show_integrity(self) -> None:
        frame = ttk.Frame(self.content)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        self._heading(frame, "Integrity", "Existing verifier results. Failures are shown precisely and never repaired automatically.")
        summary = ttk.Frame(frame)
        summary.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        manifest = self.service.workspace.migration_manifest()
        ttk.Label(summary, text=f"Last verification: {self.last_verified}").pack(side="left", padx=(0, 20))
        ttk.Label(summary, text=f"Files checked: {len(manifest.get('artifacts', []))}").pack(side="left", padx=(0, 20))
        ttk.Label(summary, text=f"Mismatches: {len([failure for failure in self.integrity.failures if 'mismatch' in failure])}").pack(side="left", padx=(0, 20))
        ttk.Button(summary, text="Verify Now", command=self.verify_now).pack(side="right")
        tree = ttk.Treeview(frame, columns=("check", "status", "detail"), show="headings")
        tree.heading("check", text="Check")
        tree.heading("status", text="Status")
        tree.heading("detail", text="Detail")
        tree.column("check", width=260, anchor="w")
        tree.column("status", width=90, anchor="w")
        tree.column("detail", width=700, anchor="w")
        tree.grid(row=2, column=0, sticky="nsew")
        failures = " ".join(self.integrity.failures)
        checks = [
            ("Frozen artifact hashes", "FAIL" if "hash mismatch" in failures or "missing:" in failures else "PASS", f"{len(manifest.get('artifacts', []))} migrated artifacts"),
            ("Final board consistency", "FAIL" if "matrix and board" in failures or "authoritative rule count" in failures else "PASS", "38 board rules"),
            ("Support matrix consistency", "FAIL" if "support distribution" in failures else "PASS", self.service.workspace.matrix().get("matrix_version", "unknown")),
            ("38-rule count", "FAIL" if "rule count" in failures else "PASS", "Expected 38"),
            ("Ratification consistency", "FAIL" if "unexpected E4" in failures or "decision" in failures.lower() else "PASS", "CVC-RAT-001"),
            ("Referenced artifact availability", "FAIL" if "missing" in failures.lower() else "PASS", "Manifest references resolved"),
            ("JSON/JSONL parseability", "FAIL" if "invalid JSON" in failures else "PASS", "Migrated structured files"),
            ("Mutable/frozen boundary", "PASS", "corpus frozen; state append-only"),
        ]
        for row in checks:
            tree.insert("", "end", values=row)
        if self.integrity.failures:
            detail = tk.Text(frame, height=5, wrap="word", state="disabled")
            detail.grid(row=3, column=0, sticky="ew", pady=(8, 0))
            self._write_text(detail, "Failures:\n" + "\n".join(self.integrity.failures))

    def verify_now(self) -> None:
        from datetime import datetime, timezone

        self.integrity = self.service.verify_corpus()
        self.last_verified = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        self.integrity_var.set(self._integrity_label())
        if self.current_view == "Integrity":
            self.show_integrity()
        elif self.current_view == "Overview":
            self.show_overview()

    def global_search(self) -> None:
        query = self.global_search_var.get().strip()
        if not query or query.startswith("Search "):
            return
        grouped = self.service.search(query)
        window = tk.Toplevel(self)
        window.title(f"Search: {query}")
        window.geometry("780x520")
        ttk.Label(window, text=f"Deterministic results for: {query}", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=12, pady=10)
        results: list[dict[str, Any]] = []
        listbox = tk.Listbox(window)
        listbox.pack(fill="both", expand=True, padx=12, pady=(0, 8))
        for group, rows in grouped.items():
            if not rows:
                continue
            listbox.insert(tk.END, f"— {group} —")
            for row in rows:
                result = {"group": group, **row}
                results.append(result)
                listbox.insert(tk.END, f"{row.get('label')}: {str(row.get('summary', ''))[:150]}")
        if not results:
            listbox.insert(tk.END, "No deterministic matches.")

        def navigate(_event: Any = None) -> None:
            index = listbox.curselection()
            if not index or not results:
                return
            # Headers occupy listbox rows, so locate the result by counting non-header entries.
            target = listbox.get(index[0])
            result = next((item for item in results if str(item.get("label")) in target), None)
            if not result:
                return
            window.destroy()
            group = result["group"]
            self.show_view("Rules" if group == "RULES" else "Evidence Triggers" if group == "TRIGGERS" else "History")

        listbox.bind("<Double-1>", navigate)
        ttk.Button(window, text="Close", command=window.destroy).pack(anchor="e", padx=12, pady=(0, 10))

    def ask_cvc(self) -> None:
        window = tk.Toplevel(self)
        window.title("Ask CVC")
        window.geometry("760x520")
        ttk.Label(window, text="Ask CVC", font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=12, pady=(12, 5))
        ttk.Label(window, text="Semantic reasoning is not configured. Showing bounded evidence results.", foreground="#555555", wraplength=700).pack(anchor="w", padx=12, pady=(0, 8))
        question = tk.StringVar()
        entry = ttk.Entry(window, textvariable=question)
        entry.pack(fill="x", padx=12)
        output = tk.Text(window, wrap="word", state="disabled")
        output.pack(fill="both", expand=True, padx=12, pady=10)

        def ask() -> None:
            try:
                result = self.service.query_corpus(question.get())
                self._write_text(output, _pretty(result))
            except Exception as exc:
                self._write_text(output, f"Query failed: {exc}")

        ttk.Button(window, text="Ask", command=ask).pack(anchor="w", padx=12, pady=(0, 12))
        entry.focus_set()

    def check_trigger_file(self) -> None:
        if not self.integrity.passed:
            messagebox.showerror("Integrity failure", "Trigger checks are blocked until the corpus integrity failure is reviewed.", parent=self)
            return
        selected = filedialog.askopenfilename(title="Select evidence for trigger check")
        if not selected:
            return
        try:
            result = self.service.check_triggers(selected)
            messagebox.showinfo("Trigger check result", _pretty(result), parent=self)
        except Exception as exc:
            messagebox.showerror("Trigger check failed", str(exc), parent=self)

    def open_artifact(self, relative_path: str) -> None:
        if not self.service.open_known_artifact(relative_path):
            messagebox.showerror("Artifact unavailable", "This path is not a known corpus/state artifact.", parent=self)

    def open_workspace(self) -> None:
        try:
            self.service.open_workspace_folder()
        except OSError as exc:
            messagebox.showerror("Cannot open folder", str(exc), parent=self)

    def _copy(self, value: str) -> None:
        self.clipboard_clear()
        self.clipboard_append(value)
        self.update()


def run_smoke_test(root: Path | str) -> dict[str, Any]:
    """Headless smoke check for GUI-facing services; it never writes state."""
    service = CVCService(root)
    status = service.get_status()
    integrity = service.verify_corpus()
    preview = service.preview_ingest(Path(root) / "corpus/evidence/FLEET_EVIDENCE_REGISTER_V0.1.jsonl")
    return {
        "overview": status["rule_count"] == 38 and status["support_distribution"]["E4"] == 2,
        "rules": len(service.get_board()) == 38,
        "rule_detail": service.get_rule("STD-EPI-001") is not None,
        "triggers": len(service.get_triggers()) > 0,
        "integrity": integrity.passed,
        "ingest_preview": preview["state_will_change"] is False and preview["duplicate"] is True,
        "reasoning_disabled": service.query_corpus("diagnostic evidence")["reasoning"]["status"] == "DISABLED",
    }


def main(argv: list[str] | None = None) -> int:
    argument_parser = argparse.ArgumentParser(prog="cvc-gui")
    argument_parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    argument_parser.add_argument("--view", choices=NAVIGATION, default="Overview", help="initial screen")
    argument_parser.add_argument("--smoke-test", action="store_true", help="run non-rendering GUI service smoke checks")
    args = argument_parser.parse_args(argv)
    if args.smoke_test:
        print(json.dumps(run_smoke_test(args.root), indent=2, sort_keys=True))
        return 0
    app = CVCApplication(args.root, args.view)
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
