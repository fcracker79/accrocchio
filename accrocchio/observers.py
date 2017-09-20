import abc


class AccrocchioObserver(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def on_accrocchio(self):
        pass  # pragma: no cover

    @abc.abstractmethod
    def reset(self):
        pass  # pragma: no cover


ACCROCCHIO_OBSERVERS = []


def add_accrocchio_observer(observer: AccrocchioObserver) -> None:
    ACCROCCHIO_OBSERVERS.append(observer)


def reset():
    for x in ACCROCCHIO_OBSERVERS:
        x.reset()
