import threading
import functools
import inspect

class Timer:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self._timers = []
        self._callbacks = []
        self._results = []
        self._event = threading.Event()
        self._lock = threading.Lock()

    def start(self, interval, callback, *args, **kwargs):
        with self._lock:
            # Ajouter le callback à la liste
            self._callbacks.append((callback, args, kwargs))
            # Démarrer ou redémarrer le timer avec le nouvel intervalle
            timer = threading.Timer(interval, self._execute_callbacks)
            self._timers.append(timer)
            timer.start()

    def _execute_callbacks(self):
        with self._lock:
            while self._callbacks:
                callback, args, kwargs = self._callbacks.pop(0)
                # Vérifier si le callback a l'argument is_last
                if self._callbacks == []:  # C'est le dernier callback
                    sig = inspect.signature(callback)
                    if 'is_last' in sig.parameters:
                        kwargs['is_last'] = True
                result = callback(*args, **kwargs)
                self._results.append(result)
            # Signaler que toutes les callbacks ont été exécutées
            self._event.set()

    def cancel(self):
        with self._lock:
            for timer in self._timers:
                timer.cancel()
            self._timers = []
            self._event.set()

    def get_result(self):
        self._event.wait()  # Wait until all callbacks are executed
        with self._lock:
            results = self._results.copy()
            self._results.clear()
            self._event.clear()  # Reset the event for future use
            return results

    @classmethod
    def instance(cls) -> "Timer":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

# Exemple d'utilisation :
if __name__ == "__main__":
    def my_callback(param1, param2):
        print(f"Le timer est terminé avec {param1} et {param2}!")
        return f"Résultat: {param1}, {param2}"

    def another_callback(param, is_last=False):
        print(f"Another callback executed with {param}! is_last={is_last}")
        return f"Another result: {param}, is_last={is_last}"

    # Démarrage du timer avec un intervalle de 2 secondes et des paramètres pour la callback
    Timer.instance().start(2, my_callback, "paramètre 1", "paramètre 2")

    # Démarrage du timer avec un intervalle de 1 seconde et des paramètres pour une autre callback
    Timer.instance().start(1, another_callback, "paramètre unique")

    # Accéder au résultat de la callback (bloquant jusqu'à ce que le résultat soit disponible)
    results = Timer.instance().get_result()
    print(results)

    # Redémarrage du timer avec un nouvel intervalle et de nouveaux paramètres
    Timer.instance().start(3, another_callback, "nouveau paramètre 1")
    Timer.instance().start(2, my_callback, "autre paramètre unique", "autre paramètre unique 2")

    # Accéder au résultat de la callback (bloquant jusqu'à ce que le résultat soit disponible)
    results = Timer.instance().get_result()
    print(results)
