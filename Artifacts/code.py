import pandas as pd
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import random
import scipy.stats as stats
import pylab
import struct
import time


%matplotlib inline

n_exp = 10000

n_exp = 500
n_discs = 5000
n_substats = 4

TOTAL_COUNT = 1_000_000
BATCH_SIZE = 10_000
#random.seed(a=2, version=2)

stats_map = {
    "None": -1,
    "HP%": 0,
    "HP": 1, 
    "ATK%": 2,
    "ATK": 3,
    "DEF%": 4,
    "DEF": 5,
    "EM": 6, # Elemental mastery
    "ER": 7, # Energy recharge
    "CRIT_RATE": 8, # Crit Rate
    "CRIT_DMG": 9, # Crit Damage
    "Physical Bonus": 10,
    "Fire Bonus": 11,
    "Hydro Bonus": 12,
    "Anemo Bonus": 13,
    "Electro Bonus": 14,
    "Dendro Bonus": 15,
    "Cryo Bonus": 16,
    "Geo Bonus": 17,
    "Heal Bonus": 18,
}

main_stat_values_map = {
    stats_map["HP%"]: 4660,
    stats_map["HP"]: 478000, 
    stats_map["ATK%"]: 4660,
    stats_map["ATK"]: 3110,
    stats_map["DEF%"]: 5830,
    stats_map["EM"]: 18700,
    stats_map["ER"]: 5180,
    stats_map["CRIT_RATE"]: 3110,
    stats_map["CRIT_DMG"]: 6220,
    stats_map["Fire Bonus"]: 4660, # same for all elements
    stats_map["Physical Bonus"]: 5830,
    stats_map["Heal Bonus"]: 3590
}


base_sub_stats_choices = [
    stats_map["HP%"],
    stats_map["HP"], 
    stats_map["ATK%"],
    stats_map["ATK"],
    stats_map["DEF%"],
    stats_map["DEF"],
    stats_map["EM"],
    stats_map["ER"],
    stats_map["CRIT_RATE"],
    stats_map["CRIT_DMG"]
]

# 100%, 90%, 80%, 70%
sub_stats_values_map = {
    stats_map["HP%"]: [408, 466, 525, 583],
    stats_map["HP"]: [20913, 23900, 26988, 29975], 
    stats_map["ATK%"]: [408, 466, 525, 583],
    stats_map["ATK"]: [1362, 1556, 1751, 1945],
    stats_map["DEF%"]: [510, 583, 656, 729],
    stats_map["DEF"]: [1620, 1852, 2083, 2315],
    stats_map["EM"]: [1632, 1865, 2098, 2331],
    stats_map["ER"]: [453, 518, 583, 648],
    stats_map["CRIT_RATE"]: [272, 311, 350, 389],
    stats_map["CRIT_DMG"]: [544, 622, 699, 777]
}

sub_stats_values_count = 4

sub_stats_weights_map = {
    stats_map["HP%"]: 4,
    stats_map["HP"]: 6,
    stats_map["ATK%"]: 4,
    stats_map["ATK"]: 6,
    stats_map["DEF%"]: 4,
    stats_map["DEF"]: 6,
    stats_map["EM"]: 4,
    stats_map["ER"]: 4,
    stats_map["CRIT_RATE"]: 3,
    stats_map["CRIT_DMG"]: 3
}

slot_1_pop = [stats_map["HP"]]
slot_1_prob = [1]

slot_2_pop = [stats_map["ATK"]]
slot_2_prob = [1]

slot_3_pop = [
    stats_map["HP%"],
    stats_map["ATK%"],
    stats_map["DEF%"],
    stats_map["ER"],
    stats_map["EM"]
]
slot_3_prob = [0.8/3, 0.8/3, 0.8/3, 0.1, 0.1]

