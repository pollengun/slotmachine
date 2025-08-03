import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QMessageBox, QTextEdit, QSpinBox
)
from PyQt5.QtCore import Qt

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1
ROWS = 3
COLS = 3

symbol_count = {"A": 2, "B": 4, "C": 6, "D": 8}
symbol_value = {"A": 5, "B": 4, "C": 3, "D": 2}


class SlotMachineApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Slot Machine Game")
        self.setFixedSize(400, 500)

        # Game state
        self.balance = 0

        # UI Elements
        self.deposit_input = QLineEdit()
        self.deposit_button = QPushButton("Deposit")
        self.line_selector = QSpinBox()
        self.bet_input = QLineEdit()
        self.spin_button = QPushButton("Spin")
        self.slot_output = QTextEdit()
        self.result_label = QLabel()
        self.balance_label = QLabel("Balance: $0")

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Deposit section
        self.deposit_input.setPlaceholderText("Enter deposit amount")
        self.deposit_input.setFixedWidth(200)
        self.deposit_button.clicked.connect(self.deposit_money)

        deposit_layout = QHBoxLayout()
        deposit_layout.addWidget(self.deposit_input)
        deposit_layout.addWidget(self.deposit_button)

        # Bet setup
        self.line_selector.setRange(1, MAX_LINES)
        self.bet_input.setPlaceholderText(f"Bet per line (${MIN_BET}-{MAX_BET})")
        self.bet_input.setFixedWidth(200)

        bet_layout = QHBoxLayout()
        bet_layout.addWidget(QLabel("Lines:"))
        bet_layout.addWidget(self.line_selector)
        bet_layout.addWidget(QLabel("Bet:"))
        bet_layout.addWidget(self.bet_input)

        # Slot and Spin
        self.slot_output.setReadOnly(True)
        self.slot_output.setFixedHeight(100)
        self.spin_button.clicked.connect(self.spin)

        # Layout
        layout.addLayout(deposit_layout)
        layout.addWidget(self.balance_label)
        layout.addLayout(bet_layout)
        layout.addWidget(self.spin_button)
        layout.addWidget(QLabel("Slot Machine Result:"))
        layout.addWidget(self.slot_output)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def deposit_money(self):
        amount_str = self.deposit_input.text()
        if amount_str.isdigit():
            amount = int(amount_str)
            if amount > 0:
                self.balance += amount
                self.update_balance()
                self.deposit_input.clear()
            else:
                self.show_error("Deposit must be greater than 0.")
        else:
            self.show_error("Please enter a valid number.")

    def update_balance(self):
        self.balance_label.setText(f"Balance: ${self.balance}")

    def get_slot_machine_spin(self):
        all_symbols = []
        for symbol, count in symbol_count.items():
            all_symbols += [symbol] * count

        columns = []
        for _ in range(COLS):
            current_symbols = all_symbols[:]
            column = []
            for _ in range(ROWS):
                value = random.choice(current_symbols)
                current_symbols.remove(value)
                column.append(value)
            columns.append(column)
        return columns

    def print_slot_machine(self, columns):
        output = ""
        for row in range(ROWS):
            row_symbols = [columns[col][row] for col in range(COLS)]
            output += " | ".join(row_symbols) + "\n"
        return output.strip()

    def check_winnings(self, columns, lines, bet):
        winnings = 0
        winning_lines = []
        for line in range(lines):
            symbol = columns[0][line]
            for column in columns:
                if column[line] != symbol:
                    break
            else:
                winnings += symbol_value[symbol] * bet
                winning_lines.append(line + 1)
        return winnings, winning_lines

    def spin(self):
        bet_str = self.bet_input.text()
        if not bet_str.isdigit():
            self.show_error("Please enter a valid bet amount.")
            return

        bet = int(bet_str)
        if not (MIN_BET <= bet <= MAX_BET):
            self.show_error(f"Bet must be between ${MIN_BET} and ${MAX_BET}.")
            return

        lines = self.line_selector.value()
        total_bet = bet * lines

        if total_bet > self.balance:
            self.show_error(f"Not enough balance! You have ${self.balance}.")
            return

        # Proceed with game
        self.balance -= total_bet
        slots = self.get_slot_machine_spin()
        output = self.print_slot_machine(slots)
        self.slot_output.setText(output)

        winnings, win_lines = self.check_winnings(slots, lines, bet)
        self.balance += winnings
        self.update_balance()

        result = f"You won ${winnings}."
        if win_lines:
            result += f" Winning lines: {', '.join(map(str, win_lines))}"
        else:
            result += " No winning lines."

        self.result_label.setText(result)

    def show_error(self, message):
        QMessageBox.warning(self, "Error", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SlotMachineApp()
    window.show()
    sys.exit(app.exec_())
