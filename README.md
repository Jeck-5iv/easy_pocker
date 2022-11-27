# Автопокер

### Инструкция:

Для игры необходим python3 версии 3.8 или выше. 

Чтобы запустить игру необходимо в папке с игрой питоном запустить файл pocker.py:
```
python3 pocker.py
```
### Правила:
Между собой автоматически играют 2 ИИ игрока. Есть стандартная колода из 52 карт.
Каждый из них получает какие-то 5 карт из колоды и тот, у кого комбинация карт выше, побеждает.
Старшинство комбинации определяется по обычным покерным 
[правилам](https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D0%BA%D0%B5%D1%80#%D0%9A%D0%BE%D0%BC%D0%B1%D0%B8%D0%BD%D0%B0%D1%86%D0%B8%D0%B8_%D0%BA%D0%B0%D1%80%D1%82_%D0%B2_%D0%BF%D0%BE%D0%BA%D0%B5%D1%80%D0%B5).

### Примеры работы программы:
```
1st player's hand:  [8 of Clubs, 2 of Clubs, 2 of Diamonds, King of Spades, King of Diamonds]
2nd player's hand:  [Queen of Hearts, 5 of Diamonds, Queen of Diamonds, 7 of Hearts, 4 of Clubs]

1st player's top combination:  TwoPairs [King of Spades, King of Diamonds, 2 of Diamonds, 2 of Clubs, 8 of Clubs]
2nd player's top combination:  Pair [Queen of Diamonds, Queen of Hearts, 7 of Hearts, 5 of Diamonds, 4 of Clubs]

Player1 won!
```
```
1st player's hand:  [Ace of Spades, Jack of Diamonds, King of Clubs, Queen of Hearts, 10 of Spades]
2nd player's hand:  [7 of Hearts, 3 of Clubs, Ace of Clubs, Jack of Hearts, 7 of Diamonds]

1st player's top combination:  Straight [Ace of Spades, King of Clubs, Queen of Hearts, Jack of Diamonds, 10 of Spades]
2nd player's top combination:  Pair [7 of Diamonds, 7 of Hearts, Ace of Clubs, Jack of Hearts, 3 of Clubs]

Player1 won!
```
```
1st player's hand:  [7 of Diamonds, 9 of Clubs, 2 of Clubs, 8 of Clubs, King of Clubs]
2nd player's hand:  [King of Diamonds, 10 of Clubs, Jack of Spades, Ace of Clubs, 5 of Diamonds]

1st player's top combination:  HighCard [King of Clubs, 9 of Clubs, 8 of Clubs, 7 of Diamonds, 2 of Clubs]
2nd player's top combination:  HighCard [Ace of Clubs, King of Diamonds, Jack of Spades, 10 of Clubs, 5 of Diamonds]

Player2 won!
```

### Планы на будущее:
1) Превратить автопокер в нормальный покер (пока основная проблема - это ИИ).
2) Добавить графический интерфейс.
3) Сделать веб-приложение для игры в покер.
