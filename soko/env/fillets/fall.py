
UP_SHIFT = (0,-1)

class Landslip:
    def __init__(self, field, models):
        self.field = field
        self.models = models

    def get_falling(self):
        immovable = self._find_immovable()
        stoned = self._calc_stoned_set(immovable)

        return [m for m in self.models if (m not in stoned)]

    def _find_immovable(self):
        immovable = []
        for model in self.models:
            if model.is_immovable():
                immovable.append(model)

        return immovable

    def _calc_stoned_set(self, immovable):
        """Returns models that are immovable or lay directly
        or indirectly on a immovable model.
        """
        stack = immovable[:]
        stoned = set(stack)
        while len(stack) > 0:
            model = stack.pop()
            above = self._get_above_set(model)
            above -= stoned
            for item in above:
                stoned.add(item)
                stack.append(item)

        return stoned

    def _get_above_set(self, model):
        above = self.field.get_resist_set(model, UP_SHIFT)
        above.discard(self.field.border)
        return above

