import abc


class AccrocchioObserver(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def on_accrocchio(self):
        pass  # pragma: no cover

    @abc.abstractmethod
    def reset(self):
        pass  # pragma: no cover


ACCROCCHIO_OBSERVERS = {}


def add_accrocchio_observer(observer: AccrocchioObserver, accrocchio_name: str='accrocchio') -> None:
    observers = ACCROCCHIO_OBSERVERS.get(accrocchio_name)
    if not observers:
        observers = []
        ACCROCCHIO_OBSERVERS[accrocchio_name] = observers
    observers.append(observer)


def reset(accrocchio_name: str='accrocchio'):
    for k, x in ACCROCCHIO_OBSERVERS.items():
        if k != accrocchio_name and accrocchio_name != 'accrocchio':
            continue
        for y in x:
            y.reset()
