EMPTY_LINE = '\n'

class Food:
    def __init__(self, calories: int) -> None:
        self.calories = calories

    def get_calories(self) -> int:
        return self.calories

class Elf:
    def __init__(self) -> None:
        self.foods = []

    def add_food(self, food: Food) -> None:
        self.foods.append(food)

    def get_total_food_calories(self):
        return sum(food.get_calories() for food in self.foods)

class Solver:
    def get_calories(self):
        list_of_elves: list[Elf] = []
        with open('input1.txt') as f:
            current_elf = None
            for line in f:
                if line == EMPTY_LINE and current_elf:
                    list_of_elves.append(current_elf)
                    current_elf = None
                else:
                    if not current_elf:
                        current_elf = Elf()
                    food = Food(int(line.strip()))
                    current_elf.add_food(food)
        totals = [elf.get_total_food_calories() for elf in list_of_elves]
        return sorted(totals)

solver = Solver()
print(solver.get_calories()[-1])
print(sum(solver.get_calories()[-3:]))
