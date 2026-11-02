# SIMULATOR PENJADWALAN CPU
# Data: (nama, waktu kedatangan, burst time, prioritas)

proses = [
    ("P1", 0, 4, 2),
    ("P2", 1, 8, 4),
    ("P3", 2, 2, 1),
    ("P4", 4, 6, 3),
    ("P5", 6, 3, 2)
]

def tampilkan_data():
    print("\nDATA PROSES")
    print("-" * 45)
    print(f"{'Proses':<10}{'Arrival':<10}{'Burst':<10}{'Prioritas':<10}")

    for nama, datang, burst, prioritas in proses:
        print(f"{nama:<10}{datang:<10}{burst:<10}{prioritas:<10}")

def fcfs():
    print("\nALGORITMA FCFS")
    waktu = 0
    total_tunggu = 0
    total_turnaround = 0
    total_respons = 0

    for nama, datang, burst, prioritas in sorted(proses, key=lambda p: p[1]):
        if waktu < datang:
            waktu = datang

        mulai = waktu
        selesai = mulai + burst
        tunggu = mulai - datang
        turnaround = selesai - datang
        respons = mulai - datang

        total_tunggu += tunggu
        total_turnaround += turnaround
        total_respons += respons

        print(f"{nama}: {mulai} - {selesai} | "
              f"WT={tunggu}, TAT={turnaround}, RT={respons}")

        waktu = selesai

    jumlah = len(proses)
    print(f"\nRata-rata Waiting Time: {total_tunggu / jumlah:.2f}")
    print(f"Rata-rata Turnaround Time: {total_turnaround / jumlah:.2f}")
    print(f"Rata-rata Response Time: {total_respons / jumlah:.2f}")

def sjf():
    print("\nALGORITMA SJF")

    waktu = 0
    selesai = []
    total_tunggu = 0
    total_turnaround = 0
    total_respons = 0

    while len(selesai) < len(proses):
        tersedia = [
            p for p in proses
            if p[1] <= waktu and p[0] not in selesai
        ]

        if not tersedia:
            waktu += 1
            continue

        p = min(tersedia, key=lambda x: x[2])
        nama, datang, burst, prioritas = p

        mulai = waktu
        akhir = mulai + burst

        tunggu = mulai - datang
        turnaround = akhir - datang
        respons = mulai - datang

        print(
            f"{nama}: {mulai} - {akhir} | "
            f"WT={tunggu}, TAT={turnaround}, RT={respons}"
        )

        total_tunggu += tunggu
        total_turnaround += turnaround
        total_respons += respons

        waktu = akhir
        selesai.append(nama)

    jumlah = len(proses)
    print(f"Rata-rata Waiting Time: {total_tunggu / jumlah:.2f}")
    print(f"Rata-rata Turnaround Time: {total_turnaround / jumlah:.2f}")
    print(f"Rata-rata Response Time: {total_respons / jumlah:.2f}")

def priority_scheduling():
    print("\nALGORITMA PRIORITY")

    waktu = 0
    selesai = []
    total_tunggu = 0
    total_turnaround = 0
    total_respons = 0

    while len(selesai) < len(proses):
        tersedia = [
            p for p in proses
            if p[1] <= waktu and p[0] not in selesai
        ]

        if not tersedia:
            waktu += 1
            continue

        p = min(tersedia, key=lambda x: x[3])
        nama, datang, burst, prioritas = p

        mulai = waktu
        akhir = mulai + burst

        tunggu = mulai - datang
        turnaround = akhir - datang
        respons = mulai - datang

        print(
            f"{nama}: {mulai} - {akhir} | "
            f"WT={tunggu}, TAT={turnaround}, RT={respons}"
        )

        total_tunggu += tunggu
        total_turnaround += turnaround
        total_respons += respons

        waktu = akhir
        selesai.append(nama)

    jumlah = len(proses)
    print(f"Rata-rata Waiting Time: {total_tunggu / jumlah:.2f}")
    print(f"Rata-rata Turnaround Time: {total_turnaround / jumlah:.2f}")
    print(f"Rata-rata Response Time: {total_respons / jumlah:.2f}")

def round_robin(quantum):
    print(f"\nALGORITMA ROUND ROBIN (Quantum = {quantum})")

    antrian = []
    sisa = {p[0]: p[2] for p in proses}
    pertama = {}
    selesai = {}
    waktu = 0
    indeks = 0
    urutan = sorted(proses, key=lambda p: p[1])
    gantt = []

    while len(selesai) < len(proses):
        while indeks < len(urutan) and urutan[indeks][1] <= waktu:
            antrian.append(urutan[indeks])
            indeks += 1

        if not antrian:
            waktu = urutan[indeks][1]
            continue

        p = antrian.pop(0)
        nama, datang, burst, prioritas = p

        if nama not in pertama:
            pertama[nama] = waktu

        jalan = min(quantum, sisa[nama])
        mulai = waktu
        waktu += jalan
        sisa[nama] -= jalan

        gantt.append((nama, mulai, waktu))

        while indeks < len(urutan) and urutan[indeks][1] <= waktu:
            antrian.append(urutan[indeks])
            indeks += 1

        if sisa[nama] > 0:
            antrian.append(p)
        else:
            selesai[nama] = waktu

    print("\nGantt Chart:")
    print(" -> ".join(
        f"{nama}({mulai}-{akhir})"
        for nama, mulai, akhir in gantt
    ))

    total_wt = 0
    total_tat = 0
    total_rt = 0

    print("\nHasil setiap proses:")

    for nama, datang, burst, prioritas in proses:
        tat = selesai[nama] - datang
        wt = tat - burst
        rt = pertama[nama] - datang

        total_wt += wt
        total_tat += tat
        total_rt += rt

        print(
            f"{nama}: WT={wt}, TAT={tat}, RT={rt}"
        )

    jumlah = len(proses)

    print(f"Rata-rata Waiting Time: {total_wt / jumlah:.2f}")
    print(f"Rata-rata Turnaround Time: {total_tat / jumlah:.2f}")
    print(f"Rata-rata Response Time: {total_rt / jumlah:.2f}")

def menu():
    while True:
        print("\n=== SIMULATOR PENJADWALAN CPU ===")
        print("1. Tampilkan data proses")
        print("2. Jalankan FCFS")
        print("3. Jalankan SJF")
        print("4. Jalankan Priority Scheduling")
        print("5. Round Robin Quantum 3")
        print("6. Round Robin Quantum 5")
        print("0. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tampilkan_data()
        elif pilihan == "2":
            fcfs()
        elif pilihan == "3":
            sjf()
        elif pilihan == "4":
            priority_scheduling()
        elif pilihan == "5":
            round_robin(3)
        elif pilihan == "6":
            round_robin(5)
        elif pilihan == "0":
            print("Program selesai.")
            break
        else:
            print("Pilihan tidak valid.")

menu()