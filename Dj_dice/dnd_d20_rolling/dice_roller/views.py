from django.shortcuts import render
from .models import roll
from random import randint


# Create your views here.

def attack_def(request):
    if request.method == "GET":

        return render(request, 'dice_roll_dir/attack.html')


    elif request.method == "POST":

        att, dmg, amount, dice_type, pro, mod, advantage, critic = hit_dice_roll(request.POST["amount"],

                                                                                 request.POST["dice_type"],

                                                                                 request.POST["pro"],

                                                                                 request.POST["mod"],

                                                                                 request.POST["advantage"],

                                                                                 request.POST["critic"])

        flag = True

        if att == "Wprowadzona wartość jest nieprawidłowa, zmień ustawienia losowania":
            flag = False

        if flag == True:
            data_base_update = roll.objects.create(d_amount=amount,

                                                   d_type=dice_type,

                                                   attack_bonus=pro,

                                                   dmg_bonus=mod,

                                                   advatage_bonus=advantage,

                                                   critic_bonus=critic,

                                                   attack_result=att,

                                                   dmg_result=dmg)

        return render(request, 'dice_roll_dir/attack.html', {"att": str(att), "dmg": str(dmg), "flag": flag})


def skill_dice_roller(mod, advantage):
    """

    mod : modyfikator do rzutu uwzględniający biegłość otraz modyfikator z cech.return. Wartość domyslna to 0

    advantage : uwzglednia: ułatwienie - True, utrudnienie - Falce, lub normalny rzut - None. Wartość domyslna to None

    return : Program zwraca wartość wylosowaną miezy 1 a 20 oraz dodaje modyfikator (mod). W przypdaku advantage = True, losowanie nastepuje dwa razy i wybierana jest wyższa liczba, w przypdaku advantage = False rowniez liczbę losuje sie dwa razy ale wybierana jest niższa.

    """

    if advantage == True:

        roll = [randint(1, 20) for x in range(1, 3)]

        roll.sort()

        value = roll[1]

    elif advantage == None:

        value = randint(1, 20)

    elif advantage == False:

        roll = [randint(1, 20) for x in range(1, 3)]

        roll.sort()

        value = roll[0]

    elif advantage not in (None, True, False):

        raise ValueError("Funcja: skill_dice_roller, niewłaściwa wartość dla zmiennej advantage")

    return value + mod


def hit_dice_roll(amount, dice_type, pro, mod, advantage, critic):
    """

    amount : iloma kosćmi rzuca osoba

    dice_type : jaki typ kości zostaje rzucony, Dostepne wersje to k2, k3, k4, k6, k8, k10, k12, k20, k100

    pro : modyfikator do trafienia przekazywany do funcki skill_dice_roller(), gdy funkcja ta zwróci wartość równą 20 + pro następuje zmiana critic na True, gdy wartość to 1 + pro funkcja zwraca warosć 0 oraz wyswietla informację o porażce

    mod : modyfikator dodawany do obrazeń końcowych

    advantage : czy rzucający ma przewagę? True - tak, None - nie, False - posiada utrudnienie. Wartość zwracana jest do funkcji skill_dice_roller

    critic : Jeżeli wartość = True podwajana jest ilosć koścmi jakimi się rzuca.

    return : zwraca informację o wskażniku trafienia oraz wartości obrazeń. Dodatkowo wyświetla wprowadzone parametry oraz wynik programu.

    """

    amount, dice_type, pro, mod, advantage, critic = check(amount, dice_type, pro, mod, advantage, critic)

    if (type(amount) != int) | (type(dice_type) != int) | (type(pro) != int) | (type(mod) != int):

        print("Kości oraz parametry muszą być liczbami naturalnymi.")

        return bad_value_error()



    elif (amount) <= 0:

        print("Ilość kośći nie może być zerowa lub ujemna,")

        return bad_value_error()



    elif dice_type not in (2, 3, 4, 6, 8, 10, 12, 20, 100):

        print("Takiej kości nie ma")

        return bad_value_error()



    elif advantage not in (None, True, False):

        print("Brak obsługi takiej wartości advantage")

        return bad_value_error()



    elif critic not in (True, False):

        print("Brak obsługi takiej wartości critic")

        return bad_value_error()

    hit = skill_dice_roller(mod=pro, advantage=advantage)

    if (hit - pro) == 20:

        critic = True



    elif (hit - pro) == 1:

        print("TOTALNA PORAŻKA")

        return "Krytyczna porażka", str(0)

    print(
        "Wprowadzono: Ilość kości:{}, typ kości: k{}, modyfikator do trafienia: {}, modyfikator do obrazeń:{}, advantage: {}, trafienie krytyczne: {}".format(
            amount, dice_type, pro, mod, advantage, critic))

    sum_of_dmg = 0

    if critic == True:
        amount = amount * 2

    for i in range(1, amount + 1):
        sum_of_dmg += randint(1, dice_type)

    print("Trafnienie: {}, dmg:{}".format(hit, sum_of_dmg))

    return hit, sum_of_dmg, amount, dice_type, pro, mod, advantage, critic


def check(amount, dice_type, pro, mod, advantage, critic):
    """

    Próba konwersji warotści input (string) na właściwe. Inaczej zwróc zmienną jako napis error.

    :return: skonwertowane zmienne

    """

    if advantage == "True":

        advantage = True

    elif advantage == "None":

        advantage = None

    elif advantage == "False":

        advantage = False

    else:

        advantage = "Error"

    if critic in ("True", "False"):

        if critic == "True":

            critic = True

        else:

            critic = False

    try:

        amount = int(amount)

    except:

        amount = "Error"

    try:

        dice_type = int(dice_type)

    except:

        dice_type = "Error"

    try:

        pro = int(pro)

    except:

        pro = "Error"

    try:

        mod = int(mod)

    except:

        mod = "Error"

    return amount, dice_type, pro, mod, advantage, critic


def bad_value_error():
    return "Wprowadzona wartość jest nieprawidłowa, zmień ustawienia losowania", 0, 0, 0, 0, 0, 0, 0
