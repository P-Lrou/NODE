import threading
import functools
import inspect

class Timer:
    _instance = {}
    _lock = threading.Lock()

    def __init__(self):
        self._timer = None
        self._callbacks = []
        self._results = []
        self._event = threading.Event()
        self._running = False
        self._lock = threading.Lock()

    def start(self, interval, callback, *args, **kwargs):
        with self._lock:
            # Ajouter le callback à la liste
            self._callbacks.append((callback, args, kwargs))
            # Annuler l'ancien timer s'il existe
            if self._timer:
                self._timer.cancel()
            # Démarrer un nouveau timer avec le nouvel intervalle
            self._timer = threading.Timer(interval, self._execute_callbacks)
            self._timer.start()
            self._running = True

    def _execute_callbacks(self):
        with self._lock:
            while self._callbacks:
                callback, args, kwargs = self._callbacks.pop(0)
                # Vérifier si le callback a l'argument is_last
                if not self._callbacks:  # C'est le dernier callback
                    sig = inspect.signature(callback)
                    if 'is_last' in sig.parameters:
                        kwargs['is_last'] = True
                result = callback(*args, **kwargs)
                self._results.append(result)
            # Signaler que toutes les callbacks ont été exécutées
            self._event.set()
            self._running = False

    def cancel(self):
        with self._lock:
            if self._timer:
                self._timer.cancel()
                self._timer = None
            self._event.set()
            self._running = False

    def get_result(self):
        self._event.wait()  # Wait until all callbacks are executed
        with self._lock:
            results = self._results.copy()
            self._results.clear()
            self._event.clear()  # Reset the event for future use
            return results

    def is_running(self):
        with self._lock:
            return self._running

    def pop_callback(self, callback, *args, **kwargs):
        with self._lock:
            for i, (cb, cb_args, cb_kwargs) in enumerate(self._callbacks):
                if cb == callback and cb_args == args and cb_kwargs == kwargs:
                    return self._callbacks.pop(i)
            return None

    @classmethod
    def instance(cls, name: str = "default") -> "Timer":
        if name not in cls._instance:
            cls._instance[name] = cls()
        return cls._instance[name]

# Exemple d'utilisation :
if __name__ == "__main__":
    def my_callback(param1, param2, is_last=False):
        print(f"Le timer est terminé avec {param1} et {param2}! is_last={is_last}")
        return f"Résultat: {param1}, {param2}, is_last={is_last}"

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

    # Vérifier si le timer est en cours d'exécution
    print("Timer is running:", Timer.instance().is_running())

    # Redémarrage du timer avec un nouvel intervalle et de nouveaux paramètres
    Timer.instance().start(3, my_callback, "nouveau paramètre 1", "nouveau paramètre 2")
    Timer.instance().start(2, another_callback, "autre paramètre unique")

    # Pop une callback spécifique
    popped_callback = Timer.instance().pop_callback(my_callback, "nouveau paramètre 1", "nouveau paramètre 2")
    print(f"Popped callback: {popped_callback}")

    # Vérifier si le timer est en cours d'exécution
    print("Timer is running:", Timer.instance().is_running())

    # Accéder au résultat de la callback (bloquant jusqu'à ce que le résultat soit disponible)
    results = Timer.instance().get_result()
    print(results)

    # Vérifier si le timer est en cours d'exécution
    print("Timer is running:", Timer.instance().is_running())
