from .component import Component
from .facet import facet
from .interfaces import SampleInlet

import multiprocessing
import queue


@facet('sample_in', SampleInlet, (('consume_sample', '_handle_put'),))
class AnimationSink(Component):
    def __init__(self, label, xlabel, ylabel, ymin, ymax):
        super().__init__()

        self.queue = multiprocessing.Queue()

        self.maxsamples = 40
        self.server = multiprocessing.Process(
            target=self._do_server, 
            kwargs=dict(label=label, 
                        xlabel=xlabel, 
                        ylabel=ylabel, 
                        ymin=ymin, 
                        ymax=ymax,
                        )
        )
        self.server.start()

    async def _handle_put(self, sample):
        # MIGHT BLOCK! multiprocessing.Queue is not awaitable. should
        # fix that.
        self.queue.put(sample)

    def _do_server(self, label, xlabel, ylabel, ymin, ymax):
        # pull in heavy stuff in the child only
        import matplotlib.pyplot as plt
        import matplotlib.animation as animation
        import matplotlib.dates as md

        samples = []

        fig, ax = plt.subplots()
        curve = ax.plot([], [], label=label)[0]
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_ylim([ymin, ymax])
        ax.legend()

        # every 'interval' milliseconds: 
        #
        # * read frame from supplied iterable 'frames' -> _read_queue. 
        #   note that _read_queue BLOCKS until real data comes in over the pipe (multiprocessing.queue is a pipe, internally).
        #   this means that the 1 milliseconds is not actually a *polling interval*, 
        #   but only something that matplotlib wants me to supply (@#$%$#@). 
        #   the loop is actually driven by samples coming in over the queue.
        # * for every incoming sample, _update is called, which ... well ... update the plot.
        myanimation = animation.FuncAnimation(
            fig=fig, 
            func=self._update, fargs=(curve, ax, samples), 
            frames=self._read_queue,
            interval=1, 
            cache_frame_data=False,
        )

        # drives the plot's main event/GUI loop. here we sit and block
        plt.show()

    def _read_queue(self):
        while True:
            yield self.queue.get()

    def _update(self, sample, curve, ax, samples):
        if sample is not None:
            samples.append(sample)
            if len(samples) > self.maxsamples:
                samples[:self.maxsamples] = samples[-self.maxsamples:]
                samples[self.maxsamples:] = []

            if len(samples) > 0:
                ax.set_xlim([samples[0].timestamp, samples[-1].timestamp])

            ax.set_xticks([s.timestamp for s in samples], labels=[s.timestamp.strftime('%Y-%m-%d %H-%M-%S.%f') for s in samples], rotation=45)
            curve.set_xdata([s.timestamp for s in samples])
            curve.set_ydata([s.data for s in samples])

        return (curve,)
