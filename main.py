from random import randint, choice
from os import system
from time import sleep


class Person:
    """
    Класс - прародитель для двух основных классов программы:
    Игрока и Опонента - компьютера.
    В этом классе прописанны все методы, которые должны быть
    переназначены классами-потомкамиЮ а также базовые методы
    для функционирования игры.
    """
    max_HP = 100
    opponent = None
    attack_heal_range = [18, 25]
    top_attack_range = [10, 35]
    actions = [
        "удар сбоку - стандартненький удар, который наносит 18-25 урона",
        "удар сверху - дерзкий удар подушкой сверху в голову. 10-35 урона",
        "сьесть подорожник - восстановит тебе 18-25 HP"
    ]

    def __init__(self, name="Someone", hp=100):
        self.name = name
        self.hp = hp

    def do_move(self):
        """
        Метод должен быть переопределен!
        Означает совершение хода у одного из персонажей игры:
        компьютера и игрока
        """
        raise Exception("Не определен метод у наследника класса Person")

    def hp_change(self, hp):
        """
        Метод для изменения показателей здоровья персонажей,
        и оповещения игрока об этом.
        :param hp: Колличество здоровья, на которое должен измениться показатель персонажа
        Если значение положительное, происходит лечение
        Если отрицательное - нанесение урона персонажу.

        В конце метод вызывает метод check_hp для проверки здоровья персонажа.
        :return: None
        """
        if hp > 0:
            self.hp += hp
            print(f"{self.name} восстановил {hp} HP! Теперь у него {self.hp} HP!")
        else:
            self.hp += hp
            print(f"{self.name} потерял {-hp} HP!!!\nТеперь у него {self.hp} HP!")
        self.check_hp()

    def check_hp(self):
        """
        Метод должен быть переопределен
        Метод, проверяющий текущее здоровье персонажа.
        В случае опускания шкаклы здоровья ниже 0
        появляется соответствующее сообщение с результатом
        подушечной битвы.
        В случае поднятия выше 100 - здоровье опускается до 100.
        Соответственно, оповещается и пользователь.
        Суть переопределения в том, что в каждом из подклассов
        должны быть свои оповещения, и свой исход битвы.
        """
        raise Exception("Не определен метод check_hp у наследника класса Person")

    def side_kick(self):
        """
        Метод означает удар сбоку.
        Определяется случайный урон из диапазона, и эта
        величина передается в метод hp_change с отрицательным
        значением (собственно обозначая снятие здоровья)
        """
        damage = randint(*self.attack_heal_range)
        print(f"{self.name} наносит удар сбоку!")
        self.opponent.hp_change(-damage)

    def top_kick(self):
        """
        Метод означает удар подушкой сверху.
        Определяется случайный урон из более широкого диапазона, и
        эта величина передается в метод hp_change с отрицательным
        значением (собственно обозначая снятие здоровья).
        Здесь также варьируются оповещения в зависимости от
        величины урона (выбранной случайным образом)
        """
        damage = randint(*self.attack_heal_range)
        if damage > 28:
            print(f"{self.name} наносит НЕВЕРОЯТНЫЙ удар сверху в голову! Рандом аж подпрыгнул!")
        elif damage > 18:
            print(f"{self.name} наносит норм такой удар сверху!")
        else:
            print(f"{self.name} наносит жалкие {damage} урона:\nПротивник успел сбегать в магазин, купить и надеть каску")
        self.opponent.hp_change(-damage)  # Вызывается метод для снятия здоровья у персонажа - опонента


class Player(Person):
    """
    Класс игрока. Наследуется от класса Person, и переопределяет внутри
    некоторые из его методов, так же имея и свои.
    Это особенности совершения хода игроком, проверка здоровья..
    """
    def do_move(self):
        """
        Метод означает совершение игроком хода.
        Соответственно, игрок сначала выбирает действие (реализовано с
        помощью функции choose_variant, описанной при определении)
        Затем в зависимости от варианта, выбраного игроком, вызывается
        соответствующий метод (из суперкласса в том числе)
        :return: None
        """
        answer = choose_variant([self, opponent], f"Выбери действие, {self.name}:", self.actions)
        if answer == "1":
            self.side_kick()
        elif answer == "2":
            self.top_kick()
        elif answer == "3":
            self.eat()

    def check_hp(self):
        """
        Метод, проверяющий текущее здоровье персонажа.
        В случае опускания шкаклы здоровья ниже 0
        появляется соответствующее сообщение с результатом
        подушечной битвы.
        В случае поднятия выше 100 - здоровье опускается до 100.
        Соответственно, оповещается и пользователь.
        :return: None
        """
        if self.hp > self.max_HP:
            self.hp = self.max_HP
            print(f"А кто это у нас тут слишком здоровый? У {self.name} снова {self.max_HP} HP")
        elif self.hp <= 0:
            print(f"Ах как жаль! {self.name} не смог получить подушку. Но ты не расстраивайся, еще встретимся:)")
            input()
            exit(0)

    def eat(self):
        """
        Метод обозначающий процесс сьедания подорожника персонажем.
        Это дает эффект лечения.
        Выбирается слуайное число из соответствующего промежутка с
        помощью функции choice модуля time. Затем происходит оповещение
        игрока и значение передается в метод hp_change с положительным
        значением. Соотрветственно в том методе происходит увеличение
        здоровья персонажа
        :return:
        """
        recovery = randint(*self.attack_heal_range)
        print(f"{self.name} спокойно отошел, сорвал подорожник, и запихнул его себе в рот...")
        self.hp_change(recovery)


