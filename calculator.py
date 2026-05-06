import tkinter as tk
from tkinter import ttk


class CalculatorEngine:
    """Core calculator logic, independent from GUI, to allow unit testing."""
    def __init__(self):
        self.clear()

    def clear(self):
        self.current_value = None  # Accumulated value (float)
        self.pending_operator = None  # '+', '-', '*', '/'
        self.current_input = ""  # Digits of the operand being typed
        self.error = False
        self.error_message = ""

    # ----- Input methods -----
    def press_digit(self, d: str):
        if self.error:
            return
        if d not in "0123456789":
            return
        # Allow leading zeros; harmless
        self.current_input += d

    def press_dot(self):
        if self.error:
            return
        if "." in self.current_input:
            return  # prevent multiple dots in the same number
        if self.current_input == "":
            self.current_input = "0."
        else:
            self.current_input += "."

    def press_operator(self, op: str):
        if self.error:
            return
        if op not in "+-*/":
            return
        if self.current_input != "":
            # We have a freshly typed operand to fold into the accumulator
            try:
                operand = float(self.current_input)
            except ValueError:
                self._set_error("Fehler: Ungültige Eingabe")
                return
            if self.current_value is None:
                self.current_value = operand
            else:
                if not self._apply_operator(self.pending_operator, operand):
                    return  # error set
            self.current_input = ""
            self.pending_operator = op
        else:
            # No new operand; allow changing the pending operator
            if self.current_value is None:
                # If no value at all, treat as 0 <op>
                self.current_value = 0.0
            self.pending_operator = op

    def press_equals(self):
        if self.error:
            return
        # If we have just a number without operator
        if self.pending_operator is None and self.current_input != "":
            try:
                self.current_value = float(self.current_input)
            except ValueError:
                self._set_error("Fehler: Ungültige Eingabe")
                return
            self.current_input = ""
            return
        # If we have an operator and a new operand
        if self.pending_operator is not None and self.current_input != "":
            try:
                operand = float(self.current_input)
            except ValueError:
                self._set_error("Fehler: Ungültige Eingabe")
                return
            if not self._apply_operator(self.pending_operator, operand):
                return  # error set
            self.pending_operator = None
            self.current_input = ""
        # Else: nothing to do (keep current_value on display)

    def press_clear(self):
        self.clear()

    # ----- Helpers -----
    def _apply_operator(self, op: str, operand: float) -> bool:
        if op is None:
            # No-op; set value to operand
            self.current_value = float(operand)
            return True
        if self.current_value is None:
            self.current_value = float(operand)
            return True
        try:
            if op == '+':
                self.current_value = self.current_value + operand
            elif op == '-':
                self.current_value = self.current_value - operand
            elif op == '*':
                self.current_value = self.current_value * operand
            elif op == '/':
                if operand == 0:
                    self._set_error("Fehler: Division durch 0")
                    return False
                self.current_value = self.current_value / operand
            else:
                self._set_error("Fehler: Ungültiger Operator")
                return False
            return True
        except Exception:
            self._set_error("Fehler: Berechnung fehlgeschlagen")
            return False

    def _set_error(self, message: str):
        self.error = True
        self.error_message = message
        self.current_input = ""
        self.pending_operator = None
        # keep current_value as-is; only C resets

    def _format_number(self, value: float) -> str:
        # Pretty formatting: avoid long floating artifacts and trailing zeros
        if value == 0:
            return "0"
        s = format(value, ".12g")  # up to 12 significant digits
        # Remove trailing . if present (shouldn't occur with g, but safe)
        if s.endswith('.'):
            s = s[:-1]
        return s

    # ----- Display -----
    def get_display(self) -> str:
        if self.error:
            return self.error_message
        if self.current_input != "":
            return self.current_input
        if self.current_value is None:
            return "0"
        return self._format_number(self.current_value)


class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Einfacher Taschenrechner")
        self.resizable(False, False)
        self.engine = CalculatorEngine()

        self.display_var = tk.StringVar(value=self.engine.get_display())

        self._build_ui()
        self._update_display()

    def _build_ui(self):
        main = ttk.Frame(self, padding=10)
        main.grid(row=0, column=0, sticky="nsew")

        # Display (read-only Entry)
        self.display = ttk.Entry(main, textvariable=self.display_var, justify="right", state="readonly", width=24)
        self.display.grid(row=0, column=0, columnspan=4, pady=(0, 8))

        # Button layout
        # Rows:
        # 7 8 9 /
        # 4 5 6 *
        # 1 2 3 -
        # C 0 . +
        # = (spans all columns)
        buttons = [
            ("7", 1, 0, self._mk_digit_cb('7')),
            ("8", 1, 1, self._mk_digit_cb('8')),
            ("9", 1, 2, self._mk_digit_cb('9')),
            ("/", 1, 3, lambda: self._on_operator('/')),

            ("4", 2, 0, self._mk_digit_cb('4')),
            ("5", 2, 1, self._mk_digit_cb('5')),
            ("6", 2, 2, self._mk_digit_cb('6')),
            ("*", 2, 3, lambda: self._on_operator('*')),

            ("1", 3, 0, self._mk_digit_cb('1')),
            ("2", 3, 1, self._mk_digit_cb('2')),
            ("3", 3, 2, self._mk_digit_cb('3')),
            ("-", 3, 3, lambda: self._on_operator('-')),

            ("C", 4, 0, self._on_clear),
            ("0", 4, 1, self._mk_digit_cb('0')),
            (".", 4, 2, self._on_dot),
            ("+", 4, 3, lambda: self._on_operator('+')),
        ]

        for text, r, c, cmd in buttons:
            btn = ttk.Button(main, text=text, command=cmd, width=5)
            btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")

        eq_btn = ttk.Button(main, text="=", command=self._on_equals)
        eq_btn.grid(row=5, column=0, columnspan=4, sticky="nsew", pady=(6, 0))

        # Configure grid weights minimally
        for r in range(1, 6):
            main.rowconfigure(r, weight=1)
        for c in range(4):
            main.columnconfigure(c, weight=1)

    def _mk_digit_cb(self, d: str):
        return lambda: self._on_digit(d)

    def _on_digit(self, d: str):
        if self.engine.error:
            # Ignore input until cleared, per requirements resetting after error via C
            return
        self.engine.press_digit(d)
        self._update_display()

    def _on_dot(self):
        if self.engine.error:
            return
        self.engine.press_dot()
        self._update_display()

    def _on_operator(self, op: str):
        if self.engine.error:
            return
        self.engine.press_operator(op)
        self._update_display()

    def _on_equals(self):
        if self.engine.error:
            return
        self.engine.press_equals()
        self._update_display()

    def _on_clear(self):
        self.engine.press_clear()
        self._update_display()

    def _update_display(self):
        self.display_var.set(self.engine.get_display())


if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
