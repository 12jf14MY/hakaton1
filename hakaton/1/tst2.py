def test(file):
    kol = 0

    with open(file, 'r', encoding='utf-8') as f:
        vopr_f = f.readlines()

    vsego = int(len(vopr_f) / 2)

    vopr = []
    st = 1
    for i in vopr_f:
        if st == 1:
            newi = i.replace("\n", "");
            q = []
            q.append(newi)
            st = 2
        else:
            newi = i.replace("\n", "");
            q.append(newi)
            vopr.append(q)
            st = 1

    for i in vopr:
        otv = input(i[0])
        if otv.upper() == i[1].upper():
            truly = "Верно"
            kol = kol + 1
        else:
            wrong = (f"Не верно, Верный ответ {i[1]}")

    finish = (kol, " верных ответов из ", vsego)