from multiprocessing import Process, Pipe


def send_money(pipe, id, time, money):
    time += 1
    sub_money(id, time, money)
    print('Банк ' + str(id) + ' отправил ' + str(money) + '$', end='\n')
    pipe.send((money, time))

    return time


def sub_money(id, time, money):
    i = time
    if id ==1:
        while mas_money1[i - 1] == 0:
            i -= 1
        mas_money1[time] = mas_money1[i - 1] - money
    elif id == 2:
        while mas_money2[i - 1] == 0:
            i -= 1
        mas_money2[time] = mas_money2[i - 1] - money
    elif id == 3:
        while mas_money3[i - 1] == 0:
            i -= 1
        mas_money3[time] = mas_money3[i - 1] - money


def receive_money(pipe, id, time):
    money, timestamp = pipe.recv()
    time = maxTime(timestamp, time)
    sum_money(id, time, money)
    print('Банк ' + str(id) + ' получил ' + str(money) + '$', end='\n')

    return time


def maxTime(receive_time, time):
    return max(receive_time, time) + 1


def sum_money(id, time, money):
    i = time
    if id == 1:
        while mas_money1[i - 1] == 0:
            i -= 1
        mas_money1[time] = money + mas_money1[i - 1]
    elif id == 2:
        while mas_money2[i - 1] == 0:
            i -= 1
        mas_money2[time] = money + mas_money2[i - 1]
    elif id == 3:
        while mas_money3[i - 1] == 0:
            i -= 1
        mas_money3[time] = money + mas_money3[i - 1]


def process1(pipe12, pipe13):
    id = 1
    time = 0
    mas_money1[time] = 10

    time = send_money(pipe12, id, time, 1)
    time = send_money(pipe12, id, time, 3)
    time = receive_money(pipe13, id, time)
    time = send_money(pipe12, id, time, 7)

    print("--------------------------------Суммы первого банка " + str(mas_money1), end='\n')
    print_sum(mas_money1, id)


def process2(pipe21, pipe23):
    id = 2
    time = 0
    mas_money2[time] = 20
    time = receive_money(pipe21, id, time)
    time = send_money(pipe23, id, time, 2)
    time = receive_money(pipe21, id, time)
    time = send_money(pipe23, id, time, 5)
    time = receive_money(pipe21, id, time)

    print()
    print("--------------------------------Суммы второго банка " + str(mas_money2), end='\n')

    print_sum(mas_money2, id)


def process3(pipe32, pipe31 ):
    id = 3
    time = 0
    mas_money3[time] = 30
    time = receive_money(pipe32, id, time)
    time = send_money(pipe31, id, time, 4)
    time = receive_money(pipe32, id, time)
    print()
    print("--------------------------------Суммы третьего банка " + str(mas_money3), end='\n')
    print_sum(mas_money3, id)


def print_sum(mas, id):
    i = check_time
    while mas[i] == 0:
        i -= 1
    print()
    print('--------------------------------На этапе времени ' + str(check_time) +
          ' банк №' + str(id) + ' имеет на счете сумму ' + str(mas[i]), end='\n')


mas_money1 = [0] * 10
mas_money2 = [0] * 10
mas_money3 = [0] * 10
check_time = 5

if __name__ == '__main__':

    print("Выполнен пример из пособия: выполнение банковской системы, использующей скалярные часы. Рис. 3.2.")
    print("Посчитаем общую сумму денег в момент времени t = 5")

    one_two, two_one = Pipe()
    one_three, three_one = Pipe()
    two_three, three_two = Pipe()

    bank1 = Process(target=process1, args=(one_two, three_one))
    bank2 = Process(target=process2, args=(two_one, two_three))
    bank3 = Process(target=process3, args=(three_two, one_three))

    bank1.start()
    bank2.start()
    bank3.start()

    bank1.join()
    bank2.join()
    bank3.join()
