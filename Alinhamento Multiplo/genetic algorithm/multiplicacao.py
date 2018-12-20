import math
import sys
from random import randrange


def value_of_pair(seq1, seq2, up_to):
    x = y = z = 0

    for i in range(up_to + 1):
        if seq1[i] == '-' and seq2[i] == '-':  # ambos sao gaps
            continue
        elif seq1[i] == seq2[i]:  # acidos nucleios iguais
            x += 1
        elif seq1[i] == '-' or seq2[i] == '-':  # um dos elementos eh gap
            z += 1
        else:  # acidos nucleicos diferentes
            y += 1
    print('x:', x, ', y:', y, ', z:', z, ', res:', alfa * x + beta * y + gama * z)
    return alfa * x + beta * y + gama * z


def value_of_state(DNAs, up_to, biggest_size):
    DNAs = standardize_sequences(DNAs, biggest_size)
    total = 0

    for i in range(len(DNAs)):
        for j in range(i + 1, len(DNAs)):
            total += value_of_pair(DNAs[i], DNAs[j], up_to)

    return total


def generate_turns(i, a, total=[]):
    if i == 0:
        total += [a]
        return
    for j in range(2):
        generate_turns(i - 1, a + [j], total)

    return total


def standardize_sequences(sequences_list, to_size):
    sequences_list = sequences_list.copy()

    for i in range(len(sequences_list)):
        sequences_list[i] = sequences_list[i] + ('-' * (to_size - len(sequences_list[i])))

    return sequences_list


dna_list = []
standard_size = 0
floor_size = sys.maxsize
while True:
    try:
        seq = input()
        dna_list += [seq]

        if len(seq) > standard_size:
            standard_size = len(seq)
        if len(seq) < floor_size:
            floor_size = len(seq)
    except:
        break

alfa = standard_size * 10
beta = 0
gama = -1
score = -sys.maxsize
turns = generate_turns(len(dna_list), [])
# pos = randrange(0, floor_size)
pos = 0
steps_without_improvement = 0
while True:
    # if steps_without_improvement == standard_size:
    #     break
    if pos >= standard_size:
        break

    print('- dna_list:', dna_list)
    print('- score: ', score)
    print('- standard_size:', standard_size)
    print('- floor_size:', floor_size)
    print('- current position:', str(pos) + '/' + str(standard_size - 1))

    best_score = -sys.maxsize
    best_list = None
    best_standard_size = standard_size
    best_floor_size = floor_size
    for turn in turns:
        print('turn:', turn)

        local_dna_list = dna_list.copy()
        local_standard_size = best_standard_size
        local_floor_size = best_floor_size
        for seq, insert_gap in enumerate(turn):
            # print('\tseq:', seq, ', insert_gap:', insert_gap)

            if insert_gap == 1 and pos < len(local_dna_list[seq]):
                local_dna_list[seq] = local_dna_list[seq][:pos] + '-' + local_dna_list[seq][pos:]

                if len(local_dna_list[seq]) > local_standard_size:
                    local_standard_size = len(local_dna_list[seq])
                if len(local_dna_list[seq]) < local_floor_size:
                    local_floor_size = len(local_dna_list[seq])

        score_up_to = value_of_state(local_dna_list, pos, local_standard_size)
        score_total = value_of_state(local_dna_list, local_standard_size - 1, local_standard_size)
        local_score = score_up_to * score_total if score_up_to > 0 and score_total > 0 \
            else -math.fabs(score_up_to * score_total)
        print(local_score, local_dna_list)  # evaluation point
        if local_score > best_score:
            best_score = local_score
            best_list = local_dna_list

            if local_standard_size > best_standard_size:
                best_standard_size = local_standard_size
            if local_floor_size < best_floor_size:
                best_floor_size = local_floor_size

    if best_score is not None and best_score > score:
        score = best_score
        dna_list = best_list
        standard_size = best_standard_size
        steps_without_improvement = 0
    else:
        steps_without_improvement += 1

    print()

    # pos = randrange(0, floor_size)
    pos += 1

print('>' * 15, 'SOLUTION:', score, standardize_sequences(dna_list, standard_size))
