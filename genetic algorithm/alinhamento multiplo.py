alfa = int(input())
beta = int(input())
gama = int(input())


class DNA:
    def __init__(self, sequence):
        self.current_gap = -1
        self.sequence = sequence


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


dna_list = []
biggest_sequence = 0
while True:
    try:
        seq = input()
        dna_list += [DNA(seq)]

        if len(seq) > biggest_sequence:
            biggest_sequence = len(seq)
    except:
        break

print(dna_list)