slot_4_pop = [
    stats_map["HP%"],
    stats_map["ATK%"],
    stats_map["DEF%"],
    stats_map["Physical Bonus"],
    stats_map["Fire Bonus"],
    stats_map["Hydro Bonus"],
    stats_map["Anemo Bonus"],
    stats_map["Electro Bonus"],
    stats_map["Dendro Bonus"],
    stats_map["Cryo Bonus"],
    stats_map["Geo Bonus"],
    stats_map["EM"]
]
slot_4_prob = [0.1925, 0.1925, 0.19, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.025]

slot_5_pop = [
    stats_map["HP%"],
    stats_map["ATK%"],
    stats_map["DEF%"],
    stats_map["CRIT_RATE"],
    stats_map["CRIT_DMG"],
    stats_map["EM"],
    stats_map["Heal Bonus"]
]
slot_5_prob = [0.22, 0.22, 0.22, 0.1, 0.1, 0.04, 0.1]

def weighted_sample_no_replacement(population, weights):
    population = population.copy()
    weights = weights.copy()
    result = []
    for _ in range(n_substats):
        choice = random.choices(population, weights=weights, k=1)[0]
        idx = population.index(choice)
        result.append(choice)
        # убираем выбранный элемент
        population.pop(idx)
        weights.pop(idx)
    return result

def generate_art_for_file(population, weights, count_roll):
    artifact = [0] * 10
    stat_0_level_sample = weighted_sample_no_replacement(population, weights) # 4 sub stat in artifact
    stat_upgrade_choice = random.choices(stat_0_level_sample, k = count_roll) # rolls doring upgrade
    
    for stat in stat_0_level_sample:
        index = random.randint(0, sub_stats_values_count - 1)
        artifact[stat] += sub_stats_values_map[stat][index]
        
    for stat in stat_upgrade_choice:
        index = random.randint(0, sub_stats_values_count - 1)
        artifact[stat] += sub_stats_values_map[stat][index]
    
    return artifact


def generate_file(deleted_stat_name):
    deleted_stat = stats_map[deleted_stat_name]
    possible_sub_stats = base_sub_stats_choices.copy()
    if deleted_stat in possible_sub_stats:
        possible_sub_stats.remove(deleted_stat)
    sub_stat_weights = [sub_stats_weights_map[value] for value in possible_sub_stats]
    with open(f"GI_artifacts/artifacts_{deleted_stat_name}.bin", "wb") as file:

        count_3_base_stat_arts = TOTAL_COUNT * 4 // 5

        for start in range(0, count_3_base_stat_arts, BATCH_SIZE):
            artifacts = []
            for _ in range(BATCH_SIZE):
                artifacts.append(generate_art_for_file(possible_sub_stats, sub_stat_weights, 4))

            # Запись batch в файл
            data = bytearray()
            for artifact in artifacts:
                data.extend(struct.pack("<10i", *artifact))
            file.write(data)
            
            generated = start + BATCH_SIZE
            percent = generated / TOTAL_COUNT * 100

            print(
                f"\rGenerated: {generated:,} / {TOTAL_COUNT:,} "
                f"({percent:.2f}%)",
                end="",
                flush=True
            )
            
        for start in range(count_3_base_stat_arts, TOTAL_COUNT, BATCH_SIZE):
            artifacts = []
            for _ in range(BATCH_SIZE):
                artifacts.append(generate_art_for_file(possible_sub_stats, sub_stat_weights, 5))

            # Запись batch в файл
            data = bytearray()
            for artifact in artifacts:
                data.extend(struct.pack("<10i", *artifact))
            file.write(data)
            
            generated = start + BATCH_SIZE
            percent = generated / TOTAL_COUNT * 100

            print(
                f"\rGenerated: {generated:,} / {TOTAL_COUNT:,} "
                f"({percent:.2f}%)",
                end="",
                flush=True
            )

    print("\nGeneration completed.")

start_time = time.time()

generate_file("HP%")
generate_file("HP")
generate_file("ATK%")
generate_file("ATK")
generate_file("DEF%")
generate_file("EM")
generate_file("ER")
generate_file("CRIT_RATE")
generate_file("CRIT_DMG")
generate_file("None")

end_time = time.time()
print(f"--- {end_time - start_time} seconds of all disks ---")