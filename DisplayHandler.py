import board
from digitalio import DigitalInOut
from adafruit_character_lcd.character_lcd import Character_LCD_Mono


class DisplayHandler:
    lcd_columns = 16
    lcd_rows = 2

    lcd_rs = DigitalInOut(board.D26)
    lcd_en = DigitalInOut(board.D12)
    lcd_d4 = DigitalInOut(board.D13)
    lcd_d5 = DigitalInOut(board.D6)
    lcd_d6 = DigitalInOut(board.D5)
    lcd_d7 = DigitalInOut(board.D11)

    lcd = None

    def __init__(self):
        self.lcd = Character_LCD_Mono(
            self.lcd_rs,
            self.lcd_en,
            self.lcd_d4,
            self.lcd_d5,
            self.lcd_d6,
            self.lcd_d7,
            self.lcd_columns,
            self.lcd_rows
        )

        self.lcd.message = "Pixel\nAI Companion"

    def set_message(self, message):
        # clear the LCD
        self.lcd.message = "                \n                "
        # set the new message
        self.lcd.message = message
