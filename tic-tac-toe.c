#include<stdio.h>
#include<stdlib.h>
#include<ctype.h>
#include<time.h>

char board[3][3];
const char player1 = 'X';
const char player2 = 'O';
char currentPlayer;
int difficulty = 1; // 1: Easy, 2: Medium, 3: Hard

void resetboard();
void printboard();
int checkfreespaces();
void playerMove(char);
void computerMove();
void computerMoveMedium();
void computerMoveHard();
int minimax(char board[3][3], int depth, int isMaximizing);
int isMovesLeft(char board[3][3]);
char checkwinner();
void printwinner(char);
void playGamePvP();
void playGamePvC();

int main() {
    int choice;
    srand(time(0));  // Seed the random number generator

    do {
        printf("\n--- TIC-TAC-TOE MENU ---\n");
        printf("1. Play Game\n");
        printf("   a) Player vs Computer\n");
        printf("   b) Player vs Player\n");
        printf("2. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("\nSelect Mode:\n");
                printf("a) Player vs Computer\n");
                printf("b) Player vs Player\n");
                printf("Enter your choice (a/b): ");
                char mode;
                scanf(" %c", &mode);

                if (tolower(mode) == 'a') {
                    playGamePvC();
                } else if (tolower(mode) == 'b') {
                    playGamePvP();
                } else {
                    printf("Invalid option!\n");
                }
                break;
            case 2:
                printf("Exiting... Thanks for playing!\n");
                break;
            default:
                printf("Invalid choice!\n");
                break;
        }
    } while (choice != 2);

    return 0;
}

void resetboard() {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            board[i][j] = ' ';
        }
    }
}

void printboard() {
    printf("\n");
    printf("  1   2   3 \n");
    printf("1 %c | %c | %c \n", board[0][0], board[0][1], board[0][2]);
    printf(" ---|---|---\n");
    printf("2 %c | %c | %c \n", board[1][0], board[1][1], board[1][2]);
    printf(" ---|---|---\n");
    printf("3 %c | %c | %c \n", board[2][0], board[2][1], board[2][2]);
    printf("\n");
}

int checkfreespaces() {
    int freespaces = 9;

    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (board[i][j] != ' ') {
                freespaces--;
            }
        }
    }
    return freespaces;
}

void playerMove(char player) {
    int x, y;

    do {
        printf("Player %c, enter row #(1-3): ", player);
        scanf("%d", &x);
        printf("Player %c, enter column #(1-3): ", player);
        scanf("%d", &y);

        x--;  // Adjust for 0-based indexing
        y--;

        if (x < 0 || x >= 3 || y < 0 || y >= 3 || board[x][y] != ' ') {
            printf("Invalid Move! Please try again.\n");
        } else {
            board[x][y] = player;
            break;
        }
    } while (1);
}

void computerMove() {
    if (difficulty == 1) {
        int x, y;
        if (checkfreespaces() > 0) {
            do {
                x = rand() % 3;
                y = rand() % 3;
            } while (board[x][y] != ' ');

            board[x][y] = player2;
        }
    } else if (difficulty == 2) {
        computerMoveMedium();
    } else if (difficulty == 3) {
        computerMoveHard();
    }
}

void computerMoveMedium() {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (board[i][j] == ' ') {
                // Test move
                board[i][j] = player2;
                if (checkwinner() == player2) {
                    return;
                }
                board[i][j] = ' ';
            }
        }
    }
    computerMove(); // Default to random move if no winning move is found
}

void computerMoveHard() {
    int bestScore = -1000;
    int moveX = -1, moveY = -1;

    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (board[i][j] == ' ') {
                // Try the move
                board[i][j] = player2;
                int score = minimax(board, 0, 0);
                // Undo the move
                board[i][j] = ' ';
                if (score > bestScore) {
                    bestScore = score;
                    moveX = i;
                    moveY = j;
                }
            }
        }
    }

    if (moveX != -1 && moveY != -1) {
        board[moveX][moveY] = player2;
    }
}

int minimax(char board[3][3], int depth, int isMaximizing) {
    char result = checkwinner();
    if (result == player2) {
        return 10 - depth;
    } else if (result == player1) {
        return depth - 10;
    } else if (!isMovesLeft(board)) {
        return 0;
    }

    if (isMaximizing) {
        int bestScore = -1000;
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (board[i][j] == ' ') {
                    board[i][j] = player2;
                    bestScore = fmax(bestScore, minimax(board, depth + 1, 0));
                    board[i][j] = ' ';
                }
            }
        }
        return bestScore;
    } else {
        int bestScore = 1000;
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (board[i][j] == ' ') {
                    board[i][j] = player1;
                    bestScore = fmin(bestScore, minimax(board, depth + 1, 1));
                    board[i][j] = ' ';
                }
            }
        }
        return bestScore;
    }
}

int isMovesLeft(char board[3][3]) {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (board[i][j] == ' ') {
                return 1;
            }
        }
    }
    return 0;
}

char checkwinner() {
    // Check rows
    for (int i = 0; i < 3; i++) {
        if (board[i][0] == board[i][1] && board[i][0] == board[i][2] && board[i][0] != ' ') {
            return board[i][0];
        }
    }
    // Check columns
    for (int i = 0; i < 3; i++) {
        if (board[0][i] == board[1][i] && board[0][i] == board[2][i] && board[0][i] != ' ') {
        return board[0][i];
    }
}
    // Check diagonals
    if (board[0][0] == board[1][1] && board[0][0] == board[2][2] && board[0][0] != ' ') {
        return board[0][0];
    }
    if (board[0][2] == board[1][1] && board[0][2] == board[2][0] && board[0][2] != ' ') {
        return board[0][2];
    }

    return ' ';
}

void printwinner(char winner) {
    if (winner == player1) {
        printf("Player 1 (X) WINS!\n");
    } else if (winner == player2) {
        printf("Player 2 (O) WINS!\n");
    } else {
        printf("IT'S A DRAW!\n");
    }
}

void playGamePvP() {
    char winner = ' ';
    resetboard();

    while (winner == ' ' && checkfreespaces() != 0) {
        printboard();
        playerMove(player1);
        winner = checkwinner();
        if (winner != ' ' || checkfreespaces() == 0) {
            break;
        }

        printboard();
        playerMove(player2);
        winner = checkwinner();
        if (winner != ' ' || checkfreespaces() == 0) {
            break;
        }
    }

    printboard();
    printwinner(winner);
}

void playGamePvC() {
    printf("\nSelect Difficulty Level:\n");
    printf("1. Easy\n");
    printf("2. Medium\n");
    printf("3. Hard\n");
    printf("Enter your choice: ");
    scanf("%d", &difficulty);

    if (difficulty < 1 || difficulty > 3) {
        printf("Invalid choice! Setting to Easy by default.\n");
        difficulty = 1;
    }

    char winner = ' ';
    resetboard();

    while (winner == ' ' && checkfreespaces() != 0) {
        printboard();
        playerMove(player1);
        winner = checkwinner();
        if (winner != ' ' || checkfreespaces() == 0) {
            break;
        }

        computerMove();
        winner = checkwinner();
        if (winner != ' ' || checkfreespaces() == 0) {
            break;
        }
    }

    printboard();
    printwinner(winner);
}
