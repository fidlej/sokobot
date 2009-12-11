
import heapq

class PriorityQueue(object):
    """A priority queue that supports changes
    in the node priorities.
    """
    def __init__(self, hashkey):
        self.opened = {}
        self.queue = []
        self.extract_key = hashkey

    def pop_smallest(self):
        """Extracts the smallest node from the queue.
        The nodes are compared by thier natural order.
        """
        while True:
            smallest = heapq.heappop(self.queue)
            key = self.extract_key(smallest)
            if key in self.opened:
                break

        del self.opened[key]
        return smallest

    def schedule(self, node):
        """Schedules or reschedules a node.
        The node is rescheduled if its value is lower
        than a previous node with the same key.
        """
        key = self.extract_key(node)
        old_item = self.opened.get(key)
        if old_item is not None and old_item <= node:
            return

        self.opened[key] = node
        heapq.heappush(self.queue, node)

    def is_empty(self):
        return len(self.opened) == 0

