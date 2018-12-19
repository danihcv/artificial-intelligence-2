import sys

alfa = int(input())
beta = int(input())
gama = int(input())


def value_of_pair(seq1, seq2):
    x = y = z = 0

    for i in range(len(seq1)):
        if seq1[i] == '-' and seq2 == '-':  # ambos sao gaps
            continue
        elif seq1[i] == seq2[i]:    # acidos nucleios iguais
            x += 1
        elif seq1[i] == '-' or seq2[i] == '-':  # um dos elementos eh gap
            z += 1
        else:   # acidos nucleicos diferentes
            y += 1

    return alfa * x + beta * y + gama * z


def value_of_state(DNAs):
    total = 0

    for i in range(len(DNAs)):
        for j in range(i + 1, len(DNAs)):
            total = value_of_pair(DNAs[i].sequence, DNAs[j].sequence)

    return total


def generate_turns(i, a, total=[]):
    if i == 0:
        total += [a]
        return
    for j in range(2):
        generate_turns(i - 1, a + [j], total)

    return total


def standardize_sequences(sequences_list, to_size):
    for i in range(len(sequences_list)):
        sequences_list[i] = sequences_list[i] + ('-' * (to_size - len(sequences_list[i])))


dna_list = []
standard_size = 0
while True:
    try:
        seq = input()
        dna_list += [seq]

        if len(seq) > standard_size:
            standard_size = len(seq)
    except:
        break

turns = generate_turns(len(dna_list), [])
pos = 0
best_score = -sys.maxsize
while True:
    if pos >= standard_size:
        break

    print('- dna_list:', dna_list)
    print('- standard_size:', standard_size)
    print('- current position:', str(pos) + '/' + str(standard_size - 1))

    for turn in turns:
        dna_list_copy = dna_list.copy()
        local_standard_size = standard_size
        print('turn:', turn)
        for seq, insert_gap in enumerate(turn):
            print('\tseq:', seq, ', insert_gap:', insert_gap)

            if insert_gap == 1 and pos < len(dna_list_copy[seq]):
                dna_list_copy[seq] = dna_list_copy[seq][:pos] + '-' + dna_list_copy[seq][pos:]

                if len(dna_list_copy[seq] > local_standard_size):
                    local_standard_size = len(dna_list_copy[seq])

        print(dna_list_copy)  # evaluation point
    print()

    pos += 1

