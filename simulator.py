# SIMULATOR PENJADWALAN CPU
# Data: (nama, waktu kedatangan, burst time, prioritas)
# Angka prioritas lebih kecil berarti prioritas lebih tinggi.

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


def tampilkan_hasil(nama_algoritma, gantt, pertama, selesai):
    print(f"\nGANTT CHART - {nama_algoritma}")
    if gantt:
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
        print(f"{nama}: WT={wt}, TAT={tat}, RT={rt}")

    jumlah = len(proses)
    print(f"Rata-rata Waiting Time: {total_wt / jumlah:.2f}")
    print(f"Rata-rata Turnaround Time: {total_tat / jumlah:.2f}")
    print(f"Rata-rata Response Time: {total_rt / jumlah:.2f}")


def fcfs():
    print("\nALGORITMA FCFS")
    waktu = 0
    gantt = []
    pertama = {}
    selesai = {}

    for nama, datang, burst, prioritas in sorted(proses, key=lambda p: p[1]):
        if waktu < datang:
            waktu = datang
        mulai = waktu
        akhir = mulai + burst
        pertama[nama] = mulai
        selesai[nama] = akhir
        gantt.append((nama, mulai, akhir))
        waktu = akhir

    tampilkan_hasil("FCFS", gantt, pertama, selesai)


def sjf():
    print("\nALGORITMA SJF (Non-Preemptive)")
    waktu = 0
    belum_selesai = proses.copy()
    gantt = []
    pertama = {}
    selesai = {}

    while belum_selesai:
        tersedia = [p for p in belum_selesai if p[1] <= waktu]
        if not tersedia:
            waktu = min(p[1] for p in belum_selesai)
            tersedia = [p for p in belum_selesai if p[1] <= waktu]

        p = min(tersedia, key=lambda x: (x[2], x[1]))
        nama, datang, burst, prioritas = p
        mulai = waktu
        akhir = mulai + burst
        pertama[nama] = mulai
        selesai[nama] = akhir
        gantt.append((nama, mulai, akhir))
        waktu = akhir
        belum_selesai.remove(p)

    tampilkan_hasil("SJF", gantt, pertama, selesai)


def srtf():
    print("\nALGORITMA SRTF (Preemptive)")
    sisa = {p[0]: p[2] for p in proses}
    pertama = {}
    selesai = {}
    gantt = []
    waktu = 0
    jumlah_selesai = 0
    proses_berjalan = None

    while jumlah_selesai < len(proses):
        tersedia = [p for p in proses if p[1] <= waktu and sisa[p[0]] > 0]
        if not tersedia:
            waktu += 1
            proses_berjalan = None
            continue

        p = min(tersedia, key=lambda x: (sisa[x[0]], x[1]))
        nama = p[0]

        if nama not in pertama:
            pertama[nama] = waktu

        if proses_berjalan == nama and gantt:
            gantt[-1] = (nama, gantt[-1][1], waktu + 1)
        else:
            gantt.append((nama, waktu, waktu + 1))

        proses_berjalan = nama
        sisa[nama] -= 1
        waktu += 1

        if sisa[nama] == 0:
            selesai[nama] = waktu
            jumlah_selesai += 1

    tampilkan_hasil("SRTF", gantt, pertama, selesai)


def priority_scheduling():
    print("\nALGORITMA PRIORITY (Non-Preemptive)")
    waktu = 0
    belum_selesai = proses.copy()
    gantt = []
    pertama = {}
    selesai = {}

    while belum_selesai:
        tersedia = [p for p in belum_selesai if p[1] <= waktu]
        if not tersedia:
            waktu = min(p[1] for p in belum_selesai)
            tersedia = [p for p in belum_selesai if p[1] <= waktu]

        p = min(tersedia, key=lambda x: (x[3], x[1]))
        nama, datang, burst, prioritas = p
        mulai = waktu
        akhir = mulai + burst
        pertama[nama] = mulai
        selesai[nama] = akhir
        gantt.append((nama, mulai, akhir))
        waktu = akhir
        belum_selesai.remove(p)

    tampilkan_hasil("Priority", gantt, pertama, selesai)


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

    tampilkan_hasil(f"Round Robin Q={quantum}", gantt, pertama, selesai)


def menu():
    while True:
        print("\n=== SIMULATOR PENJADWALAN CPU ===")
        print("1. Tampilkan data proses")
        print("2. Jalankan FCFS")
        print("3. Jalankan SJF")
        print("4. Jalankan SRTF")
        print("5. Jalankan Priority Scheduling")
        print("6. Round Robin Quantum 3")
        print("7. Round Robin Quantum 5")
        print("0. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tampilkan_data()
        elif pilihan == "2":
            fcfs()
        elif pilihan == "3":
            sjf()
        elif pilihan == "4":
            srtf()
        elif pilihan == "5":
            priority_scheduling()
        elif pilihan == "6":
            round_robin(3)
        elif pilihan == "7":
            round_robin(5)
        elif pilihan == "0":
            print("Program selesai.")
            break
        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    menu()
