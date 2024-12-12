import matplotlib.pyplot as plt

def visualize_times(times):
    labels = times.keys()
    durations = times.values()

    # Pie
    plt.figure(figsize=(8, 6))
    plt.pie(durations, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("Porovnanie časov spracovania")
    plt.show()

def visualize_bar_chart(times):
    labels = list(times.keys())
    durations = list(times.values())

    # Basic graph just for my better understanding
    plt.figure(figsize=(10, 6))
    plt.bar(labels, durations, color='skyblue')
    plt.xlabel("Algoritmus")
    plt.ylabel("Čas (sekundy)")
    plt.title("Porovnanie časov spracovania")
    plt.show()