class Opponent(Person):
    """
    Класс, описывающий опонента игрока: компьютер.
    Методы переопределены по своему, ориентируясь на компьютер.
    """
    def do_move(self):
        """
         Метод означает совершение компьютером хода.
         Соответственно, сначала случайно выбирается действие (реализовано с
         помощью функции choice модуля random)
         Затем в зависимости от варианта, выбраного рандомом, вызывается
         соответствующий метод (из суперкласса в том числе), совершающий
         соответствующее действие
         :return: None
         """
        answer = choice([str(i + 1) for i in range(len(self.actions))])
        if answer == "1":
            self.side_kick()
        elif answer == "2":
            self.top_kick()
        elif answer == "3":
            self.eat()

    def check_hp(self):
        """
        Метод, проверяющий текущее здоровье персонажа.
        В случае опускания шкаклы здоровья ниже 0
        появляется соответствующее сообщение с результатом
        подушечной битвы: игрок победил и может отобрать подшку.
        В случае поднятия выше 100 - здоровье опускается до 100.
        Соответственно, оповещается и пользователь.
        :return: None
        """
        if self.hp > self.max_HP:
            self.hp = self.max_HP
            print(f"Не, вышло как-то слишком ЗДОРОВО :D\n У {self.name} снова {self.max_HP} HP")
        elif self.hp <= 0:
            print(f"УИИИИИ! {opponent.name} завоевал подушку:) Теперь ты сможешь спать!\nМои поздравления!)")
            input()
            exit(0)

    def eat(self):
        """
        Метод обозначающий процесс сьедания подорожника персонажем.
        Это дает эффект лечения.
        Выбирается слуайное число из соответствующего промежутка с
        помощью функции choice модуля time. Затем происходит оповещение
        игрока и значение передается в метод hp_change с положительным
        значением. Соотрветственно в том методе происходит увеличение
        здоровья персонажа.

        Поскольку за этого персонажа играет компьютер, он получает увеличение
        шанса вылечиться на большее значение здоровья, чем обычно.
        Происходит проверка здоровья : if self.hp > 35,
        и в соответствии с этим включается усиленное лечение, или нет.
        Усиление лечение заключено в следующем:
        max(randint(*self.attack_heal_range), randint(*self.attack_heal_range)) + 2
        Тоесть, берется максимальное число из двух выпавших случайно чисел в том же
        диапазоне, и к исходному результату прибавляется 2.
        :return: None
        """
        if self.hp > 35:
            recovery = randint(*self.attack_heal_range)
            print(f"{self.name} спокойно отошел, сорвал подорожник, и запихнул его себе в рот...")
        else:
            # Когда низкое здоровье у компьютера, шанс его хорошего излечения увеличивается:
            recovery = max(randint(*self.attack_heal_range), randint(*self.attack_heal_range)) + 2
            print(f"{self.name} отбежал, сорвал подорожник, и запихнул его себе в рот, усиленно жуя...")
        self.hp_change(recovery)


def choose_variant(players, text, variants):
    """
    Функция для реализации получения корректного ответа пользователя
    в случае предоставления ему списка вариантов для выбора.
    Он должен выбрать число, соответствующее желаемому варианту.
    Соответсятвенно, в случае неправильного ввода пользователь получает
    уведомление об этом и ему предоставляется возможность ввести
    значение еще раз.
    И так до тех пор, пока он не введет допустимый ответ.
    Тогда будет совершен return из функции. Вернется ответ пользователя.

    :param players: Список персонажей. Нужен для нового выведения таблички со
    здоровьем каждого игрока в случае неправильного ввода. Это необходимо в
    последствии использования команды system('cls').
    :param text: Текст, который видит пользователь при вводе. Приглашение ввести что-то.
    :param variants: Список вариантов, которые может выбрать пользователь
    :return: Ответ пользователя в типе данных str.
    """
    variants_length = len(variants)
    correct_answers = [str(i + 1) for i in range(variants_length)]
    while True:
        print(f"{'-' * 6}|{text}")
        i = 1
        for variant in variants:
            print(f"{i} - {variant}")
            i += 1
        answer = input(":")
        if answer in correct_answers:
            return answer
        else:
            input("Неверный ответ(. <Enter>")
            print_parameters(players)


