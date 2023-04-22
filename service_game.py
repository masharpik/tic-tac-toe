import random


def find_best_move(matrix, computer):
    # Проверяем все возможные ходы
    best_score = -float('inf')
    best_moves = []
    for i in range(3):
        for j in range(3):
            if matrix[i][j] == '.':
                # Выполняем ход в текущую пустую клетку
                matrix[i][j] = computer
                # Проверяем, если это выигрышный ход, то сразу возвращаем его
                if check_win(matrix, computer):
                    matrix[i][j] = computer
                    return matrix, i * 3 + j + 1
                # Оцениваем этот ход
                score = check_win(matrix, computer)
                # Если этот ход лучше предыдущих, сохраняем его
                if score > best_score:
                    best_score = score
                    best_moves = [(i, j)]
                elif score == best_score:
                    best_moves.append((i, j))
                # Отменяем ход
                matrix[i][j] = '.'
    # Проверяем, если следующим ходом игрок может выиграть, чтобы помешать ему
    for move in best_moves:
        matrix[move[0]][move[1]] = 'o' if computer == 'x' else 'x'
        if check_win(matrix, 'o' if computer == 'x' else 'x'):
            matrix[move[0]][move[1]] = computer
            return matrix, move[0] * 3 + move[1] + 1
        matrix[move[0]][move[1]] = '.'
    # Выполняем лучший ход
    best_move = random.choice(best_moves)
    matrix[best_move[0]][best_move[1]] = computer
    return matrix, best_move[0] * 3 + best_move[1] + 1


# Функция для проверки наличия выигрышной комбинации
def check_win(matrix, player):
    # Проверяем все возможные выигрышные комбинации
    for i in range(3):
        if matrix[i][0] == matrix[i][1] == matrix[i][2] == player:
            return True
        if matrix[0][i] == matrix[1][i] == matrix[2][i] == player:
            return True
    if matrix[0][0] == matrix[1][1] == matrix[2][2] == player:
        return True
    if matrix[0][2] == matrix[1][1] == matrix[2][0] == player:
        return True
    return False
