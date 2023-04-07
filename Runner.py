from bakterie import Bakterie
import numpy as np  # Nødvendig pakke
import matplotlib.pyplot as plt  # Nødvendig pakkee
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
from tqdm import trange
import sys
sys.stdout = open('output.txt','wt')

print("Starting simulation")

# konstanter
b = 0.001                       # Bakterie reproduksjonsfaktor
max_alder = 10                  # Hvor lenge bakterier lever
mutasjons_sannsynlighet = 1e-2  # sannsynlighet for a reproduksjon muterer gener
simulerings_lengde = 10         # antall bakterieår simuleringen skal kjøre

# miljø for bakterier
x_celler = 100
y_celler = 100
bakterier = []


# flytting av bakterien
def flytte_funksjon(x_celler, y_celler):
    def flytt(bakterie):
        dx = np.random.choice([-1, 1])
        dy = np.random.choice([-1, 1])

        ny_x_verdi = bakterie.x + dx
        if ny_x_verdi > 0 and ny_x_verdi < x_celler - 1:
            bakterie.x = ny_x_verdi

        ny_y_verdi = bakterie.y + dy
        if ny_y_verdi > 0 and ny_y_verdi < y_celler - 1:
            bakterie.y = ny_y_verdi

        return bakterie

    return flytt


# Reproduksjon av bakterier
def sannsynlighetsfunksjon(b):
    def p(n):
        sannsynlighet = 2 * (1 - 1 / (1 + np.exp(-b * n)))
        return sannsynlighet

    return p


def reproduksjon(mammabakterie):

    antallbakterier = len(bakterier)

    p = sannsynlighetsfunksjon(b)
    sannsynlighet = p(antallbakterier)
    r = np.random.uniform(low=0, high=1)
    if r < sannsynlighet:
        return True
    else:
        return False


def skal_mutere():
    r = np.random.uniform(low=0, high=1)
    if mutasjons_sannsynlighet > r:
        return True
    # Lag en bakterie med som har mutert arvestoffet og derfor får økt antibiotikaresistans her
    else:
        return False

# Spawning av bakterier
def nybakterie(ny_x, ny_y):

    bakterie = Bakterie(
        x_celler=x_celler,
        y_celler=y_celler,
        x=ny_x,
        y=ny_y,  # np.random.randint(y_celler/4),
        resistans=None)
    bakterie.alder = 0

    return bakterie


def antibiotika_konsentrasjon(x):
    if 0 <= x < 0.2 * x_celler:
        return 0.0
    elif 0.2 * x_celler <= x < 0.4 * x_celler:
        return 0.2
    elif 0.4 * x_celler <= x < 0.6 * x_celler:
        return 0.6
    elif 0.6 * x_celler <= x < 0.8 * x_celler:
        return 0.8
    elif x >= 0.8 * x_celler:
        return 0.99


def leve_antibiotika(bakterie):
    antibiotikastyrke = antibiotika_konsentrasjon(bakterie.x)
    resistans = bakterie.resistans
    r = np.random.uniform(low=0, high=1)
    if (antibiotikastyrke - resistans) < r:
        return True
    else:
        return False


flytt = flytte_funksjon(x_celler, y_celler)

# lag 5 bakterier
bakterier.append(nybakterie(1, 1))
bakterier.append(nybakterie(1, int(0.25 * y_celler)))
bakterier.append(nybakterie(1, int(0.5 * y_celler)))
bakterier.append(nybakterie(1, int(0.75 * y_celler)))
bakterier.append(nybakterie(1, y_celler - 1))

# sett opp tegning
fig, ax = plt.subplots()
imgs = []

# simulering og visualisering
for n in trange(simulerings_lengde):
    img = np.zeros(shape=(x_celler, y_celler))

    nyfodtebakterier = []
    for bakterie in bakterier:

        # simulering
        if reproduksjon(bakterie):
            nyfodtbakterie = nybakterie(bakterie.x, bakterie.y)

            if skal_mutere():
                if bakterie.resistans < 1.0:
                    nyfodtbakterie.resistans = bakterie.resistans + 0.1
                else:
                    nyfodtbakterie.resistans = bakterie.resistans

                print(str(n) + ":ny bakterie med mutasjon er født, x:" + str(nyfodtbakterie.x) + " y:" + str(nyfodtbakterie.y) + " resistans: " + str(nyfodtbakterie.resistans))
            else:
                nyfodtbakterie.resistans = bakterie.resistans
                print(str(n) + ":ny bakterie er født, x:" + str(nyfodtbakterie.x) + " y:" + str(nyfodtbakterie.y) + " resistans: " + str(nyfodtbakterie.resistans))

            nyfodtebakterier.append(nyfodtbakterie)

        flytt(bakterie)
        bakterie.alder += 1

    bakterier.extend(nyfodtebakterier)

    for bakterie in bakterier:
        if bakterie.alder >= max_alder:
            print("Bakterie dør av alderdom og alder:" + str(bakterie.alder) + " x:" + str(bakterie.x) + " y:" + str(bakterie.y))
            bakterier.remove(bakterie)
        elif leve_antibiotika(bakterie) is False:
            print("Bakterie dør av antibiotika, resistans:" + str(bakterie.resistans) + " x:" + str(bakterie.x) + " y:" + str(
                bakterie.y))
            bakterier.remove(bakterie)

    # visualisering
    for bakterie in bakterier:
        img[bakterie.x, bakterie.y] = 1

    imgs.append([ax.imshow(img.T, animated=True)])

ani = animation.ArtistAnimation(fig, imgs, interval=1000, blit=True)

writer = PillowWriter(fps=2)
print("Skriver banana.gif")
ani.save("banana.gif", writer=writer)
plt.close()