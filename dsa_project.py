import random

# Constants given:
p_in = 0.3           # Probability that customers may enter the market
N = 10               # Number of customers to enter the market
T1, T2 = 60, 300     # Number of seconds each customer will stay
S1, S2 = 10, 60      # Number of seconds the casher takes to process the checkout
phi = 0.1           
rho = 0.005
P1, P2 = 100, 200         # Number of seconds of each customer's patience
L = 5                     # Supermarket Loss
simulation_duration = 10  # Desired duration of the simulation (in seconds)

# Function to run a single simulation
def run_simulation(M):
    customers = []
    cashiers = [0] * M  # Initialize cashiers' working time, if M = 5 then cashiers = [0,0,0,0,0]
    profit = 0

    for time in range(simulation_duration):
        # Customers entering the market
        # random.random() = a random floating-point number between 0 and 1 
        # If this condition is met, it means customers are entering the market
        if random.random() < p_in:
            num_customers = random.randint(0, N) # Randomly get number of customers entering, between 0 and N.
            for _ in range(num_customers):
                # Each customer, random shopping duration within range (T1, T2)
                customers.append(random.randint(T1, T2))

        # Customers choosing cashiers and waiting
        # For each customer in list, find cashier with least working time
        for customer in customers:
            chosen_cashier = cashiers.index(min(cashiers))
            cashiers[chosen_cashier] += customer # Add the customer's shopping time to the chosen cashier

        # Cashiers processing checkout for customers
        for i in range(M):
            if cashiers[i] > 0:
                # Calculate how much time the cashier spends processing this customer
                cashiers[i] = max(0, cashiers[i] - random.randint(S1, S2))
                # Update the profit based on the processing time and the customer's shopping time
                profit += phi * min(cashiers[i], customer)
                # Reduce the remaining customer's shopping time based on processing time
                customer -= min(cashiers[i], customer)
        # Remove customers who have finished shopping
        customers = [customer for customer in customers if customer > 0]

        # Check customer patience and remove if exceeded
        customers = [customer for customer in customers if random.randint(P1, P2) > 0]

    # returning the total profit earned during the simulation
    return profit

# Optimization process to get the optimal value of M that leads to the maximum average profit
best_profit = 0
best_M = 1

for M in range(1, 21):  # Testing different values of M (from 1 to 20)
    total_profit = 0
    for _ in range(10):  # Running multiple simulations for each M, here I am running 10 simulations
        total_profit += run_simulation(M)
    avg_profit = total_profit / 10
    if avg_profit > best_profit:
        best_profit = avg_profit
        best_M = M

print(f"Optimal number of cashiers (M) for maximum profit: {best_M}")
print(f"Maximum profit: {best_profit}")
