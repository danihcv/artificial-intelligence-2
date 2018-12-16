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


def value_of_state(sequences):
    total = 0

    for i in range(len(sequences)):
        for j in range(i + 1, len(sequences)):
            total = value_of_pair(sequences[i], sequences[j])

    return total
