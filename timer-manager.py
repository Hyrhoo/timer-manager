import time
from typing import Callable


class Timer:
    """
    Timer class represents a timer that can be started, stopped, and reset.
    """

    def __init__(self, activation_time: float=None, *, call_back: Callable=None) -> None:
        """
        Initialize a Timer object.

        Args:
            activation_time (float or None): The target time for the timer to be considered activated.
                If None, the timer will not be activated based on time.
            call_back (Callable): The function to call when the timer is activated.

        Attributes:
            target_time (float or None): The target time for the timer to be considered activated.
            start_time (float or None): The start time of the timer.
            time_spend (float): The accumulated time spent on the timer.
            call_back (Callable): The function to call when the timer is activated.
        """
        self.target_time = activation_time
        self.start_time = None
        self.time_spend = 0.0
        self.call_back = call_back

    def __repr__(self) -> str:
        """
        Return a string representation of the Timer object.

        Returns:
            str: The string representation of the Timer object.
        """
        call_back_name = self.call_back.__name__ if callable(self.call_back) else self.call_back
        return f"Timer(time_spend={self.get_time_spend()}, activation_time={self.target_time}, call_back={call_back_name})"

    def get_time_spend(self) -> float:
        """
        Get the total time spent on the timer.

        Returns:
            float: The total time spent on the timer.
        """
        if self.start_time is None:
            return self.time_spend
        return self.time_spend + time.time() - self.start_time
    
    def update(self) -> None:
        """
        Update the timer.
        """
        if self.is_activated():
            if callable(self.call_back):
                self.call_back()

    def start(self) -> None:
        """
        Start the timer.
        """
        if self.start_time is None:
            self.start_time = time.time()

    def stop(self) -> None:
        """
        Stop the timer.
        """
        if self.start_time is not None:
            self.time_spend = self.get_time_spend()
            self.start_time = None
        else:
            raise ValueError("Timer is not running.")

    def reset(self) -> None:
        """
        Reset the timer.
        """
        self.start_time = None
        self.time_spend = 0.0

    def is_activated(self, reset: bool=False) -> bool:
        """
        Check if the timer is activated.

        Args:
            reset (bool): Reset the timer if it is activated
        
        Returns:
            bool: True if the timer is activated, False otherwise.
        """
        if self.target_time and self.get_time_spend() >= self.target_time:
            if reset:
                self.reset()
                self.start()
            return True
        return False



class Timer_Manager:
    """
    Timer_Manager class manages a collection of timers.
    """

    def __init__(self) -> None:
        """
        Initialize a Timer_Manager object.

        Attributes:
            __timers (dict): A dictionary to store timers.
        """
        self.__timers = {}

    def __getattr__(self, name: str) -> Timer:
        """
        Get the timer object by its name.

        Args:
            name (str): The name of the timer.

        Returns:
            Timer: The Timer object.

        Raises:
            AttributeError: If the timer with the given name does not exist.
        """
        timer = self.__timers.get(name)
        if timer:
            return timer
        else:
            raise AttributeError(f"Timer '{name}' does not exist.")

    def __setattr__(self, name: str, value: Timer) -> None:
        """
        Set a timer object.

        Args:
            name (str): The name of the timer.
            value (Timer): The Timer object to be assigned.

        Raises:
            TypeError: If the value assigned is not a Timer object.
        """
        if isinstance(value, Timer):
            self.__timers[name] = value
        elif name == "_Timer_Manager__timers":
            super().__setattr__(name, value)
        else:
            raise TypeError(f"Inappropriate type for assignment: '{type(value).__name__}'.")

    def __delattr__(self, name: str) -> None:
        """
        Delete a timer.

        Args:
            name (str): The name of the timer.

        Raises:
            AttributeError: If the timer with the given name does not exist.
        """
        if name in self.__timers:
            del self.__timers[name]
        else:
            raise AttributeError(f"Timer '{name}' does not exist.")
    
    def __len__(self):
        return len(self.__timers)

    def __repr__(self) -> str:
        """
        Return a string representation of the Timer_Manager object.

        Returns:
            str: The string representation of the Timer_Manager object.
        """
        timer_list = ", ".join(self.__timers.keys())
        return f"Timer_Manager({timer_list})"

    def update(self) -> None:
        """
        Update all timers.
        """
        any(map(lambda x: x.update(), self.__timers.values()))
    
    def start_all(self) -> None:
        """
        Start all timers.
        """
        any(map(lambda x: x.start(), self.__timers.values()))

    def stop_all(self) -> None:
        """
        Stop all timers.
        """
        any(map(lambda x: x.stop(), self.__timers.values()))

    def reset_all(self) -> None:
        """
        Reset all timers.
        """
        any(map(lambda x: x.reset(), self.__timers.values()))

    def get_activated(self, reset: bool=False) -> list[tuple[str, Timer]]:
        """
        Give a list of tuple containing the name and the timer of all timers that are activated.

        Args:
            reset (bool): Reset the timer

        Returns:
            list (tuple (str, Timer)): list of tuple with all pairs name, Timer
        """
        return list(filter(lambda x: x[1].is_activated(reset), self.__timers.items()))

    def get_all_timers(self) -> list[tuple[str, Timer]]:
        """
        Get a list of tuple (name, timer) for all timers.

        Returns:
            list (tuple (str, Timer)): list of tuple with all pairs name, Timer
        """
        return list(self.__timers.items())






if __name__ == "__main__":
    timer_manager = Timer_Manager()
    timer_manager.timer1 = Timer(5.0)
    timer_manager.timer2 = Timer(3.0)
    timer_manager.timer3 = Timer()
    chronometre = Timer()
    del timer_manager.timer3
    print(timer_manager)

    chronometre.start()
    timer_manager.start_all()
    time.sleep(1)
    
    timer_manager.stop_all()
    timer_manager.timer1.start()
    time.sleep(1)
    
    timer_manager.start_all()
    
    for timer in timer_manager.get_all_timers():
        print(timer)
    
    last_activated = 0.0
    while True:
        timer_manager.update()
        activated = timer_manager.get_activated(True)
        chrono = chronometre.get_time_spend()
        if activated:
            print(activated, chrono)
            if abs(chrono - last_activated) < 0.05:
                break
            last_activated = chrono
        
    
    print(chronometre.get_time_spend())