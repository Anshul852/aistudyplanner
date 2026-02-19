import random


class GeneticSyllabusOptimizer:
    def __init__(self, population_size=50, mutation_rate=0.15):
        self.pop_size = max(2, int(population_size))
        self.mutation_rate = max(0.0, min(1.0, float(mutation_rate)))
        self.generations = 100

        self.topics = []
        self.days = 1
        self.velocity = "Medium"

        # Energy caps: Daily "Weight" limit for the student
        self.caps = {"Fast": 10, "Medium": 6, "Slow": 3}

    def _create_chromosome(self):
        """Creates a random schedule: [ [Day1_Topics], [Day2_Topics]... ]"""
        schedule = [[] for _ in range(self.days)]
        for topic in self.topics:
            target_day = random.randint(0, self.days - 1)
            schedule[target_day].append(topic)
        return schedule

    def calculate_fitness(self, chromosome):
        """Scores the schedule. Higher = Less stress & Better coverage."""
        score = 100.0
        daily_cap = self.caps.get(self.velocity, 6)

        covered_ids = set()
        for day_plan in chromosome:
            daily_weight = sum(t.get("weight", 1) for t in day_plan)

            # Penalty 1: Burnout (Over the daily limit)
            if daily_weight > daily_cap:
                score -= (daily_weight - daily_cap) * 10

            # Penalty 2: Inconsistency (Empty days followed by heavy days)
            if daily_weight == 0:
                score -= 5

            for t in day_plan:
                covered_ids.add(t["id"])

        # Penalty 3: Missing Topics (The ultimate sin)
        missing_count = len(self.topics) - len(covered_ids)
        score -= missing_count * 50

        return max(0, score)

    def crossover(self, parent1, parent2):
        """Mixes two schedules to create a child."""
        mid = self.days // 2
        return parent1[:mid] + parent2[mid:]

    def mutate(self, chromosome):
        """Moves one random topic to a different day to find better paths."""
        new_chrom = [list(day) for day in chromosome]
        non_empty_days = [i for i, day in enumerate(new_chrom) if day]

        if non_empty_days:
            from_day = random.choice(non_empty_days)
            to_day = random.randint(0, self.days - 1)

            topic = new_chrom[from_day].pop(
                random.randint(0, len(new_chrom[from_day]) - 1)
            )
            new_chrom[to_day].append(topic)

        return new_chrom

    def evolve(self):
        """Evolutionary search loop."""
        population = [self._create_chromosome() for _ in range(self.pop_size)]

        for _ in range(self.generations):
            population = sorted(
                population, key=lambda x: self.calculate_fitness(x), reverse=True
            )

            # Keep the top 10% with a minimum elite set of 2.
            elite_count = max(2, self.pop_size // 10)
            next_gen = population[:elite_count]

            pool = population[: max(4, self.pop_size // 2)]
            while len(next_gen) < self.pop_size:
                p1, p2 = random.sample(pool, 2)
                child = self.crossover(p1, p2)

                if random.random() < self.mutation_rate:
                    child = self.mutate(child)

                next_gen.append(child)

            population = next_gen

        population = sorted(population, key=self.calculate_fitness, reverse=True)
        return population[0]

    def solve(self, topics, days, velocity="Medium"):
        self.topics = topics or []
        self.days = max(1, int(days))
        self.velocity = velocity

        if not self.topics:
            return [[] for _ in range(self.days)]

        return self.evolve()
