
class Servomotor:
    """

    NAME = str(self.ui.textEdit_6.toPlainText())
    dan = int(self.ui.textEdit.toPlainText())  # Kolichestvo shagov
    dan_2 = int(self.ui.textEdit_2.toPlainText())  # Napravlenie
    N = int(self.ui.textEdit_11.toPlainText())  # Rezim
    skor_ = float(self.ui.textEdit_12.toPlainText())  # Скорость(кол-во шагов в минуту)

    Exp_ = float(self.ui.textEdit_5.toPlainText())  # ZADAEM ExporsureTime
    k = dan

    pauza_ = 60.0 / skor_

    x = 1  # NOMER FOTO
    j = 1  # schetchik foto
    i = 0  # schetchik shagov

    pin_3_YEL = 3  # STEP
    pin_14_BLUE = 14  # STRAHOVKA (ENA)
    pin_4_GREY = 4  # NAPRAVLENIE (DIR)
    pin_17_MS1 = 17  # №6 после земли ближе к процу
    pin_18_MS2 = 18  # REJIM oborota    №6 на 1 дальше чем предыдущи
    GPIO.setmode(GPIO.BCM)  # ZADALI NOMERATIY PINOV

    GPIO.setup(pin_3_YEL, GPIO.OUT, initial=1)  # step
    GPIO.setup(pin_14_BLUE, GPIO.OUT, initial=1)  # strahowka (ENA)
    GPIO.setup(pin_4_GREY, GPIO.OUT, initial=1)  # napravlenie step (DIR)
    GPIO.setup(pin_17_MS1, GPIO.OUT, initial=0)
    GPIO.setup(pin_18_MS2, GPIO.OUT, initial=0)

    if N == 1:
        GPIO.output(pin_17_MS1, 0)
        GPIO.output(pin_18_MS2, 0)
    elif N == 2:
        GPIO.output(pin_17_MS1, 1)
        GPIO.output(pin_18_MS2, 0)
    elif N == 4:
        GPIO.output(pin_17_MS1, 0)
        GPIO.output(pin_18_MS2, 1)
    else:
        GPIO.output(pin_17_MS1, 1)
        GPIO.output(pin_18_MS2, 1)

    GPIO.output(pin_4_GREY, dan_2)  # zadaem rejim raboti pinov  dan_2
    GPIO.output(pin_14_BLUE, 0)  #
    """

    def __init__(self, mode: str):
        self.mode = mode
    def next_step(self):
        pass
