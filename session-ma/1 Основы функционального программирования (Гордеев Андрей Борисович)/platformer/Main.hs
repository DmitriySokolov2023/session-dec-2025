import Data.List (intercalate)
import Data.Char (isDigit)

-- Тип для ячейки доски
data Cell = X | O | Empty deriving (Eq)

instance Show Cell where
    show X = "X"
    show O = "O"
    show Empty = " "

-- Тип для игрока
data Player = PlayerX | PlayerO deriving (Eq)

type Board = [Cell]

-- Начальная доска
initialBoard :: Board
initialBoard = replicate 9 Empty

-- Показать доску в консоли
displayBoard :: Board -> IO ()
displayBoard board = do
    putStrLn ""
    putStrLn "   0 | 1 | 2"
    putStrLn "   ---------"
    putStrLn $ "0  " ++ show (board !! 0) ++ " | " ++ show (board !! 1) ++ " | " ++ show (board !! 2)
    putStrLn "   ---------"
    putStrLn $ "1  " ++ show (board !! 3) ++ " | " ++ show (board !! 4) ++ " | " ++ show (board !! 5)
    putStrLn "   ---------"
    putStrLn $ "2  " ++ show (board !! 6) ++ " | " ++ show (board !! 7) ++ " | " ++ show (board !! 8)
    putStrLn ""

-- Проверить выигрыш
checkWin :: Cell -> Board -> Bool
checkWin cell board = any (all (== cell)) lines
  where
    lines = [ [board !! 0, board !! 1, board !! 2]  -- горизонтали
            , [board !! 3, board !! 4, board !! 5]
            , [board !! 6, board !! 7, board !! 8]
            , [board !! 0, board !! 3, board !! 6]  -- вертикали
            , [board !! 1, board !! 4, board !! 7]
            , [board !! 2, board !! 5, board !! 8]
            , [board !! 0, board !! 4, board !! 8]  -- диагонали
            , [board !! 2, board !! 4, board !! 6]
            ]

-- Проверить ничью
isBoardFull :: Board -> Bool
isBoardFull = all (/= Empty)

-- Получить ход от игрока
getMove :: Player -> IO Int
getMove player = do
    putStr $ "Игрок " ++ (if player == PlayerX then "X" else "O") ++ ", введите номер ячейки (0-8): "
    input <- getLine
    if null input || not (all isDigit input)
        then do
            putStrLn "Некорректный ввод! Введите число от 0 до 8."
            getMove player
        else
            let pos = read input :: Int
            in if pos < 0 || pos > 8
               then do
                   putStrLn "Некорректная позиция! Введите число от 0 до 8."
                   getMove player
               else return pos

-- Сделать ход
makeMove :: Board -> Int -> Cell -> Maybe Board
makeMove board pos cell
    | pos < 0 || pos > 8 = Nothing
    | board !! pos /= Empty = Nothing
    | otherwise = Just (take pos board ++ [cell] ++ drop (pos + 1) board)

-- Главный игровой цикл
gameLoop :: Board -> Player -> IO ()
gameLoop board player = do
    displayBoard board
    
    -- Проверить выигрыш предыдущего игрока
    let opponent = if player == PlayerX then PlayerO else PlayerX
        opponentCell = if opponent == PlayerX then X else O
    
    if checkWin opponentCell board
        then putStrLn $ "Игрок " ++ (if opponent == PlayerX then "X" else "O") ++ " выиграл!"
        else if isBoardFull board
             then putStrLn "Ничья!"
             else do
                 -- Получить ход текущего игрока
                 pos <- getMove player
                 
                 let currentCell = if player == PlayerX then X else O
                 case makeMove board pos currentCell of
                     Nothing -> do
                         putStrLn "Эта ячейка уже занята! Попробуйте снова."
                         gameLoop board player
                     Just newBoard -> do
                         -- Переключиться на другого игрока
                         let nextPlayer = if player == PlayerX then PlayerO else PlayerX
                         gameLoop newBoard nextPlayer

-- Главная функция
main :: IO ()
main = do
    putStrLn "Добро пожаловать в игру Крестики-Нолики!"
    putStrLn "Два игрока играют по очереди."
    putStrLn "Ячейки нумеруются от 0 до 8:"
    putStrLn "  0 1 2"
    putStrLn "  3 4 5"
    putStrLn "  6 7 8"
    gameLoop initialBoard PlayerX