def print_parameters(players):
    """
    Функция для очистки и обновления экрана и вывода таблички с текущими
    показателями игроков.
    Очистка экрана происходит с передачи команды 'cls' в функцию
    system из модуля os.
    :param players: Список персонажей, игрок и компьютер
    :return: None      (Нужна только для декорации)
    """
    system('cls')
    print("_" * 26)
    for parameter in ["name", "hp"]:  # Берем каждый параметр, и для него строим строку таблицы
        print("|%4s" % parameter + "| ", end="")
        for person in players:
            print("%10s" % person.__dict__[parameter], end="|")  # достаем значение атрибута персонажа из словаря
        print()                                                        # __dict__
    print("_"*26)


def choosing(players):
    """
    Функция для случайного выбора и
    красивого отображения выбранного Рандомом игрока, чей сейчас ход.
    С помощью функции sleep модуля time реализована задержка на долю секунды,
    пока в цикле выводятся точки для создания атмосферности, эфекта процесса
    выбора, чтобы вовлечь игрока.
    Выбор производится с помощью функции choice модуля time.
    Соответственно далее форматируется строка для красивого вывода имени
    выбранного персонажа.

    :param players: Список персонажей: компьютер и игрок. Из него происходит выбор.
    :return: Обьект персонажа, которого выбрал Рандом
    """
    action_person = choice(players)
    print(f"Рандом выбрал игрока с необычным именем:")
    for i in range(5):
        sleep(0.1)
        print(".")
    print(f"- - - - - -<|     {action_person.name}     |>- - - - - -\n\n")
    sleep(0.4)
    return action_person


# Для того, чтоб при импортировании функций и классов этого файла не выполнялся код ниже
if __name__ == "__main__":
    opponent_name = choice(["Алекс", "Арахис", "Кукурузий", "Боб"])
    print(f"""Привет, путник! Я {opponent_name} Анука иди сюда, сразимся на подушках!
Давай-давай, иди сюда :)

<жми Enter>""")
    input()
    system('cls')
    name = input("Так, для начала, как тебя звать то?\n")
    system('cls')
    # Правила игры
    print(f"""Так и запишем, {name}.
Ну что ж, держи подушку, теперь она твоя. Победишь меня -
и сможшь забрать ее себе. А проиграешь - ...
Ну так и будет)

Смотри, правила просты до нельзя) У каждого из нас
изначально есть, скажем, по 100 HP (Hit Points).
Цель каждого из нас - опустить шкалу HP противника
до 0, и можно сделать это разными способами.
В начале каждого хода Рандом решает,
чей из нас двоих сейчас ход. Рандом - это вон тот слон на 
бугорке, видишь, вон стоит? Супер!

Далее тот, кого выбрал Рандом, может 
совершить оно из 3 действий:
- удар сбоку - стандартненький удар, который наносит 18-25 урона.
От него трудно защититься, однако слишком сильно так не навредишь.
Ты можешь попробовать что-нибудь поопасней:
- удар сверху - дерзкий удар подушкой сверху в голову. Если противник
не успеет укрыться, его ожидает перьевой шок - он получит до 35 урона.
Однако такие удары проходят реже, и часто противник успевает надеть
защитную каску на голову, пока ты пытаешься размахнуться.
Поэтому нижний предел урона для такой атаки - всего 10 урона.
Рискнешь? )
- сьесть подорожник. Наверняка он имеет целебные свойства, и
восстановит тебе 18-25 HP, ну или хотя-бы поднимет боевой дух.
Тоже неплохо) Жуй только медленно
Собственно говоря, выбрав вариант, ты совершаешь выбранное действие,
а дальше начинается новый раунд, где Рандом заново выберет действующее
лицо.
Рандом, готов? Умничка ты моя!
Приготовь подушку) И жми <Enter>
""")
    input()
    system('cls')

    hp = 100
    # Создаем обьект Игрока и Компьютера:
    player = Player(name, hp)
    opponent = Opponent(opponent_name, hp)
    # Помещаем ссылку на игрока/компьютера в поле "Опонент" компьютера/игрока для удобства использования методов:
    player.opponent, opponent.opponent = opponent, player
    # Создание списка персонажей и помещение туда ссылки на персонажа игрока и компьютера:
    players = [player, opponent]
    while True:
        print_parameters(players)  # Очищаем экран, выводим декорации
        action_person = choosing(players)  # Выбираем персонажа, чей ход сейчас
        action_person.do_move()  # Совершение хода выбранным игроком
        input("\n\n<Enter>")  # Задержка для прочтения результатов перед обновлением экрана.
