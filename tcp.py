import socket

def solve_sudoku(sudoku):
    def is_valid_move(board, row, col, num):
        if num in board[row]:
            return False

        if num in [board[i][col] for i in range(9)]:
            return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False
        return True

    def solve(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid_move(board, row, col, num):
                            board[row][col] = num
                            if solve(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    solved_sudoku = [list(row) for row in sudoku]  
    if solve(solved_sudoku):
        return solved_sudoku
    else:
        return None

def parse_sudoku_string(sudoku_str):
    start_index = sudoku_str.find("[[")
    end_index = sudoku_str.find("]]")
    if start_index != -1 and end_index != -1:
        sudoku_data = sudoku_str[start_index:end_index + 2]  
        sudoku = eval(sudoku_data)  
        return sudoku
    else:
        return None


def main():
    host = "34.131.40.17" 
    port = 12345  

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Receive the Sudoku puzzle from the server
    sudoku_str = client_socket.recv(4096).decode("utf-8")
    sudoku_str = client_socket.recv(4096).decode("utf-8")
    count=0
    # print(sudoku_str)
    while(True):
        print(count)
        count=count+1
        sudoku=parse_sudoku_string(sudoku_str)
        sudoku=solve_sudoku(sudoku)
        # print(type(sudoku))
        # print(sudoku)
        sudoku_str=str(sudoku)
        # print(sudoku_str)
        client_socket.send(sudoku_str.encode("utf-8"))
        sudoku_str = client_socket.recv(4096).decode("utf-8")
        print(sudoku_str+"\n")
        sudoku_str = client_socket.recv(4096).decode("utf-8")
        print(sudoku_str+"\n")


    client_socket.close()

if __name__ == "__main__":
    main()
